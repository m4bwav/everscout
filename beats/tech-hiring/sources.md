# Sources: Developer and tech hiring

The watch list. Columns and markers: `beats/_template/sources.md` and `kb/SCHEMA.md`. Built 2026-09-26: every row was fetched by `everscout.py probe --beat tech-hiring` on that date. Written subreddit rules could not be fetched (old.reddit.com and the rules pages refuse the agent's web fetch), so Reddit stances are `~` from sidebar text quoted in search results and from the posts in the feed; read the rules page before relying on a stance.

| source | kind | group | stance | engage | scan | filter | notes |
|---|---|---|---|---|---|---|---|
| r/cscareerquestions | reddit | candidates | native | yes | yes | | ~ the largest CS career sub (over 1M members); search reports, interview stories, market threads. Feed ✓ 2026-09-26 |
| r/csMajors | reddit | candidates | native | yes | yes | | ~ students and new grads; internships, new-grad market, OA and interview reports. Feed ✓ 2026-09-26 |
| r/ExperiencedDevs | reddit | candidates | native | yes | yes | hiring interview interviewing job market layoff recruiter offer candidate | ~ 3+ years of experience required to post or comment outside the weekly Ask thread (sidebar rule, quoted by reddifier.com); engage only if the user qualifies. Feed ✓ 2026-09-26 |
| r/cscareerquestionsEU | reddit | candidates | native | yes | yes | | ~ European market; salaries, visas, relocation. Feed ✓ 2026-09-26 |
| r/cscareerquestionsCAD | reddit | candidates | native | no | yes | | ~ Canadian market. Feed ✓ 2026-09-26 |
| r/developersIndia | reddit | candidates | native | no | yes | hiring interview job layoff offer notice period recruiter GCC | ~ very large and busy; filter keeps the hiring threads. Feed ✓ 2026-09-26 |
| r/leetcode | reddit | interviews | native | yes | yes | interview onsite offer OA loop cheating AI | ~ interview reports by company; filter drops pure problem talk. Feed ✓ 2026-09-26 |
| r/recruitinghell | reddit | sentiment | anti | no | yes | | ~ candidate venting about recruiters and processes; read for sentiment only. Feed ✓ 2026-09-26 |
| r/recruiting | reddit | hiring side | open | yes | yes | tech engineer software developer AI ATS interview | ~ practitioner recruiters; filter keeps tech hiring. Feed ✓ 2026-09-26 |
| r/EngineeringManagers | reddit | hiring side | open | yes | yes | hiring interview candidate recruit headcount offer | ~ managers discussing hiring and interviewing. Feed ✓ 2026-09-26 |
| r/humanresources | reddit | hiring side | mixed | no | no | | ~ HR practitioners; mostly non-tech; kept for reference. Feed ✓ 2026-09-26 |
| r/jobs | reddit | candidates | mixed | no | no | | ~ general job seeking, very broad; kept for reference. Feed ✓ 2026-09-26 |
| r/layoffs | reddit | market | native | no | yes | tech software engineer developer | ~ layoff news and stories. Feed ✓ 2026-09-26 |
| r/h1b | reddit | market | native | no | yes | fee lottery layoff transfer RFE | ~ visa holders; fee and lottery changes move tech hiring. Feed ✓ 2026-09-26 |
| r/overemployed | reddit | sentiment | mixed | no | no | | ~ people holding two remote jobs; interview-fraud angle; kept for reference. Feed ✓ 2026-09-26 |
| "Ask HN: Who is hiring" | hn | market | n/a | no | yes | | ✓ 2026-09-26 query finds the 2026-09-01 thread; its comment count is a demand signal |
| "Ask HN: Who wants to be hired" | hn | market | n/a | no | yes | | ✓ 2026-09-26 query finds the 2026-09-01 thread; the monthly supply thread |
| "layoffs" | hn | market | n/a | no | yes | tech software engineers AI | ✓ 2026-09-26 17 stories in the window; several a week, a few with long threads |
| "interview" | hn | interviews | n/a | no | yes | +interview hiring coding technical candidates leetcode | ✓ 2026-09-26 50 hits, broad, so the filter requires the word interview |
| "job market" | hn | market | n/a | no | yes | software engineers developers tech hiring | ✓ 2026-09-26 7 stories in the window |
| https://hiringlab.indeed.com/feed/ | rss | data | n/a | no | yes | | ✓ 2026-09-26 feed read: monthly US snapshot, software postings, AI and seniority analyses |
| https://newsletter.pragmaticengineer.com/feed | rss | analysis | n/a | no | yes | hiring job market interview layoffs recruit | ✓ 2026-09-26 feed read; filter keeps the job-market issues |
| https://news.crunchbase.com/feed/ | rss | market | n/a | no | yes | layoffs hiring headcount | ✓ 2026-09-26 feed answers; Crunchbase News keeps the US tech layoffs tracker |
| interviewing.io blog | web | interviews | n/a | no | no | | ✓ 2026-09-26 no feed (rss.xml, /feed and /blog/rss all 404); read interviewing.io/blog by hand monthly; vendor, but publishes interview data |
| tech layoffs | news | market | n/a | no | yes | | ✓ 2026-09-26 Google News answers; official announcements |
| software engineer hiring | news | market | n/a | no | yes | | ✓ 2026-09-26 Google News answers |
| AI job interview cheating | news | interviews | n/a | no | yes | | ✓ 2026-09-26 Google News answers; interview-format changes |
| #GetFediHired@mastodon.social | mastodon | market | open | no | no | | ✓ 2026-09-26 feed answers; job ads on the fediverse; kept for reference and counting only |
| #layoffs@mastodon.social | mastodon | market | open | no | yes | tech software | ✓ 2026-09-26 feed answers, 20 items |
| layoffs.fyi | web | data | n/a | no | no | | ~ tracker, no feed; read by hand monthly |
| trueup.io/layoffs | web | data | n/a | no | no | | ~ tracker with open-jobs counts; read by hand monthly |
| FRED IHLIDXUSTPSOFTDEVE | web | data | n/a | no | no | | ~ Indeed software development postings index on FRED; fetch the series monthly |
| BLS JOLTS | web | data | n/a | no | no | | ~ openings and hires, information sector; monthly |
