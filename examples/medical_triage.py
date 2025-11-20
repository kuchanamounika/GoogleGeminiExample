"""Medical triage-style example (non-diagnostic).

IMPORTANT: This example is educational only. It does NOT provide medical advice.
Always direct users to seek professional medical care for any concerns.
"""
import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

def build_prompt(symptoms_text):
    return (
        "You are a clinical-assistant style AI that must NOT provide diagnoses or treatment. "
        "Given a brief symptom description, produce a JSON object with keys:\n"
        "  - 'red_flags': list of possible red-flag symptoms that require immediate professional attention,\n"
        "  - 'next_steps': suggested non-diagnostic next steps (e.g., seek clinician, go to ER, self-care) as plain text,\n"
        "  - 'disclaimer': short reminder that this is not medical advice.\n"
        "Respond only with JSON. Keep answers concise."
        f"\n\nSymptom description: {symptoms_text}"
    )

symptoms = input("Enter patient symptom summary (brief): ")

payload = {
    "model": "gemini-ao-small",
    "messages": [
        {"role": "system", "content": "You are a clinical-assistant style AI that must NOT provide diagnoses or treatment."},
        {"role": "user", "content": build_prompt(symptoms)}
    ],
    "temperature": 0.0,
}

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

print(json.dumps(data, indent=2))

# Attempt to extract the assistant text and parse JSON
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
