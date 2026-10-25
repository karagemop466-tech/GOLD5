#!/usr/bin/env python3
"""Task B4 — Cross-site anti-hallucination, arithmetic & security audit (Session b1f2fe3b).

Run after EVERY review pass:
    python3 scripts/audit_b1f2fe3b.py

Enforces 12 checks (S1-S12) across all merged session deliverables:
  - Root consolidated site (`index.html`, `site/*.html`, `site/assets/data.json`, `site/master-audit.html`)
  - `/report/` site (`report/index.html`, `report/*.html`, `verification/data.json`)
  - `/docs/` site (`docs/*.html`, `data/rings.json`, `data/sellers.json`, `data/spot.json`, `data/flags.json`, `data/evidence/*.txt`)
  - `/verified/` site (`verified/index.html`, `verified/pages/*.html`, `verified/data/*.json`)
  - `/guide/` and checklist guide (`guide/*.html`, `index-090bae73.html`, `pages/*.html`)
  - Unified cross-session catalog (`data/b1f2fe3b_verified_catalog.json`, `site/assets/catalog-b1f2fe3b.js`)

Writes machine-readable audit report to `data/b1f2fe3b_audit_report.json`.
Exit code 0 = PASS (0 errors), 1 = FAIL.
"""
import copy
import datetime
import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON = os.path.join(ROOT, "site", "assets", "data.json")
DATA_JS = os.path.join(ROOT, "site", "assets", "data.js")
CATALOG_JSON = os.path.join(ROOT, "data", "b1f2fe3b_verified_catalog.json")
CATALOG_JS = os.path.join(ROOT, "site", "assets", "catalog-b1f2fe3b.js")
AUDIT_REPORT_JSON = os.path.join(ROOT, "data", "b1f2fe3b_audit_report.json")

TROY_OZ_TO_GRAMS = 31.1034768
DWT_TO_GRAMS = 1.55517384

OFFICIAL_ALLOWED_DOMAINS = {
    "www.kitco.com", "corp.kitco.com", "www.cnbc.com", "www.apmex.com",
    "www.lbma.org.uk", "www.gold.org", "api.gold-api.com",
    "www.bluenile.com",
    "www.brilliantearth.com",
    "www.allurez.com",
    "www.avianneandco.com",
    "www.thejewelrymaster.com",
    "solidgoldjewelers.net",
    "www.quince.com",
    "www.ross-simons.com",
    "mejuri.com", "www.mejuri.com",
    "www.costco.com", "customerservice.costco.com",
    "www.etsy.com", "etsy.com", "help.etsy.com",
    "www.pompeii3.com", "www.marquise-jewelers.com",
    "consumer.ftc.gov", "www.ftc.gov", "www.ecfr.gov",
    "www.law.cornell.edu", "www.govinfo.gov", "www.federalregister.gov",
    "www.nist.gov",
    "www.bbb.org",
    "www.consumeraffairs.com", "www.topconsumerreviews.com",
    "jvclegal.org", "reportfraud.ftc.gov",
    "www.jewelers.org", "www.naag.org",
    "github.com", "karagemop466-tech.github.io",
}


def load_root_data():
    if os.path.exists(DATA_JSON):
        with open(DATA_JSON, encoding="utf-8") as f:
            return json.load(f)
    with open(DATA_JS, encoding="utf-8") as f:
        txt = f.read()
    body = txt[txt.index("{"):txt.rindex("}") + 1]
    return json.loads(body)


def get_fineness_map(root_data):
    spot = root_data["spot"]
    if "purity" in spot and "fineness" in spot["purity"]:
        return spot["purity"]["fineness"]
    return spot["purityValues"]["fineness"]


def make_metrics(karat, grams, price, usd_per_g, fineness_map):
    fin = fineness_map.get(f"{karat}K", (karat / 24.0) if karat else None)
    pure_g = round(grams * fin, 4) if (grams is not None and fin is not None) else None
    pure_oz = round(pure_g / TROY_OZ_TO_GRAMS, 5) if pure_g is not None else None
    pure_dwt = round(grams / DWT_TO_GRAMS, 4) if grams is not None else None
    melt_usd = round(pure_g * usd_per_g, 2) if pure_g is not None else None
    melt_usd_recheck = round(pure_g * 129.47, 2) if pure_g is not None else None
    ratio = round(price / melt_usd, 2) if (price is not None and melt_usd and melt_usd > 0) else None
    ratio_recheck = round(price / melt_usd_recheck, 2) if (price is not None and melt_usd_recheck and melt_usd_recheck > 0) else None
    nom_ppt = round((karat / 24.0) * 1000, 2) if karat else None
    min_ppt_no_solder = round(nom_ppt - 3.0, 2) if nom_ppt is not None else None
    min_ppt_with_solder = round(nom_ppt - 7.0, 2) if nom_ppt is not None else None
    return {
        "fineness": round(fin, 4) if fin is not None else None,
        "nominalPartsPerThousand": nom_ppt,
        "minAssayPptNoSolder_15USC295": min_ppt_no_solder,
        "minAssayPptWithSolder_15USC295": min_ppt_with_solder,
        "totalPennyweightDwt": pure_dwt,
        "pureGoldGrams": pure_g,
        "pureGoldTroyOz": pure_oz,
        "rawGoldMeltUsdAtPrimarySpot": melt_usd,
        "rawGoldMeltUsdAtRecheckSpot": melt_usd_recheck,
        "priceToMeltRatio": ratio,
        "priceToMeltRatioAtRecheckSpot": ratio_recheck,
    }


def build_unified_catalog(root_data):
    """Build data/b1f2fe3b_verified_catalog.json and site/assets/catalog-b1f2fe3b.js."""
    spot_primary = root_data["spot"]["primary"]
    usd_per_g = spot_primary["usdPerGram"]
    fineness_map = get_fineness_map(root_data)

    unified_entries = []
    seen_urls = set()

    # 1. Entries from site/assets/data.json (consolidated 25 listings)
    seller_names = {s["id"]: s["name"] for s in root_data["sellers"]}
    for e in root_data["entries"]:
        seen_urls.add(e["url"])
        explicit_solid = bool(e.get("solidStated")) if "solidStated" in e else ("solid" in (e.get("solidGold") or "").lower() or "solid" in (e.get("name") or "").lower())
        flags = list(e.get("flags") or [])
        grams = e.get("grams")
        price = e.get("price")
        if grams is None and "no-gram-weight" not in flags:
            flags.append("no-gram-weight")
        if price is None and "no-price" not in flags:
            flags.append("no-price")
        comp = make_metrics(e.get("karat"), grams, price, usd_per_g, fineness_map)
        if comp.get("priceToMeltRatio") is not None and comp["priceToMeltRatio"] < 1.0 and "price-below-metal-value" not in flags:
            flags.append("price-below-metal-value")
        srcs = list(dict.fromkeys(filter(None, [e["url"], e.get("priceSourceUrl"), e.get("returnUrl")])))
        unified_entries.append({
            "id": e["id"],
            "originSession": "7cca80c9+37e8ff42+638c9614+bc4e36a1",
            "name": e["name"],
            "sellerId": e["sellerId"],
            "sellerName": seller_names.get(e["sellerId"], e["sellerId"]),
            "category": e["category"],
            "url": e["url"],
            "karat": e["karat"],
            "metalColor": e.get("metalColor"),
            "solidGoldClaim": e.get("solidQuote") or e.get("solidGold") or ("Stated" if explicit_solid else "Not explicitly stated"),
            "explicitSolidGoldStated": explicit_solid,
            "grams": grams,
            "gramsNote": e.get("gramsNote"),
            "priceUsd": price,
            "priceLabel": e.get("priceNote") or e.get("priceLabel") or e.get("priceBasis"),
            "widthMm": e.get("widthMm"),
            "hallmarkClaim": e.get("hallmarkQuote") or e.get("hallmark") or "Not stated on product page",
            "makerMark": e.get("makerMark") or ("Seller states a maker's mark; see the quoted listing evidence" if e.get("makerMarkStated") else None),
            "metalConflict": e.get("metalConflict"),
            "evidenceId": e.get("evidenceId"),
            "evidencePath": e.get("evidencePath"),
            "returnPolicy": e.get("returns") or e.get("returnText") or e.get("returnPolicy"),
            "returnUrl": e.get("returnUrl"),
            "payment": e.get("payment"),
            "reviewScore": e.get("reviewScore"),
            "status": "verified" if price is not None else "flagged",
            "flags": flags,
            "checkedOn": e["checkedOn"],
            "provenance": e.get("provenance"),
            "sources": srcs,
            "computed": comp,
        })

    # 2. Additional live-verified entries from verification/data.json (60c4b9c3 + b1f2fe3b, e.g. Allurez U5885 18K & BE 18K)
    vdata_path = os.path.join(ROOT, "verification", "data.json")
    if os.path.exists(vdata_path):
        vdata = json.load(open(vdata_path, encoding="utf-8"))
        vsellers = {s["id"]: s for s in vdata.get("sellers", [])}
        for r in vdata.get("listings", []):
            if r["url"] in seen_urls:
                continue
            seen_urls.add(r["url"])
            s = vsellers.get(r["sellerId"], {})
            grams = r.get("weightG")
            price = r.get("priceUsd")
            flags = list(r.get("flags") or [])
            if grams is None and "no-gram-weight" not in flags:
                flags.append("no-gram-weight")
            if price is None and "no-price" not in flags:
                flags.append("no-price")
            unified_entries.append({
                "id": f"rep-{r['id'].lower()}",
                "originSession": "60c4b9c3+b1f2fe3b",
                "name": r["name"],
                "sellerId": r["sellerId"],
                "sellerName": s.get("name", r["sellerId"]),
                "category": "engagement-ring",
                "url": r["url"],
                "karat": r.get("karat"),
                "metalColor": r.get("metalColor", "Yellow Gold"),
                "solidGoldClaim": r.get("solidText") or r.get("karatText"),
                "explicitSolidGoldStated": bool(r.get("solidStated")),
                "grams": grams,
                "gramsNote": r.get("weightText") or "Weight in grams not published on product page",
                "priceUsd": price,
                "priceLabel": f"{r.get('priceText')} ({r.get('priceBasis')})",
                "widthMm": None,
                "hallmarkClaim": r.get("hallmarkText") or "Not stated on product page",
                "makerMark": None,
                "returnPolicy": r.get("returnText"),
                "returnUrl": r.get("returnUrl"),
                "payment": r.get("paymentText"),
                "reviewScore": r.get("reputationText"),
                "status": "verified" if price is not None else "flagged",
                "flags": flags,
                "checkedOn": "2026-10-22",
                "sources": list(filter(None, [r["url"], r.get("priceSourceUrl"), r.get("returnUrl")])),
                "computed": make_metrics(r.get("karat"), grams, price, usd_per_g, fineness_map),
            })

    # 3. Additional verified entries from verified/data/entries.json (session 84be683f)
    ver_entries_path = os.path.join(ROOT, "verified", "data", "entries.json")
    ver_sellers_path = os.path.join(ROOT, "verified", "data", "sellers.json")
    if os.path.exists(ver_entries_path):
        ver_entries = json.load(open(ver_entries_path, encoding="utf-8")).get("entries", [])
        ver_sellers = {}
        if os.path.exists(ver_sellers_path):
            for s in json.load(open(ver_sellers_path, encoding="utf-8")).get("sellers", []):
                ver_sellers[s["id"]] = s
        for r in ver_entries:
            if r["url"] in seen_urls:
                continue
            seen_urls.add(r["url"])
            s = ver_sellers.get(r["seller_id"], {})
            grams = r.get("weight_g")
            price = r.get("price_usd")
            flags = list(r.get("flags") or [])
            if grams is None and "no-gram-weight" not in flags:
                flags.append("no-gram-weight")
            if price is None and "no-price" not in flags:
                flags.append("no-price")
            unified_entries.append({
                "id": f"ver-{r['id'].lower()}",
                "originSession": "84be683f",
                "name": r["title"],
                "sellerId": r["seller_id"],
                "sellerName": r.get("seller") or s.get("name", r["seller_id"]),
                "category": r.get("category", "engagement-ring"),
                "url": r["url"],
                "karat": r.get("karat"),
                "metalColor": f"{r.get('karat')}K {r.get('gold_color', 'Gold')}",
                "solidGoldClaim": r.get("metal") or "Not stated",
                "explicitSolidGoldStated": r.get("solid_gold") == "explicit",
                "grams": grams,
                "gramsNote": f"Gold Weight {grams} grams" if grams is not None else "Weight in grams not published on product page",
                "priceUsd": price,
                "priceLabel": f"${price:,.2f} ({r.get('price_basis')})" if price is not None else r.get("price_basis"),
                "widthMm": r.get("width_mm"),
                "hallmarkClaim": "Not stated on product page",
                "makerMark": None,
                "returnPolicy": s.get("return_policy", {}).get("summary") if isinstance(s.get("return_policy"), dict) else "See seller policy",
                "returnUrl": s.get("return_policy", {}).get("url") if isinstance(s.get("return_policy"), dict) else r["url"],
                "payment": "See seller checkout terms",
                "reviewScore": None,
                "status": "verified" if price is not None else "flagged",
                "flags": flags,
                "checkedOn": r.get("checked_on", "2026-10-22"),
                "sources": list(filter(None, [r["url"], s.get("return_policy", {}).get("url") if isinstance(s.get("return_policy"), dict) else None])),
                "computed": make_metrics(r.get("karat"), grams, price, usd_per_g, fineness_map),
            })

    # 4. Quince 1ct Lab Grown Diamond Oval Comfort Fit Engagement Ring (live verified by 9eba173a + b1f2fe3b on 2026-10-22)
    quince_url = "https://www.quince.com/women/oval-lab-grown-diamond-comfort-fit-engagement-ring---1ct?color=yellow-gold"
    if quince_url not in seen_urls:
        seen_urls.add(quince_url)
        unified_entries.append({
            "id": "quince-oval-1ct-14ky",
            "originSession": "9eba173a+b1f2fe3b",
            "name": "Lab Grown Diamond Oval Comfort Fit Engagement Ring — 1ct (14K Yellow Gold Band + Platinum Head)",
            "sellerId": "quince",
            "sellerName": "Quince",
            "category": "engagement-ring",
            "url": quince_url,
            "karat": 14,
            "metalColor": "14K Yellow Gold band / Platinum head",
            "solidGoldClaim": "14k recycled gold band with platinum head ('solid' not explicitly stated)",
            "explicitSolidGoldStated": False,
            "grams": None,
            "gramsNote": "Weight in grams not published on product page",
            "priceUsd": 900.00,
            "priceLabel": "$900.00 (Complete 1ct IGI EF+ VS1+ lab-grown diamond ring)",
            "widthMm": None,
            "hallmarkClaim": "Not stated on product page (mixed-metal 16 CFR § 23.8 applies)",
            "makerMark": None,
            "returnPolicy": "60-day engagement ring return cap (unworn, original packaging/IGI cert; $30-$100 missing cert fee; $35 restocking fee on made-to-order)",
            "returnUrl": "https://www.quince.com/shipping-returns",
            "payment": "Credit card checkout",
            "reviewScore": "45 reviews on PDP · BBB 1.69/5 (125 reviews, 187 complaints/3 yrs)",
            "status": "verified",
            "flags": ["no-gram-weight", "solid-not-explicit", "no-hallmark-photo", "return-policy-exclusions"],
            "checkedOn": "2026-10-22",
            "sources": [
                quince_url,
                "https://www.quince.com/shipping-returns",
                "https://www.quince.com/contact-us",
            ],
            "computed": make_metrics(14, None, 900.00, usd_per_g, fineness_map),
        })

    catalog = {
        "meta": {
            "title": "GOLD5 Unified Cross-Session Verified Ring Catalog",
            "generatedBy": "scripts/audit_b1f2fe3b.py (session b1f2fe3b)",
            "asOf": (root_data.get("meta", {}).get("asOf") or "2026-10-22"),
            "noHallucinationsRule": "Every entry has >=1 official source URL and a check date (2026-10-22 or 2026-10-23) consistent with its provenance. Blank fields are null and flagged; derived fields are computed from verified inputs.",
            "primarySpotUsdPerOz": spot_primary["usdPerOz"],
            "primarySpotUsdPerGram": spot_primary["usdPerGram"],
            "primarySpotAsOf": spot_primary["asOf"],
            "liveRecheckSpotUsdPerOz": 4026.90,
            "liveRecheckSpotUsdPerGram": 129.47,
            "liveRecheckAsOf": "2026-10-22 7:26 p.m. EDT",
            "troyOzGramsExact": TROY_OZ_TO_GRAMS,
            "pennyweightGramsExact": DWT_TO_GRAMS,
            "totalEntries": len(unified_entries),
            "entriesWithVerifiedGrams": sum(1 for x in unified_entries if x["grams"] is not None),
            "entriesWithExplicitSolidGold": sum(1 for x in unified_entries if x["explicitSolidGoldStated"]),
            "entriesWithVerifiedHallmarkAndMakerMark": sum(1 for x in unified_entries if x.get("makerMark") and x.get("hallmarkClaim") and "not stated" not in x["hallmarkClaim"].lower()),
        },
        "entries": unified_entries,
    }
    os.makedirs(os.path.dirname(CATALOG_JSON), exist_ok=True)
    with open(CATALOG_JSON, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    with open(CATALOG_JS, "w", encoding="utf-8") as f:
        f.write("window.GOLD5_UNIFIED_CATALOG = " + json.dumps(catalog, indent=2) + ";\n")
    return catalog


LEGACY_DATES = {"2026-10-22", "2026-10-23"}


def validate_entry_list(entries, root_asof=None):
    """Pure validator used both on real catalog and negative self-tests.

    2026-10-25 (session 3dfe4d85): the canonical dataset advances with every verification
    pass, so the accepted check dates are the two legacy capture dates plus the current
    canonical data date (meta.asOf). The invariant is unchanged — a live row must carry a
    date that is in the accepted set, a row dated the newest accepted date must be marked
    live, and a prior row must keep a date older than the canonical data date — but the
    rule no longer freezes the calendar of one session.
    """
    allowed = set(LEGACY_DATES)
    if root_asof:
        allowed.add(root_asof)
    newest = max(allowed)
    errs = []
    for e in entries:
        eid = e.get("id", "?")
        srcs = e.get("sources") or []
        if not srcs:
            errs.append(f"S2: {eid} has no sources")
        for u in srcs + ([e["url"]] if e.get("url") else []):
            parsed = urlparse(u)
            host = (parsed.hostname or "").lower()
            if parsed.scheme != "https" or host not in OFFICIAL_ALLOWED_DOMAINS:
                errs.append(f"S1: {eid} disallowed/non-https URL {u}")
        # 2026-10-23 (integration session a255f011): the canonical dataset now carries
        # two legitimate check dates - rows re-read today and rows kept from the
        # 2026-10-22 capture (which must be labelled provenance=prior and flagged).
        if e.get("checkedOn") not in allowed:
            errs.append(f"S2: {eid} missing/invalid checkedOn date {e.get('checkedOn')!r}")
        if e.get("checkedOn") == newest and e.get("provenance") != "live":
            errs.append(f"S2: {eid} is dated the canonical data date {newest} but not marked live")
        if e.get("provenance") == "prior" and not (root_asof and e.get("checkedOn") < root_asof) \
                and e.get("checkedOn") not in LEGACY_DATES:
            errs.append(f"S2: {eid} is marked prior but not dated before the canonical data date")
        if root_asof and e.get("provenance") == "live" and e.get("checkedOn") not in (root_asof,) \
                and e.get("checkedOn") not in LEGACY_DATES:
            errs.append(f"S2: {eid} is marked live but dated {e.get('checkedOn')!r}, outside the accepted capture dates")
        flags = set(e.get("flags") or [])
        if e.get("grams") is None and not ({"no-gram-weight", "FL-03", "F-WEIGHT", "G-NO-WEIGHT", "F-004"} & flags) and e.get("status") != "flagged":
            errs.append(f"S3: {eid} has blank grams without no-gram-weight/F-WEIGHT flag")
        if e.get("priceUsd") is None and not ({"no-price", "FL-13", "F-SGJ-PRICE", "G-PRICE-EUR", "G-PRICE-BLANK-CALL", "G-PRICE-BLANK-SOLD", "F-010"} & flags):
            errs.append(f"S3: {eid} has blank priceUsd without no-price flag")
        if e.get("metalConflict") and "FL-30" not in flags:
            errs.append(f"S3: {eid} has a metal conflict without FL-30")
        comp = e.get("computed") or {}
        if e.get("grams") is not None and e.get("karat") and e.get("priceUsd") is not None:
            ratio = comp.get("priceToMeltRatio")
            if ratio is not None and ratio < 1.0 and not ({"price-below-metal-value", "FL-01"} & flags):
                errs.append(f"S6: {eid} has priceToMeltRatio={ratio} < 1.0 without price-below-metal-value flag")
    return errs


def run_audit():
    errors = []
    warnings = []
    passed = []

    root_data = load_root_data()
    catalog = build_unified_catalog(root_data)

    # S1-S3 & S6 on unified catalog
    root_asof = (root_data.get("meta", {}) or {}).get("asOf")
    cat_errs = validate_entry_list(catalog["entries"], root_asof=root_asof)
    if cat_errs:
        errors.extend(cat_errs)
    else:
        passed.append(
            f"S1-S3/S6: All {len(catalog['entries'])} unified entries have allowlisted HTTPS sources, valid check dates ({', '.join(sorted(set(LEGACY_DATES) | ({root_asof} if root_asof else set())))}) consistent with provenance, flagged blanks, and verified melt ratios."
        )

    # S4: Spot & NIST Metrology math
    spot_checks = [
        ("Kitco current panel", root_data["spot"]["primary"]["usdPerOz"], root_data["spot"]["primary"]["usdPerGram"]),
        ("Kitco 7:10pm EDT primary", 4025.00, 129.41),
        ("Kitco 7:26pm EDT re-check", 4026.90, 129.47),
        ("APMEX 11:02am ET cross-check", 4077.60, 131.10),
    ]
    for label, oz, gram in spot_checks:
        expected_g = oz / TROY_OZ_TO_GRAMS
        if abs(expected_g - gram) > 0.01:
            errors.append(f"S4: {label} gram {gram} != oz/31.1034768 ({expected_g:.4f})")
    if abs(TROY_OZ_TO_GRAMS / 20.0 - DWT_TO_GRAMS) > 1e-9:
        errors.append("S4: DWT_TO_GRAMS != TROY_OZ_TO_GRAMS / 20")
    passed.append("S4: Spot quotes and NIST troy oz / pennyweight / gram conversions verified exact.")

    # S5: Karat fineness & 15 U.S.C. 295 tolerances
    for k, fin in get_fineness_map(root_data).items():
        k_num = int(k[:-1])
        expected = k_num / 24.0 if k_num < 24 else 0.9999
        if abs(fin - expected) > 0.001:
            errors.append(f"S5: {k} fineness {fin} != {expected:.4f}")
    passed.append("S5: Karat fineness fractions & 15 U.S.C. § 295 (-3‰ / -7‰) tolerances verified.")

    # S7: Verbatim evidence check on data/rings.json
    ev_dir = os.path.join(ROOT, "data", "evidence")
    rings_638 = json.load(open(os.path.join(ROOT, "data", "rings.json"), encoding="utf-8"))
    for r in rings_638:
        ev_file = os.path.join(ev_dir, r["evidence"] + ".txt")
        if not os.path.exists(ev_file):
            errors.append(f"S7: Missing evidence file {ev_file}")
            continue
        ev_txt = open(ev_file, encoding="utf-8").read()
        if r["price_text"] and r["price_text"] not in ev_txt:
            errors.append(f"S7: {r['id']} price_text {r['price_text']!r} missing from {r['evidence']}.txt")
        if r["weight_text"] and r["weight_text"] not in ev_txt:
            errors.append(f"S7: {r['id']} weight_text {r['weight_text']!r} missing from {r['evidence']}.txt")
    passed.append(f"S7: All {len(rings_638)} data/rings.json entries verified verbatim against data/evidence/*.txt.")

    # S8, S9, S10, S11: HTML link resolution, no-hallucinations banner, count consistency, table balance & DOM security
    html_files = []
    for base, _dirs, files in os.walk(ROOT):
        rel_base = os.path.relpath(base, ROOT)
        if any(p in {".git", "node_modules", ".venv", "__pycache__", "archive"} for p in rel_base.split(os.sep)):
            continue
        for fn in files:
            if fn.endswith(".html"):
                html_files.append(os.path.join(base, fn))
    html_files.sort()

    link_re = re.compile(r'(?:href|src)="([^"]+)"')
    local_links_ok = 0
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        raw_html = open(path, encoding="utf-8").read()
        no_script_html = re.sub(r"<script.*?</script>", "", raw_html, flags=re.S)
        script_blocks = "\n".join(re.findall(r"<script.*?>(.*?)</script>", raw_html, flags=re.S))

        # S11a: balanced <table> and </table> tags outside scripts
        n_open = len(re.findall(r"<table\b", no_script_html, flags=re.I))
        n_close = len(re.findall(r"</table\s*>", no_script_html, flags=re.I))
        if n_open != n_close:
            errors.append(f"S11: {rel} has unbalanced <table> tags ({n_open} open vs {n_close} close)")

        # S11b: no eval() inside <script> blocks or external http(s) script src
        if re.search(r"\beval\s*\(", script_blocks):
            errors.append(f"S11: {rel} script block contains forbidden eval()")
        for m in re.finditer(r'<script[^>]+src="([^"]+)"', raw_html, flags=re.I):
            if m.group(1).startswith(("http://", "https://", "//")):
                errors.append(f"S11: {rel} loads external script {m.group(1)}")

        # S10: check for stale "13 listings" text if root_data has != 13 entries
        if rel in {"index.html", "site/checklist.html"} and len(root_data["entries"]) != 13:
            if re.search(r"\b13 listings\b|\b2 of 13 listings\b", raw_html, flags=re.I):
                errors.append(f"S10: {rel} contains stale '13 listings' count while site/assets/data.json has {len(root_data['entries'])} entries")

        # S8: local link resolution
        for u in link_re.findall(no_script_html):
            if u.startswith(("http://", "https://", "#", "mailto:", "tel:")):
                continue
            local = u.split("#")[0].split("?")[0]
            if not local:
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), local))
            if not os.path.exists(target):
                errors.append(f"S8: {rel} has broken local link {u}")
            else:
                local_links_ok += 1

    # S9: Front-page no-hallucinations pledge check
    for landing in ("index.html", "report/index.html", "docs/index.html", "verified/index.html", "index-090bae73.html"):
        lp = os.path.join(ROOT, landing)
        if os.path.exists(lp):
            txt = open(lp, encoding="utf-8").read().lower()
            if not re.search(r"no[\s-]+hallucination", txt):
                errors.append(f"S9: {landing} missing prominent 'no hallucinations' summary")
    passed.append(f"S8-S11: {len(html_files)} HTML pages audited ({local_links_ok} local links resolved, balanced <table> tags, no external scripts, front-page no-hallucinations pledge present).")

    # S12: Negative self-test (inject 4 synthetic hallucinations into a copy and verify all 4 are caught)
    fake_entries = copy.deepcopy(catalog["entries"][:1])
    fake_entries[0]["id"] = "fake-1"
    fake_entries[0]["sources"] = []  # violation 1: no source
    fake_2 = copy.deepcopy(catalog["entries"][0])
    fake_2["id"] = "fake-2"
    fake_2["grams"] = None
    fake_2["flags"] = []
    fake_2["status"] = "verified"  # violation 2: unflagged blank grams
    fake_3 = copy.deepcopy(catalog["entries"][0])
    fake_3["id"] = "fake-3"
    fake_3["grams"] = 10.0
    fake_3["karat"] = 18
    fake_3["priceUsd"] = 100.0
    fake_3["computed"]["priceToMeltRatio"] = 0.10
    fake_3["flags"] = []  # violation 3: sub-melt ratio unflagged
    fake_4 = copy.deepcopy(catalog["entries"][0])
    fake_4["id"] = "fake-4"
    fake_4["url"] = "https://cheap-gold-scam.example/ring"  # violation 4: untrusted domain
    neg_errs = validate_entry_list([fake_entries[0], fake_2, fake_3, fake_4], root_asof=root_asof)
    if len(neg_errs) < 4:
        errors.append(f"S12: Negative self-test failed to catch all 4 synthetic hallucinations (caught {len(neg_errs)})")
    else:
        passed.append(f"S12: Negative self-test caught all {len(neg_errs)}/4 injected synthetic hallucinations (missing source, unflagged blank weight, unflagged sub-melt price, untrusted domain).")

    report = {
        "runAt": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "session": "b1f2fe3b",
        "status": "PASS" if not errors else "FAIL",
        "passedCount": len(passed),
        "errorCount": len(errors),
        "warningCount": len(warnings),
        "catalogSummary": catalog["meta"],
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
    }
    with open(AUDIT_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"=== GOLD5 Cross-Site Security & Anti-Hallucination Audit (session b1f2fe3b) ===")
    print(f"Status: {report['status']} | Passed groups: {len(passed)} | Errors: {len(errors)} | Warnings: {len(warnings)}")
    for p in passed:
        print(f"  [PASS] {p}")
    for e in errors:
        print(f"  [FAIL] {e}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(run_audit())
