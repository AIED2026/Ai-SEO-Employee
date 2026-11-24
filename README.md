# ElevateDigi AI SEO Lead: founder's guide

This folder is your AI SEO employee. Open it in Claude Code (desktop app, web or terminal) and talk
to it like a senior SEO. It reads `CLAUDE.md` (its role and rules) automatically.

## What to say to it

| You say | It does |
|---|---|
| "Run the weekly check" | Crawls all 5 sites, diffs vs last week, scans for spam, gives status + top 3 actions per client |
| "Audit SIF UAE" | Full audit → `clients/sif-uae/audits/` + updated action plan |
| "Keyword research for Mira, focus on airport rentals" | Keyword map tied to pages |
| "Write a brief / draft for 'ISA AT passing marks' for Abhyaass" | SERP-based brief, optional draft (never publishes on its own) |
| "Fix the meta descriptions on SIF India" | Prepares a change table → **waits for your approval** → applies with backups → verifies |
| "AI visibility check for ElevateDigi" | Runs the prompt set, reports mentions/citations and competitors |
| "Monthly report for Mira" | Draft report for you to review (never sent to clients by itself) |
| "Onboard a new client: <name>, <url>" | Creates the folder, asks for what's missing, baseline audit, 90-day plan |

## Autonomy (what it does alone vs asks)
- **Does alone:** crawls, audits, research, briefs, drafts, reports, monitoring.
- **Asks first:** any change on a live client site (titles, meta, schema, redirects, publishing).
- **Only recommends:** structural/dev work, deleting content, anything sent to clients, spending money.

## Setup checklist (one-time)
1. **Rotate passwords** the previous SEO knew; move credentials to a password manager (see `playbooks/security-and-access.md`).
2. **WordPress access per site:** create user `seo-ai` (role **Editor**) → Profile → Application Passwords → create.
   Give it to Claude through the secure credential form (never paste into chat).
3. **Search Console + GA4:** connect via a claude.ai connector, or add the AI's access as a read-only user.
4. **PageSpeed API key** (free): Google Cloud Console → enable PageSpeed Insights API → create API key.
5. **GitHub repo** (private) to store this folder, so it persists between sessions and can run on a schedule.

## Folder map
See section 11 of `CLAUDE.md`.
