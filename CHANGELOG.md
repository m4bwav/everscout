# Changelog

Plugin versions, newest first. Skill-level changes are in each skill's `CHANGELOG.md`; the session log is `ai-docs/log.md`.

## 0.12.20 · 2026-11-07

- `lit ingest` prints the outline (up to 45 lines, the rest in toc.txt), as the skill says it does; runs had opened toc.txt in a second call (Zizza run).

## 0.12.19 · 2026-11-07

- `lit ingest --tier` refuses a new row without `--year` (Samara's Typography Workbook came in with no year and `lit check` warned after distill).

## 0.12.17 · 2026-11-07

- `lit ingest --tier T --why W --evidence E [--year Y --authors A]`: a shelf book no beat lists gets its literature row at ingest, already `reading`, instead of a later `lit add`.

## 0.12.16 · 2026-11-07

- `lit pick`: a top folder with more than five unlisted files (a magazine run, a collected works) prints as one line with its count; `--expand` lists them all. The shelf list went from 388 lines to 182.
- multi-agent-grind distils its first book, Dooley, *Software Development, Design and Coding* (Apress 2017): Amdahl, WIP, lead time and pull vocab, three questions; grindwright 0.3.6 (crew sizing by serial share, pull rule, review-cap prior).

## 0.12.15 · 2026-11-07

- `lit pick`: a beat row still `lead` or `have` for a book any beat has distilled (its title in a beat's `DATA/books`) is no longer shown as read elsewhere; The Computer Music Tutorial stopped showing as an ai-sfx lead after ai-music distilled it. The ai-sfx row is now `skip`, pointing at the ai-music note.
- ai-sfx distils Lanham, *Game Audio Development With Unity 5.x*: duck volume and ducking aliases, mixer-snapshot and vertical-remix vocab, one tools question on shared mixer returns; sfxwright 0.1.20.

## 0.12.14 · 2026-11-07

- `lit ingest`: when readwright's toc says a scan read one page per section has Chapter N headings, the chapter map from `rw.py toc --chapters` is written at the top of `toc.txt`, above the page rows (Yewdall run).

## 0.12.13 · 2026-11-07

- `lit pick`: a beat row whose title sits inside a longer title a beat has already read (Stevens and Raybould, *Game Audio Implementation*, inside Coggan, *Unity Game Audio Implementation*) is no longer shown as read elsewhere, and its file line no longer names the longer book's files (Holman run).
- Root `plugin.json` version brought in line with `.claude-plugin/plugin.json` (it said 0.7.1).
- ai-sfx distils Holman, *Sound for Film and Television* (3rd ed.): futz, scene-transition and stems vocab, one maker question on ambience across a picture cut; sfxwright 0.1.18.

## 0.12.12 · 2026-11-07

- `lit pick`: the "read elsewhere, still `lead`" rows now print before the unread file list; after 389 unread files they sat at the very end and `| head` hid them (Pirkle run).
- ai-sfx distils Pirkle, *Designing Audio Effect Plugins in C++* (2nd ed.): echo-density, look-ahead, oversampling and zipper-noise vocab, one maker question on oversampling and look-ahead; sfxwright 0.1.17.

## 0.12.11 · 2026-11-07

- `lit distill`: the applied count left out `note` rows while the parenthesis counted them ("3 changes applied (1 written into the note)" for 4); it now counts every applied row and also says how many were rejected.
- ai-sfx distils Viers, *The Sound Effects Bible* (ch. 18 encyclopedia): explosion-anatomy and imaging-element vocab, one maker question on building automatic or burst sounds; sfxwright 0.1.15.

## 0.12.10 · 2026-11-07

- `lit ingest` and `lit pick`: an author named in parentheses in the file name ("... (Vanessa Theme Ament).pdf") was dropped before the surname check, so the file was called another author's book and got a new folder and row. The check now reads the whole file name.
- ai-sfx distils Ament, *The Foley Grail* 3rd ed. (ch. 5, 10, 11): four vocab terms, one maker question; sfxwright 0.1.14.

## 0.12.9 · 2026-11-07

- `lit pick`: when several folder files hold a read-elsewhere title, the line names them (up to three) instead of only counting them.
- ai-music distils Roads, *The Computer Music Tutorial* 2e (in indie-ai-scout): time-stretch, onset and beat-tracking vocabulary, three maker questions; musicwright 0.1.24.

## 0.12.8 · 2026-11-07

- `lit pick`: each read-elsewhere line names the folder file that holds the title (`file: ...`), so a book under a dotted publisher name (`The.MIT.Press.Game.Sound...pdf`) is found without a manual search.
- ai-sfx distils Collins, *Game Sound* (canon row distilled, Ohio State syllabus added as evidence): dynamic-audio, diegetic-sound, boredom-switch, mickey-mousing and preparatory-cue vocabulary, one process question on muted play.

## 0.12.7 · 2026-11-07

- `lit distill` falls back to the title when the learnings' `book_id` (an ISBN added while reading) is not on the list row, instead of saying the row was not found.
- ai-sfx distils Chion, *Audio-Vision* (canon row distilled): synchresis, added value, materializing indices, rendering and offscreen vocabulary, two process questions.

## 0.12.6 · 2026-11-07

- `lit pick` no longer rebuilds the whole read index as a new string for every test, which raised MemoryError on a large index.
- ai-sfx gains *The Effects of Sound on People* (book note, no canon row), annoyance and equal-loudness vocabulary, and one reception question.

## 0.12.5 · 2026-11-07

- `lit pick` hides side files in a folder named for a read book (appendices, CD logs).
- ai-sfx gains *Sound Design for the Stage* (canon, distilled), production-element and orphan-effect vocabulary, and two questions.

## 0.12.4 · 2026-11-06

- `thread --thread-reader same` now honours the flag; it read through the configured fetchwright reader regardless.
- New built-in beat **ai-sfx** (sound effect models, ComfyUI, video-to-sound, procedural sound, libraries, craft and licences): 35 sources, probed 2026-11-06, feeds sfxwright. Read-only at the start.
## 0.12.3 · 2026-11-06

- `lit pick`: a file whose title holds a listed title after other words, with no listed author, is not that row (*Unity Game Audio Implementation* showed as Stevens and Raybould's book). Files named like a wanted list no longer count as read, so their titles stop showing as read elsewhere.
- *Unity Game Audio Implementation* distilled into ai-sfx.

## 0.12.2 · 2026-11-06

- `lit pick`: a much-discussed book counts as maybe read. A short title's author was ignored once the name passed 8 mentions in the records, so *Pixel Logic* listed as unread.
- *How to Suppress Women's Writing* distilled into tech-hiring.

## 0.12.1 · 2026-11-06

- `lit ingest`: `--title` now gives a book its own folder, and a listed title its colon cuts to one word (`Typography: A Manual...`) needs its author in the file name.
- `lit lint`: a toc title with ` / ` can be cited by either part.
- *Typography for Lawyers* distilled into personal-sites.

## 0.12.0 · 2026-11-05

- New built-in beat **ai-voice** (speech, voice design, cloning, singing, cleanup, craft and law): 41 sources probed 2026-11-04, feeds voicewright. Voice models live here; audio native to a video model stays in ai-video.

## 0.11.7 · 2026-11-03

- `lit ingest` drops a leftover such as `(for . .)` from the end of an EPUB title, which had reached the book folder name.

## 0.11.6 · 2026-11-03

- `lit ingest` no longer takes a book for a listed one whose title its name contains when the file names another author, and refuses a folder that holds another book's file (Better Web Typography overwrote Web Typography's `book.md` and `toc.txt`; both restored). Its report no longer says "set to reading" for a row it left alone.

## 0.11.5 · 2026-11-03

- A beat outside `EVERSCOUT_BEATS` now warns instead of silently using another clone (You Just Don't Understand run: tech-hiring is built in, not in the beats repo). tech-hiring: expertise and floor vocab, three question seeds, a study note, the book's canon row.

## 0.11.4 · 2026-11-03

- `lit pick` hides another copy of a read book by the title in its `book.md`, so a PDF twin no longer lists when the beats clone lags (Generative AI on Kubernetes run).

## 0.11.3 · 2026-11-03

- `lit ingest` accepts a path as `lit pick` prints it, relative to the book folder (Economics DeMYSTiFieD run). global-economics: gnp and deflation vocab, two question seeds, Fox and Dodge 2012 in canon.

## 0.11.2 · 2026-11-03

- `lit distill` with no list row names the `lit add ... --status distilled` command to add one (Show Your Worth run).

## 0.11.1 · 2026-11-03

- `lit add` linking a row to an ingested book also writes the row's title into book.md and learnings.md, so `lit distill` finds the row when the file's title differs (Arnold, Economics 11e: file "ECONOMICS, 11TH EDITION", row "Economics (11th ed.)"). global-economics: fed funds, administered rates, Taylor rule and currency peg vocab; two question seeds.

## 0.11.0 · 2026-11-03

- kb/method.md "Sweeping a docs or tutorial index": find the llms.txt or sitemap, watch the docs repo's path-filtered commit feed, diff against the last sweep's list, read pages not titles, record adopt/considered outcomes as notes, monthly cadence. kb/platforms.md: GitHub `commits/<branch>/<path>.atom`.
- ai-video beat: rows for the ComfyUI docs tutorials commit feed and Comfy-Org/workflow_templates releases, a monthly sweep row for docs.comfy.org's tutorials index, tutorials in the keep list. everscout-scan runs `sweep` rows by the method.
- because: Mark asked (2026-11-03) to fold the ComfyUI tutorials sweep and tutorial sweeping in general into the beat and everscout, after the comfyui-gen sweep (2026-10-30 to 11-03) tried about thirty tutorial pages.

## 0.10.12 · 2026-11-03

- `lit lint` accepts the part of a toc title before a dash as a citation: `(Life of Pixel)` for `Life of Pixel—Our First PC and Mac Launch`.
- because: Hill-Whittall's post-mortem citations were refused until rewritten with `ch. 2`.

## 0.10.11 · 2026-11-03

- `lit ingest` splits a trailing ` - Author Name` off file-name titles, as it already did `(Author Name)`.
- because: *The GameDev Business Handbook - Michael Futter.pdf* was filed as `the-gamedev-business-handbook-michael` with the author in its title.

## 0.10.10 · 2026-11-03

- `fetch` marks near-duplicates: an item whose opening text (or title, for a bare link post) shares most word shingles with an earlier item gets `dup_of` the earlier id, shown as `dup of ID` in the listing; triage reads the first copy only. Word shingles and Jaccard overlap per Manning et al. sec. 19.6 (4-word shingles, 2 for titles, threshold 0.8).
- because: *Introduction to Information Retrieval* (token-saving beat). On the indie-game-marketing cache it found 31 of 716 items were cross-posts (r/gamemarketing and r/gamedev copies of one post).

## 0.10.9 · 2026-11-02

- `lit ingest` puts swapped EPUB metadata right: a title that is a person's name and an author field holding the book title (both in the file name) are swapped back, and the name becomes the author.
- because: Tannen, *Conversational Style*: the EPUB's title read `Deborah Tannen`, so the book folder was named `deborah-tannen`.

## 0.10.8 · 2026-11-02

- `lit add --id -` no longer matches another row whose id is also `-`; a placeholder id falls back to the title.
- because: Sinicki, *Learn Unity for Android Game Development*: adding its row with `--id -` overwrote The Gamer's Brain (caught in the diff, restored).

## 0.10.7 · 2026-11-02

- `lit lint` accepts a toc title cited without its final period or its chapter number (`2. Think Process, Not Product.` cited as `(Think Process, Not Product)`); `VERSION` matches plugin.json again.
- because: Kleon, *Show Your Work!*: 13 of 14 principles were refused for a citation that named the chapter.

## 0.10.6 · 2026-11-02

- `es_discord.py peek INVITE` reads what a server shows the public with no token (invite lookup, widget on or off); `row --followed SERVER` marks a channel fed by Follow on another server's announcement channel. kb/discord.md gains "Servers you can't add the bot to".
- because: Mark asked how to read servers like r/StableDiffusion without an admin adding the bot.

## 0.10.5 · 2026-11-02

- `lit ingest` drops a leading publisher from a spaced file name (`Apress The Blender Python API ...` titled and slugged with the publisher).
- because: the Conlan book run on 2026-11-02.

## 0.10.4 · 2026-11-02

- `es_discord.py check` counts the servers the bot can list; Discord's cached `approximate_guild_count` showed 0 with the bot in Mark's server.
- because: the continue-prompt run on 2026-11-02.

## 0.10.3 · 2026-11-02

- `es_discord.py read` no longer warns that the Message Content intent is off when the only messages are system messages (the bot's own member-join message has no text); `discord_text_missing` checks user messages only.
- `kb/discord.md`: set Installation > Install Link to None before turning Public Bot off, or Discord refuses the save.
- because: the first live run on Mark's own server (2026-11-02).
## 0.10.2 · 2026-11-02

- `lit ingest` splits trailing parentheses off a file name's title: person names (`(Gilbert Mizrahi)`, `(A B, C D)`) become `authors:` in book.md, a year or publisher (`(2016)`, `(Packt Publishing)`) is dropped; other parentheses (`(3rd ed)`) stay. A run-together subtitle with no colon cannot be told apart and stays in the title.
- because: a Mizrahi prompt-engineering PDF was titled with its whole file name, author included.

## 0.10.1 · 2026-11-02

- `lit lint` accepts a numbered chapter label as a citation: a toc title `Level 11: They All Want You Dead` (or `Bonus Level 5: ...`) is cited `(Level 11)`; a label ending in a digit no longer matches a longer number (`level 1` is not `level 12`).
- because: the Level Up! run cited its chapters by label and lint refused principles 11-17.

## 0.10.0 · 2026-11-02

- Discord, through your own free bot: `scripts/es_discord.py` (standard library, REST API v10, nothing hosted) checks the token and the Message Content intent, prints a read-only invite link (View Channels and Read Message History), lists servers, channels and threads, reads history into everscout items with authors dropped, tries guild search, prints a watch-list row, and leaves a server. A new source kind `discord` (source `guild_id/channel_id`) is read by scans at one request a second; the token header goes to discord.com only, and rows are skipped when no token is set.
- Read-only by decision (`ai-docs/decisions/2026-11-02-discord-bot-read-only.md`): no posting, reacting, DMs or joining; a test fails if the client gains a POST or PATCH.
- Setup guide `kb/discord.md` (Developer Portal steps, the invite message for admins, the Developer Policy rules that bind a reader, rate limits); evidence in `ai-docs/research/2026-11-02-discord-bot-access.md`.
- because: Mark asked for a legal, free way to read Discord with as much bot code in the plugin as possible, the agent calling the bot rather than the bot forwarding to an AI API (2026-11-02).

## 0.9.7 · 2026-11-02

- `lit lint` accepts an interviewee's name as a citation: interview books title every chapter `INTERVIEW (in: RODRIGO PRIETO: MEXICO)`, so "(Prieto interview)" failed lint and section numbers had to stand in. The parts of an `(in: ...)` title and the person's surname now count as toc names.
- because: the FilmCraft run (skills/everscout-library/TESTS.md T-20261102-13).

## 0.9.6 · 2026-11-02

- `lit pick` splits CamelCase only in file names with no separators: 0.9.5 turned `FilmCraft Cinematography - Mike Goodridge.epub` into "film craft", so a book read on 2026-10-22 listed as unread. It now shows as maybe read.
- `lit ingest` turns a release-style file name (`0198237901.Oxford.University.Press.USA.Epistemic.Injustice...Aug.2007`) into a title (leading ISBN, publisher, trailing date and release tag dropped) when the PDF's own title is junk, so the book folder is `epistemic-injustice-power-and-the-ethics`, not `0198237901-oxford-university-press-usa`.
- because: the Epistemic Injustice run (skills/everscout-library/TESTS.md T-20261102-10).

## 0.9.5 · 2026-11-02

- `lit pick` splits CamelCase file names (`GenerativeDeepLearning.pdf` is three words), so a file whose title a beat already distilled is no longer listed as unread.
- because: the Essentials of Economics run (skills/everscout-library/TESTS.md T-20261102-9).

## 0.9.4 · 2026-11-02

- `lit pick` flags a file whose name is a slug that dropped the small words of a title read elsewhere (`procedural-3d-modeling-geometry-blender` for *Procedural 3D Modeling Using Geometry Nodes in Blender*): four or more file-name words in order on one line of the read index, with few words between.
- `lit lint` says when an over-long quote sits in a change row (change text needs no quote marks); the learnings template says so too.

## 0.9.3 · 2026-11-02

- because: the Five C's run (skills/everscout-library/TESTS.md T-20261102-5).
- `lit pick` ignores reading lists (files named reading-list, to-read or wishlist) in the read index: a book someone plans to read was shown as read elsewhere.
- `lit pick`'s "read elsewhere" line names the record file that shows the read.
- `lit pick` read-index entries may be `<folder>@<git ref>` (Mark's config: comfyui-gen's `ai-docs/notes@origin/master`): the folder is read as that ref has it, so notes on a branch the shared clone is not on still count. It had listed *Using Stable Diffusion with Python*, read on 2026-10-31 in comfyui-gen's notes.
- `lit pick` also matches the folder a book sits in: the folder kept the full title its file name shortened.
- `lit ingest` passes readwright's note on when it refuses a file with no text, so the way in (a DjVu twin, `rw.py ocr`) shows.

## 0.9.2 · 2026-11-02

- `lit pick` lists book files in subfolders (two levels), so a beat-listed book saved as `Title/Title.epub` is found (skills/everscout-library/TESTS.md T-20261102-3).

## 0.9.0 · 2026-11-02

- because: the Inside Palantir ingest (skills/everscout-library/TESTS.md T-20261102-1): a 14,000-word self-published book with no notes got the same treatment as a sourced history, and spot checks found misdated lawsuits and a Senate hearing that did not happen.
- `lit ingest` warns when a book is under 30,000 words and its outline has no notes, sources or index: check the author and three facts first (kb/literature.md step 1a).
- `lit distill` keeps a row set to `skip`: before, it turned the skipped book's row into `distilled`, which hid the warning against reading it again.
- kb/literature.md: step 1a (reliability check), and tutorials, forums and community threads as a source beside books for how-to beats (Mark, 2026-11-02).

## 0.8.9 · 2026-11-01

- because: the Tannen ingest (skills/everscout-library/TESTS.md T-20261101-19): the 40-character cut of "Talking From 9 to 5: Women and Men at Work" left the book folder ending on "at".
- `slugify(..., whole=True)` drops stop words (a, and, at, for, of, the, to...) left at the end of a cut title. `lit_book` still finds folders made before this (and before 0.8.3) by their old slug.

## 0.8.8 · 2026-11-01

- because: The Visual Story ingest (skills/everscout-library/TESTS.md T-20261101-17): the PDF's metadata title is its prepress standard (`ISO 15930 - Electronic document file format ... (PDF/X)`), so `lit ingest` named the book folder after it and missed the beat's `lead` row.
- `lit ingest` ignores producer and template titles (ISO, PDF/X, Microsoft Word, untitled) and falls back to the file name; with no `--id`, it finds the list row whose title appears whole in the file name. 93 offline tests (1 new).

## 0.8.7 · 2026-11-01

- because: the Murch distill (skills/everscout-library/TESTS.md T-20261101-16): the EPUB's own OCR titles a section `Seeing Around the €dge of the Frame`, so `lit lint` refused the correct citation `(Seeing Around the Edge of the Frame)`.
- `lit lint` matches toc section names with any non-ASCII symbol in the title standing for one character. 92 offline tests (1 new).

## 0.8.6 · 2026-11-01

- because: the open item from the Co-Intelligence and Making Music runs (T-20261101-14: `lit pick` hid DeSantis as read elsewhere while downtempo still listed it `lead`), and the Color & Light run (T-20261101-15: a scanned PDF stopped the previous session at `lit ingest`).
- `lit pick` ends with `read elsewhere, still lead|have in <beat> <tier>: <title>` for a beat row whose title the read index names (a two-word title also needs an author's name within 150 characters). The no-text refusal in `lit ingest` names readwright 0.9's `rw.py ocr FILE`. 91 offline tests (1 new).

## 0.8.5 · 2026-11-01

- because: friction from the Kenworthy distill (skills/everscout-library/TESTS.md T-20261101-12): on a US evening `lit ingest` dated the learnings the next day, since it wrote the UTC date while `lit due` reads the local calendar.
- `lit ingest` and `lit distill` write local dates (`local_today`). 90 offline tests (1 new).

## 0.8.4 · 2026-11-01

- because: friction from the Morales distill (skills/everscout-library/TESTS.md T-20261101-10): run from a worktree under `_wt/`, `lit ingest` found no sibling readwright clone and pointed at the stale installed 0.2.0 in the plugin cache.
- `find_readwright` also looks beside the main checkout of a git worktree. 89 offline tests (1 new).

## 0.8.3 · 2026-11-01

- because: friction from the Graesser distill (skills/everscout-library/TESTS.md T-20261101-9): `lit ingest` cut the book folder name mid-word (`foundations-of-deep-reinforcement-learni`), and `lit pick` still listed other copies of a distilled book whose literature title carries an edition, like "(3rd ed.)", and `lit lint` refused bare section numbers as citations.
- Book folders are cut at a word; `lit` still finds folders made before. Parentheticals are dropped from title keys. `lit lint` accepts a bare section number like `(10.2.1)` as a citation. 88 offline tests (2 new, the lint test extended).

## 0.8.2 · 2026-11-01

- because: friction from the Lapan distill (skills/everscout-library/TESTS.md T-20261101-8): `EVERSCOUT_BEATS` named a worktree not yet made, and `lit ingest` quietly used the configured clone ("list row not found").
- A missing `EVERSCOUT_BEATS` folder is now an error. 86 offline tests (1 new).

## 0.8.1 · 2026-11-01

- because: friction from the Lambshead distill (skills/everscout-library/TESTS.md T-20261101-7): `lit lint` rejected citations by section name like `(Player phase)` though the outline has them, and `lit pick` listed books plugin-learnings had read under a short title (Pixel Logic, Blender Master Class, FilmCraft).
- `lit lint` and `lit distill` accept a parenthesis naming a section title from the book's `toc.txt` as a citation. `lit pick` also flags a file as maybe read when two long title words appear in the read index with a rare third file-name word (an author's name) within 150 characters. 87 offline tests (2 new).

## 0.8.0 · 2026-11-01

- because: friction from the Cossu auto-pick (skills/everscout-library/TESTS.md T-20261101-5): several manual greps to find an unread book, and a scan with no text layer got a book folder.
- New `lit pick`: book files in a folder (`--dir` or config `books_folder`) that no beat's `book.md` names, beat-listed ones first; `--read-index` (or config `books_read_index`), a file or folder of notes, hides files named there and flags ones whose four-word run appears there as maybe read (`--all`). `lit ingest` refuses a file readwright reports 0 words for, unless `--force`. 83 offline tests (2 new).

## 0.7.1 · 2026-11-01

- because: friction recorded over four distilled books (skills/everscout-library/TESTS.md T-20261031-4, T-20261101-2, T-20261101-3).
- `lit lint` and `lit distill` read the first word of a change's status, so `applied (v1.2, PR #3)` passes. `lit distill` writes applied `note` rows (an edition line, reading caveats) into the book note instead of listing them as changes. `EVERSCOUT_BEATS` (path list) is searched before the configured beat dirs, so `lit` in a worktree edits that worktree's beats. 81 offline tests (2 new).

## 0.7.0 · 2026-10-30

- because: user request (keep up with each beat's literature: the most important books of all time, the most important recent ones, the latest published; integrate a provided book into the knowledge base and attached skills). Evidence: `ai-docs/research/2026-10-30-beat-literature.md`.
- New skill everscout-library and `kb/literature.md`. New `literature.md` beat file (canon, recent, latest tiers plus Open Library searches; template in `beats/_template`), validated by `beat-check` when present.
- CLI `lit list|check|add|new|due|ingest|lint|distill`: Open Library adapter (`es_sources.parse_openlibrary`, 1 s pace, a day's cache), research due per tier (yearly, quarterly, monthly), readwright outline of a provided book into `DATA/books/<book>/learnings.md`, a lint for citations, quote length and change targets (beat files, `feed:` units, `plugin:`), and a `book` note kind written by `distill` so recall finds the book.
- Every built-in beat has a literature.md (researched 2026-10-30). 79 offline tests (4 new).

## 0.6.0 · 2026-10-29

- because: evergreen's beat offer (a new evergreen unit may get a beat whose findings feed its refresh). `beat-new` takes `--scope`, repeatable `--question` and `--feeds` (written to beat.md frontmatter) so a caller seeds the beat; `leads --beat --since` lists notes and reports since a date for that caller's refresh. 75 offline tests (1 new). `StatsTests.test_unapproved_is_only_proposed_and_approval_can_be_withdrawn` seeded fixed September dates and went stale as the calendar moved on; it now seeds three weeks before today. All 75 pass.

- because: the 2026-10-16 ai-video scan flagged seven YouTube channel feeds as 404; every YouTube feed was failing, Google's own channel included (`ai-docs/research/2026-10-16-youtube-feeds-and-gdelt-refusals.md`).
- `fetch` prints one line when every YouTube feed in the run fails: the endpoint is down, not the channel ids, so fetch again later before changing `sources.md`. kb/platforms.md youtube row says the same. 66 offline tests (1 new). A patch when released.
- ai-video beat metrics (user's answers, 2026-10-16): `wiki-text-to-video` promoted to active; `news-ai-video-share` archived as `source-gone` (GDELT refuses this address on the first call, three scans running).
- Plan for Reddit discovery after Arctic Shift (`ai-docs/plans/2026-10-16-reddit-discovery-after-arctic-shift.md`): pickup from items already fetched and user captures first, the agent's own web search next.
- because: that plan (Mark, 2026-10-16: build it) and lane plan steps 3 and 4. Finding Reddit threads once nothing lists a subreddit, with no new host and no key. A minor version when released.
- Pickup: `fetch` reads Reddit thread links (any permalink form, `redd.it`, links inside feed HTML, Mastodon posts and Bluesky facets) from every non-Reddit item inside the fetch window. It keeps them 14 days in the beat's state (`reddit_seen_elsewhere`), one mention per linking item. A listed Reddit item that other sources linked carries `elsewhere: N` in the fetch JSON. Items gain `reddit_links`.
- `discover list --beat` ranks the threads ready to read (24 hours after the first link, since Google's index lags; a web-search result at once) by distinct sources, mentions, vocabulary and showcase words. It prints coverage (how many of the Reddit threads noted in the last 14 days pickup also found) and the captures wanted. `discover add <url> --via websearch|capture` records a URL from the agent's own search; `discover mark <url> --status read|dropped|wanted|new` sets an entry's status.
- `fetchwright.max_reads_per_scan` (default 10): fresh fetchwright reads by `thread --beat` and `new-note` count from one fetch to the next and stop with exit 6 at the cap. Cached threads cost nothing.
- Captures: `captures --beat` lists the files the user saved into `DATA/captures/` with the thread URLs inside. `new-note <url> --capture FILE --title --posted` writes a note from one without fetching (`source: user-capture`, `capture:`) and moves the file to `captures/done/`.
- Notes record `via` (the reader behind `interest`), `discovered` and `mentions` for discovered threads. A thread with no listing date takes the earliest linking item's date.
- everscout-scan: Step 2 and procedure section G (C-20261016-1). kb/platforms.md "Reddit thread discovery without a listing"; kb/SCHEMA.md fields and the captures folder; conduct rule 16 and AGENTS.md lines on captures. 74 offline tests (8 new).
- First live check (`ai-docs/research/2026-10-16-reddit-pickup-coverage-live.md`): a week of ai-video's non-Reddit sources linked no Reddit thread. For that beat, web search and captures carry discovery.

## 0.5.0 · 2026-10-16

- because: Mark, 2026-10-15: "integrate it with everscout now. I don't want to wait on Arctic Shift, I want to see if it works now." Decision `ai-docs/decisions/2026-10-15-thread-reader-fetchwright.md`.
- Reddit threads through [fetchwright](https://github.com/m4bwav/fetchwright), opt-in: config `reddit.thread_reader` (`same`, the default, or `fetchwright`) and `--thread-reader` on `thread` and `new-note`. everscout runs fetchwright's CLI as a subprocess (config `fetchwright.cli`, then `FETCHWRIGHT_CLI`, then the installed plugin) and never imports it or reads the key. The thread carries `via: fetchwright`, no handles or dates, the poster's replies marked, and a `fetchwright` block with the model, Google's retrieval statuses and token counts.
- Paced at 5 s or more, cached for `thread_ttl_seconds` and purged with the cache. A 429 (fetchwright exit 3) sets a cool-down for Google's stated retry time, at least an hour, and later reads refuse at once (exit 3). A key problem exits 4 and names fetchwright-setup; a missing plugin exits 2 and names it. Optional `fetchwright.models`; `fetchwright.max_comments` defaults to 100 (0 asks for every comment). `followups` always uses the listing's reader (it needs authors and times). `new-note` takes the date from the fetched listing when the thread has none.
- Live on 2026-10-16: 9 of 10 threads read, every comment real, about three quarters of the archive's comments; a real ai-video scan read 7 of 8 kept threads (`ai-docs/research/2026-10-15-fetchwright-thread-reader-live.md`). Run `gemini-3.5-flash-lite` first (`fetchwright.models`). 65 offline tests (9 new).
- ai-video beat: 8 new tool entries (LongTakeNoCuts, the H3 anti-burn LoRA, OBVPM, RTX Video, Depth Anything, Video Helper Suite, AudioFirst X2, ExactAudioLock).

## Earlier unreleased knowledge (now in 0.5.0)

- because: plan `ai-docs/plans/2026-10-15-reddit-via-gemini-url-context.md` Stage 2 step 3; the reader shipped as its own plugin, [fetchwright](https://github.com/m4bwav/fetchwright) (2026-10-15).
- kb/conduct.md rule 17 and a kb/platforms.md keyed-sources row for Reddit threads through Gemini's URL context: never Google Search for discovery, public threads only (free-tier prompts may be read by Google's reviewers), stop at the first 429. Knowledge only; no CLI change. A minor version when released.

## 0.4.0 · 2026-10-15

- because: Reddit's logged-out feeds end 2026-11-13 and Mark chose the Arctic Shift lane on 2026-10-15 (plan `ai-docs/plans/2026-10-11-reddit-lane-after-rss.md`; a Gemini route was checked first and fails on Google's terms, `ai-docs/research/2026-10-15-reddit-through-gemini.md`).
- Reddit through the Arctic Shift archive: `fetch`, `thread`, `probe` and `search --community` read `arctic-shift.photon-reddit.com` when config `reddit.reader` is `arcticshift`, or from 2026-11-13 when it is `auto`. The default stays `rss` (the feeds): the archive's legal footing is grey, so each user opts in. After 2026-11-13 a fetch on `rss` says how to switch. `--reddit-reader` overrides it per command. Beats keep their `r/name` rows; item ids are unchanged, so seen state carries over.
- The fetch window ends `reddit.settle_hours` (36) ago, so scores and comment counts have settled, and runs `--max-age-days` back; one request per 100 posts, paged back to the window's start (`reddit.max_pages`, 10). Items carry points and comment counts, shown in the fetch listing. A failed later page keeps the earlier ones and says what is missing.
- Fetcher: `x-ratelimit-reset` paces Reddit's own hosts only (Arctic Shift sends it on every answer); on a 429 it is the wait when no `Retry-After` comes. Hosts under `photon-reddit.com` get everscout's own User-Agent, not Reddit's.
- kb/platforms.md row, conduct rule 17 and the Reddit platform note, README host list and privacy paragraph, scan skill fetch step. 56 offline tests (6 new). Live run 2026-10-15: ai-video's 17 subreddits, 1,904 posts in 48 requests and 2.5 minutes.

## 0.3.3 · 2026-10-06

- Ready for GitHub Copilot CLI and the awesome-copilot marketplace: a root `plugin.json` (Agent Plugins 1.0), and each skill now links its own copy of the `kb/` files it uses (`references/kb/`), because Agent Skills linters reject links that leave the skill folder. `kb/` stays the one to edit; `python scripts/sync-skill-refs.py` rewrites the copies and `--check` (run by the test suite) fails when one drifts.
- Prepared for the Claude plugin directory: README Privacy section (every host class the CLI contacts, what each request carries, no credentials read, no posting), plugin.json homepage, documentationUrl, supportUrl and privacyPolicyUrl. Two skill references reworded ("add `--override`", "give `new-note` the options") so the directory scanner does not read "pass" as the password manager.
- New built-in beat **personal-sites** (how tech and design people think about and build personal and professional websites and blogs): 34 sources (10 subreddits, 3 Hacker News queries, 9 feeds including IndieNews, Smashing, Typewolf, Dave Rupert, Jeremy Keith, Josh Comeau and Maggie Appleton, 3 Google News queries, 4 Mastodon tags, 4 hand-read galleries), 60 entities in 5 facets, 21 question seeds, an 11-chapter study outline, 2 candidate metrics. Probed clean on 2026-09-27. Built to refresh Mark's site and to seed a personal-site design skill.
- personal-sites: AI and visual design merged in rather than a separate beat (same communities): research question 7, an "AI and design" vocabulary facet (18 entities), 9 sources (r/vibecoding, HN "AI slop" and "vibe coded", Sidebar, UX Collective, Awwwards blog, Creative Bloq, Google News, avoid-ai-design), 4 question seeds, 4 searches, study chapter 04b.

## 0.3.2 · 2026-09-27

- because: Mark said yes to two candidates while GDELT was cooling down and they had no points, so the yes had to wait in a handoff note.
- Pre-approved promotion: `stats approve --beat B METRIC [--withdraw]` stamps an optional `approved` column in `metrics.md` (old catalogs stay valid). `stats collect`, `stats review` and `approve` itself promote an approved candidate once it meets the normal rule (3 points at C3 or better), print `promoted X (pre-approved <date>)` and log it. Unapproved candidates are still only proposed. `beat-check` validates the date. kb/SCHEMA.md, kb/stats.md, scan skill and report reference updated. 49 offline tests.

## 0.3.1 · 2026-09-27

- because: GDELT answered 429 all through the 0.3.0 session and to a single probe 10 minutes after the last call; its only published limit is "one request every 5 seconds" in the refusal text, and reports show blocks lasting much longer (ai-docs/solutions/2026-09-27-gdelt-rate-limit.md).
- GDELT gap raised from 6 s to 10 s between completed calls.
- A GDELT refusal starts a cool-down in `LOCAL/cooldown.json` (1 h, doubling per refusal in a row, at most 24 h); `stats collect` skips GDELT metrics until it passes, sends nothing and writes no failed row; a success clears it. New test (46 offline tests).
- tech-hiring: `wiki-layoff` promoted to active (the user's yes, 8 points).
- `kb/platforms.md` GDELT row and `kb/stats.md` updated.

## 0.3.0 · 2026-09-27

Beat statistics, built from the approved design in `ai-docs/research/2026-09-27-beat-statistics.md` (section 5).

- because: Mark wants each beat to gather statistics over time, propose and retire metrics, and feed chartwright; the research note found no skill that does the loop and set the schema, storage and lifecycle.
- Metric catalog `metrics.md` per beat (id, question, definition, unit, kind, source, method, cadence, Admiralty grade, status, version, created, reviewed, archive_reason, headline), validated by `beat-check`. The template and the four starter beats ship candidates (notes per week, GDELT news volume, Wikipedia pageviews), sources checked live on 2026-09-27.
- Append-only `DATA/stats/series.csv` (`date,metric,version,value,unit,source,note_ref`); failed collections are rows with an empty value.
- CLI `stats list|add|collect|review|export`. Adapters: tally (notes or an entity, count or share), GDELT DOC 2.0 TimelineVol and TimelineVolRaw, Wikimedia pageviews, derived, manual. Network reads go through the paced fetcher with a 60 s timeout (GDELT took 45 s for an OR query on 2026-09-27) and no retries; a refusal is never cached.
- Lifecycle in `stats review`: promotion after 3 points at grade C3 or better on the user's yes; archive as stale (3 failed periods, or no value for 3 periods), flat (CV under 5% over 8 points), irrelevant, gamed or superseded; never deletes rows; a definition change bumps the version and export splits the series. Thresholds configurable under `stats` in config.json. Trends and co-movement shown, never acted on.
- `stats export` writes a chartwright-ready long CSV and, when chartwright is found, prints or builds (`--charts`) a line chart, sparklines and small multiples into `DATA/reports/charts/`. Chartwright stays optional.
- Skills: everscout-beat defines metrics, everscout-scan collects, everscout-report reviews and charts, everscout-ask reads the series (procedure in `kb/stats.md`). beat and report descriptions updated with skill-tidy (check OK).
- `kb/SCHEMA.md` and `kb/platforms.md` document the files and the two new sources. 45 offline tests (15 new); root plugin evals 12/12 after the description changes.

## 0.2.2 · 2026-09-26

- The five skill descriptions shortened with skill-tidy so each is under the 1,024-character spec cap (some hosts drop longer ones), under 200 words and at most 12 quoted phrases, with every trigger meaning kept and a boundary sentence naming the siblings. ask 1,415 to 962 chars, beat 1,081 to 926, engage 1,165 to 1,011, report 1,102 to 920, scan 1,096 to 949.
- New `evals/` at the plugin root: 12 trigger and decoy cases for `claude plugin eval . --ablation none --no-publish --trust-plugin` (runs on native Windows); first run 12/12. `evals/results/` is ignored.

## 0.2.1 · 2026-09-26

- `followups` recognises replies imported without a comment id (matched by time), so a migrated ledger does not collect the same answer twice. Found moving indie-ai-scout onto everscout as the private beat `indie-ai-games` (its plan and log are in indie-ai-scout's private doc set).

## 0.2.0 · 2026-09-26

- New skill **everscout-ask**: interrogate a beat like a reporter. It recalls what the beat's knowledge base holds, grades whether that is enough and fresh (corrective retrieval: enough, partial, none), researches the gaps in the beat's communities, data pages and the web, answers with what the scout had seen, what is new, where sources disagree, confidence and unknowns, and saves the answer under `answers/` so the next question starts from it.
- CLI: `recall --beat --q` ranks notes, answers, reports, study and the journal against a question and prints the signals for the entities it names; `index` and `lint` cover `answers/`; `fetch --peek` reads without marking items seen; vocabulary aliases also match their plural.
- Tested headless: "Ask my tech-hiring scout: are companies moving interviews back on-site because of AI cheating?" passed 3 of 3 (everscout-ask TESTS.md, T-20260926-1).
- New built-in beat **tech-hiring** (developer and tech hiring), the first beat built from scratch by everscout-beat: 33 sources (15 subreddits, 5 Hacker News queries, Indeed Hiring Lab, the Pragmatic Engineer, Crunchbase News, Google News, Mastodon, data pages), 49 entities in 5 facets, 27 question seeds, an 11-chapter study outline.

## 0.1.2 · 2026-09-27

From the second headless test of "set up a scout for ai video generation" (everscout-beat TESTS.md, T-20260927-2, 3 of 3 passed).

- `probe --save` merges a partial probe into the day's snapshot instead of overwriting it.
- The built-in ai-video beat takes the test run's verified refresh: 46 sources, all answering on 2026-09-27; three GitHub rows moved to commit feeds (the repositories publish no releases); AI film newsletters, a Bluesky feed generator, arXiv and Lemmy added; PixVerse, KlingAI and SeedVR2 in the vocabulary.
- Procedure and platform guide: check `releases.atom` before adding a GitHub row; prefer arXiv category RSS.

## 0.1.1 · 2026-09-26

Fixes from the first headless test of "set up a scout for ai video generation" (everscout-beat TESTS.md, T-20260926-1).

- `probe` checks Reddit through multireddit requests, ten subreddits each, and probes alone only the ones that do not appear.
- everscout-beat waits for the probe instead of ending with it running, and refreshes a matching starter beat with a discovery pass instead of only copying it.

## 0.1.0 · 2026-09-26

First release. A topic-agnostic scout, generalised from the private indie-ai-scout 0.3.1.

- Beats: a subject is a folder of markdown files (`beat.md`, `sources.md`, `vocab.md`, `questions.md`, `searches.md`, `study.md`). Built-in starter beats `ai-video`, `global-economics`, `downtempo`, and `_template`. Private beats in `~/.everscout/beats` shadow built-in ones.
- Sources, all keyless, checked live on 2026-09-26: Reddit Atom feeds, Hacker News (Algolia), Bluesky (profile RSS, feed generators, threads), Mastodon (tag and account RSS, threads), Lemmy (community RSS, threads), Discourse (latest and category RSS, topics), any RSS or Atom feed, YouTube channel and playlist feeds, GitHub releases, arXiv API, Hugging Face trending models, spaces and daily papers, Google News search. One paced, cached fetcher with a per-host gap, an honest User-Agent, retries on 429, 503 and transient 406.
- Notes with one list field per vocabulary facet, prefilled by alias matching; `validate`, `tally` (counts, 30-day velocity, spread, decayed weight, signal new, rising, steady, fading, dormant), `index`, `lint` (report and study links resolve; external URLs must be held by a note, a snapshot or the source log), `source-log`, `retention`.
- Engagement: `candidates`, `questions`, one ledger across beats with per-platform pace rules (`engage-check`, `engage-record`, `engage-update`, `ledger`, `followups`). Everscout never posts; the person pastes.
- Knowledge base: `kb/conduct.md` (a 20-rule conduct code from the engagement-ethics research), `kb/platforms.md`, `kb/method.md` (netnography stages, signal rubric, radar rings, faithfulness rules), `kb/SCHEMA.md`, `kb/voice-template.md`.
- Four evergreen skills: everscout-beat, everscout-scan, everscout-engage, everscout-report, each with research, changelog, learnings, tests and evals.
- Research notes under `ai-docs/research/`: platform access, engagement ethics, prior art, sample beats.
