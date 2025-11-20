"""Batch embeddings example: break a long list into chunks for the embeddings endpoint.

This demonstrates a safe batching strategy and saving results to disk.
"""
import os
import requests
import json
from math import ceil

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i+size]

texts = [f"Example sentence number {i}" for i in range(1, 51)]
batch_size = 8

url = f"{ENDPOINT.rstrip('/')}/embeddings"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

all_embeddings = []
for batch in chunked(texts, batch_size):
    payload = {"model": "gemini-emb-small", "input": batch}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # common shape: {data:[{embedding: [...]}, ...]}
    for item in data.get("data", []):
        all_embeddings.append(item.get("embedding"))

with open("batch_embeddings.json", "w", encoding="utf-8") as f:
    json.dump({"texts": texts, "embeddings_len": len(all_embeddings)}, f)

print(f"Wrote {len(all_embeddings)} embeddings to batch_embeddings.json (metadata only)")
