---
name: daily-check
description: "Daily SEO health summary across all clients (playbook section 2): GSC/GA4 monitoring when Chrome is signed in, money-page/robots/sitemap/spam watch, priority keyword movement, competitor signals and task follow-up, in the format what changed · why it matters · evidence · action · owner · urgency · status. Use for '/daily', 'daily check', 'anything wrong today', or a scheduled daily run."
metadata:
  version: "1.1.0"
---

# Daily check (mostly Tier A; escalate anomalies)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md` and `references/operating-model.md` (load first). Work from the SEO workspace folder (the repo root, marked by `_seo-workspace.md`); run tools as `python3 "cowork/elevatedigi-seo-lead/tools/<tool>.py" …`.
## Steps (each client, one at a time)
1. **Technical watch:** `daily_watch.py . <slug>` (money pages from `money-pages.txt`, robots.txt,
   sitemaps, spam URLs). Its P0/P1 lines are candidate findings.
2. **Performance (if Chrome is available and signed in):** `data-pull` light mode: GSC Performance last 7 days
   vs previous 7 (note the 2–3 day data delay), GA4 organic sessions + key events yesterday vs same weekday
   last week. Flag: site clicks −30% vs 7-day average; money page −20% on ≥100 impressions; key events at 0
   (tracking broken?). Not signed in → say "performance not checked (no access)", don't guess.
3. **Priority keywords:** tracked keywords in `keywords.csv` whose GSC position moved ≥ 3 places, or that
   entered/left the top 10.
4. **Competitor signals (light):** if a competitor snapshot is older than 7 days, skip; otherwise note any
   new competitor URLs from the last `competitor_watch.py` run.
5. **Task follow-up:** open tasks past `due` or `verify_by`; approved tasks not yet applied; blocked items.
6. Distinguish normal volatility from meaningful anomalies. If clicks fell ≥ 20% on a meaningful base,
   start `traffic-drop-diagnosis` (and say so).
7. Add new P0/P1 findings to `tasks.csv` (dedupe first); log `observe`/`alert` lines; rebuild the dashboard.

## Output: the daily health summary (one table for the portfolio)
| Client | What changed | Why it matters | Evidence (source, date range) | Recommended action | Owner | Urgency | Status |
- If nothing meaningful changed for a client: one row "No meaningful change" plus what was checked.
- Keep it phone-readable. P0 items first. Never invent findings to fill the table.
