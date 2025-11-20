"""Function-calling / structured-output example.

This demonstrates requesting a structured JSON-like response (e.g., asking model to return a specific schema).
It does simple validation of the returned JSON.
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

prompt = (
    "You are an assistant that returns weather report data as JSON. "
    "Return a JSON object with keys: city (string), temperature_c (number), condition (string). "
    "Do not include any extra commentary outside the JSON."
)

payload = {
    "model": "gemini-ao-small",
    "messages": [
        {"role": "system", "content": "You must only return valid JSON matching the schema."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.0,
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

print(json.dumps(data, indent=2))

# Try to extract textual output and parse it as JSON
text_out = None
choices = data.get("choices") if isinstance(data, dict) else None
if choices and isinstance(choices, list):
    text_out = choices[0].get("message", {}).get("content")
elif isinstance(data, dict) and "output" in data:
    # fallback
    text_out = data["output"].get("text")

if text_out:
    try:
        parsed = json.loads(text_out)
        # Very simple schema check
        if isinstance(parsed, dict) and "city" in parsed and "temperature_c" in parsed:
            print("Parsed structured output:", parsed)
        else:
            print("Parsed JSON but schema mismatch:", parsed)
    except json.JSONDecodeError:
        print("Could not parse model output as JSON; raw output:\n", text_out)
else:
    print("Could not find textual model output in response")
