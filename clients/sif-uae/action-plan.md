# SIF UAE — Action plan (baseline 2026-11-24)

Source: own crawl, 71 URLs, `crawls/2026-11-24/`. No GSC data yet. The structure is good; the gaps are SEO plumbing and depth.

## P0 — Foundations (one afternoon)

| # | Action | Evidence | Tier | Status |
|---|---|---|---|---|
| 1 | Install an SEO plugin (Rank Math or Yoast) to manage titles, meta, canonicals, schema and sitemaps. Keep one sitemap (drop the duplicate `sitemap.xml` + `wp-sitemap.xml` declaration) | No SEO plugin; two sitemaps in robots | C (plugin install) | Open |
| 2 | Home title "Sif UAE" → e.g. "Manhole Covers & Gratings Supplier UAE – Municipality Approved \| SIF" | 19 titles under 25 chars ("About Us – Sif UAE") | B | Open |
| 3 | Meta descriptions for 37 pages (home included) and shorten 10 that exceed 165 chars | crawl | A → B | Open |
| 4 | robots.txt: replace fake AI bot names, drop crawl-delay | robots.txt | B | Open |

## P1 — Structured data & entity

| # | Action | Tier |
|---|---|---|
| 5 | Organization + LocalBusiness (Sharjah address, phone, geo, opening hours), `sameAs` LinkedIn/GBP | B |
| 6 | Product schema on product pages (material, standard, load class) and FAQPage on blog/approval pages. No JSON-LD on 50 of 61 pages today | B |
| 7 | Google Business Profile for the Hamriyah Free Zone address (if not present), category "Manufacturer"/"Building materials supplier" | C |

## P2 — Depth & differentiation

| # | Action | Why |
|---|---|---|
| 8 | **Make smaller-emirate pages substantive.** Dubai manhole page has ~1,600 words; Ajman has ~210. Each emirate page needs local projects, delivery times from Sharjah, authority approvals and a contact | Avoid thin/doorway signals; serve real searchers |
| 9 | Approval pages: add certificate numbers/images, scope, validity dates, approved product list (text, not image) | Specifiers and LLMs cite verifiable facts |
| 10 | Projects page: case studies with project name, emirate, contractor, products and load class | Trust + long-tail |
| 11 | Arabic versions of the 3 approval pages + home (human translation) with hreflang ar-AE/en-AE | Public-sector buyers |
| 12 | Technical downloads as HTML pages with spec tables (EN 124 class tables) | AEO answers ("what is D400") |
| 13 | Mentions: UAE supplier directories (Yellow Pages UAE, Connect.ae, Dubai Chamber), LinkedIn company posts per project | Off-site entity signals |

## Measurement
GSC queries containing emirate names and "approved"; enquiry form (Fluent Forms) + tel/WhatsApp clicks as GA4 events.
