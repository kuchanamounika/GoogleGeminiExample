"""WebSocket proxy example.

This script demonstrates a pattern: accept WebSocket client connections and forward
their messages to a model provider's WebSocket endpoint, streaming back model chunks
to the client in real time.

This is a generic template — adapt authentication and message format to your provider.
If `GEMINI_WS_ENDPOINT` is not set, the proxy will connect to the local demo server
(`ws://localhost:8765`) so you can test locally.
"""
import os
import asyncio
import json
import websockets

GEMINI_WS = os.getenv("GEMINI_WS_ENDPOINT") or "ws://localhost:8765"
API_KEY = os.getenv("GEMINI_API_KEY")

PROXY_HOST = "0.0.0.0"
PROXY_PORT = 8766

async def forward_client_to_model(client_ws, model_ws):
    async for msg in client_ws:
        # client message => forward to model websocket
        # Expect either plain text or JSON: {"input": "..."}
        try:
            data = json.loads(msg)
            payload = data
        except Exception:
            payload = {"input": msg}

        # Provider may require a particular handshake/auth message; include API_KEY if needed
        if API_KEY:
            # This is an example header-like message — adapt to provider
            await model_ws.send(json.dumps({"type": "auth", "key": API_KEY}))

        await model_ws.send(json.dumps(payload))

async def forward_model_to_client(model_ws, client_ws):
    async for msg in model_ws:
        # Forward model message directly
        await client_ws.send(msg)

async def proxy_handler(client_ws, path):
    # For each client, open a model connection and pipe messages
    async with websockets.connect(GEMINI_WS) as model_ws:
        # run both directions concurrently
        await asyncio.gather(
            forward_client_to_model(client_ws, model_ws),
            forward_model_to_client(model_ws, client_ws)
        )

async def main():
    print(f"Starting WebSocket proxy on ws://{PROXY_HOST}:{PROXY_PORT} -> {GEMINI_WS}")
    async with websockets.serve(proxy_handler, PROXY_HOST, PROXY_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Proxy stopped")
