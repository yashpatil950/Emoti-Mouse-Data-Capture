"""
EmotiBit UDP -> WebSocket bridge for mionix_capture.html.

Requirements:
    pip install websockets

Run:
    python3 emotibit_ws_bridge.py
"""

import argparse
import asyncio
import json
import socket
import time
from typing import Set

import websockets


CLIENTS: Set[websockets.WebSocketServerProtocol] = set()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bridge EmotiBit UDP packets to WebSocket clients.")
    parser.add_argument("--udp-host", default="127.0.0.1", help="UDP bind host")
    parser.add_argument("--udp-port", type=int, default=12346, help="UDP bind port")
    parser.add_argument("--ws-host", default="127.0.0.1", help="WebSocket host")
    parser.add_argument("--ws-port", type=int, default=8765, help="WebSocket port")
    return parser.parse_args()


def parse_emotibit_packet(raw: str) -> dict:
    parts = raw.split(",")
    if len(parts) < 7:
        return {}
    value = ",".join(parts[6:]).strip()
    try:
        value_num = float(value)
        value_out = value_num
    except ValueError:
        value_out = value
    return {
        "unix_ms": int(time.time() * 1000),
        "emotibit_time": parts[0].strip(),
        "stream_tag": parts[3].strip(),
        "reliability": parts[5].strip(),
        "value": value_out,
        "raw_packet": raw,
    }


async def ws_handler(ws: websockets.WebSocketServerProtocol) -> None:
    CLIENTS.add(ws)
    try:
        await ws.wait_closed()
    finally:
        CLIENTS.discard(ws)


async def broadcast_message(payload: dict) -> None:
    if not CLIENTS:
        return
    msg = json.dumps(payload)
    await asyncio.gather(*(client.send(msg) for client in list(CLIENTS)), return_exceptions=True)


async def udp_loop(args: argparse.Namespace) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.udp_host, args.udp_port))
    sock.setblocking(False)
    print(f"[UDP] Listening on {args.udp_host}:{args.udp_port}")

    loop = asyncio.get_running_loop()
    while True:
        data, _ = await loop.sock_recvfrom(sock, 2048)
        raw = data.decode("utf-8", errors="replace").strip()
        pkt = parse_emotibit_packet(raw)
        if pkt:
            await broadcast_message(pkt)


async def main_async(args: argparse.Namespace) -> None:
    print(f"[WS] Serving on ws://{args.ws_host}:{args.ws_port}")
    async with websockets.serve(ws_handler, args.ws_host, args.ws_port):
        await udp_loop(args)


def main() -> None:
    args = parse_args()
    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("\nBridge stopped.")


if __name__ == "__main__":
    main()
