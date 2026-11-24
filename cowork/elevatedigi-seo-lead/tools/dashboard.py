#!/usr/bin/env python3
"""SEO Intelligence Dashboard: one self-contained HTML page for the whole portfolio.

Consolidates, per client: status, site health (latest crawl vs previous), daily-watch alerts,
search visibility (latest GSC summary), open tasks by severity, items awaiting approval, top actions
and recent activity. Reads only files in the workspace; writes <workspace>/_dashboard.html.

Usage: python3 dashboard.py <workspace> [--out path.html]
"""
import argparse, csv, datetime, glob, html, json, os, re

H = html.escape


def latest(pattern, n=1):
    files = sorted(glob.glob(pattern))
    return files[-n:] if files else []


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


def client_data(ws, slug):
    c = os.path.join(ws, "clients", slug)
    prof = read(os.path.join(c, "profile.md"))
    name = (re.search(r"^#\s+(.+)$", prof, re.M) or [None, slug])[1]
    url = (re.search(r"\|\s*URL\s*\|\s*(\S+)", prof) or [None, ""])[1]
    d = {"slug": slug, "name": name, "url": url}
    wk = latest(os.path.join(c, "reports", "weekly-*.md"))
    d["status"] = (re.search(r"Status:\s*(.+)", read(wk[0])) or [None, "No weekly check yet"])[1].strip() if wk else "No weekly check yet"
    d["status_date"] = os.path.basename(wk[0])[7:17] if wk else ""
    crawls = sorted(p for p in glob.glob(os.path.join(c, "crawls", "*", "summary.json")))
    d["crawl_date"], d["pages"], d["issues"] = "", 0, []
    if crawls:
        cur = json.load(open(crawls[-1])); prev = json.load(open(crawls[-2])) if len(crawls) > 1 else None
        d["crawl_date"] = os.path.basename(os.path.dirname(crawls[-1])); d["pages"] = cur["meta"].get("crawled", 0)
        for k, v in sorted(cur["issue_counts"].items(), key=lambda kv: -kv[1])[:6]:
            pv = prev["issue_counts"].get(k, 0) if prev else None
            d["issues"].append((k, v, None if pv is None else v - pv))
    wt = latest(os.path.join(c, "watch", "*.md"))
    d["watch_date"] = os.path.basename(wt[0])[:-3] if wt else ""
    d["watch"] = [l[2:] for l in read(wt[0]).splitlines() if l.startswith("- **P0") or l.startswith("- **P1")] if wt else []
    gs = latest(os.path.join(c, "data", "*gsc-summary.md"))
    d["gsc"] = ""
    if gs:
        m = re.search(r"## Queries\s*\n(Totals[^\n]+)", read(gs[0]))
        d["gsc"] = f"{m.group(1)} ({os.path.basename(gs[0])[:10]})" if m else f"see {os.path.basename(gs[0])}"
    tasks = list(csv.DictReader(open(os.path.join(c, "tasks.csv"), encoding="utf-8"))) if os.path.exists(os.path.join(c, "tasks.csv")) else []
    pri = lambda t: t.get("priority") or t.get("severity", "P9")
    opn = [t for t in tasks if t.get("stage") != "close" and t.get("status") not in ("completed", "done", "verified")]
    d["sev"] = {s: sum(1 for t in opn if pri(t) == s) for s in ("P0", "P1", "P2", "P3")}
    d["approvals"] = [t for t in opn if t.get("stage") == "await-approval" or t.get("status") == "awaiting-approval"]
    d["top"] = sorted(opn, key=lambda t: (pri(t), -float(t["score"] or 0)))[:5]
    for t in d["top"]:
        t["_pri"] = pri(t)
    d["done"] = sum(1 for t in tasks if t not in opn)
    d["verified"] = sum(1 for t in tasks if t.get("verification") == "passed")
    ob = read(os.path.join(c, "onboarding.md"))
    d["gate"] = (re.search(r"Gate status:\s*\**([A-Z ]+)", ob) or [None, "unknown"])[1].strip()
    d["integrations"] = [(m[0].strip(), m[1].strip(), m[2].strip()) for m in re.findall(r"^\|\s*([^|]+?)\s*\|\s*(connected|not connected|partial|not applicable|not available)\s*\|\s*([^|]*?)\s*\|", ob, re.M)]
    rep = lambda pat: (os.path.basename(latest(os.path.join(c, pat))[0]) if latest(os.path.join(c, pat)) else "")
    d["cadence"] = {"daily": d["watch_date"] or "never", "weekly": d["status_date"] or "never",
                    "monthly": (re.search(r"(\d{4}-\d{2})", rep("reports/*-report.md")) or [None, "never"])[1]}
    d["log"] = [l for l in read(os.path.join(c, "log.md")).splitlines() if re.match(r"\d{4}-\d{2}-\d{2}", l)][-3:]
    return d


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#16202a;--muted:#5b6875;--line:#e3e7ec;--p0:#c62828;--p1:#e07800;--p2:#2f6fb3;--p3:#6b7785;--ok:#2e7d32;--accent:#0d3b46}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0f1418;--card:#172028;--ink:#e6edf3;--muted:#9aa7b4;--line:#26323d;--accent:#7cc4d3}}
:root[data-theme="dark"]{--bg:#0f1418;--card:#172028;--ink:#e6edf3;--muted:#9aa7b4;--line:#26323d;--accent:#7cc4d3}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1200px;margin:0 auto;padding:24px 16px}h1{font-size:24px;margin:0 0 4px}h2{font-size:18px;margin:0}
.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px;margin-top:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;overflow-wrap:anywhere}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.wrap{overflow-x:auto}.pill{display:inline-block;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:600;color:#fff}
.P0{background:var(--p0)}.P1{background:var(--p1)}.P2{background:var(--p2)}.P3{background:var(--p3)}
ul{margin:6px 0 0;padding-left:18px}li{margin:2px 0}.kpis{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.kpi{border:1px solid var(--line);border-radius:8px;padding:6px 10px;min-width:70px}.kpi b{display:block;font-size:18px}
h3{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:14px 0 4px}a{color:var(--accent)}
"""


def render(ws, cl):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tot = {s: sum(c["sev"][s] for c in cl) for s in ("P0", "P1", "P2", "P3")}
    appr = sum(len(c["approvals"]) for c in cl)
    o = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
         f"<title>SEO Intelligence Dashboard</title><style>{CSS}</style></head><body><main>",
         f"<h1>SEO Intelligence Dashboard</h1><div class='muted'>ElevateDigi portfolio · built {now} from workspace files · numbers carry their own dates</div>",
         "<div class='kpis'>" + "".join(f"<div class='kpi'><span class='pill {s}'>{s}</span><b>{tot[s]}</b><span class='muted'>open</span></div>" for s in tot),
         f"<div class='kpi'><span class='muted'>Awaiting approval</span><b>{appr}</b></div></div>",
         "<div class='card wrap'><table><tr><th>Client</th><th>Status</th><th>Alerts (daily watch)</th><th>Open P0/P1</th><th>Approvals</th><th>Last crawl</th><th>Search Console</th><th>Onboarding gate</th><th>Jobs (daily · weekly · monthly)</th></tr>"]
    for c in cl:
        o.append(f"<tr><td><a href='#{c['slug']}'>{H(c['name'])}</a></td><td>{H(c['status'])}<div class='muted'>{c['status_date']}</div></td>"
                 f"<td>{len(c['watch'])}<div class='muted'>{c['watch_date'] or 'not run'}</div></td><td>{c['sev']['P0']} / {c['sev']['P1']}</td>"
                 f"<td>{len(c['approvals'])}</td><td>{c['crawl_date']} · {c['pages']} pages</td><td>{H(c['gsc']) or '<span class=muted>not connected</span>'}</td><td>{H(c['gate'])}</td><td class='muted'>{c['cadence']['daily']} · {c['cadence']['weekly']} · {c['cadence']['monthly']}</td></tr>")
    o.append("</table></div><div class='grid'>")
    for c in cl:
        o.append(f"<section class='card' id='{c['slug']}'><h2>{H(c['name'])}</h2><div class='muted'>{H(c['url'])}</div>")
        o.append("<h3>Top actions (task queue)</h3><ul>" + ("".join(
            f"<li><span class='pill {H(t['_pri'])}'>{H(t['_pri'])}</span> {H(t['title'])} <span class='muted'>· {H(t['owner'])} · approval {H(t.get('approval', t.get('approval_tier','')))} · {H(t.get('stage') or t.get('status',''))}</span></li>" for t in c["top"]) or "<li class='muted'>No open tasks</li>") + "</ul>")
        if c["watch"]:
            o.append("<h3>Daily watch alerts</h3><ul>" + "".join(f"<li>{H(w)}</li>" for w in c["watch"][:6]) + "</ul>")
        if c["issues"]:
            o.append(f"<h3>Site health (crawl {c['crawl_date']})</h3><table>" + "".join(
                f"<tr><td>{H(k)}</td><td>{v}</td><td class='muted'>{'' if dlt is None else f'{dlt:+d}'}</td></tr>" for k, v, dlt in c["issues"]) + "</table>")
        if c["approvals"]:
            o.append("<h3>Awaiting your approval</h3><ul>" + "".join(f"<li>{H(t['id'])}: {H(t['title'])}</li>" for t in c["approvals"]) + "</ul>")
        if c["integrations"]:
            o.append("<h3>Integrations (status · last data)</h3><table>" + "".join(
                f"<tr><td>{H(n)}</td><td>{'✅' if s == 'connected' else ('➖' if s in ('not applicable',) else '⚠️')} {H(s)}</td><td class='muted'>{H(dt)}</td></tr>" for n, s, dt in c["integrations"]) + "</table>")
        o.append(f"<h3>Recent activity</h3><ul>" + ("".join(f"<li class='muted'>{H(l[:160])}</li>" for l in c["log"]) or "<li class='muted'>none</li>") + f"</ul><div class='muted'>Tasks completed: {c['done']} · verified: {c['verified']}</div></section>")
    o.append("</div></main></body></html>")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workspace"); ap.add_argument("--out")
    a = ap.parse_args()
    slugs = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(a.workspace, "clients", "*", "profile.md")))
    cl = [client_data(a.workspace, s) for s in slugs]
    cl.sort(key=lambda c: (-c["sev"]["P0"], -c["sev"]["P1"]))
    out = a.out or os.path.join(a.workspace, "_dashboard.html")
    open(out, "w", encoding="utf-8").write(render(a.workspace, cl))
    print(f"Dashboard written: {out} ({len(cl)} clients)")


if __name__ == "__main__":
    main()
