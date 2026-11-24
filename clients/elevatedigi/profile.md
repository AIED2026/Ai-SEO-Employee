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
