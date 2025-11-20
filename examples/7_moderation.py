"""Moderation / safety example: send text to a moderation endpoint and inspect labels.

Replace the endpoint path and response handling per your provider's moderation API.
"""
import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

url = f"{ENDPOINT.rstrip('/')}/moderation"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {"input": "I will hurt you!"}

resp = requests.post(url, headers=headers, json=payload, timeout=15)
resp.raise_for_status()
data = resp.json()

print(json.dumps(data, indent=2))

# Example: interpret common fields if present
if isinstance(data, dict):
    result = data.get("results") or data.get("categories") or data
    print("Moderation result summary:")
    print(result)
