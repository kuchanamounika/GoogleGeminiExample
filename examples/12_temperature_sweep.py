"""Temperature sweep example: run the same prompt with different temperatures.

This helps illustrate how temperature affects variability/creativity.
"""
import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

prompt = "Write a 1-sentence creative description of a blue bicycle in a whimsical style."
temps = [0.0, 0.3, 0.7, 1.0]

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

results = {}
for t in temps:
    payload = {"model": "gemini-ao-small", "messages": [{"role": "user", "content": prompt}], "temperature": t}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    text_out = None
    choices = data.get("choices") if isinstance(data, dict) else None
    if choices and isinstance(choices, list):
        text_out = choices[0].get("message", {}).get("content")
    if not text_out and isinstance(data, dict) and "output" in data:
        text_out = data["output"].get("text")
    results[t] = text_out or json.dumps(data)

print("Temperature sweep results:\n")
for t, out in results.items():
    print(f"-- temp={t} --\n{out}\n")
