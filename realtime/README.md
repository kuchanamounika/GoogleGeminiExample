# Realtime examples (WebSocket)

This folder demonstrates a common realtime pattern used across IT industries: a WebSocket-based real-time chat/streaming setup.

Files
- `realtime_ws_proxy.py` — example proxy that relays messages between browser/clients and a model WebSocket endpoint. The script shows how to connect to a provider WebSocket (placeholder), receive streaming chunks, and forward them in real time to connected clients.
- `demo_local_realtime_server.py` — a small local WebSocket server that simulates an LLM streaming responses (useful for testing without an external provider).

Env vars
- `GEMINI_WS_ENDPOINT` — (optional) provider websocket endpoint for model streaming (e.g., `wss://api.provider/v1/realtime`)
- `GEMINI_API_KEY` — API key used when connecting to provider websocket (if needed)

Notes
- Both examples use `websockets` and `asyncio` and are intentionally generic so you can adapt them to your provider's exact websocket protocol.
- The proxy contains comments where you need to adapt authentication and message shapes for your provider.

Run the demo local server (PowerShell):
```powershell
pip install -r ../examples/requirements.txt
python demo_local_realtime_server.py
```

In another terminal, connect with a websocket client (e.g., `websocat` or a small JS client) to `ws://localhost:8765` and send messages to see simulated streaming replies.
