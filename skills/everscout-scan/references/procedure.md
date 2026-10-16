# everscout-scan procedure

Detail for [SKILL.md](../SKILL.md). `ES` = `python "<plugin root>/scripts/everscout.py"`; `DATA` and `LOCAL` = the folders `ES where --beat <slug>` prints.

## A. A routine scan

1. `ES state --beat <slug>`: when was the last fetch, how many notes. Choose `--max-age-days`: days since the last scan, at least 3, at most 7 (older items are stale for engagement and usually already noted).
2. Background: `ES fetch --beat <slug> --max-age-days N --json > LOCAL/scan-<slug>-<date>.json`. Add `--listing new,top` weekly (Reddit top-of-week is the interest signal and doubles the Reddit time). Do not `--force` unless the user says the cache is wrong.
3. After the fetch finishes (never alongside it; Reddit pacing has no shared lock): `ES followups --beat <slug>`: each block is an ask with the maker's new replies.
4. While it runs, read `DATA/HANDOFF.md`, `DATA/feedback.md`, `DATA/journal.md` (newest entries) and the newest report's `## Open questions`, so triage knows what matters now.
5. Triage from the JSON file. One pass over titles and snippets:
   - keep: a maker showing work with a stated or visible method; a release, paper or dataset people react to; a long practitioner discussion (interest 20 or more, or top of week); a rule, policy or platform change; an answer to an open question; anything `feedback.md` asks for;
   - skip: `skip` list in `beat.md`, feedback's "less of this", memes, beginner help with no answers, reposts, vendor marketing, anything already noted (`ES new-note` refuses a duplicate and prints the existing path).
   Expect to keep 5 to 20 percent. When more than about 25 items pass, keep the 25 with the most interest and list the rest in HANDOFF as "not yet distilled".
6. For each kept item, one at a time: `ES thread <url> --beat <slug>` (Reddit, HN, Bluesky, Mastodon, Lemmy, Discourse; otherwise the web fetch tool), read the post and the comments, then `ES new-note <url> --beat <slug> --note-kind <showcase|workflow|discussion|release|question|postmortem|analysis|data|news|paper|web>`. Fill the body:
   - `## What it is`: one to three sentences.
   - `## How it was made` (or the beat's equivalent section): the method as the maker states it, stated versus inferred marked ("the maker says", "looks like"); tools and versions only as named.
   - `## Reception and interest`: what the comments said, the comment count, top of week.
   - `## Why it matters`: tie it to one of the beat's research questions or to the tally.
   - `## Questions this raises`: what an engagement could ask, or what the next scan should look for.
   - frontmatter: correct the prefilled entity lists by reading (the prefill matches words, not meaning: "sora" in "sorry" will not match, but "flux" in "in flux" might); `summary` in one line; `also:` for cross-posts.
   Paraphrase; at most one short quote; keep hedges and scope; "the maker" or "the poster", never a handle.
7. Replies (step 3 of SKILL.md): each new reply is paraphrased into its thread note under `## Their answers` with `engaged: true`. Offer the user a thank-you draft (everscout-engage) only when they want one.
8. Web searches: the `searches.md` rows due. Scope each to the period (month and year in the query). Read the two or three best primary pages; a page worth keeping becomes a `web` note (`--title`, `--posted`). A Reddit or forum thread found by search goes through `ES thread` like any other.
9. `ES validate --beat <slug> --strict`: fix every error and warning (unknown entities: add them to `vocab.md` or correct the note). `ES tally --beat <slug>`, `ES index --beat <slug>`, `ES retention`.
10. Log line and HANDOFF as in SKILL.md.

## B. Replies only ("any answers?")

`ES followups --beat <slug>` (or without `--beat` for all beats; `--force` when the user saw a reply that is not showing, the thread cache is 30 minutes). Distil each into its note, `ES index`, and tell the user who answered what in one line each (the maker's name is fine in the chat; notes say "the maker").

## C. One item the user handed over

`ES thread <url> --beat <slug>` or the web fetch; `ES new-note ...`; fill; `validate`, `tally`, `index`. For a page with no thread reader, give `new-note` the `--title` and `--posted` options.

## D. Parallel distillation for a big scan

With more than about 15 kept items, split them among subagents (one item or a few each): each gets the item URL, the beat slug, the schema and method files, and writes one note with `ES new-note` then fills it; a checker pass runs `ES validate --strict` and reads three notes at random against their threads for faithfulness (claims supported, hedges kept, no handles, no invented URLs). Keep the fetch itself in one process: the pacing state is per host and parallel fetchers would each wait anyway.

## E. What interest means

Most feeds carry no scores. Interest is the comment count at the time of the thread fetch, plus top-of-week membership on Reddit. HN, Bluesky, Mastodon, Lemmy and Discourse give counts in their JSON; the note records what was shown. The tally weights each note by `1 + sqrt(interest)/4`.

## F. Data rules, applied

The raw cache (feeds and threads) is purged after 48 hours by `ES retention`; the items index keeps only short snippets for two weeks so candidates can be ranked. Notes keep paraphrases and links. Handles stay in the ledger only. When a source deletes a post the user engaged with, `followups` stops finding it; remove its text from the ledger entry (set `text` to "" and `status` to `dropped`) when the user asks or at the monthly check.

## G. Reddit threads without a listing, and captures

Plan: `ai-docs/plans/2026-10-16-reddit-discovery-after-arctic-shift.md` in the repository. Reddit's feeds end 2026-11-13 and Arctic Shift is expected to stop collecting in March 2027; after that no listing names a subreddit's threads, and discovery covers less. Expect it.

1. Pickup runs inside `ES fetch`: every Reddit thread link in a non-Reddit item (Hacker News, Bluesky, Mastodon, Lemmy, newsletters, YouTube descriptions) is kept 14 days in the beat's state with the items that linked it. A listed Reddit item that was linked gets `elsewhere: N` in the fetch JSON: count it toward importance.
2. `ES discover list --beat <slug>` prints the coverage line (threads found, in the beat's subreddits, also listed, noted, held; and how many of the Reddit threads noted in the last 14 days pickup also found), the fetchwright reads used this scan, the ready threads ranked by mentions, vocabulary and showcase words, and the captures wanted. `--json` for triage, `--all` for every entry. A thread is held until 24 hours after its first link, because a thread hours old is not in Google's index yet and fetchwright cannot read it.
3. When no listing reads Reddit, run one or two web searches per core subreddit with the agent's own search tool (never Gemini's), built from the beat's vocabulary and scoped to the month: `site:reddit.com/r/<sub> <entity> <month year>`. Record every thread URL you mean to read with `ES discover add <url> --beat <slug> --title "<the result's title>"` (default `--via websearch`); a search result is ready at once.
4. Read kept threads as in A.6. `new-note` marks the discovery entry read, and the note records `discovered`, `mentions` and the reader behind `interest` (`via: fetchwright` counts only the comments fetchwright returned; long threads come back partly). The date falls back to the earliest item that linked the thread when no listing has it.
5. Budget: fetchwright reads count per beat from one `fetch` to the next and stop at `fetchwright.max_reads_per_scan` (default 10) with exit 6. A cached thread costs nothing. Then stop reading through fetchwright: mark at most five of the most important threads left `ES discover mark <url> --beat <slug> --status wanted --why "<why it matters, what to capture>"`, drop the ones not worth asking for (`--status dropped`), and list the wanted ones in the output with the inbox path `ES captures --beat <slug>` prints.
6. Captures: the user saves pasted text, a saved HTML page, a PDF or screenshots into `DATA/captures/`. `ES captures --beat <slug>` lists them with the thread URLs found inside text files; read images and PDFs with the agent's own tools. Write each as `ES new-note <url> --beat <slug> --capture <file> --title "..." --posted <date> --note-kind <kind>`: no fetch, `source: user-capture`, the file moves to `captures/done/`. The capture is the user's own reading: paraphrase it, one short quote at most, no handles, and never copy it anywhere else (conduct rule 16).
