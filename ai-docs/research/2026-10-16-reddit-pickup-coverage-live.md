---
title: Reddit pickup on the ai-video beat - first live coverage check
kind: research
status: active
date: 2026-10-16
verified: 2026-10-16
tags: [reddit, discovery, pickup, coverage, ai-video, arctic-shift]
summary: read before relying on pickup alone to find Reddit threads after the archive ends; one week of ai-video's other sources linked no Reddit thread
---

# Reddit pickup on the ai-video beat: first live coverage check

Plan: [../plans/2026-10-16-reddit-discovery-after-arctic-shift.md](../plans/2026-10-16-reddit-discovery-after-arctic-shift.md). Built the same session: `fetch` picks Reddit thread links out of every non-Reddit item, `discover list` ranks them and prints coverage.

## Run

2026-10-16 about 04:00 UTC, from the `feat/reddit-discovery` branch. `EVERSCOUT_LOCAL` pointed at a scratch folder holding a copy of the beat's state and items, so the user's own state was not touched. `fetch --beat ai-video --kinds rss,youtube,github,huggingface,hn,mastodon,news,bluesky --max-age-days 7`: 26 non-Reddit sources (11 RSS, 7 YouTube, 2 GitHub, 2 Hugging Face, one each of HN, Mastodon, Google News and Bluesky), 19 fetched, 0 errors, 383 items filtered out by the beat's filters, 13 new.

## Findings

- **Inside the 7-day window, no item linked a Reddit thread.** `discover list`: 0 threads found; "pickup found 0 of the 24 Reddit threads noted in that time" (the beat's Reddit notes posted in the last 14 days).
- Before the window filter was added, pickup took one thread (`r/comfyui`, linked from two Comfy blog posts dated 2026-08-19 and 2026-09-03). Feeds keep posts for months, so without the filter the same old threads would come back every time their entries are purged. Since the fix, pickup reads only items inside the fetch window.
- All 7 YouTube channel feeds returned 404 during the run (the endpoint outage in `2026-10-16-youtube-feeds-and-gdelt-refusals.md`), so video descriptions were not checked. Check them again when YouTube answers.
- Muted items (the 383 filtered out) are not picked up. That is on purpose: the beat's filters say they are off topic.

## What it means

For ai-video, pickup alone finds close to nothing. Its non-Reddit sources (labs, release feeds, arXiv, newsletters) rarely link Reddit. After the archive ends, discovery for this beat rests on the agent's own web search (route B) and the user's captures (route C). Pickup costs no requests, so it stays on. Other beats may do better: tech-hiring and indie-ai-games have HN and Bluesky sources that link Reddit more often. Untested.

## Next measurement

Let pickup run in the user's real state through the weekly scans until the archive ends. Each `discover list` prints the coverage line, so the number builds up without a separate study. Re-check after four weekly scans (around 2026-11-13, when the feeds end), and once YouTube answers again.
