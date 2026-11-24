# SIF India — Action plan (baseline 2026-11-24)

Source: own crawl, 175 URLs, `crawls/2026-11-24/`. No GSC data yet.

## P0 — Indexing errors

| # | Issue | Evidence | Fix | Tier | Status |
|---|---|---|---|---|---|
| 1 | **Wrong canonicals de-index product pages.** 9 different product pages canonicalise to `/reticuline-gratings-manufacturers-in-usa/`, telling Google they are duplicates of an unrelated page | tactile-plate-manufacturers-in-usa, fabricated-steel-products-usa, welded-gratings-manufacturers-in-usa, steel-fencing-manufacturers-in-usa/-canada/-india, warning-plates-manufacturers-in-canada, ditch-inlet-manufacturers-in-canada, reticuline-gratings-manufacturers-usa | Set each page's Yoast canonical to itself (likely a page duplicated from a template with the canonical field filled). Then request indexing in GSC | B | Open |
| 2 | Sitemap advertises author, category and slider URLs that robots.txt blocks; `/sample-page/` and `/sliders/*` are indexable | sitemap_index + robots | In Yoast: disable author archives and the `sliders` post type in search, noindex category archives, delete Sample Page (with approval) | B | Open |
| 3 | Duplicate country pages: 18 duplicate titles and 11 duplicate meta descriptions (e.g., two "Trench Grates Manufacturers in USA" pages) | crawl | Decide one URL per product × market, 301 the other, unique title/meta | B/C | Open |
| 4 | 16 internal links still point to `*-north-america` URLs that 301 | crawl | Update menu/internal links to final URLs | B | Open |

## P1 — On-page (high volume, low effort)

| # | Action | Scale | Tier |
|---|---|---|---|
| 5 | Meta descriptions for 106 pages (home has none). Home title "Home - Super Iron Foundry" → e.g. "Ductile & Cast Iron Castings Manufacturer, India – Exporter to 38 Countries" | 106 | A (draft) → B |
| 6 | Heading structure: Breakdance outputs H1 for every product card (16 H1s on the home page; 123 pages with multiple H1s). Change card titles to H2/H3 in the Breakdance global template | 123 pages, one template fix | B (template) |
| 7 | Alt text on 174 pages (all images missing alt; likely builder images), descriptive and product-specific | ~all | B (bulk via wp.py) |
| 8 | Blog titles > 65 chars (13); permalinks contain dates → future posts use `/blog/slug/` | 13 | B |
| 9 | Orphan pages: sustainability, media, about-us, financial-information, etc. have no internal links in | 16 | B |

## P2 — Growth (export demand)

| # | Action | Why |
|---|---|---|
| 10 | Make country pages genuinely local (standards, approvals, ports, lead times, project references per market) or consolidate them. Cloned country pages risk being treated as doorway pages | Quality/scaled-content risk |
| 11 | hreflang only if real language variants exist. Review GTranslate: auto-translated pages should be noindexed, or replaced with human-reviewed translations for priority markets | Thin auto-translated content |
| 12 | Product schema (Product + Offer-less specs), Organization schema with `sameAs` (LinkedIn, BSE/NSE listing, IndiaMART, TradeIndia), FAQ blocks on product pages built from buyer questions | Rich results + AI citations |
| 13 | Spec sheets as HTML (not just PDFs): load class, dimensions, weight, standard and test certificate per product | Specifier queries + LLM citations |
| 14 | Export credibility pages: certifications (ISO, BIS, EN 124 test reports), export countries map with case studies | E-E-A-T for B2B |
| 15 | Link and mention building: industry associations (IIF, EEPC India), US/EU distributor pages, trade fair exhibitor listings, supplier directories (ThomasNet, Europages, Kompass) | Authority in buyer markets |

## Measurement
GSC by country (USA, Canada, UK, UAE, India), RFQ form submissions by country (GA4 event + CRM), impressions for standards-term queries.
