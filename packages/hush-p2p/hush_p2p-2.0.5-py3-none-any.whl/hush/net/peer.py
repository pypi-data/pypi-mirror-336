import socket
import threading
import json
import os
from hush.utils.settings import load_settings
from hush.crypto.crypto import encrypt_message, decrypt_message
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import sys  # Add this at the top if not already imported


class Peer:
    def __init__(self, username, private_key, public_key, listen_port=None):
        self.username = username
        self.private_key = private_key
        self.public_key = public_key
        self.settings = load_settings()
        self.public_keys = {}  # ip -> public_key
        self.aliases = {}      # alias -> ip
        self.keys_sent = set()  # ✅ Track IPs we've sent our public key to
        self.last_sender = None

        self.listen_port = listen_port or self.settings.get("LISTEN_PORT", 5001)
        self.broadcast_addr = self.settings.get("BROADCAST_ADDR", "255.255.255.255")
        self.broadcast_port = self.settings.get("BROADCAST_PORT", 5001)
        self.file_port = self.settings.get("FILE_PORT", self.listen_port + 1)
        
        self.keys_file = os.path.expanduser(f"~/.hush/{self.username}_known_keys.json")
        os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)

        self._load_keys_from_disk()

        print(f"🔧 Debug: Initialized Peer '{self.username}' on port {self.listen_port}")
        print(f"🔧 Debug: Listening for key exchanges and messages...")

    def _load_keys_from_disk(self):
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, "r") as f:
                    raw_keys = json.load(f)
                    for alias, record in raw_keys.items():
                        ip = record["ip"]
                        key = load_pem_public_key(record["key"].encode())
                        self.public_keys[ip] = key
                        self.aliases[alias] = ip
                print(f"💾 Loaded {len(self.public_keys)} keys from disk.")
            except Exception as e:
                print(f"⚠️ Failed to load keys from disk: {e}")

    def _save_keys_to_disk(self):
        try:
            to_save = {}
            for alias, ip in self.aliases.items():
                key = self.public_keys.get(ip)
                if key:
                    pem = key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ).decode()
                    to_save[alias] = {"ip": ip, "key": pem}
            os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)
            with open(self.keys_file, "w") as f:
                json.dump(to_save, f, indent=2)
            print(f"💾 Saved {len(to_save)} keys to disk.")
        except Exception as e:
            print(f"❌ Failed to save keys: {e}")

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(('', self.listen_port))
        except OSError as e:
            print(f"❌ Failed to bind on port {self.listen_port}: {e}")
            return

        print(f"🟢 Listening for messages on port {self.listen_port}...")

        while True:
            data, addr = s.recvfrom(4096)
            self.last_sender = addr
            print(f"\n📥 Received packet from {addr[0]}:{addr[1]}")

            if self._handle_key_exchange(data, addr):
                print(f"🔧 Debug: Handled key exchange from {addr}")
                continue

            try:
                plaintext = decrypt_message(self.private_key, data)
                print(f"\n🔐 Decrypted from {addr[0]}:{addr[1]}:\n   {plaintext}\n> ", end='')
                self._log_message(addr[0], addr[1], plaintext, protocol="UDP")
            except Exception as e:
                print(f"\n📩 Plaintext from {addr[0]}:{addr[1]} (decryption failed):")
                print(data.decode(errors='ignore'))
                print(f"⚠️ Decryption failed: {str(e)}\n> ", end='')


    def listen_tcp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(('', self.listen_port))
            s.listen()
            print(f"🧲 Listening for TCP messages on port {self.listen_port}...")
        except OSError as e:
            print(f"❌ Failed to bind TCP on port {self.listen_port}: {e}")
            return

        while True:
            conn, addr = s.accept()
            print(f"\n🔌 TCP connection from {addr[0]}:{addr[1]}")
            try:
                data = conn.recv(4096)
                plaintext = decrypt_message(self.private_key, data)
                print(f"🔐 [TCP] Decrypted from {addr[0]}:\n   {plaintext}\n> ", end='')
                self._log_message(addr[0], addr[1], plaintext, protocol="TCP")
            except Exception as e:
                print(f"⚠️ [TCP] Decryption failed from {addr[0]}: {e}")
            finally:
                conn.close()

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.listen_tcp, daemon=True).start()
        self.start_file_receiver()  # ✅ Add this here!
        if sys.stdin.isatty():
            while True:
                try:
                    msg = input("> ").strip()

                    if msg.startswith("/sendkey"):
                        parts = msg.split(" ")
                        if len(parts) != 3:
                            print("⚠️ Usage: /sendkey <ip> <port>")
                            continue
                        ip = parts[1]
                        port = int(parts[2])
                        self.send_public_key(ip, port)

                    elif msg.startswith("/alias"):
                        parts = msg.split(" ")
                        if len(parts) != 4:
                            print("⚠️ Usage: /alias <name> <ip> <port>")
                            continue
                        name, ip, port = parts[1], parts[2], int(parts[3])
                        self.aliases[name] = ip
                        print(f"✅ Alias '{name}' set to {ip}:{port}")

                    elif msg.startswith("/msg"):
                        parts = msg.split(" ", 2)
                        if len(parts) != 3:
                            print("⚠️ Usage: /msg <alias|ip:port> <message>")
                            continue
                        target, message = parts[1], parts[2]
                        if ":" in target:
                            ip, port = target.split(":")
                            self.send_direct(ip, int(port), message)
                        elif target in self.aliases:
                            ip = self.aliases[target]
                            self.send_direct(ip, self.listen_port, message)  # Assuming default port

                    elif msg.startswith("/sendtcp"):
                        parts = msg.split(" ", 3)
                        if len(parts) != 4:
                            print("⚠️ Usage: /sendtcp <ip> <port> <message>")
                            continue
                        ip = parts[1]
                        port = int(parts[2])
                        message = parts[3]
                        self.send_tcp(ip, port, message)

                    elif msg.startswith("/sendfile"):
                        parts = msg.split(" ", 3)
                        if len(parts) != 4:
                            print("⚠️ Usage: /sendfile <ip> <port> <filepath>")
                            continue
                        ip = parts[1]
                        port = int(parts[2])
                        filepath = parts[3]
                        self.send_file(ip, port, filepath)

                    else:
                        self.send_broadcast(msg)

                except KeyboardInterrupt:
                    print("\n👋 Exiting.")
                    break
        else:
            print("🛡️ Running in background (no CLI input)...")
            threading.Event().wait()

    def start_old(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.listen_tcp, daemon=True).start()
        self.start_file_receiver()  # ✅ Add this here!
        while True:
            try:
                msg = input("> ").strip()

                if msg.startswith("/sendkey"):
                    parts = msg.split(" ")
                    if len(parts) != 3:
                        print("⚠️ Usage: /sendkey <ip> <port>")
                        continue
                    ip = parts[1]
                    port = int(parts[2])
                    self.send_public_key(ip, port)

                elif msg.startswith("/alias"):
                    parts = msg.split(" ")
                    if len(parts) != 4:
                        print("⚠️ Usage: /alias <name> <ip> <port>")
                        continue
                    name, ip, port = parts[1], parts[2], int(parts[3])
                    self.aliases[name] = ip
                    print(f"✅ Alias '{name}' set to {ip}:{port}")

                elif msg.startswith("/msg"):
                    parts = msg.split(" ", 2)
                    if len(parts) != 3:
                        print("⚠️ Usage: /msg <alias|ip:port> <message>")
                        continue
                    target, message = parts[1], parts[2]
                    if ":" in target:
                        ip, port = target.split(":")
                        self.send_direct(ip, int(port), message)
                    elif target in self.aliases:
                        ip = self.aliases[target]
                        self.send_direct(ip, self.listen_port, message)  # Assuming default port

                elif msg.startswith("/sendtcp"):
                    parts = msg.split(" ", 3)
                    if len(parts) != 4:
                        print("⚠️ Usage: /sendtcp <ip> <port> <message>")
                        continue
                    ip = parts[1]
                    port = int(parts[2])
                    message = parts[3]
                    self.send_tcp(ip, port, message)                 
              

                elif msg.startswith("/sendfile"):
                    parts = msg.split(" ", 3)
                    if len(parts) != 4:
                        print("⚠️ Usage: /sendfile <ip> <port> <filepath>")
                        continue
                    ip = parts[1]
                    port = int(parts[2])
                    filepath = parts[3]
                    self.send_file(ip, port, filepath)
                #else:
                    #print(f"❌ Unknown peer or alias '{target}'")

                else:
                    self.send_broadcast(msg)

            except KeyboardInterrupt:
                print("\n👋 Exiting.")
                break

    def send_broadcast(self, message):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            msg = f"{self.username}: {message}"
            s.sendto(msg.encode(), (self.broadcast_addr, self.broadcast_port))
            print(f"📡 Broadcasted message: {msg}")
        except Exception as e:
            print(f"❌ Failed to send broadcast: {e}")

    def send_direct(self, ip, port, message):
        key = self.public_keys.get(ip)
        if not key:
            print(f"⚠️ No public key for {ip}. Use /sendkey first.")
            print(f"🔧 Debug: Known public keys: {list(self.public_keys.keys())}")
            return

        try:
            encrypted = encrypt_message(key, f"{self.username}: {message}")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(encrypted, (ip, port))
            print(f"📤 Encrypted message sent to {ip}:{port}:\n   {message}")
        except Exception as e:
            print(f"❌ Failed to send encrypted message to {ip}:{port}: {e}")

    def send_tcp(self, ip, port, message):
        key = self.public_keys.get(ip)
        if not key:
            print(f"⚠️ No public key for {ip}. Use /sendkey first.")
            return

        try:
            encrypted = encrypt_message(key, f"{self.username}: {message}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.sendall(encrypted)
            s.close()
            print(f"📤 [TCP] Encrypted message sent to {ip}:{port}:\n   {message}")
        except Exception as e:
            print(f"❌ Failed to send TCP message to {ip}:{port}: {e}")

    def start_file_receiver(self):
        def handler():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                #s.bind(('', self.listen_port))

                s.bind(('', self.file_port))                
                s.listen()
                print(f"📥 Listening for file transfers on port {self.listen_port}...")
            except Exception as e:
                print(f"❌ Failed to start file receiver: {e}")
                return

            while True:
                conn, addr = s.accept()
                print(f"\n🔌 Incoming file transfer from {addr[0]}")

                try:
                    buffer = b""
                    while b"\n\n" not in buffer:
                        buffer += conn.recv(1024)
                    header, rest = buffer.split(b"\n\n", 1)
                    metadata = json.loads(header.decode())

                    if metadata.get("type") != "file_transfer":
                        print("⚠️ Not a file transfer request. Ignoring.")
                        conn.close()
                        continue

                    filename = metadata["filename"]
                    output_path = os.path.expanduser(f"~/Downloads/hush/{filename}")
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    with open(output_path, "wb") as f:
                        #f.write(decrypt_message(self.private_key, rest))
                        f.write(rest)
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                break
                            #f.write(decrypt_message(self.private_key, chunk))
                            f.write(chunk)

                    print(f"✅ [FILE] Received and saved file to: {output_path}")

                except Exception as e:
                    print(f"❌ File receive error from {addr[0]}: {e}")

                finally:
                    conn.close()

        threading.Thread(target=handler, daemon=True).start()

    def send_file(self, ip, port, filepath):
        if not os.path.isfile(filepath):
            print(f"❌ File not found: {filepath}")
            return

        key = self.public_keys.get(ip)
        if not key:
            print(f"❌ No public key for {ip}. Use /sendkey first.")
            return

        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)

            metadata = {
                "type": "file_transfer",
                "filename": filename,
                "size": filesize,
                "username": self.username
            }
            meta_json = json.dumps(metadata).encode()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(meta_json + b"\n\n")  # metadata block

                with open(filepath, "rb") as f:
                    while chunk := f.read(4096):
                        #encrypted_chunk = encrypt_message(key, chunk)
                        #s.sendall(encrypted_chunk)
                        s.sendall(chunk)
            print(f"📤 [FILE] Encrypted file '{filename}' sent to {ip}:{port}")

        except Exception as e:
            print(f"❌ Failed to send file to {ip}:{port}: {e}")


    def send_public_key_tor(self, ip, port):
        try:
            use_tcp = ".onion" in ip  # 🧠 Automatically use TCP if it's a .onion address

            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            payload = {
                "type": "key_exchange",
                "username": self.username,
                "port": self.listen_port,
                "key": pem
            }

            msg = json.dumps(payload).encode()

            if use_tcp:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.sendall(msg)
                s.close()
                print(f"📡 [TCP] Sent public key to {ip}:{port}")
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(msg, (ip, port))
                print(f"📡 [UDP] Sent public key to {ip}:{port}")

            print(f"ℹ️ Awaiting key exchange response from peer...")
        except Exception as e:
            print(f"❌ Failed to send public key to {ip}:{port}: {e}")



    def send_public_key(self, ip, port):
        try:
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            payload = {
                "type": "key_exchange",
                "username": self.username,
                "port": self.listen_port,
                "key": pem
            }

            msg = json.dumps(payload).encode()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(msg, (ip, port))

            print(f"📡 Sent public key to {ip}:{port}")
            print(f"ℹ️ Awaiting key exchange response from peer...")
        except Exception as e:
            print(f"❌ Failed to send public key to {ip}:{port}: {e}")


    def _handle_key_exchange(self, data, addr):
        sender_ip, sender_port = addr
        print(f"\n🧩 Received potential key exchange packet from {sender_ip}:{sender_port}")

        try:
            try:
                decoded = data.decode()
                print(f"📝 Decoded payload: {decoded}")
            except UnicodeDecodeError:
                print(f"⚠️ Skipped key exchange: Packet from {sender_ip}:{sender_port} was not valid UTF-8.")
                return False

            try:
                payload = json.loads(decoded)
                print(f"🧾 Parsed JSON payload: {payload}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error from {sender_ip}:{sender_port}: {e}")
                return False

            if payload.get("type") != "key_exchange":
                print(f"📛 Packet from {sender_ip}:{sender_port} is not a key exchange. Ignoring.")
                return False

            username = payload.get("username", "Unknown")
            key_data = payload.get("key")

            if not key_data:
                print(f"❌ No key found in payload from {sender_ip}:{sender_port}")
                return False

            try:
                public_key = load_pem_public_key(key_data.encode())
                print(f"🔑 Loaded public key for {username} from {sender_ip}")
            except Exception as e:
                print(f"❌ Failed to load public key from {sender_ip}: {e}")
                return False

            self.public_keys[sender_ip] = public_key
            self.aliases[username] = sender_ip
            self._save_keys_to_disk()

            print(f"✅ Stored public key for '{username}' at {sender_ip}")
            print(f"📚 Current known public keys: {list(self.public_keys.keys())}")
            print(f"📛 Alias map: {self.aliases}")

            # ✅ Auto-respond with your public key (if not already sent)
            if not hasattr(self, 'keys_sent'):
                self.keys_sent = set()

            if sender_ip not in self.keys_sent:
                print(f"📡 Responding with our public key to {sender_ip}:{self.listen_port}")
                self.send_public_key(sender_ip, self.listen_port)
                self.keys_sent.add(sender_ip)
            else:
                print(f"♻️ Already sent our public key to {sender_ip}, skipping response.")

            return True

        except Exception as e:
            print(f"❌ Unexpected error while handling key exchange from {sender_ip}:{sender_port}: {e}")
            return False

    def _log_message(self, sender_ip, sender_port, plaintext, protocol="UDP"):
        log_dir = os.path.expanduser("~/.hush/logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"{self.username}_messages.log")
        with open(log_path, "a") as f:
            f.write(f"[{protocol}] {sender_ip}:{sender_port} -> {self.username}: {plaintext}\n")
