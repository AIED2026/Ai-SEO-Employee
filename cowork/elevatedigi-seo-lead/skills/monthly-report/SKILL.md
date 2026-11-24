---
name: monthly-report
description: "Monthly SEO review and report for a client (playbook section 4): business-outcome performance report, comprehensive audit with remediation plan, competitor and keyword-gap report, keyword map and content calendar, backlink and authority report, AI search visibility, and next month's roadmap, drafted for founder approval. Use for '/report', 'monthly report', 'month-end review', 'client report'."
metadata:
  version: "1.1.0"
---

# Monthly review & report (Tier A drafts; strategic approval by founders)

House rules: `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md`, `references/operating-model.md` and
`references/reporting.md` (load first). Work from the SEO workspace.

## Data (state exact date ranges everywhere)
Via `data-pull`: GSC last full month vs previous month and vs the same month last year (if 16 months exist);
GA4 organic sessions, key events, conversion rate, AI referrals; GBP performance (local clients); Bing WMT.
CRM qualified leads/revenue only if the founders provide them. Missing data → state it and how to fix it.

## The 7 monthly deliverables (delegate; then merge)
| # | Deliverable | How | File |
|---|---|---|---|
| 1 | Performance report with business outcomes | `analytics-agent` | `reports/<YYYY-MM>-report.md` (main) |
| 2 | Comprehensive audit + prioritised remediation | `site-audit` skill (technical-seo-agent) | `audits/<date>-audit.md` |
| 3 | Competitor & keyword-gap report | `competitor-intel` skill (monthly mode) | `reports/competitors-<YYYY-MM>.md` |
| 4 | Keyword map & content calendar (next 4–6 weeks) | `keyword-research` + `content-audit` | `reports/<YYYY-MM>-content-calendar.md` |
| 5 | Backlink & authority report | `backlink-review` | `reports/backlinks-<YYYY-MM>.md` |
| 6 | AI search visibility observations | `ai-visibility-check` (ai-search-agent) | `reports/ai-visibility-<YYYY-MM>.md` |
| 7 | Next-month growth roadmap | you (orchestrator) | section in the main report |

## Main report structure (`reports/<YYYY-MM>-report.md`)
1. **Summary (3 lines):** what moved, why, what's next.
2. **Business outcomes:** organic conversions, conversion rate, qualified leads/revenue (if CRM), MoM + YoY.
3. **Visibility:** clicks, impressions, CTR, non-brand clicks, top-10 tracked keywords; top gaining/losing pages and queries.
4. **KPI table** vs the baseline and targets in `profile.md`.
5. **Technical health:** P0/P1 resolved **and verified** this month; still open; new.
6. **Content:** published/refreshed pages and their early results.
7. **Authority:** new relevant referring domains, notable mentions.
8. **AI search:** mentioned x/N, cited x/N, change, competitor sources.
9. **Work done** (from `log.md`) with links. **Experiments & outcomes** (update `profile.md`).
10. **Risks & what we need from the client/founders.**
11. **Next-month roadmap:** 3–5 priorities with expected impact, owner, approval needed.

Rules: every number has source and date range; label Observed vs Hypothesis; never promise rankings or traffic.
Mark the file **DRAFT, for founder review**. Never send anything to a client. Log it; rebuild the dashboard.
