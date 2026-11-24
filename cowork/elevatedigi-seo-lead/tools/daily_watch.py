#!/usr/bin/env python3
"""Daily technical watch for one client: money pages, robots.txt, sitemaps, spam URLs.

Reads  <workspace>/clients/<slug>/money-pages.txt   (one URL per line; first line = home page)
Writes <workspace>/clients/<slug>/watch/<YYYY-MM-DD>.json   snapshot
Prints a markdown list of changes vs the previous snapshot, with urgency (P0–P3).

Usage: python3 daily_watch.py <workspace> <slug>
"""
import datetime, glob, hashlib, json, os, re, sys, time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; SEO-Audit-Bot/1.0; +agency daily watch)"
SPAM = re.compile(r"casino|betting|bet\d|slot|1xbet|baji|jeet|krikya|viagra|cialis|escort|porn|loan-app|nagad|crickex", re.I)
S = requests.Session(); S.headers["User-Agent"] = UA


def get(url, timeout=30):
    t = time.time()
    try:
        r = S.get(url, timeout=timeout, allow_redirects=True)
        return r, round(time.time() - t, 2), None
    except Exception as e:
        return None, round(time.time() - t, 2), str(e)[:160]


def page(url):
    r, secs, err = get(url)
    if r is None:
        return {"status": "ERR", "error": err, "secs": secs}
    d = {"status": r.status_code, "final_url": r.url, "secs": secs, "x_robots": r.headers.get("x-robots-tag", "")}
    if "html" in r.headers.get("content-type", ""):
        s = BeautifulSoup(r.text, "lxml")
        rb = s.find("meta", attrs={"name": re.compile("^robots$", re.I)})
        can = s.find("link", rel=lambda v: v and "canonical" in v)
        body = s.body.get_text(" ", strip=True) if s.body else ""
        d.update({
            "title": s.title.get_text(" ", strip=True) if s.title else "",
            "robots_meta": rb.get("content", "") if rb else "",
            "canonical": can.get("href", "") if can else "",
            "h1_count": len(s.find_all("h1")),
            "words": len(body.split()),
            "text_hash": hashlib.md5(body.encode()).hexdigest()[:12],
        })
    return d


def sitemap_urls(root, robots):
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots or "") or [urljoin(root, "/sitemap.xml")]
    seen, urls, q = set(), [], list(maps)
    while q and len(seen) < 40:
        sm = q.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r, _, _ = get(sm)
        if r is None or r.status_code != 200:
            continue
        for l in re.findall(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)", r.text):
            (q if l.endswith(".xml") else urls).append(l)
    return sorted(set(urls)), sorted(seen)


def main():
    ws, slug = sys.argv[1], sys.argv[2]
    cdir = os.path.join(ws, "clients", slug)
    mp = os.path.join(cdir, "money-pages.txt")
    pages = [l.strip() for l in open(mp, encoding="utf-8") if l.strip().startswith("http")]
    root = f"{urlparse(pages[0]).scheme}://{urlparse(pages[0]).netloc}/"
    rr, _, _ = get(urljoin(root, "/robots.txt"))
    robots = rr.text if rr is not None and rr.status_code == 200 else ""
    sm_urls, sm_files = sitemap_urls(root, robots)
    snap = {
        "date": datetime.date.today().isoformat(), "root": root,
        "robots_hash": hashlib.md5(robots.encode()).hexdigest()[:12], "robots_disallow_all": bool(re.search(r"(?im)^disallow:\s*/\s*$", robots)),
        "sitemaps": sm_files, "sitemap_count": len(sm_urls),
        "spam_urls": [u for u in sm_urls if SPAM.search(u)],
        "sitemap_sample": sm_urls[:3000],
        "pages": {u: page(u) for u in pages},
    }
    wdir = os.path.join(cdir, "watch"); os.makedirs(wdir, exist_ok=True)
    prev_files = sorted(f for f in glob.glob(os.path.join(wdir, "*.json")) if not f.endswith(snap["date"] + ".json"))
    json.dump(snap, open(os.path.join(wdir, snap["date"] + ".json"), "w"), indent=1)
    prev = json.load(open(prev_files[-1])) if prev_files else None

    ch = []  # (urgency, what, evidence)
    for u, p in snap["pages"].items():
        if p["status"] != 200:
            ch.append(("P0", f"Money page not 200: {u}", f"status {p['status']} {p.get('error','')}"))
        if "noindex" in (p.get("robots_meta", "") + p.get("x_robots", "")).lower():
            ch.append(("P0", f"Money page is noindex: {u}", p.get("robots_meta") or p.get("x_robots")))
        if p.get("canonical") and p["canonical"].rstrip("/") != p.get("final_url", u).rstrip("/"):
            ch.append(("P1", f"Money page canonicalised elsewhere: {u}", f"canonical → {p['canonical']}"))
        if p.get("secs", 0) > 5:
            ch.append(("P2", f"Slow response: {u}", f"{p['secs']} s for HTML"))
    if snap["robots_disallow_all"]:
        ch.append(("P0", "robots.txt disallows the whole site", "Disallow: /"))
    if snap["spam_urls"]:
        ch.append(("P0", f"{len(snap['spam_urls'])} spam-like URLs in sitemap", "; ".join(snap["spam_urls"][:5])))
    if prev:
        if prev["robots_hash"] != snap["robots_hash"]:
            ch.append(("P1", "robots.txt changed", f"hash {prev['robots_hash']} → {snap['robots_hash']}"))
        if prev["sitemap_count"] and abs(snap["sitemap_count"] - prev["sitemap_count"]) / max(prev["sitemap_count"], 1) > 0.2:
            ch.append(("P1", "Sitemap URL count changed > 20%", f"{prev['sitemap_count']} → {snap['sitemap_count']}"))
        new_urls = sorted(set(snap["sitemap_sample"]) - set(prev.get("sitemap_sample", [])))
        if new_urls:
            ch.append(("P3", f"{len(new_urls)} new URLs in sitemap", "; ".join(new_urls[:5])))
        for u, p in snap["pages"].items():
            q = prev["pages"].get(u)
            if not q:
                continue
            for f, urg in (("title", "P2"), ("canonical", "P1"), ("robots_meta", "P0"), ("h1_count", "P3")):
                if str(q.get(f, "")) != str(p.get(f, "")):
                    ch.append((urg, f"{f} changed on {u}", f"{q.get(f, '')!r} → {p.get(f, '')!r}"))
            if q.get("words") and p.get("words") is not None and p["words"] < 0.6 * q["words"]:
                ch.append(("P1", f"Content shrank > 40% on {u}", f"{q['words']} → {p['words']} words"))
            elif q.get("text_hash") != p.get("text_hash"):
                ch.append(("P3", f"Content edited on {u}", "text hash changed"))
    ch.sort(key=lambda x: x[0])
    out = [f"## {slug}: daily watch {snap['date']} (vs {os.path.basename(prev_files[-1])[:-5] if prev_files else 'no previous snapshot'})",
           f"Checked {len(pages)} money pages, robots.txt, {len(sm_files)} sitemap(s) / {snap['sitemap_count']} URLs."]
    if not ch:
        out.append("- No meaningful change.")
    out += [f"- **{urg}** {what}. Evidence: {ev}" for urg, what, ev in ch]
    open(os.path.join(wdir, snap["date"] + ".md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
