# Next session: after everscout 0.5.0 (Reddit threads through fetchwright)

Written 2026-10-16 after the 0.5.0 release. Run from `D:\m4bwa\Claude\Projects\Ai`. The everscout repository is `Ai/everscout` (public, m4bwav/everscout); its main clone may hold another session's uncommitted edits, so work in a worktree off origin/main.

## Where things stand

- everscout 0.5.0 is released. Reddit threads can be read through fetchwright (opt-in: `reddit.thread_reader` or `--thread-reader fetchwright`); results in `ai-docs/research/2026-10-15-fetchwright-thread-reader-live.md`.
- fetchwright main has the quota fall-through (PR #2) but no release. Mark's `~/.everscout/config.json` points `fetchwright.cli` at the clone `Ai/fetchwright/skills/fetchwright/scripts/fetchwright.py` and runs `gemini-3.5-flash-lite` first.

## Read first

1. `AGENTS.md`, `ai-docs/HANDOFF.md`.
2. The research note above and `ai-docs/decisions/2026-10-15-thread-reader-fetchwright.md`.

## Next steps

1. **fetchwright 0.2.0**, only with Mark's go-ahead.
   - Bump every version field (fetchwright's AGENTS.md lists them), tag, and publish the release.
   - Update the installed plugin, then remove `fetchwright.cli` from Mark's config so everscout finds the installed copy.
2. **The ai-video beat's own follow-ups** (its data folder's HANDOFF):
   - seven YouTube channel feeds return 404;
   - the first monthly report is overdue;
   - GDELT 429s.
3. **Plan Stage 2 step 4 (discovery after Arctic Shift).** What fetchwright needs from it:
   - thread URLs in any form (the bare `/comments/<id>/` permalink reads);
   - threads at least a day old, so they are in Google's index;
   - a budget inside the daily quotas. flash-lite's limit is unverified; about 20 reads in one session drew no 429.

## Limits

- Opt-in only; nothing may make a key required.
- Never Gemini's Google Search, and never find Reddit URLs through Gemini.
- Never retry a 429 within the hour, and honour Google's stated retry time.
- Notes follow conduct rule 16: paraphrase, one short quote at most, no handles, drop deleted text.
- Never commit fetched text, real usernames or a recorded response.

## Rules

- Commit with `156112+m4bwav@users.noreply.github.com`. No AI attribution.
- Document as you go. Kill processes by PID only.
- No doc may call the route "legal".
- Merge your own PRs once tests pass. Tags and releases need Mark's go-ahead.

## When to stop and ask

- When the key stops working, or on a 429 from every model.
- If Gemini returns text from deleted or removed posts.
- Before any release.

When you stop, rewrite this file for the session after you: what to read first, the next step and its limits, the rules, when to stop and ask. Its last paragraph must give that session this same instruction.
