#!/usr/bin/env python3
"""Single prioritised task queue per client: <workspace>/clients/<slug>/tasks.csv

Usage:
  tasks.py <workspace> list [--client SLUG] [--status open,awaiting-approval] [--type technical] [--top 10]
  tasks.py <workspace> approvals                      # everything awaiting approval, all clients
  tasks.py <workspace> rescore [--client SLUG]        # recompute score = impact × confidence ÷ effort, sort
  tasks.py <workspace> add SLUG --type T --title "…" --severity P1 --impact 4 --confidence 4 --effort 2 \
                           --owner AI --tier B [--evidence "…"] [--due YYYY-MM-DD] [--verify-by YYYY-MM-DD]
  tasks.py <workspace> set SLUG ID field=value [field=value …]
  tasks.py <workspace> check                          # validate all task files
"""
import argparse, csv, datetime, glob, os, sys

COLS = ["id", "created", "type", "title", "evidence", "severity", "impact", "confidence", "effort", "score",
        "owner", "approval_tier", "status", "due", "depends_on", "verify_by", "result"]
TYPES = {"technical", "content", "keyword", "local", "offpage", "analytics", "ai-search", "competitor", "security"}
STATUSES = {"open", "awaiting-approval", "approved", "in-progress", "done", "verified", "rejected", "blocked"}
OPEN = {"open", "awaiting-approval", "approved", "in-progress", "blocked"}


def path(ws, slug): return os.path.join(ws, "clients", slug, "tasks.csv")


def load(ws, slug):
    p = path(ws, slug)
    if not os.path.exists(p):
        return []
    return list(csv.DictReader(open(p, encoding="utf-8")))


def save(ws, slug, rows):
    with open(path(ws, slug), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})


def score(r):
    try:
        return round(float(r["impact"]) * float(r["confidence"]) / max(float(r["effort"]), 1), 1)
    except (ValueError, KeyError, TypeError):
        return 0.0


def order(rows):
    return sorted(rows, key=lambda r: (r.get("status") not in OPEN, r.get("severity", "P9"), -float(r.get("score") or 0)))


def clients(ws, only=None):
    return [only] if only else sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ws, "clients", "*", "profile.md")))


def show(rows, slug):
    for r in rows:
        print(f"| {slug} | {r['id']} | {r['severity']} | {r['score']} | {r['type']} | {r['title'][:80]} | {r['owner']} | {r['approval_tier']} | {r['status']} | {r.get('due','')} |")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workspace"); sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list"); l.add_argument("--client"); l.add_argument("--status"); l.add_argument("--type"); l.add_argument("--top", type=int, default=50)
    sub.add_parser("approvals"); sub.add_parser("check")
    rs = sub.add_parser("rescore"); rs.add_argument("--client")
    ad = sub.add_parser("add"); ad.add_argument("slug")
    for k in ("type", "title", "severity", "impact", "confidence", "effort", "owner", "tier"):
        ad.add_argument("--" + k, required=True)
    for k in ("evidence", "due", "verify-by", "depends-on"):
        ad.add_argument("--" + k, default="")
    st = sub.add_parser("set"); st.add_argument("slug"); st.add_argument("id"); st.add_argument("pairs", nargs="+")
    a = ap.parse_args(); ws = a.workspace
    hdr = "| client | id | sev | score | type | title | owner | tier | status | due |\n|---|---|---|---|---|---|---|---|---|---|"
    if a.cmd == "list":
        print(hdr)
        sts = set(a.status.split(",")) if a.status else OPEN
        for c in clients(ws, a.client):
            rows = [r for r in order(load(ws, c)) if r["status"] in sts and (not a.type or r["type"] == a.type)]
            show(rows[: a.top], c)
    elif a.cmd == "approvals":
        print(hdr)
        for c in clients(ws):
            show([r for r in order(load(ws, c)) if r["status"] == "awaiting-approval"], c)
    elif a.cmd == "rescore":
        for c in clients(ws, a.client):
            rows = load(ws, c)
            for r in rows:
                r["score"] = score(r)
            save(ws, c, order(rows)); print(f"{c}: {len(rows)} tasks rescored")
    elif a.cmd == "add":
        rows = load(ws, a.slug)
        n = max([int(r["id"].split("-")[-1]) for r in rows if r["id"].split("-")[-1].isdigit()] or [0]) + 1
        r = {"id": f"{a.slug[:4].upper()}-{n:03d}", "created": datetime.date.today().isoformat(), "type": a.type, "title": a.title,
             "evidence": a.evidence, "severity": a.severity, "impact": a.impact, "confidence": a.confidence, "effort": a.effort,
             "owner": a.owner, "approval_tier": a.tier, "status": "open", "due": a.due, "depends_on": a.depends_on,
             "verify_by": a.verify_by, "result": ""}
        r["score"] = score(r); rows.append(r); save(ws, a.slug, order(rows)); print(f"added {r['id']} (score {r['score']})")
    elif a.cmd == "set":
        rows = load(ws, a.slug)
        hit = [r for r in rows if r["id"] == a.id]
        if not hit:
            sys.exit(f"no task {a.id}")
        for pr in a.pairs:
            k, v = pr.split("=", 1)
            if k not in COLS:
                sys.exit(f"unknown field {k}")
            if k == "status" and v not in STATUSES:
                sys.exit(f"status must be one of {sorted(STATUSES)}")
            hit[0][k] = v
        hit[0]["score"] = score(hit[0]); save(ws, a.slug, order(rows)); print(f"updated {a.id}")
    elif a.cmd == "check":
        bad = 0
        for c in clients(ws):
            for r in load(ws, c):
                errs = [e for e, ok in (("type", r["type"] in TYPES), ("status", r["status"] in STATUSES),
                                        ("severity", r["severity"] in {"P0", "P1", "P2", "P3"}), ("tier", r["approval_tier"] in {"A", "B", "C"})) if not ok]
                if errs:
                    bad += 1; print(f"{c} {r['id']}: invalid {', '.join(errs)}")
        print("OK" if not bad else f"{bad} invalid rows")


if __name__ == "__main__":
    main()
