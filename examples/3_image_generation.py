"""Image generation example — send a prompt and save returned image bytes/base64.

Adjust endpoint and response handling to match your provider. Example assumes base64.
"""
import os
import requests
import base64

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

url = f"{ENDPOINT.rstrip('/')}/images:generate"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {
    "model": "gemini-image-small",
    "prompt": "A friendly robot reading a book on a sunny windowsill, digital art",
    "size": "1024x1024",
}

resp = requests.post(url, headers=headers, json=payload, timeout=60)
resp.raise_for_status()
data = resp.json()

# Example shape: {data:[{b64_json: "..."}]}
image_bytes = None
if isinstance(data, dict):
    items = data.get("data") or []
    if items:
        b64 = items[0].get("b64_json") or items[0].get("image_base64")
        if b64:
            image_bytes = base64.b64decode(b64)

if image_bytes:
    path = "generated_image.png"
    with open(path, "wb") as f:
        f.write(image_bytes)
    print(f"Saved image to {path}")
else:
    print("No image bytes found in response; full response printed below:")
    import json
    print(json.dumps(data, indent=2))
