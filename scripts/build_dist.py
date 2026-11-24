#!/usr/bin/env python3
"""Build install packages into dist/:
  elevatedigi-seo-lead.zip          the Cowork plugin (upload in Cowork → Customize → Plugins)
  ElevateDigi-SEO-Workspace.zip     starter workspace: clients/ memory + _seo-workspace.md + _inbox/
Also re-syncs the cloud copy first.
"""
import os, subprocess, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "cowork", "elevatedigi-seo-lead")
DIST = os.path.join(ROOT, "dist")
SKIP = ("__pycache__", ".pyc", ".DS_Store")


def add_tree(z, src, arc_prefix):
    for dp, _, files in os.walk(src):
        for f in files:
            p = os.path.join(dp, f)
            if any(s in p for s in SKIP):
                continue
            z.write(p, os.path.join(arc_prefix, os.path.relpath(p, src)))


def main():
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "sync_cloud.py")], check=True)
    os.makedirs(DIST, exist_ok=True)
    with zipfile.ZipFile(os.path.join(DIST, "elevatedigi-seo-lead.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        add_tree(z, PLUGIN, "")
    ws = "ElevateDigi SEO"
    with zipfile.ZipFile(os.path.join(DIST, "ElevateDigi-SEO-Workspace.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        add_tree(z, os.path.join(ROOT, "clients"), os.path.join(ws, "clients"))
        z.write(os.path.join(ROOT, "_seo-workspace.md"), os.path.join(ws, "_seo-workspace.md"))
        z.writestr(os.path.join(ws, "_inbox", ".keep"), "")
        if os.path.exists(os.path.join(ROOT, "_dashboard.html")):
            z.write(os.path.join(ROOT, "_dashboard.html"), os.path.join(ws, "_dashboard.html"))
    for f in sorted(os.listdir(DIST)):
        print(f"{f}: {os.path.getsize(os.path.join(DIST, f)) // 1024} KB")


if __name__ == "__main__":
    main()
