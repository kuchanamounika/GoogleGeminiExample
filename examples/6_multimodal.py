"""Multimodal example: send an image and a prompt and receive model commentary.

This demonstrates multipart upload of an image plus a textual prompt.
Adjust the endpoint and form fields to match your provider.
"""
import os
import requests
from PIL import Image
import io

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

# Create a small example image in-memory (replace with a real file in practice)
img = Image.new("RGB", (256, 256), color=(73, 109, 137))
buf = io.BytesIO()
img.save(buf, format="PNG")
buf.seek(0)

url = f"{ENDPOINT.rstrip('/')}/multimodal:analyze"
headers = {"Authorization": f"Bearer {API_KEY}"}

files = {
    "image": ("example.png", buf, "image/png"),
}
data = {
    "model": "gemini-multi-small",
    "prompt": "Describe the image and suggest three creative captions."
}

resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)
resp.raise_for_status()
print(resp.text)
