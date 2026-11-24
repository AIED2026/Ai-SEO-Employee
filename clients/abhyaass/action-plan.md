# Abhyaass — Action plan (baseline 2026-11-24)

Source: own crawl (10 URLs; the site is small), KW-Progress sheet. No GSC data yet.

## P0 — Domain & canonical (check before anything else)

| # | Issue | Evidence | Fix | Tier | Status |
|---|---|---|---|---|---|
| 1 | **Canonical points to `abhyaass.graphy.com`** on 9 of 10 pages, so Google is told the real page is on Graphy's subdomain, and the custom domain may get no credit | `<link rel=canonical href="https://abhyaass.graphy.com/...">` | In Graphy: set `www.abhyaass.com` as the **primary** custom domain (Graphy settings → custom domain / SEO). If Graphy can't, raise a support ticket; ask them to 301 the graphy subdomain to the custom domain | C | Open |
| 2 | Check which host Google indexes: `site:abhyaass.graphy.com` vs `site:abhyaass.com`, and GSC (add both properties) | — | Verify after GSC access | A | Open |
| 3 | Bare `abhyaass.com` failed TLS/connection in our test | host check | DNS/SSL: point apex to Graphy and redirect to www | C | Verify |
| 4 | Remove the plaintext login stored at the bottom of the KW-Progress sheet and change that password | sheet rows 24–25 | Founders | C | **Urgent** |

## P1 — Content hub (the site has ~1 content page)

Search demand is informational and seasonal. Build an evergreen **ISA/DISA 3.0 hub** on Graphy pages / blog:

| Page | Target queries (seen in tracker) | Format |
|---|---|---|
| ISA AT exam guide: pattern, number of MCQs, passing marks, duration, negative marking | isa at passing marks, how many mcqs for isa at | Answer-first + table + FAQ |
| ISA AT eligibility & registration | isa at eligibility | Steps + official ICAI source links |
| ISA AT exam dates (updated every cycle) | isa at exam date november 2026 | Dated table, update each cycle |
| DISA 3.0 vs DISA 4.0 (if 4.0 exists; verify on ICAI first) | disa 3.0 vs disa 4.0 | Comparison table |
| Module-wise MCQ practice pages (free sample of 10 MCQs per module) | disa 3.0 mcqs, isa 3.0 mcqs, question bank | Quiz/MCQ + CTA |
| Free mock test landing page | isa at online mock test | Lead magnet |
| Fees & plans (transparent) | isa at course fees | Pricing table, Course schema |

All facts must be checked against ICAI's official notifications. Exam rules change; never guess.

## P2 — AEO/GEO & off-site
- Course + FAQPage + Organization schema (if Graphy allows custom code; otherwise via GTM is a weak fallback).
- YouTube: short "How many MCQs in ISA AT / passing marks" explainers. AI engines cite YouTube for exam queries.
- Answer on Quora/Reddit (r/CAIndia) and in CA communities as the founder (disclosed affiliation).
- One H1 per page (home has 9; the DISA guide has 13).

## Measurement
GSC position by query (replace manual page checks), sign-ups/purchases from organic (GA4), monthly AI-visibility prompts ("best DISA 3.0 notes", "ISA AT passing marks").
