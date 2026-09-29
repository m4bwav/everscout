---
title: Token-saving processes and scripts for everscout sessions
kind: solution
status: active
date: 2026-09-28
verified: 2026-09-28
tags: [tokens, cost, thread, ledger, followups, housekeeping, scripts]
summary: read before running thread, followups, ledger lookups or scan housekeeping in a session; lists what saved tokens on 2026-09-28 and the CLI additions that would save more
---

# Token-saving processes and scripts for everscout sessions

## Problem

Engagement and answer-filing sessions spend most of their tokens printing whole threads, re-fetching threads for answers the ledger already holds, and reading housekeeping output. Observed in the 2026-09-28 session (an r/aivideo ask, two answers filed on the indie-ai-games beat). "Net" below means the saving is larger than the cost of the extra command.

## Fix

In use now, no code change needed:


1. **Slice a thread with `--json` instead of printing it.** `thread <url> --json > <scratchpad>/t.json`, then a few lines of Python that print only the comments you need (for example the user's own comment and the five after it). The fishing-game thread has 126 comments. The text view prints the post and the first 60, about 4k tokens (all 126 in full would be about 7k). The slice printed 8 comments, about 350 tokens, measured from the saved JSON at 4 characters per token. The text view would also have missed the user's comment if it had been past number 60. Set `PYTHONIOENCODING=utf-8` or emoji in comments crash the print on Windows.
2. **Read a maker's answer from the ledger, not the thread.** `followups` stores the full reply in `engagements.jsonl` (`replies[].text`). One `grep <item id>` on that file costs a few hundred tokens and no Reddit request. The `thread` text view also cuts every comment at 600 characters, so it can hide the part you need (the BLOCKFALL art and sound answer was lost this way).
3. **Grep the beat before fetching anything.** When the user names a post by topic ("the fishing game"), `grep -ril <word>` over the beat's notes, HANDOFF and the ledger finds the note, the draft and the URL in one call. The alternative, fetching candidate threads, costs paced Reddit requests and whole threads.
4. **Run `followups` in the background.** It waits on Reddit's pace (20 to 60 seconds per request) and ran past the 120-second foreground timeout. In the background it costs nothing while other work continues.
5. **Trim housekeeping output.** `validate --strict | tail -2`, `tally > /dev/null` (unless the movers are the point), `index | tail -1`. The full outputs list every note and entity.
6. **Edit notes with a scripted assert-and-replace.** For several small changes to one note, one Python call with `assert old in s` per replacement changes the note in one go and fails loudly if the text moved. It saves one Edit round trip per change.
7. **`engage-check` before anything else.** It costs a few dozen tokens and ends the task early when the pace blocks it, before any thread is read.

Proposed CLI additions (not built). Each replaces a hand-written script that cost roughly 1k to 2k tokens to write and run.

- `engage-record --ts <iso>`, or better `engage-record --from-thread`: find the user's own comment in the thread by their handle, and fill `text`, `ts` (the comment's `published` time) and any replies. Needed whenever an ask was posted without a ledger entry. Without `--ts` a late record is stamped "now" and wrongly blocks the pace for an hour. On 2026-09-28 this took a hand patch of the JSONL.
- `thread --author <handle> [--context N]`: print only that person's comments and the N comments after each. This replaces the slice in item 1.
- `thread` text view: end a cut comment with `[cut]` and say when comments beyond `--limit` were dropped (`showing 60 of 126`). Agents then know to use `--json` or the ledger.
- `ledger --item <id> [--json]`: print one entry with its replies. This replaces grep plus a JSON parse.
- `followups --item <id>`: check one thread instead of every open ask on the beat (the full run took over two minutes).

Not worth it here: delegating these steps to the local Ollama models (local-delegate) saves nothing: every input is small and the work is judgment (which comment, what to record). Delegation pays for large logs, diffs and bulk classification, as in `scan` distillation.

## Verified by

Item 1: sizes measured from the saved `thread --json` of r/aigamedev 1ws5zlf on 2026-09-28 (text view about 16k characters, slice about 1.4k). Item 2: BLOCKFALL's ledger reply held the art and sound answer that the 600-character text view cut off. Item 4: `followups --beat indie-ai-games` moved to the background at the 120-second timeout and finished with `0 new replies`. The proposed additions are untested ideas.
