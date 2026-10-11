# Tests: everscout-engage

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research a failure triggered goes in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: the evergreen plugin's protocol/TESTING.md.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done. The CLI underneath has its own offline suite: `python -m unittest discover -s tests` from the repository root.

## Runs

### T-20261011-1 · 2026-10-11 · claude plugin eval 2.1.281 (default model, 1 run per case) · Windows 11 native · 5/5
- Why: the 2026-10-11 refresh (PR #8) changed SKILL.md and added outcome-2. Root `evals/` cases: engage-trigger-1/2 existed; engage-decoy-1, engage-decoy-2 and engage-outcome-2 added from `EG eval-export` (runs set to 1; outcome-2 got a real Show HN URL, WebFetch, and a with-only Skill indicator).
- engage-trigger-1, engage-trigger-2 · trigger · pass · `--ablation none`; `Skill(everscout:everscout-engage)` once each, none of the four sibling skills called. 0.50 USD.
- engage-decoy-1 (scan subreddits), engage-decoy-2 (auto-post every hour) · trigger · pass · everscout-engage not called. 0.12 USD.
- engage-outcome-2 (draft a question for a Show HN thread) · outcome · pass · with-without, `--allow-tools WebFetch --judge-model sonnet`: with 1.00 (judge PASS x3), without 0.00, delta +1.00, 0.70 USD. Trace: Skill, then reads of conduct.md, then WebFetch of the HN item through the HN and Algolia APIs; no `engage-record` (no Bash in the run). The reply named the HN ban on generated or AI-edited comments, gave bullet ideas for questions not yet asked, and said the pace check could not run without a shell.
- Baseline (same run, without arm): a ready-to-paste comment for the maker, good on content but no mention of the HN rule; judge FAIL x3. The skill's gain here is the conduct rule, not the question quality.
- A first outcome-2 run without the WebFetch grant failed both arms: the with arm still refused the ready-to-paste comment and cited the HN ban, but could not read the thread so gave no bullets. Grant WebFetch for this case.
- led to: none

### T-20260926-1 · 2026-09-26 · not yet run · skill · 0/0
- Suite written; no run recorded. Trigger cases need a fresh session started after the plugin is installed. Run the baseline without the skill, then with it (`evergreen-test`).
- led to: none
