# ElevateDigi — Action plan (baseline 2026-11-24)

Source: own crawl of 250 URLs (cap reached), `crawls/2026-11-24/`. No GSC data yet.

## P0 — Site-wide blockers (fix before any content/link work)

| # | Issue | Evidence | Fix | Tier | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | **Main site is invisible to crawlers.** React SPA serves an empty `<div id="root">`: no title, meta, H1, text, canonical or schema in HTML | 124/124 app URLs: 0 words, no `<title>` | Pre-render or SSR. Options in order of preference: (a) migrate to Next.js/Astro with static generation; (b) build-time prerender (vite-plugin-prerender / react-snap) for all routes; (c) prerender service at the edge for bots. Each route must ship its own title, meta, canonical, H1, body copy, JSON-LD | C | Dev | Open |
| 2 | **Soft 404s.** Any URL returns 200 with the app shell | `/this-page-should-404-seo-check` → 200 | Server returns real 404 for unknown routes (LiteSpeed/.htaccess rule or prerender 404 map) | C | Dev | Open |
| 3 | **Three hosts serve the site.** www and non-www both return 200; /blogs lives on non-www | host-variant check | Pick one host (recommend `https://www.theelevatedigi.com`), 301 everything else, including `/blogs/` | C | Dev | Open |
| 4 | **Duplicate blog.** 76 posts at `/blog/<slug>` (SPA) **and** `/blogs/<slug>` (WP) | crawl overlap | Keep one URL per post (recommend WP `/blogs/` until #1 ships). 301 the other version. Update sitemap & internal links | C | Dev | Open |
| 5 | robots.txt uses fake AI bot names and `Crawl-delay: 10`; blocks `/career/`, `/careers/` while the sitemap lists `careers` | robots.txt | Rewrite with real user agents (see `playbooks/aeo-geo.md`), drop crawl-delay, align with sitemap | B | AI | Draft ready on request |

## P1 — Within 30 days of P0

| # | Action | Why | Tier |
|---|---|---|---|
| 6 | Unique title/meta/H1/body for each location-service page (Kolkata, Mumbai, UAE) with real proof: client logos, case results, team, address | These are the money pages; currently empty to Google | A (draft) → B |
| 7 | Organization + ProfessionalService/LocalBusiness schema, `sameAs` (LinkedIn, GBP, Clutch, GoodFirms, DesignRush), real Kolkata NAP | Entity clarity for AI answers | B |
| 8 | Case studies with numbers (SIF, Mira, Abhyaass once results exist; with client permission) | Agency SEO converts on proof; LLMs cite specifics | A → C (permission) |
| 9 | WP blog clean-up: 125 posts with 2 H1s each (theme + content), 43 duplicate meta descriptions on paginated category pages, noindexed `/blogs/` root, `yoast-seo-vs-rank-math` noindexed | Quality + crawl budget | B |
| 10 | Consolidate thin/overlapping posts (multiple "SEO trends 2026", "SEO techniques 2026", "SEO fundamentals 2026") into one strong hub per topic, 301 the rest | Keyword cannibalisation | B/C |
| 11 | Google Business Profile for the Kolkata office: categories, services, photos, review programme | "digital marketing agency near me" | C (owner) |

## P2 — Authority & AI visibility (ongoing)
- Listings and profiles on Clutch, GoodFirms, DesignRush and Sortlist (India agency directories that LLMs cite).
- Founder thought-leadership on LinkedIn with original data from client work (anonymised).
- Monthly AI-visibility test: "best SEO agency in Kolkata", "AEO agency India", "who offers GEO services in Kolkata".

## KPIs to set once GSC/GA4 are connected
Non-brand organic clicks to service pages, organic leads (form submits from organic), AI mentions (x/20 prompts).
