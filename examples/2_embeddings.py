"""Embeddings example: send a list of texts and print/save the vectors.

Adapt the endpoint path/payload to your provider. This stores vectors as JSON.
"""
import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

texts = [
    "Machine learning makes software smarter.",
    "Unit tests catch bugs early and speed up development.",
    "Python is a popular programming language for data science."
]

url = f"{ENDPOINT.rstrip('/')}/embeddings"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {"model": "gemini-emb-small", "input": texts}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

print(json.dumps(data, indent=2))

# Try to extract embeddings if present in a common shape
embeddings = []
if isinstance(data, dict):
    # shape: {data: [{embedding: [...]}, ...]}
    for item in data.get("data", []):
        vec = item.get("embedding") or item.get("vector")
        embeddings.append(vec)

if embeddings:
    with open("embeddings.json", "w", encoding="utf-8") as f:
        json.dump({"texts": texts, "embeddings": embeddings}, f)
    print("Saved embeddings to embeddings.json")
