# Next session: the Gemini URL context route now lives in fetchwright

Written 2026-10-15 (night). Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repository is `Ai\everscout` (public, m4bwav/everscout); its main clone holds another session's uncommitted edits, so work in a worktree off origin/main (`Ai\everscout-wt-urlctx`).

## Where things stand

- Stage 2 of `ai-docs/plans/2026-10-15-reddit-via-gemini-url-context.md` is built as its own public plugin, **fetchwright** (name agreed with Mark on 2026-10-15). Its repository is github.com/m4bwav/fetchwright and its clone is `Ai\fetchwright`. Version 0.1.0 is on main, not released.
- Here: conduct rule 17 and a `kb/platforms.md` keyed-sources row for the route (PR #18).
- everscout 0.4.0 still reads Reddit through Arctic Shift (Mark's config `auto`, switching on 2026-11-13). Arctic Shift is expected to stop in March 2027.

## Read first

1. `fetchwright/ai-docs/next-session-prompt.md`: the main line of work continues there (evals, wiki, re-testing gemini-3.8-flash).
2. `ai-docs/plans/2026-10-15-reddit-via-gemini-url-context.md`, the Status line and Stage 2 step 4.
3. `kb/conduct.md` rule 17 and the `kb/platforms.md` keyed-sources section.

## The next step and its limits (everscout side)

1. Only after Mark agrees: let `everscout.py thread` call `fetchwright.py read --json` as a subprocess when config `reddit.thread_reader` is `fetchwright`, for after Arctic Shift stops. That needs a decision record, tests with synthetic fixtures, and a minor version. everscout stays keyless by default.
2. Discovery after Arctic Shift (plan Stage 2 step 4): the agent's own web search and Reddit links found in Hacker News, Bluesky, Mastodon and newsletter items. Never Gemini's Google Search.
3. Release the knowledge change from PR #18 with the next everscout version (needs Mark's go-ahead).

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Document as you go: the ai-docs log, plan status and HANDOFF. Kill processes by PID only.
- No README or doc may call the route "legal". State what the terms say and what is untested.
- Merge your own PRs once checks pass, unless the change is a release or publish workflow or a public API. Tagging, releases and publishing need Mark's go-ahead. Batch what needs his hands into one message.

## When to stop and ask

- Before wiring everscout to fetchwright.
- When the key stops working.
- If Gemini starts returning text from deleted or removed posts.
- If requests fail with refusals or 429s (record and stop, conduct rule 17).
- Before any release.

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
