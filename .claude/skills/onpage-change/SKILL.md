---
name: onpage-change
description: Prepare, get approval for, apply and verify on-page changes on a client's WordPress site (titles, meta, H1, alt text, internal links, schema, content updates, publishing drafts). Use whenever a change to a live client site is needed.
---

# On-page change (Tier B: approval required)

## 1. Prepare
- Build a change table and save it as `clients/<slug>/changes/<today>-<topic>.md`:
  | # | URL | Element | Current | Proposed | Reason | Expected effect |
- Current values must come from a fresh fetch (crawl or `python3 tools/wp.py get <site> <url>`).
- Batch similar changes (≤ 25 rows per approval) so the founders can approve quickly.

## 2. Ask for approval
Show the table and ask: "Approve all, approve rows …, or edit?" Do nothing until approved.

## 3. Apply
- WordPress content/title/excerpt/media alt: `python3 tools/wp.py update …` (dry-run first, then `--apply`).
  The tool saves a JSON backup of the previous values in `clients/<slug>/changes/backups/`.
- SEO-plugin fields (Yoast/AIOSEO/Rank Math titles & meta) are often not writable via REST. If the
  tool reports that, produce a CSV for the plugin's bulk editor or hand the table to whoever has
  wp-admin. Don't try to log in with admin passwords.
- Template-level issues (multiple H1s from a builder) are Tier C: write instructions for the developer.

## 4. Verify
Re-fetch each URL and confirm the new value is live (cache may need purging). Mark rows ✅/❌ in the change file.

## 5. Log & follow up
Append to `log.md` with a next-check date (14 days). On the check date compare GSC impressions/CTR
for the changed pages (7–14 days after vs before) and note the result.

## Rollback
`python3 tools/wp.py restore <backup.json> --apply` restores the saved values.
