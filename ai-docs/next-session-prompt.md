# Next session: release Reddit discovery, then measure it on real scans

Written 2026-10-16. Run from the folder that holds the everscout clones. The everscout repository is `Ai/everscout` (public, m4bwav/everscout). Its main clone may hold another session's uncommitted edits, so work in a worktree off origin/main (`Ai/everscout-wt-urlctx` was used last).

## Where things stand

- Reddit discovery without a listing is built and merged to main, unreleased: pickup of Reddit links during `fetch`, `discover list|add|mark`, `captures`, `new-note --capture`, and `fetchwright.max_reads_per_scan` (exit 6). The everscout-scan skill's Step 2 and procedure section G say how a scan uses them. Plan and status: `ai-docs/plans/2026-10-16-reddit-discovery-after-arctic-shift.md`.
- First live check: a week of ai-video's non-Reddit sources linked no Reddit thread (`ai-docs/research/2026-10-16-reddit-pickup-coverage-live.md`). YouTube feeds were down, so video descriptions were not checked.
- Also unreleased on main: the YouTube outage line in `fetch`, and the ai-video metric changes.

## Read first

1. `AGENTS.md`, then the first section of `ai-docs/HANDOFF.md`.
2. The plan's Status section and the research note above.

## Next steps

1. **Ask Mark whether to release 0.6.0** (minor: new CLI commands and config). On a yes: bump `.claude-plugin/plugin.json` and `VERSION` in `scripts/everscout.py`, turn the root CHANGELOG's Unreleased into `## 0.6.0 · <date>`, tag `v0.6.0`, and run `gh release create v0.6.0 --title "everscout 0.6.0" --notes-file <that section>`. Then update the installed plugin.
2. **On the next ai-video scan** (or any beat's), follow the skill as written: read the `discover list` coverage line and write the number into the research note. Check whether the YouTube feeds answer again; if they do, see whether video descriptions link Reddit.
3. **Try pickup on a beat with HN and Bluesky sources** (tech-hiring or indie-ai-games) to see whether coverage is better than on ai-video.
4. Standing: Reddit app registration before 2027-01-12 is Mark's call. Arctic Shift after March 2027 is unknown (maintainer issue #76).

## Limits

- Opt-in only; nothing may make a key required.
- Never Gemini's Google Search, and never find Reddit URLs through Gemini.
- Never retry a 429 within the hour, and honour Google's stated retry time. Never retry GDELT while its cool-down runs.
- Notes follow conduct rule 16: paraphrase, one short quote at most, no handles, drop deleted text. Captures are the user's own reading and are never redistributed.
- Never commit fetched text, real usernames or a recorded response.
- Tagging and publishing need Mark's explicit go-ahead.

Before you finish, write the next session's prompt to this file, and end it with this same instruction.
