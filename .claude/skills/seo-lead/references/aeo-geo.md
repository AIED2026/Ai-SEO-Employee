# Playbook: AEO & GEO (AI Overviews, ChatGPT, Perplexity, Gemini, Copilot, Claude)

## How AI answers pick sources (working model)
1. **Retrieval:** the engine searches its index (Google's for AI Overviews/Gemini; Bing and its own
   crawlers for ChatGPT/Copilot; its own crawler + partners for Perplexity; Brave and others for Claude).
   If you're not indexed or not readable without JS, you're not a candidate.
2. **Selection:** passages that directly answer the sub-question, with specific facts, from sources
   that look authoritative (entity known, mentioned elsewhere, consistent).
3. **Citation:** engines prefer citing a page whose passage was used. Clear, self-contained passages
   get quoted.

## Checklist per site
- [ ] Content present in raw HTML (`curl -s URL | grep "<h1"`). SPAs need SSR/prerender.
- [ ] robots.txt allows the real AI user agents (template below); no blanket Crawl-delay.
- [ ] Indexed in Google **and** Bing (Bing Webmaster Tools verified, sitemap submitted, IndexNow on).
- [ ] Organization/LocalBusiness schema with name, logo, address, phone, `sameAs`.
- [ ] About page: real people, credentials, address, years in business, certifications.
- [ ] Key pages have answer-first blocks: question as H2, a 40–60 word direct answer, then detail.
- [ ] Specific facts: prices, specs, standards, dates, numbers, named projects.
- [ ] Comparison tables and FAQs built from real queries (GSC, People Also Ask, Reddit/Quora).
- [ ] Consistent brand facts across the site, GBP, directories, LinkedIn (no conflicting phone numbers or addresses).
- [ ] Third-party presence: industry directories, review sites, Reddit/Quora answers, YouTube, press.

## robots.txt template (WordPress)
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /*?s=
Disallow: /*?replytocom

# Search + AI assistants: allowed explicitly
User-agent: Googlebot
User-agent: Bingbot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: Applebot
Allow: /

Sitemap: https://DOMAIN/sitemap_index.xml
```
Notes:
- `Google-Extended` and `Applebot-Extended` are opt-out tokens for model training. They do not affect
  search or AI Overviews. Leave them allowed unless the client objects to training use.
- Don't block CSS/JS. Don't add Crawl-delay (Googlebot ignores it; it only slows other engines).
- Disallow is not noindex: to drop pages from the index, use `noindex` and keep them crawlable.

## AI-visibility test (monthly)
- 15–25 prompts per client, fixed set, stored in `clients/<slug>/ai-prompts.md`:
  - category ("best manhole cover supplier in Dubai")
  - problem ("what load class manhole cover for a highway")
  - comparison ("Zoomcar vs local car rental in Goa")
  - brand ("is Mira Car Rentals Goa reliable")
- Run them through web search (or the engines directly when available); record: mentioned? cited URL?
  which competitors/sources are cited? Track the share over time. Note that results vary by run and location.
- The cited sources list is the off-site target list: get mentioned where the engines already look.

## Writing for extraction
- One idea per paragraph, 2–4 sentences. Put the definition or answer in the first sentence.
- Use the exact question wording as the heading.
- Units and standards spelled out ("EN 124 Class D400 (400 kN test load)").
- Date-stamp time-sensitive facts ("As of November 2026, ICAI's ISA AT has…").
- Cite primary sources (ICAI, municipality, standards bodies) with links.
