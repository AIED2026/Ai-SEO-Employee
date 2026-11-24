---
name: local-seo-review
description: "Local SEO review for clients with a local presence (Mira Car Rentals, ElevateDigi Kolkata, SIF UAE): Google Business Profile performance and completeness, reviews, NAP consistency, local rankings and location-page quality (playbook section 3). Use for '/local', 'GBP review', 'reviews', 'local rankings', or inside weekly reviews for local clients."
metadata:
  version: "1.1.0"
---

# Local SEO review (Tier A; GBP edits, posts and review replies are Tier B)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md` and `references/operating-model.md` (load first). Work from the SEO workspace folder (the repo root, marked by `_seo-workspace.md`); run tools as `python3 "cowork/elevatedigi-seo-lead/tools/<tool>.py" …`.
Delegate to `local-seo-agent`. Follow `references/local-seo-india.md`.
1. **GBP (Chrome, read-only):** categories, services/products, hours, photos (recency), posts (last date),
   Q&A, attributes; Performance last month vs previous: calls, direction requests, website clicks, bookings,
   searches by keyword.
2. **Reviews:** count, average, new this period, unanswered, themes (praise/complaints). Draft replies for
   unanswered reviews (Tier B: approval before posting). Never solicit fake or incentivised reviews.
3. **NAP:** website footer/contact vs GBP vs JustDial/Sulekha/TripAdvisor/Yellow Pages UAE (web search). List mismatches.
4. **Local visibility:** spot-check the money terms + place names (e.g., "car rental Calangute"): is the
   client in the local pack / top 10? Who is? (Non-personalised sample; say so.)
5. **Location pages:** unique local value vs thin/duplicate (crawl data; see Mira duplicates).
6. **Output** `clients/<slug>/reports/local-<date>.md` + `tasks.csv` rows (type local). Log it.
