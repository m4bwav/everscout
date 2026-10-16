---
title: Reddit discovery after Arctic Shift - where thread URLs come from when nothing lists a subreddit
kind: plan
status: active
date: 2026-10-16
tags: [reddit, discovery, fetchwright, arctic-shift, captures, post-2027]
summary: read before building anything that finds Reddit thread URLs without a subreddit listing (after the feeds and Arctic Shift end)
---

# Reddit discovery after Arctic Shift

Stage 2 step 4 of `2026-10-15-reddit-via-gemini-url-context.md`, and steps 3 and 4 of `2026-10-11-reddit-lane-after-rss.md` seen from the reader's side. Read this before building anything that finds Reddit threads without a subreddit listing. Nothing here may make a key required.

## Goal

Keep finding the Reddit threads a beat needs once nothing lists a subreddit, without a key, without Gemini's search, and within fetchwright's daily quota.

## Status

2026-10-16: plan only, nothing built. Mark said build steps 1 to 5 in the next session (2026-10-16).

## Next single action

Build step 1 (`reddit_ids_in`) and step 2 (pickup during `fetch`), then compare a week of pickup against Arctic Shift's full listing for ai-video to measure coverage.

## The problem

Today a scan lists each subreddit (the feeds until 2026-11-13, then Arctic Shift), keeps the threads worth a note, and reads each kept thread (the feed, the archive, or fetchwright). Arctic Shift collects through Reddit's Data API, which is expected to end for it in March 2027 (maintainer issue #76, `../research/2026-10-11-reddit-after-the-api.md`). After that nothing lists a subreddit: fetchwright reads one URL at a time and must never find URLs through Gemini's Google Search (conduct rule 17). Discovery has to come from somewhere else, and it will cover less than a full listing. Expect it.

## What fetchwright needs from discovery (checked 2026-10-15 and 2026-10-16)

- **A thread URL in any form.** The bare `/comments/<id>/` permalink reads; Google resolves it to the slug URL from its index.
- **Threads at least a day old.** On 2026-10-16 a thread posted the day before was not in Google's index yet and did not read (`../research/2026-10-15-fetchwright-thread-reader-live.md`). Discovery should hold a new URL until it is 24 hours old, which suits the settled-score window anyway.
- **A budget inside the daily quota.** `gemini-3.8-flash` allows 20 requests a day on the free tier (Google's 429 said so on 2026-10-15). `gemini-3.5-flash-lite`'s limit is unverified; about 20 reads in one session drew no 429. So plan for at most 10 fetchwright reads per scan by default (config `fetchwright.max_reads_per_scan`), which leaves room for a second beat or a re-read the same day.

## Where URLs can come from

| route | cost | coverage | footing | build |
|---|---|---|---|---|
| A. Pickup from items already fetched (Hacker News, Bluesky, Mastodon, Lemmy, newsletters, YouTube descriptions, web notes) | no extra requests | low: only threads someone links elsewhere, but those are the ones that travelled | clean: the URL is in public data everscout already holds | CLI: extract `reddit.com/r/<sub>/comments/<id>` and `redd.it/<id>` from item text and links during `fetch`; dedupe by id; record where each came from; count mentions toward importance (lane step 3) |
| B. The agent's own web search (Claude Code's WebSearch, never Gemini) | one search a query; the scan already budgets searches in `searches.md` | medium for named topics, poor for "everything new in r/x" | a person's search; the result is a URL, the reading is fetchwright's | skill text in everscout-scan: per core subreddit, one or two searches built from the beat's vocabulary (`site:reddit.com/r/<sub> <entity>`) with a recent-date filter where the tool has one; the agent records each URL with a new CLI `ES discover add <url> --beat <slug> --via websearch` |
| C. User captures (lane step 4) | the user's time | whatever the user reads | the user's own reading | `captures/` inbox, `captures-wanted` list in the scan report, notes with `source: user-capture` |
| D. A keyed search API (Brave Search and the like) | metered; a card is required even for the free credit (third-party reports, 2026; Brave's own pricing page still lists a free tier: unverified) | medium | each API's terms on storing results need reading first | not now; only on Mark's ask, opt-in, the same way fetchwright is |
| E. Reddit's own Data API with a registered app | free for personal use if approved | full listings | Reddit's policy; approval uncertain | Mark's call before 2027-01-12 (lane plan decision 2); would replace this plan, not add to it |

Recommended: A and C first (no new host, no key), then B as skill text. D and E stay Mark's decisions.

## Ranking without scores

Discovered threads come with no points or comment counts: fetchwright drops them and route A and B give none. Rank candidates in triage by:

1. mentions across platforms (route A's count; a thread linked from two places beats one found by search);
2. vocabulary match on the title and the linking text (the scan's existing `vocab_match`);
3. the beat's `showcase_words` and `skip_words`, as now;
4. after the read, the comment count fetchwright returns, kept in the note's `interest` with `via: fetchwright` so tallies can tell it from archive scores.

## Shape of the build (when Mark says go)

1. `es_sources.py`: `reddit_ids_in(text)` returns `(id, sub, url)` from any permalink form, `redd.it` short links and old.reddit links; tests on synthetic text.
2. `everscout.py fetch`: collect ids from every non-Reddit item into `state["reddit_seen_elsewhere"]` (id, first seen, from, count), purged after 14 days; `ES discover list --beat <slug>` shows ids at least 24 hours old not yet read; `ES discover add <url> --via websearch|capture` records one by hand.
3. Triage: discovered ids join the candidate list with `via: pickup|websearch` and the ranking above; `new-note` and `thread` read them through `reddit.thread_reader`.
4. Budget: `fetchwright.max_reads_per_scan` (default 10); the scan stops reading at the cap and lists the rest as `captures-wanted`.
5. Skill text: everscout-scan's discovery step (route B queries, the 24-hour hold, the budget), and the captures step (lane step 4).
6. Docs: `kb/platforms.md` row "Reddit thread discovery after the archive", conduct rule 17 unchanged (it already forbids Gemini search), README host list unchanged (no new host).

## Size

About 120 lines of Python plus 6 to 8 tests for steps 1 to 4, and a page of skill text for step 5. One session. No new host and no key, so it can ship as a minor release before Arctic Shift ends and run alongside it: comparing what pickup finds with the archive's full listing is the cheapest way to measure coverage while the archive still exists.

## Limits that carry over

- Never Gemini's Google Search, and never find Reddit URLs through Gemini.
- Never retry a 429 within the hour; honour Google's stated retry time.
- Notes follow conduct rule 16: paraphrase, one short quote at most, no handles, drop deleted text.
- Never commit fetched text, real usernames or a recorded response.
