# Learnings: everscout-ask

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first: add, update, retire, or none.

## Active

### L-001 · 2026-09-26 · Recall only finds what the vocabulary spells
- Trigger: the first recall on tech-hiring named no entity for "on-site" and "AI cheating"; the aliases were "onsite" and "interview cheating"
- Hypothesis: recall is word and alias matching, so a spelling the vocabulary lacks is invisible to it
- Rule: when a question names nothing, reword it in the beat's aliases before grading the recall as none, and add the missing spellings to `vocab.md`
- Evidence: tech-hiring build, 2026-09-26
- Scope: everscout-ask step 2; everscout-beat procedure C
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-26

### L-002 · 2026-09-29 · A thread's list of related-post titles is a search plan
- Trigger: on ai-video, a commenter answered a settings question with about 15 earlier thread titles; the thread view shows titles but no links
- Hypothesis: `ES search --kind reddit --community <sub> --q "<title words>" --t month` finds each one in a request, and those older threads held the substance (sampler, turbo and fast-motion threads) the new one lacked
- Rule: when a thread lists related posts, search two or three of the most relevant titles before going to the open web; keep them serial with other Reddit calls
- Evidence: ai-video asks, 2026-09-29 (three searches found 1wjsdoo, 1wqtn4c, 1wj6bkb)
- Scope: everscout-ask step 4
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-29
