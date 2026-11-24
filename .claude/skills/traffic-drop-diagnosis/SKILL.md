---
name: traffic-drop-diagnosis
description: "Investigate a meaningful organic decline (e.g., clicks or conversions down 20%) the way a senior SEO manager would (playbook section 7): validate, segment, find contributors, check technical/release/analytics changes, review SERP and competitor shifts, rank hypotheses with evidence and confidence, recommend corrective actions, execute only approved changes, monitor recovery. Use for 'traffic dropped', 'why did clicks fall', 'rankings fell', or when daily-check finds a ≥20% decline."
metadata:
  version: "1.1.0"
---

# Traffic-drop diagnosis (Tier A analysis; fixes are Tier B/C)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md` and `references/operating-model.md` (load first). Work from the SEO workspace folder (the repo root, marked by `_seo-workspace.md`); run tools as `python3 "cowork/elevatedigi-seo-lead/tools/<tool>.py" …`.
Use the specialists: `analytics-agent` (steps 1–3), `technical-seo-agent` (step 4), `competitor-intelligence-agent` (step 5). Write `clients/<slug>/audits/<date>-traffic-drop.md`.

1. **Validate** the decline against the right comparison (same weekdays; previous period and same period
   last year). Account for seasonality (profile.md), weekday mix, tracking changes (GA4 tag, consent), GSC
   data delay. If it's not real or not meaningful, say so and stop.
2. **Segment** by page, query, country, device, brand vs non-brand, search type (web/image/news) and
   search appearance. GSC exports: Pages, Queries, Countries, Devices, Dates.
3. **Contributors:** list the pages and queries that explain ≥ 80% of the loss (clicks lost each).
4. **Technical & release checks:** `daily_watch.py` + `diff_crawls.py` vs the last good crawl; check
   indexing (GSC Pages report), canonicals, redirects, robots, noindex, sitemap, status codes, rendering,
   site releases/plugin updates (ask the founders/developer), analytics changes, Manual actions/Security.
5. **SERP & market:** for the top lost queries, check the current SERP (new AI Overview, local pack,
   competitor, aggregator, video). Note known Google updates in the period (web search, cite source/date).
   Check competitor_watch for competitor launches.
6. **Hypotheses**, ranked:
   | # | Hypothesis | Evidence for | Evidence against | Confidence | What would confirm/disprove it |
7. **Corrective actions** with impact, effort, risk, owner and approval tier → `tasks.csv` (type per action).
8. **Execute only approved changes** (`onpage-change`), and log exactly what changed.
9. **Monitor:** set `verify_by` (+14 and +28 days); on those dates compare affected pages/queries and
   report whether the expected recovery happened; update the hypothesis table.

Output to the founders: 5-line summary (is it real? how big? where? most likely cause + confidence?
what we propose and what needs approval).
