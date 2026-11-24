#!/usr/bin/env python3
"""PageSpeed Insights (free API): lab scores + CrUX field data for URLs.

Usage: python3 tools/psi.py URL [URL ...] [--strategy mobile|desktop]
Needs network access to www.googleapis.com. Optional env PSI_API_KEY raises the rate limit
(or store the key as a network secret for www.googleapis.com so the proxy injects it).
"""
import argparse, os, sys
import requests

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def run(url, strategy):
    params = {"url": url, "strategy": strategy, "category": "performance"}
    if os.environ.get("PSI_API_KEY"):
        params["key"] = os.environ["PSI_API_KEY"]
    r = requests.get(API, params=params, timeout=120)
    if r.status_code != 200:
        return {"url": url, "error": f"{r.status_code} {r.text[:200]}"}
    d = r.json()
    lh = d.get("lighthouseResult", {})
    au = lh.get("audits", {})
    fe = d.get("loadingExperience", {}).get("metrics", {})
    def field(k):
        m = fe.get(k)
        return f"{m['percentile']} ({m['category']})" if m else "no field data"
    opps = sorted(
        [(a.get("details", {}).get("overallSavingsMs", 0) or 0, a.get("title")) for a in au.values()
         if a.get("details", {}).get("type") == "opportunity"], reverse=True)[:5]
    return {
        "url": url,
        "score": round((lh.get("categories", {}).get("performance", {}).get("score") or 0) * 100),
        "lab_LCP": au.get("largest-contentful-paint", {}).get("displayValue"),
        "lab_TBT": au.get("total-blocking-time", {}).get("displayValue"),
        "lab_CLS": au.get("cumulative-layout-shift", {}).get("displayValue"),
        "field_LCP_ms": field("LARGEST_CONTENTFUL_PAINT_MS"),
        "field_INP_ms": field("INTERACTION_TO_NEXT_PAINT"),
        "field_CLS": field("CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        "top_opportunities": [f"{t} (~{int(s)} ms)" for s, t in opps if s],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--strategy", default="mobile")
    a = ap.parse_args()
    for u in a.urls:
        res = run(u, a.strategy)
        print(f"\n## {u} [{a.strategy}]")
        for k, v in res.items():
            if k != "url":
                print(f"- {k}: {v}")


if __name__ == "__main__":
    sys.exit(main())
