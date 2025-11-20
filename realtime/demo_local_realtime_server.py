"""Local demo WebSocket server that simulates streaming model responses.

Run this to test realtime client integration without an external API.
Clients connect and send a single message; server replies in multiple small chunks with delays.
"""
import asyncio
import json
import websockets
import time

HOST = "localhost"
PORT = 8765

async def simulate_stream(ws, text):
    # Simulates chunked streaming by sending small partial messages with a short delay
    parts = [f"{text} — part {i}" for i in range(1, 6)]
    for p in parts:
        # Send a JSON payload similar to SSE/chunked model output
        payload = {"type": "chunk", "text": p}
        await ws.send(json.dumps(payload))
        await asyncio.sleep(0.6)
    # final event
    await ws.send(json.dumps({"type": "done"}))

async def handler(websocket):
    async for message in websocket:
        try:
            # Accept plain text or JSON with {"input":...}
            data = json.loads(message)
            text = data.get("input") or data.get("message") or str(data)
        except Exception:
            text = message
        # echo back a simple ack, then stream
        await websocket.send(json.dumps({"type": "ack", "received": True}))
        await simulate_stream(websocket, f"Reply to: {text}")

async def main():
    print(f"Starting demo realtime server at ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")
