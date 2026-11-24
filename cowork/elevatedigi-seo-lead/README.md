# ElevateDigi SEO Lead: Cowork plugin

Your AI Senior SEO Lead (SEO · AEO · GEO) inside Claude Cowork. It works in **your own signed-in
Chrome**, so it can read Search Console, GA4 and Business Profile and edit WordPress, without you
ever sharing a password.

## Install (once per computer)
1. **Claude desktop app → Cowork → Customize → Plugins → Upload** → choose
   `elevatedigi-seo-lead.zip` → confirm.
2. Install **Claude in Chrome** (the Chrome extension), and in Cowork set the preferred browser to that Chrome.
3. **Make a dedicated Chrome profile** "SEO Lead" and sign in there to:
   - the agency Google account (Search Console, GA4, Business Profile)
   - Bing Webmaster Tools
   - each client's **wp-admin** (Editor role is enough) and Graphy admin for Abhyaass
   Don't sign in to email, hosting/cPanel or domain registrars in this profile.
4. Unzip `ElevateDigi-SEO-Workspace.zip` into a folder on your computer (e.g. `Documents/ElevateDigi SEO`,
   not inside a Google Drive synced folder) and **grant Cowork access** to it.
5. In Cowork type **`/seo-setup`**. It finds the workspace, checks every sign-in and tells you what's missing.
6. Schedule the weekly check: in Cowork create a **scheduled task**, every Monday at 8:45 AM, prompt `/weekly`.
   (Your computer must be on and the Claude app open at that time.)

## Commands
| Command | What it does |
|---|---|
| `/seo-setup` · `/seo-doctor` | Setup and health check |
| `/weekly [client]` | Crawl, diff, spam scan, Search Console movers, status + top 3 actions |
| `/audit <client>` | Full SEO/AEO/GEO audit → prioritised action plan |
| `/gsc <client> [range]` | Pull GSC / GA4 / GBP data via Chrome and summarise it |
| `/keywords <client> [focus]` | Keyword map tied to pages |
| `/brief <client> <topic> [draft]` | SERP-based brief (and draft) |
| `/fix <client> <what>` | Change table → **your approval** → applied in wp-admin → verified |
| `/ai-check <client>` | AI-visibility check (mentions/citations vs competitors) |
| `/report <client> [month]` | Monthly report draft for founder review |
| `/new-client <name> <url>` | Onboard a new client |

Plain language works too: "how is Mira doing this week?", "fix SIF India's canonicals".

## What it does alone vs asks
- **Alone:** reads, crawls, exports, researches, drafts, reports.
- **Asks first:** any change to a live site, Business Profile, or Search Console action.
- **Never:** passwords, email, hosting, users/plugins/themes/settings, sending anything to clients, spending money.

## Client memory
`<workspace>/clients/<slug>/`: profile, action plan, log, keywords, AI prompts, audits, crawls,
changes (with backups), data exports, reports. Back it up by syncing the workspace to the GitHub
repo `AIED2026/Ai-SEO-Employee`, or by copying the folder.

## Claude Code (terminal) install, optional
```
/plugin install elevatedigi-seo-lead --marketplace AIED2026/ai-seo-employee
```
