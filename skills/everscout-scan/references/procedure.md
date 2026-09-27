# everscout-scan procedure

Detail for [SKILL.md](../SKILL.md). `ES` = `python "<plugin root>/scripts/everscout.py"`; `DATA` and `LOCAL` = the folders `ES where --beat <slug>` prints.

## A. A routine scan

1. `ES state --beat <slug>`: when was the last fetch, how many notes. Choose `--max-age-days`: days since the last scan, at least 3, at most 7 (older items are stale for engagement and usually already noted).
2. Background: `ES fetch --beat <slug> --max-age-days N --json > LOCAL/scan-<slug>-<date>.json`. Add `--listing new,top` weekly (Reddit top-of-week is the interest signal and doubles the Reddit time). Do not `--force` unless the user says the cache is wrong.
3. Background or after: `ES followups --beat <slug>`: each block is an ask with the maker's new replies.
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

`ES thread <url> --beat <slug>` or the web fetch; `ES new-note ...`; fill; `validate`, `tally`, `index`. For a page with no thread reader, pass `--title` and `--posted` to `new-note`.

## D. Parallel distillation for a big scan

With more than about 15 kept items, split them among subagents (one item or a few each): each gets the item URL, the beat slug, the schema and method files, and writes one note with `ES new-note` then fills it; a checker pass runs `ES validate --strict` and reads three notes at random against their threads for faithfulness (claims supported, hedges kept, no handles, no invented URLs). Keep the fetch itself in one process: the pacing state is per host and parallel fetchers would each wait anyway.

## E. What interest means

Most feeds carry no scores. Interest is the comment count at the time of the thread fetch, plus top-of-week membership on Reddit. HN, Bluesky, Mastodon, Lemmy and Discourse give counts in their JSON; the note records what was shown. The tally weights each note by `1 + sqrt(interest)/4`.

## F. Data rules, applied

The raw cache (feeds and threads) is purged after 48 hours by `ES retention`; the items index keeps only short snippets for two weeks so candidates can be ranked. Notes keep paraphrases and links. Handles stay in the ledger only. When a source deletes a post the user engaged with, `followups` stops finding it; remove its text from the ledger entry (set `text` to "" and `status` to `dropped`) when the user asks or at the monthly check.
