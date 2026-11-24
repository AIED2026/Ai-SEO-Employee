#!/usr/bin/env python3
"""
SEO site crawler for the AI SEO employee.

Crawls a site from its sitemap(s) and internal links, records per-page SEO
signals, and writes:
  <out>/pages.csv     one row per URL
  <out>/summary.md    issue rollup with counts and example URLs
  <out>/summary.json  machine-readable rollup (for week-over-week diffs)

Usage:
  python3 tools/crawl.py https://example.com --max 300 --out clients/example/crawls/2026-11-24
"""
import argparse, csv, json, os, re, sys, time
from collections import defaultdict, Counter
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; SEO-Audit-Bot/1.0; +agency audit)"
SKIP_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg|pdf|zip|mp4|mp3|css|js|ico|woff2?|ttf|xml|docx?|xlsx?)(\?|$)", re.I)

S = requests.Session()
S.headers["User-Agent"] = UA


def fetch(url, timeout=25):
    t = time.time()
    try:
        r = S.get(url, timeout=timeout, allow_redirects=True)
        return r, round(time.time() - t, 2), None
    except Exception as e:
        return None, round(time.time() - t, 2), str(e)[:200]


def norm(u):
    u, _ = urldefrag(u)
    return u.strip()


def sitemap_urls(root, robots_txt):
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots_txt or "")
    if not maps:
        maps = [urljoin(root, p) for p in ("/sitemap_index.xml", "/sitemap.xml", "/wp-sitemap.xml")]
    seen, out = set(), []
    queue = list(maps)
    while queue and len(seen) < 60:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r, _, err = fetch(sm)
        if not r or r.status_code != 200 or "<" not in r.text[:200]:
            continue
        locs = re.findall(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)\s*(?:\]\]>)?\s*</loc>", r.text)
        for l in locs:
            l = l.replace("&amp;", "&")
            if l.endswith(".xml") or "sitemap" in l.split("/")[-1]:
                queue.append(l)
            else:
                out.append(l)
    return out, sorted(seen)


def schema_types(soup):
    types = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(sc.string or "{}")
        except Exception:
            types.append("INVALID_JSONLD")
            continue
        def walk(x):
            if isinstance(x, dict):
                t = x.get("@type")
                if t:
                    types.extend(t if isinstance(t, list) else [t])
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(d)
    return types


def analyse(url, r, secs, host_set):
    row = {"url": url, "status": r.status_code, "final_url": r.url, "redirected": r.url.rstrip("/") != url.rstrip("/"),
           "redirect_hops": len(r.history),
           "secs": secs, "bytes": len(r.content), "content_type": r.headers.get("content-type", "")}
    links = []
    if "html" not in row["content_type"]:
        return row, links
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    rb = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
    can = soup.find("link", rel=lambda v: v and "canonical" in v)
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    imgs = soup.find_all("img")
    body_text = soup.body.get_text(" ", strip=True) if soup.body else ""
    st = schema_types(soup)
    row.update({
        "title": title, "title_len": len(title),
        "meta_desc": (md.get("content") or "").strip() if md else "",
        "robots_meta": (rb.get("content") or "") if rb else "",
        "x_robots": r.headers.get("x-robots-tag", ""),
        "canonical": can.get("href", "") if can else "",
        "h1_count": len(h1s), "h1": " | ".join(h1s)[:200],
        "h2_count": len(soup.find_all("h2")),
        "words": len(body_text.split()),
        "imgs": len(imgs), "imgs_no_alt": sum(1 for i in imgs if not (i.get("alt") or "").strip()),
        "schema": ",".join(sorted(set(st))),
        "hreflang": len(soup.select("link[hreflang]")),
        "lang": soup.html.get("lang", "") if soup.html else "",
        "og_title": bool(soup.find("meta", property="og:title")),
    })
    row["meta_desc_len"] = len(row["meta_desc"])
    http_links = 0
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if h.startswith("http://") and urlparse(h).netloc in host_set:
            http_links += 1
        if h.startswith(("mailto:", "tel:", "javascript:", "#", "whatsapp:")):
            continue
        absu = norm(urljoin(r.url, h))
        if urlparse(absu).netloc in host_set:
            links.append(absu)
    row["internal_links_out"] = len(set(links))
    row["http_internal_links"] = http_links
    return row, links


def crawl(root, max_pages, delay):
    root = root if root.endswith("/") else root + "/"
    rr, _, _ = fetch(root)
    if rr is None:
        sys.exit(f"Cannot reach {root}")
    base = f"{urlparse(rr.url).scheme}://{urlparse(rr.url).netloc}/"
    host = urlparse(base).netloc
    bare = host[4:] if host.startswith("www.") else host
    host_set = {bare, "www." + bare}
    robots_r, _, _ = fetch(urljoin(base, "/robots.txt"))
    robots = robots_r.text if robots_r is not None and robots_r.status_code == 200 else ""
    sm_urls, sm_files = sitemap_urls(base, robots)

    # host consistency checks
    variants = {}
    for v in (f"https://{bare}/", f"https://www.{bare}/", f"http://{bare}/"):
        r, _, err = fetch(v)
        variants[v] = f"{r.status_code} -> {r.url}" if r is not None else f"ERR {err}"
    probe, _, _ = fetch(urljoin(base, "/this-page-should-404-seo-check"))
    soft404 = probe is not None and probe.status_code == 200

    queue = [base] + [u for u in sm_urls if urlparse(u).netloc in host_set]
    seen, rows, inlinks = set(), [], Counter()
    sources = defaultdict(list)
    while queue and len(rows) < max_pages:
        u = norm(queue.pop(0))
        if u in seen or SKIP_EXT.search(u) or "?" in u and len(rows) > 20:
            continue
        seen.add(u)
        r, secs, err = fetch(u)
        if r is None:
            rows.append({"url": u, "status": "LOOP" if "redirect" in (err or "").lower() else "ERR", "error": err, "secs": secs})
            continue
        row, links = analyse(u, r, secs, host_set)
        row["in_sitemap"] = u in sm_urls
        rows.append(row)
        for l in set(links):
            inlinks[l] += 1
            if len(sources[l]) < 5:
                sources[l].append(u)
            if l not in seen and not SKIP_EXT.search(l):
                queue.append(l)
        time.sleep(delay)
    for row in rows:
        row["internal_links_in"] = inlinks.get(row["url"], 0)
        row["linked_from"] = " ".join(sources.get(row["url"], [])[:3])
    meta = {"root": base, "robots_txt": robots, "sitemaps": sm_files, "sitemap_url_count": len(sm_urls),
            "host_variants": variants, "soft_404": soft404, "crawled": len(rows),
            "crawl_capped": bool(queue) and len(rows) >= max_pages}
    return rows, meta


def rollup(rows, meta):
    issues = defaultdict(list)
    html = [r for r in rows if "html" in str(r.get("content_type", "")) and r.get("status") == 200]
    titles, descs = defaultdict(list), defaultdict(list)
    for r in rows:
        u, st = r["url"], r.get("status")
        if st == "ERR" or (isinstance(st, int) and st >= 400):
            issues["Broken/erroring URLs (4xx/5xx/ERR)"].append(f"{u} [{st}]")
        if r.get("redirected"):
            issues["Internal URLs that redirect"].append(f"{u} -> {r.get('final_url')}")
        if int(r.get("redirect_hops") or 0) >= 2:
            issues["Redirect chains (2+ hops)"].append(f"{u} ({r['redirect_hops']} hops) -> {r.get('final_url')}")
        if st == "LOOP":
            issues["Redirect loops"].append(u)
        if (st == "ERR" or st == "LOOP" or (isinstance(st, int) and st >= 400)) and r.get("linked_from"):
            issues["Broken internal links (target ← linked from)"].append(f"{u} [{st}] ← {r['linked_from']}")
    for r in html:
        u = r["url"]
        if "noindex" in (r.get("robots_meta", "") + r.get("x_robots", "")).lower():
            issues["Noindex pages"].append(u)
        if not r.get("title"):
            issues["Missing <title>"].append(u)
        elif r["title_len"] > 65:
            issues["Title > 65 chars (truncation risk)"].append(f"{u} ({r['title_len']})")
        elif r["title_len"] < 25:
            issues["Title < 25 chars (under-optimised)"].append(f"{u} ({r['title']})")
        if not r.get("meta_desc"):
            issues["Missing meta description"].append(u)
        elif r["meta_desc_len"] > 165:
            issues["Meta description > 165 chars"].append(u)
        if r.get("h1_count", 0) == 0:
            issues["No H1"].append(u)
        elif r["h1_count"] > 1:
            issues["Multiple H1s"].append(f"{u} ({r['h1_count']})")
        can = r.get("canonical", "")
        if not can:
            issues["Missing canonical"].append(u)
        elif urlparse(can).netloc and urlparse(can).netloc not in (urlparse(meta["root"]).netloc, urlparse(meta["root"]).netloc.replace("www.", "")):
            issues["Canonical points to ANOTHER domain"].append(f"{u} -> {can}")
        elif can.rstrip("/") != r.get("final_url", u).rstrip("/"):
            issues["Canonicalised to a different URL"].append(f"{u} -> {can}")
        if r.get("words", 0) < 250:
            issues["Thin content (< 250 words rendered in HTML)"].append(f"{u} ({r.get('words')})")
        if r.get("imgs_no_alt", 0):
            issues["Images missing alt text"].append(f"{u} ({r['imgs_no_alt']}/{r['imgs']})")
        if not r.get("schema"):
            issues["No structured data (JSON-LD)"].append(u)
        elif "INVALID_JSONLD" in r.get("schema", ""):
            issues["Invalid JSON-LD (parse error)"].append(u)
        if r.get("http_internal_links", 0):
            issues["Internal links using http:// (HTTPS consistency)"].append(f"{u} ({r['http_internal_links']})")
        if r.get("secs", 0) > 3:
            issues["Slow server response (> 3s full HTML)"].append(f"{u} ({r['secs']}s)")
        if r.get("internal_links_in", 0) == 0 and r["url"].rstrip("/") != meta["root"].rstrip("/"):
            issues["Orphan-ish (0 internal links found pointing in)"].append(u)
        if r.get("title"):
            titles[r["title"]].append(u)
        if r.get("meta_desc"):
            descs[r["meta_desc"]].append(u)
    for t, us in titles.items():
        if len(us) > 1:
            issues["Duplicate titles"].append(f"'{t[:70]}' x{len(us)}: {us[0]} ...")
    for d, us in descs.items():
        if len(us) > 1:
            issues["Duplicate meta descriptions"].append(f"x{len(us)}: {us[0]} ...")
    if meta["soft_404"]:
        issues["SITE: non-existent URLs return 200 (soft 404)"].append(meta["root"])
    finals = {v.split("-> ")[-1].rstrip("/") for v in meta["host_variants"].values() if "->" in v}
    if len(finals) > 1:
        issues["SITE: www/non-www/http do not resolve to one host"].extend(f"{k}: {v}" for k, v in meta["host_variants"].items())
    if not meta["sitemaps"]:
        issues["SITE: no sitemap found"].append(meta["root"])
    return issues, html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("--delay", type=float, default=0.3)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows, meta = crawl(a.root, a.max, a.delay)
    issues, html = rollup(rows, meta)
    keys = sorted({k for r in rows for k in r})
    first = ["url", "status", "title", "title_len", "meta_desc_len", "h1_count", "h1", "words", "canonical", "schema",
             "imgs", "imgs_no_alt", "internal_links_in", "in_sitemap", "secs"]
    keys = first + [k for k in keys if k not in first]
    with open(os.path.join(a.out, "pages.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    summary = {"meta": {k: v for k, v in meta.items() if k != "robots_txt"},
               "issue_counts": {k: len(v) for k, v in issues.items()}, "html_pages_200": len(html)}
    json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=2)
    with open(os.path.join(a.out, "summary.md"), "w", encoding="utf-8") as f:
        f.write(f"# Crawl summary: {meta['root']}\n\n")
        f.write(f"- Pages crawled: {meta['crawled']} (HTML 200: {len(html)}){' — CAPPED' if meta['crawl_capped'] else ''}\n")
        f.write(f"- Sitemaps: {', '.join(meta['sitemaps']) or 'none'} ({meta['sitemap_url_count']} URLs)\n")
        f.write(f"- Soft 404: {meta['soft_404']}\n- Host variants: {json.dumps(meta['host_variants'])}\n\n")
        f.write("## Issues (count, up to 8 examples)\n\n")
        for k, v in sorted(issues.items(), key=lambda kv: -len(kv[1])):
            f.write(f"### {k} — {len(v)}\n")
            for x in v[:8]:
                f.write(f"- {x}\n")
            f.write("\n")
        f.write("## robots.txt\n\n```\n" + meta["robots_txt"][:3000] + "\n```\n")
    print(f"{meta['root']}: crawled {meta['crawled']}, issues: " + ", ".join(f"{k}={len(v)}" for k, v in sorted(issues.items(), key=lambda kv: -len(kv[1]))))


if __name__ == "__main__":
    main()
