# Google Gemini Example - Gemini AO examples

This folder contains concise example scripts demonstrating common concepts when using Gemini (AO) style model APIs.

Each example is self-contained and uses environment variables for credentials and endpoints:

- `GEMINI_API_KEY` — API key or token
- `GEMINI_API_ENDPOINT` — base URL for the Gemini API (for example `https://api.your-provider.com/v1`)

Install requirements:

```powershell
pip install -r requirements.txt
```

Run an example (PowerShell):

```powershell
$env:GEMINI_API_KEY = "your_key_here"
$env:GEMINI_API_ENDPOINT = "https://api.your-provider.com/v1"
python 1_getting_started.py
```

Files in this folder:
- `1_getting_started.py` — simple chat/text generation example
- `2_embeddings.py` — create embeddings for texts
- `3_image_generation.py` — generate and save an image
- `4_function_calling.py` — request structured (function-like) JSON output
- `5_streaming.py` — streaming (chunked / SSE) response example
- `6_multimodal.py` — send image + text prompt for multimodal responses
- `7_moderation.py` — moderation/content-safety example
 - `4_function_calling.py` — request structured (function-like) JSON output
 - `5_streaming.py` — streaming (chunked / SSE) response example
 - `6_multimodal.py` — send image + text prompt for multimodal responses
 - `7_moderation.py` — moderation/content-safety example
 - `8_few_shot.py` — demonstrate few-shot prompting with example pairs
 - `9_rate_limit_retry.py` — robust request with retry/backoff for rate limits
 - `10_batch_embeddings.py` — batch texts for embeddings and save results
 - `11_conversation_memory.py` — simple conversation memory persisted locally
 - `12_temperature_sweep.py` — compare outputs across several temperatures

Notes:
- These examples use `requests` or standard libraries so they can be adapted to SDKs.
- Replace endpoints and payload fields to match the provider's exact API schema.

**Industry examples**
- **General / Demo:** `1_getting_started.py`, `5_streaming.py`, `realtime/demo_local_realtime_server.py`
- **Research / NLP:** `2_embeddings.py`, `10_batch_embeddings.py`, `12_temperature_sweep.py`, `8_few_shot.py`, `research_summarization.py` (new)
- **Medical / Healthcare (non-diagnostic):** `medical_triage.py` (new) — high-level triage-style prompts with clear disclaimers; not a substitute for professional medical advice
- **IT / Operations / Realtime:** `5_streaming.py`, `realtime/realtime_ws_proxy.py`, `realtime/demo_local_realtime_server.py`, `11_conversation_memory.py`, `it_alerts_stream.py` (new)
- **Safety / Content Moderation:** `7_moderation.py`
- **Developer / Integration:** `4_function_calling.py`, `9_rate_limit_retry.py`

If you'd like, I can also split these into subfolders (for example `examples/industry/medical`, `examples/industry/research`, etc.) and add README files per industry with more tailored guidance and disclaimers.
