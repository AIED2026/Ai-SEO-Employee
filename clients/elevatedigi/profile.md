# ElevateDigi (own agency site)

| Field | Value |
|---|---|
| URL | https://www.theelevatedigi.com/ (main app) + https://theelevatedigi.com/blogs/ (WordPress blog) |
| Business | Digital marketing agency, Kolkata. Services: SEO, AEO, performance/Google Ads, social, LinkedIn, YouTube, programmatic, website development |
| Markets | Kolkata (primary), Mumbai, UAE (has location landing pages for each) |
| Goal | Inbound leads for agency services; credibility as an AEO/GEO expert |
| Conversion | Lead form (Google Ads conversion `AW-17450911739` fires on submit), Freshsales CRM, Meta Pixel |
| Stack | Main site: React/Vite single-page app, **client-side rendered**, LiteSpeed server. Blog: WordPress + Yoast on /blogs/ |
| Analytics | GA4 `G-HKJ0CL3HXG`, GSC verified (meta tag present) |
| Access | GSC/GA4 owned by the ElevateDigi Google account. **Not yet connected to the AI employee.** WordPress: needs a dedicated Editor user + Application Password |

## Money pages (intended)
seo-company-kolkata · aeo-services-kolkata · digital-marketing-company-kolkata ·
social-media-marketing-company-kolkata · google-ads-agency-kolkata · performance-marketing-agency-kolkata ·
seo-company-mumbai · social-media-marketing-company-mumbai · digital-marketing-company-uae · services/*

## Competitors (to confirm with founders)
To identify from GSC + SERP for "seo company in kolkata", "digital marketing agency kolkata",
"aeo services india". Ask founders for the 3–5 agencies they lose pitches to.

## Notes
- Every blog post exists twice: `/blog/<slug>` (SPA, empty HTML) and `/blogs/<slug>` (WordPress).
  76 of 76 SPA blog slugs duplicate a WP post.
- Positioning opportunity: the agency sells AEO/GEO, so its own site must be the showcase.

## Conversions & lead qualification
- Primary conversions: Lead form submit (Google Ads conversion + Freshsales CRM). Qualified = business with budget ≥ (TBD) for SEO/ads retainer
- Revenue goals: TBD (ask founders: target leads/month and average deal value)

## Brand voice, editorial rules, compliance
- Voice: ElevateDigi, the agency's own voice: confident, practical, proof-led
- Compliance / prohibited claims: Don't claim guaranteed rankings or 'No. 1 agency'. Client names only with permission
- Brand terms (for brand vs non-brand split in GSC): elevatedigi, elevate digi, the elevate digi

## Seasonality
B2B budgets reset in April; Q4 (Oct–Dec) festive marketing demand

## KPIs & baseline (agree with founders; fill from first GSC/GA4 pull)
| KPI | Baseline (period, source) | Target | Reporting window |
|---|---|---|---|
| Organic clicks (non-brand) | TBD | TBD | monthly |
| Organic conversions | TBD | TBD | monthly |
| Organic conversion rate | TBD | TBD | monthly |
| Top-10 tracked keywords | TBD | TBD | monthly |
| AI visibility (mentioned / cited, of N prompts) | TBD | TBD | monthly |
| P0/P1 technical issues open (verified fixed) | see tasks.csv | 0 P0 | weekly |
Attribution: GA4 default (data-driven), organic channel. Conversion definitions as above.

## Experiments & outcomes
(Record each change test: date, pages, hypothesis, result after 28 days. See changes/ and log.md.)

## Approvals, permissions, owners, escalation
- Approver for Tier B changes: TBD (founder name)
- Implementers: Developer (TBD), Writer (TBD), client contact (TBD)
- Escalation: P0/security → founders same day; client-facing items → founders only
- Access (Cowork, signed-in Chrome): GSC TBD · GA4 TBD · GBP TBD · wp-admin/platform TBD · Bing WMT TBD
