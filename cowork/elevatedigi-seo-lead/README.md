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
6. Schedule the operating calendar in Cowork **scheduled tasks** (your computer must be on, Claude app open):
   daily 9:10 AM Mon–Sat `/daily` · Mondays 8:45 AM `/weekly` · 3rd of each month `/report <client>` + `/dashboard`.

## How it's organised (from the founders' Senior SEO Manager Playbook)
- **Loop:** Observe → Diagnose → Decide → Execute → Verify → Learn. SOP and acceptance test: the founders' Master Operating Checklist.
- **Team:** this session is the AI SEO Manager (orchestrator) with 8 specialist subagents: keyword
  research, technical SEO, content SEO, off-page, analytics, AI search, local SEO, competitor intelligence.
- **One task queue per client** (`tasks.csv`) with priority, score, owner, approval, status (Pending/In Progress/Completed/Blocked), workflow stage (Detect → … → Close) and verification; full
  audit log in `log.md`; **SEO Intelligence Dashboard** at `<workspace>/_dashboard.html`.
- Spec and coverage map: `docs/` in the GitHub repo.

## Commands
| Command | What it does |
|---|---|
| `/seo-setup` · `/seo-doctor` | Setup and health check |
| `/daily [client]` | Daily health summary: what changed · why · evidence · action · owner · urgency · status |
| `/weekly [client]` | Weekly review: the 7 weekly deliverables and answers to the 7 senior-SEO questions |
| `/diagnose <client> [what dropped]` | Traffic-drop investigation with ranked hypotheses |
| `/dashboard` · `/tasks [client\|approvals]` | Portfolio dashboard · task queue and approvals |
| `/competitors` · `/backlinks` · `/content-audit` · `/local` `<client>` | Workstream reviews |
| `/audit <client>` | Full SEO/AEO/GEO audit → prioritised action plan |
| `/gsc <client> [range]` | Pull GSC / GA4 / GBP data via Chrome and summarise it |
| `/keywords <client> [focus]` | Keyword map tied to pages |
| `/brief <client> <topic> [draft]` | SERP-based brief (and draft) |
| `/fix <client> <what>` | Change table → **your approval** → applied in wp-admin → verified |
| `/ai-check <client>` | AI-visibility check (mentions/citations vs competitors) |
| `/report <client> [month]` | Monthly review: the 7 monthly deliverables, report drafted for founder review |
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
