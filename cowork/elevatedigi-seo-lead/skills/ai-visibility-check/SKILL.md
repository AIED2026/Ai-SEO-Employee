---
name: ai-visibility-check
description: Measure a client's visibility in AI answers (AI Overviews, ChatGPT, Perplexity, Gemini-style results) using a fixed prompt set; record mentions, citations and competitor sources. Use for "AI visibility", "are we showing in ChatGPT", "GEO check", or the monthly report.
---

# AI visibility check

House rules: `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md` (load first). Work from the SEO workspace folder (`<workspace>`, marked by `_seo-workspace.md`).


1. Load or create `<workspace>/clients/<slug>/ai-prompts.md` (15–25 prompts: category, problem, comparison,
   brand, local). Keep the set stable month to month; add new prompts at the end with a date.
2. For each prompt, run a web search, plus the AI engines directly if tools are available. Record:
   - Is the brand mentioned? Is the site cited/linked? Which URL?
   - Which competitors are named? Which third-party sources are cited (directories, Reddit, YouTube, news)?
   - Does Google show an AI Overview for it (where observable)?
3. Save `<workspace>/clients/<slug>/reports/ai-visibility-<YYYY-MM>.md` with a table and a summary:
   mention rate (x/N), citation rate, change vs last month, top cited third-party domains.
4. Turn findings into actions: missing from a source the engines cite → add it to the off-site
   target list in `action-plan.md`; a competitor is cited for a fact → create a better, specific, citable page.
5. Log it.

Be honest about method limits: AI answers vary by run, location and login state. Report results as a sample.
