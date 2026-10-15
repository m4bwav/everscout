# Next session: Reddit lane steps 3-4, and the Gemini API as a backup to learn

Written 2026-10-15. Run from `D:\m4bwa\Claude\Projects\Ai`.

## Where things stand

- everscout 0.4.0 is merged (PR #12): Reddit through the Arctic Shift archive, opt-in by `reddit.reader` (`rss` default, `arcticshift`, `auto`); Mark's own `~/.everscout/config.json` has `auto`, so his scout switches on 2026-11-13. Live run on ai-video worked.
- The Gemini idea was checked and written up: `everscout/ai-docs/research/2026-10-15-reddit-through-gemini.md`. In short, Google's Gemini API terms forbid letting a third party (Claude) analyse, cache, mix or store answers made with the Google Search tool ("Grounded Results"), and the free tier gives new users no search grounding at all. A Gemini chat told Mark the opposite (that only training a competing model is forbidden); the terms page section "Grounding with Google Search" says otherwise. Do not build a route that hands grounded results to Claude.
- Mark wants Arctic Shift as the main lane and the Gemini API kept as a backup he can learn from.

## Read first

1. `everscout/ai-docs/HANDOFF.md` (0.4.0 section) and `plans/2026-10-11-reddit-lane-after-rss.md`.
2. The 2026-10-15 research note above.
3. `kb/conduct.md` rule 17 and `kb/platforms.md` (Reddit rows).
4. Vault PROFILE (`C:\Users\m4bwa\everlast-vault\user\PROFILE.md`, "Code and repos") before making any new public repo.

## Next steps, in order

1. everscout plan step 3: cross-platform pickup (a Reddit URL found in an HN, Bluesky, Mastodon or newsletter item counts toward that thread's importance). Small CLI change plus tests; worktree off origin/main (the main clone `Ai/everscout` holds another session's uncommitted edits). Merge once tests pass; no release or publish workflow is touched.
2. Plan step 4: capture requests (`captures-wanted` in the scan report, at most five, a beat `captures/` inbox read as user-supplied data with `source: user-capture`).
3. The Gemini backup, only after asking Mark which shape he wants:
   - a learning plugin for the Gemini API toolset (setup advisor: AI Studio key, tiers, quotas, privacy of the free tier; a small stdlib CLI), where answers made with Google Search are shown to Mark verbatim and never read by Claude, or
   - a test of the URL context tool on a reddit.com thread (its terms carry no Grounded Results clause; whether Google's fetcher reads Reddit is unknown). This needs Mark's key: check `GEMINI_API_KEY` in his environment first (it was not set on 2026-10-15); never run a browser login yourself.
   - Current model ids (2026-10-15): `gemini-3.8-flash` (stable), `gemini-3.5-flash-lite`; Gemini 2.5 is limited to past users. Re-check the models and pricing pages before pinning one.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`; no AI attribution anywhere.
- Document as you go (ai-docs log, research, decisions, HANDOFF); kill processes by PID only.
- Tagging, publishing a release, or making a new public repo for the Gemini work needs Mark's go-ahead; batch what needs his hands into one message.

## When to stop and ask

Before any Gemini code that sends Google Search results to Claude, before creating a public repo for the Gemini work, and if Arctic Shift starts refusing requests (record it and stop, conduct rule 17).

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
