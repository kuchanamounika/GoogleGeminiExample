"""IT alerts classification example.

This script simulates a stream of alerts (log messages) and calls the model to classify
severity and recommend next steps. It is suitable for monitoring/ops workflows.
"""
import os
import time
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

alerts = [
    {"id": 1, "msg": "CPU usage on host db-prod-01 at 97% for 5 minutes"},
    {"id": 2, "msg": "Failed login attempts exceeded threshold on auth-service"},
    {"id": 3, "msg": "Disk I/O high on storage-02; many timeouts reported"},
    {"id": 4, "msg": "Service payment-processor returned 502 for 10% of requests"},
]

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def classify_alert(alert_text):
    prompt = (
        "You are an operations assistant. Given an alert message, return a JSON object with fields:\n"
        "  - 'severity' (one of 'critical','high','medium','low'),\n"
        "  - 'suggested_action' (short bullet/one-line action),\n"
        "  - 'is_escalation' (true/false).\n"
        "Return only JSON.\n\nAlert:\n" + alert_text
    )
    payload = {"model": "gemini-ao-small", "messages": [{"role": "user", "content": prompt}], "temperature": 0.0}
    resp = requests.post(url, headers=headers, json=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    # try to extract assistant text
    assistant_text = None
    choices = data.get("choices") if isinstance(data, dict) else None
    if choices and isinstance(choices, list):
        assistant_text = choices[0].get("message", {}).get("content")
    elif isinstance(data, dict) and "output" in data:
        assistant_text = data["output"].get("text")
    if assistant_text:
        try:
            return json.loads(assistant_text)
        except json.JSONDecodeError:
            return {"raw": assistant_text}
    return {"error": "no_output", "full_response": data}

if __name__ == "__main__":
    for a in alerts:
        print(f"Processing alert {a['id']}: {a['msg']}")
        result = classify_alert(a['msg'])
        print(json.dumps(result, indent=2))
        time.sleep(1.2)
