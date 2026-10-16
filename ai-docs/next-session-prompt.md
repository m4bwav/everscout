# Next session: build Reddit discovery (Stage 2 step 4)

Written 2026-10-16. Run from the folder that holds the everscout clones. The everscout repository is `Ai/everscout` (public, m4bwav/everscout); its main clone may hold another session's uncommitted edits, so work in a worktree off origin/main (`Ai/everscout-wt-urlctx` was used last).

## Where things stand

- everscout 0.5.0 is released. Since then, on main and unreleased: `fetch` prints one line when every YouTube feed fails (YouTube's feed server 404s for every channel at once, on and off, since December 2025). Evidence: `ai-docs/research/2026-10-16-youtube-feeds-and-gdelt-refusals.md`.
- Mark's ai-video data folder (`python scripts/everscout.py where --beat ai-video`) has its first monthly radar, `reports/2026-10-16-radar.md`. The beat's HANDOFF lists its follow-ups.
- Stage 2 step 4 (Reddit discovery after Arctic Shift) is planned, not built: `ai-docs/plans/2026-10-16-reddit-discovery-after-arctic-shift.md`.
- fetchwright 0.2.0 is released and installed; everscout finds it without `fetchwright.cli` (removed from Mark's config). Mark's config runs `gemini-3.5-flash-lite` first.
- Mark's answers on 2026-10-16: ai-video `wiki-text-to-video` promoted, `news-ai-video-share` archived (PR #23); build the discovery plan this session.

## Read first

1. `AGENTS.md`, `ai-docs/HANDOFF.md` (the "After 0.5.0" section).
2. The discovery plan and the research note above.

## Next steps

1. **Build the discovery plan, steps 1 to 5** (Mark said go on 2026-10-16): `reddit_ids_in`, pickup of Reddit ids during `fetch` (14-day purge), `discover list|add`, triage joins and ranking, `fetchwright.max_reads_per_scan` (default 10) with the rest listed as `captures-wanted`, then the everscout-scan skill text and a kb/platforms.md row. Synthetic-fixture tests for each CLI change; `python -m unittest discover -s tests` before committing. A minor release only with Mark's go-ahead.
2. **Measure coverage** while Arctic Shift lasts: on the next ai-video scan, compare what pickup found against the archive's full listing, and write the numbers into a research note.
3. **On that scan:** check whether the YouTube feeds answer again; if one channel answers and others still 404, those others need everscout-beat. The Bluesky feed generator is still off-topic (beat HANDOFF item 3). `notes-per-week` is up for review after November.

## Limits

- Opt-in only; nothing may make a key required.
- Never Gemini's Google Search, and never find Reddit URLs through Gemini.
- Never retry a 429 within the hour, and honour Google's stated retry time. Never retry GDELT while its cool-down runs.
- Notes follow conduct rule 16: paraphrase, one short quote at most, no handles, drop deleted text.
- Never commit fetched text, real usernames or a recorded response.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`. No AI attribution.
- Document as you go. Kill processes by PID only.
- No doc may call the route "legal".
- Merge your own PRs once tests pass. Tags and releases need Mark's go-ahead.
- `ai-docs/HANDOFF.md` has CRLF line endings; the other docs are LF. Keep each file's endings.

## When to stop and ask

- When the key stops working, or on a 429 from every model.
- If Gemini returns text from deleted or removed posts.
- Before any release, and before archiving or promoting a metric.
- Before adding a keyed search API (plan route D) or anything that needs Reddit app registration (route E): both are Mark's calls.

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
