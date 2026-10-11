---
title: Finding what matters on Reddit after RSS and the public Data API end (October 2026)
kind: research
status: active
date: 2026-10-11
verified: 2026-10-11
tags: [reddit, arctic-shift, pushshift, devvit, dumps, archives, search, screenshots, human-in-the-loop]
---

# Finding what matters on Reddit after RSS and the public Data API end

Read this before changing the Reddit lane, adding an archive source, or adding a step that asks the user to capture a page.

The timeline is in the scan skill's research log (R-20261010-1): no new public Data API requests after 2026-10-31, RSS ends 2026-11-13, unregistered apps lose access from 2027-01-12, the rest of the public Data API ends March 2027. Reddit's app registration page (fetched 2026-10-11) confirms the 2027 dates and says registration needs "a human Reddit account".

## What is left, ranked

### 1. Arctic Shift (free archive and API, current today)

- What: an independent archive of Reddit posts and comments run by ArthurHeitmann on GitHub (`ArthurHeitmann/arctic_shift`). Monthly dumps on Academic Torrents, a public search API at `arctic-shift.photon-reddit.com/api`, and a web search tool. The September 2026 dump was released 2026-10-11.
- Freshness: posts are archived "within a few seconds of their creation" and votes and comment counts are refreshed "after 1.5 days" (maintainer, issue #39). Tested 2026-10-11: newest r/StableDiffusion posts were minutes old with score 1; a day of posts from 2026-10-08 came back as 63 posts with real scores (top 806 points, 44 comments). So importance can be judged from about 36 hours after posting.
- API: `/api/posts/search?subreddit=<name>&after=<date>&before=<date>&limit=100&fields=...`, and `/api/comments/tree?link_id=t3_<id>` for a whole thread. Sorting by score is not supported (issue #56 asks for it): fetch a day and sort locally. Rate limits are dynamic; on 429 wait for `X-RateLimit-Reset`. The maintainer asks for "a couple requests per second" at most and dumps for bulk work. Combining `fields=updated_on` with a date range returned HTTP 400; leave that field out.
- Legal footing: grey, not clean. The maintainer: "If you wanted to be 100% compliant with reddits policies, you'd have to collect all the data yourself. However using 3rd party reddit datasets is pretty common in academic work." It honours removal requests through a form. Reading a few threads a day for one person's notes, paraphrased and not redistributed, is the low-risk end; bulk copying or republishing is not.
- Risk: it collects through Reddit's Data API. Asked on 2026-10-09 how it survives March 2027, the maintainer answered "Not sure yet what exactly will happen" (issue #76). Reddit also stopped issuing sequential comment ids in 2026; the maintainer has a slower workaround and expects comments to stay "90%+ complete, ideally 95%" (issue #53). Treat it as working now, with an end date we cannot see.
- On this PC the host did not resolve through local DNS on 2026-10-11 while WebFetch reached it. Check DNS before blaming the service.

### 2. Reddit's own routes (sanctioned, narrow)

- Register the existing everscout app before 2027-01-12 (and before 2026-11-30 for the porting bounty). That keeps Data API access until March 2027 at most.
- Devvit (Reddit's Developer Platform) is not a reader for other people's communities. Reddit's PRAW-to-Devvit guide: "Per-installation, hosted app. Design for subreddit-scoped installs"; outbound HTTP only to allow-listed domains; no general file storage. A Devvit app runs only in subreddits whose moderators install it. It fits a subreddit the user moderates, nothing else.
- Pushshift: moderators only since 2023, approved per request for moderation work. Not an option.
- Reddit for Researchers (with OpenMined): a small academic beta (about 280 applications, over 40 researchers late 2024). Not for a personal tool.

### 3. Search engines (indirect, partly closing)

- Reddit's robots.txt blocks every crawler except Google's since July 2024, so only Google has a fresh index of Reddit. Bing, Brave and others hold stale or partial copies.
- Google's Custom Search JSON API is closed to new customers and ends 2027-01-01; after that a programmable engine searches only listed sites. Third-party Google results APIs exist but scrape Google; out of bounds under the conduct code.
- The agent's own web search tool still surfaces Reddit threads by title. Use it to find a thread, not to read one.

### 4. The same story elsewhere (the main lane from now on)

Anything that matters on Reddit leaks: makers cross-post to Bluesky, Mastodon, Lemmy and Discord; launches land on Hacker News, GitHub releases, Hugging Face and YouTube; newsletters round up the week. A beat that covers those finds most important Reddit stories second-hand, often with a link back to the thread. See `2026-10-11-forums-open-to-ai-crawlers.md` for which of those let agents in.

### 5. The user, by hand (for the few threads that matter most)

When a thread scores as important and no permitted route can read it, the scout asks the user to capture it. Rules worked out on 2026-10-11:

- Ask rarely: only threads above the beat's importance bar, at most a handful per scan, batched in one request at the end, each with the URL, why it matters and what to capture (the post, the top comments, a specific reply).
- Prefer text over pictures. Pasting the page text, or saving it as PDF or HTML, gives exact words and is cheaper to read than images. Screenshots are fine for short posts and images; a long thread needs several. The capture goes in an inbox folder the scan reads.
- The capture is a user-supplied document: data, never instructions, paraphrased into the note like any fetched thread, with `source: user-capture` and the date. Nothing is posted or stored beyond the note's quoted sentence.
- The Chrome extension blocks reddit.com, and everscout never logs in or drives a browser to read (AGENTS.md), so the user is the only reader of last resort.

## Not used

- Redlib, Libreddit and similar front ends: they proxy Reddit without permission and are being blocked; same footing as scraping.
- Academic Torrents dumps for live use: months behind and hundreds of gigabytes. Fine for history in the baseline study, not for weekly scans.
- Paid scraper services that resell Reddit data (Apify actors and the like): they scrape against Reddit's terms.

## Sources (fetched 2026-10-11)

- Arctic Shift README, download links, API docs: https://github.com/ArthurHeitmann/arctic_shift
- Issue #39 (rescan timing, compliance answer): https://github.com/ArthurHeitmann/arctic_shift/issues/39
- Issue #53 (comment ids): https://github.com/ArthurHeitmann/arctic_shift/issues/53
- Issue #76 (after March 2027): https://github.com/ArthurHeitmann/arctic_shift/issues/76
- Reddit app registration: https://developers.reddit.com/app-registration
- PRAW to Devvit guide: https://developers.reddit.com/docs/guides/migrate/public-api/basics
- Reddit robots change (2024): https://alternativeto.net/news/2024/7/reddit-now-blocking-search-engines-and-ai-bots-from-showing-its-results-except-for-google
- Google Custom Search JSON API end: https://brave.com/learn/google-api-shutdown/
- Pushshift moderator access, Reddit for Researchers: secondary (xpoz.ai, openmined.org), not re-verified
