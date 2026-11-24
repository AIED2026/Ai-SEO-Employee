# Playbook → implementation coverage map

Spec: `docs/senior-seo-manager-playbook.md` (founders' "AI SEO Employee: The Senior SEO Manager Operating
Playbook"). Plugin root: `cowork/elevatedigi-seo-lead/` (abbreviated `P/`).

| § | Playbook requirement | Where it lives | Status |
|---|---|---|---|
| 1 | 10 core responsibilities; operate like a Senior SEO Manager, not isolated tasks | `P/skills/seo-lead/SKILL.md`, `references/role-and-judgment.md`, `references/operating-model.md` | ✅ |
| 2 | Daily workstreams (GSC/GA4 monitoring, keyword movement, technical health, content optimisation, competitor signals, execution follow-up) | `daily-check` skill, `tools/daily_watch.py`, `data-pull`, `/daily` | ✅ (GSC/GA4 need Chrome sign-in in Cowork) |
| 2 | Daily deliverable: what changed · why · evidence · action · owner · urgency · status | `daily-check` output table | ✅ |
| 3 | 10 weekly workstreams | `weekly-check` + 8 specialist agents; `competitor-intel`, `backlink-review`, `content-audit`, `local-seo-review`, `keyword-research` | ✅ |
| 3 | 7 weekly deliverables | `weekly-check` → `reports/weekly-<date>*.md`, `tasks.csv` | ✅ |
| 3 | Questions a senior SEO manager asks | `weekly-check` report section "Answers to the 7 questions"; `operating-model.md` | ✅ |
| 4 | 6 monthly workstreams + 7 monthly deliverables | `monthly-report` (orchestrates site-audit, competitor-intel, keyword-research, content-audit, backlink-review, ai-visibility-check) | ✅ |
| 5 | Tools & data sources; verify access; label unavailable metrics | `role-and-judgment.md` §8 tool-status table; `seo-setup` health check | ✅ GSC, GA4, GBP, Bing, Trends, Rich Results via Chrome · ⚠️ PSI key, Keyword Planner · ❌ Ahrefs/Semrush (substituted, labelled) · ➖ Screaming Frog → `crawl.py`, Looker Studio → `dashboard.py` |
| 6 | Orchestrator + 8 specialist agents, shared client knowledge base, single task queue | Main session = orchestrator (`seo-lead`); `P/agents/*.md` (8); `clients/<slug>/` memory; `tasks.csv` + `tools/tasks.py` | ✅ |
| 6 | Operating flow Observe → Diagnose → Decide → Execute → Verify | `operating-model.md`; structure of weekly/daily/diagnosis skills | ✅ |
| 7 | Incident workflow: organic traffic drops 20% (9 steps) | `traffic-drop-diagnosis` skill, `/diagnose` | ✅ |
| 8 | KPIs + measurement principle (baseline, conversion definitions, attribution, window; no promises) | `operating-model.md` KPI table; `profile.md` "KPIs & baseline" per client | ✅ structure · ⏳ baselines after first GSC/GA4 pull |
| 9 | Operating calendar with approval model | `operating-model.md`; Cowork scheduled tasks (daily/weekly/monthly) via `seo-setup`; cloud weekly scheduled task | ✅ |
| 10 | SEO Intelligence Dashboard (MVP) | `tools/dashboard.py` → `_dashboard.html`; `/dashboard` | ✅ |
| 10 | AI SEO Audit (MVP) | `site-audit`, `crawl.py`, `technical-seo-agent` | ✅ |
| 10 | AI Content Strategist (MVP) | `keyword-research`, `content-brief`, `content-audit`, `content-seo-agent` | ✅ |
| 10 | Autonomous SEO Reporting (MVP) | `daily-check`, `weekly-check`, `monthly-report` | ✅ |
| 10 | Competitor Intelligence (Phase 2) | `competitor-intel`, `competitor_watch.py`, agent | ✅ (watch lists to be confirmed per client) |
| 10 | GEO / AI Search Optimisation (Phase 2) | `ai-visibility-check`, `ai-search-agent`, `ai-prompts.md` per client | ✅ |
| 11 | Guardrails: read-only auto; drafts auto; approval for content edits, redirects, canonicals, robots, sitemap rules, templates, site-wide settings; never auto-delete/disavow | Autonomy tiers A/B/C in `role-and-judgment.md` + `seo-lead`; `onpage-change` approval flow | ✅ |
| 11 | Audit log (source, reasoning, recommendation, approval, action, actor, verification) | `log.md` format in `operating-model.md` | ✅ |
| 11 | Client isolation, least privilege | One client per task/agent brief; Chrome rules; `security-and-access.md` | ✅ |
| 11 | Source, timestamp, scope, confidence; facts vs hypotheses | Evidence standard in `operating-model.md`; agent output contract | ✅ |
| 11 | No mass low-value content | `content.md` quality bar | ✅ |
| 11 | Rollback instructions | `onpage-change` backup column; `wp.py restore` | ✅ |
| 12 | Isolated client workspace with 7 memory categories | `clients/<slug>/profile.md` sections + tasks/log/keywords/competitors/money-pages | ✅ structure · ⏳ TBD fields for founders |
| 13 | Definition of a high-quality AI SEO employee | Self-review checklist in `operating-model.md` | ✅ |
| 14 | MVP build sequence | Foundation ✅ · Measurement ⏳ (needs GSC/GA4 sign-in) · Audit & prioritisation ✅ · Content intelligence ✅ · Workflow execution ✅ (approvals in chat + tasks.csv; CMS via wp-admin) · Advanced ✅ | — |
| 15 | Portfolio AI employee; expand autonomy only after permissions, verification, logging, isolation are dependable | Default tiers keep live changes behind approval | ✅ |

## Open items to reach full coverage
1. Sign-ins in the Cowork Chrome profile: GSC, GA4, GBP, Bing WMT, each wp-admin/Graphy → unlocks daily/weekly performance sections and KPI baselines.
2. Founders fill `TBD` fields in each `profile.md` (revenue goals, approvers, implementers, competitor list).
3. Free PageSpeed API key (Core Web Vitals).
4. Optional: Ahrefs or Semrush (both have Claude connectors) for keyword volumes, rank tracking and backlink intelligence.
