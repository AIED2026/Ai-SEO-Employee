---
name: backlink-review
description: "Backlink and authority review for one client without paid tools (playbook sections 3–4): GSC Links export and Bing Webmaster backlinks via Chrome, new/lost links vs last snapshot, referring-domain relevance, suspicious patterns, digital PR and outreach opportunities. Use for '/backlinks', 'link profile', 'authority report', or inside weekly/monthly reviews."
metadata:
  version: "1.1.0"
---

# Backlink review (Tier A; outreach is Tier B, disavow Tier C)

House rules: `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md` and `references/operating-model.md` (load first). Work from the SEO workspace folder (`<workspace>`, marked by `_seo-workspace.md`); run tools as `cd "<workspace>" && python3 "${CLAUDE_PLUGIN_ROOT}/tools/<tool>.py" …`.
Delegate to `offpage-seo-agent` for full reviews.
1. **Data:** GSC → Links → export (top linking sites, top linked pages, top anchor text) and Bing Webmaster
   Tools → Backlinks (export; it also compares against competitor domains) → save in
   `clients/<slug>/data/<date>-links-gsc.zip` / `-links-bing.csv`. Say clearly that Ahrefs/Semrush data
   is unavailable, so counts are partial.
2. **Compare** with the previous snapshot: new and lost referring domains; changes in linked pages and anchors.
3. **Assess** relevance and credibility of referring domains (industry, geography, editorial vs directory).
   Flag suspicious patterns (sudden spikes, casino/pharma anchors, sitewide footer links, scraped copies).
   **Do not assume every low-quality link is harmful**; Google mostly ignores them. Disavow is Tier C and only
   for manual actions or clear paid-link schemes.
4. **Opportunities:** see `references/link-building.md` by client type; unlinked brand mentions
   (web search "brand" -site:domain); pages competitors earn links to that we could do better.
5. **Output** `clients/<slug>/reports/backlinks-<date>.md`: observations, quality notes, 5–10 outreach
   targets (each needs approval before contact) → `tasks.csv` (type offpage). Log it.
