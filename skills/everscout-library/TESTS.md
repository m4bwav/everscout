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

## T-20261101-10: Grokking Deep Reinforcement Learning, auto-pick, distilled end to end

`lit pick`: 76 unread, none beat-listed; picked Morales, *Grokking Deep Reinforcement Learning* (Manning 2020; Mark's copy is the MEAP V11 pre-release PDF, 128k words): unread anywhere, and its bandit, horizon and environment chapters add to Lapan and Graesser. Recent-tier row in game-design (Manning page; author teaches Georgia Tech's RL and Decision Making course), `lit ingest`, one reader agent told to skip what the two earlier RL books cover; 15 principles, 6 changes, `lit lint` 0, pre-approved and applied: beat vocab multi-armed-bandit and rl-horizon plus two questions (indie-ai-scout PR #6), ludowright 0.1.21 (PR #28), unity-agent 1.2.11 (PR #28, `EpisodeInterrupted` checked against ML-Agents source), note; `lit distill`, tally, index. Friction fixed in everscout 0.8.4: from a `_wt/` worktree `lit ingest` printed the stale installed readwright 0.2.0 (now also looks beside the main checkout). readwright frictions (titles losing spaces, same-page sections sharing text, escaped quotes, repeated `--section`, page furniture) went to readwright 0.6.0. Pass.

## T-20261101-9: Foundations of Deep Reinforcement Learning, auto-pick, distilled end to end

`lit pick` (stale beats clone, so Lapan's other copies still listed): Co-Intelligence fits no beat, Brownlee's GAN book had only self-published evidence; picked Graesser & Keng, *Foundations of Deep Reinforcement Learning* (Addison-Wesley 2019, PDF): unread anywhere, its debugging and environment-design chapters add to Lapan. Recent-tier row in game-design (Pearson higher-education page, independent review; age warning like Play to Learn), `lit ingest`, one reader agent; 19 principles, 6 changes, `lit lint` 0, pre-approved and applied: beat vocab rl-debugging and action-space-design (indie-ai-scout PR #5), ludowright 0.1.20 (PR #27), unity-agent 1.2.10 (PR #27), note; `lit distill`, tally, index. Friction fixed in everscout 0.8.3 (PR #50): book folder cut mid-word; edition parenthetical kept other copies of a distilled book in `lit pick`; `lit lint` refused bare `(10.2.1)` citations. Open (readwright): `read --section` starts about a page early (the previous section's tail), and `grep --max` fills with early-chapter hits (no section filter). Pass.

## T-20261101-8: Deep Reinforcement Learning Hands-On, auto-pick, distilled end to end

`lit pick`: 83 unread, none beat-listed; picked Lapan, *Deep Reinforcement Learning Hands-On* 3rd ed. (Packt 2024, epub, 184k words): unread anywhere, feeds learned game agents. Recent-tier row in game-design (UW-Madison catalogue, O'Reilly), `lit ingest`, two part readers (ch. 1-10, ch. 11-22); 22 principles, 5 changes, `lit lint` 0, pre-approved and applied: beat vocab and a question (indie-ai-scout PR #4), ludowright 0.1.19 (PR #26), unity-agent 1.2.9 (PR #26, ML-Agents checklist checked against release 23 docs), note; `lit distill`, tally, index. Friction fixed: everscout 0.8.2 (PR #48) fails on a missing `EVERSCOUT_BEATS` folder (ingest ran before the worktree existed and fell back silently); readwright gets chapter-merged `toc` and `toc --depth` (EPUB chapter numbers were separate empty sections). Pass.

## T-20261101-7: One-hour Ancient and Medieval Skirmish Wargames, auto-pick, distilled end to end

`lit pick` listed Pixel Logic, FilmCraft and Blender Master Class though plugin-learnings had read them (short titles); verified by grep and skipped. Picked Lambshead, *One-hour Ancient and Medieval Skirmish Wargames* (Pen and Sword 2024, epub, 23k words): unread anywhere, a fast-play tabletop ruleset for game-design and ludowright. `lit ingest` (no literature row), 17 sections read directly; 17 principles, 7 changes, pre-approved and applied: beat vocab and a question (indie-ai-scout PR #3), ludowright 0.1.18 (PR #25: uncertainty 26-28, balance 24-26, scope 23-25, space 22-23), note; `lit distill`, tally, index. Friction fixed in everscout 0.8.1 (PR #47): `lit lint` rejected `(Player phase)` citations (now accepts toc section titles); `lit pick` short-title matches with a rare word nearby. Pass.

## T-20261101-6: Unity 2018 AI Cookbook, `lit pick` auto-pick, distilled end to end

First run of `lit pick` (0.8.0): Palacios, *Unity 2018 Artificial Intelligence Cookbook* (Packt 2018, mobi, 51k words), the top unread plugin-relevant file. `lit ingest` into game-design (no literature row; a cookbook, not canon), one reader agent, 14 principles (7 new), 5 changes, `lit lint` 0, pre-approved and applied: beat vocab (indie-ai-scout PR #2), unity-agent 1.2.8 (PR #25), ludowright 0.1.17 (PR #24), note; `lit distill`. Friction fixed: readwright 0.4.0 (PR #7) names the recipe on generic repeated titles and adds `read --max-words`. Open: `lit pick` matches by file name, so books read under a different name (Azzi, DeSantis) still list; verify each pick. Pass.

## T-20261101-5: Beginning Game AI with Unity, auto-pick, distilled end to end

Agent auto-pick after every `lead` book in the folder proved already read; the first pick (a scanned PDF, 0 words) was dropped. `lit ingest` into game-design, ch. 1 and 5 read, ch. 2 to 4 by grep; 12 principles, 5 changes, `lit lint` 0; Mark pre-approved; unity-agent 1.2.7 (PR #24), ludowright 0.1.16 (PR #23), note; `lit distill`, tally, index. Friction: ingest accepts a file with no text layer; no `lit pick` to list unread books.

## T-20261101-4: AI for Games, auto-pick, distilled end to end

Agent auto-pick (no book named in the kickoff). Canon row (SDU DM810, Wrexham GME706), `lit ingest`, three part readers, 25 principles, 12 changes, `lit lint` 0, all approved and applied: beat vocab and questions (indie-ai-scout PR #1), ludowright 0.1.15 (PR #22), unity-agent 1.2.6 (PR #23), roblox-agent 0.1.9 (PR #22), book note; `lit distill`, tally, index. Friction fixed: readwright 0.3.0 (PR #6) prints grep offsets, adds `read --at-para` and flags giant PDF sections in `toc`. Pass.
