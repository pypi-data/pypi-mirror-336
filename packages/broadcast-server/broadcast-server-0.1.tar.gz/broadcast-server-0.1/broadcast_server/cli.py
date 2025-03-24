import argparse
import pyfiglet
from broadcast_server.server import start_server
from broadcast_server.client import connect_to_server
import asyncio

def print_banner():
    banner = pyfiglet.figlet_format("Broadcast Server")
    print(banner)


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Broadcast Server CLI")
    subparsers = parser.add_subparsers(dest="command")

    start_parser = subparsers.add_parser("start", help="Start the broadcast server")
    connect_parser = subparsers.add_parser("connect", help="Connect to the broadcast server as client")

    start_parser.add_argument("--host", default="localhost", help="Host to bind server")
    start_parser.add_argument("--port", type=int, default=8765, help="Port to bind server")

    connect_parser.add_argument("--uri", default="ws://localhost:8765", help="WebSocket URI to connect to")


    args = parser.parse_args()

    if args.command == "start":
        start_server(host=args.host, port=args.port)
    elif args.command == "connect":
        asyncio.run(connect_to_server(uri=args.uri))

    else:
        parser.print_help()
