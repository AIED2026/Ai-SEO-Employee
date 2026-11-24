#!/usr/bin/env python3
"""Single prioritised task queue per client: <workspace>/clients/<slug>/tasks.csv
Fields follow the founders' Master Operating Checklist §11.

  status:       pending | in-progress | completed | blocked
  stage:        detect → investigate → recommend → await-approval → execute → verify → report → close
  approval:     not-required | required | approved | rejected     (tier A → not-required; B/C → required)
  verification: not-checked | passed | failed
  priority:     P0 | P1 | P2 | P3;  score = impact × confidence ÷ effort (risk/urgency override via priority)

Usage:
  tasks.py <ws> list [--client SLUG] [--status pending,in-progress,blocked] [--type T] [--top N]
  tasks.py <ws> approvals                       # stage=await-approval or approval=required & not yet decided
  tasks.py <ws> overdue                         # due or verify_by in the past, not closed
  tasks.py <ws> rescore [--client SLUG]
  tasks.py <ws> add SLUG --type T --title "…" --priority P1 --impact 4 --confidence 4 --effort 2 --owner AI --tier B [--evidence …] [--due …] [--verify-by …] [--depends-on …] [--stage detect]
  tasks.py <ws> set SLUG ID field=value [field=value …]
  tasks.py <ws> check                           # validate; blocks execute/verify/close stages without approval
  tasks.py <ws> migrate                         # upgrade old-format files (severity/status) in place
"""
import argparse, csv, datetime, glob, os, sys

COLS = ["id", "created", "type", "title", "evidence", "priority", "impact", "confidence", "effort", "score", "owner",
        "approval_tier", "approval", "status", "stage", "verification", "due", "depends_on", "verify_by", "result"]
ENUM = {
    "type": {"technical", "content", "keyword", "local", "offpage", "analytics", "ai-search", "competitor", "security", "onboarding"},
    "priority": {"P0", "P1", "P2", "P3"},
    "approval_tier": {"A", "B", "C"},
    "approval": {"not-required", "required", "approved", "rejected"},
    "status": {"pending", "in-progress", "completed", "blocked"},
    "stage": {"detect", "investigate", "recommend", "await-approval", "execute", "verify", "report", "close"},
    "verification": {"not-checked", "passed", "failed"},
}
STAGES = ["detect", "investigate", "recommend", "await-approval", "execute", "verify", "report", "close"]
TODAY = datetime.date.today().isoformat()


def path(ws, slug): return os.path.join(ws, "clients", slug, "tasks.csv")


def load(ws, slug):
    p = path(ws, slug)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


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


def is_open(r): return r.get("stage") != "close" and r.get("status") != "completed"


def order(rows):
    return sorted(rows, key=lambda r: (not is_open(r), r.get("priority", "P9"), -float(r.get("score") or 0)))


def clients(ws, only=None):
    return [only] if only else sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ws, "clients", "*", "profile.md")))


HDR = "| client | id | pri | score | type | title | owner | approval | status | stage | verif. | due |\n|---|---|---|---|---|---|---|---|---|---|---|---|"


def show(rows, slug):
    for r in rows:
        print(f"| {slug} | {r['id']} | {r['priority']} | {r['score']} | {r['type']} | {r['title'][:80]} | {r['owner']} | "
              f"{r['approval']} | {r['status']} | {r['stage']} | {r['verification']} | {r.get('due', '')} |")


def problems(r):
    errs = [f"{k}={r.get(k)!r}" for k, allowed in ENUM.items() if r.get(k) not in allowed]
    if r.get("approval") in ("required", "rejected") and r.get("stage") in ("execute", "verify", "report", "close"):
        errs.append(f"stage {r['stage']} without approval (approval={r['approval']})")
    if r.get("approval_tier") == "A" and r.get("approval") == "required":
        errs.append("tier A should be approval=not-required")
    if r.get("stage") == "close" and r.get("verification") == "not-checked" and r.get("approval_tier") != "A":
        errs.append("closed without verification")
    return errs


def migrate_row(r):
    if "priority" in r and r.get("stage"):
        return r
    old = r.get("status", "open")
    n = dict(r)
    n["priority"] = r.get("severity", r.get("priority", "P2"))
    tier = r.get("approval_tier", "B")
    n["approval"] = "not-required" if tier == "A" else {"approved": "approved", "rejected": "rejected"}.get(old, "required")
    n["status"] = {"open": "pending", "awaiting-approval": "pending", "approved": "pending", "in-progress": "in-progress",
                   "done": "completed", "verified": "completed", "rejected": "completed", "blocked": "blocked"}.get(old, "pending")
    n["stage"] = {"open": "recommend", "awaiting-approval": "await-approval", "approved": "execute", "in-progress": "execute",
                  "done": "verify", "verified": "close", "rejected": "close", "blocked": "recommend"}.get(old, "recommend")
    n["verification"] = "passed" if old == "verified" else "not-checked"
    return n


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workspace"); sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list"); l.add_argument("--client"); l.add_argument("--status"); l.add_argument("--type"); l.add_argument("--top", type=int, default=50)
    for n in ("approvals", "overdue", "check", "migrate"):
        sub.add_parser(n)
    rs = sub.add_parser("rescore"); rs.add_argument("--client")
    ad = sub.add_parser("add"); ad.add_argument("slug")
    for k in ("type", "title", "priority", "impact", "confidence", "effort", "owner", "tier"):
        ad.add_argument("--" + k, required=True)
    for k in ("evidence", "due", "verify-by", "depends-on"):
        ad.add_argument("--" + k, default="")
    ad.add_argument("--stage", default="detect")
    st = sub.add_parser("set"); st.add_argument("slug"); st.add_argument("id"); st.add_argument("pairs", nargs="+")
    a = ap.parse_args(); ws = a.workspace

    if a.cmd == "list":
        print(HDR); sts = set(a.status.split(",")) if a.status else {"pending", "in-progress", "blocked"}
        for c in clients(ws, a.client):
            show([r for r in order(load(ws, c)) if r["status"] in sts and (not a.type or r["type"] == a.type)][: a.top], c)
    elif a.cmd == "approvals":
        print(HDR)
        for c in clients(ws):
            show([r for r in order(load(ws, c)) if is_open(r) and (r["stage"] == "await-approval")], c)
    elif a.cmd == "overdue":
        print(HDR)
        for c in clients(ws):
            show([r for r in order(load(ws, c)) if is_open(r) and ((r.get("due") and r["due"] < TODAY) or (r.get("verify_by") and r["verify_by"] < TODAY))], c)
    elif a.cmd == "rescore":
        for c in clients(ws, a.client):
            rows = load(ws, c)
            for r in rows:
                r["score"] = score(r)
            save(ws, c, order(rows)); print(f"{c}: {len(rows)} tasks rescored")
    elif a.cmd == "add":
        rows = load(ws, a.slug)
        nums = [int(r["id"].rsplit("-", 1)[-1]) for r in rows if r["id"].rsplit("-", 1)[-1].isdigit()]
        prefix = rows[0]["id"].rsplit("-", 1)[0] if rows else a.slug[:3].upper()
        r = {"id": f"{prefix}-{(max(nums) if nums else 0) + 1:03d}", "created": TODAY, "type": a.type, "title": a.title,
             "evidence": a.evidence, "priority": a.priority, "impact": a.impact, "confidence": a.confidence, "effort": a.effort,
             "owner": a.owner, "approval_tier": a.tier, "approval": "not-required" if a.tier == "A" else "required",
             "status": "pending", "stage": a.stage, "verification": "not-checked", "due": a.due,
             "depends_on": a.depends_on, "verify_by": a.verify_by, "result": ""}
        r["score"] = score(r)
        bad = problems(r)
        if bad:
            sys.exit("invalid: " + "; ".join(bad))
        rows.append(r); save(ws, a.slug, order(rows)); print(f"added {r['id']} (score {r['score']})")
    elif a.cmd == "set":
        rows = load(ws, a.slug); hit = [r for r in rows if r["id"] == a.id]
        if not hit:
            sys.exit(f"no task {a.id}")
        new = dict(hit[0])
        for pr in a.pairs:
            k, v = pr.split("=", 1)
            if k not in COLS:
                sys.exit(f"unknown field {k}")
            new[k] = v
        new["score"] = score(new)
        bad = problems(new)
        if bad:
            sys.exit("refused: " + "; ".join(bad) + "  (record approval first: approval=approved)")
        hit[0].update(new); save(ws, a.slug, order(rows)); print(f"updated {a.id}")
    elif a.cmd == "check":
        bad = 0
        for c in clients(ws):
            for r in load(ws, c):
                e = problems(r)
                if e:
                    bad += 1; print(f"{c} {r['id']}: " + "; ".join(e))
        print("OK" if not bad else f"{bad} problem rows")
    elif a.cmd == "migrate":
        for c in clients(ws):
            rows = load(ws, c)
            if rows:
                save(ws, c, order([migrate_row(r) for r in rows])); print(f"{c}: migrated {len(rows)}")


if __name__ == "__main__":
    main()
