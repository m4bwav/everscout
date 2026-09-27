# Learnings: everscout-beat

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first: add, update, retire, or none.

Lessons inherited from indie-ai-scout (its LEARNINGS, 2026-09-18 to 2026-09-20) are folded into the procedures rather than copied: triage from the saved fetch file; fetch kept threads one at a time; never retry a block within the hour; a thank-you needs its own pace rule; drafts are handed over for pasting.

## Active

### L-001 · 2026-09-26 · A headless session kills background work when it ends
- Trigger: T-20260926-1, the probe was backgrounded and the run ended before it reported
- Hypothesis: `claude -p` (and any non-interactive harness) exits after the final message; background shells die with it
- Rule: never end the turn while a command the outcome depends on is still running; run it in the foreground or wait for it
- Evidence: T-20260926-1, C-20260926-2
- Scope: global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-26

### L-002 · 2026-09-27 · `probe --source X --save` overwrites the day's full snapshot
- Trigger: after the full probe, per-source probes of new rows each saved `probe-<date>.json`, leaving a one-row snapshot
- Hypothesis: `--save` writes the file for the date from this run's rows only; it does not merge
- Rule: probe new rows without `--save` (or with it, then finish with one full `probe --beat <slug> --save`); the saved snapshot is the full run. The full rerun is fast the same day because feeds come from cache
- Evidence: ai-video refresh 2026-09-27, snapshot held 1 row until the full rerun
- Scope: everscout-beat procedure B and step 3
- Status: resolved 2026-09-27 by C-20260927-1 (`--save` now merges a partial probe into the day's snapshot); kept for the record

### L-003 · 2026-09-27 · GitHub model repos often publish no releases; a manual arXiv API check triggers the 406 cooldown
- Trigger: Wan-Video/Wan2.2, Lightricks/ComfyUI-LTXVideo, MiniMax-AI/MiniMax-H3 releases.atom had 0 entries (tags too); a curl to the arXiv API followed minutes later by the probe got HTTP 406
- Rule: before adding a `github` row, check `releases.atom` has entries; if not, use an `rss` row on `commits.atom`. For arXiv, prefer `rss.arxiv.org/rss/<cat>` with a filter, and never hit the API by hand right before a probe
- Evidence: ai-video refresh 2026-09-27
- Scope: everscout-beat procedure A step 4
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-09-27

