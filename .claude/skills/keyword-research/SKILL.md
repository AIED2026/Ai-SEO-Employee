---
name: keyword-research
description: Keyword and intent research for a client without paid tools — GSC mining, autocomplete/PAA, competitor pages, SERP intent — producing a prioritised keyword map tied to pages. Use for "keyword research", "what should we target", "find opportunities", or before planning content.
---

# Keyword research (₹0 tools)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md` (load first). Work from the SEO workspace folder (the repo root, marked by `_seo-workspace.md`).


## Sources, in order of value
1. **GSC** (via `data-pull`, last 3 months, Queries + Pages export): queries with impressions in the last 3 months. Gold: position 5–20, high
   impressions, low CTR. Also queries landing on the wrong page (cannibalisation).
2. **Client knowledge:** ask for their top 20 customer questions, what customers call the product,
   and which products and regions carry the best margins.
3. **Web search:** autocomplete variations (seed + a–z, "near me", "price", "best", "vs", "for",
   Hinglish "kaise", "kitna"), People Also Ask, related searches. Run searches for the client's market.
4. **Competitor pages** ranking top 5: their H2s show the sub-topics searchers expect.
5. **Google Trends** for seasonality (India/UAE/US as relevant).
6. **Google Keyword Planner** (free with an Ads account) for volume ranges, if the founders give access.

## Classify each keyword
intent (informational / commercial / transactional / navigational / local) · funnel stage ·
business value (1–5, ask the founders if unsure) · difficulty proxy (who ranks: aggregators/govt/big brands = hard) ·
target URL (existing or new) · SERP features (AI Overview, local pack, video, PAA).

## Output
- Update `clients/<slug>/keywords.csv` (keyword, intent, target_page, notes).
- `clients/<slug>/audits/<today>-keyword-map.md`: clusters (one page per cluster), with each cluster's
  primary keyword, secondaries, target URL, action (create/improve/merge), priority.
- Never report search volumes you didn't get from a real source. Use "volume unknown" otherwise.
