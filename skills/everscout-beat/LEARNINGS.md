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
- Hypothesis: model labs push to the default branch without cutting releases; arXiv's API rate-limits by IP over a window of minutes, not per request
- Rule: before adding a `github` row, check `releases.atom` has entries; if not, use an `rss` row on `commits.atom`. For arXiv, prefer `rss.arxiv.org/rss/<cat>` with a filter, and never hit the API by hand right before a probe
- Evidence: ai-video refresh 2026-09-27
- Scope: everscout-beat procedure A step 4
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-09-27

### L-004 · 2026-09-26 · A verification fetch used up the first scan's new items
- Trigger: building tech-hiring, `fetch --sources ... --all --max-age-days 14` to read posts for the vocabulary marked 656 items seen; the first scan would have reported nothing new. A multireddit batch also fetched subreddits that were not asked for (9 sources for 6 named)
- Hypothesis: every fetch writes the seen set and `last_fetch`; `--all` changes only what is printed
- Rule: while building or answering, fetch with `--peek` (0.2.0), which saves neither; if a plain fetch already ran on an unscanned beat, clear `seen` in `LOCAL/state-<slug>.json`
- Evidence: tech-hiring build 2026-09-26; state reset by hand; test `test_peek_leaves_items_new`
- Scope: everscout-beat procedure A4; everscout-ask step 4
- Status: resolved 2026-09-26 by C-20260926-4 · helpful 1 · harmful 0 · last_confirmed 2026-09-26

### L-005 · 2026-09-26 · Claude Code's web fetch refuses old.reddit.com too
- Trigger: WebFetch of `old.reddit.com/r/cscareerquestions/about/rules` and `/r/ExperiencedDevs/about/rules` answered "Claude Code is unable to fetch from old.reddit.com"
- Hypothesis: the fetch tool blocks Reddit hosts outright, not just the new site's JavaScript
- Rule: for rules, search `"r/<name>" rules` and read the sidebar text the results quote (reddifier.com quoted r/ExperiencedDevs' 3-years rule), or a Wayback snapshot; mark the row `~` unless the rules text itself was read
- Evidence: tech-hiring build 2026-09-26
- Scope: everscout-beat procedure A4
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-26

### L-006 · 2026-09-26 · The CLI stamps dates in UTC
- Trigger: at 19:57 US Central on 2026-09-26 the probe saved `probe-2026-09-27.json` and the data HANDOFF said "Updated 2026-09-27"
- Hypothesis: `today()` is `now_utc()`; in the Americas' evening files carry tomorrow's date
- Rule: expect the one-day skew; beat files and log lines written by hand use the user's local date, and a missing `probe-<local date>.json` is not a failed probe
- Evidence: tech-hiring build 2026-09-26
- Scope: all everscout skills
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-09-26
