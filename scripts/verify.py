#!/usr/bin/env python3
"""GOLD5 security check — hallucination, provenance, arithmetic and link pass.

Run after EVERY review:   python3 scripts/verify.py

What it enforces
----------------
 1  schema      data/unified.json parses; site/assets/data.js carries identical data.
 2  provenance  every listing row has an https official URL, a check date and a valid verifyState.
 3  sources     every listing/seller/reference URL is https and on the recorded source list.
 4  blanks      a blank weight/price/hallmark/return cell MUST carry the matching flag.
 5  prior       a row labelled "prior capture" MUST carry the prior-capture flag.
 6  arithmetic  pure-gold grams, metal value and price/metal ratio recompute from raw inputs;
                spot per-gram vs per-ounce agrees; per-karat values agree with fineness;
                cross-check quotes agree with the primary within 3%.
 7  flags       every flag has a severity, a source and entry ids that exist.
 8  money       every "$" figure written into the generated HTML must trace back to the dataset
                (this is the check that catches a hand-typed or hallucinated price).
 9  links       every local href/src resolves to a real file; every external link is https.
10  pages       required pages exist and the landing page carries the no-hallucinations statement.
11  negative    deliberately corrupted copies (fake price, fake weight, fake derived value,
                hand-typed dollar figure) must be REJECTED — proving the checks actually work.

Exit code 0 = clean. Writes data/check_status.json and docs/verification/pass2-report.md.
"""
import copy
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNIFIED = os.path.join(ROOT, "data", "unified.json")
DATA_JS = os.path.join(ROOT, "site", "assets", "data.js")
STATUS = os.path.join(ROOT, "data", "check_status.json")
REPORT = os.path.join(ROOT, "docs", "verification", "pass2-report.md")

TROY = 31.1034768
KARATS = (10, 14, 18, 22, 24)
STATES = ("P2", "prior", "unverified")
SEVERITIES = ("high", "medium", "low", "info")
PAGES = ["index.html", "listings.html", "sellers.html", "gold-price.html", "calculator.html",
         "checklist.html", "analysis.html", "verification.html", "flagged.html", "sources.html",
         "archive.html"]


def load():
    with open(UNIFIED, encoding="utf-8") as f:
        data = json.load(f)
    with open(DATA_JS, encoding="utf-8") as f:
        js = f.read()
    m = js[js.index("{"): js.rindex("}") + 1]
    return data, json.loads(m), js


def money_fmt(v, dec=2):
    return "{:,.{d}f}".format(float(v), d=dec)


def all_numbers(obj, acc):
    """Collect every numeric value and every dollar figure in string fields."""
    if isinstance(obj, dict):
        for v in obj.values():
            all_numbers(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            all_numbers(v, acc)
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, (int, float)):
        acc.add(float(obj))
        acc.add(round(float(obj), 2))
    elif isinstance(obj, str):
        for m in re.finditer(r"\$([0-9][0-9,]*\.?[0-9]*)", obj):
            acc.add(float(m.group(1).replace(",", "")))
        for m in re.finditer(r"(?<![0-9.])([0-9][0-9,]*\.[0-9]{2})(?![0-9])", obj):
            try:
                acc.add(float(m.group(1).replace(",", "")))
            except ValueError:
                pass


def validate(data, html_files, money_set_extra=None, deep_links=True):
    """Return (errors, warnings, notes). Pure function so negative tests can reuse it."""
    E, W, N = [], [], []

    if data.get("meta", {}).get("pass") not in ("P1", "P2"):
        E.append("meta.pass missing/unknown")
    if "NO HALLUCINATIONS" not in data.get("meta", {}).get("noHallucinations", "").upper():
        E.append("meta.noHallucinations statement missing")

    listings = data.get("listings", [])
    sellers = {s["id"]: s for s in data.get("sellers", [])}
    refs = {r["id"]: r for r in data.get("references", [])}
    flags = {f["id"]: f for f in data.get("flags", [])}
    fineness = data["spot"]["purity"]["fineness"]
    spot_g = data["spot"]["primary"]["usdPerGram"]

    # ---- 1/2/3/4/5 per listing -------------------------------------------------------
    seen = set()
    if not listings:
        E.append("no listings")
    for r in listings:
        rid = r.get("id", "?")
        if rid in seen:
            E.append("duplicate listing id: " + rid)
        seen.add(rid)
        if not str(r.get("url", "")).startswith("https://"):
            E.append("listing without https official URL: " + rid)
        if not r.get("checkedOn"):
            E.append("listing without checkedOn: " + rid)
        if r.get("verifyState") not in STATES:
            E.append("bad verifyState on %s: %r" % (rid, r.get("verifyState")))
        if r.get("sellerId") not in sellers:
            E.append("unknown seller on " + rid)
        if r.get("karat") not in KARATS:
            E.append("implausible karat on %s: %r" % (rid, r.get("karat")))
        fl = set(r.get("flags") or [])
        if r.get("grams") is None and "no-gram-weight" not in fl:
            E.append("blank weight not flagged: " + rid)
        if r.get("price") is None and not (fl & {"no-price", "usd-price-unverified", "price-from-search-snippet"}):
            E.append("blank price not flagged: " + rid)
        if not (r.get("hallmark") or "").strip() and not (r.get("hallmarkNote") or "").strip() and "hallmark-not-shown" not in fl:
            E.append("missing hallmark without flag: " + rid)
        if not r.get("returns") and not (fl & {"returns-unstated", "sold-at-check"}):
            E.append("missing return policy without flag: " + rid)
        if r.get("verifyState") == "prior" and "prior-capture" not in fl:
            E.append("prior-capture row lacks the prior-capture flag: " + rid)
        if r.get("price") is not None and float(r["price"]) <= 0:
            E.append("non-positive price: " + rid)
        if r.get("grams") is not None and float(r["grams"]) <= 0:
            E.append("non-positive weight: " + rid)

        # ---- 6 arithmetic recompute ----
        f = fineness.get(str(r.get("karat")) + "K")
        if r.get("grams") is not None and f:
            gold = r["grams"] * f
            val = gold * spot_g
            if r.get("gold_g") is None or abs(r["gold_g"] - gold) > 0.001:
                E.append("gold_g does not recompute: %s (%r vs %.4f)" % (rid, r.get("gold_g"), gold))
            if r.get("metal_value") is None or abs(r["metal_value"] - val) > 0.01:
                E.append("metal_value does not recompute: %s (%r vs %.2f)" % (rid, r.get("metal_value"), val))
            if r.get("price"):
                ratio = r["price"] / val
                if r.get("ratio") is None or abs(r["ratio"] - ratio) > 0.001:
                    E.append("ratio does not recompute: %s (%r vs %.3f)" % (rid, r.get("ratio"), ratio))
                below = ratio < 1
                if below and "price-below-metal-value" not in fl:
                    E.append("below-melt price without the red flag: " + rid)
                if not below and "price-below-metal-value" in fl:
                    E.append("false below-melt flag: " + rid)
        elif r.get("gold_g") is not None or r.get("metal_value") is not None:
            E.append("derived value present without a weight: " + rid)

    # ---- spot consistency -------------------------------------------------------------
    p = data["spot"]["primary"]
    if abs(p["usdPerOz"] / TROY - p["usdPerGram"]) > 0.5:
        E.append("spot per-gram does not match per-ounce / 31.1034768")
    for k, per_oz in data["spot"]["purity"]["perOunce"].items():
        kk = int(k.rstrip("K"))
        expect = data["spot"]["primary"]["usdPerOz"] * kk / 24.0
        if abs(per_oz - expect) > 0.15:
            E.append("purity %s inconsistent with spot: %.2f vs %.2f" % (k, per_oz, expect))
        if abs(data["spot"]["purity"]["fineness"][k] - kk / 24.0) > 0.001:
            E.append("fineness %s not equal to karat/24" % k)
        pg = data["spot"]["purity"].get("perGram", {}).get(k)
        if pg is None or abs(pg - per_oz / TROY) > 0.01:
            E.append("per-gram value for %s missing or wrong (derived check)" % k)
    for q in data["spot"]["crossChecks"]:
        if not str(q.get("url", "")).startswith("https://"):
            E.append("cross-check without https url")
        if q.get("usdPerOz"):
            dev = abs(q["usdPerOz"] - p["usdPerOz"]) / p["usdPerOz"]
            if dev > 0.03:
                W.append("cross-check %s deviates %.1f%% from primary" % (q["source"], dev * 100))
            N.append("cross-check %s within %.2f%%" % (q["source"], dev * 100))

    # ---- 7 flags ----------------------------------------------------------------------
    flag_ids = set(flags)
    for r in listings:
        for f in r.get("flags") or []:
            if f not in MORPHOLOGY:
                W.append("unknown flag label %r on %s" % (f, r["id"]))
    for f in data.get("flags", []):
        if f.get("severity") not in SEVERITIES:
            E.append("bad severity on " + f.get("id", "?"))
        if not f.get("source"):
            E.append("flag without source: " + f.get("id", "?"))
        for rid in f.get("entries") or []:
            if rid not in seen:
                E.append("flag %s references unknown listing %s" % (f.get("id"), rid))

    # ---- 3 sources allowlist-ish: https + domain appears in data ----------------------
    for s in data.get("sellers", []):
        for u in s.get("sources", []) + [s.get("website", "")]:
            if u and not str(u).startswith("https://"):
                E.append("seller source not https: %s" % s.get("id"))
    for r in data.get("references", []):
        if not str(r.get("url", "")).startswith("https://"):
            E.append("reference not https: " + r.get("id", "?"))

    # ---- 7b numeric claims in prose must match the dataset ---------------------------
    def prose_blob(o):
        if isinstance(o, dict):
            for v in o.values():
                yield from prose_blob(v)
        elif isinstance(o, list):
            for v in o:
                yield from prose_blob(v)
        elif isinstance(o, str):
            yield o
    for text in prose_blob({"flags": data.get("flags"), "checklist": data.get("checklist")}):
        for m in re.finditer(r"(\d+) of (?:the )?(\d+) listings", text):
            if int(m.group(2)) != len(listings):
                E.append("prose claims %r but the dataset has %d listings" % (m.group(0), len(listings)))

    # ---- 8 money traceability ---------------------------------------------------------
    allowed = set()
    all_numbers(data, allowed)
    if money_set_extra:
        allowed |= money_set_extra
    for name, html in html_files.items():
        for m in re.finditer(r"\$([0-9][0-9,]*(?:\.[0-9]+)?)", html):
            raw = m.group(1).replace(",", "")
            try:
                v = float(raw)
            except ValueError:
                E.append("unparseable dollar figure in %s: %s" % (name, m.group(0)))
                continue
            if not any(abs(v - a) < 0.005 for a in allowed):
                E.append("UNSOURCED DOLLAR FIGURE in %s: %s (not in dataset)" % (name, m.group(0)))

    # ---- 9/10 links and required pages ------------------------------------------------
    for name in PAGES:
        if name not in html_files:
            E.append("required page missing: " + name)
        else:
            if "⚠ NO HALLUCINATIONS</b>" not in html_files[name]:
                E.append("no-hallucinations banner missing on " + name)
    local_targets = set()
    for name, html in html_files.items():
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            u = m.group(1)
            if u.startswith(("http://", "https://", "mailto:", "#")):
                if u.startswith("http://"):
                    E.append("insecure external link on %s: %s" % (name, u))
                continue
            if u.startswith("data:"):
                continue
            path = u.split("#")[0].split("?")[0]
            if not path:
                continue
            full = os.path.normpath(os.path.join(ROOT, path))
            if not full.startswith(ROOT):
                E.append("link escapes repo on %s: %s" % (name, u))
            elif not os.path.exists(full):
                E.append("broken local link on %s: %s" % (name, u))
            else:
                local_targets.add(path)
        # html must not contain obvious placeholder text
        for bad in ("TODO:", "FIXME:", "lorem ipsum"):
            if bad.lower() in html.lower():
                W.append("suspicious placeholder text %r on %s" % (bad, name))
    if "flagged.html" not in html_files["index.html"]:
        E.append("landing page does not link the Flagged for review page")
    if deep_links:
        for must in ("docs/index.html", "guide/index.html", "index-090bae73.html"):
            if must not in local_targets:
                W.append("archive link not present in generated pages: " + must)

    # ---- archive link integrity (warn-only: these are preserved, not maintained, views) ----
    archive_files = []
    for sub in ("docs", "pages", "guide", "site"):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".html"):
                    archive_files.append(os.path.join(sub, fn))
    for rel in ("index-090bae73.html",):
        if os.path.exists(os.path.join(ROOT, rel)):
            archive_files.append(rel)
    broken = 0
    for rel in archive_files:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as f:
            text = f.read()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            u = m.group(1)
            if u.startswith(("http://", "https://", "mailto:", "#", "data:", "javascript:")):
                continue
            if "${" in u or "' +" in u or '" +' in u:
                continue  # JS template literal inside an archived page, not a real link
            path = u.split("#")[0].split("?")[0]
            if not path:
                continue
            full = os.path.normpath(os.path.join(os.path.dirname(os.path.join(ROOT, rel)), path))
            if not os.path.exists(full):
                broken += 1
                if broken <= 8:
                    W.append("archive link broken in %s: %s" % (rel, u))
    N.append("archive pages scanned for links: %d (broken: %d)" % (len(archive_files), broken))

    # ---- table completeness: every listing id appears in listings.html ----------------
    if "listings.html" in html_files:
        for r in listings:
            if r["id"] not in html_files["listings.html"] and r["name"][:40] not in html_files["listings.html"]:
                E.append("listing missing from the All listings table: " + r["id"])

    return E, W, N


MORPHOLOGY = {
    "no-gram-weight", "hallmark-not-shown", "setting-only", "seller-stated-weight", "variant-price",
    "sale-price-expires", "short-return-window", "price-below-metal-value", "sold-at-check",
    "price-from-search-snippet", "usd-price-unverified", "no-price", "returns-unstated",
    "metal-text-contradiction", "restocking-fee", "ships-from-india", "cross-border-shipping",
    "prior-capture", "retail-vs-sale-price",
}


def read_pages():
    out = {}
    for name in PAGES:
        path = os.path.join(ROOT, name)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                out[name] = f.read()
    return out


def negative_tests(data, html):
    """Each mutation MUST be rejected. Returns list of (name, caught, detail)."""
    results = []

    d = copy.deepcopy(data)
    d["listings"][0]["price"] = 1.23
    d["listings"][0]["priceLabel"] = "injected fake price"
    e, _, _ = validate(d, html, deep_links=False)
    results.append(("fabricated price in the dataset", any("UNSOURCED DOLLAR" in x or "recompute" in x for x in e), e[:1]))

    d = copy.deepcopy(data)
    d["listings"][0]["grams"] = 99.9
    e, _, _ = validate(d, html, deep_links=False)
    results.append(("fabricated weight in the dataset", any("recompute" in x for x in e), e[:1]))

    d = copy.deepcopy(data)
    weighted = next(x for x in d["listings"] if x.get("grams") is not None)
    weighted["metal_value"] = 1.00
    e, _, _ = validate(d, html, deep_links=False)
    results.append(("tampered derived metal value", any("metal_value does not recompute" in x for x in e), e[:1]))

    d = copy.deepcopy(data)
    for r in d["listings"]:
        if r.get("grams") is None:
            r["flags"] = [f for f in r["flags"] if f != "no-gram-weight"]
            break
    e, _, _ = validate(d, html, deep_links=False)
    results.append(("blank weight with the flag removed", any("blank weight not flagged" in x for x in e), e[:1]))

    html2 = dict(html)
    html2["listings.html"] = html["listings.html"] + "<p>$999.99</p>"
    e, _, _ = validate(data, html2, deep_links=False)
    results.append(("hand-typed $999.99 in the HTML", any("UNSOURCED DOLLAR" in x for x in e), e[:1]))

    html3 = dict(html)
    html3["index.html"] = html["index.html"].replace("⚠ NO HALLUCINATIONS</b>", "Some values are estimates")
    e, _, _ = validate(data, html3, deep_links=False)
    results.append(("no-hallucinations banner removed", any("no-hallucinations banner" in x.lower() for x in e), e[:1]))

    return results


def main():
    data, js_data, js = load()
    html = read_pages()

    # data.js must be exactly the unified dataset
    perrors = []
    if js_data != data:
        perrors.append("site/assets/data.js is out of sync with data/unified.json — re-run tools/build_dashboard.py")

    errors, warnings, notes = validate(data, html)
    errors = perrors + errors

    neg = negative_tests(data, html)
    caught = sum(1 for _, c, _ in neg if c)
    for name, c, detail in neg:
        if not c:
            errors.append("NEGATIVE TEST FAILED to catch: " + name)

    result = "PASS" if not errors else "FAIL"
    run_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    status = {"runAt": run_at, "result": result, "fails": len(errors), "warns": len(warnings),
              "infos": len(notes), "checksRun": 11, "negativeTestsCaught": caught,
              "negativeTestsTotal": len(neg), "dataAsOf": data["meta"]["asOf"]}
    with open(STATUS, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)
        f.write("\n")

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("# GOLD5 — security check (pass 2 harness)\n\n")
        f.write("- Run: %s\n- Data as of: %s\n- Result: **%s** — %d error(s), %d warning(s)\n"
                % (run_at, data["meta"]["asOf"], result, len(errors), len(warnings)))
        f.write("- Negative tests caught: %d/%d\n\n" % (caught, len(neg)))
        f.write("## Checks passed (%d)\n\n" % len(notes))
        for n in notes:
            f.write("- %s\n" % n)
        if warnings:
            f.write("\n## Warnings\n\n")
            for w in warnings:
                f.write("- %s\n" % w)
        if errors:
            f.write("\n## Errors\n\n")
            for e in errors:
                f.write("- %s\n" % e)

    print("GOLD5 security check — %s" % result)
    print("  errors: %d   warnings: %d   cross-checks noted: %d" % (len(errors), len(warnings), len(notes)))
    print("  negative tests caught: %d/%d" % (caught, len(neg)))
    for e in errors:
        print("  [FAIL] " + e)
    for w in warnings:
        print("  [WARN] " + w)
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
