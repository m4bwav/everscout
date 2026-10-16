---
title: Gemini URL context on Reddit threads - Stage 1 test results (passed on gemini-3.5-flash-lite)
kind: research
status: active
date: 2026-10-15
verified: 2026-10-15
tags: [reddit, gemini, url-context, arctic-shift, stage-1, test]
---

# Gemini URL context on Reddit threads: Stage 1 results

Stage 1 of [../plans/2026-10-15-reddit-via-gemini-url-context.md](../plans/2026-10-15-reddit-via-gemini-url-context.md), run on the evening of 2026-10-15 (local time; 00:20 to 01:30 UTC on 2026-10-16). Probe, cases and setup history: [../notes/2026-10-15-gemini-url-context-probe.md](../notes/2026-10-15-gemini-url-context-probe.md). Raw responses stayed in the session scratchpad, not the repo. The `google_search` tool was not used in any request.

**Verdict: passes the plan's bar on `gemini-3.5-flash-lite`.** All six Reddit threads came back with the right title and body, the settled thread gave 47 real comments, and no comment was shown to be invented. `gemini-3.8-flash`, the model the plan named, could not be tested: Google's side was overloaded all session.

## The key works now

The 403s of the afternoon are gone. A plain "Say OK." `generateContent` call gave HTTP 200 on `gemini-3.5-flash-lite`. `gemini-2.5-flash` answers 404 "no longer available to new users". `gemini-3.8-flash` answered either 503 "This model is currently experiencing high demand" within half a second, or held the connection and dropped it at exactly 60 s. That happened with curl too (`-m 180`), with streaming (`streamGenerateContent?alt=sse`), and with no tool at all, so the 60 s drops in the earlier note were this overload, not URL context and not the network path. Every response reported `service_tier: "standard"`.

## How URL context reads Reddit

- Every Reddit call returned two `url_context_result` entries: the slug URL (`.../comments/1x3y8ot/nvidia_rtx_video_super_resolution_for_comfyui/`) with `status: "success"`, and the bare URL we passed with `status: "error"`. So the text comes from Google's index cache under the canonical URL; the live fetch of reddit.com fails. A thread Google has not indexed yet will not read. The fresh case, 8.6 hours old, was already indexed.
- Status values seen: `success`, `error` (the docs name only `unsafe`).
- The GitHub control page came back `error` (the model said "Not able to browse the provided URL"), and so did a Wikipedia URL for a page that probably does not exist. `https://en.wikipedia.org/wiki/Reddit` through `generateContent` gave `URL_RETRIEVAL_STATUS_SUCCESS`. So URL context works; some ordinary pages simply fail the live fetch.
- When reading failed, the model said so (`read_ok: false`) and invented nothing.
- The Interactions endpoint (`/v1beta/interactions`) and `generateContent` with `tools: [{"url_context": {}}]` both work. The fetched page counts as `usage.total_tool_use_tokens`, not `tool_use_input_tokens` as the plan said.

## Results

Ground truth: `everscout.py thread <url> --reddit-reader arcticshift --json`, plus a second copy from the Reddit RSS reader (`--reddit-reader rss`, allowed until 2026-11-13), because the archive turned out to miss comments and to hold pre-edit post bodies. One request per case, about 6 s apart; latency 2.7 to 20 s.

| case | thread (age, comments) | title | body | Gemini comments | real (archive / RSS only / near) | handle as text | placeholder | unverified | page tokens | out tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| fresh | r/comfyui 1x6p7lt (8.6 h, 21) | exact | matches current post | 20 | 18 / 0 / 2 | 0 | 0 | 0 | 4,348 | 1,232 |
| settled | r/StableDiffusion 1x3y8ot (3 days, 51) | exact | matches current post (archive holds the pre-edit body) | 47 | 39 / 8 / 0 | 0 | 0 | 0 | 7,744 | 4,633 |
| long | r/aivideos 1x3dr2c (251) | exact | none (both) | 89 | 60 / 17 / 3 | 6 | 0 | 3 | 4,336 | 2,544 |
| old | r/StableDiffusion 1od9gcj (Oct 2025, 185) | exact | exact | 151 | 127 / 12 / 3 | 0 | 9 | 0 | 15,103 | 9,866 |
| media | r/aivideo 1x48vay (video, 174) | exact | none (both) | 62 | 44 / 2 / 2 | 13 | 1 | 0 | 2,938 | 1,815 |
| removed | r/StableDiffusion 1x2aqmw (post deleted, 13) | exact | empty (post is `[deleted]`) | 12 | 9 / 2 / 0 | 1 | 0 | 0 | 5,677 | 619 |

Counts: "real" means the comment's text is in the Arctic Shift tree, only in the RSS tree, or a near match (similarity 0.85 or more after markdown is stripped). "Handle as text" means a username came back as a comment's text (a page-parsing slip). "Placeholder" means "Comment removed by moderator" or "Comment deleted by user" came back as the text.

Against the plan's pass bar:

- Post body matching in at least four of six: 6 of 6 (fresh and settled match the post as it reads now, which is newer than the archive's copy; the deleted post came back empty).
- A settled thread with ten or more real comments: 47.
- No fabricated comment in the sample: none shown. Three comments in the long thread ("I like this version better than the original.", "I'd play just for the dance offs", "The song is good though.") appear in neither source, but that thread has 109 collapsed comments that neither reader fetches, so they are unverified, not shown false.

## What it means for a reader

- Coverage drops on long threads: 89 of 251 comments (long), 62 of 174 (media), 151 of 185 (old). Fine for triage and a paraphrased note, not a full copy.
- Deleted and removed content: Gemini returned the placeholders, not the removed text, and an empty body for the deleted post. On this sample it honours deletions better than the archive, which holds comment text that Reddit now shows as removed. Conduct rule 16 still applies downstream: drop placeholders.
- Usernames leak into comment text (20 of 381 comments, mostly in the video post). A reader must drop single-token items that look like handles before anything reaches a note (rule 16: no handles in notes).
- Formatting is lost: strikethrough in the fresh post came back as plain text, so a struck-out claim reads as asserted. Keep an eye on this when distilling.
- Cost per thread: 3,000 to 15,000 page tokens plus 600 to 10,000 output tokens on flash-lite, mostly output, because the instruction asks for every comment word for word. Asking for a summary or fewer comments would cut it.
- Freshness depends on Google's index, not on a live fetch. An 8.6 hour old thread was indexed; an hour-old one was not tested.

## Other findings

- `everscout.py fetch ... --reddit-reader arcticshift --settle-hours 0 --max-age-days 1` drew a 422 Unprocessable Entity from the archive once; the same URL answered 200 a minute later, so it was transient.
- The Arctic Shift comment tree misses comments that the RSS tree has (8 of 47 real comments in settled were RSS-only), and its post bodies can predate an edit. Ground truth for later tests should take both sources while the feeds last.

## Untested

- `gemini-3.8-flash` (overloaded all session) and paid tiers.
- A thread under an hour old, and threads that were never indexed.
- Rate limits and daily quota: about 20 requests in an hour caused no 429.
- Reddit's side: nothing found that forbids reading Google's licensed copy this way, and nothing that blesses it (see the plan). This note does not call the route legal.
