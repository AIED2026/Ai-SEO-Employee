# Product acceptance checklist: current status

From the founders' Master Operating Checklist §13. Updated 2026-11-24. ✅ pass · ⚠️ partial · ❌ not yet.

| # | Criterion | Status | Evidence / what's left |
|---|---|---|---|
| 1 | Each client has an isolated workspace and knowledge base | ✅ | `clients/<slug>/` (profile, onboarding, tasks, log, keywords, money pages, competitors, prompts, audits, crawls, watch, changes, reports, data); one client per task and per agent brief |
| 2 | Integrations show connection status, data freshness and permission scope | ⚠️ | Shown per client in `onboarding.md` and on the dashboard; all Google integrations still "not connected" until Chrome sign-in in Cowork |
| 3 | Daily, weekly and monthly jobs run on the configured cadence | ⚠️ | Cloud weekly job live (Mondays 08:45 IST). Cowork daily/weekly/monthly scheduled tasks are created by `/seo-setup` on your computer; the dashboard shows last run per job |
| 4 | Every finding includes source, date range, affected URL/query and evidence | ✅ | Evidence standard (operating-model.md); crawler and daily-watch output include URLs and evidence; agent output contract |
| 5 | Anomaly detection accounts for seasonality, data delays and tracking changes | ⚠️ | Rules in daily-check, the 5 daily decision questions and traffic-drop-diagnosis; needs GSC/GA4 data to run on real numbers |
| 6 | Tasks have priority, owner, status, approval and verification fields | ✅ | `tasks.csv` schema (§11 fields + stage) for 66 tasks; `tasks.py check` passes |
| 7 | Risky website changes are blocked until authorised approval is recorded | ✅ | Tier B/C rules; `tasks.py` refuses execute/verify/close while approval=required; onpage-change waits for "approved" |
| 8 | Execution logs and rollback guidance exist for supported changes | ✅ | log.md audit format; change files with Backup column; `wp.py restore` |
| 9 | Reports distinguish observed data from estimates and hypotheses | ✅ | Observed/Hypothesis + confidence labels required in all reports; mandatory rules |
| 10 | Client data cannot be accessed across workspaces without explicit permission | ⚠️ | Enforced by rules (one client per task/agent, separate folders); not a technical permission boundary, because one operator account can read all folders. A SaaS build would need per-client access control |

**To reach ✅ on 2, 3, 5:** complete `/seo-setup` in Cowork with Chrome signed in to GSC, GA4, GBP and Bing, and create the scheduled tasks.
**Item 10** is a known limit of a single-operator setup. Revisit if this becomes a multi-user SaaS.
