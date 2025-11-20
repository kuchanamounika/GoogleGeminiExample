"""Research summarization example: summarize abstracts and extract key contributions.

This script accepts a short abstract (or multiple) and asks the model to return
a concise summary, key contributions, methods, and suggested follow-ups.
"""
import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

abstract = input("Paste paper abstract (single line or paragraph): ")

prompt = (
    "You are an assistant that summarizes academic abstracts. Return a JSON object with keys:\n"
    "  - 'summary' (1-2 sentences),\n"
    "  - 'key_contributions' (bullet list),\n"
    "  - 'methods' (short description),\n"
    "  - 'potential_follow_up' (one or two suggested follow-up experiments or research directions).\n"
    "Respond only with JSON."
    f"\n\nAbstract:\n{abstract}"
)

payload = {
    "model": "gemini-ao-small",
    "messages": [
        {"role": "system", "content": "You summarize and extract structured information from research abstracts."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.0,
}

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

print(json.dumps(data, indent=2))

assistant_text = None
choices = data.get("choices") if isinstance(data, dict) else None
if choices and isinstance(choices, list):
    assistant_text = choices[0].get("message", {}).get("content")
elif isinstance(data, dict) and "output" in data:
    assistant_text = data["output"].get("text")

if assistant_text:
    try:
        parsed = json.loads(assistant_text)
        print("Parsed JSON result:\n", json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("Model did not return strict JSON. Raw output:\n", assistant_text)
