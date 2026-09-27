# everscout-beat procedure

Detail for [SKILL.md](../SKILL.md). `ES` = `python "<plugin root>/scripts/everscout.py"`; `DATA` = the data folder `ES where --beat <slug>` prints.

## A. A new beat

1. **Interview (one message, three questions at most).** What to follow and what is out of scope; what they want to learn (three to eight research questions: "which tools do makers of short AI films actually finish with?", "what do central bankers signal before a pivot?"); whether to engage with makers, and on which platforms they have accounts. If the user already said enough, skip the questions.
2. **Scaffold.** `ES beat-new <slug> --title "<title>"`. The slug is short and stable (`ai-video`, `global-economics`, `downtempo`). Fill `beat.md` first: scope, research questions, keep and skip, `showcase_words` for the domain (music: "my new track", "EP", "out now"; economics: "new paper", "working paper", "chart", "my latest"), `mute_words` for the domain's spam.
3. **Research, pass one: discovery (about 20 to 40 searches).** For each platform in `kb/platforms.md`:
   - Reddit: `"<subject>" site:reddit.com`, `best subreddits for <subject> <year>`, sidebars of the first communities found ("related communities"). Then `ES search --kind reddit --q "<subject term>" --t year` to see which subreddits the results come from.
   - Hacker News: `ES search --kind hn --q "<term>" --t year` for comment counts; a query row is worth it if there are several threads a month.
   - Bluesky: the web search for `"<subject>" bluesky starter pack` and `"<subject>" bluesky feed`; a feed generator (`at://.../app.bsky.feed.generator/...`) is the best keyless source; profile RSS for a handful of key people.
   - Mastodon: `#tag` usage through `https://<instance>/api/v2/search?q=<tag>&type=hashtags` (history shows weekly use); two or three tags on a large instance.
   - Lemmy and PieFed: `site:lemmy.world "<subject>"`, the instance's community search.
   - Forums: `"<subject>" forum`, known ones for the domain (music: KVR, Gearspace, Elektronauts, lines; maker tools: the tool's Discourse).
   - Feeds: newsletters (Substack, Ghost), blogs, podcasts, YouTube channels (find the `UC...` id from the channel page source or `youtube.com/@handle` then the canonical link), GitHub repos for tool releases, arXiv categories or queries, Hugging Face pipeline tags, Google News queries for official news.
   - Official and data sources the reports will cite (release notes, statistics offices, labels' pages).
4. **Research, pass two: verify each candidate.** For each community: `ES fetch --beat <slug> --sources <name> --all --max-age-days 14` after adding the row (or read the newest posts with the web tool); read the rules page (web fetch of `https://www.reddit.com/r/<name>/about/rules` often fails; use `old.reddit.com/r/<name>/about/rules`, a Wayback snapshot, or search `"r/<name>" rules`). Decide:
   - `stance` from the rules and from how AI or self-promotion posts are received;
   - `engage: yes` only with a real showcase culture (makers post their own work and answer comments) and rules that allow ordinary comments; anything that bans AI-written comments stays `yes` only with a note saying the user writes by hand there;
   - `scan: no` for communities with fewer than about three relevant posts a week (keep the row for reference);
   - a `filter` for broad sources;
   - the marker: `✓ <date>` when rules were read, `~` when only posts were read, `?` when nothing was readable.
   Aim for 15 to 40 scanned sources. More costs time: Reddit alone is about a minute per subreddit per listing.
5. **Vocabulary.** From the threads read in pass two plus the web: three to six facets (for a making-things beat: tools, models or instruments, techniques, formats or genres, topics; for a news-and-analysis beat: institutions, indicators, policies, themes, regions; for a music beat: artists, labels, gear and software, subgenres, techniques). 30 to 80 entities with the spellings people actually use as aliases (`kling-3: Kling 3, Kling 3.0, kling3`). Current version names only when confirmed on a primary page; mark others `(unverified)` in the vocab file's notes section. Run `ES vocab-match --beat <slug> --text "<a real post's text>"` on three or four posts to check the aliases catch what people write.
6. **Question bank.** 15 to 40 seeds in three to seven categories a curious peer would ask about the work: process, tools, craft, data or sources (for analysis beats), reception and release, what they would do differently. Tag the ones that mention AI with `ai`. Never an accusation, never "did you use AI". For an analysis beat, the seeds ask about data, method and what would change the author's mind. Read three or four threads where a maker answered questions and copy the shape of the questions that got long answers.
7. **Searches.** 8 to 15 queries with cadence, plus pages worth reading directly and a "what not to trust" list for the domain.
8. **Study outline.** Five to twelve chapters (origins and eras, the current state, practice guides, reception and policy, open questions, sources) and three to five perspectives (a newcomer, a veteran maker, a critic, an institution or platform). Show the outline to the user before the study is written (everscout-report does the writing).
9. **Verify and record** as in SKILL.md step 3. Snapshot the rules you read into `DATA/sources/rules-<community>-<date>.md` (a paraphrase with the URL and date) so the stance can be re-checked later.

## B. Sources: add, check, drop

- Add: research the one community as in A4, add the row, `ES beat-check`, `ES probe --beat <slug> --source <name> --save`, log `## [date] beat | <slug>: added <source> (<stance>, engage <yes/no>)`.
- Check all: `ES probe --beat <slug> --save` (background it). For each `BAD`: 404 means gone or renamed (search for the new name); 403 or "not a feed" means a login wall or block page (do not retry within the hour; note it in the row; check `kb/platforms.md` for a changed rule); a feed with no items in 30 days is dead (set `scan: no`).
- Drop: delete the row (the notes already written keep their data). Never leave a failing row with `scan: yes`.
- Re-verify stances quarterly: a `~` row older than 90 days gets its rules read again.

## C. Vocabulary and question bank upkeep

- `ES validate --beat <slug>` warnings list values that are not in `vocab.md`. For each: add it as a new entity, add it as an alias of an existing one, or fix the note. Then `ES tally`.
- A new version of a tool or model: its own entity when people compare versions (`veo-3` and `veo-3.1`), an alias otherwise.
- Questions: retire seeds that never got an answer in the ledger (`ES ledger --beat <slug> --json`, entries without replies); add the ones that did from the user's own comments. Keep under 60 seeds.

## D. Why the beat files are markdown tables

People edit them in any editor or Obsidian; agents read them without a parser library; diffs are readable; the CLI parses the first table only, so prose around the table is free. Keep the column names.
