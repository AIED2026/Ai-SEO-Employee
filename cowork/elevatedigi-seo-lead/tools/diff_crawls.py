#!/usr/bin/env python3
"""Compare two crawl folders from crawl.py and report what changed.

Usage: python3 tools/diff_crawls.py <old_crawl_dir> <new_crawl_dir> [--out file.md]
"""
import argparse, csv, json, os, re

WATCH = ["status", "title", "meta_desc", "canonical", "robots_meta", "x_robots", "h1", "schema"]
SPAM = re.compile(r"casino|betting|bet\d|slot|1xbet|baji|jeet|krikya|viagra|cialis|escort|porn|loan-app", re.I)


def load(d):
    rows = {r["url"]: r for r in csv.DictReader(open(os.path.join(d, "pages.csv"), encoding="utf-8"))}
    summ = json.load(open(os.path.join(d, "summary.json")))
    return rows, summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old"); ap.add_argument("new"); ap.add_argument("--out")
    a = ap.parse_args()
    o, os_ = load(a.old)
    n, ns = load(a.new)
    out = [f"# Crawl diff: {os.path.basename(a.old.rstrip('/'))} → {os.path.basename(a.new.rstrip('/'))}\n"]
    added = sorted(set(n) - set(o)); removed = sorted(set(o) - set(n))
    spam = [u for u in added if SPAM.search(u + n[u].get("title", ""))]
    if spam:
        out.append(f"## 🚨 New spam-like URLs ({len(spam)})\n" + "\n".join(f"- {u}" for u in spam) + "\n")
    out.append(f"## Pages: {len(o)} → {len(n)} (+{len(added)} / −{len(removed)})\n")
    for label, lst in (("New URLs", added), ("Gone URLs", removed)):
        if lst:
            out.append(f"### {label}\n" + "\n".join(f"- {u}" for u in lst[:40]) + ("\n- …" if len(lst) > 40 else "") + "\n")
    changes = []
    for u in sorted(set(o) & set(n)):
        for f in WATCH:
            a1, b1 = (o[u].get(f) or "").strip(), (n[u].get(f) or "").strip()
            if a1 != b1:
                changes.append((f, u, a1[:90], b1[:90]))
    crit = [c for c in changes if c[0] in ("status", "canonical", "robots_meta", "x_robots")]
    if crit:
        out.append(f"## ⚠️ Critical field changes ({len(crit)})\n| field | url | before | after |\n|---|---|---|---|")
        out += [f"| {f} | {u} | {b} | {c} |" for f, u, b, c in crit[:60]]
        out.append("")
    other = [c for c in changes if c not in crit]
    if other:
        out.append(f"## Other changes ({len(other)})\n| field | url | before | after |\n|---|---|---|---|")
        out += [f"| {f} | {u} | {b} | {c} |" for f, u, b, c in other[:80]]
        out.append("")
    oc, nc = os_.get("issue_counts", {}), ns.get("issue_counts", {})
    out.append("## Issue counts\n| issue | before | after | Δ |\n|---|---|---|---|")
    for k in sorted(set(oc) | set(nc), key=lambda k: -(nc.get(k, 0))):
        b, c = oc.get(k, 0), nc.get(k, 0)
        out.append(f"| {k} | {b} | {c} | {c - b:+d} |")
    text = "\n".join(out) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
