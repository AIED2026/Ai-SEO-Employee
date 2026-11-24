# Playbook: Technical SEO

## Triage order (stop and fix at the first failure)
1. **Reachability:** site up, one canonical host (http→https, www↔non-www 301 to one), real 404s.
2. **Renderability:** primary content, title, meta, canonical and links present in the raw HTML.
3. **Indexability:** no accidental `noindex` or `X-Robots-Tag`; canonicals self-referencing on
   indexable pages; robots.txt not blocking what should rank; sitemap lists only indexable 200 URLs.
4. **Duplication:** one URL per intent. Watch for clones of location/country pages, tag/category/author
   archives, pagination, parameters, http/https and trailing-slash variants.
5. **Site architecture:** money pages ≤ 3 clicks from home, each with internal links in; no orphans.
6. **Performance:** LCP < 2.5 s, INP < 200 ms, CLS < 0.1 (field data/CrUX first, lab second). In
   India test on mobile with throttling. Typical WordPress fixes: page cache, image WebP/AVIF +
   width/height, defer JS, drop unused plugins and sliders, font-display swap.
7. **Structured data:** valid JSON-LD matching visible content; one Organization entity site-wide.
8. **International:** hreflang only for real variants (reciprocal, self-referencing, x-default).

## How to run
```bash
python3 tools/crawl.py https://DOMAIN --max 500 --out clients/<slug>/crawls/$(date +%F)
python3 tools/diff_crawls.py clients/<slug>/crawls/<old> clients/<slug>/crawls/<new>
python3 tools/psi.py https://DOMAIN/ https://DOMAIN/money-page/ --strategy mobile
```
The crawler reads raw HTML (like AI crawlers do). If a site needs JS to show content, the crawler
sees 0 words, which is the point: that's what GPTBot sees too. To check what Googlebot renders,
use GSC URL Inspection → "View crawled page".

## Common WordPress problems seen in our portfolio
- Page builders (Breakdance, Elementor) output H1 for every heading widget. Fix in the global
  template, not page by page.
- Duplicated pages keep the original's canonical in the SEO plugin field (SIF India). After
  duplicating any page, clear the canonical field.
- Theme prints the post title as H1 and the content also starts with an H1: 2 H1s per post.
- Spam posts injected via compromised accounts or "guest post" sellers (Mira). Check weekly.
- mod_security/WAF blocking crawlers or our tools. Whitelist Googlebot/Bingbot; don't over-block.

## Severity guide
- **Critical:** site-wide noindex/canonical/rendering faults, hacks, soft-404 site-wide, money pages de-indexed.
- **High:** duplicate money pages, wrong canonicals on a few pages, slow LCP on money pages, broken internal links to money pages.
- **Medium:** missing/duplicate meta, multiple H1s, missing schema, orphan pages.
- **Low:** alt text on decorative images, title length cosmetics.
