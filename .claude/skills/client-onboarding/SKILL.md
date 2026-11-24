---
name: client-onboarding
description: Onboard a new SEO client — create the client folder, profile, access checklist, baseline crawl, quick wins and a 90-day plan. Use for "new client", "add client", "onboard <brand>".
---

# Client onboarding

1. Create `clients/<slug>/` with: profile.md, action-plan.md, log.md, keywords.csv, audits/, crawls/, changes/, reports/, content/.
2. Gather (ask the founders in one message; ask only for what's missing):
   - business, products/services, margins (which ones matter), markets/cities, languages
   - goals and how a lead/sale is counted; average deal value
   - top 5 competitors; top 20 customer questions; brand voice; things never to say
   - past SEO work, previous agency, known penalties, migrations
   - access: GSC, GA4, GBP, WordPress Editor + Application Password (see `playbooks/security-and-access.md`)
3. Baseline: run `site-audit`; record GSC/GA4 baselines (last 3 and 12 months) in profile.md.
4. Make sure the network allowlist includes the client domain (ask the founders to approve if blocked).
5. 90-day plan in action-plan.md: Month 1 = fix blockers + quick wins; Month 2 = money-page depth +
   local/entity; Month 3 = content clusters + authority. Each item with KPI and tier.
6. Create `ai-prompts.md` and run a first `ai-visibility-check`.
7. Log it.
