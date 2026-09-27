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
