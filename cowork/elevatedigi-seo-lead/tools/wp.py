#!/usr/bin/env python3
"""
Safe WordPress REST helper for the AI SEO employee.

Auth: a dedicated Editor user with an Application Password. Preferred: store it as a network
secret (Basic auth) for the site's host in the cloud environment, so the proxy injects the
Authorization header and no secret lives in files. Fallback: env vars WP_USER / WP_APP_PASSWORD.

Every write is a DRY RUN unless --apply is passed, and saves a JSON backup of the previous values.

Usage:
  wp.py get     <site> <page-url>
  wp.py update  <site> <page-url> [--title T] [--excerpt E] [--content-file F] [--client SLUG] [--apply]
  wp.py alt     <site> <media-id> "<alt text>" [--client SLUG] [--apply]
  wp.py draft   <site> --title T --content-file F [--type posts|pages] [--apply]
  wp.py restore <backup.json> [--apply]
  wp.py whoami  <site>
"""
import argparse, base64, datetime, json, os, sys
from urllib.parse import urlparse
import requests

S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (compatible; ElevateDigi-SEO/1.0)"
if os.environ.get("WP_USER") and os.environ.get("WP_APP_PASSWORD"):
    tok = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    S.headers["Authorization"] = f"Basic {tok}"


def api(site):
    return site.rstrip("/") + "/wp-json/wp/v2"


def find(site, url):
    slug = [p for p in urlparse(url).path.split("/") if p][-1] if urlparse(url).path.strip("/") else None
    for typ in ("pages", "posts"):
        if slug is None:
            break
        r = S.get(f"{api(site)}/{typ}", params={"slug": slug, "context": "edit", "status": "any"}, timeout=40)
        if r.status_code in (400, 401, 403):  # not authenticated as an editor: fall back to public read
            r = S.get(f"{api(site)}/{typ}", params={"slug": slug}, timeout=40)
        if r.status_code != 200:
            sys.exit(f"REST error {r.status_code}: {r.text[:200]} (WAF/mod_security or REST disabled?)")
        for item in r.json():
            if item.get("link", "").rstrip("/") == url.rstrip("/") or len(r.json()) == 1:
                return typ, item
    sys.exit(f"Not found via REST: {url}")


def raw(v):
    return v.get("raw", v.get("rendered", "")) if isinstance(v, dict) else v


def backup(client, kind, payload):
    d = os.path.join("clients", client or "_unknown", "changes", "backups")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{datetime.datetime.now():%Y%m%d-%H%M%S}-{kind}.json")
    json.dump(payload, open(p, "w"), indent=2, ensure_ascii=False)
    return p


def cmd_get(a):
    typ, it = find(a.site, a.url)
    yo = it.get("yoast_head_json") or {}
    print(json.dumps({
        "type": typ, "id": it["id"], "link": it.get("link"), "status": it.get("status"),
        "title": raw(it.get("title", {})), "excerpt": raw(it.get("excerpt", {}))[:300],
        "seo_title(yoast)": yo.get("title"), "seo_desc(yoast)": yo.get("description"),
        "canonical(yoast)": yo.get("canonical"), "robots(yoast)": yo.get("robots"),
        "aioseo": it.get("aioseo_head_json") and {k: it["aioseo_head_json"].get(k) for k in ("title", "description", "canonical_url")},
        "modified": it.get("modified"),
    }, indent=2, ensure_ascii=False))


def cmd_update(a):
    typ, it = find(a.site, a.url)
    new = {}
    if a.title: new["title"] = a.title
    if a.excerpt: new["excerpt"] = a.excerpt
    if a.content_file: new["content"] = open(a.content_file, encoding="utf-8").read()
    if not new:
        sys.exit("Nothing to update")
    old = {k: raw(it.get(k, {})) for k in new}
    print(f"{typ} #{it['id']} {it.get('link')}")
    for k in new:
        print(f"- {k}: {str(old[k])[:120]!r}  →  {str(new[k])[:120]!r}")
    if not a.apply:
        print("DRY RUN. Re-run with --apply after approval."); return
    bp = backup(a.client, f"{typ}-{it['id']}", {"site": a.site, "endpoint": f"{typ}/{it['id']}", "old": old, "new": new})
    r = S.post(f"{api(a.site)}/{typ}/{it['id']}", json=new, timeout=60)
    print(f"HTTP {r.status_code}; backup: {bp}")
    if r.status_code >= 300: print(r.text[:400])


def cmd_alt(a):
    r = S.get(f"{api(a.site)}/media/{a.media_id}", params={"context": "edit"}, timeout=40)
    if r.status_code != 200: sys.exit(f"{r.status_code} {r.text[:200]}")
    old = r.json().get("alt_text", "")
    print(f"media #{a.media_id}: {old!r} → {a.alt!r}")
    if not a.apply:
        print("DRY RUN."); return
    bp = backup(a.client, f"media-{a.media_id}", {"site": a.site, "endpoint": f"media/{a.media_id}", "old": {"alt_text": old}, "new": {"alt_text": a.alt}})
    r = S.post(f"{api(a.site)}/media/{a.media_id}", json={"alt_text": a.alt}, timeout=60)
    print(f"HTTP {r.status_code}; backup: {bp}")


def cmd_draft(a):
    body = {"title": a.title, "content": open(a.content_file, encoding="utf-8").read(), "status": "draft"}
    print(f"Create {a.type[:-1]} DRAFT: {a.title!r} ({len(body['content'])} chars)")
    if not a.apply:
        print("DRY RUN."); return
    r = S.post(f"{api(a.site)}/{a.type}", json=body, timeout=60)
    print(f"HTTP {r.status_code}", r.json().get("link") if r.ok else r.text[:300])


def cmd_restore(a):
    b = json.load(open(a.backup))
    print(f"Restore {b['endpoint']} on {b['site']}: {json.dumps(b['old'], ensure_ascii=False)[:300]}")
    if not a.apply:
        print("DRY RUN."); return
    r = S.post(f"{api(b['site'])}/{b['endpoint']}", json=b["old"], timeout=60)
    print(f"HTTP {r.status_code}")


def cmd_whoami(a):
    r = S.get(f"{api(a.site)}/users/me", params={"context": "edit"}, timeout=30)
    print(r.status_code, r.json().get("name") if r.ok else r.text[:200], r.json().get("roles") if r.ok else "")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get"); g.add_argument("site"); g.add_argument("url")
    u = sub.add_parser("update"); u.add_argument("site"); u.add_argument("url")
    u.add_argument("--title"); u.add_argument("--excerpt"); u.add_argument("--content-file")
    m = sub.add_parser("alt"); m.add_argument("site"); m.add_argument("media_id"); m.add_argument("alt")
    d = sub.add_parser("draft"); d.add_argument("site"); d.add_argument("--title", required=True)
    d.add_argument("--content-file", required=True); d.add_argument("--type", default="posts", choices=["posts", "pages"])
    r = sub.add_parser("restore"); r.add_argument("backup")
    w = sub.add_parser("whoami"); w.add_argument("site")
    for p in (u, m, d, r):
        p.add_argument("--apply", action="store_true")
    for p in (u, m):
        p.add_argument("--client")
    a = ap.parse_args()
    {"get": cmd_get, "update": cmd_update, "alt": cmd_alt, "draft": cmd_draft, "restore": cmd_restore, "whoami": cmd_whoami}[a.cmd](a)


if __name__ == "__main__":
    main()
