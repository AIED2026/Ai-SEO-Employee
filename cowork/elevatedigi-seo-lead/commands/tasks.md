---
description: "Show the prioritised task queue (all clients or one), or what is awaiting approval"
argument-hint: "[client slug | approvals]"
---
Find the SEO workspace. If the argument is "approvals", run `tasks.py "<workspace>" approvals`; otherwise `tasks.py "<workspace>" list` (add `--client <slug>` if a client is named). Tools are in `${CLAUDE_PLUGIN_ROOT}/tools/`. Show the table, then ask which items to approve, reassign or close. Record approvals in tasks.csv (`tasks.py set <slug> <id> status=approved`) and as an `approval` line in log.md.

Argument: $ARGUMENTS
