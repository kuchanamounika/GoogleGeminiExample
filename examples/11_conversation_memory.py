"""Conversation memory example: persist a short chat history locally and reuse it.

This shows a simple file-backed memory for multi-turn conversations.
"""
import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")
MEM_FILE = "conv_memory.json"

if not API_KEY or not ENDPOINT:
    raise SystemExit("Set GEMINI_API_KEY and GEMINI_API_ENDPOINT environment variables")

def load_memory():
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # start with a system instruction
    return [{"role": "system", "content": "You are a helpful assistant that remembers prior chat turns."}]

def save_memory(mem):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(mem[-20:], f, ensure_ascii=False, indent=2)

memory = load_memory()

user_input = input("User: ")
memory.append({"role": "user", "content": user_input})

url = f"{ENDPOINT.rstrip('/')}/chat"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
payload = {"model": "gemini-ao-small", "messages": memory, "temperature": 0.4}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

# try to append assistant reply to memory
reply_text = None
choices = data.get("choices") if isinstance(data, dict) else None
if choices and isinstance(choices, list):
    reply_text = choices[0].get("message", {}).get("content")
elif isinstance(data, dict) and "output" in data:
    reply_text = data["output"].get("text")

if reply_text:
    print("Assistant:\n", reply_text)
    memory.append({"role": "assistant", "content": reply_text})
    save_memory(memory)
else:
    print("Could not extract assistant reply; full response below")
    print(json.dumps(data, indent=2))
