---
name: everscout-report
description: "Write what an everscout beat has learned: the dated radar-style trend report (direction, entities new, rising, steady or fading with tally counts, Adopt, Trial, Assess, Hold rings with rationale, notable threads, maker answers, reception, open questions), a weekly digest, the beat's metric review and charts, or the baseline study, a multi-chapter history and guide to the subject written STORM style from an approved outline. Every claim cites a note and every link is checked. Use whenever the user says 'report', 'write the trend report', 'what's hot', 'which tools are rising', 'what changed this month', 'chart the metrics', 'weekly digest', 'summarize what the scout found', 'build the baseline', 'write the study', 'refresh the study', or wants the direction, history of or a guide to a subject they have a beat for. Also for 'refresh everscout-report' and 'is everscout-report stale'. Fetching and distilling is everscout-scan; setting up the subject is everscout-beat."
---

# everscout-report

Outcome: a dated report under `DATA/reports/` (or a digest, or study chapters under `DATA/study/`) with the frontmatter in `kb/SCHEMA.md`, every ranking backed by `signals/tallies.json`, every claim linked to a note, `ES lint --beat <slug>` exiting 0, indexes regenerated, and a log line. Evidence: the file, the lint and index output, the log line.

Plugin root: two levels above this file. `ES` = `python "<plugin root>/scripts/everscout.py"`. `DATA` = the path `ES where --beat <slug>` prints. Method (signals, rubric, radar rings, faithfulness): [references/kb/method.md](references/kb/method.md). Procedures: [references/report.md](references/report.md) (reports and digests) and [references/study.md](references/study.md) (the baseline study).

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `verify_at_use` is true, re-check the due `volatile_claims` before relying on them, one search each, then stamp them (`evergreen.py claims <unit> --stamp due`). If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run the refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh unless the task depends on the stale claim.

## Step 1: route

| Ask | Mode | Writes |
|---|---|---|
| "report", "what's hot", "direction", "what changed", monthly by the beat's cadence | report | `reports/<date>-radar.md` |
| "digest", "this week", "catch me up" (short) | digest | `reports/<date>-digest.md` |
| "baseline", "history", "study", "guide", first report with an empty `study/` | study | `study/00-overview.md` and chapters, after the outline is approved |
| "refresh the study" | study-refresh | edited chapters, `verified` bumped |

A report needs notes: with fewer than ten notes in the period, say "thin: N notes" and offer a scan first (a report on nothing is a guess). The study does its own research and can start from zero notes.

## Step 2: do it

Report and digest: `ES tally --beat <slug>` first, then references/report.md. A radar also runs the metric review and charts (`ES stats collect`, `ES stats review`, `ES stats export --charts`; [references/kb/stats.md](references/kb/stats.md)): a Metrics section, promotions only on the user's yes, `--apply` only after saying what it archives. Every "new", "rising" or "fading" claim quotes the tally's numbers; every blip links at least one note; the rubric and rings come from kb/method.md; practitioner answers come from the ledger's replies (`ES ledger --beat <slug> --days 90 --json`); the user's `journal.md` is read and may be quoted. Study: references/study.md, chapter by chapter, each written to disk before the next, with `DATA/HANDOFF.md` updated between chapters because a study can span sessions.

## Step 3: prove and log

`ES lint --beat <slug>` must exit 0: fix broken links, and replace any external link no note holds (an unheld URL is either a claim with no note, so write the note, or a URL from memory, so remove it). `ES index --beat <slug>`. Append `## [date] report | <title>` (or `digest`, `study`) to `DATA/log.md`.

## Output

Report: the path, then the Direction section verbatim (three to six sentences), then the movers in one line, then what is due next. Digest: the path and its five bullets. Study: the chapter list with paths and one-line status each.

## Rules

- Numbers over adjectives; "thin: N notes" where data is thin; "unverified" where it is.
- No hype-cycle stages; no trend without its cluster (kb/method.md).
- URLs only from notes; quote before paraphrasing; keep hedges.
- Handles never appear in reports; "a maker in r/X said" is enough.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (check existing entries first: add, update, retire, or nothing). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (topic: how to turn community monitoring into faithful trend reports and a sourced baseline study: horizon-scanning signal methods, radar formats, citation faithfulness; tier `medium`, currently every 30 days, next due 2026-10-26). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`; procedures in `references/`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
