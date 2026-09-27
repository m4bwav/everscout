---
title: Beat statistics live in a per-beat catalog and one append-only CSV, reviewed by explicit rules
kind: decision
status: active
date: 2026-09-27
verified: 2026-09-27
tags: [metrics, statistics, series, lifecycle, chartwright, gdelt, wikimedia]
summary: read before changing metrics.md, series.csv, the stats command, its adapters or the promote and archive rules
---

# Decision: beat statistics (0.3.0)

## Context

Mark asked for each beat to gather statistics over time, propose new metrics, update and archive old ones, and feed charts through chartwright. The research and design are in [../research/2026-09-27-beat-statistics.md](../research/2026-09-27-beat-statistics.md); Mark approved the design on 2026-09-27.

## Decision

- The catalog is `metrics.md` in the beat folder (a flat table, so `beat-check` parses it). Values are one long-form CSV per beat at `DATA/stats/series.csv`, appended and never rewritten. A failed collection is a row with an empty value.
- One CLI command, `stats list|add|collect|review|export`, standard library only. No separate skill: the four existing skills route to `kb/stats.md` (define in beat, collect in scan, review and chart in report, read and propose in ask).
- Adapters: tally (from the notes; periods before the first note are left empty, not zero), GDELT DOC 2.0 timelines, Wikimedia pageviews, derived, manual. Values are per complete period (ISO weeks dated by Monday, months, quarters). The first collect backfills up to eight periods.
- Network reads use the shared paced fetcher, a 20 s timeout and no retries (`Fetcher.retry = False`), so a busy API costs one request and a gap row, and never stalls a scan. A non-JSON body (GDELT's rate-limit text) is removed from the cache.
- Promotion needs three points at grade C3 or better and the user's yes (`--promote`); `review` alone only proposes. `--apply` archives stale and flat metrics. Thresholds are defaults in `STATS_DEFAULTS`, overridable under `stats` in config.json.
- A change to definition, unit, source or method bumps `version`; export labels each version as its own series.
- Chartwright is optional: export finds `cw.py` next to the repository, in the Claude Code plugin cache, or at `$EVERSCOUT_CHARTWRIGHT` / config `chartwright`, and otherwise just writes the CSV.

## Rejected

- JSONL series: chartwright and spreadsheets read CSV.
- A fifth metrics skill: trigger competition (research note 5.4).
- Google Trends: only scrapers through proxies; against the conduct rules.
- Retrying 429s during collection (the feed fetcher waits up to six minutes; too long for a number that can be collected next week).
- Auto-promotion: the design requires the user's yes.

## Consequences

- Built-in beats ship candidates; editing a built-in beat's `metrics.md` warns that the beat should be copied to the private beat dir first.
- The thresholds are judgment. Revisit them after three months of real data (the research note says so).
