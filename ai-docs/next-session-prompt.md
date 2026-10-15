# Next session: test Gemini's URL context tool on Reddit threads (the post-2027 Reddit route)

Written 2026-10-15. Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repo is `Ai\everscout` (public, m4bwav/everscout); its main clone holds another session's uncommitted edits, so work in a worktree off origin/main.

## Where things stand

- everscout 0.4.0 (merged) reads Reddit through the Arctic Shift archive, opt-in (`reddit.reader`; Mark's own config is `auto`, switching on 2026-11-13 when Reddit's feeds end). Arctic Shift collects through Reddit's Data API, which ends March 2027, so Mark expects it to die then.
- Sending answers made with Gemini's Google Search tool to Claude is ruled out by Google's Gemini API terms (exact quotes in `everscout/ai-docs/research/2026-10-15-reddit-through-gemini.md`). Mark argued it with a Gemini chat twice; the terms text stands. Do not reopen it unless Google's terms page changes.
- The route Mark chose to pursue: find Reddit thread URLs without Gemini's search, then have Gemini read each URL with its URL context tool, then Claude distils. The plan, with the request format, the test cases, pass criteria and both outcomes, is `everscout/ai-docs/plans/2026-10-15-reddit-via-gemini-url-context.md`.

## Read first

1. That plan, in full.
2. The 2026-10-15 research note (what is ruled out and why).
3. `everscout/kb/conduct.md` rule 16 and 17, `kb/platforms.md` Reddit rows.

## The next step and its limits

1. Check for the key: `[Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')` in PowerShell (also `$env:GEMINI_API_KEY`). If it is missing, ask Mark once for it (aistudio.google.com/apikey, then `setx GEMINI_API_KEY "<key>"` and a VS Code restart) and stop. Never print the key, never put it in a repo file, never run a browser login.
2. Run Stage 1 of the plan: the scratch probe (standard-library Python in the session scratchpad), six Reddit threads chosen through `everscout.py fetch --reddit-reader arcticshift --peek` and `thread`, plus one non-Reddit control page, paced a few seconds apart. Do not use the `google_search` tool anywhere in this route.
3. Write the results into `everscout/ai-docs/research/2026-10-<day>-gemini-url-context-reddit-test.md` (statuses, token counts, fidelity against Arctic Shift, fabrication check, free-tier behaviour), a log line, and the plan's status. Docs-only PR, merge it yourself.
4. If it passes, put the Stage 2 shape question to Mark (standalone public plugin, everscout reader, or both; the plan recommends the standalone plugin) before writing code. If it fails, record why and stop.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`; no AI attribution anywhere.
- Document as you go (ai-docs log, research, plan status, HANDOFF); kill processes by PID only.
- No README or doc may call the route "legal"; state what the terms say and what is untested.
- Tagging, releases and publishing need Mark's go-ahead; batch what needs his hands into one message.

## When to stop and ask

When the key is missing; after Stage 1, before any Stage 2 code; if Gemini returns text from deleted or removed posts (decide with Mark how notes treat it); if requests start failing with refusals (record and stop, conduct rule 17).

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
