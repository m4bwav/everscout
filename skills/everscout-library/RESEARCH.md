# Research: everscout-library

Findings that back [SKILL.md](SKILL.md). Changes they caused are in [CHANGELOG.md](CHANGELOG.md); lessons in [LEARNINGS.md](LEARNINGS.md); tests in [TESTS.md](TESTS.md); schedule in `evergreen.json`.

Topic: keeping up with a subject's books and distilling a provided book. Tier `medium`. Created 2026-10-30.

## Current understanding

- **Open Library is the keyless book source (R-20261030-1).** `search.json` with `sort=new` and `fields` answers JSON with work keys, first publish year, ISBNs and subjects. The guidelines ask for a User-Agent with app name and contact (3 requests a second when identified, 1 otherwise), caching, and no bulk harvesting. https://openlibrary.org/developers/api (read 2026-10-30)
- **Google Books keyless is unusable (R-20261030-2).** On 2026-10-30 the keyless volumes endpoint answered 429 `RESOURCE_EXHAUSTED` on the shared anonymous daily quota. A key would be the user's to set up; not built.
- **Importance needs mixed evidence (R-20261030-3).** The first research pass for eight beats (ai-docs/research/2026-10-30-beat-literature.md) found practitioner listicles easy to get and syllabi or award lists harder; rows resting on one listicle are marked as judgment. Hence the two-kinds rule in kb/literature.md.
- The book-to-plugin distillation shape (principles cited by chapter, gaps naming a target file, proposals) follows the owner's 2026-10-22 book-learnings run, which worked across 19 tracks.
