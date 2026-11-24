---
name: competitor-intel
description: "Competitor intelligence for one client (playbook sections 2–4): competitor new/updated pages via sitemap snapshots, SERP changes for money queries, keyword and content gaps, AI-answer competitors, using free methods. Use for '/competitors', 'what are competitors doing', 'keyword gap', or inside weekly and monthly reviews."
metadata:
  version: "1.1.0"
---

# Competitor intelligence (Tier A)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md` and `references/operating-model.md` (load first). Work from the SEO workspace folder (the repo root, marked by `_seo-workspace.md`); run tools as `python3 "cowork/elevatedigi-seo-lead/tools/<tool>.py" …`.
1. Maintain `clients/<slug>/competitors.md`: business competitors and **search** competitors (who ranks
   top 3 for the client's 10 money queries, incl. aggregators). Refresh monthly via SERP spot checks
   (web search, India/UAE/US as relevant; note non-personalised sample). Add confirmed domains to "## Watch list".
2. Run `competitor_watch.py . <slug>` → new/updated/removed competitor URLs since last snapshot.
   (Domains must be reachable: in the cloud environment they need allowlisting; in Cowork, sandbox network.)
3. For notable new/updated competitor pages: open them (web fetch/Chrome) and note topic, format, depth,
   schema, offers. Ask "do we need a response?" (often no).
4. Gaps: topics competitors rank for that the client lacks; client GSC queries where competitors outrank;
   AI-answer competitors from the latest `ai-visibility` file.
5. Output `clients/<slug>/reports/competitors-<date>.md`: changes table (competitor · URL · what changed ·
   why it matters · our response or "none") + keyword/content gap list → `tasks.csv` rows (type competitor/content/keyword).
Weekly: summary of notable changes only. Monthly: full competitor & keyword-gap report.
