---
name: monthly-report
description: Draft the monthly SEO report for a client (outcomes, GSC visibility, AI visibility, work done, next month) for founder approval. Use for "monthly report", "client report", "month-end update".
---

# Monthly report

House rules: `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md` (load first). Work from the SEO workspace folder (`<workspace>`, marked by `_seo-workspace.md`).


Follow `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/references/reporting.md`.

1. Data via `data-pull` in Chrome (state exact date ranges): GSC last full month vs previous month and the same month last
   year; GA4 organic sessions and key events (forms, WhatsApp, calls); GBP performance for local
   clients; the latest `ai-visibility` file; work from `log.md` for the month.
2. Write `<workspace>/clients/<slug>/reports/<YYYY-MM>-report.md` with sections: Summary (3 lines) · Outcomes ·
   Visibility · AI visibility · Work done · Issues & what we need from you · Next month.
3. Where data is missing (no GSC access yet), say so plainly in the report and list how to fix it.
   Never fill gaps with estimates presented as data.
4. Optionally build a shareable HTML version (Artifact) if the founders ask.
5. Mark it **DRAFT, for founder review**. Never send it to the client.
