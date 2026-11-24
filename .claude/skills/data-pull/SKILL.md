---
name: data-pull
description: "Pull real performance data for a client through the user's signed-in Chrome: Google Search Console (queries, pages, countries, devices, indexing, sitemaps, manual actions, security), GA4 (organic sessions and key events such as forms, WhatsApp and calls), Google Business Profile performance, and Bing Webmaster Tools. Saves exports in the client's data folder and summarises them. Use for 'pull GSC', 'how is <client> doing', 'rankings', 'traffic', 'what queries', 'indexing status', and inside weekly-check, site-audit, keyword-research and monthly-report."
metadata:
  version: "1.0.0"
---

# Data pull via Chrome (Tier A: read and export only)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md`. Before reading anything, confirm the
selected property matches the client (domain in the property picker and URL bar).

## Google Search Console
1. Open `https://search.google.com/search-console?resource_id=<property>` (Domain property
   `sc-domain:<domain>` preferred; otherwise the URL-prefix property). Find it in the property picker.
2. **Performance → Search results.** Date: *Compare* last 28 days vs previous 28 days (weekly: last 7
   vs previous 7; monthly report: last month vs previous month, and vs same month last year if 16
   months of data exist). Tick Clicks, Impressions, CTR, Position.
3. **Export** (top right) → *Download CSV*. The zip lands in `_inbox/`. Move it to
   `clients/<slug>/data/<YYYY-MM-DD>-gsc-<range>.zip`, then run:
   `python3 "cowork/elevatedigi-seo-lead/tools/gsc_summary.py" clients/<slug>/data/<file>.zip --out clients/<slug>/data/<YYYY-MM-DD>-gsc-summary.md`
4. **Indexing → Pages:** record indexed / not indexed counts and the top reasons (with counts).
5. **Sitemaps:** status, discovered URLs, last read.
6. **Security & Manual actions:** must read "No issues detected". Anything else → ALERT.
7. For specific URLs: **URL Inspection** → coverage, Google-selected canonical, last crawl.
   "Request indexing" is Tier B (approval first).
If the export can't be downloaded, read the tables on screen (top 25 queries and pages) and say so.

## GA4
1. `https://analytics.google.com/` → select the client's property.
2. Reports → Acquisition → **Traffic acquisition**. Filter *Session default channel group = Organic
   Search* (also note "Organic Shopping" and referral from chatgpt.com / perplexity.ai / gemini.google.com
   / copilot.microsoft.com as **AI referrals**). Same date ranges as GSC.
3. Reports → Engagement → **Events / Key events**: forms (`generate_lead`, `form_submit`), WhatsApp and
   tel click events. If none exist, record "conversion tracking missing" as a P1 action (Tier C:
   set up via GTM by the developer).
4. Export (Share → Download CSV) to the client's `data/` folder, or read on screen.

## Google Business Profile (local clients)
business.google.com → the location → **Performance**: calls, direction requests, website clicks,
bookings, searches by keyword (last month vs previous). Reviews: count, average rating, unanswered reviews.

## Bing Webmaster Tools
bing.com/webmasters → site → Search Performance (clicks, impressions), Sitemaps, **Site Scan** issues,
and whether IndexNow is active.

## Output
Write `clients/<slug>/data/<YYYY-MM-DD>-snapshot.md`: every metric with source + date range, and a
"what changed and likely why" section. Update `keywords.csv` with `gsc_avg_position`, clicks and impressions
for tracked keywords. Log the pull in `log.md`.
