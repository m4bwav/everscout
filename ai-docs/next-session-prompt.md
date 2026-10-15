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

Stage 1 was started on 2026-10-15 and is blocked on the key's project, not on URL context. Read `everscout/ai-docs/notes/2026-10-15-gemini-url-context-probe.md` first: it holds the probe script, the seven test cases, what happened, and what to try.

1. Check the key: `[Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')` (it was set on 2026-10-15, project 268277778089). Never print it, never put it in a repo file, never run a browser login.
2. Smoke test first: one plain `generateContent` call ("Say OK.") on `gemini-3.8-flash` with a 180 s timeout, and the same with `curl -m 180`. If it answers 200, go on. If it is still 403 or hangs, follow the note's "If the 403s persist" list; anything that needs the browser (checking the key's project or restrictions, a new key in a new AI Studio project) is Mark's: ask once and stop.
3. Run Stage 1: copy the probe from the note into the session scratchpad, replace the "fresh" case with a thread under a day old (the note says how), run all cases paced a few seconds apart. Do not use the `google_search` tool anywhere in this route.
4. Get ground truth with `everscout.py thread <url> --reddit-reader arcticshift --json` and score each case as the plan says (status, tokens, comments returned, exact-sentence match, fabrication, removed text).
5. Write `everscout/ai-docs/research/2026-10-<day>-gemini-url-context-reddit-test.md`, a log line, the plan's status, and update the note. Docs-only PR, merge it yourself.
6. If it passes, put the Stage 2 shape question to Mark (standalone public plugin, everscout reader, or both; the plan recommends the standalone plugin) before writing code. If it fails, record why and stop.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`; no AI attribution anywhere.
- Document as you go (ai-docs log, research, plan status, HANDOFF); kill processes by PID only.
- No README or doc may call the route "legal"; state what the terms say and what is untested.
- Tagging, releases and publishing need Mark's go-ahead; batch what needs his hands into one message.

## When to stop and ask

When the key is missing or its project still refuses; after Stage 1, before any Stage 2 code; if Gemini returns text from deleted or removed posts (decide with Mark how notes treat it); if requests start failing with refusals (record and stop, conduct rule 17).

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
