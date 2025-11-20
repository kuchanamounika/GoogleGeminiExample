"""Streaming example (chunked or server-sent events).

This is a best-effort example showing how to consume chunked streaming responses.
Adjust to the provider's streaming API (SSE, WebSocket, etc.).
"""
import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

url = f"{ENDPOINT.rstrip('/')}/chat:stream"
headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "text/event-stream"}

payload = {"model": "gemini-ao-small", "messages": [{"role": "user", "content": "Tell a short story"}]}

with requests.post(url, headers=headers, json=payload, stream=True) as resp:
    resp.raise_for_status()
    print("Streaming response:")
    for chunk in resp.iter_lines(chunk_size=8192, decode_unicode=True):
        if chunk:
            # Many streaming APIs prefix SSE messages. Show raw chunk.
            print(chunk)

# Note: Many providers use WebSockets or a specific SSE format. Use the appropriate client
# (e.g., `websockets` or an SSE client) for production streaming.
