---
title: Gemini URL context probe for Reddit threads (Stage 1 script and progress)
kind: note
status: active
date: 2026-10-15
tags: [gemini, url-context, reddit, probe, stage-1]
---

# Gemini URL context probe (Stage 1)

The scratch probe for Stage 1 of `../plans/2026-10-15-reddit-via-gemini-url-context.md`, kept here so the next session can run it. Copy the script below to the session scratchpad as `probe.py`, then run `python -I probe.py gemini-3.8-flash` (all cases) or `python -I probe.py gemini-3.8-flash control fresh` (some). It reads `GEMINI_API_KEY` from the environment, never prints it, and writes each raw response to `raw/<case>.json` next to the script (keep raw responses out of the repo).

## Cases (chosen 2026-10-15 with Arctic Shift)

| case | URL | why |
|---|---|---|
| control | github.com/ArthurHeitmann/arctic_shift | non-Reddit page: tells "URL context down" from "Reddit refused" |
| fresh | r/comfyui 1x6t37u (5 h old, 15 comments when picked) | index lag, live fetch |
| settled | r/StableDiffusion 1x3y8ot (47 comments) | the normal scan case |
| long | r/aivideos 1x3dr2c (251 comments) | how much of a long thread comes back |
| old | r/StableDiffusion 1od9gcj (October 2025, 156 comments) | old index entries |
| media | r/aivideo 1x48vay (video post, 152 comments) | what comes back for media |
| removed | r/StableDiffusion 1x2aqmw (author and body deleted, 13 comments) | does Gemini return removed text (conduct rule 16) |

"fresh" will not be fresh in a later session: pick a new one with `everscout.py fetch --beat ai-video --kinds reddit --reddit-reader arcticshift --settle-hours 0 --max-age-days 1 --peek --json` (r/StableDiffusion's one-day window timed out at the archive twice on 2026-10-15, "Timeout. Maybe slow down a bit"; small subreddits answered). Ground truth for fidelity: `everscout.py thread <url> --reddit-reader arcticshift --json`.

## Progress on 2026-10-15

- Key: set at user level (`GEMINI_API_KEY`), visible to the session after a VS Code restart.
- First call: HTTP 403 `SERVICE_DISABLED`, "Gemini API has not been used in project 268277778089 before or it is disabled": the key was made in a Cloud project without the API switched on. Mark opened the API page and found it already showing Enabled.
- Calls in the next minutes: the control case with `url_context` hung and the connection dropped at exactly 60 s (`RemoteDisconnected`), twice; plain calls without a tool answered 403, either `SERVICE_DISABLED` again or "The caller does not have permission", flipping from call to call; the models list answered 403 `SERVICE_DISABLED`; `generateContent` on `gemini-3.8-flash`, `gemini-3.5-flash-lite` and `gemini-2.5-flash` all 403. That reads as the switch-on still spreading. No verdict on URL context yet. A last retry about 15 minutes after enabling: a plain `generateContent` "Say OK." on `gemini-3.8-flash` answered 403 "The caller does not have permission" once, then the next try hung until the 60 s read timeout. So the 60 s hangs are not URL context: any call that gets past the permission check hung. Either the new project is still being set up, or something on the network path holds the connection (test with `curl -m 180` and a longer Python timeout before blaming Google).

## If the 403s persist in the next session

1. In AI Studio (aistudio.google.com/apikey) check which project the key belongs to, and that it is project 268277778089, whose Gemini API page shows Enabled.
2. Check the key's API restrictions in the Cloud console (Credentials): it must allow the Generative Language API.
3. Simplest fix: in AI Studio create a new key in a new project that AI Studio makes itself, run `setx GEMINI_API_KEY` again and restart VS Code. (Mark's hands; never a browser login by the agent.)
4. If plain calls work but `url_context` calls still drop at 60 s, try streaming or the API's background mode and poll; check the Interactions API reference for the current field names first.

## Script

```python
"""Stage 1 probe: can Gemini's URL context tool read Reddit threads? Standard library only.
Reads GEMINI_API_KEY from the environment (never printed). Saves each raw response to raw/<case>.json."""
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-3.8-flash"
API = "https://generativelanguage.googleapis.com/v1beta/interactions"

CASES = [
    ("control", "https://github.com/ArthurHeitmann/arctic_shift"),
    ("fresh", "https://www.reddit.com/r/comfyui/comments/1x6t37u/"),
    ("settled", "https://www.reddit.com/r/StableDiffusion/comments/1x3y8ot/"),
    ("long", "https://www.reddit.com/r/aivideos/comments/1x3dr2c/"),
    ("old", "https://www.reddit.com/r/StableDiffusion/comments/1od9gcj/"),
    ("media", "https://www.reddit.com/r/aivideo/comments/1x48vay/"),
    ("removed", "https://www.reddit.com/r/StableDiffusion/comments/1x2aqmw/"),
]

INSTRUCTION = """Read this page with the URL context tool: {url}

Return ONLY a JSON object, no prose, no code fences:
{{"read_ok": true or false, "why_not": "<if the page could not be read, what you saw instead>",
 "title": "<post title, word for word>", "body": "<post body text, word for word, empty if none>",
 "comments": [{{"text": "<comment text word for word>", "author_is_op": true or false}}]}}
Include as many comments as the page shows, in page order, copied exactly. Do not summarise or paraphrase.
If you could not read the page, set read_ok false and do not invent content."""


def call(url):
    body = {"model": MODEL, "input": INSTRUCTION.format(url=url), "tools": [{"type": "url_context"}]}
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST",
                                 headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode("utf-8")), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, {"http_error": e.read().decode("utf-8", "replace")[:2000]}, time.time() - t0
    except Exception as e:  # dropped connections, timeouts
        return "net", {"net_error": f"{type(e).__name__}: {e}"}, time.time() - t0


def main():
    if not KEY:
        sys.exit("GEMINI_API_KEY not set")
    os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)
    only = set(sys.argv[2:])
    for name, url in CASES:
        if only and name not in only:
            continue
        status, data, secs = call(url)
        with open(os.path.join(HERE, "raw", f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump({"case": name, "url": url, "model": MODEL, "status": status, "seconds": round(secs, 1), "response": data},
                      f, indent=1, ensure_ascii=False)
        print(f"{name:<8} HTTP {status} {secs:5.1f}s  {url}", flush=True)
        time.sleep(6)


if __name__ == "__main__":
    main()
```
