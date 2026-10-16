---
title: YouTube channel feeds 404 for every channel; GDELT refuses on the first call
kind: research
status: active
date: 2026-10-16
verified: 2026-10-16
tags: [youtube, gdelt, outage, rate-limit, sources]
summary: read before changing a beat's YouTube rows after a 404, or before retrying or replacing a GDELT metric
---

# YouTube channel feeds 404 for every channel; GDELT refuses on the first call

Checked 2026-10-16 around 03:20 UTC, after the ai-video scan reported seven YouTube channel feeds returning 404 and a third GDELT 429.

## YouTube

What was tried (curl, everscout's User-Agent, 3 s apart):

- All seven ai-video channel ids: `youtube.com/feeds/videos.xml?channel_id=<id>` answered 404, served by "YouTube RSS Feeds server". Each channel page (`youtube.com/channel/<id>`) answered 200, so the ids are valid.
- Controls: Google Developers' channel id, the `playlist_id=UU...` uploads form and the `user=` form all answered 404 as well. A plain curl User-Agent got 404 too.
- The 2026-09-29 scan read the same feeds without error.

What others report: intermittent 404s from the same endpoint for active public channels since about 2025-12-20, at varying times of day, with the URLs often loading in a browser meanwhile; no official statement; a Google staff member asked for reproduction details on 2026-01-09 and the thread shows no answer. Sources: Google AI Developers Forum thread "YouTube RSS feed endpoint returns 404 errors" (https://discuss.ai.google.dev/t/youtube-rss-feed-endpoint-returns-404-errors/113379, posts 2025-12-27 to 2026-05-02) and the n8n community thread of the same name (https://community.n8n.io/t/youtube-rss-feed-endpoint-returns-404-errors/241692, 2025-12-27 to 30). Workarounds tried there (a browser User-Agent, slower polling) did not stop it; the Data API (keyed, low quota) did.

Conclusion: when every channel fails at once, the endpoint is down, not the ids. Do not edit `sources.md` on such a run. Fix in the CLI (unreleased, after 0.5.0): `fetch` prints one line saying so when every YouTube feed in the run fails. Unverified: whether this is the same intermittent fault or a lasting change; re-check on the next scan.

## GDELT

`news-ai-video-share` (DOC 2.0 `TimelineVol`) drew 429 on 2026-09-28, 2026-10-10 and 2026-10-16, each time on the first GDELT call after days without one. tech-hiring's GDELT metric failed the same way on 2026-09-27. The cool-down (1 h, doubling, `solutions/2026-09-27-gdelt-rate-limit.md`) works as designed; it cannot fix a refusal on the first call.

Reports from 2026: an MCP server issue measured 429s even with 5.2 s spacing and a block of about a minute (https://github.com/cyanheads/gdelt-mcp-server/issues/44); another project's server got 1 success in 14 calls over 30 hours and replaced the DOC API with GDELT 2.0's 15-minute GKG bulk files, losing phrase queries (https://github.com/ikorfale/errata-pulse/issues/16, 2026-10-06). GDELT itself publishes no quota beyond the refusal text ("one every 5 seconds").

Options for the ai-video beat, for Mark: keep the metric as a candidate and let the cool-down skip it (it costs one refused call a scan), or archive it with the reason "GDELT refuses this address". Its question (Q5) is already covered by `wiki-text-to-video`, and the two series do not move together (r = 0.17 over 8 points). A GKG bulk-file adapter would lose the "AI video" phrase query and is a large build for one metric: not recommended now.
