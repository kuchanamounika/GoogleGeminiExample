"""Few-shot prompting example: provide example Q/A pairs to guide the model.

This shows constructing a short few-shot prompt and sending to the chat endpoint.
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

# Few-shot examples (not exhaustive). These illustrate the pattern, not verbatim copies.
examples = [
    {"question": "What is the time complexity of binary search?",
     "answer": "O(log n) — binary search halves the search space each step."},
    {"question": "Give a short definition of unit testing.",
     "answer": "Unit testing verifies small parts of code (functions/methods) behave as expected."}
]

user_question = "Explain why code review is useful in 2 sentences."

# Build a single prompt string including the few-shot examples
prompt_lines = ["Use the examples to match style and brevity.\n"]
for ex in examples:
    prompt_lines.append(f"Q: {ex['question']}\nA: {ex['answer']}\n")
prompt_lines.append(f"Q: {user_question}\nA:")

payload = {
    "model": "gemini-ao-small",
    "messages": [
        {"role": "system", "content": "You are a concise assistant that follows the examples' style."},
        {"role": "user", "content": "\n".join(prompt_lines)}
    ],
    "temperature": 0.3,
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

print(json.dumps(data, indent=2))
