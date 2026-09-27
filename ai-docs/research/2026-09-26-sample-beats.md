---
title: Sources, vocabularies and question banks for three starter beats (AI video, global economics, down-tempo)
kind: research
status: active
date: 2026-09-26
verified: 2026-09-26
tags: [beats, ai-video, economics, downtempo, reddit, feeds, youtube]
summary: read before editing a built-in beat; which communities and feeds were verified on 2026-09-26, their activity and stance, the context behind each vocabulary, and what was left unverified
---

# Starter beats research (2026-09-26)

## Summary

Three beats researched in one pass: AI video (a maker community, open about AI, busy), global economics (analysis and data, few "makers", strict subreddits), down-tempo (musicians, broadly hostile to AI music). Every subreddit below was seen in Reddit's feeds on 2026-09-26; activity is posts a day estimated from a multireddit window. Member counts are GummySearch figures (R). Written subreddit rules could not be read (reddit.com blocks the agent's web fetch), so stances are `~` unless a moderator post title confirmed them. V = fetched today; R = reported; U = unverified or conflicting.

## Method findings (for the CLI)

- Multireddit feeds work logged out: `https://www.reddit.com/r/a+b+c/new/.rss?limit=100` returns the newest 100 posts across the listed subreddits, each tagged with `category term="<sub>"` (V). One request can cover several quiet subreddits; a busy one fills the window, so batching needs a fallback.
- Requests 7 s apart drew 429; 45 to 60 s apart worked (V).
- hnrss.org returned 502 (V); the Algolia API worked.
- Six AI video subreddits did not appear in any window and were dropped: aicinema, aifilms, AIGeneratedVideo, AIVideoGenerators, HailuoAI, WanVideo. For economics: macroeconomics, ukeconomy, China_Economy, DevelopmentEconomics (quiet or gone). For music: balearic, trip_hop, Lofi_Producers, ElectronicMusicProd.

## A. AI video

Subreddits (posts a day V; members R): r/aivideo about 42 (396k; the core showcase sub, tool questions common), r/StableDiffusion about 78 (1.0M; open-source and local, "Workflow Included" flair), r/comfyui about 55 (212k; Show and Tell; people expect a workflow), r/SoraAi about 13 (91k; now "a hub for AI video generation, open and closed" after Sora's shutdown), r/aivideos (124k), r/AIFilmmaking about 8 (narrative work), r/generativeAI about 33 (156k; vendor spam), r/aiArt about 80 (mostly images), r/MiniMax_AI about 4, r/VEO3 about 3.5 (36k), r/KlingAI_Videos about 1.6 (31k), r/LTXvideo about 2, r/seedance about 2, r/runwayml about 1.6, r/HiggsfieldAI about 1.6 (vendor-adjacent), r/midjourney about 6, r/Filmmakers about 23 (hostile to AI; sentiment only), r/VideoEditing about 3, r/singularity (news, hype-prone).

Feeds (V): GitHub releases for Comfy-Org/ComfyUI (moved from comfyanonymous; v0.37.0 on 2026-09-21), Wan-Video/Wan2.2, Lightricks/LTX-2 (v1.3.0 on 2026-08-26; the old LTX-Video feed is stale), Lightricks/ComfyUI-LTXVideo, MiniMax-AI/MiniMax-H3; kijai/ComfyUI-WanVideoWrapper commits (cooling since May 2026). Hugging Face trending for text-to-video and image-to-video (MiniMax-H3 derivatives, LTX-2.5 and LTX-2.3 lead). Blogs: blog.comfy.org/feed, deepmind.google/blog/rss.xml, blog.google/technology/ai/rss/, therundown.ai/feed, bensbites.com/feed, curiousrefuge.com/blog?format=rss. No feed: Runway (404), the Artificial Analysis video leaderboard (read the page). Mastodon `mastodon.social/tags/aivideo.rss` (low volume). HN: `"video model"` with points above 30 gave 26 stories in 90 days; model names alone gave almost nothing. Banodoco's Discord is unreadable; banodoco.ai and github.com/banodoco are.

YouTube channel ids (V, active Sept 2026): Theoretically Media UC9Ryt3XOGYBoAJVsBHNGDzA, Curious Refuge UClnFtyUEaxQOCd1s5NKYGFA, Olivio Sarikas UCCKx8mAHiFus-XYQLy_WnaA, Sebastian Kamph UCvKqTb-65iAmXK59sFNKINQ, pixaroma UCmMbwA-s3GZDKVzGZ-kPwaQ, Nerdy Rodent UC4-5v-f-xKnbi1yaAuRSi_w, MattVidPro UC5Wz4fFacYuON6IKbhSa7Zw, Purz UCzkUNNsV1TYuf6U_wGnMlnw.

Model context (R unless marked): Veo 3.1 (Veo 4 not released at I/O 2026); Gemini Omni Flash (2026-05-19; first with audio on Artificial Analysis, Elo 1233, V); Sora 2 (app ended April 2026, API closed 2026-09-24); Kling 3.0 with Turbo and Omni (2026-06-17), Kling O1, 2.6, Kling 4.0 expected (U); Runway Gen-4.5 and Aleph 2.0 (no Gen-5); Seedance 2.0 (AA 5th, V) and 2.5 (30 s clips, announced 2026-06-23); Luma Ray3; Pika 2.5; Grok Imagine; Midjourney video (version U); SkyReels V4 and MAGI-2 and HappyHorse (V on AA); MiniMax H3 (33B, stereo audio, AA 3rd to 4th); Wan 3.0 (AA 2nd, V; closed weights R), Wan 2.7 (open or API-only conflicts, U), Wan 2.2 (Apache-2.0, V); LTX-2.5 (2026-07-23, V), LTX-2.3; HunyuanVideo 1.5. LTX's licence has a revenue cap.

Do not trust: vendor launch reels, "best AI video generator" listicles by resellers, benchmark claims without confidence intervals, "which is best" threads seeded by aggregators, "open source" without a licence check.

## B. Global economics

Context as of 2026-09-26 (R): Fed chair Kevin Warsh; the Fed hiked 25 bp to 3.75 to 4.00 percent on 2026-09-16 (12-0, first hike since 2023); the ECB hiked 25 bp to a 2.50 percent deposit rate (10 Sep); the Bank of England held at 3.75 percent (6-3, three for a hike), UK CPI 3.1 percent; Brent about 90 to 100 dollars in a Middle East energy shock; the Supreme Court struck down IEEPA tariffs on 2026-02-20 (Learning Resources v. Trump), a Section 122 10 percent surcharge followed (150-day cap; status after that U); IMF and World Bank Annual Meetings in Bangkok 12 to 18 Oct 2026 with the October WEO; OECD's September interim outlook put 2026 global growth at 2.6 percent.

Subreddits: r/Economics about 8.7 a day (5.8M; link posts, comments must engage the article), r/AskEconomics about 12 (1.5M; in-depth answers only), r/badeconomics (772k; quiet), r/econmonitor about 0.7 (45k; data releases and professional commentary, no news or opinion; highest signal), r/academiceconomics about 2.7, r/econometrics about 3.3 (method questions welcome), r/EconomicHistory about 2, r/bonds about 20, r/economy about 35 (partisan noise), r/dataisbeautiful about 14 (OC charts must state source and tool: the best place to find chart makers), r/neoliberal about 17, r/geopolitics about 8 (submission statement required), r/investing about 14, r/supplychain about 3.3, r/indianeconomy about 7, r/georgism about 4.7, r/mmt_economics about 1.3, r/austrian_economics about 0.7 (school-specific).

Feeds (V, September posts unless noted): noahpinion.blog/feed, adamtooze.substack.com/feed, marginalrevolution.com/feed, paulkrugman.substack.com/feed, libertystreeteconomics.newyorkfed.org/feed/, fredblog.stlouisfed.org/feed/, bankunderground.co.uk/feed/, conversableeconomist.com/feed/, employamerica.org/feed, ourworldindata.org/atom.xml, slowboring.com/feed, ft.com/alphaville?format=rss (paywalled bodies), econlib.org/feed/, resolutionfoundation.org/feed/, cepr.org/rss.xml, bruegel.org/rss.xml (last post July). Official: federalreserve.gov/feeds/press_all.xml, ecb.europa.eu/rss/press.html and /rss/blog.html, bankofengland.co.uk/rss/news, apps.bea.gov/rss/rss.xml, BIS doclists (cbspeeches.rss, wppubls.rss). Stale or broken: Apricitas (last 2026-03-05), Kyla Scanlon (May), Calculated Risk (Blogger feed ends January 2026), The Overshoot (Cloudflare), Brad Setser's Follow the Money (no working feed), PIIE and CGD (404, 403), BLS and IMF RSS (403 to scripts), World Bank blogs (404).

YouTube (V): Money and Macro UCCKpicnIwBP3VPxBAZWDeNA, Economics Explained UCZ4AMrDcNrfy3X6nsU8-rPg, Ben Felix UCDXTQ8nWmx_EhZ2v-kp7QxA, The Economist UC0p5jTq6Xx_DosDFxVXnWaQ, IMF UCIYhr3JsLYfKkCM7-W5B6DA, Federal Reserve UCAzhpt9DmG6PnHXjmJTvRGQ.

Fediverse and Bluesky: econtwitter.net/tags/econsky.rss, mastodon.social/tags/econtwitter.rss and /tags/economics.rss (V). Bluesky profile RSS works, but check activity per account (Tooze's last Bluesky post was October 2025). Starter packs (R): "Excellent Posting Economists", "Business Economists", The Economist's pack, Aaron Sojourner's guide. HN: "inflation" gave 49 stories in 30 days (V).

Do not trust: partisan outlets and think tanks without naming their lean, "collapse" blogs, r/economy virality, charts without source or units, nominal versus real confusion, single prints as trends, preliminary data without revisions, unsourced consensus figures, AI-written summary sites.

## C. Down-tempo

Context (R): Bandcamp banned music "generated wholly or in substantial part by AI" (2026-01-13); SubmitHub banned AI submissions (Sept 2026); TIDAL pays no royalties on fully AI tracks; Ninja Tune was acquired by Concord (March 2026) and Concord is merging into BMG (announced September 2026); Bonobo released Distance in Static (2026-09-11); Emancipator released Chrysalis (2026). Bandcamp Daily's "Trip Hop Strikes Back" (2026-04-15, V) covers the revival: labels 3XL, Pace Yourself, Efficient Space; artists a.s.o., trickpony, Headache, Erika de Casier, Stone, james K, YS, Th Blisks.

Subreddits: r/triphop about 9 a day (41k; Original Content flair; hostile to AI in practice, no written rule found), r/ambientmusic about 7.6 (131k; frequent "is this AI?" threads), r/LofiHipHop about 5 (1.4M; bans AI music, moderator post 2024-08-28, widened to "all AI slop" 2025-11-10, V titles), r/downtempo about 1.4, r/chillout about 0.5, r/lofi about 0.9, r/chillhop about 1.5, r/chillmusic about 4.5 (posters label tracks "NOT AI"), r/idm about 6, r/boardsofcanada about 6.5 (BoC-style production posts common), r/ambient about 4, r/Dubtechno about 2, r/Chillwave about 1, r/Vaporwave about 8, r/WeAreTheMusicMakers about 4 (3.8M; promotion only in the weekly thread; AI posts banned), r/synthesizers about 39 (moderator post on AI and vibe-coding 2026-05-21), r/ableton about 23, r/edmproduction about 8, r/electronicmusic about 17, r/makinghiphop about 11, r/modular about 17, r/Samplehunters about 5.5, r/musicproduction about 5.5.

Forums and feeds (V): elektronauts.com/latest.rss (very active), kvraudio.com/forum/feed (Atom), daily.bandcamp.com/feed, acloserlisten.com/feed/, ambientblog.net/blog/feed/, headphonecommute.com/feed/ (August), thequietus.com/feed, attackmagazine.com/feed/, cdm.link/feed/, musicradar.com/feeds.xml, igloomag.com/feed, stereofox.com/feed/, pitchfork.com/feed/feed-album-reviews/rss, ra.co/xml/podcast.xml, musicforprogramming.net/rss.xml, tru-thoughts.co.uk/feed/, wahwah45s.com/feed, om-records.com/news?format=rss. Not readable: lines (llllllll.co, 403 to the agent; Discourse, so try `/latest.rss` again), Gearspace (Cloudflare), Ninja Tune site, Compost and Café del Mar (no feeds), Bandcamp tag pages (HTML only, and Bandcamp forbids scraping), Discogs (403 to scripts). Dead: Fact (April 2026), XLR8R (2024). HN: "ambient music" had no stories in 30 days; skip HN for this beat. Mastodon `mastodon.social/tags/ambient.rss` (V).

YouTube (V): Lofi Girl UCSJ4gkVC6NrvII8umztf0Ow, Chillhop Music UCOxqgCwgOqC2lMqC5PYz_Dg, Café del Mar Music UCCVnnVO0zRVPD5FFgz3WwcQ (last upload March), Ninja Tune UCEXRv_qihRwjsV91ftx23-A, loopop UC-RA5BzE_BnZhf5iVdNF1hA, Red Means Recording UChnxLLvzviaR5NeKOevB8iQ, Andrew Huang UCdcemy56JtVTrsFIOoqvV8g.

Rule for asking: never ask a musician whether a track used AI; across these communities it reads as an accusation.

Do not trust: SEO chill-playlist farms and playlist-pitching services, AI mood-music channels, "top 50 downtempo artists" lists, AI-written genre explainers (one search summary invented a 2026 Bonobo album "Fragments"), gear-shop "producer secrets".

## Unfinished

Written subreddit rules (only r/LofiHipHop's AI ban confirmed by moderator post titles; r/WeAreTheMusicMakers from its wiki via Wayback in the ethics note); subscriber counts for r/downtempo and r/Dubtechno; lines and Gearspace feeds; a Setser feed; Bluesky music accounts; the Wan 2.7 licence; Section 122 after July 2026; the current ECB and BoE heads.

Related: [platform access](2026-09-26-platform-access.md), [engagement ethics](2026-09-26-engagement-ethics.md), [prior art](2026-09-26-prior-art.md)
