"""Rate-limit and retry example: simple exponential backoff for 429/5xx responses.

This script shows a conservative retry policy that you can adapt.
"""
import os
import time
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
payload = {"model": "gemini-ao-small", "messages": [{"role": "user", "content": "Give a brief tip for debugging Python."}]}

def post_with_retries(url, headers, json_payload, max_retries=5, backoff_base=1.0):
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = requests.post(url, headers=headers, json=json_payload, timeout=30)
            if resp.status_code == 429 or 500 <= resp.status_code < 600:
                raise requests.HTTPError(f"Retryable status {resp.status_code}")
            resp.raise_for_status()
            return resp
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            if attempt > max_retries:
                raise
            sleep = backoff_base * (2 ** (attempt - 1))
            # jitter
            sleep = sleep * (0.5 + os.urandom(1)[0] / 255 / 2)
            print(f"Attempt {attempt} failed: {e}. Backing off for {sleep:.1f}s")
            time.sleep(sleep)

resp = post_with_retries(url, headers, payload)
print(resp.status_code)
print(resp.text)
