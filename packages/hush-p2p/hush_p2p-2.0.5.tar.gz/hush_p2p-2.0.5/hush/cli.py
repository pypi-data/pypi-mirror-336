import click
import os
from cryptography.hazmat.primitives import serialization
from hush.crypto.crypto import generate_keys
from hush.net.peer import Peer

@click.group()
@click.option('--username', default="CLI", help="Username for this peer identity")
@click.option('--port', default=5001, help="Port to use for sending/listening")
@click.pass_context
def cli(ctx, username, port):
    """🔐 Hush CLI - Decentralized P2P Messaging"""
    ctx.ensure_object(dict)
    ctx.obj['username'] = username
    ctx.obj['port'] = port

def get_peer(ctx):
    import secrets
    import json

    username = ctx.obj['username']
    port = ctx.obj['port']

    hush_dir = os.path.expanduser("~/.hush")
    os.makedirs(hush_dir, exist_ok=True)

    priv_path = os.path.join(hush_dir, f"{username}_private_key.pem")
    pub_path = os.path.join(hush_dir, f"{username}_public_key.pem")
    auth_path = os.path.join(hush_dir, f"{username}_auth.json")

    # 🔐 Load or generate keys
    if os.path.exists(priv_path) and os.path.exists(pub_path):
        with open(priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(pub_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
    else:
        private_key, public_key = generate_keys()
        with open(priv_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(pub_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    # 🔒 Generate/load password
    if not os.path.exists(auth_path):
        password = secrets.token_urlsafe(12)
        with open(auth_path, "w") as f:
            json.dump({"username": username, "password": password}, f)
        print(f"🔐 Auth password generated for {username}: {password}")
    else:
        with open(auth_path, "r") as f:
            creds = json.load(f)
        password = creds["password"]

    # 🧠 Attach to peer object
    peer = Peer(username=username, private_key=private_key, public_key=public_key, listen_port=port)
    peer.auth_password = password

    return peer

def get_peer_bk(ctx):
    username = ctx.obj['username']
    port = ctx.obj['port']

    hush_dir = os.path.expanduser("~/.hush")
    os.makedirs(hush_dir, exist_ok=True)
    priv_path = os.path.join(hush_dir, f"{username}_private_key.pem")
    pub_path = os.path.join(hush_dir, f"{username}_public_key.pem")

    if os.path.exists(priv_path) and os.path.exists(pub_path):
        with open(priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(pub_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
    else:
        private_key, public_key = generate_keys()
        with open(priv_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(pub_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    return Peer(username=username, private_key=private_key, public_key=public_key, listen_port=port)

@cli.command()
@click.option('--ip', required=True)
@click.option('--port', required=True, type=int)
@click.pass_context
def sendkey(ctx, ip, port):
    """Send your public key to a peer"""
    peer = get_peer(ctx)
    peer.send_public_key(ip, port)

@cli.group()
def alias():
    """Manage peer aliases"""
    pass

@alias.command("add")
@click.argument('name')
@click.argument('ip')
@click.argument('port', type=int)
@click.pass_context
def alias_add(ctx, name, ip, port):
    peer = get_peer(ctx)
    peer.aliases[name] = ip
    peer._save_keys_to_disk()
    click.echo(f"✅ Alias '{name}' set to {ip}:{port}")

@cli.command()
@click.option('--target', required=True)
@click.option('--message', required=True)
@click.pass_context
def msg(ctx, target, message):
    """Send an encrypted message via UDP"""
    peer = get_peer(ctx)
    peer._load_keys_from_disk()

    if ":" in target:
        ip, port = target.split(":")
        peer.send_direct(ip, int(port), message)
    elif target in peer.aliases:
        ip = peer.aliases[target]
        peer.send_direct(ip, peer.listen_port, message)
    else:
        click.echo("❌ Unknown target")

@cli.command()
@click.option('--ip', required=True)
@click.option('--port', required=True, type=int)
@click.option('--message', required=True)
@click.pass_context
def sendtcp(ctx, ip, port, message):
    peer = get_peer(ctx)
    peer._load_keys_from_disk()
    peer.send_tcp(ip, port, message)

@cli.command()
@click.option('--ip', required=True)
@click.option('--port', required=True, type=int)
@click.option('--filepath', required=True, type=click.Path(exists=True))
@click.pass_context
def sendfile(ctx, ip, port, filepath):
    peer = get_peer(ctx)
    peer._load_keys_from_disk()
    peer.send_file(ip, port, filepath)

@cli.command()
@click.pass_context
def start(ctx):
    """Start peer in interactive mode"""
    peer = get_peer(ctx)
    peer.start()

#@cli.command()
#@click.option('--username', required=True)
#@click.option('--port', default=5001)
#def start(username, port):
#    """Start peer in interactive mode"""
#    private_key, public_key = generate_keys()
#    peer = Peer(username, private_key, public_key, listen_port=port)
#    peer.start()

@cli.command()
@click.option('--tail', is_flag=True, help="Tail the log file")
@click.pass_context
def receive(ctx, tail):
    """📨 View received messages"""
    username = ctx.obj['username']
    log_path = os.path.expanduser(f"~/.hush/logs/{username}_messages.log")

    if not os.path.exists(log_path):
        click.echo("📭 No messages received yet.")
        return

    if tail:
        click.echo(f"📨 Tailing messages for {username}...\n(Press Ctrl+C to stop)")
        try:
            with open(log_path, "r") as f:
                f.seek(0, os.SEEK_END)
                while True:
                    line = f.readline()
                    if line:
                        click.echo(line.strip())
        except KeyboardInterrupt:
            click.echo("\n👋 Stopped tailing.")
    else:
        click.echo(f"📨 Messages for {username}:")
        with open(log_path, "r") as f:
            for line in f:
                click.echo(line.strip())


import subprocess

@cli.group()
def service():
    """Manage hush systemd services"""
    pass

@service.command()
@click.option("--username", required=True, help="Username for the node")
@click.option("--port", default=5001, help="Port to run the peer on")
def start(username, port):
    """Start the hush peer as a systemd user service"""
    home = os.path.expanduser("~")
    systemd_dir = os.path.join(home, ".config", "systemd", "user")
    os.makedirs(systemd_dir, exist_ok=True)

    service_path = os.path.join(systemd_dir, f"hush@{username}.service")
    project_path = os.path.abspath(".")

    content = f"""
[Unit]
Description=Hush P2P Node for {username}
After=network.target

[Service]
ExecStart=/usr/bin/env PYTHONPATH={project_path} /usr/bin/python3 {project_path}/hush/main.py --username {username} --port {port}
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
"""

    with open(service_path, "w") as f:
        f.write(content)

    click.echo(f"✅ Created systemd service: {service_path}")

    subprocess.run(["systemctl", "--user", "daemon-reexec"])
    subprocess.run(["systemctl", "--user", "daemon-reload"])
    subprocess.run(["systemctl", "--user", "enable", f"hush@{username}.service"])
    subprocess.run(["systemctl", "--user", "start", f"hush@{username}.service"])

    click.echo(f"🚀 Service hush@{username} started")

@service.command()
@click.argument("username")
def stop(username):
    """Stop the hush systemd service"""
    subprocess.run(["systemctl", "--user", "stop", f"hush@{username}.service"])
    click.echo(f"🛑 Stopped hush@{username}.service")

@service.command()
@click.argument("username")
def restart(username):
    """Restart the hush systemd service"""
    subprocess.run(["systemctl", "--user", "restart", f"hush@{username}.service"])
    click.echo(f"🔁 Restarted hush@{username}.service")

@service.command()
@click.argument("username")
def status(username):
    """Check the status of the hush systemd service"""
    subprocess.run(["systemctl", "--user", "status", f"hush@{username}.service"])


@cli.command()
@click.pass_context
def show_password(ctx):
    """🔐 Show the dashboard login password for this node"""
    import json

    username = ctx.obj['username']
    auth_path = os.path.expanduser(f"~/.hush/{username}_auth.json")

    if not os.path.exists(auth_path):
        click.echo("❌ No password found. Run `hush start` first to initialize keys and auth.")
        return

    with open(auth_path, "r") as f:
        creds = json.load(f)

    click.echo(f"🔑 Dashboard login for {username}")
    click.echo(f"   👤 Username: admin")
    click.echo(f"   🔐 Password: {creds['password']}")

@cli.command()
@click.pass_context
def dashboard(ctx):
    """📊 Launch the password-protected dashboard (web UI)"""
    import subprocess
    import sys

    username = ctx.obj['username']
    os.environ["DASH_USER"] = username

    click.echo(f"🚀 Starting dashboard for {username} at http://localhost:8787")
    subprocess.run([sys.executable, "web_gateway.py"])

if __name__ == "__main__":
    cli()
