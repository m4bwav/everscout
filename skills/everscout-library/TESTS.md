# Tests: everscout-library

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A test passes on evidence (the `everscout.py lit` calls in the trace, the files, exit codes), never on the transcript's claim. The CLI's `lit` commands have offline tests in `tests/test_everscout.py` (LiteratureTests).

## Runs

### T-20261031-1: first end-to-end distillation (manual, real book)

Spelunky (Derek Yu, 2016) into a private game-development beat. `lit ingest` (readwright outline, 12 sections), a reading agent read Parts I to IV, `learnings.md` filled (24 principles, 14 changes), `lit lint` exit 0, the user approved all groups, changes applied (a game-design plugin's kb, the beat's vocab and questions, one study chapter), `lit lint` 14 applied, `lit distill` wrote the `book` note and set the row `distilled`, `tally` and `index` ran. Pass. Notes: `(Part I)` citations were accepted by lint; book text copies the reading agent made in its scratch folder were deleted afterwards.

Trigger cases: `evals/library-trigger-1`, `library-trigger-2`, `library-decoy-1` (see T-20261031-2).

### T-20261031-2 · 2026-10-31 · claude plugin eval (default model, 1 run per case) · Windows 11 native · 3/3

- library-trigger-1 (must-read books for a beat): everscout-library fired; scan, ask, report did not. Baseline 0.75.
- library-trigger-2 (distil a game design epub into a beat and its skills): fired, others did not. Baseline 0.75.
- library-decoy-1 (fantasy novel for a holiday): no everscout skill fired.
- The two trigger runs hit max_turns 3 after the skill loaded; the graders only check the Skill call, so this is expected.

### T-20261031-3: second distillation (manual, real book, chapter-split reading)

Press Reset (Jason Schreier, 2021, 98k words) into the same private beat. `lit ingest` (30 sections), one agent read the intro and epilogue and split chapters 1 to 9 over three reading agents, `learnings.md` 24 principles and 12 changes, `lit lint` exit 0, the user approved all four groups, changes applied (game-design plugin 0.1.10, beat vocab and questions, study chapters 01 and 12), `lit distill`, `tally`, `index`. Pass. Notes: the principles for chapters 1 to 9 rest on the readers' summaries, and the learnings file says so; the reading agents' book text copies in the scratch folder were deleted.

### T-20261101-3: seventh distillation (manual, real book, agent pick, two readers, six repositories)

Generative Deep Learning (David Foster, 2nd ed. 2023) into ai-video, picked from the user's downloads folder as the only unread book a beat lists. `lit ingest`, two reader agents (diffusion and multimodal; music and world models), 23 principles, 14 changes, `lit lint` 0, the user approved all. Applied: ai-video vocab, questions and literature row (this PR), comfyui-gen PR #121, cinewright PR #68, artwright 0.7.4 (PR #28), musicwright 0.1.4 (PR #19, `render --check` key_fit with tests), ludowright 0.1.14 (PR #21), edition line in the note. `lit lint` 14 applied, `lit distill`, `tally`, `index`. Pass. Finding: `lit ingest` and `lit distill` write the list row to the beat dir in the user's config (the main clone), so a session working in a worktree must copy the row across by hand.

### T-20261101-2: sixth distillation (manual, real book, three part readers, six repositories)

Game Engine Architecture (Jason Gregory, 2nd ed. 2014) into game-design. Canon row added with two syllabi, `lit ingest`, three reader agents (Parts I-II, III, IV-V), 25 principles, 17 changes, `lit lint` 0, the user approved all 17. Applied: beat vocab, question, literature (indie-ai-scout e36a0d2, a2dd567), ludowright 0.1.13 (PR #20, R-58 to R-61), game-juice 1.3.2 (PR #7), unity-agent 1.2.5 (PR #22), threewright 0.6.8 (PR #17), roblox-agent 0.1.8 (PR #20), polywright 0.5.2 (PR #42), edition line in the note. `lit lint` 17 applied, `lit distill`, `tally`, `index`. Pass. Finding: apply agents wrote statuses like `applied (unity-agent 1.2.5, pr #22)`, which `lit lint` rejects; the status cell must be the bare word, with versions kept in the log.

### T-20261101-1: fifth distillation (manual, real book, agent pick, two repositories)

Play to Learn (Sharon Boller, Karl Kapp, 2017) into game-design. Ingested 2026-10-31 (ch. 4, 5, 9 read to the 25k-character cut); the user approved all 18 changes. Applied: beat vocab, questions, searches and literature row (indie-ai-scout de88bdf), ludowright 0.1.12 (PR #19, released v0.1.12), book_id OL20198942W in book.md, reading caveats in the note. `lit lint` 18 applied, `lit distill`, `tally`, `index`. Pass.

### T-20261031-5: fourth distillation (manual, real book, second edition, three repositories)

The Gamer's Brain (Celia Hodent, 2026 second edition) into game-design. Ingested and linted earlier the same day; the user approved all 20 changes. Applied: beat vocab, questions, searches and literature row (indie-ai-scout e1155de, its first commit of the beat), ludowright 0.1.11 (PR #18), game-juice 1.3.1 (PR #6), edition line in book.md. `lit lint` 20 applied, `lit distill`, edition line added to the note, `tally` and `index`. Pass.

### T-20261031-4: third distillation (manual, real book, technical, changes across five repositories)

AI Engineering (Chip Huyen, 2024) into a token-saving beat. `lit ingest`, sectioned reading, `learnings.md` 25 principles and 18 changes, `lit lint` exit 0, the user approved all 18. Applied: the beat's questions, vocab, searches, study and metrics (beat repository), the book note, and four plugins through their own CHANGELOG and RESEARCH files (two patch releases, two docs-only PRs), each on its own worktree and PR. `lit lint` 18 applied, `lit distill` wrote the note and set the row `distilled`, `tally` and `index` ran. Pass. Notes: the `note` row was applied by editing the note after `lit distill`, since distill writes the note from the principles and does not act on `note` rows; the beat had never been committed, so its first commit carried the whole folder.

## T-20261101-20: The Venture Alchemists (Lalka 2024), auto-pick into global-economics

No book named and no beat-listed file unread; picked Lalka because global-economics had no distilled book and nothing on market power, venture finance or gig work (`recall` for antitrust, gig, dual-class: no hits). `lit add` recent row, status `have` (Judgment call: Mark's copy; MIT Technology Review and Publishers Weekly reviews). Two reader agents (Act I, act intros, Epilogue; ch. 6-15) in parallel: 15 principles, 4 changes, all applied in the everscout PR (five Themes vocab entries, four question seeds, a study perspective, note). Lint passed first time; distill, tally, index, lit check, beat-check clean. Frictions: EPUB note numbers glued to sentences ("after that.40 Uber") misread as figures, and a reader's first call was `rw.py outline`; both fixed in readwright 0.9.3 (PR #17). Other reader complaints (several sections per call, snippet width, UTF-8) were features that exist. Pass.

## T-20261101-19: Talking From 9 to 5 (Tannen 1994), auto-pick into tech-hiring

No book named and no beat-listed file unread; picked Tannen off the RL and ai-video run because interview judgement, credit and calibration fit tech-hiring, which had nothing on them (`recall` for self-promotion: no hits). `lit add` canon row (Evergreen State College programme page, Open Road ebook in print, 7 Open Library editions). Two reader agents (Preface, ch. 1-4; ch. 5-9, Afterword) in parallel: 17 principles, 4 changes, all applied in everscout PR (vocab Interview judgement section, four question seeds, a study perspective, note). Lint passed first time; distill, tally, index clean. Frictions: both readers missed `rw.py read --max-chars` and sampled 50-85k-character chapters (readwright 0.9.2: the footer offers it, the skill tells book runs to pass it); the folder slug ended on "at" (0.8.9). Chapters 5, 6 and 9 were read only in part.

## T-20261101-18: Hands-On Generative AI with Transformers and Diffusion Models, from the plugin-learnings read

No book named; `lit pick` listed four read-elsewhere rows. AI Engineering was already distilled, Five C's and Don't Make Me Think have no file, so this ai-video recent `lead` came from the 2026-10-30 comfyui-gen read (Ai/books/plugin-learnings/diffusion-hands-on-genai.md). `git grep` of the book's short name in the target repos showed its proposals P1-P7 already in comfyui-gen (PR #104, LoRA note) and brandwright-train; P8 (music models copying training tracks) was only half in musicwright, so musicwright PR #25 adds a copy-check row for every released cue. 16 principles, 4 changes, all applied (vocab: six techniques and four aliases; questions: four Diffusion settings seeds; note). `lit lint` 0 on the first run. Tool change: kb/literature.md step 0 says how to check which of an earlier read's proposals landed. Pass.

## T-20261101-17: The Visual Story, from the plugin-learnings read

No book named; `lit pick` listed five read-elsewhere rows. Block (ai-video canon, `lead`, file present; Five C's and Don't Make Me Think have no file) came from the 2026-10-22 cinewright read of the full ch. 1-10 (Ai/books/plugin-learnings/cinema-b-block-brown-filmcraft-resolve.md). First ingest named the folder `iso-15930-electronic-document-file` from the PDF's metadata and missed the row; fixed in 0.8.8 and ingested again. 15 principles, 3 changes, all applied (vocab: visual-structure, contrast-affinity, story-intensity, space-type; questions: two Visual structure seeds; note with the edition line). Pass.

## T-20261101-16: In the Blink of an Eye and Film Directing Shot by Shot, from the plugin-learnings read

No book named; `lit pick` listed seven beat rows read elsewhere and the handoff said to distil those first. Murch and Katz (ai-video canon, `lead`) came from the 2026-10-22 cinewright read (Ai/books/plugin-learnings/cinema-a-katz-mascelli-murch.md), whose cinewright changes were already applied. Both files ingested, principles rechecked against the outlines: 15 and 16 principles, 3 changes each, all applied (vocab: six editing and staging terms; questions: four Editing and craft seeds; notes). Friction: lint refused a citation because the EPUB's OCR wrote `€dge`; fixed in 0.8.7. Mascelli's Five C's is not in the books folder (the earlier read used a DjVu twin), so it stays `lead`. Pass.

## T-20261101-15: Color & Light (3dtotal), auto-pick, a scanned PDF OCR'd first

Auto-pick for ai-video (off the RL run; Gurney's different book was read in plugin-learnings). An earlier session had made a worktree and stopped at `lit ingest`'s no-text refusal. readwright 0.9.0 (PR #14) added `rw.py ocr` (Windows' built-in OCR, 384 pages in about 3 minutes, 95k words); new recent row (ISBN 9781912843411, Parka Blogs review), `lit ingest`, one reader agent, 21 principles, 11 changes, `lit lint` 0 after two fixes (quote marks in change text read as quotes; `feed:` targets the beat does not list became `plugin:`). All applied: artwright 0.7.5 (PR #30), comfyui-gen PR #135 and #136, cinewright PR #75, ai-video vocab and questions, book note. Miss: comfyui-gen had already read this book (its PR #132, notes on a branch outside `books_read_index`), so one bullet was duplicated and then folded in. Tool changes: everscout 0.8.6 (`lit pick` flags read-elsewhere `lead` rows, 8 now; ingest names `rw.py ocr`), readwright 0.9.1 (PR #15: `printed_pages` offset in info, grep's `-i` hint).

## T-20261101-14: Making Music, Mark's nudge ("don't forget musicwright"), distilled from an earlier read

DeSantis was read in full on 2026-10-22 for musicwright (Ai/books/plugin-learnings) but its downtempo row stayed `lead`. `lit ingest`, learnings built from that read and checked against the toc (17 principles, sec. N citations), 4 changes all applied: downtempo vocab (3 techniques) and questions (2 seeds), musicwright 0.1.5 (PR #20, theory.md "Rhythm and groove", the five strategies the first pass left out), note. Lesson: `lit pick` skips a book the read index lists, but a beat row can still be `lead`; check both.

## T-20261101-13: Co-Intelligence, auto-pick, distilled end to end

Agent auto-pick for tech-hiring (DeSantis, the downtempo lead, was already read for musicwright; RL books skipped as over-represented). New recent row (Forbes 2024 list, NYT bestseller), `lit ingest`, two part readers, 17 principles, 4 changes, `lit lint` 0, all applied: tech-hiring vocab (AI at work, 6 ids), questions (4 seeds), study chapters 03-05, note. readwright 0.8.1 (PR #13): `--drop-repeated` drops endnote back-links repeated inside one section. One reader's friction list was mostly wrong (toc word counts, `--offset` and `grep --width` exist; its word-count mismatch was `wc` on cut output): check reader reports before building.

## T-20261101-12: Master Shots Vol. 1, auto-pick, distilled end to end

Agent auto-pick: `lit pick` listed it among unread files, and ai-video's literature lists Master Shots (series) as `lead`, unread anywhere, a move away from three RL books. `lit ingest` (folder named after the series row, Vol. 1 only), one reader agent on ch. 1-2, 9, 11 (fights, chases, cars, arguments); 18 principles, 9 changes, `lit lint` 0, pre-approved and applied: cinewright PR #74 (new cinewright-shots scene-setups.md plus rules in camera-moves, move-grammar, lens-choice, blocking, cutting-on-action), beat vocab and questions, note; `lit distill`, tally, index. Friction fixed in everscout 0.8.5: `lit ingest` wrote the UTC date (tomorrow on a US evening). The reader looped single sections, not knowing `--section N-M --quiet` exist, and every section carried a repeated image-credit line: readwright tip and a repeated-line filter. Pass.

## T-20261101-11: Video Generation with AI, Mark's topic pick, distilled end to end

Mark asked for a recent video-generation book, ComfyUI if possible. None in his folder names ComfyUI; Enochs, *Video Generation with AI* (O'Reilly 2026, epub) has 54 ComfyUI mentions. plugin-learnings had already harvested it broadly, so the reader was told to skip those points (metrics, LTX-2 internals, VACE repair, node security) and cover training, LoRA fine-tuning, Wan and systems. Latest-tier row in ai-video (O'Reilly page, retailer listing), `lit ingest`, one reader; 15 principles, 7 changes, `lit lint` 0, pre-approved and applied: beat vocab cfg-cost and wan-moe-experts plus two questions, comfyui-gen PR #134 (LoRA troubleshooting, trainer cache, VRAM-holding nodes), cinewright PR #73 (Wan 2.2 two experts verified against the Wan README and ComfyUI template; ltx-trainer option renamed, current name written); `lit distill`, tally, index. Friction fixed in readwright 0.7.0 (PR #11): one combined hint per read and `--quiet`, `--max-words` footer gives the resume offset, `--skip-code`, a technical-book reading tip. Pass.

## T-20261101-10: Grokking Deep Reinforcement Learning, auto-pick, distilled end to end

`lit pick`: 76 unread, none beat-listed; picked Morales, *Grokking Deep Reinforcement Learning* (Manning 2020; Mark's copy is the MEAP V11 pre-release PDF, 128k words): unread anywhere, and its bandit, horizon and environment chapters add to Lapan and Graesser. Recent-tier row in game-design (Manning page; author teaches Georgia Tech's RL and Decision Making course), `lit ingest`, one reader agent told to skip what the two earlier RL books cover; 15 principles, 6 changes, `lit lint` 0, pre-approved and applied: beat vocab multi-armed-bandit and rl-horizon plus two questions (indie-ai-scout PR #6), ludowright 0.1.21 (PR #28), unity-agent 1.2.11 (PR #28, `EpisodeInterrupted` checked against ML-Agents source), note; `lit distill`, tally, index. Friction fixed in everscout 0.8.4: from a `_wt/` worktree `lit ingest` printed the stale installed readwright 0.2.0 (now also looks beside the main checkout). readwright frictions (titles losing spaces, same-page sections sharing text, escaped quotes, repeated `--section`, page furniture) went to readwright 0.6.0. Pass.

## T-20261101-9: Foundations of Deep Reinforcement Learning, auto-pick, distilled end to end

`lit pick` (stale beats clone, so Lapan's other copies still listed): Co-Intelligence fits no beat, Brownlee's GAN book had only self-published evidence; picked Graesser & Keng, *Foundations of Deep Reinforcement Learning* (Addison-Wesley 2019, PDF): unread anywhere, its debugging and environment-design chapters add to Lapan. Recent-tier row in game-design (Pearson higher-education page, independent review; age warning like Play to Learn), `lit ingest`, one reader agent; 19 principles, 6 changes, `lit lint` 0, pre-approved and applied: beat vocab rl-debugging and action-space-design (indie-ai-scout PR #5), ludowright 0.1.20 (PR #27), unity-agent 1.2.10 (PR #27), note; `lit distill`, tally, index. Friction fixed in everscout 0.8.3 (PR #50): book folder cut mid-word; edition parenthetical kept other copies of a distilled book in `lit pick`; `lit lint` refused bare `(10.2.1)` citations. Open (readwright): `read --section` starts about a page early (the previous section's tail), and `grep --max` fills with early-chapter hits (no section filter). Pass.

## T-20261101-8: Deep Reinforcement Learning Hands-On, auto-pick, distilled end to end

`lit pick`: 83 unread, none beat-listed; picked Lapan, *Deep Reinforcement Learning Hands-On* 3rd ed. (Packt 2024, epub, 184k words): unread anywhere, feeds learned game agents. Recent-tier row in game-design (UW-Madison catalogue, O'Reilly), `lit ingest`, two part readers (ch. 1-10, ch. 11-22); 22 principles, 5 changes, `lit lint` 0, pre-approved and applied: beat vocab and a question (indie-ai-scout PR #4), ludowright 0.1.19 (PR #26), unity-agent 1.2.9 (PR #26, ML-Agents checklist checked against release 23 docs), note; `lit distill`, tally, index. Friction fixed: everscout 0.8.2 (PR #48) fails on a missing `EVERSCOUT_BEATS` folder (ingest ran before the worktree existed and fell back silently); readwright gets chapter-merged `toc` and `toc --depth` (EPUB chapter numbers were separate empty sections). Pass.

## T-20261101-7: One-hour Ancient and Medieval Skirmish Wargames, auto-pick, distilled end to end

`lit pick` listed Pixel Logic, FilmCraft and Blender Master Class though plugin-learnings had read them (short titles); verified by grep and skipped. Picked Lambshead, *One-hour Ancient and Medieval Skirmish Wargames* (Pen and Sword 2024, epub, 23k words): unread anywhere, a fast-play tabletop ruleset for game-design and ludowright. `lit ingest` (no literature row), 17 sections read directly; 17 principles, 7 changes, pre-approved and applied: beat vocab and a question (indie-ai-scout PR #3), ludowright 0.1.18 (PR #25: uncertainty 26-28, balance 24-26, scope 23-25, space 22-23), note; `lit distill`, tally, index. Friction fixed in everscout 0.8.1 (PR #47): `lit lint` rejected `(Player phase)` citations (now accepts toc section titles); `lit pick` short-title matches with a rare word nearby. Pass.

## T-20261102-2: Invisible Women, auto-pick, distilled end to end

Auto-pick (no beat-listed file unread; not RL, not ai-video): Criado Perez, *Invisible Women* (2019, epub, 111k words) into tech-hiring. Canon row from the 2019 Royal Society Science Book Prize and FT and McKinsey Business Book of the Year pages; Open Library OL20157508W. Reliability check passed (major publisher, endnotes, index; two spot checks pass, two contested or wrong as worded). Two parallel reader agents (ch. 3-6; Preface, Introduction, ch. 9, Afterword and grep hits), 14 principles, 4 changes, `lit lint` 0, all applied (vocab section, four questions, a study perspective, note); `lit distill`, tally, index. Friction fixed: `lit add` after ingest left the row `lead` and the folder's book_id `-` (0.9.1 links them); readwright 0.10.0 titles an untocced notes file `Endnotes: Chapter 13` and adds `rw.py note` to resolve a marker. Pass.

## T-20261102-1: Inside Palantir, auto-pick, rejected on a reliability check

Auto-pick (no beat-listed file unread): Elsen, *Inside Palantir* (2025, self-published, 14k words) into global-economics. Four sections read; three spot checks against Law360, VentureBeat, Bloomberg Law and Fortune: i2 and hiring-bias lawsuits misdated, a Senate hearing with no record. Row `skip`, 4 changes (3 applied, 1 rejected), `lit lint` 0, `lit distill`. Friction fixed in 0.9.0: no reliability step (kb step 1a, ingest warning) and `lit distill` overwrote `skip` with `distilled`. Pass.

## T-20261101-6: Unity 2018 AI Cookbook, `lit pick` auto-pick, distilled end to end

First run of `lit pick` (0.8.0): Palacios, *Unity 2018 Artificial Intelligence Cookbook* (Packt 2018, mobi, 51k words), the top unread plugin-relevant file. `lit ingest` into game-design (no literature row; a cookbook, not canon), one reader agent, 14 principles (7 new), 5 changes, `lit lint` 0, pre-approved and applied: beat vocab (indie-ai-scout PR #2), unity-agent 1.2.8 (PR #25), ludowright 0.1.17 (PR #24), note; `lit distill`. Friction fixed: readwright 0.4.0 (PR #7) names the recipe on generic repeated titles and adds `read --max-words`. Open: `lit pick` matches by file name, so books read under a different name (Azzi, DeSantis) still list; verify each pick. Pass.

## T-20261101-5: Beginning Game AI with Unity, auto-pick, distilled end to end

Agent auto-pick after every `lead` book in the folder proved already read; the first pick (a scanned PDF, 0 words) was dropped. `lit ingest` into game-design, ch. 1 and 5 read, ch. 2 to 4 by grep; 12 principles, 5 changes, `lit lint` 0; Mark pre-approved; unity-agent 1.2.7 (PR #24), ludowright 0.1.16 (PR #23), note; `lit distill`, tally, index. Friction: ingest accepts a file with no text layer; no `lit pick` to list unread books.

## T-20261101-4: AI for Games, auto-pick, distilled end to end

Agent auto-pick (no book named in the kickoff). Canon row (SDU DM810, Wrexham GME706), `lit ingest`, three part readers, 25 principles, 12 changes, `lit lint` 0, all approved and applied: beat vocab and questions (indie-ai-scout PR #1), ludowright 0.1.15 (PR #22), unity-agent 1.2.6 (PR #23), roblox-agent 0.1.9 (PR #22), book note; `lit distill`, tally, index. Friction fixed: readwright 0.3.0 (PR #6) prints grep offsets, adds `read --at-para` and flags giant PDF sections in `toc`. Pass.

### T-20261102-3: Prompt Engineering for LLMs, Mark's pick, distilled end to end

The session auto-picked Phoenix and Taylor, *Prompt Engineering for Generative AI* (ingested, row `reading`, not read further) before Mark named Berryman and Ziegler, *Prompt Engineering for LLMs* (O'Reilly 2024, EPUB, 89k words), a `lead` row in token-saving recent. `lit pick` had missed it: the file sat in a subfolder (fixed in 0.9.2). `lit ingest --id OL38627018W` set the row `reading`; 14 sections read with `rw.py read --max-chars`; 15 principles, 4 changes, `lit lint` 0 on first try; applied: beat vocab and questions (indie-ai-scout PR #7, #8), tokenwright 0.2.13 (PR #41; habits.md budget forced folding two rows into levers.md), note. `lit distill` wrote the book note. readwright 0.10.1 (PR #19) fixed the Phoenix PDF's split hyphens and running heads. Pass.

### T-20261102-4: Prompt Engineering for Generative AI, carried over, distilled end to end

The book ingested in T-20261102-3 (row `reading`) was finished: two parallel reader agents with `rw.py read --max-chars 30000` over ch. 1, 3, 4, 5, 6 (ch. 10 searched); 14 principles; `lit lint` 0 on first try with `EVERSCOUT_BEATS` set to a beats worktree; applied: token-saving vocab (history-trimming, few-shot-budget, chunk-overlap, hierarchical-summary aliases) and three question seeds (indie-ai-scout PR #9), note. `lit distill` wrote the book note and set the row `distilled`. readwright 0.10.2 (PR #20) fixed pipe-less running heads, page-break sentence splits, unhyphenated word splits, lost compound hyphens and inline captions. Pass.

### T-20261102-5: The Five C's of Cinematography, auto-pick, distilled from an earlier read

No book named. `lit pick`'s first candidate, Zhu, *Using Stable Diffusion with Python*, had been read on 2026-10-31 in comfyui-gen's notes, which the read index did not cover (Mark's `books_read_index` now includes comfyui-gen's `ai-docs/notes`). Its read-elsewhere line for Krug, *Don't Make Me Think*, came from a reading list, not a read (fixed in 0.9.3). Picked Mascelli (ai-video canon `lead`, read 2026-10-22 for cinewright). `lit ingest` refused the image-only EPUB; readwright's note named the DjVu twin, which ingested (90,633 words, one section). 14 principles from the earlier read, checked with `rw.py grep`; cinewright already held nearly all of them, so 3 changes went to the beat (7 vocab terms, three continuity questions, note; PR #75). `lit lint` 0 first try; `lit distill`, tally, index, beat-check 0. Friction fixed: everscout 0.9.3 (reading lists ignored, the stale line names its record, ingest's refusal passes readwright's note on); readwright: image-only EPUB OCR and heading splits for one-section books (separate agent).

### T-20261102-6: User Friendly, auto-pick into personal-sites

No book named and `lit pick` listed no beat-listed file (308 unread, 0 listed by a beat). Picked Kuang and Fabricant, *User Friendly* (FSG 2019) by topic: personal-sites had one book row read elsewhere and none distilled; the plugin-learnings index had not read it. Row added with `lit add` (canon; Amazon Best Books of 2019 and the NYT Book Review, found this session), `lit ingest` (41 sections, 120k words), reliability check passed, two parallel reader agents (ch. 1-5, ch. 6-10 and Afterword). 14 principles; 4 changes applied: vocab "Usability" section, three question seeds, sitewright-audit usability pass (sitewright PR #8), note. `lit lint` 0 errors first time; `lit distill` wrote the book note. Pass. Friction: one reader's 60,000-character cap cut a 60,750-character chapter mid-sentence; readwright 0.11.1 now cuts at a paragraph or sentence break.

### T-20261102-7: The Reverse Centaur's Guide to Life After AI, auto-pick into global-economics

No book named; `lit pick` listed 306 unread, none beat-listed, and no global-economics canon or recent book in the folder. Picked Doctorow, *The Reverse Centaur's Guide to Life After AI* (FSG/Verso 2026) by topic: the beat's AI-economics thread (Power and Progress) and only one book distilled; plugin-learnings had skipped it as a consumer AI book. Row added with `lit add` (recent, WAMC interview as evidence), `lit ingest` (33 sections, 51k words), one reader agent; reliability check passed 3/3 (Moffatt v. Air Canada $812.02, Nvidia ~$589B DeepSeek-day loss, Bartz v. Anthropic $1.5B). 18 principles; 3 changes applied: five vocab themes (ai-bubble, gpu-depreciation, surveillance-pricing, algorithmic-wage-discrimination, enshittification), three interpretation questions, note. `lit lint` 0 errors first time. Pass. Friction: the reader wanted per-section files for multi-chapter reads; readwright 0.12.0 `read --out-dir`. No everscout tool changes needed.

### T-20261102-8: Guerrilla Marketing, auto-pick into indie-ai-games

No book named; `lit pick` listed 304 unread, none beat-listed; the beat-listed books are not in the folder. Picked Levinson, *Guerrilla Marketing* (4th ed., 2007): not RL or ai-video, and it fills the beat's reception and marketing gap. `lit pick` had shown *Procedural 3D Modeling Using Geometry Nodes* as unread although plugin-learnings read it (slug file name); fixed in 0.9.4. One reader agent: its first pass sampled 3,500 characters a section and was sent back for a full read (17 principles). Lint failed once on quoted change text (0.9.4 hint). 7 changes applied: two Topics vocab terms, three Reception questions (indie-ai-scout PR #10), sitewright 0.2.0 audit check (PR #9), note. Distill, tally, index, lit check clean. Pass.

### T-20261102-9: Essentials of Economics, auto-pick into global-economics

No book named. `lit pick` listed `GenerativeDeepLearning.pdf` as unread although Foster's 2nd ed. was distilled into ai-video on 2026-10-31 (PR #43): CamelCase file name; fixed in 0.9.5. No beat-listed file left unread (301 unread). Picked Mateer, Coppock and O'Roark, *Essentials of Economics* (Norton 2016) for global-economics, which had no grounding text on reading data releases. Row added with `lit add` (recent, Judgment call: Mark's copy; Norton 2020 second-edition page as evidence; beat-check warns it is older than the recent window). Two parallel reader agents (ch. 10-13, ch. 14-18). 16 principles; 6 changes applied: five vocab terms (participation-rate, u6, long-term-unemployment, crowding-out, policy-lags), three question seeds, note. `lit lint` 0 errors first time; distill, tally, index, beat-check clean. Pass. Friction for readwright: stray carriage returns in PDF section titles, unexpanded ligatures, small-caps splits (Tabl e).

### T-20261102-10: Epistemic Injustice, auto-pick into tech-hiring

No book named. `lit pick` listed *FilmCraft Cinematography* as unread, but the 2026-10-22 plugin-learnings run had read it: 0.9.5's CamelCase split broke "FilmCraft" (fixed in 0.9.6). Picked Fricker, *Epistemic Injustice* (OUP 2007) for tech-hiring (credibility bias in interviews, next to the Criado Perez section). `lit ingest` made the slug `0198237901-oxford-university-press-usa` from the release-style file name (fixed in 0.9.6; re-ingested). The PDF has no outline (199 page sections): readwright 0.14.0 adds `toc --group` (22 chapter ranges) and drops repeated running heads under `--strip-boilerplate`. Canon row with syllabus and reading-list evidence. One reader agent; 22 principles; 4 changes applied (six vocab terms, four question seeds, note). `lit lint` 0 errors first time; distill, tally, index, lit check clean. Pass.
