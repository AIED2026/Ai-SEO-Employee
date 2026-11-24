# ElevateDigi AI SEO Lead

An AI Senior SEO Manager (SEO · AEO · GEO) that runs the founders' **Senior SEO Manager Operating
Playbook** (`docs/senior-seo-manager-playbook.md`) for a portfolio of client websites.

## Two ways to run it
| | **Cowork (recommended for daily work)** | **Cloud / Claude Code on the web** |
|---|---|---|
| Install | Upload `dist/elevatedigi-seo-lead.zip` in Cowork → Customize → Plugins; unzip `dist/ElevateDigi-SEO-Workspace.zip` | Start a session with this repo selected |
| Data access | Your signed-in Chrome: Search Console, GA4, Business Profile, Bing, wp-admin | Crawls and public data only (no Chrome) |
| Schedule | Cowork scheduled tasks: daily / weekly / monthly | Weekly cloud check (Mondays 8:45 IST) |
| Guide | `cowork/elevatedigi-seo-lead/README.md` | `CLAUDE.md` |

## Layout
- `cowork/elevatedigi-seo-lead/`: the plugin and **single source of truth** (skills, 8 specialist
  agents, references, tools, commands)
- `.claude/skills`, `.claude/agents`: generated for cloud sessions by `python3 scripts/sync_cloud.py`
- `clients/<slug>/`: client memory (profile, action plan, task queue, audit log, keywords, money pages,
  competitors, AI prompts, audits, crawls, watch snapshots, changes, reports, data)
- `_dashboard.html`: SEO Intelligence Dashboard (`python3 cowork/elevatedigi-seo-lead/tools/dashboard.py .`)
- `docs/`: founders' playbook (spec) and `spec-coverage.md`
- `dist/`: install packages (rebuild with `python3 scripts/build_dist.py`)
