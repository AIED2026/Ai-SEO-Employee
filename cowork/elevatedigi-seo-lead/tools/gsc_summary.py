#!/usr/bin/env python3
"""Summarise a Google Search Console Performance export (the zip or folder from "Export → Download CSV").

Handles both single-range and "Compare" exports. Writes a markdown summary:
totals, top queries/pages, biggest gainers/losers (compare mode), and striking-distance
opportunities (avg position 5–20 with impressions).

Usage: python3 gsc_summary.py <export.zip | folder> [--out summary.md] [--top 25]
"""
import argparse, csv, io, os, re, sys, zipfile


def read_tables(path):
    tables = {}
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        for n in z.namelist():
            if n.lower().endswith(".csv"):
                tables[os.path.basename(n)[:-4]] = list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8-sig")))
    else:
        for n in os.listdir(path):
            if n.lower().endswith(".csv"):
                tables[n[:-4]] = list(csv.DictReader(open(os.path.join(path, n), encoding="utf-8-sig")))
    return tables


def num(v):
    v = (v or "").replace(",", "").replace("%", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0.0


def cols(rows):
    """Map metric -> (current_col, previous_col|None)."""
    keys = list(rows[0].keys()) if rows else []
    out = {}
    for m in ("Clicks", "Impressions", "CTR", "Position"):
        cands = [k for k in keys if k.strip().endswith(m)]
        if len(cands) == 1:
            out[m] = (cands[0], None)
        elif len(cands) >= 2:
            cur = [k for k in cands if re.match(r"(Last|Current|This)", k, re.I)] or [cands[0]]
            prev = [k for k in cands if re.match(r"(Previous|Prior)", k, re.I)] or [cands[1]]
            out[m] = (cur[0], prev[0])
    return keys[0] if keys else None, out


def section(title, rows, top):
    if not rows:
        return f"## {title}\n_no data_\n"
    dim, c = cols(rows)
    compare = any(p for _, p in c.values())
    lines = [f"## {title}"]
    cl, im = c.get("Clicks"), c.get("Impressions")
    tot_c = sum(num(r[cl[0]]) for r in rows) if cl else 0
    tot_i = sum(num(r[im[0]]) for r in rows) if im else 0
    if compare:
        pc = sum(num(r[cl[1]]) for r in rows) if cl and cl[1] else 0
        pi = sum(num(r[im[1]]) for r in rows) if im and im[1] else 0
        lines.append(f"Totals (rows in export): clicks {tot_c:.0f} vs {pc:.0f} ({tot_c - pc:+.0f}), impressions {tot_i:.0f} vs {pi:.0f} ({tot_i - pi:+.0f})\n")
    else:
        lines.append(f"Totals (rows in export): clicks {tot_c:.0f}, impressions {tot_i:.0f}\n")
    pos = c.get("Position"); ctr = c.get("CTR")
    lines.append(f"| {dim} | clicks | impr | CTR | pos |" + (" Δclicks | Δpos |" if compare else ""))
    lines.append("|---|---|---|---|---|" + ("---|---|" if compare else ""))
    for r in sorted(rows, key=lambda r: -num(r[cl[0]]) if cl else 0)[:top]:
        row = f"| {r[dim]} | {num(r[cl[0]]):.0f} | {num(r[im[0]]):.0f} | {r[ctr[0]] if ctr else ''} | {num(r[pos[0]]):.1f} |"
        if compare:
            row += f" {num(r[cl[0]]) - num(r[cl[1]]):+.0f} | {(num(r[pos[0]]) - num(r[pos[1]])) if pos[1] and num(r[pos[1]]) else 0:+.1f} |"
        lines.append(row)
    if compare and cl[1]:
        delta = sorted(rows, key=lambda r: num(r[cl[0]]) - num(r[cl[1]]))
        lines.append(f"\n**Biggest losers:** " + "; ".join(f"{r[dim]} ({num(r[cl[0]]) - num(r[cl[1]]):+.0f})" for r in delta[:8] if num(r[cl[0]]) - num(r[cl[1]]) < 0))
        lines.append(f"\n**Biggest gainers:** " + "; ".join(f"{r[dim]} ({num(r[cl[0]]) - num(r[cl[1]]):+.0f})" for r in delta[::-1][:8] if num(r[cl[0]]) - num(r[cl[1]]) > 0))
    if pos and im:
        sd = [r for r in rows if 5 <= num(r[pos[0]]) <= 20 and num(r[im[0]]) >= 20]
        sd.sort(key=lambda r: -num(r[im[0]]))
        if sd:
            lines.append(f"\n**Striking distance (pos 5–20, ≥20 impressions):** " + "; ".join(f"{r[dim]} (pos {num(r[pos[0]]):.1f}, {num(r[im[0]]):.0f} impr)" for r in sd[:12]))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export"); ap.add_argument("--out"); ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    t = read_tables(a.export)
    if not t:
        sys.exit("No CSV tables found in export")
    filt = t.get("Filters", [])
    out = [f"# GSC summary: {os.path.basename(a.export)}\n"]
    if filt:
        out.append("Filters/date range: " + "; ".join(" ".join(v for v in r.values() if v) for r in filt) + "\n")
    for name in ("Queries", "Pages", "Countries", "Devices", "Search appearance"):
        if name in t:
            out.append(section(name, t[name], a.top if name in ("Queries", "Pages") else 10))
    text = "\n".join(out)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
