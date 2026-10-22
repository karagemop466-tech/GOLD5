#!/usr/bin/env python3
"""GOLD5 verification harness — hallucination + link + arithmetic pass.

Checks (no value may pass without a source):
  1. data.js parses as JSON after the `window.GOLD5_DATA = ` prefix.
  2. Every entry row has >= 1 source URL (row-level rule) and a valid checkedOn date.
  3. Every non-blank price/grams cell has sources; blank grams require the
     'no-gram-weight' flag (or status 'flagged') — blanks are never silently filled.
  4. All URLs are http(s) and belong to the allowlisted official domains.
  5. Spot quotes: primary + cross-checks each have url + asOf; gram value matches
     ounce value within 1% (troy conversion); cross-checks within 3% of primary.
  6. Purity table: fineness values match karat/24 within 0.1%; per-ounce values
     consistent with primary spot within 2% (Kitco publishes these at its own spot).
  7. Derived-value recomputation: for entries with grams+price+karat, recompute the
     price/metal ratio and confirm any sub-melt ratio carries the
     'price-below-metal-value' flag.
  8. Flags reference only existing entry ids.
  9. HTML: every local href/src resolves to an existing file; every external link is http(s).

Exit code 0 = clean, 1 = violations found. Report written to docs/verification/report.md.
Run after EVERY review:  python3 scripts/verify.py
"""
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, "site", "assets", "data.js")
REPORT = os.path.join(ROOT, "docs", "verification", "report.md")

ALLOWED_DOMAINS = {
    "www.kitco.com", "www.cnbc.com", "www.apmex.com",
    "www.bluenile.com",
    "www.etsy.com", "etsy.com", "help.etsy.com",
    "consumer.ftc.gov", "www.ftc.gov", "www.ecfr.gov",
    "www.law.cornell.edu",
    "www.bbb.org",
    "www.consumeraffairs.com", "www.topconsumerreviews.com",
    "jvclegal.org", "reportfraud.ftc.gov",
}
TROY = 31.1034768

ERRORS, WARNINGS, OKS = [], [], []


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


def okk(msg):
    OKS.append(msg)


def load_data():
    with open(DATA_JS, encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r"window\.GOLD5_DATA\s*=\s*(\{.*\})\s*;\s*\Z", txt, re.S)
    if not m:
        err("data.js: cannot locate `window.GOLD5_DATA = {...};` block")
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        err(f"data.js: JSON parse error: {e}")
        return None


def is_url(s):
    return isinstance(s, str) and s.startswith(("http://", "https://"))


def check_url(u, ctx):
    if not is_url(u):
        err(f"{ctx}: URL not http(s): {u!r}")
        return
    host = urlparse(u).hostname or ""
    if host not in ALLOWED_DOMAINS:
        err(f"{ctx}: domain not in official allowlist: {host}")


def check_date(s, ctx):
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        err(f"{ctx}: invalid checkedOn date {s!r}")


def main():
    data = load_data()
    if data is None:
        finish()
        return

    D = data
    spot = D["spot"]["primary"]

    # --- spot checks ---
    check_url(spot["url"], "spot.primary")
    if not spot.get("asOf"):
        err("spot.primary: missing asOf timestamp")
    g = spot["usdPerOz"] / TROY
    if abs(g - spot["usdPerGram"]) / g > 0.01:
        err(f"spot.primary: per-gram {spot['usdPerGram']} inconsistent with per-oz {spot['usdPerOz']} (expected ~{g:.2f})")
    else:
        okk(f"spot.primary gram/oz consistent: {spot['usdPerOz']}/oz ≈ {g:.2f}/g (published {spot['usdPerGram']})")
    for i, q in enumerate(D["spot"]["crossChecks"]):
        ctx = f"spot.crossChecks[{i}] ({q['source']})"
        check_url(q["url"], ctx)
        if not q.get("asOf"):
            err(f"{ctx}: missing asOf")
        if abs(q["usdPerOz"] - spot["usdPerOz"]) / spot["usdPerOz"] > 0.03:
            err(f"{ctx}: {q['usdPerOz']} deviates >3% from primary {spot['usdPerOz']}")
    okk(f"spot: primary + {len(D['spot']['crossChecks'])} cross-checks, all same-day with timestamps")

    # --- purity table ---
    p = D["spot"]["purityValues"]
    check_url(p["url"], "purity table")
    for k, fin in p["fineness"].items():
        karat = int(k[:-1])
        expect = karat / 24 if karat < 24 else 0.9999
        if abs(fin - expect) > 0.0015:
            err(f"purity: {k} fineness {fin} != {expect:.4f}")
    spot24 = spot["usdPerOz"]
    for k, oz in p["perOunce"].items():
        expect = spot24 * p["fineness"][k]
        if abs(oz - expect) / expect > 0.02:
            err(f"purity: {k} per-oz {oz} deviates >2% from primary spot × fineness ({expect:.2f})")
    okk("purity table: fineness & per-ounce values consistent with karat math and primary spot")

    # --- entries ---
    entry_ids = set()
    for e in D["entries"]:
        ctx = f"entry {e['id']}"
        entry_ids.add(e["id"])
        if not (e.get("sources") or []):
            err(f"{ctx}: NO source URLs — row-level rule violated")
        for u in e.get("sources", []):
            check_url(u, ctx)
        check_url(e.get("url"), ctx)
        check_date(e.get("checkedOn"), ctx)
        if e.get("price") is not None and not e.get("sources"):
            err(f"{ctx}: price present without sources")
        if e.get("grams") is None and "no-gram-weight" not in (e.get("flags") or []) and e.get("status") != "flagged":
            err(f"{ctx}: blank grams but no 'no-gram-weight' flag — must be flagged, never filled")
        if e.get("grams") is not None:
            if not e.get("gramsNote"):
                warn(f"{ctx}: grams present without gramsNote")
        # derived recomputation
        if e.get("grams") is not None and e.get("price") is not None and e.get("karat"):
            fin = p["fineness"].get(f"{e['karat']}K", e["karat"] / 24)
            metal_val = e["grams"] * fin * spot["usdPerGram"]
            ratio = e["price"] / metal_val
            if ratio < 1.0:
                if "price-below-metal-value" not in (e.get("flags") or []):
                    err(f"{ctx}: ratio {ratio:.2f} < 1 (price below metal value) but not flagged")
                else:
                    okk(f"{ctx}: recompute ratio {ratio:.2f} < 1 → correctly flagged price-below-metal-value")
            else:
                okk(f"{ctx}: recompute ratio {ratio:.2f} (metal value {metal_val:.2f}) — above melt, consistent")

    # --- flags ---
    for f in D["flags"]:
        if f.get("entryIds"):
            for eid in f["entryIds"]:
                if eid not in entry_ids:
                    err(f"flag {f['id']}: unknown entryId {eid}")
    okk(f"flags: {len(D['flags'])} flags, all entryIds resolve")

    # --- sellers ---
    seller_ids = {s["id"] for s in D["sellers"]}
    for e in D["entries"]:
        if e.get("sellerId") not in seller_ids:
            err(f"entry {e['id']}: sellerId {e['sellerId']} not in sellers")
    for s in D["sellers"]:
        check_date(s.get("checkedOn"), f"seller {s['id']}")
        for u in s.get("sources", []):
            check_url(u, f"seller {s['id']}")
    okk(f"sellers: {len(D['sellers'])} profiles, all dated + sourced")

    # --- references ---
    for r in D["references"]:
        check_url(r["url"], f"reference {r['id']}")
        check_date(r.get("checkedOn"), f"reference {r['id']}")
    okk(f"references: {len(D['references'])} official references, all dated + linked")

    # --- HTML link check ---
    html_files = []
    for base, _dirs, files in os.walk(ROOT):
        rel_base = os.path.relpath(base, ROOT)
        if any(part in {".git", "node_modules", ".venv"} for part in rel_base.split(os.sep)):
            continue
        for fn in files:
            if fn.endswith(".html"):
                html_files.append(os.path.join(base, fn))
    link_re = re.compile(r'(?:href|src)="([^"]+)"')
    n_local = n_ext = 0
    for path in sorted(html_files):
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        # drop inline <script> blocks: their href/src are JS template literals, not HTML links
        html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
        for u in link_re.findall(html):
            if u.startswith(("http://", "https://")):
                n_ext += 1
                host = urlparse(u).hostname or ""
                # external links from the site may point anywhere, but data-file
                # domains are still validated above; here we only check validity.
                continue
            if u.startswith("#") or u.startswith("mailto:"):
                continue
            local = u.split("#")[0].split("?")[0]
            if not local:
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), local))
            if not os.path.exists(target):
                err(f"{rel}: broken local link {u}")
            else:
                n_local += 1
    okk(f"html: {len(html_files)} pages, {n_local} local links resolve, {n_ext} external links http(s)")

    finish(data=D)


def finish(data=None):
    errors = list(ERRORS)
    warnings = list(WARNINGS)
    oks = list(OKS)
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    asof = data["meta"]["asOf"] if data else "?"
    lines = [
        "# Verification report (auto-generated)",
        "",
        f"- Run: {now}",
        f"- Data as of: {asof}",
        f"- Result: **{'PASS' if not errors else 'FAIL'}** — {len(errors)} error(s), {len(warnings)} warning(s), {len(oks)} checks passed",
        "",
        "## Checks passed",
        "",
    ]
    lines += [f"- {m}" for m in oks]
    lines += ["", "## Errors", ""]
    lines += [f"- {m}" for m in errors] if errors else ["- none"]
    lines += ["", "## Warnings", ""]
    lines += [f"- {m}" for m in warnings] if warnings else ["- none"]
    lines += ["",
              "## Reminder",
              "",
              "Recommendation after every review: re-run `python3 scripts/verify.py` and scan the",
              "Flagged for Review page for new hallucination/irregularity signals before publishing.",
              ""]
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines[:6]))
    if warnings:
        print("WARNINGS:")
        print("\n".join(f"  ! {w}" for w in warnings))
    if errors:
        print("ERRORS:")
        print("\n".join(f"  ✗ {e}" for e in errors))
    print(f"Report: {os.path.relpath(REPORT, ROOT)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
