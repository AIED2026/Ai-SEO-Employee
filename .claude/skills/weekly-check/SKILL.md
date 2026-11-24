---
name: weekly-check
description: Monday health check for one or all SEO clients — crawl, diff against last crawl, spam scan, GSC movers, then a 5-line status note and top 3 actions per client. Use for "weekly check", "how are the clients doing", "run the Monday check", or a scheduled weekly run.
---

# Weekly check

Run for the client named, or all clients in `clients/` if none is named. One client at a time.

## Steps (per client)
1. Read `profile.md`, `action-plan.md`, and the tail of `log.md`.
2. Crawl:
   `python3 tools/crawl.py <url from profile> --max 500 --out clients/<slug>/crawls/<today>`
3. Diff against the most recent previous crawl folder:
   `python3 tools/diff_crawls.py clients/<slug>/crawls/<prev> clients/<slug>/crawls/<today>`
4. **Spam scan:** `grep -iE "casino|betting|bet[0-9]|slot|1xbet|baji|jeet|krikya|viagra|cialis|loan-app|escort|porn" clients/<slug>/crawls/<today>/pages.csv`.
   Any hit on a URL not seen last week → ALERT (see `playbooks/security-and-access.md`).
5. If GSC is available: last 7 days vs previous 7 days for clicks, impressions, position. List top 5
   gaining/losing pages and queries. Flag money pages that lost > 20% clicks.
6. Check that the P0 items in `action-plan.md` still reproduce; mark fixed ones `Done (verified <date>)`.
7. Write `clients/<slug>/reports/weekly-<today>.md`:
   ```
   Status: 🟢/🟠/🔴 — one-line reason
   Changed since last week: …
   Alerts: … (or none)
   Top 3 actions this week: 1. … 2. … 3. … (with tier A/B/C)
   Blockers: who owes what
   ```
8. Append a line to `log.md`.

## Output to the founders
One combined message: a table of client · status · top alert · top action, then any Tier B approvals
needed (change tables). Keep it scannable on a phone.

## Alert thresholds
New 4xx/5xx on money pages · new noindex or canonical change on any indexable page · indexable page
count ±20% · spam URLs · site unreachable · money-page clicks −30% week over week.
