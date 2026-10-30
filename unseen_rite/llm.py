"""Model client. Gemma 4 through Google AI Studio's REST API. The key comes from the
environment (GEMINI_API_KEY) or a local .env file that git ignores."""
import json
import os
import time
import urllib.error
import urllib.request

GEMMA = os.environ.get("RITE_MODEL", "gemma-4-26b-a4b-it")
CLOSED = "gemini-flash-latest"
USAGE = {"calls": 0, "failed": 0}


def _key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(here, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"')
    raise RuntimeError("GEMINI_API_KEY is not set")


def ask(prompt, model=None, temperature=0.4, max_tokens=4096, tries=8, thinking="minimal"):
    model = model or GEMMA
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    config = {"temperature": temperature, "maxOutputTokens": max_tokens}
    if thinking and model.startswith("gemma"):
        config["thinkingConfig"] = {"thinkingLevel": thinking}
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": config,
    }).encode()
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(url, data=body, headers={
            "content-type": "application/json", "x-goog-api-key": _key()})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=420))
            USAGE["calls"] += 1
            parts = data["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
        except urllib.error.HTTPError as err:
            last = f"HTTP {err.code}"
            if err.code not in (429, 500, 502, 503, 504):
                raise
        except Exception as err:  # network blip, odd reply shape
            last = str(err)
        USAGE["failed"] += 1
        time.sleep(min(60, 5 * (attempt + 1)))
    raise RuntimeError(f"model call failed after {tries} tries: {last}")
