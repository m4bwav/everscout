---
title: Reddit lane after RSS ends - Arctic Shift reader, cross-platform pickup, user captures
kind: plan
status: proposed
date: 2026-10-11
tags: [reddit, arctic-shift, captures, screenshots, scan]
---

# Reddit lane after RSS ends

Read this before touching the Reddit adapter or the scan procedure's Reddit steps. Evidence: `../research/2026-10-11-reddit-after-the-api.md`. Waits for the user's go-ahead; nothing here is built.

## Decisions the user owns

1. Use Arctic Shift as the Reddit reader (grey legal footing, see the research note), or drop Reddit reading and keep only second-hand pickup plus captures.
2. Register the everscout Reddit app before 2027-01-12 (it buys at most until March 2027).

## Steps if approved

1. `es_sources.py`: an `arcticshift` adapter. One request per subreddit per scan for the window from 36 hours to 8 days ago (scores are settled after about 1.5 days), sorted locally by score and comments; thread text through `/api/comments/tree`. Host gap 2 s, honour `X-RateLimit-Reset`, honest User-Agent. `kb/platforms.md` row with the date checked; synthetic-fixture tests.
2. Beats keep their `r/name` rows; the adapter replaces the RSS URL after 2026-11-13 (or at once, by config).
3. Cross-platform pickup: in triage, a Reddit URL found in a Hacker News, Bluesky, Mastodon or newsletter item counts toward that thread's importance.
4. Capture requests: when a thread passes the beat's importance bar and the scan could not read it, add it to a `captures-wanted` list in the scan report (URL, why it matters, what to capture), at most five per scan. The user drops pasted text, a saved PDF or HTML, or screenshots into the beat's `captures/` inbox; the next scan reads them as user-supplied data and writes the note with `source: user-capture`.
5. Conduct code and AGENTS.md: one line each saying captures are the user's own reading, paraphrased, never redistributed.

## Size

About 150 lines of Python plus tests for steps 1 to 3, and a page of skill text for step 4. One session.

## Checked 2026-10-15: Gemini as a licensed go-between

Mark asked for a Reddit route through Gemini's Google Search grounding instead of Arctic Shift. It fails on Google's own terms (no analysis by third parties, no caching, no mixing, no database) and on the free tier (no grounding for new users). Arctic Shift, cross-platform pickup and user captures above are still the options; a Gemini answer Mark reads and pastes himself is a user capture. Evidence: `../research/2026-10-15-reddit-through-gemini.md`.
