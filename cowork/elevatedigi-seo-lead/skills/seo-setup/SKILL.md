---
name: seo-setup
description: "First-run setup and health check for the ElevateDigi SEO Lead in Cowork: choose or create the SEO workspace folder, import the starter client data, check Claude in Chrome sign-ins (Search Console, GA4, Business Profile, Bing Webmaster, each client's WordPress), check that scripts can reach client sites, and set up the Monday scheduled task. Use for '/seo-setup', '/seo-doctor', 'set up the SEO employee', 'health check', 'is everything connected', or when no _seo-workspace.md exists."
metadata:
  version: "1.0.0"
---

# SEO setup & health check

Follow the house rules in `${CLAUDE_PLUGIN_ROOT}/skills/seo-lead/SKILL.md`.

## A. Setup (when no workspace exists)
1. Ask the user to pick or create a folder on this computer for the SEO workspace (recommended:
   `Documents/ElevateDigi SEO`, a folder Google Drive does NOT sync) and grant Cowork access to it.
2. If the user has the starter workspace (`ElevateDigi-SEO-Workspace.zip`, or the GitHub repo
   `AIED2026/Ai-SEO-Employee` downloaded), copy its `clients/` folder into the workspace. Otherwise
   create `clients/` empty and offer `client-onboarding` for each client.
3. Create `_inbox/` and `_seo-workspace.md` with:
   ```
   # SEO workspace
   agency: ElevateDigi (Kolkata)
   timezone: Asia/Kolkata
   clients: sif-india, sif-uae, abhyaass, mira-car-rentals, elevatedigi
   chrome: <which Chrome profile is signed in to the agency Google account>
   weekly_check: Monday 08:45 IST
   approvals_by: <founder name(s)>
   ```
4. Ask the user to set Chrome's download location to `<workspace>/_inbox` (Settings → Downloads →
   Location; "Ask where to save each file" off), so exports land where Cowork can read them.
5. Run the health check (B).
6. Offer to create the scheduled tasks in Cowork (the playbook's operating calendar):
   - **Daily** 09:10 IST, Mon–Sat → `/daily`
   - **Weekly** Monday 08:45 IST → `/weekly`
   - **Monthly** 3rd of the month 10:20 IST → `/report` for each client, then `/dashboard`
   (The computer must be on and the Claude app open at those times.)
7. Build the dashboard: `dashboard.py "<workspace>"` and show the user where `_dashboard.html` is.

## B. Health check (/seo-doctor)
Show a table: item · status ✅/⚠️/❌ · fix (one plain line). Check, in Chrome (read-only; never log in for the user):

| Item | How to check |
|---|---|
| Workspace folder + `_seo-workspace.md` | file exists, writable |
| Chrome connected (Claude in Chrome) | a tab can be opened |
| Search Console | open search.google.com/search-console; list which client properties are visible (domain and URL-prefix) |
| GA4 | open analytics.google.com; list visible properties per client |
| Google Business Profile | business.google.com/locations: Mira, ElevateDigi Kolkata, SIF UAE (if any) |
| Bing Webmaster Tools | bing.com/webmasters: sites listed |
| WordPress admin per client | open `<site>/wp-admin/`: signed in? role (Editor/Admin)? Don't click anything else |
| Graphy admin (Abhyaass) | signed in? |
| Script network access | `cd "<workspace>" && python3 "${CLAUDE_PLUGIN_ROOT}/tools/crawl.py" https://sifintuae.com --max 3 --out _inbox/nettest` |
| Python packages | `python3 -c "import requests, bs4, lxml"` (else `pip install requests beautifulsoup4 lxml`) |

Map what's missing to each client in `clients/<slug>/profile.md` → "Access" line. Finish with the
3 most important fixes and what the employee can already do today.
