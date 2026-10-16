# Next session: finish the live test of everscout's fetchwright thread reader

Written 2026-10-16 (rewritten after Mark's answers, about 02:40 UTC). Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repository is `Ai\everscout` (public, m4bwav/everscout). Its main clone holds another session's uncommitted edits, so work in the worktree `Ai\everscout-wt-urlctx`, branch `feat/thread-reader-fetchwright` (the open PR).

## Where things stand

- The everscout wiring is built and tested (65 offline tests). PR #21 (branch `feat/thread-reader-fetchwright`) is open. Decision: `ai-docs/decisions/2026-10-15-thread-reader-fetchwright.md`. Results so far: `ai-docs/research/2026-10-15-fetchwright-thread-reader-live.md`. Two of three threads read well, a 183-comment thread broke the JSON, then the free tier's 20 a day on `gemini-3.8-flash` gave a 429.
- **Mark answered on 2026-10-16:**
  1. A 429 on one model's quota may move to the next model. Done in fetchwright PR #2 (merged on main, unreleased).
  2. flash-lite first. Mark's `~/.everscout/config.json` has `fetchwright.models` = `gemini-3.5-flash-lite,gemini-3.8-flash` and `fetchwright.cli` pointing at the clone `Aietchwright\skillsetchwright\scriptsetchwright.py`, which has the fall-through. The installed plugin is still 0.1.0.
  3. Merge #21 **and** tag and release everscout v0.5.0 once the gate passes. A fetchwright release (0.2.0) was not asked for; ask before tagging it.
- The cool-down in `~/.everscout/local/cooldown.json` runs to **2026-10-17 00:00 UTC**. Shortening it was refused as weakening a safeguard: never edit it, and wait.

## The work, after 2026-10-17 00:00 UTC

1. **Finish the sample.**
   - Read six to eight settled ai-video threads with `thread --thread-reader fetchwright --json`.
   - Include one long thread with `fetchwright.max_comments` 100 in the config. Take it out afterwards unless it helped.
   - Compare with Arctic Shift and the feeds as before: counts only. Rebuild the comparison script from the research note's method if the scratchpad is gone.
   - Record which model answered for each thread.
2. **Gate.**
   - Four of six readable: merge #21 once tests pass, then tag v0.5.0 and publish the GitHub Release (`gh release create v0.5.0 --title "everscout 0.5.0" --notes-file <the 0.5.0 CHANGELOG section>`). Mark said yes to this.
   - Fewer than four: stop and report to Mark.
3. **Scan.**
   - Run one real everscout-scan of ai-video with `--thread-reader fetchwright` on `thread` and `new-note`.
   - Notes go in Mark's data folder (`ES where --beat ai-video`), never the repository. The last full scan was 2026-10-10.
4. **Write it down.**
   - Update the research note, the `kb/platforms.md` row (then `python scripts/sync-skill-refs.py`), the changelogs, `ai-docs/log.md`, HANDOFF and the plan status.
   - In fetchwright, record the new learnings and the outcome of the long-thread cap.

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
- Before a fetchwright release (everscout 0.5.0 is approved once the gate passes).

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
