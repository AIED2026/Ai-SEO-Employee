---
name: weekly-check
description: "Weekly SEO review for one or all clients (playbook section 3): crawl + diff + spam scan, performance & anomaly report, keyword opportunities, content plan, technical issue tracker, competitor summary, backlink observations, local review where relevant, and next week's prioritised plan. It answers the senior SEO manager's 7 questions. Use for '/weekly', 'weekly check', 'how are the clients doing', 'run the Monday check', or a scheduled weekly run."
metadata:
  version: "1.1.0"
---

# Weekly review (Tier A; recommends Tier B/C work for approval)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md` and `references/operating-model.md`
(load first). Work from the SEO workspace (the repo root); run tools as
`python3 "cowork/elevatedigi-seo-lead/tools/<tool>.py" …`.

Run for the client named, or for every client in `clients/`, one at a time (strict isolation).

## 1. Observe (per client)
1. Read `profile.md`, `action-plan.md`, open rows of `tasks.csv`, tail of `log.md`.
2. Crawl: `crawl.py <url> --max 500 --out clients/<slug>/crawls/<today>` (ElevateDigi: `--max 300`).
   Diff: `diff_crawls.py clients/<slug>/crawls/<prev> clients/<slug>/crawls/<today>`.
3. Spam scan: new URLs matching casino/betting/pharma/etc. in the crawl or diff → **P0 security alert**.
4. `daily_watch.py . <slug>` (money pages, robots, sitemaps).
5. Performance via `data-pull` (Chrome signed in): GSC last 7 days vs previous 7 and 28-day trend; GA4
   organic sessions and key events. If unavailable, say "not available (no access)" in every section that needs it.

## 2. Diagnose: delegate to the specialists (briefs: client slug, workspace, date ranges, output path)
| Deliverable | Agent | Output file |
|---|---|---|
| Performance & anomaly report | `analytics-agent` | `reports/weekly-<date>-performance.md` |
| Prioritised keyword opportunities (pos 5–20, high-impr/low-CTR) | `keyword-research-agent` | `reports/weekly-<date>-keywords.md` |
| Content production & refresh plan | `content-seo-agent` | `reports/weekly-<date>-content.md` |
| Technical issue tracker (severity, owner) | `technical-seo-agent` | updates `tasks.csv` (type technical) |
| Competitor intelligence summary | `competitor-intelligence-agent` | `reports/weekly-<date>-competitors.md` |
| Backlink / authority observations | `offpage-seo-agent` | `reports/weekly-<date>-links.md` |
| Local review (Mira, ElevateDigi, SIF UAE only) | `local-seo-agent` | `reports/weekly-<date>-local.md` |
Small clients or quiet weeks: do the light version yourself instead of spawning every agent. Note which
sections were skipped and why.

## 3. Decide
Merge findings, dedupe against `tasks.csv`, add new tasks (`tasks.py add …`), `tasks.py rescore`.
Pick **3–5 actions for next week** by score, urgency, dependencies and risk.

## 4. Write `clients/<slug>/reports/weekly-<today>.md`
```
Status: 🟢/🟠/🔴 (one-line reason)
## Answers to the 7 questions
1. Why did traffic/visibility/conversions change? … (Observed/Hypothesis · source · confidence)
2. Which pages and queries explain the largest movement? …
3. Which relevant keywords rank 5–20 with realistic upside? …
4. Which competitors are gaining, on which topics? …
5. Which high-impression pages have weak CTR? …
6. Are we attracting the right audience and qualified enquiries? …
7. Which action creates the greatest business impact next? …
## Performance & anomalies · ## Keyword opportunities · ## Content plan · ## Technical tracker (P0/P1)
## Competitors · ## Backlinks/authority · ## Local (if relevant)
## Next week's plan (task IDs, owner, tier) · ## Needs approval · ## Blockers (who owes what)
```
Then log (`observe`, `diagnose`, `decide` lines) and rebuild the dashboard (`dashboard.py .`).

## 5. Output to the founders (one message for the portfolio)
Table: client · status · top alert · top action · approvals needed. Then the Tier B change tables to approve.
Phone-readable. Never pad; "no meaningful change" is a valid answer.
