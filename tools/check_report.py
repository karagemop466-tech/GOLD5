#!/usr/bin/env python3
"""GOLD5 report checker — the no-hallucination gate for the dashboard in report/ + index.html.

Checks
  1  dataset schema + required fields
  2  EVIDENCE MATCH: every recorded value must appear verbatim in the saved capture of its page
     (a token), so a number cannot exist in the data without being on the page
  3  every seller URL / reference URL is on an allowlisted official domain
  4  spot arithmetic (oz <-> g, purity table) recomputed from the published figures
  5  DERIVED VALUES recomputed (fine gold, metal value, troy oz, price/g) and required to be
     present in the rendered HTML
  6  MONEY AUDIT: every $ or EUR amount rendered in HTML must trace to a data price, a reference
     quote, or a recomputed value — a hand-typed price fails the build
  7  link integrity: every local href/src and anchor resolves
  8  flag cross-references (flag -> listing, listing -> flag) resolve
  9  required disclosure text present on every page
 10  pass log: every recorded pass marked rendered appears on the Method page

Exit 0 = clean. Writes verification/passes.json. `--record` appends this run as a new pass.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "verification", "data.json")
EVID = os.path.join(ROOT, "verification", "evidence")
PASSES = os.path.join(ROOT, "verification", "passes.json")
TROY = 31.1034768
FINE = {10: 10 / 24, 14: 14 / 24, 18: 18 / 24, 22: 22 / 24, 24: 1.0}

ALLOWED = {
    "www.kitco.com", "corp.kitco.com",
    "www.bluenile.com", "www.brilliantearth.com", "www.allurez.com", "www.avianneandco.com",
    "www.thejewelrymaster.com", "solidgoldjewelers.net",
    "www.etsy.com", "etsy.com", "help.etsy.com",
    "consumer.ftc.gov", "www.ftc.gov", "www.ecfr.gov", "www.law.cornell.edu", "reportfraud.ftc.gov",
    "www.bbb.org", "jvclegal.org",
    "www.google.com",  # seller-complaint search links (manual review), never a data value
    "github.com",
}

FAIL, WARN, INFO, OK = [], [], [], []
checks = 0


def fail(m):
    FAIL.append(m)


def warn(m):
    WARN.append(m)


def info(m):
    INFO.append(m)


def ok(m):
    OK.append(m)


def count(n=1):
    global checks
    checks += n



def nums_in(txt):
    return {round(float(re.sub(r"[$€,\s]", "", m)), 2)
            for m in re.findall(r"[$€]\s?[\d][\d,]*(?:\.\d+)?", txt or "")}


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def fmt(x, dp=2):
    return "{:,.{}f}".format(x, dp)


def money(x, dp=2):
    return "$" + fmt(x, dp)


def read_evidence(name):
    for base in (EVID, ROOT):
        p = os.path.join(base, name)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return f.read()
    return None


def host_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1).lower() if m else None


# --------------------------------------------------------------------------- 1. schema
def check_schema(d):
    for k in ("meta", "spot", "listings", "sellers", "references", "flags"):
        count()
        if k not in d:
            fail(f"data.json missing top-level key '{k}'")
    req = ("id", "sellerId", "name", "url", "provenance", "checkedOn", "evidence", "priceUsd",
           "priceText", "karat", "weightG", "solidStated", "hallmarkStated", "flags")
    ids = set()
    for r in d["listings"]:
        count(len(req))
        for k in req:
            if k not in r:
                fail(f"{r.get('id','?')}: missing field '{k}'")
        if r["id"] in ids:
            fail(f"duplicate listing id {r['id']}")
        ids.add(r["id"])
        if r["provenance"] not in ("A", "B"):
            fail(f"{r['id']}: provenance must be A or B")
        if r["sellerId"] not in {s["id"] for s in d["sellers"]}:
            fail(f"{r['id']}: unknown sellerId {r['sellerId']}")
        # blank-is-blank rule: a blank weight must never be 0
        if r["weightG"] is not None and not isinstance(r["weightG"], (int, float)):
            fail(f"{r['id']}: weightG is not numeric or null")
        if isinstance(r["weightG"], (int, float)) and r["weightG"] <= 0:
            fail(f"{r['id']}: weightG <= 0")
        if isinstance(r["priceUsd"], (int, float)) and r["priceUsd"] <= 0:
            fail(f"{r['id']}: priceUsd <= 0")
    ok(f"schema: {len(d['listings'])} listings, fields present")


# --------------------------------------------------------------------------- 2. evidence match
def check_evidence(d):
    for r in d["listings"]:
        count()
        text = read_evidence(r["evidence"])
        if text is None:
            fail(f"{r['id']}: evidence file not found: {r['evidence']}")
            continue
        for extra in r.get("evidenceExtra", []):
            t2 = read_evidence(extra)
            if t2 is None:
                fail(f"{r['id']}: extra evidence file not found: {extra}")
            else:
                text += "\n" + t2
        toks = r.get("tokens") or []
        if not toks:
            fail(f"{r['id']}: no evidence tokens")
            continue
        for t in toks:
            count()
            if t not in text:
                fail(f"{r['id']}: token not found verbatim in {r['evidence']}: {t!r}")
        # the price must be traceable to a token
        if r["priceUsd"] is not None:
            count()
            p1, p2 = fmt(r["priceUsd"], 2), fmt(r["priceUsd"], 0)
            if not any(p1 in t or p2 in t for t in toks):
                fail(f"{r['id']}: price {r['priceUsd']} has no token containing it")
            if r["priceUsd"] and (r["priceUsd"] > 50000):
                warn(f"{r['id']}: unusually large price, double-check")
        # the weight must be traceable to a token
        if r["weightG"] is not None:
            count()
            w = "{:g}".format(r["weightG"])
            if not any(w in t for t in toks):
                fail(f"{r['id']}: weight {r['weightG']} has no token containing {w!r}")
        # any amount written in the row's own prose must also be on the captured page
        page_nums = nums_in(text)
        prose = " ".join(str(r.get(k) or "") for k in
                         ("priceText", "priceBasis", "weightText", "solidText", "hallmarkText",
                          "returnText", "paymentText", "reputationText", "name"))
        for v in sorted(nums_in(prose)):
            count()
            if v in page_nums:
                continue
            literal = "{:,.2f}".format(v)
            literal0 = "{:,.0f}".format(v)
            if literal in text or literal0 in text:
                continue
            fail(f"{r['id']}: prose mentions an amount not on the captured page ({v:,.2f})")
        # a 'solid' claim must be quoted somewhere
        if r["solidStated"]:
            count()
            if not any("solid" in t.lower() for t in toks) and "solid" not in (r.get("solidText") or "").lower():
                fail(f"{r['id']}: solidStated=True but no solid-gold claim recorded")
    ok("evidence: every token found verbatim in its capture")


# --------------------------------------------------------------------------- 3. domains
def check_domains(d):
    urls = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and o.startswith("http"):
            urls.append(o)

    walk(d)
    bad = set()
    for u in urls:
        count()
        h = host_of(u)
        if h not in ALLOWED:
            bad.add(u)
    for u in sorted(bad):
        fail(f"URL outside the official allowlist: {u}")
    if not bad:
        ok(f"domains: {len(urls)} URLs, all allowlisted")


# --------------------------------------------------------------------------- 4. spot
def check_spot(d):
    s = d["spot"]
    count(3)
    g_implied = s["bidUsdPerOz"] / TROY
    if abs(g_implied - s["usdPerGramUsed"]) / g_implied > 0.01:
        fail(f"spot: {s['bidUsdPerOz']}/oz implies {g_implied:.2f}/g but data says {s['usdPerGramUsed']}")
    if abs(s["usdPerGramToggle"] - s["bidUsdPerOz"] / TROY) / (s["bidUsdPerOz"] / TROY) > 0.01:
        fail("spot: published per-gram figure is inconsistent with the per-ounce figure by >1%")
    for k, v in s["purityPerOz"].items():
        count()
        exp = s["bidUsdPerOz"] * FINE[int(k)]
        if abs(v - exp) / exp > 0.005:
            fail(f"spot: {k}K per-ounce value {v} inconsistent with {s['bidUsdPerOz']}/oz "
                 f"(expected ≈{exp:.2f})")
    txt = read_evidence(s["evidence"]) or ""
    for t in s["tokens"]:
        count()
        if t not in txt:
            fail(f"spot: token not in evidence: {t!r}")
    if s["usdPerGramUsed"] > min(s["usdPerGramToggle"], s["usdPerGramTable"]):
        fail("spot: the gram figure used must be the lowest one published, so metal values stay conservative")
    ok("spot: oz↔g and per-karat table reconcile with the published figures")


# --------------------------------------------------------------------------- 5/6. derived + money audit
def derived(r, spot):
    if r["weightG"] is None or r["karat"] is None:
        return None
    fine = r["weightG"] * FINE[r["karat"]]
    melt = fine * spot
    return {"fine": fine, "melt": melt, "troy": r["weightG"] / TROY,
            "perFine": (r["priceUsd"] / fine) if r["priceUsd"] else None,
            "premium": (r["priceUsd"] / melt) if r["priceUsd"] else None}


def check_derived(d, html_pages):
    spot = d["spot"]["usdPerGramUsed"]
    pool = "\n".join(html_pages.values())
    computed = []
    for r in d["listings"]:
        dv = derived(r, spot)
        if not dv:
            continue
        computed.append(dv)
        count(3)
        if fmt(dv["fine"]) not in pool:
            fail(f"{r['id']}: computed fine gold {fmt(dv['fine'])} g missing from the site")
        if money(dv["melt"]) not in pool:
            fail(f"{r['id']}: computed metal value {money(dv['melt'])} missing from the site")
        if dv["premium"] and f'{dv["premium"]:.2f}×' not in pool:
            fail(f"{r['id']}: computed price/metal multiple {dv['premium']:.2f}x missing from the site")
    ok(f"derived: {len(computed)} computed rows re-derived and found in the HTML")

    # money audit
    allowed = set()

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            for m in re.findall(r"[$€]\s?[\d][\d,]*(?:\.\d+)?", o):
                allowed.add(re.sub(r"\s", "", m))
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            allowed.add(money(o))
            allowed.add(money(o, 0))

    walk(d)
    allowed |= {money(spot), money(spot, 0), money(d["spot"]["bidUsdPerOz"]),
                money(d["spot"]["askUsdPerOz"]), money(d["spot"]["usdPerOzTable"]),
                money(d["spot"]["usdPerOzWidget"])}
    for k, v in d["spot"]["purityPerOz"].items():
        allowed.add(money(v))
        allowed.add(money(v / TROY))
    allowed.add(money(d["spot"]["usdPerGramToggle"]))
    allowed.add(money(d["spot"]["usdPerGramTable"]))
    for r in d["listings"]:
        if r["weightG"] and r["priceUsd"]:
            allowed.add(money(r["priceUsd"] / r["weightG"]))
    for dv in computed:
        allowed |= {money(dv["melt"]), money(dv["troy"], 4)}
        if dv["perFine"]:
            allowed.add(money(dv["perFine"]))
    # worked example on the value page: price - metal value for A01
    # karat comparison delta quoted on the By-karat page (A04 price - A01 price)
    a = {r["id"]: r for r in d["listings"]}
    if a.get("A01") and a.get("A04") and a["A01"]["priceUsd"] and a["A04"]["priceUsd"]:
        allowed.add(money(a["A04"]["priceUsd"] - a["A01"]["priceUsd"]))
    a01 = next((r for r in d["listings"] if r["id"] == "A01"), None)
    if a01:
        dv = derived(a01, spot)
        allowed.add(money(a01["priceUsd"] - dv["melt"]))

    def num_of(tok):
        try:
            return round(float(re.sub(r"[$€,\s]", "", tok)), 2)
        except ValueError:
            return None

    allowed_nums = {num_of(a) for a in allowed if num_of(a) is not None}
    bad = []
    for name, page in html_pages.items():
        for m in re.findall(r"[$€]\s?[\d][\d,]*(?:\.\d+)?", page):
            count()
            if num_of(m) not in allowed_nums:
                bad.append((name, m))
    for name, tok in bad:
        fail(f"{name}: renders an amount that is not traceable to data ({tok})")
    if not bad:
        ok("money audit: every amount in the HTML traces to a source price or a recomputation")


def check_references(d):
    for r in d["references"]:
        count()
        if not r.get("evidence"):
            info(f"{r['id']}: no evidence file (quote not used as a data value)")
            continue
        txt = read_evidence(r["evidence"])
        if txt is None:
            fail(f"{r['id']}: reference evidence file missing: {r['evidence']}")
            continue
        def norm(x):
            x = re.sub(r"[*#`\\]", "", x)
            return re.sub(r"\s+", " ", x).strip()
        flat_t = norm(txt)
        for q in r["quotes"]:
            count()
            frag = re.split(r"\.\.\.|…", q)[0]
            frag = norm(frag)[:70]
            if frag and frag not in flat_t:
                fail(f"{r['id']}: quote fragment not found in {r['evidence']}: {frag!r}")
    ok("references: every quoted fragment found in its saved capture")


# --------------------------------------------------------------------------- 7. links
def check_links(html_pages, root):
    for name, page in html_pages.items():
        base = os.path.dirname(os.path.join(root, name))
        for href in re.findall(r'(?:href|src)="([^"]+)"', page):
            if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                if href.startswith("#"):
                    count()
                    anchor = href[1:]
                    if anchor and f'id="{anchor}"' not in page:
                        fail(f"{name}: dead in-page anchor #{anchor}")
                continue
            count()
            path, _, anchor = href.partition("#")
            target = os.path.normpath(os.path.join(base, path))
            if not os.path.exists(target):
                fail(f"{name}: broken local link {href}")
            elif anchor:
                with open(target, encoding="utf-8") as f:
                    if f'id="{anchor}"' not in f.read():
                        fail(f"{name}: link to missing anchor {href}")
    ok("links: all local hrefs/srcs and anchors resolve")


# --------------------------------------------------------------------------- 8. flags
def check_flags(d):
    fids = set()
    lids = {r["id"] for r in d["listings"]}
    for f in d["flags"]:
        count(3)
        if f["id"] in fids:
            fail(f"duplicate flag id {f['id']}")
        fids.add(f["id"])
        if f["severity"] not in ("high", "medium", "low"):
            fail(f"{f['id']}: bad severity")
        if not f.get("sources"):
            fail(f"{f['id']}: flag has no source link")
        for i in f.get("listingIds", []):
            if i not in lids:
                fail(f"{f['id']}: mentions unknown listing {i}")
    for r in d["listings"]:
        count(len(r["flags"]))
        for fid in r["flags"]:
            if fid not in fids:
                fail(f"{r['id']}: references unknown flag {fid}")
    if not any(r["weightG"] is None for r in d["listings"]) is False:
        count()
        if "G-NO-WEIGHT" not in fids:
            fail("rows have blank weights but G-NO-WEIGHT is not published")
    ok(f"flags: {len(fids)} flags cross-referenced in both directions")


def check_flag_amounts(d):
    corpus = ""
    for folder in (EVID, os.path.join(ROOT, "data", "evidence"), os.path.join(ROOT, "docs", "verification")):
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if name.endswith((".txt", ".md")):
                with open(os.path.join(folder, name), encoding="utf-8") as f:
                    corpus += "\n" + f.read()
    corpus_nums = nums_in(corpus)
    for f in d["flags"]:
        for v in sorted(nums_in(f.get("detail", "") + " " + f.get("title", ""))):
            count()
            if v in corpus_nums:
                continue
            if "{:,.2f}".format(v) in corpus or "{:,.0f}".format(v) in corpus:
                continue
            fail(f"{f['id']}: flag text quotes an amount with no capture behind it ({v:,.2f})")
    ok("flags: every amount quoted in a flag is documented in the evidence corpus")


# --------------------------------------------------------------------------- 9. disclosure
def check_disclosure(html_pages):
    for name, page in html_pages.items():
        count(2)
        if "No hallucinations" not in page and "no hallucinations" not in page:
            fail(f"{name}: missing the no-hallucinations disclosure")
        if "../" in page and "GOLD5" not in page:
            fail(f"{name}: missing branding")
    ok("disclosure: every page carries the no-hallucinations notice")


# --------------------------------------------------------------------------- 10. pass log
def check_passes(d, html_pages, root):
    if not os.path.exists(PASSES):
        info("no pass log yet")
        return
    with open(PASSES, encoding="utf-8") as f:
        pl = json.load(f)
    page = html_pages.get("report/method.html", "")
    for p in pl["passes"]:
        if p.get("rendered"):
            count()
            if f'<td>{p["n"]}</td>' not in page:
                fail(f"pass #{p['n']} is marked rendered but is not on the Method page")
    ok(f"pass log: {len(pl['passes'])} pass(es) recorded")


def main():
    record = "--record" in sys.argv
    d = load()
    pages = {}
    for rel in ["index.html"] + [f"report/{n}.html" for n in
                                 ("listings", "karat", "value", "sellers", "checklist",
                                  "flagged", "sources", "method")]:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            fail(f"missing page {rel}")
            continue
        with open(p, encoding="utf-8") as f:
            pages[rel] = f.read()

    check_schema(d)
    check_evidence(d)
    check_domains(d)
    check_spot(d)
    check_derived(d, pages)
    check_references(d)
    check_links(pages, ROOT)
    check_flags(d)
    check_flag_amounts(d)
    check_disclosure(pages)
    check_passes(d, pages, ROOT)

    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if record:
        pl = {"passes": []}
        if os.path.exists(PASSES):
            with open(PASSES, encoding="utf-8") as f:
                pl = json.load(f)
        pl["passes"].append({
            "n": len(pl["passes"]) + 1,
            "when": when,
            "what": "full pass: evidence match, spot, derived, money audit, links, flags",
            "checks": checks,
            "fail": len(FAIL),
            "warn": len(WARN),
            "note": "records only; build again to render this pass on the Method page",
            "rendered": False,
        })
        os.makedirs(os.path.dirname(PASSES), exist_ok=True)
        with open(PASSES, "w", encoding="utf-8") as f:
            json.dump(pl, f, indent=1)

    print(f"\nGOLD5 report check — {when}")
    print(f"checks run: {checks}   FAIL: {len(FAIL)}   WARN: {len(WARN)}   INFO: {len(INFO)}")
    for m in FAIL[:40]:
        print("  FAIL:", m)
    for m in WARN[:20]:
        print("  WARN:", m)
    for m in INFO[:10]:
        print("  INFO:", m)
    for m in OK[-6:]:
        print("  ok:", m)
    print("\nRESULT:", "PASS" if not FAIL else "FAIL")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
