# Next session: finish the live test of everscout's fetchwright thread reader

Written 2026-10-16 (01:56 UTC stop). Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repository is `Ai\everscout` (public, m4bwav/everscout). Its main clone holds another session's uncommitted edits, so work in the worktree `Ai\everscout-wt-urlctx`, branch `feat/thread-reader-fetchwright` (the open PR).

## Where things stand

- The wiring is built and tested (65 offline tests), and the PR is open, **not merged**:
  - config `reddit.thread_reader` (`same` or `fetchwright`) and `--thread-reader` on `thread` and `new-note`;
  - config `fetchwright.cli|models|max_comments|timeout_seconds`;
  - a subprocess adapter in `load_thread`, a cache, a 5 s pace, and a cool-down on a 429 that follows Google's retry time.
- Decision: `ai-docs/decisions/2026-10-15-thread-reader-fetchwright.md`.
- Live results so far, in `ai-docs/research/2026-10-15-fetchwright-thread-reader-live.md`:
  - two threads read well (20 of 22 and 72 of 76 comments, all real, no handles);
  - a 183-comment thread came back as broken JSON;
  - then a 429: the free tier allows `gemini-3.8-flash` **20 requests a day**.
- fetchwright tries `gemini-3.8-flash` first and stops at a 429 instead of trying `gemini-3.5-flash-lite`.
- The cool-down in `~/.everscout/local/cooldown.json` runs to **2026-10-17 00:00 UTC**. Do not call Gemini before then, and never edit the file to shorten it.

## Read first

1. `AGENTS.md`.
2. The decision and research notes above.
3. The PR's diff: `scripts/everscout.py` (`read_fetchwright`, `thread_from_fetchwright`, `load_thread`).
4. Mark's answers, if he gave any, to these questions:
   - may a 429 on one model fall through to the next (a fetchwright change);
   - should flash-lite run first;
   - may the PR merge.

## The work, once the cool-down has passed and Mark has answered

1. **Finish the sample.**
   - Set `fetchwright.models` in `~/.everscout/config.json` to what Mark chose (for example `gemini-3.5-flash-lite,gemini-3.8-flash`).
   - Read six to eight more settled ai-video threads with `thread --thread-reader fetchwright --json`.
   - Include one long thread with `fetchwright.max_comments` 100.
   - Compare with Arctic Shift and the feeds the same way as before: counts only.
   - Rebuild the comparison script if the scratchpad is gone. The method is in the research note.
2. **Gate.**
   - Four of six readable: merge the PR (tests must pass).
   - Fewer than four: stop and report to Mark.
3. **Scan.** Run one real everscout-scan of ai-video with `--thread-reader fetchwright` on `thread` and `new-note`, and distil notes into Mark's data folder (`ES where --beat ai-video`), never the repository. The last full scan was 2026-10-10.
4. **Write it down.** Update the research note, the `kb/platforms.md` row (then `python scripts/sync-skill-refs.py`), the changelogs, `ai-docs/log.md`, HANDOFF, and the plan status.
5. **Release.** Tag v0.5.0 and publish the GitHub Release only with Mark's go-ahead.

## Limits

- Opt-in only; nothing may make a key required.
- Never Gemini's Google Search, and never find Reddit URLs through Gemini.
- Never retry a 429 within the hour, and honour Google's stated retry time.
- Budget: the free tier's 20 a day on `gemini-3.8-flash` is shared with every other use of the key. Count every call. fetchwright's `check` command also costs calls.
- Notes follow conduct rule 16: paraphrase, one short quote at most, no handles, drop deleted text.
- Never commit fetched text, real usernames or a recorded response.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Document as you go. Kill processes by PID only.
- No doc may call the route "legal".
- Merge your own PRs once tests pass and the gate is met. Tagging and releases need Mark's go-ahead.
- Batch what needs Mark's hands into one message.

## When to stop and ask

- When the key stops working, or on another 429.
- If Gemini returns text from deleted or removed posts.
- If live results fall below four of six.
- Before any release.

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
