# GDELT DOC 2.0 refuses with 429 long after a burst

Date: 2026-09-27. Applies to: `stats collect` metrics with `gdelt:` or `gdelt-raw:` sources.

## Problem

During the 0.3.0 build, GDELT answered the first timeline call and then HTTP 429 for the rest of the session. The version-2 tech-hiring GDELT metric never got a value.

## Rate-limited or blocked?

Rate-limited with a penalty window, not banned by name. One careful probe (everscout User-Agent, `timespan=1week`) at 16:38 UTC, 10 minutes after the last call, still got:

```
HTTP/1.1 429 Too Many Requests
Server: GDELT Server
Please limit requests to one every 5 seconds or contact <GDELT contact> for larger queries. All high-traffic users should switch to our ngrams dataset: https://blog.gdeltproject.org/using-the-new-web-ngrams-dataset-to-find-relevant-coverage/. ...
```

No Retry-After header. So a burst earns a refusal window much longer than 5 seconds.

## What GDELT publishes

- No rate-limit page. The DOC 2.0 launch post (https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/, 2017-06-20) gives no quota. The refusal text is the only official statement: one request every 5 seconds, per IP as far as reports tell.
- Anecdotal: https://github.com/cyanheads/gdelt-mcp-server/issues/44 (2026) saw 429s at 5.2 s and at 30 s spacing and recommends spacing from completion and a shared gate. Other reports (search summaries only, unverified): blocks of about a minute, some lasting a whole session, and cloud or shared IPs refused on the first call. No User-Agent guidance found.

## Dead ends

- Retrying inside a run (the 0.3.0 fetcher at first): each retry extends the block.
- Treating the 6 s gap as enough: it keeps us under the published rate but does not end a block.

## Fix (0.3.1)

- Gap 10 s between completed GDELT calls (`es_sources.DEFAULT_HOST_GAPS`).
- A refusal (429, or the plain-text body) calls `Fetcher.set_cooldown`: 1 h, doubling for each refusal in a row, capped at 24 h, stored in `LOCAL/cooldown.json`. `stats collect` skips GDELT metrics while it runs and writes no failed row ("cooling" in the report). A success clears it.
- Test: `test_gdelt_refusal_starts_a_cooldown_that_collect_respects`.

## Verify

`python -m unittest discover -s tests` (46 tests). Live: `python scripts/everscout.py stats collect --beat tech-hiring` after the time in `LOCAL/cooldown.json` passes; expect `ok news-tech-layoffs` or `cooling`.
