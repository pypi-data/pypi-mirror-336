import click
import os
from cryptography.hazmat.primitives import serialization
from hush.crypto.crypto import generate_keys
from hush.net.peer import Peer

@click.group()
@click.option('--username', default="CLI", help="Username for this peer identity")
@click.option('--port', default=5000, help="Port to use for sending/listening")
@click.pass_context
def cli(ctx, username, port):
    """🔐 Hush CLI - Decentralized P2P Messaging"""
    ctx.ensure_object(dict)
    ctx.obj['username'] = username
    ctx.obj['port'] = port

def get_peer(ctx):
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
#@click.option('--port', default=5000)
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

if __name__ == "__main__":
    cli()
