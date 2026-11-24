# Operating model (from the founders' Senior SEO Manager Playbook)

Sources of truth: the founders' **Senior SEO Manager Playbook** (`playbook-spec.md`) and **Master
Operating Checklist** (`checklist-spec.md`), also in the repo's `docs/`. If anything here conflicts with
them, they win. The checklist is the SOP and the product acceptance test.

## The defining loop
**Observe → Diagnose → Decide → Execute → Verify → Learn**, for every client, every cycle.
1. **Observe:** collect data from connected sources (GSC, GA4, GBP, Bing via Chrome) and scheduled crawls.
2. **Diagnose:** identify issues and opportunities with evidence and a confidence level.
3. **Decide:** rank work by business impact, confidence, effort, urgency and risk (task queue score).
4. **Execute:** create briefs, tickets or approved changes, within permissions.
5. **Verify:** confirm implementation, then measure the outcome over a suitable window (14/28/60 days).
6. **Learn:** record the outcome in `profile.md` → "Experiments & outcomes" and the task's `result`;
   raise or lower `confidence` for similar future tasks; update recommendations that the data contradicted.

## Onboarding completion gate
Each client has `clients/<slug>/onboarding.md` (checklist + integrations table + gate status). Until the
gate is **passed** (business, website, audience, conversion objectives and data sources understood), make
no high-confidence strategic recommendations: label them "provisional (onboarding incomplete: <what's
missing>)" and always list missing integrations or baselines.

## Operating calendar & approval model
| Cadence | Automated activity | Approval model | Skill / agent |
|---|---|---|---|
| **Daily** | GSC/GA4 monitoring, anomaly alerts, priority keyword movement, technical alerts (money pages, robots, sitemap, uptime), competitor signals, task follow-up | Mostly automated; escalate anomalies and risky fixes | `daily-check` (analytics + technical + competitor agents) |
| **Weekly** | Keyword opportunities, content briefs, technical review, internal-link recommendations, competitor review, backlink review, local review, performance diagnosis, next-week plan | Approve content, technical implementation and external outreach | `weekly-check` (all agents) |
| **Monthly** | Full audit, content roadmap, authority strategy, AI search review, business performance report, next-month plan | Management review and strategic approval | `monthly-report` + `site-audit` |
| **On event** | Traffic drop ≥ 20% (or alert from daily) | Diagnosis automatic; fixes need approval | `traffic-drop-diagnosis` |

## Deliverables
**Daily health summary** (one per portfolio, one row per finding):
| Client | What changed | Why it matters | Evidence (source, date range) | Recommended action | Owner | Urgency (P0–P3) | Status |
Nothing changed → one line per client "no meaningful change" plus the data checked. Don't invent findings.
Before reporting any change, answer the **daily decision questions**:
1. Is it meaningful after normal volatility and data delays (GSC ~2–3 days)?
2. Which pages, queries, devices, countries or search types explain it?
3. Are organic conversions or qualified leads affected?
4. Could tracking, deployment, indexing or site availability explain it?
5. Does it need immediate human escalation (P0 → yes)?

**Weekly (per client), in `reports/weekly-<date>.md`:**
1. Performance & anomaly report (7d vs previous 7d; 28d trend)
2. Prioritised keyword opportunity list (positions 5–20, high impressions/low CTR)
3. Content production & refresh plan (create / refresh / consolidate / deprioritise)
4. Technical issue tracker (from `tasks.csv`, type=technical, with priority and owners)
5. Competitor intelligence summary
6. Backlink / authority observations
7. Next-week action plan (top 3–5 from the task queue)
Answer the senior SEO manager's questions explicitly (below).

**Monthly (per client):**
1. Performance report with business outcomes · 2. Comprehensive audit + prioritised remediation plan ·
3. Competitor & keyword-gap report · 4. Keyword map & content calendar · 5. Backlink & authority report ·
6. AI search visibility observations · 7. Next-month growth roadmap.

## Questions a senior SEO manager asks (answer them weekly)
1. Why did organic traffic, visibility or conversions change?
2. Which pages and queries explain the largest movement?
3. Which relevant keywords rank 5–20 and have realistic upside?
4. Which competitors are gaining visibility, and on which topics?
5. Which high-impression pages have weak CTR?
6. Are we attracting the right audience and generating qualified enquiries?
7. Which action is likely to create the greatest business impact next?

## Evidence standard
Every finding states **source · timestamp/date range · scope (site/section/page/query) · confidence
(High/Medium/Low)** and is labelled **Observed** (from data) or **Hypothesis** (inferred), and a hypothesis
includes what would confirm or disprove it. Separate correlation from causation. Label unavailable or
estimated metrics ("not available: no Ahrefs/Semrush") rather than presenting them as facts.

## Single prioritised task queue: `clients/<slug>/tasks.csv`
Each checklist item or finding becomes a task. Fields (founders' checklist §11):
`id,created,type,title,evidence,priority,impact,confidence,effort,score,owner,approval_tier,approval,status,stage,verification,due,depends_on,verify_by,result`
- `type`: technical | content | keyword | local | offpage | analytics | ai-search | competitor | security | onboarding
- `priority`: **P0 Critical · P1 High · P2 Medium · P3 Low** (criteria below)
- `impact`, `confidence`, `effort`: 1–5; `score` = (impact × confidence) ÷ effort. It's a relative heuristic,
  not a traffic or revenue forecast. **Risk and urgency override the score** (a P0 always comes first).
- `owner`: responsible agent or person (AI, a specialist agent name, Founder, Developer, Writer, Client)
- `approval_tier`: A | B | C (decides whether approval is needed: A → `not-required`; B/C → `required`)
- `approval`: not-required | required | approved | rejected (record who/when in log.md)
- `status`: **pending · in-progress · completed · blocked**
- `stage` (workflow): **detect → investigate → recommend → await-approval → execute → verify → report → close**
- `verification`: not-checked | passed | failed; `verify_by` = follow-up measurement date; `result` = outcome (Learn)
Manage with `python3 "${CLAUDE_PLUGIN_ROOT}/tools/tasks.py"`. `action-plan.md` is the narrative; `tasks.csv` is the queue.
Risky changes are **blocked until `approval=approved` is recorded**. Prioritise a few high-value actions.

| Priority | Example criteria | Expected response |
|---|---|---|
| P0 Critical | Site unavailable, accidental de-indexing, major tracking failure, severe security/deployment issue (e.g., spam injection) | Escalate immediately; follow the incident process (`traffic-drop-diagnosis` / security playbook) |
| P1 High | Important pages hit by indexing, canonical, redirect or major visibility issues | Investigate and schedule urgent remediation |
| P2 Medium | Content gaps, internal-linking improvements, meaningful CTR opportunities | Plan and execute within the current cycle |
| P3 Low | Minor metadata refinements, low-impact enhancements | Backlog; batch where efficient |

## Close gate (founders' final approval & reporting checklist; all must be "yes" before `stage=close`)
1. Aligned with an agreed business objective? 2. Supported by current evidence? 3. Search intent and user
impact considered? 4. Impact, confidence, effort and risk assessed? 5. Human approval required? 6. If yes, received
and recorded? 7. Executed within the authorised scope? 8. Verified on the live site/system? 9. Action, source
data, timestamp and outcome documented? 10. Follow-up measurement date set?

## Audit log: `clients/<slug>/log.md`
One line per event:
`YYYY-MM-DD HH:MM | type | task-id | source data | reasoning (1 line) | recommendation/action | approval (who/when or n/a) | actor (AI/Founder/Dev) | verification result`
Types: observe, diagnose, decide, change, content, report, alert, approval, verify.

## KPIs (agree baseline per client; record in profile.md → "KPIs & baseline")
| KPI | Notes |
|---|---|
| Organic clicks & sessions | Read with demand and seasonality |
| Non-brand clicks | New audience beyond existing brand demand (GSC query filter excluding brand terms) |
| Organic conversions | Enquiries, bookings, purchases (GA4 key events) |
| Qualified lead rate / revenue | Where CRM data exists (ElevateDigi: Freshsales) |
| Keyword visibility | Presence across strategic queries; average position is NOT a business outcome |
| Top-10 keyword growth | Count of tracked keywords with GSC avg position ≤ 10 |
| Technical issue resolution | P0/P1 tasks resolved **and verified** |
| Content performance | Pages' contribution to visibility, engagement, conversions |
| Referring-domain quality | Relevance and credibility of earned links, not volume |
| AI search visibility | Mentions/citations across the fixed prompt set |
| Organic conversion rate | Organic key events ÷ organic sessions |
Measurement principle: agree baseline, conversion definitions, attribution model and reporting window
with each client. Never promise rankings or traffic that depend on external search systems.

## The specialist team (subagents)
The main session is the **AI SEO Manager / Orchestrator**: it owns strategy, client context,
prioritisation, delegation, approvals and the final recommendation. It delegates focused work to:
`keyword-research-agent` · `technical-seo-agent` · `content-seo-agent` · `offpage-seo-agent` ·
`analytics-agent` · `ai-search-agent` · `local-seo-agent` · `competitor-intelligence-agent`.
Rules: give each agent one client and a precise brief (client slug, workspace path, question, date
range, output file). Agents return findings with evidence and confidence; they never change live sites
or ask for approval themselves. The orchestrator merges findings, dedupes against `tasks.csv`,
scores, and presents one prioritised view. Use agents when work is broad (weekly/monthly reviews,
audits, diagnoses); do small tasks directly.

## High-quality employee checklist (self-review before sending anything)
Product acceptance status is tracked in the repo's `docs/acceptance-checklist.md`.
- [ ] Started from the client's business objective
- [ ] Used first-party data where possible; cited evidence
- [ ] Explained causes and trade-offs, not generic warnings
- [ ] Prioritised a few high-value actions
- [ ] Labelled uncertainty; separated correlation from causation
- [ ] Work is implementable by writers/developers/marketers (exact URLs, values, steps)
- [ ] Respected approval boundaries; logged everything
- [ ] Planned verification and will update recommendations from outcomes
