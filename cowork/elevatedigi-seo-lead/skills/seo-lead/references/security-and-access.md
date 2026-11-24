# Playbook: Security, access & incident response

## Access model (least privilege)
| System | Access the AI employee should have | How to grant |
|---|---|---|
| WordPress | A dedicated user `seo-ai` with **Editor** role + an **Application Password** (Users → Profile → Application Passwords). Never an admin password | Site admin creates it; the password goes into the cloud environment's secret store, never into chat or files |
| Search Console | Restricted or Full user (read) | GSC → Settings → Users and permissions, or via a connector |
| GA4 | Viewer | GA4 → Admin → Property access management |
| GBP | Manager (only if posting) | Business Profile → People and access |
| Hosting, cPanel, email, domain registrar | **None.** Humans only | — |

## Handover from the previous SEO (do now)
1. Rotate every password they knew (credentials spreadsheet). Start with WordPress admins,
   hosting and email. Enable 2FA on WordPress (Wordfence/Two-Factor plugin) and Google accounts.
2. Remove their WordPress users or downgrade them; check for any unknown users on every site.
3. Remove them from GSC/GA4/GBP if they had personal access.
4. Move the credentials spreadsheet into a password manager (Bitwarden/1Password Teams) and delete the sheet.
5. Delete passwords stored inside working sheets (e.g., the Abhyaass KW-Progress sheet).

## Incident: spam/hacked content
1. Inventory: crawl and list the spam URLs (`crawl.py` + grep for casino/betting/pharma terms).
2. Escalate to founders the same day with the list and the risk.
3. Founders/dev: find the entry point (users, plugins, file changes), rotate credentials, scan, patch.
4. Delete spam (410/404), remove links to it, check GSC Security & Manual Actions, Removals tool.
5. Monitor weekly for recurrence. Log everything in `log.md`.

## Signs to check weekly
New URLs with off-topic terms · new outbound links on old pages · unknown users · sudden indexed
page count spikes in GSC · "This site may be hacked" in the SERP · GSC security emails.

## In Cowork (Claude in Chrome)
Access is the user's own signed-in browser sessions. The employee never sees or types passwords.
- Sign in yourself, in the Chrome that Cowork uses, to: Search Console, GA4, Business Profile, Bing
  Webmaster Tools (agency Google account) and each client's wp-admin. Use an **Editor** WordPress
  account for day-to-day SEO, not an Administrator account, where possible.
- Do **not** stay signed in to client hosting, cPanel, domain registrars or email in that Chrome profile.
  Best: a dedicated Chrome profile "SEO Lead" holding only the accounts above.
- Turn on 2FA everywhere; the browser session carries the trust, not a password.
