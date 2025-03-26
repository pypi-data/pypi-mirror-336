import click
import os
from cryptography.hazmat.primitives import serialization
from hush.net.peer import Peer
from hush.crypto.crypto import generate_keys
from hush.utils.settings import load_settings

def load_or_generate_keys(username):
    hush_dir = os.path.expanduser("~/.hush")
    os.makedirs(hush_dir, exist_ok=True)
    priv_path = os.path.join(hush_dir, f"{username}_private_key.pem")
    pub_path = os.path.join(hush_dir, f"{username}_public_key.pem")

    if os.path.exists(priv_path) and os.path.exists(pub_path):
        with open(priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(pub_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        print(f"💾 Loaded keys from disk for {username}")
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
        print(f"🔑 New keys generated and saved for {username}")
    
    return private_key, public_key

@click.command()
@click.option('--username', required=True, help='Your display name')
@click.option('--port', default=5000, type=int, help='Custom listening port')
def cli(username, port):
    """🔐 Hush - Decentralized Encrypted P2P Messaging"""
    settings = load_settings()
    private_key, public_key = load_or_generate_keys(username)

    print(f"👤 Username: {username}")
    print(f"📡 Starting peer on port {port}...\n")

    peer = Peer(username=username, private_key=private_key, public_key=public_key, listen_port=port)
    peer.start()

if __name__ == "__main__":
    cli()
