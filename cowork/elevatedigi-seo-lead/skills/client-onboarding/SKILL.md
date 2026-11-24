---
name: client-onboarding
description: Onboard a new SEO client — create the client folder, profile, access checklist, baseline crawl, quick wins and a 90-day plan. Use for "new client", "add client", "onboard <brand>".
---

# Client onboarding

House rules: `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md` (load first). Work from the SEO workspace folder (`<workspace>`, marked by `_seo-workspace.md`).


1. Create `<workspace>/clients/<slug>/` with: profile.md (all section-12 fields: business model, services, audience, locations/markets; conversions + lead qualification + revenue goals; site structure, CMS, analytics properties, connected accounts; brand voice, editorial rules, compliance, prohibited claims; target keywords, priority pages, competitors, seasonality; KPIs & baseline; experiments & outcomes; approval contacts, permissions, owners, escalation), action-plan.md, tasks.csv (header from `references/operating-model.md`), log.md, keywords.csv, money-pages.txt (home first, then 4–8 money pages), competitors.md (with "## Watch list"), ai-prompts.md, and folders audits/, crawls/, watch/, changes/, reports/, content/, data/.
2. Gather (ask the founders in one message; ask only for what's missing):
   - business, products/services, margins (which ones matter), markets/cities, languages
   - goals and how a lead/sale is counted; average deal value
   - top 5 competitors; top 20 customer questions; brand voice; things never to say
   - past SEO work, previous agency, known penalties, migrations
   - access: ask the user to sign in, in the Chrome that Cowork uses, to GSC, GA4, GBP and the client's wp-admin (Editor role is enough); then run the `seo-setup` health check (see `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/references/security-and-access.md`)
3. Baseline: run `site-audit`; record GSC/GA4 baselines (last 3 and 12 months) in profile.md.
4. Make sure the network allowlist includes the client domain (ask the founders to approve if blocked).
5. 90-day plan in action-plan.md: Month 1 = fix blockers + quick wins; Month 2 = money-page depth +
   local/entity; Month 3 = content clusters + authority. Each item with KPI and tier.
6. Create `ai-prompts.md` and run a first `ai-visibility-check`.
7. Log it.
