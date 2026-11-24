#!/usr/bin/env python3
"""Competitor watch (free alternative to paid page-tracking): snapshot competitor sitemaps and diff.

Reads  <workspace>/clients/<slug>/competitors.md  → every line starting "- http" under "## Watch list"
Writes <workspace>/clients/<slug>/watch/competitors/<domain>/<YYYY-MM-DD>.json
Prints new URLs, removed URLs and URLs whose <lastmod> changed since the last snapshot.

Usage: python3 competitor_watch.py <workspace> <slug> [--max 5000]
"""
import argparse, datetime, glob, json, os, re
from urllib.parse import urljoin, urlparse
import requests

S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (compatible; SEO-Audit-Bot/1.0)"


def fetch(u):
    try:
        r = S.get(u, timeout=30)
        return r if r.status_code == 200 else None
    except Exception:
        return None


def snapshot(root, cap):
    rb = fetch(urljoin(root, "/robots.txt"))
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", rb.text if rb else "") or [urljoin(root, p) for p in ("/sitemap_index.xml", "/sitemap.xml", "/wp-sitemap.xml")]
    seen, out, q = set(), {}, list(maps)
    while q and len(seen) < 60 and len(out) < cap:
        sm = q.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r = fetch(sm)
        if not r:
            continue
        for block in re.findall(r"<(?:url|sitemap)>(.*?)</(?:url|sitemap)>", r.text, re.S):
            loc = re.search(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)", block)
            if not loc:
                continue
            lm = re.search(r"<lastmod>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)", block)
            u = loc.group(1)
            if u.endswith(".xml") or "sitemap" in u.rsplit("/", 1)[-1]:
                q.append(u)
            else:
                out[u] = lm.group(1)[:10] if lm else ""
    return out, sorted(seen)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workspace"); ap.add_argument("slug"); ap.add_argument("--max", type=int, default=5000)
    a = ap.parse_args()
    cfile = os.path.join(a.workspace, "clients", a.slug, "competitors.md")
    text = open(cfile, encoding="utf-8").read()
    watch = text.split("## Watch list", 1)[1] if "## Watch list" in text else ""
    roots = [re.match(r"-\s*(https?://\S+)", l.strip()).group(1) for l in watch.splitlines() if re.match(r"-\s*https?://", l.strip())]
    if not roots:
        print("No competitors under '## Watch list' in competitors.md"); return
    today = datetime.date.today().isoformat()
    print(f"# Competitor watch: {a.slug}, {today}\n")
    for root in roots:
        dom = urlparse(root).netloc
        d = os.path.join(a.workspace, "clients", a.slug, "watch", "competitors", dom); os.makedirs(d, exist_ok=True)
        urls, maps = snapshot(root, a.max)
        prevs = sorted(f for f in glob.glob(os.path.join(d, "*.json")) if not f.endswith(today + ".json"))
        json.dump({"date": today, "sitemaps": maps, "urls": urls}, open(os.path.join(d, today + ".json"), "w"))
        print(f"## {dom}: {len(urls)} URLs in {len(maps)} sitemap(s)")
        if not urls:
            print("- Sitemap not readable (blocked, missing, or network not allowed). Use web search spot checks instead.\n"); continue
        if not prevs:
            recent = sorted(((lm, u) for u, lm in urls.items() if lm), reverse=True)[:10]
            print("- First snapshot (baseline). Most recently modified:")
            for lm, u in recent:
                print(f"  - {lm} {u}")
            print(); continue
        old = json.load(open(prevs[-1]))["urls"]
        new = sorted(set(urls) - set(old)); gone = sorted(set(old) - set(urls))
        upd = sorted(u for u in set(urls) & set(old) if urls[u] and old[u] and urls[u] != old[u])
        print(f"- vs {os.path.basename(prevs[-1])[:-5]}: +{len(new)} new, −{len(gone)} removed, {len(upd)} updated")
        for label, lst in (("New", new), ("Updated", upd), ("Removed", gone)):
            for u in lst[:15]:
                print(f"  - {label}: {u}")
        print()


if __name__ == "__main__":
    main()
