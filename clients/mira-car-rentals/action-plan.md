# Mira Car Rentals — Action plan (baseline 2026-11-24)

Source: own crawl, 118 URLs, `crawls/2026-11-24/`. No GSC data yet.

## 🚨 P0 — SECURITY INCIDENT: gambling spam on the site

**40 gambling/casino spam posts were found on the domain** (Bangladeshi betting apps: Krikya, JW8,
MCW, Nagad88, Jeetbuzz, CV666, 1xBet, Crickex; plus German and Finnish casino posts). Five of them are linked from
~70 pages (a sitewide widget/menu or "recent posts" block). They are indexable, not in the XML
sitemap, and the post sitemap was modified on 2026-11-21, so the activity is recent.

Likely causes: (a) the site has been hacked, or (b) someone with WordPress access is publishing paid
gambling posts (common "guest post" selling). Either way this is a **Google spam-policy risk (site reputation
abuse / hacked content)** that can lead to a manual action and lost rankings for the whole site.

| # | Step | Tier | Status |
|---|---|---|---|
| 1 | In wp-admin → Posts: filter by author/date; identify who published them and when. Check Users for unknown admins; check recently installed plugins/themes | C (founders) | **Urgent** |
| 2 | Rotate ALL passwords for this site (WP users, hosting, FTP, database); enable 2FA; remove unknown users | C | **Urgent** |
| 3 | Scan for malware/backdoors (Wordfence or hosting malware scan); update core/plugins | C | **Urgent** |
| 4 | Delete the spam posts (list in `crawls/2026-11-24/pages.csv`; filter by betting/casino terms). Let them return 410/404. Do NOT redirect them to money pages | C (approval) | Open |
| 5 | Remove the widget/menu linking to them | B | Open |
| 6 | GSC: check Security & Manual Actions; use Removals for the spam URLs; inspect the home page | A (once access) | Open |
| 7 | Add a weekly spam-scan check (the `weekly-check` skill does this) | A | Done (in skill) |

## P1 — Technical clean-up

| # | Issue | Evidence | Fix | Tier |
|---|---|---|---|---|
| 8 | Duplicate location pages: `/car-rental-in-candolim/` vs `/self-drive-car-rentals-in-candolim-goa/` vs `/car-rental-in-candolim-beach` (and Baga, Calangute variants); 7 duplicate title groups; `self-drive-car-rentals-in-calangute-goa` canonicalises to the **Candolim** page | crawl | One page per place; 301 duplicates; fix canonical | B/C |
| 9 | Internal links use `http://` and malformed relative URLs (`/miracarrentalsgoa.com/car-rental-in-baga/`) | crawl | Fix hrefs to absolute https | B |
| 10 | Slow responses: 11 pages took 3–14 s to return HTML (blog, faq, fort-aguada) | crawl timings | Page caching (LiteSpeed/WP Rocket/hosting cache), image compression; re-test with `tools/psi.py` | C |
| 11 | Titles > 65 chars on 66 pages; 57 missing and 22 over-long meta descriptions | crawl | Rewrite with the place name first and a price/benefit hook | A → B |
| 12 | Multiple H1s on 49 pages (theme + content) | crawl | Theme fix | B |
| 13 | Homepage H2s are keyword-stuffed ("Car Rental in Goa", "Best car rentals in Goa", "Hire car in Goa"…) | home | Rewrite H2s to help users (fleet, prices, pickup points, documents needed) | B |

## P2 — Local growth (season is NOW: Dec–Jan peak)

| # | Action | Why |
|---|---|---|
| 14 | **Google Business Profile**: categories (Car rental agency + Taxi service), service areas, real fleet photos, weekly posts, Q&A, review requests after every trip via WhatsApp link | The local pack drives most bookings |
| 15 | Transparent price table (per car type, per day, season) on home and location pages | Top query modifier is "price"; AI answers cite prices |
| 16 | Location pages with unique value: pickup point, distance and time from airport (GOI/Mopa), parking tips, nearby attractions | Remove the thin/spun feel |
| 17 | Separate pages for **Mopa (GOX) airport** and **Dabolim (GOI) airport** car rental | Distinct high-intent queries |
| 18 | Citations: JustDial, Sulekha, TripAdvisor, IndiaMART-style local listings with identical NAP | Local + AI mentions |
| 19 | Documents-required / deposit / fuel policy FAQ (answer-first) | AEO + conversion |

## Measurement
GBP calls, direction requests and website clicks; GA4 WhatsApp and tel click events; GSC clicks for "car rental in <place>" queries.
