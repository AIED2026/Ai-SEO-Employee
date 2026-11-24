---
name: onpage-change
description: "Prepare, get approval for, apply and verify on-page changes on a client's site (titles, meta descriptions, H1, alt text, internal links, schema, canonicals, robots.txt, redirects, content updates, publishing approved drafts) through the user's signed-in WordPress admin in Chrome or the WordPress REST tool. Use whenever a live client site needs changing: 'fix the meta', 'update the title', 'apply the changes', 'publish the article'."
metadata:
  version: "1.0.0"
---

# On-page change (Tier B: approval required)

House rules: `cowork/elevatedigi-seo-lead/skills/seo-lead/SKILL.md`.

## 1. Prepare
- Fetch current values fresh (crawl the URL, or open it in Chrome, or
  `python3 "cowork/elevatedigi-seo-lead/tools/wp.py" get <site> <url>`).
- Write `clients/<slug>/changes/<YYYY-MM-DD>-<topic>.md`, a change table:
  | # | URL | Element | Current | Proposed | Reason | Expected effect |
- Max 25 rows per approval, grouped by type.

## 2. Ask for approval
Show the table in chat: "Approve all, approve rows …, or edit?" Wait for explicit approval.

## 3. Apply through wp-admin in Chrome (preferred in Cowork)
For each approved row:
1. Open `<site>/wp-admin/`. If it asks for login, stop and ask the user to sign in.
2. Find the page/post (Pages or Posts → search by title) → Edit.
3. Make only the approved change:
   - **SEO title / meta description / canonical:** the SEO plugin box under the editor
     (Yoast: "Yoast SEO" panel → SEO title, Meta description, Advanced → Canonical URL;
     AIOSEO: "AIOSEO Settings" → Post Title, Meta Description, Advanced → Canonical URL;
     Rank Math: "Edit Snippet"). Sites without an SEO plugin (SIF UAE) → Tier C: recommend installing one.
   - **H1/title/body text:** block editor or page builder (Breakdance/Elementor: edit only the
     approved element, then the builder's Save/Update).
   - **Alt text:** Media → Library → the image → Alternative Text.
4. Before saving, copy the *current* values into the change file's "Backup" column (rollback).
5. Click Update/Save once. Purge the cache if the site has a cache plugin and the change isn't visible.
Never touch: Plugins, Themes, Users, Settings, Tools → Export/Import, anything outside the approved element.

**REST alternative** (if the user has created an Application Password and stored it securely):
`python3 "cowork/elevatedigi-seo-lead/tools/wp.py" update <site> <url> --title "…" --client <slug>` (dry run) → `--apply`.
SEO-plugin fields usually can't be written by REST; use wp-admin for those.

## 4. Verify
Reload the live URL (logged-out check via `curl` or a crawl of the URL): confirm the new value is in the
HTML. Mark each row ✅/❌ in the change file.

## 5. Log and follow up
Append to `log.md` with a next-check date (+14 days). At the check, compare GSC clicks, CTR and position for the
changed pages (`data-pull`) and record the result in the change file.

## Rollback
Re-apply the "Backup" values the same way (also Tier B, but pre-approved if the change caused harm).
