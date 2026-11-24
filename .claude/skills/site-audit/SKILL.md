---
name: site-audit
description: Full SEO/AEO/GEO audit of a client site producing a prioritised, evidence-backed action plan. Use for "audit <client>", quarterly reviews, new clients, or after a major site change or traffic drop.
---

# Site audit

## Inputs
Client slug. Read `profile.md`, `action-plan.md`, `log.md` first.

## Procedure
1. **Crawl** (up to 1000 URLs): `python3 tools/crawl.py <url> --max 1000 --out clients/<slug>/crawls/<today>`
2. **Speed:** `python3 tools/psi.py <home> <2–4 money pages> --strategy mobile`
3. **Index coverage (GSC, if connected):** indexed vs not-indexed reasons, sitemaps status, manual actions, security issues.
4. **Raw-HTML check of 3 money pages:** `curl -sL URL | grep -iE "<title|<h1|canonical|application/ld\+json"`. Is the content in HTML?
5. **robots.txt and AI-crawler access** against `playbooks/aeo-geo.md`.
6. **Duplication:** duplicate titles, clusters of near-identical location/country pages (sample 2–3
   pairs and compare text), canonical targets.
7. **On-page of money pages:** intent match vs the current SERP (web search), title/meta/H1, answer-first blocks, schema, internal links in.
8. **Entity & off-site:** brand SERP, GBP, key directories, NAP consistency, review count/rating vs competitors.
9. **AI visibility:** run `ai-visibility-check` (5–10 prompts if quick).
10. **Content gaps:** competitor pages that rank for the client's money terms and that we lack.

## Output
- `clients/<slug>/audits/<today>-audit.md`: executive summary (5 bullets, plain English), then
  findings grouped Critical/High/Medium/Low, each with evidence (URL + data + source), fix, tier,
  owner, effort, expected impact.
- Update `action-plan.md` (P0/P1/P2) with Impact × Confidence ÷ Effort ordering.
- Log it.

Never pad an audit with generic best practice. Every finding must cite evidence from this site.
