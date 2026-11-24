#!/usr/bin/env python3
"""Regenerate the cloud (Claude Code on the web) copy of the SEO Lead from the Cowork plugin.

Single source of truth: cowork/elevatedigi-seo-lead/  (skills, agents, references, tools)
Generated:             .claude/skills/, .claude/agents/  (paths rewritten for the repo layout)

In the repo, the workspace is the repo root, and the plugin root is cowork/elevatedigi-seo-lead.
Run after any change to the plugin:  python3 scripts/sync_cloud.py
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "cowork", "elevatedigi-seo-lead")
PLUGIN_REL = "cowork/elevatedigi-seo-lead"


def rewrite(text):
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", PLUGIN_REL)
    text = text.replace('cd "<workspace>" && ', "")
    text = text.replace('"<workspace>"', ".").replace("<workspace>/", "").replace("`<workspace>`", "the repo root")
    return text


def copy_tree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    for dirpath, _, files in os.walk(src):
        rel = os.path.relpath(dirpath, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            s, d = os.path.join(dirpath, f), os.path.join(dst, rel, f)
            if f.endswith(".md"):
                open(d, "w", encoding="utf-8").write(rewrite(open(s, encoding="utf-8").read()))
            else:
                shutil.copy2(s, d)


def main():
    copy_tree(os.path.join(PLUGIN, "skills"), os.path.join(ROOT, ".claude", "skills"))
    copy_tree(os.path.join(PLUGIN, "agents"), os.path.join(ROOT, ".claude", "agents"))
    for old in ("tools", "playbooks"):  # superseded by the plugin copies
        p = os.path.join(ROOT, old)
        if os.path.isdir(p):
            shutil.rmtree(p)
    n_sk = len(os.listdir(os.path.join(ROOT, ".claude", "skills")))
    n_ag = len(os.listdir(os.path.join(ROOT, ".claude", "agents")))
    print(f"synced {n_sk} skills and {n_ag} agents to .claude/ (tools and references live in {PLUGIN_REL}/)")


if __name__ == "__main__":
    main()
