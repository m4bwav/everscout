---
title: everscout's fetchwright thread reader, first live run
kind: research
status: active
date: 2026-10-15
verified: 2026-10-16
tags: [reddit, fetchwright, gemini, thread-reader, quota]
summary: four live reads through everscout's new fetchwright reader; two read well, one long thread broke the JSON, and the free tier's daily limit for gemini-3.8-flash (20 requests) stopped the run
---

# everscout's fetchwright thread reader, first live run

Run on the evening of 2026-10-15 (US time; 2026-10-16 01:56 UTC at the stop) from Mark's PC, everscout 0.5.0 branch, fetchwright 0.1.0 (installed plugin), Mark's `GEMINI_API_KEY` (free tier). Decision: [../decisions/2026-10-15-thread-reader-fetchwright.md](../decisions/2026-10-15-thread-reader-fetchwright.md). Counts only: no fetched text, no usernames.

## Method

- Listings: `fetch --beat ai-video --kinds reddit --peek --json --all --reddit-reader arcticshift --max-age-days 3` (660 posts, window ending 36 h back so counts had settled).
- Nine threads were picked by size, media and deleted comments, using the Arctic Shift comment tree for reference counts.
- Each thread was read three ways: Arctic Shift (the reference), Reddit's feeds (Mark's current reader, `auto` = `rss` until 2026-11-13), and `load_thread(..., reader="fetchwright")`.
- A comment "matches" when its normalised text shares a 20 to 60 character prefix with an archive comment, or a 0.8 similarity ratio.
- Handles: any archive author name of 4 or more characters found as a word in a fetchwright comment. Placeholders: `[deleted]`, `[removed]`, "removed by", "deleted by".
- Scripts in the session scratchpad (not committed): `arctic_scan.py`, `compare.py`.

## Results

| thread | reference comments (archive, collapsed) | feeds | fetchwright | matched archive | not in archive | handles | placeholders | OP marked (archive) | model | page / output tokens | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| r/comfyui, 22 comments, 2 deleted | 22 (0) | 21 | 20 | 20 | 0 | 0 | 0 | 7 (8) | gemini-3.8-flash | 5,060 / 1,647 | 21.5 |
| r/StableDiffusion, 183 comments + 18 collapsed, 5 deleted | 183 (18) | 190 | not read | - | - | - | - | - | - | - | 78.9 |
| r/Filmmakers, 76 comments, 3 deleted | 76 (0) | 75 | 72 | 72 | 0 | 0 | 0 | 10 (10) | gemini-3.5-flash-lite | 6,180 / 2,940 | 8.5 |
| r/StableDiffusion, 75 comments, 2 deleted | - | - | stopped: 429 | - | - | - | - | - | - | - | - |

- Titles matched exactly on both reads. Bodies matched 0.97 and 0.99.
- fetchwright dropped 2 lone tokens (likely handles returned as comments) on the Filmmakers thread. None got through as text.
- Nothing came back that the archive did not hold, and no deleted comment's old text came back.
- The bare permalink `/r/<sub>/comments/<id>/` (the form Arctic Shift listings carry) read fine: Google answered `success` for the slug URL and `error` for the bare one, as in Stage 1.
- Not read, the 183-comment thread: after 79 s the model's answer was not the JSON asked for. The likely cause is an answer cut off on a long thread; unverified, because everscout does not keep fetchwright's `unparsed` text. everscout now passes `fetchwright.max_comments` (config) as `--max-comments`, so a cap can be tested.
- Stopped, the fourth thread: HTTP 429 from Google, "Rate limit exceeded for model gemini-3.8-flash (limit: 20 requests per day on Free Tier). Please retry in 22h3m56s". This session made about 5 Gemini calls (each read tries `gemini-3.8-flash` first). Earlier sessions the same day (Stage 1, fetchwright's tests and smoke runs) used the rest.
- everscout did what the decision says: exit 3, a cool-down in `~/.everscout/local/cooldown.json`, and every later fetchwright read refuses at once. The cool-down now follows Google's "retry in" time (here to 2026-10-17 00:00 UTC), never less than an hour.

## What it means

- Where the reads worked, quality matches Stage 1: 92 of 98 reference comments came back across two threads, all of them real, with no handles and no deleted text. The feeds returned about as many (96).
- Coverage of long threads is still the weak point, and now a failure mode as well as a shortfall.
- The free-tier daily limit decides the design. 20 requests a day on `gemini-3.8-flash` is about one weekly scan's worth of kept threads, shared with every other use of the key. `gemini-3.5-flash-lite` has its own limit, a forum claims 500 a day (unverified), and it read every thread in Stage 1.
- fetchwright stops at the first 429 and does not try the next model. That honours rule 17, but a per-model daily quota on the first model blocks the whole route. Whether a quota 429 on one model may fall through to another is Mark's call, and a fetchwright change.
- Too small a sample to pass the plan's gate (four of six threads readable): two of three attempts read. The wiring is opt-in and off by default, but the gate was not met, so the PR waits for Mark.

## Next

- After 2026-10-17 00:00 UTC, with Mark's go-ahead, finish the sample with `fetchwright.models` set to `gemini-3.5-flash-lite` (or flash-lite first), and test `fetchwright.max_comments` 100 on the long thread.
- Then run one real everscout-scan of ai-video with `--thread-reader fetchwright`.
