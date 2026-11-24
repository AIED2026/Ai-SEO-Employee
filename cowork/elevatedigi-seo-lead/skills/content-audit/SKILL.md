---
name: content-audit
description: "Content audit for one client (playbook sections 3–4): find declining, outdated, thin, overlapping or underperforming pages and decide keep / refresh / merge / redirect / deprioritise; high-impression low-CTR fixes; internal-link gaps. Use for '/content-audit', 'which pages to refresh', 'content decay', 'cannibalisation', or inside weekly/monthly reviews."
metadata:
  version: "1.1.0"
---

# Content audit (Tier A analysis; changes Tier B, deletions Tier C)

House rules: `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md` and `references/operating-model.md` (load first). Work from the SEO workspace folder (`<workspace>`, marked by `_seo-workspace.md`); run tools as `cd "<workspace>" && python3 "${CLAUDE_PLUGIN_ROOT}/tools/<tool>.py" …`.
Delegate to `content-seo-agent` for full audits.
1. **Inventory:** latest crawl `pages.csv` (URL, title, H1, words, schema, inlinks, canonical, status).
2. **Performance:** GSC Pages export for last 3 months vs the previous 3 (and YoY when available) via `data-pull`.
   Without GSC, say so and audit on crawl data only (lower confidence).
3. **Classify** each indexable page:
   - **Decaying:** clicks down > 30% with stable demand → refresh
   - **Underperforming:** impressions but CTR below the site median at a similar position → title/meta/intent fix
   - **Thin/outdated:** < 300 useful words, old dates/prices, wrong facts → refresh or merge
   - **Overlapping/cannibalising:** several pages for one query/intent (GSC query → multiple pages; similar titles) → merge + 301
   - **No value:** no impressions in 6 months, no links, no business role → deprioritise; noindex or redirect only with approval (Tier C)
   - **Keep:** performing and current
4. **Internal links:** money pages with few internal links in (`internal_links_in`) → propose 3–5 contextual links
   each (source page · anchor · target).
5. **Output** `clients/<slug>/audits/<date>-content-audit.md`: table page · verdict · evidence · action · priority,
   plus a 4-week refresh plan → `tasks.csv` (type content). Log it.
