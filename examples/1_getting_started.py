"""Simple text/chat generation example using HTTP and environment variables.

This example shows a minimal POST to a chat/generate endpoint and prints the reply.
Modify `GEMINI_API_ENDPOINT` and request body to match your provider's API.
"""
import os
import requests
import json


API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {
    "model": "gemini-ao-small",  # example model name — replace as needed
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the benefits of unit testing in 2 sentences."}
    ],
    "temperature": 0.2,
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()

# The exact shape of the response varies by provider. This prints the raw JSON.
data = resp.json()
print(json.dumps(data, indent=2))

# If the provider returns a direct text field, you can extract it like:
maybe_text = None
if isinstance(data, dict):
    # common shapes: {choices:[{message:{content:...}}]} or {output: {text:...}}
    choices = data.get("choices")
    if choices and isinstance(choices, list):
        maybe_text = choices[0].get("message", {}).get("content")
    elif "output" in data and isinstance(data["output"], dict):
        maybe_text = data["output"].get("text")

if maybe_text:
    print("\nAssistant reply:\n", maybe_text)
