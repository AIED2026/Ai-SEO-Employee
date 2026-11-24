---
name: content-brief
description: Create a SERP-informed content brief (and optionally a full draft) for a client page or article, optimised for Google, AI Overviews and LLM citation. Use for "write a brief", "plan a blog", "write an article/page for <client>", "improve this page".
---

# Content brief → draft

Follow `playbooks/content.md`. Steps:

1. Read the client files. Confirm the keyword cluster exists in `keywords.csv` (else run a light `keyword-research`).
2. Cannibalisation check: does an existing page already target it? (search crawl `pages.csv` titles/H1s). If yes, brief an **update** instead.
3. SERP study via web search: page types, top-3 coverage, PAA questions, AI Overview presence, who ranks.
4. Write the brief to `clients/<slug>/content/<slug-of-topic>-brief.md`:
   - Primary + secondary keywords, intent, target URL
   - Title (50–60 chars) ×2 options, meta (140–160) ×2 options
   - Outline: H1, H2/H3 as real questions, each with a 40–60 word answer-first snippet
   - Required client inputs (prices, specs, photos, case studies, expert quote): **list them explicitly**
   - Internal links: 3+ pages that should link in (with anchor), 2+ links out to money pages
   - Schema type(s), CTA, word range
5. If asked for a draft: write it to `clients/<slug>/content/<topic>-draft.md` (or create a WordPress
   **draft** via `tools/wp.py`, Tier A). Mark every claim that needs client confirmation as `[CONFIRM: …]`.
   Never publish (Tier B).
6. Log it.
