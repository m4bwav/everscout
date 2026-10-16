---
title: Reddit threads may be read through fetchwright, opt-in, as a subprocess
kind: decision
status: active
date: 2026-10-15
verified: 2026-10-15
tags: [reddit, fetchwright, gemini, thread-reader, keys]
summary: read before changing how everscout reads a Reddit thread, or before making everscout depend on another plugin or a key
---

# Decision: Reddit thread reading can go through fetchwright, opt-in

## Context

Reddit's logged-out feeds end on 2026-11-13. Arctic Shift, the archive everscout 0.4.0 reads after that, has grey footing and an unknown future after March 2027. Stage 1 of `../plans/2026-10-15-reddit-via-gemini-url-context.md` showed that Gemini's URL context tool reads a public Reddit thread from Google's index, and the reader was built the same night as the separate public plugin [fetchwright](https://github.com/m4bwav/fetchwright) (0.1.0). On 2026-10-15 Mark asked to wire everscout to it now and test it live, without waiting for the feeds or Arctic Shift to end.

## Decision

- **Threads only.** A new config `reddit.thread_reader` takes `same` (the default: Reddit threads follow `reddit.reader`) or `fetchwright`. The `thread` and `new-note` commands take `--thread-reader` to override it. Listings stay on `rss` or `arcticshift`: fetchwright reads one URL a request and never searches, so it cannot list a subreddit.
- **A subprocess, never an import.** everscout runs `python fetchwright.py read URL --thread --json --max-chars 0` and maps the JSON onto its thread shape (`via: fetchwright`, no handles, the model, Google's retrieval statuses and token counts kept under `fetchwright` for the note's provenance). everscout keeps no Gemini code, needs no key, and stays standard-library. The CLI is found through config `fetchwright.cli`, then `FETCHWRIGHT_CLI`, then the installed plugin under `~/.claude/plugins/`; when it is missing, the command says which plugin and which setup skill to use, and exits 2.
- **Keyless by default.** Nothing changes for a user who does not set it. No command requires a key.
- **everscout's rules wrap it.** A host gap of at least 5 s for `generativelanguage.googleapis.com`; reads cached for `thread_ttl_seconds` and purged with the rest of the cache after 48 h; fetchwright's exit 3 (a 429) writes a cool-down to `cooldown.json` (Google's stated retry time when the message gives one, never less than an hour, doubling on repeats) and every later fetchwright read refuses at once until it passes (conduct rule 17); exit 4 points at the fetchwright-setup skill; exits 1 and 5 return "not read".
- **`followups` always uses the listing's reader.** It matches replies by author and time, which fetchwright does not return.

## Rejected options

- **Import fetchwright's module.** It would tie everscout's release cycle and Python floor (fetchwright needs 3.10, everscout 3.9) to another plugin, and put key handling inside everscout.
- **Call the Gemini API from everscout directly.** It duplicates fetchwright's retrieval checks, placeholder and handle drops and model fallback, and makes a public, keyless tool hold a key path.
- **fetchwright for listings too.** It reads one URL at a time and must never find URLs through Gemini's Google Search (the Gemini API terms forbid using grounded results to find pages to crawl), so it has no way to list new posts.
- **Make it the default, or the default after the feeds end.** It needs a personal key, free-tier prompts may be read by Google's reviewers, it drops handles and dates (follow-ups need both), and it returns long threads in part. An opt-in keeps everyone's default where it is.
- **Automatic fallback to fetchwright when the feeds or the archive fail.** It would send URLs to Google without the user having chosen it, and hide failures that the user should see.

## Consequences

- A note made from a fetchwright read has no author, no date from the thread (`new-note` takes the date from the fetched listing) and no scores. Long threads come back partly.
- A fetchwright read costs Gemini quota: about 3,000 to 15,000 page tokens and 600 to 10,000 output tokens a thread in Stage 1. The free tier's daily limit is not published.
- Evidence and live results: `../research/2026-10-15-fetchwright-thread-reader-live.md`.
