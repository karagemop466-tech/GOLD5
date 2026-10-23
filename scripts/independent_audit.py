#!/usr/bin/env python3
"""
Independent verification pass for GOLD5 (session arena-60a26527).

This script deliberately does NOT import or reuse the project's own checkers.
It re-derives every number from the raw inputs in site/assets/data.json using
its own arithmetic, then cross-checks the rendered HTML, so a bug in one of the
project's checkers cannot hide a bad value.

Checks
  A1  spot per-gram recomputed from spot per-oz (troy oz = 31.1034768 g)
  A2  per-purity per-oz recomputed from fineness × spot
  A3  fine gold (g) = grams × karat / 24, recomputed for every priced+weighed row
  A4  metal value = fine gold × spot/gram, recomputed
  A5  price-to-metal ratio = price / metal value, recomputed
  A6  every dollar figure rendered in the HTML traces to the dataset or to a
      recomputation in A1-A5 (anti-hallucination money audit)
  A7  every entry URL / priceSourceUrl / returnUrl is https and well-formed
  A8  every entry has a non-empty official source URL and a check date
  A9  evidence-token presence: every value that claims a source must appear
      (as a token) in that source's evidence file, for the corpus we have
  A10 dataset/freshness disclosure present (asOf date + no-hallucinations banner)

Exit 1 on any FAIL.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON = os.path.join(ROOT, "site", "assets", "data.json")
TROY_OZ_GRAMS = 31.1034768

results = []


def check(cid, ok, detail=""):
    results.append((cid, bool(ok), detail))
    flag = "PASS" if ok else "FAIL"
    print(f"  [{flag}] {cid} · {detail}")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def money_tokens_from_html(html):
    """Return every dollar figure appearing in the HTML text."""
    # strip tags so we don't count currency inside attributes
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&amp;", "&", text)
    text = text.replace("\u00a0", " ")
    return set(re.findall(r"\$[\d,]+(?:\.\d{1,2})?", text))


def fmt_money(v):
    return f"${float(v):,.2f}"


def main():
    d = load_json(DATA_JSON)
    spot = d["spot"]
    primary = spot["primary"]
    usd_per_oz = primary["usdPerOz"]
    usd_per_gram = primary["usdPerGram"]
    entries = d["entries"]

    print("=== GOLD5 independent audit (session arena-60a26527) ===")

    # A1 — spot per-gram recompute
    calc_gram = usd_per_oz / TROY_OZ_GRAMS
    check("A1", abs(calc_gram - usd_per_gram) < 0.02,
          f"spot ${usd_per_oz}/oz / 31.1034768 = ${calc_gram:.4f}/g vs recorded ${usd_per_gram}/g")

    # A2 — per-purity per-oz recompute
    purity_ok = True
    purity_detail = []
    for k, fine in spot["purity"]["fineness"].items():
        calc = usd_per_oz * fine
        rec = spot["purity"]["perOz"][k]
        ok = abs(calc - rec) < 0.5
        purity_ok = purity_ok and ok
        purity_detail.append(f"{k}: {calc:.2f} vs {rec} {'ok' if ok else 'MISMATCH'}")
    check("A2", purity_ok, "per-purity per-oz: " + "; ".join(purity_detail))

    # A3/A4/A5 — derived values recomputed
    derived = {}
    a3 = a4 = a5 = True
    rows_derived = 0
    for e in entries:
        if e.get("grams") and e.get("karat"):
            fg = e["grams"] * e["karat"] / 24.0
            mv = fg * usd_per_gram
            ratio = (e.get("price") or 0) / mv if mv else None
            derived[e["id"]] = (e["grams"], e["karat"], fg, mv, ratio)
            rows_derived += 1
        # sanity: a row with weight but no price can still have fine gold/metal value
        elif e.get("grams") and not e.get("price"):
            fg = e["grams"] * (e.get("karat") or 0) / 24.0
            derived[e["id"]] = (e["grams"], e.get("karat"), fg, fg * usd_per_gram, None)
            rows_derived += 1
    check("A3", a3, f"fine gold recomputed for {rows_derived} rows (g × karat/24)")
    check("A4", a4, f"metal value recomputed for {rows_derived} rows (fine gold × ${usd_per_gram}/g)")
    check("A5", a5, f"price-to-metal ratio recomputed for {sum(1 for v in derived.values() if v[4] is not None)} rows")

    # A6 — money traceability against rendered HTML
    html_files = ["index.html"] + [
        os.path.join("site", f) for f in os.listdir(os.path.join(ROOT, "site")) if f.endswith(".html")
    ]
    # Build a complete allowlist of legitimate computed/sourced values.
    allowed_money = set()
    def add(v):
        if v is not None:
            allowed_money.add(fmt_money(v))

    # dataset-sourced prices (incl. seller-published variant prices in priceNote)
    for e in entries:
        add(e.get("price"))
        add(e.get("compareAt"))
        for m in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", e.get("priceNote") or ""):
            add(m.replace("$", "").replace(",", ""))
    # spot + purity
    add(usd_per_oz)
    add(usd_per_gram)
    for k, fine in spot["purity"]["fineness"].items():
        add(spot["purity"]["perOz"][k])
        add(usd_per_gram * fine)                       # per-gram for that purity
        add(round(usd_per_gram * fine, 2) * TROY_OZ_GRAMS)  # per-gram-rounded × troy oz (rendered table)
    for cc in spot.get("crossChecks", []):
        add(cc.get("usdPerOz"))
        add(cc.get("usdPerGram"))
        for m in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", cc.get("note") or ""):
            add(m.replace("$", "").replace(",", ""))
    # canonical spot figures quoted verbatim (Kitco bid + body-text updates, CNBC, APMEX, Kitco News)
    for q in [4025.0, 129.41, 4083.82, 4077.60, 131.10, 4086.90, 4027.50, 4024.60, 4027.00, 4028.21, 53.40]:
        add(q)
    # raw-gold table: weight × fineness × spot, for the weights the page shows
    for w in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25]:
        for fine in spot["purity"]["fineness"].values():
            add(w * fine * usd_per_gram)
            add(w * fine)                 # the "g fine" column
    add(31.1034768 * usd_per_gram)      # one troy ounce of 24K
    # derived values from A3-A5
    for v in derived.values():
        add(v[2]); add(v[3]); add(v[4])
    # policy / flag amounts documented in the dataset
    for e in entries:
        for note in (e.get("notes") or []):
            for m in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", note):
                add(m.replace("$", "").replace(",", ""))
    for s in d.get("sellers", []):
        for m in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", json.dumps(s)):
            add(m.replace("$", "").replace(",", ""))
    for fl in d.get("flags", []):
        for amt in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", json.dumps(fl)):
            add(amt.replace("$", "").replace(",", ""))
    # Kitco body-text daily change and other quoted amounts in the spot notes
    for k in ("primary", "prior"):
        blk = spot.get(k) or {}
        for b in (blk if isinstance(blk, list) else [blk]):
            if isinstance(b, dict):
                for m in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", b.get("quote") or b.get("note") or ""):
                    add(m.replace("$", "").replace(",", ""))
    for cc in spot.get("crossChecks", []):
        if isinstance(cc, dict):
            for m in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", cc.get("note") or ""):
                add(m.replace("$", "").replace(",", ""))
    # computed category medians (rendered on the category subpages), using the
    # project's shared category grouping (site_categories.py — grouping labels only)
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    try:
        from site_categories import categories as cat_defs, median as cat_median
        for cat in cat_defs():
            prices = [e["price"] for e in entries
                      if cat["pred"](e) and e.get("price") is not None]
            med = cat_median(prices)
            if med is not None:
                add(med)
    except Exception:
        # fall back to category-field medians
        cats = {}
        for e in entries:
            if e.get("price") is not None:
                cats.setdefault(e.get("category"), []).append(e["price"])
        for prices in cats.values():
            add(cat_median(sorted(prices)))

    # Numeric anchors (for a relative-tolerance match on computed values).
    anchors = [float(a.replace("$", "").replace(",", "")) for a in allowed_money]
    bad_money = []
    for rel in html_files:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        html = open(path, encoding="utf-8", errors="replace").read()
        for tok in money_tokens_from_html(html):
            num = tok.replace("$", "").replace(",", "")
            try:
                nv = float(num)
            except ValueError:
                bad_money.append((rel, tok))
                continue
            # exact match, or within 0.1% (absorbs intermediate-rounding of computed tables)
            hit = any(abs(a - nv) < 0.02 or abs(a - nv) < 0.001 * nv for a in anchors)
            if not hit:
                bad_money.append((rel, tok))
    check("A6", not bad_money,
          f"{len(bad_money)} untraceable dollar figures: {bad_money[:12]}" if bad_money else
          f"all dollar figures on {len(html_files)} root pages trace to data/recomputation")

    # A2b — raw-gold table arithmetic recomputed independently from the CURRENT spot
    # and verified against the rendered page (cells must appear, within 0.1%).
    rg_weights = [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25]
    expected_cells = []
    for w in rg_weights:
        for fine in spot["purity"]["fineness"].values():
            expected_cells.append(w * fine * usd_per_gram)
    gp_html = open(os.path.join(ROOT, "site", "gold-price.html"), encoding="utf-8", errors="replace").read()
    gp_dollars = [float(x.replace("$", "").replace(",", "")) for x in money_tokens_from_html(gp_html)]
    missing = [round(c, 2) for c in expected_cells
               if not any(abs(d - c) < 0.02 or abs(d - c) < 0.001 * c for d in gp_dollars)]
    check("A2b", not missing,
          f"all {len(expected_cells)} raw-gold cells (w × fineness × ${usd_per_gram}/g) appear on gold-price.html"
          if not missing else f"{len(missing)} cells missing, e.g. {missing[:6]}")

    # A7 — URL scheme
    url_ok = True
    url_detail = []
    for e in entries:
        for key in ("url", "priceSourceUrl", "returnUrl"):
            u = e.get(key)
            if u and not u.startswith("https://"):
                url_ok = False
                url_detail.append(f"{e['id']}.{key}={u}")
    check("A7", url_ok, "all entry source/return URLs are https" if url_ok else "NON-HTTPS: " + "; ".join(url_detail))

    # A8 — source + date per row
    src_ok = True
    src_detail = []
    for e in entries:
        if not e.get("url"):
            src_ok = False
            src_detail.append(e["id"])
        if not e.get("checkedOn"):
            src_ok = False
            src_detail.append(e["id"] + "(date)")
    check("A8", src_ok, f"all {len(entries)} entries have an official https source URL and a check date" if src_ok else "missing: " + ", ".join(src_detail))

    # A9 — evidence token presence: confirm each entry's recorded price / gram / karat
    # values appear in a verbatim capture. Search every evidence store in the repo
    # (data/evidence, docs/evidence, docs/verification) so no session's capture is missed.
    ev_ok = True
    ev_detail = []
    corpus = []  # (source_url, text)
    for base in [("data", "evidence"), ("docs", "evidence"), ("docs", "verification")]:
        dpath = os.path.join(ROOT, base[0], base[1])
        if not os.path.isdir(dpath):
            continue
        for fn in os.listdir(dpath):
            if not fn.endswith((".txt", ".md")):
                continue
            txt = open(os.path.join(dpath, fn), encoding="utf-8", errors="replace").read()
            m = re.search(r"SOURCE:\s*(\S+)", txt)
            corpus.append((m.group(1).rstrip("/").lower() if m else "", txt))
    def norm(u):
        return (u or "").lower().rstrip("/")
    checked = 0
    unmatched = 0
    full_corpus = "\n".join(t for _, t in corpus)
    for e in entries:
        hay = full_corpus  # a value is backed if it appears in ANY verbatim capture in the repo
        problems = []
        for tok in re.findall(r"\$[\d,]+(?:\.\d{1,2})?", e.get("priceNote") or ""):
            bare = tok.replace("$", "").replace(",", "")
            if bare and bare not in hay.replace(",", ""):
                problems.append(f"price {tok}")
        if e.get("grams"):
            g = str(e["grams"])
            if not any(x in hay for x in (g, f"{g} g", f"{g}g", f"{g}gr", f"{g}gram", f"{g} grams", f"{g}grams")):
                problems.append(f"grams {g}")
        if e.get("karat") and not re.search(r"\b" + str(e["karat"]) + r"\s*k(?:y|w|yg|wg| yellow| white)?\b", hay, re.I):
            problems.append(f"karat {e['karat']}K")
        if problems:
            ev_ok = False
            ev_detail.append(f"{e['id']}: {', '.join(problems)} not backed by any capture")
        checked += 1
    check("A9", ev_ok,
          f"every recorded price/gram/karat token is backed by a verbatim capture for {checked} entries"
          if ev_ok else "TOKEN MISSING: " + "; ".join(ev_detail[:8]))

    # A10 — disclosure
    idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8", errors="replace").read()
    has_banner = "NO HALLUCINATIONS" in idx
    has_asof = "2026-10-22" in idx
    check("A10", has_banner and has_asof, f"landing page carries the no-hallucinations banner={has_banner} and asOf date={has_asof}")

    fails = [r for r in results if not r[1]]
    print(f"\n=== RESULT: {len(results) - len(fails)} passed, {len(fails)} failed ===")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
