# Next session: Stage 2 of the Gemini URL context reader for Reddit (after Mark picks its shape)

Written 2026-10-15 (evening). Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repo is `Ai\everscout` (public, m4bwav/everscout); its main clone holds another session's uncommitted edits, so work in a worktree off origin/main.

## Where things stand

- everscout 0.4.0 reads Reddit through the Arctic Shift archive (opt-in; Mark's config is `auto`, switching on 2026-11-13 when Reddit's feeds end). Arctic Shift collects through Reddit's Data API, which ends March 2027.
- The backup route: find Reddit thread URLs without Gemini's search, have Gemini read each one with its URL context tool, then Claude distils. **Stage 1 passed on 2026-10-15 on `gemini-3.5-flash-lite`**: six of six threads with the right title and body, 47 real comments in the settled thread, no comment shown invented, placeholders instead of removed text. `gemini-3.8-flash` was overloaded (503 or a 60 s drop on every call) and is untested.
- Gemini's Google Search tool stays ruled out for this route (Google's terms, `ai-docs/research/2026-10-15-reddit-through-gemini.md`). Do not reopen it unless Google's terms page changes.
- `GEMINI_API_KEY` is set at user level and works (project 268277778089, free tier as far as known).

## Read first

1. `everscout/ai-docs/research/2026-10-15-gemini-url-context-reddit-test.md`, the results and what a reader must handle.
2. `everscout/ai-docs/plans/2026-10-15-reddit-via-gemini-url-context.md`, Stage 2.
3. `everscout/ai-docs/notes/2026-10-15-gemini-url-context-probe.md`, the probe script (a good starting point for the reader's request code).
4. `everscout/kb/conduct.md` rules 16 and 17, `kb/platforms.md` Reddit rows.

## The next step and its limits

1. Check whether Mark has chosen the Stage 2 shape: look at the end of `ai-docs/log.md` and the plan's status line. The choices are a standalone public plugin that reads pages other fetchers cannot (the plan recommends it: everscout stays keyless by default and the reader is useful beyond Reddit), a reader inside everscout (`reddit.thread_reader: gemini`), or both, with everscout calling the plugin's CLI. If no choice is recorded, ask him once and stop.
2. Build what he chose, as the plan's Stage 2 says. The reader must: try `gemini-3.8-flash` and fall back to `gemini-3.5-flash-lite` on 503 or a 60 s drop; never send `google_search`; drop items whose text is a lone username, and drop "Comment removed by moderator" or "Comment deleted by user" placeholders; record each `url_context_result` status; read the key from the environment, never print it or write it to a file.
3. Offline tests on recorded responses (key and handles scrubbed) and one live smoke test that skips without a key. Conduct rule 17 and `kb/platforms.md`: a row for the route, the "never Google Search for discovery" line, the free-tier privacy line.
4. A standalone plugin is a new public repo: README banner, SECURITY.md, size budget with green, yellow and red limits, icon, wiki. Creating the repo was approved in the original kickoff; tagging and releasing need Mark's go-ahead.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`; no AI attribution anywhere.
- Document as you go (ai-docs log, research, plan status, HANDOFF); kill processes by PID only.
- No README or doc may call the route "legal"; state what the terms say and what is untested.
- Merge your own PRs once checks pass, unless the change is a release or publish workflow or a public API; tagging, releases and publishing need Mark's go-ahead. Batch what needs his hands into one message.

## When to stop and ask

When the shape is not chosen; when the key stops working; if Gemini starts returning text from deleted or removed posts (decide with Mark how notes treat it); if requests start failing with refusals or 429s (record and stop, conduct rule 17); before any release.

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
