---
title: Building the tech-hiring beat from scratch (sources, stances, data, what failed)
kind: research
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [beats, tech-hiring, reddit, feeds, labour-data, test]
summary: read before editing beats/tech-hiring or building another beat from scratch; which sources were verified, what could not be, the data context on the day, and what the build taught the skill
---

# Tech-hiring beat research (2026-09-26)

Mark asked for "a scout for developer and tech hiring" as a test and for use. It is the first beat everscout-beat built with no starter to copy. No interview questions were asked (Mark prefers no needless stops); the scope defaults to both sides of the table (candidates, hiring managers and recruiters) plus labour data, with engagement allowed only where the rules permit it and only for people who publish their own search or hiring data.

## Sources found and verified

- Reddit (15): r/cscareerquestions, r/csMajors, r/ExperiencedDevs, r/cscareerquestionsEU, r/cscareerquestionsCAD, r/developersIndia, r/leetcode, r/recruitinghell, r/recruiting, r/EngineeringManagers, r/humanresources, r/jobs, r/layoffs, r/h1b, r/overemployed. All answered the probe on 2026-09-26 (items per feed: 3 to 63). Four are `scan: no` (broad or off-topic), kept for reference.
- Hacker News (5 queries): "Ask HN: Who is hiring" and "Who wants to be hired" find the 2026-09-01 threads; "layoffs" (17 stories in the window), "interview" (50, broad, so the filter requires the word), "job market" (7).
- Feeds: Indeed Hiring Lab `/feed/` (monthly US snapshot and software postings analyses), the Pragmatic Engineer `/feed` (filtered to job-market issues), Crunchbase News `/feed/` (layoffs tracker). interviewing.io has no feed (four URLs 404); it is a `web` row.
- Google News: "tech layoffs", "software engineer hiring", "AI job interview cheating".
- Mastodon: #layoffs@mastodon.social (scanned, filtered); #GetFediHired (job ads, reference only).
- Data pages (web rows): layoffs.fyi, TrueUp layoffs, FRED series IHLIDXUSTPSOFTDEVE (Indeed software development postings), BLS JOLTS.

## What could not be verified

Subreddit rules: Claude Code's web fetch refuses both reddit.com and old.reddit.com. Only r/ExperiencedDevs' "3+ years of experience to post or comment outside the weekly Ask thread" was confirmed, through a third-party page quoting the sidebar (reddifier.com). Every Reddit stance is `~`. Bluesky was not searched for a hiring feed generator; worth a look at the next refresh.

## Data context on the day (for the first answers and the study)

- Indeed Hiring Lab, 2026-07-23: 71 percent of the increase in software development postings between May 2025 and May 2026 came from senior roles; 37 percent from titles mentioning AI. Entry-level share of software postings 4.5 percent in Q1 2026. Postings up about 14 percent year over year but still roughly 30 percent below February 2020. https://hiringlab.indeed.com/2026/07/23/the-labor-market-is-tilting-toward-seniority/
- TrueUp, as quoted in September 2026 coverage: 622 tech layoffs affecting about 190,000 people so far in 2026. Unverified at the source.
- Reddit titles on 2026-09-26 show the live topics: company-specific online assessments and superdays, DoorDash's "AI Code Craft" interview (AI allowed), fake postings used to harvest résumés, "WITCH" offers for new grads, lying on résumés, background-check vendors.

## What the build taught the skill

`fetch` during a build used up the first scan's new items (fixed with `--peek`, everscout-beat L-004); rules pages need search, not fetch (L-005); the CLI's dates are UTC (L-006); aliases that are ordinary words (Indeed, Lever, EM, lottery) were caught and made specific before the first tally.
