# Beat literature: book sources and the first research pass (2026-10-30)

Why: the user asked everscout to keep up with each beat's books (the most important of all time, the most important recent, the latest published) and to distil a provided book into the beat and the skills it feeds. Built as `everscout.py lit` and the everscout-library skill (0.7.0).

## Book APIs, checked live 2026-10-30

- **Open Library `search.json`**: answers JSON with `sort=new`, `fields=`, work keys (`/works/OL...W`), `first_publish_year`, ISBNs, subjects, languages. The guidelines (https://openlibrary.org/developers/api) ask for a User-Agent with app name and contact (3 requests a second identified, 1 otherwise), caching, no HTML scraping, no bulk harvesting. `robots.txt` disallows `/search` for crawlers; the JSON API is the documented route for applications. everscout: 1 s per request, cached a day.
- **Google Books keyless** `volumes?q=...&orderBy=newest`: HTTP 429 `RESOURCE_EXHAUSTED`, "Queries per day" on the shared anonymous project. Not used.

## First research pass

Three research agents (web search plus Open Library lookups) built canon and recent tables for the five built-in beats and three private beats; `lit new` filled the latest tier. Findings:

- Practitioner "best books" lists are easy to find. Syllabi, award lists and citation counts were barely checked, so about half the rows rest on one source; their `why` starts "Judgment call". Rechecking those is the first job of the next canon pass.
- Young subjects (AI video, token saving for agents) have no canon of their own; their canon is the older craft (film editing and cinematography; lean and flow thinking, retrieval).
- personal-sites has no strong 2021 to 2026 book on the personal site itself; downtempo has no recent trip-hop history; indie-ai-games has no good book on AI-assisted indie game making. Gaps, not omissions.
- `lit new` noise: self-published titles, a content-farm imprint with a dozen 2026 "Claude Code" books, IMF country reports under macroeconomics subjects. Kept 4 latest books across 8 beats.
- Research files stored queries URL-encoded with fixed year ranges (`q=subject:%22...%22+first_publish_year:[2020+TO+2026]`); `lit new` returned nothing until `lit_clean_query` undid both.

## Books for the user's plugins

A separate pass proposed 25 books across 13 plugins (8 for everscout itself: Kozinets *Netnography*, Hines and Bishop on foresight, Webb *The Signals Are Talking*, Heuer *Psychology of Intelligence Analysis* (free), Bazzell *OSINT Techniques*, Portigal *Interviewing Users*, the AoIR ethics guidelines 3.0 (free), Meadows *Thinking in Systems*). The list lives outside this public repository, with the user's other reading lists.
