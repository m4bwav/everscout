---
title: Reddit after 2027 - find thread URLs elsewhere, read them with Gemini's URL context tool
kind: plan
status: active
date: 2026-10-15
tags: [reddit, gemini, url-context, arctic-shift, backup, post-2027]
---

# Reddit after 2027: find URLs elsewhere, read them with Gemini's URL context

**Status (2026-10-16): everscout 0.5.0 released with the fetchwright thread reader; the live gate passed (9 of 10 threads read on the second run, flash-lite first).** Earlier the same night: everscout wired to fetchwright: config `reddit.thread_reader` and `--thread-reader` run fetchwright's CLI as a subprocess (decision `../decisions/2026-10-15-thread-reader-fetchwright.md`). Live: two of three threads read well, a long thread broke the JSON, then the free tier's daily limit for `gemini-3.8-flash` (20 requests) answered 429 and the run stopped (`../research/2026-10-15-fetchwright-thread-reader-live.md`). The four-of-six gate was met on the second run. What step 4 (discovery) must give fetchwright: thread URLs in any form (the bare `/comments/<id>/` permalink reads), one at a time, and a budget that fits the daily quota (about 20 kept threads a day on `gemini-3.8-flash`; flash-lite's limit is unverified).

**Earlier status (2026-10-15 night): Stage 2 built as its own plugin, [fetchwright](https://github.com/m4bwav/fetchwright) 0.1.0** (public; not yet released). Stage 2 steps 1 to 3 are done: the reader with model fallback, Google Search refused in code, retrieval checks, placeholder and handle drops, 37 offline tests and a live smoke test; conduct rule 17 and a kb/platforms.md keyed-sources row here. Live on 2026-10-15: gemini-3.8-flash answers plain calls but still 503s or drops on URL context; gemini-3.5-flash-lite read every page. New: word-for-word copies of long pages are blocked as recitation, so pages default to a digest. Step 4 (discovery after Arctic Shift) and wiring everscout to call fetchwright's CLI are open. Stage 1 passed earlier the same day on `gemini-3.5-flash-lite` (results: `../research/2026-10-15-gemini-url-context-reddit-test.md`).

Read this before building any Gemini reader for Reddit. Evidence for what is ruled out: `../research/2026-10-15-reddit-through-gemini.md`. Arctic Shift (0.4.0) collects through Reddit's Data API, which ends March 2027, so it is expected to stop then; this plan is the backup Mark asked for on 2026-10-15.

## The route

1. **Find** thread URLs without Gemini's Google Search tool: Arctic Shift subreddit listings while they last, then the agent's own web search (thread titles), and Reddit links found in Hacker News, Bluesky, Mastodon and newsletter items (lane plan step 3).
2. **Read** each thread with Gemini's URL context tool: the model is handed the URL and returns the page's content. The docs (updated 2026-10-13) say it "first tries an internal index cache" and falls back to a live fetch; Google's index is the one fresh copy of Reddit (Reddit's robots.txt admits only Google).
3. **Distil** in Claude as now (everscout note, paraphrase, one short quote).

## Why it may be clean, and the one line not to cross

- The Gemini API Additional Terms (effective 2026-03-23) restrict "Grounded Results", answers made with Grounding with Google Search: no analysis by third parties, no caching, no mixing, shown only to the end user who asked. The terms page has no such section for URL context; the URL context docs list technical limits only.
- Not allowed: using Gemini's Google Search tool to find the URLs. The terms: "it is a violation of these terms to use Grounding with Google Search to extract or collect one or more of these components for another purpose (for example, using programmatic or automated means to collect Links, using Links to build an index, or using Links to identify destination pages for crawling or scraping)". Never put `google_search` and `url_context` in the same request for this route.
- Still true for any Gemini use: the free tier's prompts and answers may be used to improve Google products and read by reviewers (public posts only, nothing private); 18+; only paid services may serve users in the EEA, Switzerland or the UK (matters for a public plugin's README).
- Reddit's side is untested ground: Google reads its own licensed copy and hands Mark its reading of the page. No clause found that forbids it; nothing found that blesses it either. Say exactly that, never "legal", in any README.

## Request (from the docs, 2026-10-15)

```
POST https://generativelanguage.googleapis.com/v1beta/interactions
x-goog-api-key: <GEMINI_API_KEY>
Content-Type: application/json
{"model": "gemini-3.8-flash", "input": "<instruction with the URL>", "tools": [{"type": "url_context"}]}
```

Text comes back in a `model_output` step (`content` blocks of `type: text`, `url_citation` annotations); a `url_context_result` step gives each URL's retrieval `status` (the docs name only `"unsafe"`; record every other value seen). Up to 20 URLs a request, 34 MB a URL, public pages only. Tokens of the fetched page count as input (seen as `usage.total_tool_use_tokens` on 2026-10-15). Seen in Stage 1: Reddit pages come from Google's index under the slug URL (`success`), while the live fetch of the bare URL gives `error`.

## Stage 0: key (Mark's hands)

Mark creates a key at https://aistudio.google.com/apikey and runs `setx GEMINI_API_KEY "<key>"`, then restarts VS Code. The agent checks `[Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')` (a session started before `setx` will not see it in `$env:`), never prints the key, never writes it to a file in a repo, never runs a browser login.

## Stage 1: the test (about ten minutes, scratch only)

A standard-library Python probe in the session scratchpad, not in the repo. Pick six Reddit threads with the Arctic Shift reader (it gives ground truth while it lasts) plus one non-Reddit control page:

| case | why |
|---|---|
| a thread under 24 hours old | does Google's index lag; does the live fetch reach Reddit |
| a thread 2 to 5 days old, settled | the normal scan case |
| a thread with 200+ comments | how much of a long thread comes back |
| a thread about a year old | old index entries |
| an image or video post | what comes back for media |
| a thread whose post was deleted or removed | does Gemini return the removed text (if so, the note must not use it: conduct rule 16) |
| a non-Reddit page (control) | separates "URL context is down" from "Reddit is refused" |

Instruction per URL: return the post title, body and as many top-level comments as the page shows, word for word, as JSON (`title`, `body`, `comments: [{text, author_is_op}]`), no summary, and say so when the page could not be read. Record per case: HTTP status, the `url_context_result` status, latency, input and output tokens, comments returned against Arctic Shift's count, exact-sentence match rate of the body and of five sampled comments against Arctic Shift's text, any comment not in Arctic Shift's tree (fabrication), and free-tier refusals (429, quota). Pace one request every few seconds.

Pass: at least four of the six Reddit cases return the post body matching Arctic Shift, a settled thread returns ten or more real comments, and no fabricated comment in the sample. Write the results either way into `../research/2026-10-15-gemini-url-context-reddit-test.md`, with the raw responses kept in the scratchpad, not the repo.

## Stage 2 if it passes: build

1. Shape, decided with Mark: a reader inside everscout (config `reddit.thread_reader: gemini`, key from the environment), a standalone public plugin that reads pages other fetchers cannot (Mark's original ask: setup advisor skill for the key, tiers, quotas and privacy; stdlib CLI; icon, wiki, SECURITY.md, size budget; creating the public repo was approved in the original kickoff), or both, everscout calling the plugin's CLI. Recommendation to put to him: the standalone plugin, because everscout stays keyless by default and the reader is useful beyond Reddit.
2. Offline tests on recorded responses (key and personal data scrubbed); one live smoke test that skips without a key.
3. Conduct rule 17 and `kb/platforms.md`: a row for the route, the "never Google Search for discovery" line, the free-tier privacy line.
4. Discovery after Arctic Shift: web search plus cross-platform pickup; expect weaker coverage than Arctic Shift's full listings.

## Stage 2 if it fails

Record the failure (statuses, error text) in the research note and stop. What is left then is Mark's choice: a private Google Search pipe at his own risk under Google's terms (never published as legal), a Reddit commercial Data API licence (price and eligibility unchecked), or captures he saves by hand.

## Size

Stage 1: one probe script of about 100 lines, one session hour. Stage 2: 200 to 300 lines of Python plus tests for the reader; a standalone plugin adds the full public-repo package.
