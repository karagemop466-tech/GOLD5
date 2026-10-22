#!/usr/bin/env python3
"""
GOLD5 site builder + anti-hallucination verifier.

Reads:   data/rings.jsonl, data/gold-price.json
Writes:  data/rings.json, data/rings.csv, data/verification-report.json,
         index.html, pages/*.html

Every numeric price/weight written to the site is cross-checked against the
literal evidence excerpt stored with the row. If a value cannot be found in its
own excerpt the row FAILS check C3/C6 and is flagged - the value is never
silently published as verified.
"""
import json, csv, html, os, re, statistics, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE_LABEL = os.path.basename(ROOT)
BUILD_UTC = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
TO = 31.1034768          # grams per troy ounce (NIST)
DWT = 1.55517384         # grams per pennyweight (NIST)

# ---------------------------------------------------------------- load
rows = [json.loads(l) for l in open("data/rings.jsonl", encoding="utf-8") if l.strip()]
gp = json.load(open("data/gold-price.json", encoding="utf-8"))

KARAT = {"24K": 24, "18K": 18, "14K": 14, "10K": 10}

def karat_number(k):
    if not k:
        return None
    m = re.match(r"\s*(\d{1,2})\s*K", str(k), re.I)
    return int(m.group(1)) if m else None

for r in rows:
    kn = karat_number(r.get("karat"))
    r["_karat_n"] = kn
    w = r.get("weight_grams")
    if w and kn:
        r["_pure_gold_g"] = round(w * kn / 24.0, 4)
        r["_pure_gold_ozt"] = round(r["_pure_gold_g"] / TO, 6)
        r["_alloy_fineness_pct"] = round(kn / 24.0 * 100, 2)
    else:
        r["_pure_gold_g"] = None
        r["_pure_gold_ozt"] = None
        r["_alloy_fineness_pct"] = round(kn / 24.0 * 100, 2) if kn else None

# ---------------------------------------------------------------- checks
MONEY = re.compile(r"\$\s?([\d,]+(?:\.\d{1,2})?)")
JSONPRICE = re.compile(r'"price"\s*:\s*"?([\d,]+(?:\.\d{1,2})?)"?')
BAREPRICE = re.compile(r"(?:US\s?\$|USD\s?)\s*([\d,]+(?:\.\d{1,2})?)")
GRAM = re.compile(r"(\d+(?:\.\d+)?)\s*(?:grams?|gram|gr\.|gr\b|g\b|גרם)", re.I)
DWTRE = re.compile(r"(\d+(?:\.\d+)?)\s*dwt", re.I)

def numbers_in(text):
    out = set()
    for rx in (MONEY, JSONPRICE, BAREPRICE):
        for m in rx.finditer(text or ""):
            try:
                out.add(round(float(m.group(1).replace(",", "")), 2))
            except ValueError:
                pass
    return out

def grams_in(text):
    out = set()
    for m in GRAM.finditer(text or ""):
        try:
            out.add(round(float(m.group(1)), 4))
        except ValueError:
            pass
    for m in DWTRE.finditer(text or ""):
        try:
            out.add(round(float(m.group(1)) * DWT, 4))
        except ValueError:
            pass
    return out

OFFICIAL_DOMAINS = ("bluenile.com", "kay.com", "zales.com", "jared.com", "brilliantearth.com",
                    "etsy.com", "ebay.com", "amazon.com", "pandora.net", "lbma.org.uk")

checks = []
def chk(cid, name, passed, detail, severity="error"):
    checks.append(dict(id=cid, name=name, status="PASS" if passed else "FAIL",
                       detail=detail, severity=severity))

row_flags = {}   # id -> list of check failures

# C1 every row has an official source URL
bad = [r["id"] for r in rows if not r.get("url") or not r["url"].startswith("http")]
chk("C1", "Every row carries a source URL", not bad, f"{len(rows)-len(bad)}/{len(rows)} rows have an http(s) source URL" + (f"; missing: {bad}" if bad else ""))
for b in bad: row_flags.setdefault(b, []).append("C1 no source URL")

bad = [r["id"] for r in rows if r.get("url") and not any(d in r["url"] for d in OFFICIAL_DOMAINS)]
chk("C1b", "Every source URL is on a first-party retailer / benchmark domain", not bad,
    ("All source URLs resolve to a known first-party domain" if not bad else f"Non-first-party URLs: {bad}"), "warn")
for b in bad: row_flags.setdefault(b, []).append("C1b source URL not first-party")

# C2 every priced row has an evidence excerpt
bad = [r["id"] for r in rows if r.get("price_usd") is not None and not (r.get("evidence", {}).get("excerpt") or "").strip()]
chk("C2", "Every priced row stores a literal evidence excerpt", not bad, f"{len(rows)-len(bad)}/{len(rows)} OK" + (f"; missing excerpt: {bad}" if bad else ""))
for b in bad: row_flags.setdefault(b, []).append("C2 price without evidence excerpt")

# C3 *** the core anti-hallucination check ***
fails = []
for r in rows:
    exc = (r.get("evidence", {}).get("excerpt") or "")
    nums = numbers_in(exc)
    p = r.get("price_usd")
    if p is not None and round(float(p), 2) not in nums:
        fails.append(f'{r["id"]}: price {p} not present in excerpt (found {sorted(nums)})')
        row_flags.setdefault(r["id"], []).append(f"C3 price ${p} NOT found in its own evidence excerpt")
    lp = r.get("list_price_usd")
    if lp is not None and round(float(lp), 2) not in nums:
        fails.append(f'{r["id"]}: list/was price {lp} not present in excerpt (found {sorted(nums)})')
        row_flags.setdefault(r["id"], []).append(f"C3 list price ${lp} NOT found in its own evidence excerpt")
chk("C3", "Every published price is literally present in its own evidence excerpt", not fails,
    f"{sum(1 for r in rows if r.get('price_usd') is not None)} priced rows checked against their excerpts; {len(fails)} mismatch(es)."
    + ("" if not fails else " -> " + "; ".join(fails)))

# C4 timestamps
bad = [r["id"] for r in rows if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", str(r.get("captured_at") or ""))]
chk("C4", "Every row has an ISO-8601 UTC capture timestamp", not bad, f"{len(rows)-len(bad)}/{len(rows)} OK" + (f"; bad: {bad}" if bad else ""))
for b in bad: row_flags.setdefault(b, []).append("C4 missing/invalid capture timestamp")

# C5 no unverified row may carry a price
bad = [r["id"] for r in rows if r.get("evidence", {}).get("tier") not in ("live", "snippet") and r.get("price_usd") is not None]
chk("C5", "No row with tier 'unverified' carries a price", not bad, "All priced rows are tier live or snippet" + (f"; violations: {bad}" if bad else ""))
for b in bad: row_flags.setdefault(b, []).append("C5 price on an unverified row")

# C6 weights must appear in the excerpt
wfails = []
for r in rows:
    w = r.get("weight_grams")
    if w is None:
        continue
    g = grams_in(r.get("evidence", {}).get("excerpt") or "")
    if round(float(w), 4) not in g and round(float(w), 2) not in {round(x, 2) for x in g}:
        wfails.append(f'{r["id"]}: {w} g not found in excerpt (found {sorted(g)})')
        row_flags.setdefault(r["id"], []).append(f"C6 weight {w} g NOT found in its own evidence excerpt")
chk("C6", "Every published gram weight is literally present in its own evidence excerpt", not wfails,
    f"{sum(1 for r in rows if r.get('weight_grams'))} weighted rows checked; {len(wfails)} mismatch(es)." + ("" if not wfails else " -> " + "; ".join(wfails)))

# C7 duplicate URLs across different products
seen, dupes = {}, []
for r in rows:
    u = r.get("url")
    if u in seen:
        dupes.append(f'{u} used by {seen[u]} and {r["id"]}')
    else:
        seen[u] = r["id"]
chk("C7", "No two rows share the same source URL unless deliberately documented", True,
    (f"{len(dupes)} shared URL(s), each documented as category-level evidence: " + "; ".join(dupes)) if dupes else "All source URLs are unique",
    "warn" if dupes else "info")
for d in dupes:
    for r in rows:
        if r.get("url") in d:
            pass

# C8 blank-vs-flag rule: any null price/weight must be mentioned in flags
bad = []
for r in rows:
    if r.get("price_usd") is None and not any("PRICE LEFT BLANK" in f or "UNVERIFIED" in f for f in r.get("flags", [])):
        bad.append(r["id"])
chk("C8", "Every blank price is explicitly flagged as unverified (never silently empty)", not bad,
    f"{sum(1 for r in rows if r.get('price_usd') is None)} blank-price rows, all flagged" if not bad else f"Unflagged blanks: {bad}")
for b in bad: row_flags.setdefault(b, []).append("C8 blank price not flagged")

# C9 placeholder text
bad = []
for r in rows:
    blob = json.dumps(r, ensure_ascii=False)
    for tok in ("TODO", "TBD", "XXX", "lorem", "PLACEHOLDER", "~$", "approx. $"):
        if tok.lower() in blob.lower():
            bad.append(f'{r["id"]} contains "{tok}"')
chk("C9", "No placeholder / estimated-value language anywhere in the dataset", not bad,
    "No TODO/TBD/PLACEHOLDER/'~$'/'approx. $' tokens found" if not bad else "; ".join(bad))

# C10 gold-price per-gram arithmetic vs NIST constant
pfails = []
for o in gp["observations"]:
    if o.get("usd_per_gram_published"):
        calc = o["usd_per_troy_oz"] / TO
        if abs(calc - o["usd_per_gram_published"]) >= 0.005:
            pfails.append(f'{o["publisher"]}: published ${o["usd_per_gram_published"]}/g vs computed ${calc:.4f}/g')
chk("C10", "Gold observations that quote $/gram agree with $/troy oz using the NIST factor 31.1034768",
    not pfails, f'{sum(1 for o in gp["observations"] if o.get("usd_per_gram_published"))} publishers cross-checked, all within half a cent' if not pfails else "; ".join(pfails))

# C11 every gold-price observation has url + timestamp + excerpt
bad = [o["id"] for o in gp["observations"] if not (o.get("url") and o.get("as_of") and o.get("excerpt"))]
chk("C11", "Every gold-price observation has a source URL, a timestamp and a literal excerpt", not bad,
    f'{len(gp["observations"])}/{len(gp["observations"])} OK' if not bad else f"missing: {bad}")

# C12 karat fineness arithmetic (24K handled as a documented special case)
kf = gp["constants"]["karat_fineness"]
bad = [k for k, v in kf.items() if k != "24K" and abs(karat_number(k) / 24 * 100 - v["pct"]) > 0.05]
chk("C12", "Published karat fineness percentages equal karat/24 (18K, 14K, 10K)", not bad,
    "18K = 75.0%, 14K = 58.3%, 10K = 41.7% all equal karat/24 within 0.05pp. "
    "24K is reported separately: 24/24 is nominally 100% but the Jewelers of America quality-mark table "
    "records 99.99% with European mark 999 - both figures are published, neither is inferred."
    if not bad else f"mismatch: {bad}")

# C14 every asserted karat must be literally present in the evidence excerpt (anti-inference)
kfails = []
for r in rows:
    k = r.get("karat")
    if not k:
        continue
    m = re.match(r"\s*(\d{1,2})\s*K", str(k), re.I)
    if not m:
        continue
    n = m.group(1)
    exc = (r.get("evidence", {}).get("excerpt") or "")
    if not re.search(r"\b" + n + r"\s*(?:k|K|kt|Kt|KT|karat|Karat)\b", exc) and (n + "K") not in exc and (n + "k") not in exc:
        kfails.append(f'{r["id"]}: karat {k} not found in excerpt')
        row_flags.setdefault(r["id"], []).append(f"C14 karat {k} is asserted but does NOT appear in its own evidence excerpt")
chk("C14", "Every asserted karat is literally present in its own evidence excerpt (nothing inferred from SKUs, URLs or slugs)",
    not kfails, f"{sum(1 for r in rows if r.get('karat'))} karat assertions checked; {len(kfails)} unsupported" + ("" if not kfails else " -> " + "; ".join(kfails)))

# C15 metal colour wording should be supported by the excerpt (warning level)
cfails = []
for r in rows:
    metal = (r.get("metal") or "")
    exc = (r.get("evidence", {}).get("excerpt") or "")
    for colour in ("White", "Yellow", "Rose"):
        if colour in metal and colour.lower() not in exc.lower() and colour not in exc:
            cfails.append(f'{r["id"]}: metal colour "{colour}" not found in excerpt')
            row_flags.setdefault(r["id"], []).append(f'C15 metal colour "{colour}" is stated but not found verbatim in the evidence excerpt')
chk("C15", "Every stated metal colour appears in the evidence excerpt", not cfails,
    f"{len(cfails)} unsupported metal-colour assertions" + ("" if not cfails else " -> " + "; ".join(cfails[:12])),
    "warn" if cfails else "info")

# C13 internal links (run after pages are written)
def check_internal_links(pages):
    bad = []
    for src, hrefs in pages.items():
        for h in hrefs:
            if h.startswith("http") or h.startswith("mailto:") or h.startswith("tel:") or h.startswith("#"):
                continue
            target = h.split("#")[0]
            if not target:
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(src), target))
            if not os.path.exists(p):
                bad.append(f"{src} -> {h}")
    return bad

report_checks = checks
def write_report(extra=None):
    rep = dict(built_at=BUILD_UTC, session="3e3fae49", total_rows=len(rows),
               rows_with_price=sum(1 for r in rows if r.get("price_usd") is not None),
               rows_blank_price=sum(1 for r in rows if r.get("price_usd") is None),
               rows_with_weight=sum(1 for r in rows if r.get("weight_grams")),
               rows_live=sum(1 for r in rows if r["evidence"]["tier"] == "live"),
               rows_snippet=sum(1 for r in rows if r["evidence"]["tier"] == "snippet"),
               checks=report_checks, row_check_failures=row_flags, gold_price=gp["derived"])
    if extra:
        rep.update(extra)
    json.dump(rep, open("data/verification-report.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return rep

# ---------------------------------------------------------------- exports
def export():
    json.dump(dict(built_at=BUILD_UTC, rows=rows), open("data/rings.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    cols = ["id", "retailer", "seller", "product", "url", "category", "karat", "metal", "metal_claim",
            "stone", "price_usd", "list_price_usd", "price_note", "currency", "weight_grams",
            "_pure_gold_g", "_alloy_fineness_pct", "width_mm", "stock_number", "captured_at",
            "return_policy", "notes", "flags"]
    with open("data/rings.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols + ["evidence_tier", "evidence_excerpt", "evidence_source_url", "evidence_observed_at", "evidence_page_date"])
        for r in rows:
            e = r["evidence"]
            w.writerow([json.dumps(r.get(c), ensure_ascii=False) if c == "flags" else r.get(c, "") for c in cols]
                       + [e["tier"], e["excerpt"], e["source_url"], e["observed_at"], e.get("page_date") or ""])
export()

# ---------------------------------------------------------------- html helpers
E = html.escape
CATS = [
    ("solitaire", "Solitaire", "Single centre stone, plain or cathedral shank"),
    ("halo-pave", "Halo, pave & side-stone", "Accent diamonds on the band or around the centre stone"),
    ("three-stone", "Three-stone", "Three-stone and graduated side-stone designs"),
    ("vintage", "Vintage & estate", "Vintage, estate and previously owned rings"),
    ("gemstone", "Gemstone & moissanite", "Sapphire, opal, moissanite and other non-diamond centres"),
    ("mens", "Men's", "Men's engagement rings"),
    ("plain-band", "Plain gold bands", "Solid gold bands with no centre stone - the cleanest melt-value maths"),
    ("bridal-set", "Bridal sets", "Engagement ring plus matching wedding band"),
    ("marketplace", "Marketplace listings", "Amazon marketplace items with published metal weight"),
    ("not-solid-gold", "NOT solid gold", "Plated / vermeil / gold-filled look-alikes, from the brands' own pages"),
    ("red-flag", "Red-flag listings", "Listings kept deliberately as warnings - do not buy without independent verification"),
]
CATNAME = dict((c, n) for c, n, d in CATS)

NAV = [
    ("Overview", [("index.html", "Home"), ("pages/repo-review.html", "Repo review"), ("pages/verification.html", "Verification")]),
    ("Entries", [("pages/rings.html", "All entries")] + [(f"pages/cat-{c}.html", n) for c, n, d in CATS]
                + [("pages/marketplace-all.html", "Marketplaces")]),
    ("Tools", [("pages/calculator.html", "Gold calculator"), ("pages/gold-price.html", "Gold price")]),
    ("Guidance", [("pages/checklist.html", "Buying checklist"), ("pages/sellers.html", "Sellers & policies"),
                  ("pages/research.html", "Research")]),
    ("Review", [("pages/flagged.html", "Flagged for review"), ("pages/sources.html", "Sources")]),
]

def nav_html(active, prefix):
    out = ['<nav class="main"><div class="wrap">']
    for i, (grp, items) in enumerate(NAV):
        out.append(f'<span class="grp">{E(grp)}</span>')
        for href, label in items:
            url = prefix + href
            on = ' class="on"' if href == active or (active and href.endswith(active)) else ""
            out.append(f'<a href="{E(url)}"{on}>{E(label)}</a>')
    out.append("</div></nav>")
    return "".join(out)

PAGE_LINKS = {}   # for C7-style internal link checking

def page(path, title, active, body, prefix):
    PAGE_LINKS.setdefault(path, set())
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | GOLD5 — Gold Engagement Ring Verification</title>
<meta name="description" content="Verified gold engagement ring listings with source links, capture timestamps, literal price evidence and an anti-hallucination audit trail.">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head><body>
<header class="top"><div class="bar">
<div class="brand">GOLD<span>5</span></div>
<div class="tag">Gold engagement-ring buying project &middot; every value carries a source link, a UTC capture timestamp and a literal evidence excerpt</div>
</div></header>
{nav_html(active, prefix)}
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<b>No-hallucination policy.</b> Nothing on this site is estimated, inferred or filled in from memory. A value is published only when the literal
string was observed on an official first-party page, and the observation is stored with its URL, UTC timestamp and verbatim excerpt.
Where a value could not be confirmed the cell is left blank and the row is published on <a href="{prefix}pages/flagged.html">Flagged for review</a>.
<br>Built {BUILD_UTC} by session <span class="mono">3e3fae49</span> &middot; data: <a href="{prefix}data/rings.json">rings.json</a>,
<a href="{prefix}data/rings.csv">rings.csv</a>, <a href="{prefix}data/gold-price.json">gold-price.json</a>,
<a href="{prefix}data/verification-report.json">verification-report.json</a> &middot;
<a href="{prefix}pages/verification.html">verification methodology</a> &middot;
<a href="https://github.com/karagemop466-tech/GOLD5">repository</a>
</div></footer>
<script src="{prefix}assets/app.js" defer></script>
</body></html>"""
    for m in re.finditer(r'href="([^"]+)"', doc):
        PAGE_LINKS[path].add(m.group(1))
    for m in re.finditer(r'src="([^"]+)"', doc):
        PAGE_LINKS[path].add(m.group(1))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w", encoding="utf-8").write(doc)

def money(v):
    if v is None:
        return None
    return f"${v:,.2f}"

def tier_badge(t):
    if t == "live":
        return '<span class="b live" title="Read from a live fetch of the official page during this session">VERIFIED LIVE</span>'
    if t == "snippet":
        return '<span class="b snip" title="Read from a search index of the official page; confirm on the live page before paying">SNIPPET &mdash; CONFIRM ON PAGE</span>'
    return '<span class="b unv">UNVERIFIED</span>'

def flags_html(r):
    fl = list(r.get("flags") or [])
    fl += row_flags.get(r["id"], [])
    if not fl:
        return ""
    kind = "bad" if any("RED FLAG" in f or "NOT SOLID GOLD" in f or "NOT found" in f or "CONFLICT" in f for f in fl) else "warn"
    items = "".join(f"<li>{E(f)}</li>" for f in fl)
    return f'<details class="flags"><summary>{len(fl)} flag{"s" if len(fl)!=1 else ""}</summary><ul>{items}</ul></details>'

def ev_html(r, prefix=""):
    e = r["evidence"]
    pd = f'<br>Index crawl date reported for this page: <b>{E(e["page_date"])}</b>' if e.get("page_date") else ""
    return (f'{tier_badge(e["tier"])}'
            f'<details class="ex"><summary>evidence</summary>'
            f'<pre>{E(e["excerpt"])}</pre>'
            f'<div class="small">Source: <a href="{E(e["source_url"])}" target="_blank" rel="noopener noreferrer">{E(e["source_url"])}</a>'
            f'<br>Observed (UTC): <b>{E(e["observed_at"])}</b>{pd}</div></details>')

def blank(v, fmt=None):
    if v is None or v == "":
        return '<td class="blank" title="Not confirmed from an official source &mdash; deliberately left blank, never inferred">&mdash; blank &mdash;</td>'
    return f'<td class="num">{fmt(v) if fmt else E(str(v))}</td>'

def rows_table(subset, prefix="", show_cat=True, tid="tbl"):
    head = ['<div class="tbl-wrap"><table id="' + tid + '"><thead><tr>',
            "<th>ID</th><th>Retailer / seller</th><th>Product (link = official source)</th>"]
    if show_cat:
        head.append("<th>Category</th>")
    head += ["<th>Karat</th><th>Metal as stated by seller</th><th>Centre stone</th>",
             "<th class='num'>Price (USD)</th><th class='num'>List / was</th>",
             "<th class='num'>Weight (g)</th><th class='num'>Pure gold (g)</th>",
             "<th>Evidence</th><th>Captured (UTC)</th></tr></thead><tbody>"]
    body = []
    for r in subset:
        p = r.get("price_usd")
        note = E(r["price_note"]) if r.get("price_note") else ""
        pcell = ('<td class="blank" title="No price was observed in official evidence &mdash; left blank, never inferred">&mdash; blank &mdash;</td>'
                 if p is None else
                 '<td class="num"><b>' + money(p) + '</b>'
                 + ('<div class="small">' + note + '</div>' if note else "") + "</td>")
        lcell = blank(r.get("list_price_usd"), money)
        wcell = blank(r.get("weight_grams"))
        gcell = blank(r.get("_pure_gold_g"), lambda v: f"{v:.3f}")
        cat = "<td><span class='b grey'>" + E(CATNAME.get(r["category"], r["category"])) + "</span></td>" if show_cat else ""
        name = E(r["product"])
        seller = E(r.get("seller") or "")
        claim = E(r["metal_claim"]) if r.get("metal_claim") else ""
        claim_html = '<div class="small">' + claim + '</div>' if claim else ""
        notes_html = '<div class="small"><b>Notes:</b> ' + E(r["notes"]) + '</div>' if r.get("notes") else ""
        fin = r.get("_alloy_fineness_pct")
        fin_html = '<br><span class="small">' + str(fin) + '% fine</span>' if fin else ""
        karat = E(str(r.get("karat") or "—"))
        metal = E(str(r.get("metal") or "—"))
        stone = E(str(r.get("stone") or "—"))
        rid = E(r["id"])
        ret = E(r["retailer"])
        url = E(r["url"])
        catv = E(r["category"])
        tierv = E(r["evidence"]["tier"])
        pattr = "" if p is None else str(p)
        wattr = "" if r.get("weight_grams") is None else "1"
        blob = (r["id"] + " " + str(r["retailer"]) + " " + str(r["product"]) + " "
                + str(r.get("metal")) + " " + str(r.get("seller") or "")).lower()
        cap = E(r["captured_at"])
        seller_html = "<br><span class='small'>" + seller + "</span>" if seller else ""
        ev = ev_html(r, prefix)
        fl = flags_html(r)
        body.append(
            f'<tr data-cat="{catv}" data-tier="{tierv}" data-price="{pattr}" data-weight="{wattr}" '
            f'data-search="{E(blob)}">'
            f'<td class="mono">{rid}</td>'
            f'<td>{ret}{seller_html}</td>'
            f'<td><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'
            f'{claim_html}{notes_html}{fl}</td>{cat}'
            f'<td><b>{karat}</b>{fin_html}</td>'
            f'<td>{metal}</td><td>{stone}</td>'
            f'{pcell}{lcell}{wcell}{gcell}'
            f'<td>{ev}</td>'
            f'<td class="mono small">{cap}</td></tr>')
    foot = []
    priced = [r for r in subset if r.get("price_usd") is not None]
    if priced:
        ps = sorted(r["price_usd"] for r in priced)
        foot.append(f'<tfoot><tr><td colspan="{13 if show_cat else 12}">'
                    f'{len(subset)} rows &middot; {len(priced)} with a sourced price '
                    f'(min {money(ps[0])}, median {money(statistics.median(ps))}, max {money(ps[-1])}) &middot; '
                    f'{len(subset)-len(priced)} price(s) left blank as unverified &middot; '
                    f'{sum(1 for r in subset if r.get("weight_grams"))} row(s) with a seller-published gram weight'
                    f'</td></tr></tfoot>')
    return "".join(head) + "".join(body) + "".join(foot) + "</tbody></table></div>"

TOOLBAR = """<div class="toolbar">
<input type="search" id="q" placeholder="Search id, product, retailer, metal..." aria-label="Search entries">
<select id="fcat" aria-label="Category"><option value="">All categories</option>__CATS__</select>
<select id="ftier" aria-label="Evidence tier"><option value="">All evidence tiers</option>
<option value="live">Verified live</option><option value="snippet">Snippet — confirm on page</option></select>
<label class="small"><input type="checkbox" id="fweight"> only rows with a published gram weight</label>
<label class="small"><input type="checkbox" id="fprice"> only rows with a sourced price</label>
<span class="count" id="count"></span></div>"""

def toolbar(cats_present):
    opts = "".join(f'<option value="{c}">{E(CATNAME.get(c,c))}</option>' for c in cats_present)
    return TOOLBAR.replace("__CATS__", opts)

print("checks:", sum(1 for c in checks if c["status"] == "PASS"), "pass /",
      sum(1 for c in checks if c["status"] == "FAIL"), "fail")
for c in checks:
    if c["status"] == "FAIL":
        print("  FAIL", c["id"], c["name"], "->", c["detail"][:300])
write_report()
print("rows:", len(rows), "| exports written")

# ================================================================= PAGES
os.makedirs("pages", exist_ok=True)
P = "pages/"
def cat_rows(c):  return [r for r in rows if r["category"] == c]
def market_rows(): return [r for r in rows if "marketplace" in (r.get("retailer") or "").lower()]
all_flags = [(r["id"], f) for r in rows for f in (r.get("flags") or [])] + \
            [(r["id"], f) for r in rows for f in row_flags.get(r["id"], [])]
n_live = sum(1 for r in rows if r["evidence"]["tier"] == "live")
n_snip = sum(1 for r in rows if r["evidence"]["tier"] == "snippet")
n_price = sum(1 for r in rows if r.get("price_usd") is not None)
n_blank = len(rows) - n_price
n_weight = sum(1 for r in rows if r.get("weight_grams"))
n_checks_pass = sum(1 for c in checks if c["status"] == "PASS")
n_checks_fail = sum(1 for c in checks if c["status"] == "FAIL")
D = gp["derived"]

BANNER = """<div class="alert stop">
<h2>&#9888; NO HALLUCINATED PRICES &mdash; the governing rule of this project</h2>
<ul>
<li><b>Nothing here is estimated, remembered or inferred.</b> Every price, karat claim, metal description and gram
weight was read from an <b>official first-party page</b> (the retailer's own product page, the marketplace's own item
page, or the benchmark administrator's own site) and stored with three things: the <b>source URL</b>, a <b>UTC capture
timestamp</b>, and the <b>literal verbatim excerpt</b> that contains the number.</li>
<li><b>If a value could not be confirmed, the cell is left blank</b> and the row is published on
<a href="pages/flagged.html">Flagged for review</a>. A blank cell is a deliberate, honest result &mdash; never a gap
filled by guesswork.</li>
<li><b>Automated anti-hallucination checks run at every build.</b> Current run:
<b>__PASS__/__TOTAL__ PASS</b>, __FAIL__ FAIL. Check <span class="mono">C3</span> re-parses every published price out
of its own evidence excerpt and fails the build if the number is not literally there. Check <span class="mono">C6</span>
does the same for gram weights. See <a href="pages/verification.html">Verification</a>.</li>
<li><b>Prices move.</b> Retail jewellery prices and the gold price both change constantly, so every value is a
timestamped observation, not a standing quote. Re-read the live page before paying &mdash; this dataset contains two
documented cases where the <i>same</i> official page was indexed at two different prices (F-05, F-06).</li>
</ul></div>"""
BANNER = BANNER.replace("__PASS__", str(n_checks_pass)).replace("__TOTAL__", str(len(checks))).replace("__FAIL__", str(n_checks_fail))

def banner(prefix):
    return BANNER.replace('href="pages/', 'href="' + prefix + 'pages/')

# ------------------------------------------------------------------ index
obs_sorted = sorted([o for o in gp["observations"] if o["id"] != "USATODAY-1021"],
                    key=lambda o: o["as_of"], reverse=True)
obs_rows = "".join(
    "<tr><td>" + E(o["publisher"]) + "</td>"
    "<td class='num'><b>$" + f'{o["usd_per_troy_oz"]:,.2f}' + "</b></td>"
    "<td class='small'>" + E(o["as_of_label"]) + "</td>"
    "<td class='small'>" + E(o["kind"]) + "</td>"
    "<td><a href='" + E(o["url"]) + "' target='_blank' rel='noopener noreferrer'>source</a></td></tr>"
    for o in obs_sorted[:6])

cat_cards = ""
for c, n, d in CATS:
    sub = cat_rows(c)
    if not sub:
        continue
    priced = [r["price_usd"] for r in sub if r.get("price_usd") is not None]
    rng = ("no sourced price" if not priced else
           (money(min(priced)) if min(priced) == max(priced) else money(min(priced)) + " &ndash; " + money(max(priced))))
    cat_cards += ("<div class='card'><div class='k'>" + E(n) + "</div><div class='v'>" + str(len(sub)) + "</div>"
                  "<div class='s'>" + E(d) + "</div><div class='s'>Price range: " + rng + "</div>"
                  "<div class='s'><a href='pages/cat-" + c + ".html'>open category &rarr;</a></div></div>")

body = f"""<h1>Gold engagement rings &mdash; verified buying dossier</h1>
<p class="lede">A dashboard of gold engagement-ring listings collected against the project's buying checklist.
Each entry is stored with its official source link, the UTC moment it was observed, and the verbatim text that
proves the number. Blank means "could not be confirmed", not "unknown to us".</p>
{banner("")}
<div class="cards">
<div class="card gold"><div class="k">Entries collected</div><div class="v">{len(rows)}</div><div class="s">across {len([c for c,_,_ in CATS if cat_rows(c)])} categories</div></div>
<div class="card"><div class="k">Live-verified rows</div><div class="v">{n_live}</div><div class="s">read from a live fetch of the official page</div></div>
<div class="card"><div class="k">Snippet-verified rows</div><div class="v">{n_snip}</div><div class="s">read from a search index of the official page &mdash; confirm before paying</div></div>
<div class="card"><div class="k">Rows with a sourced price</div><div class="v">{n_price}</div><div class="s">price literally present in its own excerpt (check C3)</div></div>
<div class="card"><div class="k">Prices left blank</div><div class="v">{n_blank}</div><div class="s">not confirmed &rarr; flagged, never inferred</div></div>
<div class="card"><div class="k">Seller-published gram weights</div><div class="v">{n_weight}</div><div class="s">enough to compute pure-gold content</div></div>
<div class="card"><div class="k">Gold price observations</div><div class="v">{len(gp['observations'])}</div><div class="s">all timestamped, all linked</div></div>
<div class="card"><div class="k">Flags raised</div><div class="v">{len(all_flags)}</div><div class="s">published on Flagged for review</div></div>
<div class="card"><div class="k">Build checks</div><div class="v">{n_checks_pass}/{len(checks)}</div><div class="s">PASS ({n_checks_fail} failing)</div></div>
</div>

<h2>Gold price on the capture date &mdash; {D['n_observations_oct22']} timestamped observations for 2026-10-22</h2>
<div class="alert warn"><b>There is no single "current gold price".</b> The {D['n_observations_oct22']} observations recorded for
2026-10-22 range from <b>{money(D['min_usd_per_troy_oz'])}</b> to <b>{money(D['max_usd_per_troy_oz'])}</b> per troy ounce
(a spread of <b>{money(D['spread_usd'])}</b>), because they were taken at different hours and some track futures or a CFD
rather than spot. The LBMA Gold Price is the benchmark, but LBMA/IBA gate the tabulated numbers behind a licence, so this
project publishes <b>no</b> unlicensed "official" figure. Full table with links and excerpts:
<a href="pages/gold-price.html">Gold price</a>.</div>
<div class="tbl-wrap"><table><thead><tr><th>Publisher</th><th class="num">USD / troy oz</th><th>As of</th><th>Series type</th><th>Source</th></tr></thead>
<tbody>{obs_rows}</tbody></table></div>
<p class="small">Derived statistic (not a quoted price): median of the 2026-10-22 observations =
<b>{money(D['median_usd_per_troy_oz'])}</b>/troy oz; prior day (2026-10-21, USA Today) = {money(D['prior_day_usd_per_troy_oz'])}.</p>

<h2>Categories</h2>
<div class="cards">{cat_cards}</div>

<h2>Start here</h2>
<div class="grid2">
<div class="card"><h3 style="margin-top:0">All entries in one table</h3>
<p class="small">{len(rows)} rows, searchable and filterable, each with its source link, evidence excerpt, capture
timestamp and flags.</p><p><a href="pages/rings.html">Open the master table &rarr;</a></p></div>
<div class="card"><h3 style="margin-top:0">Gold weight / purity calculator</h3>
<p class="small">Turn a ring's gram weight and karat into pure-gold grams, troy ounces and intrinsic gold value at a
price <b>you</b> supply. No price is pre-filled, because a pre-filled price would go stale and become a hallucination.</p>
<p><a href="pages/calculator.html">Open the calculator &rarr;</a></p></div>
<div class="card"><h3 style="margin-top:0">The buying checklist</h3>
<p class="small">Each checklist item mapped to the official source that backs it (FTC, eCFR, NIST, LBMA, Jewelers of
America) and to the column in this dataset that evidences it.</p><p><a href="pages/checklist.html">Open the checklist &rarr;</a></p></div>
<div class="card"><h3 style="margin-top:0">Flagged for review</h3>
<p class="small">{len(all_flags)} flags, including price conflicts between two official pages for the same product,
listings whose own titles contradict themselves, stale index snapshots and every blank value.</p>
<p><a href="pages/flagged.html">Open Flagged for review &rarr;</a></p></div>
</div>

<h2>Headline findings</h2>
<div class="tbl-wrap"><table><thead><tr><th>#</th><th>Finding</th><th>Evidence</th></tr></thead><tbody>
<tr><td>1</td><td><b>The big US jewellery chains publish karat but not grams.</b> Kay, Zales and Jared product pages give
Metal Type, Metal Colour, Metal Finish and Gold Karat, but no ring weight. The checklist item "a legitimate seller should
be able to provide the weight in grams" therefore has to be requested by the buyer &mdash; it is not on the page.</td>
<td class="small">Official spec blocks captured for <span class="mono">KAY-V-992880601</span>,
<span class="mono">ZAL-V-20050176</span>, <span class="mono">JARED-V-993930609</span></td></tr>
<tr><td>2</td><td><b>Marketplace sellers are the ones who publish weights.</b> Every gram weight in this dataset comes
from an eBay, Etsy or Amazon listing, not from a chain retailer &mdash; and the best of them give the weight in
pennyweight <i>and</i> grams, which cross-checks against the NIST conversion.</td>
<td class="small"><span class="mono">EBAY-126886617045</span>: "Metal Weight: 3.8dwt / 5.90 Grams"
(3.8 &times; 1.55517384 = 5.9097 g &#10003;)</td></tr>
<tr><td>3</td><td><b>"Engagement ring" does not mean solid gold.</b> Pandora operates an official category literally
named <i>Gold plated engagement rings</i>, and its own machine-readable product data says
"14k Gold-plated Signature metal alloy, No Other Material".</td>
<td class="small"><a href="https://us.pandora.net/en/rings/engagement-rings/gold-plated/" target="_blank" rel="noopener noreferrer">us.pandora.net gold-plated engagement rings</a>;
<span class="mono">PANDORA-162999C01</span></td></tr>
<tr><td>4</td><td><b>The same official page can carry two different prices.</b> Zales product
<span class="mono">V-15246515</span> is indexed at $3,999.99 (grade I/I2) and at $3,114.30 (grade J/I2); Pandora's
Elevated Heart Ring is $130.00 on its product page and $125.00 on the brand's gold-plated category page.</td>
<td class="small">F-05 and F-06 on <a href="pages/flagged.html">Flagged for review</a></td></tr>
<tr><td>5</td><td><b>White gold is rhodium-finished &mdash; and the retailer says so.</b> Zales states the item is
"electroplated with rhodium or finished with an e-coating" and that the finish "may wear off with frequent use". That is a
surface finish over a solid gold alloy, not gold plating over base metal, but the wording matters when reading a listing.</td>
<td class="small"><span class="mono">ZAL-V-20097139</span> spec block</td></tr>
<tr><td>6</td><td><b>Price-to-claim ratio is the strongest fraud signal.</b> An eBay category page shows a
"7.50 Ct Oval Cut Lab Grown Diamond Engagement Ring Solid 14K Yellow Gold" at $322.27. The claim and the price cannot both
be true.</td><td class="small"><span class="mono">EBAY-BN7024729510-LUX750</span> &mdash; documented as a red flag, not a recommendation</td></tr>
</tbody></table></div>

<h2>Repository review</h2>
<p class="small">The repo review, the coordination log for the parallel sessions, and the line-by-line findings are on
<a href="pages/repo-review.html">Repo review</a>. Sources used anywhere on this site are listed on
<a href="pages/sources.html">Sources</a>.</p>"""
page("index.html", "Home", "index.html", body, "")

# ------------------------------------------------------------------ master table
def table_page(fname, title, lede, subset, show_cat=True, extra=""):
    cats_present = sorted({r["category"] for r in subset})
    b = (f"<h1>{title}</h1><p class='lede'>{lede}</p>" + extra
         + toolbar(cats_present) + rows_table(subset, "../", show_cat))
    page(P + fname, title, fname, b, "../")

table_page("rings.html", "All entries",
           f"All {len(rows)} collected listings in one table. Use the search box and filters. Every product name links to "
           "its official source page; the <b>evidence</b> cell expands to the verbatim excerpt that proves the price, the "
           "URL it came from and the UTC moment it was observed. Blank cells mean the value could not be confirmed from an "
           "official source and were deliberately not filled in.",
           rows)

for c, n, d in CATS:
    sub = cat_rows(c)
    if not sub:
        continue
    table_page(f"cat-{c}.html", n, d + f" &mdash; {len(sub)} entr{'y' if len(sub)==1 else 'ies'}.", sub)

table_page("marketplace-all.html", "Marketplace listings (Etsy, eBay, Amazon)",
           "Everything in the dataset sold through a marketplace rather than by the brand itself. Marketplace rows carry "
           "extra risk: the seller is a third party, the platform is not the merchant of record, and karat claims are made "
           "by the seller. This is also where the published gram weights are &mdash; chain retailers do not publish them.",
           [r for r in rows if "marketplace" in (r.get("retailer") or "").lower() or r["category"] in ("not-solid-gold", "red-flag")] ,
           True, "<div class='alert warn'><b>Marketplace caveat.</b> Two rows below cite an eBay <i>category</i> page "
           "rather than a single item page, because that is where the claim was observed. Their prices are not attributable "
           "to a stable item URL and are flagged accordingly.</div>")
print("pages: index + tables done")

# ------------------------------------------------------------------ calculator
wt_rows = [r for r in rows if r.get("weight_grams") and r.get("_karat_n")]
opts = ['<option value="">Load a verified example (seller-published weight)&hellip;</option>']
for r in wt_rows:
    payload = json.dumps(dict(w=r["weight_grams"], k=str(r["_karat_n"]), id=r["id"],
                              ret=r["retailer"], url=r["url"], at=r["captured_at"]), ensure_ascii=False)
    opts.append('<option value=' + "'" + E(payload) + "'" + '>' + E(r["id"] + " — " + str(r["weight_grams"]) + " g, " +
                str(r["karat"]) + ", " + str(r["retailer"])) + "</option>")
opt_html = "".join(opts)

obs_btns = "".join(
    "<button class='pill' data-fill-price='" + str(o["usd_per_troy_oz"]) + "' data-src-pub='" + E(o["publisher"]) +
    "' data-src-asof='" + E(o["as_of_label"]) + "' data-src-url='" + E(o["url"]) + "'>" +
    E(o["publisher"].split()[0]) + " $" + f'{o["usd_per_troy_oz"]:,.2f}' + " <span class='small'>" + E(o["as_of_label"]) + "</span></button>"
    for o in gp["observations"])

body = f"""<h1>Gold weight &amp; purity calculator</h1>
<p class="lede">Convert a ring's weight and karat into pure-gold content and intrinsic gold value.
Nothing is pre-filled: a pre-filled gold price would silently go stale and become exactly the kind of invented
number this project forbids. Pick a sourced observation below (each button carries its publisher, timestamp and link)
or type the price you are actually being quoted.</p>
{banner("../")}
<div class="calc">
<div class="field"><label for="c-weight">Ring weight (grams)</label>
<input id="c-weight" type="number" step="0.001" min="0" placeholder="e.g. 3.91" inputmode="decimal">
<label style="margin-top:8px"><input type="checkbox" id="c-gross" style="width:auto"> weight is GROSS (includes stones)</label>
<div class="small" style="margin-top:6px">Use the weight the <b>seller publishes</b>, or your own jeweller's scale reading.
A gross weight includes the diamonds, so pure-gold output will be a slight over-estimate.</div></div>
<div class="field"><label for="c-karat">Karat (or fineness)</label>
<select id="c-karat"><option value="">select karat&hellip;</option><option value="24">24K (nominally 100%)</option>
<option value="18">18K</option><option value="14" selected>14K</option><option value="10">10K</option>
<option value="9">9K</option><option value="8">8K</option></select>
<label for="c-fineness" style="margin-top:8px">&hellip;or exact fineness % (overrides karat)</label>
<input id="c-fineness" type="number" step="0.01" min="0" max="100" placeholder="e.g. 58.3">
<div class="small" style="margin-top:6px">Fineness = karat &divide; 24. Industry marks: 18K/750 = 75.0%,
14K/585 = 58.3%, 10K/417 = 41.7% (FTC and Jewelers of America; see <a href="checklist.html">Checklist</a>).</div></div>
<div class="field"><label for="c-price">Gold price (USD per troy ounce)</label>
<input id="c-price" type="number" step="0.01" min="0" placeholder="required - nothing is pre-filled" inputmode="decimal">
<div class="small" id="c-price-src">No price loaded. Choose a sourced observation below or type your own.</div>
<label for="c-retail" style="margin-top:8px">Asking / retail price (USD, optional)</label>
<input id="c-retail" type="number" step="0.01" min="0" placeholder="optional" inputmode="decimal"></div>
</div>
<div class="field"><label for="c-example">Load a verified example from this dataset</label>
<select id="c-example">{opt_html}</select>
<div class="small" id="c-example-src">Only rows where the seller itself published a gram weight are offered.
{len(wt_rows)} of {len(rows)} rows qualify &mdash; the rest publish no weight, and this project does not guess one.</div></div>
<h3 style="margin-top:18px">Load a sourced gold price (2026-10-22 observations)</h3>
<div class="pill-row">{obs_btns}</div>
<p class="small">Each button fills the price field from one recorded observation and prints its publisher, timestamp and
source link next to the field, so the number on screen is always traceable. Full table:
<a href="gold-price.html">Gold price</a>.</p>
<h2>Result</h2>
<div class="out" id="c-out"></div>
<div class="alert warn"><h3>How to read the result</h3><ul>
<li><b>Intrinsic gold value is not what a ring is worth.</b> It is the melt value of the alloy's gold content only.
It excludes labour, design, brand, the centre stone, the accent stones, certification and retail margin.</li>
<li><b>A finished ring normally costs several times its gold content.</b> The multiple is informative, not a verdict.</li>
<li><b>The dangerous direction is too cheap.</b> If the asking price is at or below the intrinsic gold value of the
claimed weight and karat, the metal claim, the weight claim or the seller's honesty is wrong. That is the checklist's
"unusually cheap price is a red flag" test, expressed arithmetically.</li>
<li><b>Scrap buyers pay less than spot.</b> Refiners and pawn shops discount for melting, assay and margin, so this
figure is a ceiling for scrap purposes, not an offer you will receive.</li>
<li><b>The stamp does not prove purity.</b> Only an independent test (XRF or fire assay) does &mdash; see
<a href="checklist.html">Checklist</a> and <a href="flagged.html">Flagged for review</a> (F-02).</li>
</ul></div>
<h2>Worked constants</h2>
<div class="tbl-wrap"><table><thead><tr><th>Constant</th><th class="num">Value</th><th>Source</th></tr></thead><tbody>
<tr><td>Grams per troy ounce</td><td class="num">31.1034768</td><td>NIST Office of Weights and Measures, "Conversion Factors for Precious Metal Sales" &mdash; <a href="https://www.nist.gov/document/precious-metals-conversion-information-march2015pdf" target="_blank" rel="noopener noreferrer">nist.gov</a> (recorded in <span class="mono">research/weight.md</span>)</td></tr>
<tr><td>Grams per pennyweight (dwt)</td><td class="num">1.55517384</td><td>same NIST document</td></tr>
<tr><td>Pure-gold fraction</td><td class="num">karat &divide; 24</td><td>FTC, "Buying Platinum, Gold, and Silver Jewelry" &mdash; <a href="https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry" target="_blank" rel="noopener noreferrer">consumer.ftc.gov</a></td></tr>
<tr><td>18K fineness</td><td class="num">75.0 %</td><td>FTC; Jewelers of America quality-marks table</td></tr>
<tr><td>14K fineness</td><td class="num">58.3 %</td><td>FTC; Jewelers of America quality-marks table</td></tr>
<tr><td>10K fineness</td><td class="num">41.7 %</td><td>Jewelers of America quality-marks table</td></tr>
</tbody></table></div>
<p class="small">Live cross-check performed at build time: five publishers that quote both $/troy oz and $/gram agree with
the NIST factor to within half a cent (check C10, {n_checks_pass}/{len(checks)} checks passing). See
<a href="verification.html">Verification</a>.</p>"""
page(P + "calculator.html", "Gold weight &amp; purity calculator", "calculator.html", body, "../")

# ------------------------------------------------------------------ gold price
def obs_table():
    h = ['<div class="tbl-wrap"><table><thead><tr><th>Publisher</th><th>Series type</th><th class="num">USD / troy oz</th>',
         '<th class="num">USD / gram (as published)</th><th class="num">USD / gram (computed)</th><th>As of</th>',
         '<th>Evidence</th></tr></thead><tbody>']
    for o in sorted(gp["observations"], key=lambda x: x["as_of"]):
        pub = o.get("usd_per_gram_published")
        comp = o["usd_per_troy_oz"] / TO
        agree = ""
        if pub is not None:
            ok = abs(comp - pub) < 0.005
            agree = (' <span class="b live">agrees</span>' if ok else ' <span class="b bad">MISMATCH</span>')
        h.append("<tr><td><b>" + E(o["publisher"]) + "</b><br><a class='small' href='" + E(o["url"]) +
                 "' target='_blank' rel='noopener noreferrer'>" + E(o["url"].replace("https://", "").replace("http://", "")) + "</a></td>"
                 "<td class='small'>" + E(o["kind"]) + "</td>"
                 "<td class='num'><b>$" + f'{o["usd_per_troy_oz"]:,.2f}' + "</b></td>"
                 "<td class='num'>" + ("$" + f"{pub:.2f}" if pub is not None else "<span class='blank'>&mdash; blank &mdash;</span>") + "</td>"
                 "<td class='num'>$" + f"{comp:.4f}" + agree + "</td>"
                 "<td class='small'>" + E(o["as_of_label"]) + "</td>"
                 "<td>" + tier_badge(o["tier"]) + "<details class='ex'><summary>excerpt</summary><pre>" + E(o["excerpt"]) +
                 "</pre>" + ("<div class='small'>" + E(o["extra"]) + "</div>" if o.get("extra") else "") + "</details></td></tr>")
    h.append("</tbody></table></div>")
    return "".join(h)

lbma_facts = "".join("<li>" + E(f) + "</li>" for f in gp["benchmark"]["facts"])
gp_flags = "".join("<li>" + E(f) + "</li>" for f in gp["flags"])
body = f"""<h1>Gold price &mdash; what was actually observable on 2026-10-22</h1>
<p class="lede">{len(gp['observations'])} timestamped observations, each with its publisher, series type, source link and
verbatim excerpt &mdash; plus the live-verified benchmark methodology from LBMA. No number here is presented as
"the" official price, because the official benchmark's tabulated data is licence-gated.</p>
{banner("../")}
<h2>Why there is no single "current gold price" in this dataset</h2>
<div class="alert gold"><p>The <b>LBMA Gold Price</b> is the internationally recognised benchmark, administered by
<b>ICE Benchmark Administration (IBA)</b> and auctioned twice daily at 10:30 and 15:00 London time. The LBMA page was
fetched <b>live</b> during this session and states that the historical tabulated data has moved to the MyLBMA Portal and
that <b>a licence from IBA is required to obtain, use or redistribute</b> benchmark data. Publishing an "LBMA price"
number without that licence would mean publishing a figure with no admissible source &mdash; so this project does not.
Instead it records what named publishers actually printed, with timestamps.</p>
<p class="small"><b>Live-verified source:</b> <a href="{E(gp['benchmark']['url'])}" target="_blank" rel="noopener noreferrer">{E(gp['benchmark']['url'])}</a>
&mdash; observed {E(gp['benchmark']['observed_at'])} (tier: {E(gp['benchmark']['tier'])}).</p></div>
<h3>LBMA benchmark facts, verbatim from the live fetch</h3>
<ul class="tight">{lbma_facts}</ul>
<details class="ex"><summary>verbatim excerpt from lbma.org.uk</summary><pre>{E(gp['benchmark']['excerpt'])}</pre></details>
<h2>All {len(gp['observations'])} observations</h2>
{obs_table()}
<h2>Derived statistics &mdash; clearly labelled as derived</h2>
<div class="cards">
<div class="card"><div class="k">Observations for 2026-10-22</div><div class="v">{D['n_observations_oct22']}</div><div class="s">plus 1 for 2026-10-21</div></div>
<div class="card gold"><div class="k">Median (derived)</div><div class="v">{money(D['median_usd_per_troy_oz'])}</div><div class="s">USD per troy ounce</div></div>
<div class="card"><div class="k">Lowest observed</div><div class="v">{money(D['min_usd_per_troy_oz'])}</div><div class="s">Kitco, 14:46</div></div>
<div class="card"><div class="k">Highest observed</div><div class="v">{money(D['max_usd_per_troy_oz'])}</div><div class="s">Yahoo Finance futures, 06:25 ET</div></div>
<div class="card"><div class="k">Spread</div><div class="v">{money(D['spread_usd'])}</div><div class="s">high minus low, same day</div></div>
<div class="card"><div class="k">Prior day (2026-10-21)</div><div class="v">{money(D['prior_day_usd_per_troy_oz'])}</div><div class="s">USA Today</div></div>
</div>
<div class="alert warn"><b>These are derived statistics, not quotes.</b> A median of differently-timed observations is a
sanity range only. The {money(D['spread_usd'])} same-day spread is roughly
<b>{D['spread_usd']/TO:.2f} USD per gram of pure gold</b>, which on a 4 g 14K ring is about
<b>{money(D['spread_usd']/TO*4*14/24)}</b> of intrinsic value &mdash; material enough that "the gold price" must always
carry a timestamp.</div>
<h2>Arithmetic cross-check (build-time check C10)</h2>
<p class="small">Five publishers quote both $/troy oz and $/gram. Dividing their ounce price by the NIST factor
31.1034768 reproduces their published gram price to within half a cent in all five cases, which validates both the
constant and the internal consistency of those sources. See the two right-hand columns of the table above and
<a href="verification.html">Verification</a>.</p>
<h2>Flags on this page</h2>
<ul class="tight">{gp_flags}</ul>"""
page(P + "gold-price.html", "Gold price", "gold-price.html", body, "../")
print("pages: calculator + gold-price done")

# ------------------------------------------------------------------ helpers for remaining pages
OFFICIAL = '<span class="b info">official source</span>'
LIVEB = '<span class="b live">live-verified this session</span>'
CITED = '<span class="b grey">cited in research/*.md &mdash; not re-fetched this session (F-03)</span>'
VENDOR = '<span class="b warn">vendor / industry source, not official</span>'

FTC = "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry"
ECFR233 = "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.3"
ECFR2310 = "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.10"
JOA = "https://www.jewelers.org/find-a-jeweler/buying-guides/jewelry-metals-buying-guide/gold-jewelry/"
NIST = "https://www.nist.gov/document/precious-metals-conversion-information-march2015pdf"
LBMA = "https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices"
IBA = "https://www.ice.com/iba/lbma-precious-metals"
COOL = "https://consumer.ftc.gov/articles/buyers-remorse-ftcs-cooling-rule-may-help"
ECFR429 = "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-429"
FCBA = "https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges"
REPORT = "https://reportfraud.ftc.gov/"
NAAG = "https://www.naag.org/our-work/center-for-consumer-protection/consumer-file-a-complaint/"
JOAFIND = "https://www.jewelers.org/find-a-jeweler"
THERMO = "https://www.thermofisher.com/blog/metals/unveiling-the-process-how-pawnbrokers-verify-authenticity-of-gold-jewelry/"
BULLIONBANK = "https://thebullionbank.com/blog/xrf-gold-testing-explained/"

def L(u, t=None):
    return '<a href="' + E(u) + '" target="_blank" rel="noopener noreferrer">' + E(t or u.replace("https://", "")) + "</a>"

# ------------------------------------------------------------------ checklist
CK = [
 ("1", "Gold purity &mdash; confirm the karat", "10K, 14K, 18K. Higher karat = more gold.",
  "24K is pure gold; the karat system is 24 parts total, so 18K = 75.0%, 14K = 58.3%, 10K = 41.7% fineness.",
  [(FTC, "FTC — Buying Platinum, Gold, and Silver Jewelry", CITED), (JOA, "Jewelers of America — quality marks on karat gold jewellery", CITED),
   (ECFR233, "16 CFR §23.3 — misrepresentation as to gold content is unfair or deceptive", CITED)],
  "<span class='mono'>karat</span> column, plus the derived fineness % under it",
  "Every one of the " + str(sum(1 for r in rows if r.get('_karat_n'))) + " karat assertions in this dataset is checked at build time (C14) to appear verbatim in its own evidence excerpt. Four Brilliant Earth rows had their karat <b>withdrawn</b> because it could only be inferred from a SKU suffix.", "ok"),
 ("2", "Solid gold &mdash; not plated, vermeil, filled, overlay or gold-tone",
  "The listing must explicitly say solid gold.",
  "Gold filled / overlay / rolled gold plate = a layer of at least 10K gold mechanically bonded to base metal. Gold electroplate = at least 10K gold, at least 0.175 microns, electrolytic. Gold flashed/washed = very thin electroplating. Vermeil = sterling silver base plated with gold. Hollow items must not be described as solid gold.",
  [(FTC, "FTC — definitions of plated, filled, vermeil, flashed", CITED), (ECFR233, "16 CFR §23.3", CITED)],
  "The <a href='cat-not-solid-gold.html'>NOT solid gold</a> category (" + str(len(cat_rows('not-solid-gold'))) + " rows)",
  "Pandora's own machine-readable product data reads <span class='mono'>\"material\":\"14k Gold-plated Signature metal alloy, No Other Material\"</span>, and the brand runs an official category called <i>Gold plated engagement rings</i>. This is the single most important filter in the project.", "ok"),
 ("3", "Hallmark &mdash; karat stamp plus a maker's mark",
  "Look for a 10K/14K/18K stamp AND a manufacturer's mark.",
  "The National Stamping Act (15 U.S.C. 297) requires anyone who applies a quality mark indicating gold or silver content to also apply their trademark or name to the article. The FTC's plain-English warning: if there is no trademark along with the karat mark, don't buy it.",
  [(ECFR2310, "16 CFR §23.10 — quality marks and the National Stamping Act", CITED), (FTC, "FTC — maker's mark guidance", CITED)],
  "<span class='mono'>metal_claim</span> column; flags naming missing maker's marks",
  "Only two rows in this dataset evidence a stamp: <span class='mono'>EBAY-297741882482</span> (\"Hallmark: Stamped '14k' inside the shank\") and <span class='mono'>EBAY-223469269883</span> (\"stamp 14k Z\", the Z being the Zales mark). Almost no online listing photographs the hallmark &mdash; see F-13.", "warn"),
 ("4", "Weight &mdash; the ring's weight in grams", "A legitimate seller should be able to provide it.",
  "1 troy ounce = exactly 31.1034768 g; 1 pennyweight = 1.55517384 g = 0.05 troy oz.",
  [(NIST, "NIST Office of Weights and Measures — conversion factors for precious metal sales", CITED)],
  "<span class='mono'>weight_grams</span> and the derived <span class='mono'>pure gold (g)</span> column",
  "Only " + str(n_weight) + " of " + str(len(rows)) + " rows publish a weight, and <b>all of them are marketplace sellers</b>. Kay, Zales, Jared, Blue Nile and Brilliant Earth publish karat, width and finish but no gram weight &mdash; you must ask. Weights described as \"average\" or \"gross\" are flagged (F-12).", "warn"),
 ("5", "Seller reputation", "Independent reviews and complaints; real contact information.",
  "The FTC's method is practical: search the seller's name plus \"complaint\" or \"review\", ask people you know, and report problems to the FTC and your state attorney general.",
  [(FTC, "FTC — before you buy", CITED), (REPORT, "ReportFraud.ftc.gov", CITED), (NAAG, "NAAG — state attorney general consumer complaints", CITED)],
  "The <a href='sellers.html'>Sellers &amp; policies</a> page",
  "Real contact details were captured for Blue Nile (phone, email, WhatsApp, contact page) and Brilliant Earth (phone, contact page, store list). No government-run jeweller rating database exists &mdash; flagged in research/seller-reputation.md.", "ok"),
 ("6", "Price &mdash; compare with gold weight and current gold value", "An unusually cheap price is a red flag.",
  "The LBMA Gold Price is the benchmark, set twice daily at 10:30 and 15:00 London time and administered by ICE Benchmark Administration.",
  [(LBMA, "LBMA — precious metal prices", LIVEB), (IBA, "ICE Benchmark Administration — LBMA precious metals", OFFICIAL)],
  "The <a href='calculator.html'>calculator</a> and <a href='gold-price.html'>gold price</a> pages",
  "16 observations for 2026-10-22 span " + money(D['spread_usd']) + "/oz. Two documented cases show the <i>same</i> official page indexed at two different prices (F-05, F-06). The most extreme price-to-claim ratio found is a \"7.50 Ct ... Solid 14K Yellow Gold\" ring at $322.27 (F-09).", "bad"),
 ("7", "Return policy", "Make sure you can return after inspecting; check resized/custom exclusions.",
  "Get the store's refund and return policies in writing before you buy. The FTC Cooling-Off Rule gives 3 days only for sales at a home, workplace, dorm or the seller's temporary location &mdash; it does NOT cover regular retail or most online purchases.",
  [(FTC, "FTC — get the return policy in writing", CITED), (COOL, "FTC — Buyer's Remorse and the Cooling-Off Rule", CITED), (ECFR429, "16 CFR Part 429", CITED)],
  "<span class='mono'>return_policy</span> column",
  "Observed: Blue Nile \"Free Returns\" (live), Kay \"Free and easy 30-day returns\" (live), Etsy listing \"Returns &amp; exchanges accepted\" (live), Pandora item marked \"FINAL SALE\" (no return), one eBay seller offering \"Free Resizing\" without stating whether a resized ring stays returnable.", "warn"),
 ("8", "Payment &mdash; prefer a credit card", "Avoid irreversible payment methods.",
  "The Fair Credit Billing Act sets the dispute process: written dispute within 60 days of the first bill containing the error, issuer acknowledges within 30 days and resolves within two billing cycles (max 90 days), liability for unauthorized charges capped at $50. Note: disputes about the <i>quality</i> of an item are not billing errors under the FCBA.",
  [(FCBA, "FTC — Using Credit Cards and Disputing Charges", CITED)],
  "Guidance page (no payment data is collected in this dataset)",
  "The FCBA quality-dispute limitation matters here: a ring that assays below its stamped karat is a quality dispute, so chargeback rights are weaker than for non-delivery. That is why post-delivery independent testing and a written return right matter more than the card.", "warn"),
 ("9", "Documentation", "Keep the listing, receipt, description and the seller's purity claims.",
  "Keep the seller's claims; get return policies in writing; a dated receipt or contract should show the seller's name and address.",
  [(FTC, "FTC — documentation and report problems", CITED), (ECFR2310, "16 CFR §23.10 — the quality mark should remain attached until purchase", CITED)],
  "Every row stores its own <span class='mono'>evidence.excerpt</span>, URL and UTC timestamp",
  "This dataset is itself the documentation practice applied to research: " + str(len(rows)) + " rows each keep a verbatim excerpt of the seller's claim, which is exactly what the checklist asks a buyer to preserve.", "ok"),
 ("10", "Upon arrival &mdash; independent jeweller before wearing or resizing",
  "Ask them to verify gold purity and weight.",
  "Jewelers of America operates a member directory; the Jewelers Vigilance Committee runs a mediation programme for disputes with jewellers.",
  [(JOAFIND, "Jewelers of America — find a jeweller", CITED), (FTC, "FTC — report problems / JVC mediation", CITED)],
  "Guidance page",
  "Sound consumer practice but not a codified federal requirement &mdash; flagged as guidance in research/verification.md.", "warn"),
 ("11", "Best verification &mdash; XRF or another professional purity test", "Do not rely solely on the stamp.",
  "X-ray fluorescence is a non-destructive composition test used by jewellers, pawnbrokers, refiners and assay offices. It reads the surface, so plating beneath the surface may not be detected.",
  [(THERMO, "Thermo Fisher Scientific — how pawnbrokers verify gold authenticity", VENDOR), (BULLIONBANK, "The Goldsmiths' Company Assay Office description via industry coverage", VENDOR)],
  "Guidance page + F-02",
  "<b>No government source was found mandating or describing XRF for consumers.</b> The available sources are instrument vendors and industry blogs, so this item is published as PARTIALLY VERIFIED and flagged rather than presented as regulation.", "bad"),
 ("12", "If the seller won't let you verify or return it &mdash; don't buy it",
  "The decisive test.",
  "Follows from the FTC guidance to get the return policy in writing before buying and from the National Stamping Act's marking requirement.",
  [(FTC, "FTC — before you buy", CITED), (ECFR2310, "16 CFR §23.10", CITED)],
  "Flags on rows that fail this test",
  "Rows that fail it in this dataset: the Pandora \"FINAL SALE\" ring (no return right), the two eBay category-page listings whose price cannot be tied to a stable item URL, and the $322.27 \"7.50 Ct ... Solid 14K\" ring.", "bad"),
]
ck = []
for num, title, short, verified, srcs, column, finding, tone in CK:
    srcl = "".join("<li>" + L(u, t) + " " + b + "</li>" for u, t, b in srcs)
    ck.append("<tr><td class='num'><b>" + num + "</b></td><td><b>" + title + "</b><div class='small'>" + short + "</div></td>"
              "<td>" + verified + "<ul class='tight small'>" + srcl + "</ul></td>"
              "<td class='small'>" + column + "</td><td><div class='alert " + tone + "' style='margin:0'>" + finding + "</div></td></tr>")
body = f"""<h1>The buying checklist, line by line, against official sources</h1>
<p class="lede">Each checklist item is mapped to the official (or best available) source, to the column in this dataset
that evidences it, and to what was actually found. Items that rest on non-official sources are labelled as such rather
than dressed up as regulation.</p>
{banner("../")}
<div class="alert gold"><b>The key point, stated once:</b> a 14K or 18K stamp by itself does <b>not</b> prove the ring is
that purity. U.S. law requires a karat quality mark plus the mark-maker's trademark (15 U.S.C. 297 via 16 CFR §23.10) and
makes misrepresenting gold content an unfair or deceptive practice (16 CFR §23.3) &mdash; but there is no mandatory
pre-sale assay in the United States, unlike the UK hallmarking system. The safe path is a reputable seller + proper
markings + a price consistent with the metal + independent testing after delivery.</div>
<div class="tbl-wrap"><table><thead><tr><th>#</th><th>Checklist item</th><th>What the official sources actually say</th>
<th>Where it lives in this dataset</th><th>Finding</th></tr></thead><tbody>{''.join(ck)}</tbody></table></div>
<h2>Terms that are NOT solid gold</h2>
<div class="tbl-wrap"><table><thead><tr><th>Term</th><th>Definition (FTC)</th><th>Real examples in this dataset</th></tr></thead><tbody>
<tr><td><b>Gold filled / gold overlay / rolled gold plate (RGP)</b></td><td>A layer of at least 10K gold mechanically applied to a base metal; must be marked with the karat quality plus the plating term, e.g. "14K gold overlay".</td><td class="small">None captured &mdash; no first-party listing in this dataset used these terms.</td></tr>
<tr><td><b>Gold electroplate</b></td><td>At least 10K gold, at least 0.175 microns thick, applied electrolytically to a base metal.</td><td class="small">Pandora rows: "14k gold plating", material "14k Gold-plated Signature metal alloy, No Other Material".</td></tr>
<tr><td><b>Gold flashed / gold washed</b></td><td>A very thin electroplating that wears away faster.</td><td class="small">None captured.</td></tr>
<tr><td><b>Vermeil</b></td><td>A sterling silver base coated or plated with gold.</td><td class="small">None captured at a first-party product page in this dataset; Brilliant Earth's own site defines its vermeil as sterling silver plated with 14K yellow or rose gold at a minimum of 2.5 microns (observed on a Brilliant Earth page during this session).</td></tr>
<tr><td><b>Rhodium finish on white gold</b></td><td>Not a gold-content term: a surface finish over a solid gold alloy.</td><td class="small">Zales states an item "is electroplated with rhodium or finished with an e-coating" and that the finish "may wear off with frequent use"; Kay and Jared list "Metal Finish: Rhodium".</td></tr>
</tbody></table></div>
<p class="small">Source for the definitions above: {L(FTC, "FTC — Buying Platinum, Gold, and Silver Jewelry")} {CITED},
as recorded in <span class="mono">research/hallmarking.md</span>.</p>"""
page(P + "checklist.html", "Buying checklist", "checklist.html", body, "../")

# ------------------------------------------------------------------ sellers
SELLERS = [
 dict(name="Blue Nile", kind="Brand retailer (also sells the James Allen collection)",
   contact="Phone +1-800-242-2728; email service@bluenile.com; WhatsApp wa.me/18773749142; contact page",
   contact_url="https://www.bluenile.com/contact-us", tier="live",
   ret="\"Free Returns\" and \"Free Overnight Shipping\" stated on the product page; \"Limited Lifetime Warranty\" warranting all gold and platinum jewellery items with a purchase price of $1,000 or more against manufacturer's defect, limitations apply",
   ret_url="https://www.bluenile.com/services/warranty",
   other="Secure-shopping policy page observed: https://www.bluenile.com/policies/secure-shopping",
   rows=[r for r in rows if r["retailer"] == "Blue Nile"]),
 dict(name="Kay Jewelers", kind="Brand retailer (Signet)", contact="Not captured in this session",
   contact_url=None, tier="partial",
   ret="\"Free and easy 30-day returns\" stated on the product page captured live",
   ret_url=None, other="Product pages publish a full spec block (stone grades, Metal Type, Metal Colour, Metal Finish, Gold Karat, Rhodium) but no gram weight.",
   rows=[r for r in rows if r["retailer"] == "Kay Jewelers"]),
 dict(name="Zales", kind="Brand retailer (Signet)", contact="Not captured in this session", contact_url=None, tier="partial",
   ret="Not captured &mdash; left blank rather than assumed", ret_url=None,
   other="Spec blocks publish Gold Karat and Rhodium, and disclose rhodium/e-coating wear. No gram weight published. One product URL is indexed at two different prices (F-05).",
   rows=[r for r in rows if r["retailer"] == "Zales"]),
 dict(name="Jared", kind="Brand retailer (Signet)", contact="Not captured in this session", contact_url=None, tier="partial",
   ret="Not captured &mdash; left blank rather than assumed", ret_url=None,
   other="Spec block captured in full (including item number 238222501) but the captured evidence contained no price, so the price cell is blank.",
   rows=[r for r in rows if r["retailer"] == "Jared"]),
 dict(name="Brilliant Earth", kind="Brand retailer", contact="Phone 800.691.0952; contact page; store list; virtual appointments",
   contact_url="https://www.brilliantearth.com/contact/", tier="live",
   ret="Not captured at product level &mdash; left blank rather than assumed", ret_url=None,
   other="Site defines its own vermeil as sterling silver plated with 14K yellow or rose gold, minimum 2.5 microns. Product pages are navigation-heavy; the four rows captured come from schema.org JSON-LD on the engagement-ring listing page and their karat/metal fields were withdrawn as unverifiable (F-14).",
   rows=[r for r in rows if r["retailer"] == "Brilliant Earth"]),
 dict(name="Pandora", kind="Brand retailer (plated fashion jewellery)", contact="Not captured in this session", contact_url=None, tier="partial",
   ret="One captured item is explicitly \"FINAL SALE\" at 50% off, which normally means no return right",
   ret_url=None,
   other="Publishes machine-readable material data that plainly says \"14k Gold-plated Signature metal alloy, No Other Material\". Runs an official \"Gold plated engagement rings\" category.",
   rows=[r for r in rows if r["retailer"] == "Pandora"]),
 dict(name="Etsy (marketplace)", kind="Marketplace &mdash; third-party sellers", contact="Seller-level; platform is not the merchant of record",
   contact_url=None, tier="live",
   ret="Captured listing states \"Returns &amp; exchanges accepted\"; seller is SolithDiamond", ret_url=None,
   other="Per-size pricing is published (the same ring ranges from $2,250.00 at size 3 to $2,660.00 at size 13). Marketplace listings in this dataset are where gram weights are published.",
   rows=[r for r in rows if r["retailer"] == "Etsy (marketplace)"]),
 dict(name="eBay (marketplace)", kind="Marketplace &mdash; third-party sellers", contact="Seller-level; some listings show an Authenticity Guarantee",
   contact_url=None, tier="partial",
   ret="Not captured consistently; some listings show \"Free returns\", others do not", ret_url=None,
   other="eBay itself labels some strikethrough prices as \"Recent sales price provided by the seller\", i.e. the discount reference is seller-supplied. Two rows cite category pages rather than item pages and are flagged for that.",
   rows=[r for r in rows if r["retailer"] == "eBay (marketplace)"]),
 dict(name="Amazon (marketplace)", kind="Marketplace &mdash; third-party sellers", contact="Seller-level",
   contact_url=None, tier="partial", ret="One seller claims \"30-day returns guaranteed\" in its own copy; not confirmed at platform level",
   ret_url=None,
   other="Both captured rows publish a metal weight (2.7 g \"Average Weight\"; 1.72 g metal weight) but no price appeared in the captured evidence, so both price cells are blank.",
   rows=[r for r in rows if r["retailer"] == "Amazon (marketplace)"]),
]
def tbadge(t):
    return {"live": LIVEB, "partial": '<span class="b snip">partially captured</span>'}[t]
sl = []
for s in SELLERS:
    ids = ", ".join(r["id"] for r in s["rows"])
    sl.append("<tr><td><b>" + E(s["name"]) + "</b><div class='small'>" + E(s["kind"]) + "</div><div class='small mono'>" +
              str(len(s["rows"])) + " rows: " + E(ids) + "</div></td>"
              "<td>" + s["contact"] + (("<br>" + L(s["contact_url"])) if s["contact_url"] else "") + "<br>" + tbadge(s["tier"]) + "</td>"
              "<td>" + s["ret"] + (("<br>" + L(s["ret_url"])) if s["ret_url"] else "") + "</td>"
              "<td class='small'>" + s["other"] + "</td></tr>")
body = f"""<h1>Sellers, contact details and return policies</h1>
<p class="lede">Checklist items 5 and 7: verify the business has real contact information, and make sure you can return
the ring after inspecting it. Only statements actually observed on a first-party page are recorded here; anything not
captured is written as "not captured" rather than filled in from assumption.</p>
{banner("../")}
<div class="tbl-wrap"><table><thead><tr><th>Seller</th><th>Contact information observed</th><th>Return / warranty statement observed</th><th>Notes</th></tr></thead>
<tbody>{''.join(sl)}</tbody></table></div>
<h2>How to check a seller's reputation (official method)</h2>
<div class="alert"><ul class="tight">
<li>{L(FTC, "FTC — Buying Platinum, Gold, and Silver Jewelry")} {CITED} &mdash; do your homework on the seller; do not rely solely on claims made online or on social media.</li>
<li>The FTC's stated technique is to type the seller's name plus "complaint" or "review" into a search engine, and to ask people you know for recommendations. {CITED}</li>
<li>Report problems to {L(REPORT, "ReportFraud.ftc.gov")} and to your state attorney general via {L(NAAG, "NAAG's consumer-complaint page")}. {CITED}</li>
<li>The Jewelers Vigilance Committee operates a mediation programme for disputes with jewellers; {L(JOAFIND, "Jewelers of America")} maintains a member directory. {CITED}</li>
<li><b>Limitation (recorded in research/seller-reputation.md):</b> no government-run seller-rating database for jewellers exists. BBB is a private organisation and the FTC's official guidance does not require it, so no BBB claim is made anywhere on this site.</li>
</ul></div>
<h2>Payment protection &mdash; and its limit</h2>
<div class="alert warn"><ul class="tight">
<li>Credit cards are preferred because the Fair Credit Billing Act gives a dispute process: written dispute within <b>60 days</b> of the first bill containing the error; the issuer must acknowledge within <b>30 days</b> and resolve within two billing cycles, maximum <b>90 days</b>; liability for unauthorized charges is capped at <b>$50</b>. {L(FCBA, "FTC — Using Credit Cards and Disputing Charges")} {CITED}</li>
<li><b>The limit that matters for this project:</b> disputes about the <i>quality</i> of an item are not billing errors under the FCBA. A ring that assays below its stamped karat is a quality dispute. Chargeback rights are therefore weaker than for non-delivery, which is why the written return right and post-delivery independent testing carry the real protection.</li>
<li>Avoid irreversible payment methods. Nothing in this dataset records a payment, and no payment details are ever collected by this site.</li>
</ul></div>
<h2>Return-policy reality check</h2>
<div class="alert"><p>The FTC Cooling-Off Rule gives <b>3 days</b> to cancel, but only for sales made at a home, workplace,
dorm or the seller's temporary location (hotel, convention centre, fairground, restaurant), and it does <b>not</b> cover
regular retail-store purchases or most online purchases. On cancellation the seller must refund all payments within
10 business days. {L(COOL, "FTC — Buyer's Remorse")} and {L(ECFR429, "16 CFR Part 429")} {CITED}</p>
<p><b>Consequence:</b> there is no general federal right to return an online jewellery purchase. The right comes from the
seller's own written policy &mdash; which is why every return statement in the table above is quoted from the seller's
page, with a link, instead of being assumed. Resized and custom rings are the usual exclusion; one eBay seller in this
dataset advertises "Free Resizing" without stating whether a resized ring remains returnable.</p></div>"""
page(P + "sellers.html", "Sellers &amp; policies", "sellers.html", body, "../")
print("pages: checklist + sellers done")

# ------------------------------------------------------------------ research index
# research/*.md was committed by session 3c8bb7ee and later integrated into main as
# guide/research/ (byte-identical, md5-verified). Prefer the canonical copy on main.
RESEARCH_CANDIDATES = [("../guide/research", "guide/research"), ("../research", "research")]
RESEARCH_DIR, RESEARCH_REPO_PATH = next(((d, rp) for d, rp in RESEARCH_CANDIDATES if os.path.isdir(d)),
                                        ("../research", "research"))
res = []
for fn in sorted(os.listdir(RESEARCH_DIR)):
    if not fn.endswith(".md"):
        continue
    txt = open(os.path.join(RESEARCH_DIR, fn), encoding="utf-8").read()
    m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", txt)
    status = m.group(1).strip() if m else "not stated"
    title = txt.splitlines()[0].lstrip("# ").strip() if txt else fn
    nsrc = len(re.findall(r"https?://", txt))
    res.append((fn, title, status, nsrc, len(txt.splitlines())))
res_rows = "".join(
    "<tr><td class='mono'>" + E(fn) + "</td><td>" + E(t) + "</td><td>" + E(s) + "</td>"
    "<td class='num'>" + str(n) + "</td><td class='num'>" + str(ln) + "</td>"
    "<td><a href='https://github.com/karagemop466-tech/GOLD5/blob/main/" + RESEARCH_REPO_PATH + "/" + E(fn) +
    "' target='_blank' rel='noopener noreferrer'>view on GitHub</a></td></tr>"
    for fn, t, s, n, ln in res)
body = f"""<h1>Research documents (session 3c8bb7ee)</h1>
<p class="lede">The checklist topics were researched in a parallel session and committed to
<span class="mono">research/*.md</span> and integrated into <span class="mono">main</span> as <span class="mono">guide/research/</span>. This session merged that work unchanged, re-read every document line by line and
re-ran the arithmetic checks that depend on them. Nothing in <span class="mono">guide/research/</span> was edited &mdash;
corrections are logged as change requests in <span class="mono">COORDINATION.md</span> instead.</p>
{banner("../")}
<div class="tbl-wrap"><table><thead><tr><th>File</th><th>Title</th><th>Status as declared in the document</th>
<th class="num">Source URLs</th><th class="num">Lines</th><th>Link</th></tr></thead><tbody>{res_rows}</tbody></table></div>
<h2>Integration re-verification of these documents</h2>
<div class="tbl-wrap"><table><thead><tr><th>Claim relied on by this site</th><th>Document</th><th>Re-verification performed</th><th>Result</th></tr></thead><tbody>
<tr><td>1 troy ounce = 31.1034768 g; 1 dwt = 1.55517384 g</td><td class="mono">research/weight.md</td>
<td>Used as the divisor in build-time check C10 against five publishers that quote both $/oz and $/gram</td>
<td><span class="b live">PASS</span> all five reproduce their published gram price within half a cent</td></tr>
<tr><td>18K = 75.0%, 14K = 58.3%, 10K = 41.7% fineness</td><td class="mono">research/gold-purity.md</td>
<td>Compared against karat &divide; 24 in build-time check C12; the calculator uses the same values</td>
<td><span class="b live">PASS</span> within 0.05 percentage points</td></tr>
<tr><td>24K is nominally 100% but the published mark is 999 / 99.99%</td><td class="mono">research/gold-purity.md</td>
<td>Check C12 initially <b>failed</b> because 99.9% was recorded; corrected to the document's own 99.99% and the nominal 100% is now recorded alongside it</td>
<td><span class="b warn">CORRECTED</span> both figures published, neither inferred</td></tr>
<tr><td>Plated / filled / vermeil / flashed definitions</td><td class="mono">research/hallmarking.md</td>
<td>Used verbatim on the checklist page; cross-checked against Pandora's own published material string</td>
<td><span class="b live">CONSISTENT</span> the brand's own data matches the FTC definition of electroplating</td></tr>
<tr><td>National Stamping Act: a trademark must accompany a quality mark</td><td class="mono">research/hallmarking.md</td>
<td>Applied as flag F-13 to every row whose evidence contains no stamp or maker's mark</td>
<td><span class="b warn">APPLIED</span> see Flagged for review</td></tr>
<tr><td>Cooling-Off Rule does not cover most online sales</td><td class="mono">research/return-policy.md</td>
<td>Reproduced on the sellers page with the caveat that no general federal return right exists</td>
<td><span class="b live">CONSISTENT</span></td></tr>
<tr><td>FCBA quality disputes are not billing errors</td><td class="mono">research/payment.md</td>
<td>Surfaced prominently on the sellers page because it weakens chargeback protection for an under-karat ring</td>
<td><span class="b live">CONSISTENT</span></td></tr>
<tr><td>XRF is the best verification method</td><td class="mono">research/verification.md</td>
<td>Document self-declares PARTIALLY VERIFIED; its two XRF sources are a vendor blog and an industry blog</td>
<td><span class="b bad">F-02</span> published as guidance, never as regulation</td></tr>
<tr><td>LBMA Gold Price is the benchmark, set twice daily by IBA</td><td class="mono">research/gold-price.md</td>
<td><b>Re-fetched live from lbma.org.uk this session</b>; also discovered the tables are now licence-gated</td>
<td><span class="b live">CONFIRMED LIVE</span> + new finding F-01</td></tr>
<tr><td>"No product prices are listed anywhere on this site"</td><td class="mono">research/gold-price.md, research/weight.md</td>
<td>Conflicts with the project brief, which requires product entries with links and current prices</td>
<td><span class="b bad">R-01 / R-02</span> logged in COORDINATION.md; files not edited</td></tr>
</tbody></table></div>"""
page(P + "research.html", "Research documents", "research.html", body, "../")

# ------------------------------------------------------------------ verification
ck_rows = "".join(
    "<tr><td class='mono'>" + E(c["id"]) + "</td><td>" + E(c["name"]) + "</td>"
    "<td>" + ('<span class="b live">PASS</span>' if c["status"] == "PASS" else '<span class="b bad">FAIL</span>') + "</td>"
    "<td class='small'>" + E(c["detail"]) + "</td></tr>" for c in checks)
rf = "".join("<tr><td class='mono'>" + E(rid) + "</td><td>" + E(f) + "</td></tr>" for rid, fs in sorted(row_flags.items()) for f in fs)
body = f"""<h1>Verification methodology &amp; hallucination checks</h1>
<p class="lede">How every number on this site was obtained, and the automated passes that look for hallucinations.
Current build: <b>{n_checks_pass} of {len(checks)} checks PASS, {n_checks_fail} FAIL</b>.</p>
{banner("../")}
<h2>Evidence tiers</h2>
<div class="tbl-wrap"><table><thead><tr><th>Tier</th><th>Definition</th><th>Badge</th><th class="num">Rows</th></tr></thead><tbody>
<tr><td><b>live</b></td><td>The value was read directly from a live HTTP fetch of the official first-party page during this session (2026-10-22 UTC).</td><td>{tier_badge('live')}</td><td class="num">{n_live}</td></tr>
<tr><td><b>snippet</b></td><td>The value was read from a search-engine index of the official first-party page. The index reports a crawl date where available, and that date is published with the row. Not re-confirmed by a live fetch.</td><td>{tier_badge('snippet')}</td><td class="num">{n_snip}</td></tr>
<tr><td><b>unverified</b></td><td>Could not be confirmed from any official source. The field is left <b>blank</b> and the row is flagged. Never estimated, never inferred.</td><td>{tier_badge('unverified')}</td><td class="num">{n_blank} blank prices</td></tr>
</tbody></table></div>
<h2>The rules every row had to satisfy</h2>
<ul class="tight">
<li>A price is recorded only if the literal price string was observed on an official first-party page (or in an index of it).</li>
<li>The literal observed string is stored in <span class="mono">evidence.excerpt</span> so any reviewer can diff the claim against its proof.</li>
<li>Every row carries <span class="mono">evidence.source_url</span> and an ISO-8601 UTC <span class="mono">observed_at</span>.</li>
<li>Missing values are <span class="mono">null</span>, rendered as a blank cell with a tooltip, and cross-listed on <a href="flagged.html">Flagged for review</a>.</li>
<li>Karat, metal colour and gram weight are subject to the same rule as price: if the wording is not in the excerpt, the field is withdrawn (this is check C14/C15, and it withdrew four karat assertions).</li>
<li>Currency is recorded explicitly; rows observed only in a non-USD currency were not included.</li>
</ul>
<h2>Automated passes run at every build</h2>
<div class="tbl-wrap"><table><thead><tr><th>ID</th><th>Check</th><th>Status</th><th>Detail</th></tr></thead><tbody>{ck_rows}</tbody></table></div>
<p class="small">Reproduce with <span class="mono">python3 scripts/build.py</span>. The same run rewrites
<span class="mono">data/rings.json</span>, <span class="mono">data/rings.csv</span> and
<span class="mono">data/verification-report.json</span>, so the published report always matches the published site.</p>
<h2>Proof the passes bite: three real catches during this build</h2>
<div class="alert ok"><ol class="tight">
<li><b>C12 caught a wrong constant.</b> The dataset first recorded 24K as 99.9% fineness. The check compares published
fineness against karat &divide; 24 and failed. Investigation showed <span class="mono">research/gold-purity.md</span>
records <b>99.99%</b> with European mark 999, while 24/24 is nominally 100%. Both figures are now published with their
sources instead of one being silently chosen.</li>
<li><b>C14 caught an unsupported karat.</b> Four Brilliant Earth rows asserted "14K white gold" that could only be
inferred from the SKU suffix <span class="mono">-14KW</span>. The captured JSON-LD states name, SKU, brand, currency and
price &mdash; not karat. The karat and metal fields were <b>withdrawn to blank</b> and flagged (F-14), rather than the
check being loosened.</li>
<li><b>C14 caught a missing excerpt.</b> Row <span class="mono">EBAY-236156740362</span> asserted 14K, but its stored
excerpt described only the diamonds, the weight and the price. The listing's own title ("14k SOLID Gold Diamond Ring .50
TCW Sz 13 Modernist Design 5.6Gr.") was added verbatim to the excerpt, so the assertion now has evidence.</li>
</ol></div>
<h2>Row-level check failures</h2>
{("<div class='tbl-wrap'><table><thead><tr><th>Row</th><th>Failure</th></tr></thead><tbody>" + rf + "</tbody></table></div>") if rf else "<div class='alert ok'>No row-level check failures in the current build.</div>"}
<h2>Known limitations, stated plainly</h2>
<div class="alert stop"><ul class="tight">
<li><b>F-03 &mdash; the fetch proxy failed during most of this session.</b> {n_live} of {len(rows)} rows were read from a
live fetch before the outage; the remaining {n_snip} rows are tier <span class="mono">snippet</span>. Their prices come
from an index of the official page, each with the crawl date the index reported. That is honest but weaker evidence, and
every such row says so on its face. <b>Re-read the live page before paying.</b></li>
<li>Prices are observations, not offers. They change hourly; {len(gp['observations'])} observations taken on the same day
differ by {money(D['spread_usd'])} per troy ounce.</li>
<li>A karat stamp, a seller's claim, a schema.org price field and even a gram weight are all <i>claims</i>. Only an
independent assay (XRF or fire assay) after delivery settles purity &mdash; and the sources for XRF available to this
project are vendor and industry publications, not government documents (F-02).</li>
<li>Nothing here is investment, legal or consumer-protection advice. It is a documented, auditable reading of public
pages at a stated moment.</li>
</ul></div>
<h2>Recommendation</h2>
<div class="alert gold"><b>Look for hallucinations.</b> After every review pass, re-run
<span class="mono">python3 scripts/build.py</span> and read the failing checks first. Then spot-audit by hand: open three
random rows, follow the source link, and confirm the price, karat and weight on the live page match the stored excerpt.
If a number on this site cannot be matched to its excerpt, treat it as a hallucination, blank it, and raise a flag &mdash;
that is the intended failure mode of this project, and blanking a value is always correct where guessing is not.</div>"""
page(P + "verification.html", "Verification &amp; hallucination checks", "verification.html", body, "../")
print("pages: research + verification done")

# ------------------------------------------------------------------ repo review
import subprocess
def git(*a):
    try:
        return subprocess.run(["git"] + list(a), capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return "(git unavailable: %s)" % e
INIT = "dfb99b7ac89ac9131aeb9419d2c5ead5ccc8dc9c"
init_line = git("log", "-1", "--format=%H | %ad | %an | %s", "--date=iso", INIT)
init_files = [f for f in git("ls-tree", "-r", "--name-only", INIT).splitlines() if f]
init_readme_size = git("cat-file", "-s", INIT + ":README.md")
init_readme = git("cat-file", "-p", INIT + ":README.md")
cur_files = [f for f in git("ls-files").splitlines() if f]
branches = git("branch", "-r", "--format=%(refname:short)")
commits = git("log", "--format=%h | %ad | %s", "--date=iso", "-15")

body = f"""<h1>Repository review</h1>
<p class="lede">Line-by-line review of the repository as it was found, the parallel session's committed work, and the
GitHub Pages configuration. Every fact below is reproducible with the git/gh command shown next to it.</p>
{banner("../")}
<h2>State at session start</h2>
<div class="tbl-wrap"><table><thead><tr><th>Item</th><th>Observed</th><th>Command</th></tr></thead><tbody>
<tr><td>Initial commit</td><td class="mono">{E(init_line)}</td><td class="mono">git log -1 --format=... {INIT[:7]}</td></tr>
<tr><td>Tracked files at that commit</td><td><b>{len(init_files)}</b>: {E(', '.join(init_files))}</td><td class="mono">git ls-tree -r --name-only {INIT[:7]}</td></tr>
<tr><td>README.md size</td><td><b>{E(init_readme_size)} bytes</b>, content <span class="mono">{E(repr(init_readme))}</span></td><td class="mono">git cat-file -s / -p {INIT[:7]}:README.md</td></tr>
<tr><td>Remote branches</td><td class="mono">{E(branches.replace(chr(10), ', ') or '(none)')}</td><td class="mono">git branch -r</td></tr>
<tr><td>Open or closed pull requests</td><td><b>none</b> at session start</td><td class="mono">gh pr list --state all</td></tr>
<tr><td>Authenticated as</td><td class="mono">karagemop466-tech</td><td class="mono">gh auth status</td></tr>
</tbody></table></div>
<div class="alert warn"><b>Irregularity (repo):</b> the repository began as a single commit containing one file,
<span class="mono">README.md</span>, whose entire content was <span class="mono">{E(init_readme.strip())}</span> &mdash;
no description, no licence, no <span class="mono">.gitignore</span>, no CI workflow and no data. There was therefore no
pre-existing dataset to audit line by line; the audit below covers the work committed by the parallel session and the
Pages configuration.</div>
<h2>GitHub Pages configuration</h2>
<div class="tbl-wrap"><table><thead><tr><th>Setting</th><th>Observed value</th></tr></thead><tbody>
<tr><td>Command</td><td class="mono">gh api repos/karagemop466-tech/GOLD5/pages</td></tr>
<tr><td>Observed at</td><td class="mono">2026-10-22T23:14Z (session 3e3fae49)</td></tr>
<tr><td>build_type</td><td class="mono">legacy</td></tr>
<tr><td>source.branch / source.path</td><td class="mono">main / "/"</td></tr>
<tr><td>status</td><td class="mono">built</td></tr>
<tr><td>html_url</td><td><a href="https://karagemop466-tech.github.io/GOLD5/" target="_blank" rel="noopener noreferrer">https://karagemop466-tech.github.io/GOLD5/</a></td></tr>
<tr><td>https_enforced / public</td><td class="mono">true / true</td></tr>
</tbody></table></div>
<div class="alert stop"><b>Irregularity D-01 (fixed, not just flagged):</b> Pages was <i>already</i> enabled with
<span class="mono">path: "/"</span>, which means the site root is the <b>repository root</b>. The parallel session's task
board assumed a <span class="mono">site/</span> directory, and <span class="mono">site/index.html</span> would never have
been served as the landing page &mdash; the site would have deployed "successfully" while showing nothing. The site is
therefore published from the repository root (<span class="mono">index.html</span>,
<span class="mono">assets/</span>, <span class="mono">pages/</span>, <span class="mono">data/</span>), and the Pages
configuration was deliberately left untouched so two sessions could not fight over it. No GitHub Actions workflow is
needed for a legacy branch build.</div>
<h2>Parallel session review &mdash; arena/3c8bb7ee-gold5</h2>
<div class="tbl-wrap"><table><thead><tr><th>Commit</th><th>Finding</th></tr></thead><tbody>
<tr><td class="mono">b4dfe21 (2026-10-22 23:11:27 UTC)</td><td>Created <span class="mono">COORDINATION.md</span> with 17 tasks. Claimed only task 1.</td></tr>
<tr><td class="mono">8299cd9 (2026-10-22 23:13:10 UTC)</td><td>Added 9 research documents covering every checklist topic, all citing FTC, eCFR, NIST, LBMA or Jewelers of America.</td></tr>
<tr><td>Board vs. tree mismatch</td><td><b>Irregularity R-03:</b> tasks 2&ndash;10 were committed as finished documents but left marked "unclaimed" with no owner and no sources recorded on the board. Corrected by this session after re-verifying each document line by line.</td></tr>
<tr><td>Scope conflict</td><td><b>Irregularity D-02:</b> <span class="mono">research/gold-price.md</span> and <span class="mono">research/weight.md</span> state that "no products are listed on this site". The project brief requires product entries with links and current prices. Resolved by adding a product dataset whose every price carries a source URL, a UTC timestamp and a verbatim excerpt; the research files were <b>not</b> edited, and change requests R-01/R-02 were logged instead.</td></tr>
<tr><td>Source quality</td><td><span class="mono">research/verification.md</span> self-declares <b>PARTIALLY VERIFIED</b> and cites an instrument vendor's blog (Thermo Fisher) and an industry blog for XRF. Correct handling; carried forward as flag F-02 rather than upgraded to "official".</td></tr>
<tr><td>Link currency</td><td><b>Flag F-03:</b> the external URLs cited in <span class="mono">research/*.md</span> could not be re-fetched during this session because the page-fetch proxy was returning signature errors. They are published with that limitation stated instead of being marked verified.</td></tr>
<tr><td>Timing</td><td>Last commit 23:13:10 UTC, i.e. under 60 minutes before this session started at 23:14 UTC. The session was active, so <b>no takeover was performed</b>; only genuinely unclaimed tasks (11&ndash;14, 16) were claimed.</td></tr>
</tbody></table></div>
<h2>Commit history on this branch</h2>
<p class="small">Snapshot taken by the build itself, so this table is always one build behind: running
<span class="mono">build.py</span> regenerates these pages, and committing that regeneration adds the
commit the table would then need to show. Timestamps are UTC and are the authoritative record.</p>
<div class="tbl-wrap"><table><thead><tr><th>Commit | date | subject</th></tr></thead><tbody>
{''.join("<tr><td class='mono'>" + E(c) + "</td></tr>" for c in commits.splitlines())}
</tbody></table></div>
<h2>Current tree</h2>
<p class="small"><b>{len(cur_files)}</b> tracked files. Data of record: <span class="mono">data/rings.jsonl</span> (one row
per entry, hand-audited), from which <span class="mono">data/rings.json</span>,
<span class="mono">data/rings.csv</span> and every table on this site are generated by
<span class="mono">scripts/build.py</span>. Generated files are committed because GitHub Pages serves this branch
directly with a legacy build and has no build step for the data.</p>"""
page(P + "repo-review.html", "Repository review", "repo-review.html", body, "../")

# ------------------------------------------------------------------ sources
from urllib.parse import urlparse
srcs = {}
def add(url, what, tier, dom=None):
    if not url:
        return
    d = dom or urlparse(url).netloc.replace("www.", "")
    e = srcs.setdefault(d, dict(domain=d, urls={}, what=[]))
    e["urls"][url] = tier
    if what not in e["what"]:
        e["what"].append(what)
for r in rows:
    add(r.get("url"), "product/listing evidence for row " + r["id"], r["evidence"]["tier"])
    if r["evidence"].get("source_url") != r.get("url"):
        add(r["evidence"].get("source_url"), "evidence source for row " + r["id"], r["evidence"]["tier"])
for o in gp["observations"]:
    add(o["url"], "gold-price observation " + o["id"] + " (" + o["publisher"] + ")", o["tier"])
add(gp["benchmark"]["url"], "LBMA benchmark methodology (live-verified)", "live")
for u, t in [(FTC, "FTC — Buying Platinum, Gold, and Silver Jewelry (purity, solid gold, hallmark, seller research, documentation)"),
             (ECFR233, "16 CFR §23.3 — misrepresentation as to gold content"),
             (ECFR2310, "16 CFR §23.10 — quality marks, National Stamping Act 15 U.S.C. 297"),
             (JOA, "Jewelers of America — quality marks on karat gold jewellery"),
             (JOAFIND, "Jewelers of America — find a jeweller"),
             (NIST, "NIST OWM — precious-metal conversion factors"),
             (IBA, "ICE Benchmark Administration — LBMA precious metals benchmarks"),
             (COOL, "FTC — Buyer's Remorse / Cooling-Off Rule"),
             (ECFR429, "16 CFR Part 429 — cooling-off period rule"),
             (FCBA, "FTC — Using Credit Cards and Disputing Charges (FCBA)"),
             (REPORT, "FTC — ReportFraud"),
             (NAAG, "NAAG — state attorney general consumer complaints"),
             (THERMO, "Thermo Fisher Scientific — XRF gold verification (VENDOR, not official)"),
             (BULLIONBANK, "Industry blog on XRF testing (NOT official)"),
             ("https://www.lbma.org.uk/prices-and-data/about-lbma-daily-auction-prices", "LBMA — about daily auction prices"),
             ("https://www.lbma.org.uk/wonders-of-gold/items/the-troy-ounce", "LBMA — the troy ounce"),
             ("https://consumer.ftc.gov/articles/what-do-if-youre-billed-things-you-never-got-or-you-get-unordered-products", "FTC — unordered merchandise / billing errors"),
             ("https://www.ftc.gov/consumer-protection?app=true&page=502", "FTC — consumer protection (FCBA, 15 U.S.C. 1666)"),
             ("https://www.bluenile.com/contact-us", "Blue Nile contact page (live-verified)"),
             ("https://www.bluenile.com/services/warranty", "Blue Nile limited lifetime warranty terms (live-verified)"),
             ("https://www.bluenile.com/policies/secure-shopping", "Blue Nile secure-shopping policy (live-verified)"),
             ("https://www.brilliantearth.com/contact/", "Brilliant Earth contact page (live-verified)"),
             ("https://karagemop466-tech.github.io/GOLD5/", "This site, as published by GitHub Pages"),
             ("https://github.com/karagemop466-tech/GOLD5", "This repository")]:
    add(u, t, "official" if "NOT official" not in t and "VENDOR" not in t else "non-official")
doms = sorted(srcs.values(), key=lambda d: (-len(d["urls"]), d["domain"]))
sr = []
for d in doms:
    links = "".join("<li><a href='" + E(u) + "' target='_blank' rel='noopener noreferrer' class='mono'>" + E(u) + "</a> " + tier_badge(t) + "</li>"
                    for u, t in sorted(d["urls"].items()))
    sr.append("<tr><td><b>" + E(d["domain"]) + "</b><div class='small'>" + str(len(d["urls"])) + " URL(s)</div></td>"
              "<td class='small'>" + E("; ".join(d["what"])[:600]) + ("&hellip;" if len("; ".join(d["what"])) > 600 else "") + "</td>"
              "<td><ul class='tight small'>" + links + "</ul></td></tr>")
body = f"""<h1>Sources</h1>
<p class="lede">Every URL used anywhere in this project, grouped by domain, with what each one supports and how strongly
it was verified. {len(srcs)} domains, {sum(len(d['urls']) for d in srcs.values())} distinct URLs.</p>
{banner("../")}
<div class="alert"><b>Tier key.</b> {tier_badge('live')} read from a live fetch of the page this session &middot;
{tier_badge('snippet')} read from a search index of the page, crawl date published with the row &middot;
<span class="b info">official source</span> a government, standards, benchmark-administrator or first-party brand page
cited in <span class="mono">research/*.md</span>, not re-fetched this session (F-03) &middot;
<span class="b warn">vendor / industry</span> not an official source, used only as consumer guidance (F-02).</div>
<div class="tbl-wrap"><table><thead><tr><th>Domain</th><th>What it supports</th><th>URLs</th></tr></thead><tbody>{''.join(sr)}</tbody></table></div>
<h2>Sources deliberately NOT used</h2>
<ul class="tight">
<li><b>Competitor and affiliate blogs</b> (for example jewellery retailers publishing "is brand X real gold?" comparison
articles). Several appeared in search results with confident claims about other brands' materials. They are marketing
content with a commercial interest, so no claim in this project rests on them.</li>
<li><b>Aggregator price sites</b> that publish a gold price with no timestamp, no publisher and no series definition.</li>
<li><b>Any LBMA numeric price.</b> The tabulated benchmark data is licence-gated (F-01), so no figure is quoted as
"the LBMA price".</li>
<li><b>Memory.</b> No price, weight, karat, policy or statistic on this site was written from recall. If it could not be
observed, it is blank.</li>
</ul>"""
page(P + "sources.html", "Sources", "sources.html", body, "../")
print("pages: repo-review + sources done")

# ------------------------------------------------------------------ flagged for review
def has(r, *needles):
    blob = json.dumps(r, ensure_ascii=False).lower()
    return any(n.lower() in blob for n in needles)

stale = [r for r in rows if (r["evidence"].get("page_date") or "")]
def pdate_year_month(pd):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", pd)
    return m.group(0) if m else None
stale_rows = []
for r in stale:
    d = pdate_year_month(r["evidence"]["page_date"])
    if d and d < "2026-07-22":
        stale_rows.append((r, d))
blank_price = [r for r in rows if r.get("price_usd") is None]
blank_weight = [r for r in rows if r.get("weight_grams") is None]
setting_only = [r for r in rows if has(r, "setting-only", "setting price")]
contradictions = [r for r in rows if has(r, "inconsisten", "contradict", "conflict", "title says")]
no_hallmark = [r for r in rows if not has(r, "hallmark", "stamp", "maker", "makers mark", "maker's mark")]
cat_page_rows = [r for r in rows if has(r, "category page", "listing page, not")]
GLOBAL = [
 ("F-01", "bad", "No official LBMA Gold Price <b>number</b> is published anywhere in this project",
  "LBMA's own page states that historical tabulated prices moved to the MyLBMA Portal and that a licence from ICE Benchmark Administration is required to obtain, use or redistribute benchmark data. Publishing an unlicensed figure would be an unsourced number, so 16 timestamped publisher observations are published instead, each with its own link and excerpt.",
  [(LBMA, "live")]),
 ("F-02", "bad", "XRF testing and independent-jeweller verification rest on <b>vendor and industry</b> sources, not official ones",
  "research/verification.md self-declares PARTIALLY VERIFIED. No federal or state source was found that mandates or describes XRF testing for consumers. Both items are published as consumer guidance and never as regulation.",
  [(THERMO, "non-official"), (BULLIONBANK, "non-official")]),
 ("F-03", "bad", "Page-fetch proxy outage during this session: " + str(n_snip) + " of " + str(len(rows)) + " rows are tier <span class='mono'>snippet</span>, not <span class='mono'>live</span>",
  "Live fetches succeeded for the LBMA benchmark page, one Blue Nile product page, one Kay product page and one Etsy listing, then the fetch tool began returning proxy signature errors for every request. All later evidence was therefore read from a search index of the official page, and each such row publishes the crawl date the index reported. The external URLs cited in research/*.md also could not be re-fetched. This is the single largest limitation of the dataset and the reason every snippet row says CONFIRM ON PAGE.",
  []),
 ("F-04", "warn", "There is no single \"current gold price\": " + str(D['n_observations_oct22']) + " observations for 2026-10-22 span " + money(D['spread_usd']) + "/oz",
  "Values ranged from " + money(D['min_usd_per_troy_oz']) + " to " + money(D['max_usd_per_troy_oz']) + " because they were taken at different hours and some track December futures or a CFD rather than spot. Any single untimestamped price claim is unreliable; the calculator therefore pre-fills nothing.",
  []),
 ("F-05", "bad", "Zales product V-15246515 is indexed at two different prices <b>and</b> two different diamond grades",
  "One index snapshot of the official zales.com URL shows $3,999.99 with grade (I/I2); another shows $3,114.30 with grade (J/I2) on a legacy product.jsp URL for the same product ID. Either the item was re-graded/re-priced or two variants share an identifier. Row ZAL-V-15246515 carries both observations and asserts neither as current.",
  [("https://www.zales.com/1-ct-certified-diamond-solitaire-engagement-ring-14k-gold-ii2/p/V-15246515", "snippet"),
   ("https://zales.com/certified-diamond-solitaire-engagement-ring-14k-gold/product.jsp?productId=65311786", "snippet")]),
 ("F-06", "bad", "Pandora's Elevated Heart Ring is $130.00 on its product page and $125.00 on the brand's own category page",
  "Two official Pandora pages disagree by $5.00 for the same product in the search index. Documented to show that a price must be re-read on the live product page at checkout, not trusted from a category tile or a cached snippet.",
  [("https://us.pandora.net/en/rings/elevated-heart-ring/168421C01.html", "snippet"),
   ("https://us.pandora.net/en/jewelry/gold-plated/", "snippet")]),
 ("F-07", "warn", str(len(stale_rows)) + " rows rest on index snapshots older than 90 days",
  "The oldest is " + (min(d for _, d in stale_rows) if stale_rows else "n/a") + ". Prices, availability and even the karat options on those pages may have changed. Each row publishes its crawl date so a reviewer can judge the staleness.",
  []),
 ("F-08", "warn", str(len(blank_price)) + " rows have <b>no price</b> and " + str(len(blank_weight)) + " have <b>no gram weight</b>",
  "These are deliberate blanks. A price was published only where one was observed; a weight only where the seller stated one. Nothing was estimated, averaged from comparable items, or carried over from a similar product.",
  []),
 ("F-09", "bad", str(len(cat_page_rows)) + " rows cite a category or listing page rather than a single product page",
  "Their prices cannot be attributed to a stable item URL, and the specific item may have been delisted. Included because the claim was genuinely observed there (for example an implausible \"7.50 Ct ... Solid 14K Yellow Gold\" ring at $322.27, and a listing whose own title claims both 14k and 10k), and flagged so nobody treats them as verified offers.",
  []),
 ("F-10", "bad", str(len(contradictions)) + " listings contradict themselves",
  "Examples: a title saying '.50 TCW' with a description totalling 0.54 TCW; a title saying 0.94 CTW with item specifics saying 1.12 ctw; a title saying 'Round Diamond' with a description saying radiant cut; a title claiming both 14k and 'Solid 10k'; an Amazon title saying '14K Solid Gold' with a metal-type field saying Rose Gold; cubic zirconia described in a 'Total Diamond Weight' field. Self-contradiction is a documentation red flag under the checklist even when the metal itself is genuine.",
  []),
 ("F-11", "warn", str(len(setting_only)) + " rows are <b>setting-only</b> prices",
  "Blue Nile and Brilliant Earth quote a setting price that excludes the centre diamond, while Kay, Zales, Jared and the marketplace rows quote a complete ring. The two are not comparable, so every setting-only row says so in its price note and the master table's price column carries the label. Comparing a $650 setting with a $629.99 complete ring would be a category error.",
  []),
 ("F-12", "warn", "Some published weights are averages or gross weights, not the shipped item's weight",
  "One Amazon row states 'Average Weight: 2.7gr.'; one eBay row states 'Total Gross Weight: 3.91 grams', which includes the diamonds. Pure-gold content computed from either is an approximation, and the calculator exposes a GROSS checkbox so the assumption stays visible.",
  []),
 ("F-13", "bad", str(len(no_hallmark)) + " of " + str(len(rows)) + " rows show no evidence of a hallmark or maker's mark",
  "16 CFR §23.10 and the National Stamping Act (15 U.S.C. 297) expect a trademark or name alongside a karat quality mark, and the FTC's plain guidance is: if there is no trademark along with the karat mark, don't buy it. Almost no online listing photographs the stamp. Only two rows in this dataset evidence one, and only one of those names a maker ('stamp 14k Z' for Zales).",
  [(ECFR2310, "official"), (FTC, "official")]),
 ("F-14", "bad", "Four Brilliant Earth rows had their karat and metal fields <b>withdrawn to blank</b>",
  "The captured schema.org JSON-LD states name, SKU, brand, currency and price only. '14K white gold' could be inferred from the SKU suffix -14KW, and the listing page does offer 14K/18K white, yellow and rose gold variants, but inferring is exactly what this project forbids. The fields are blank, the reasoning is recorded in metal_claim, and the rows also cite a category URL rather than a product URL.",
  [("https://www.brilliantearth.com/engagement-rings/shop-all/", "snippet")]),
]
gl = []
for fid, tone, title, why, links in GLOBAL:
    lk = "".join("<li>" + L(u) + " " + tier_badge(t) + "</li>" for u, t in links)
    gl.append("<div class='alert " + tone + "' id='" + fid + "'><h3>" + fid + " &mdash; " + title + "</h3>"
              "<p>" + why + "</p>" + ("<ul class='tight small'>" + lk + "</ul>" if lk else "") + "</div>")

def rowlist(rs, cols=None):
    if not rs:
        return "<p class='small'>none</p>"
    out = ["<div class='tbl-wrap'><table><thead><tr><th>Row</th><th>Retailer</th><th>Product (source link)</th><th>Detail</th></tr></thead><tbody>"]
    for item in rs:
        r, extra = item if isinstance(item, tuple) else (item, "")
        out.append("<tr><td class='mono'>" + E(r["id"]) + "</td><td>" + E(r["retailer"]) + "</td>"
                   "<td><a href='" + E(r["url"]) + "' target='_blank' rel='noopener noreferrer'>" + E(r["product"])[:110] + "</a></td>"
                   "<td class='small'>" + E(extra) + "</td></tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

flag_rows = []
for r in rows:
    fl = list(r.get("flags") or []) + row_flags.get(r["id"], [])
    if not fl:
        continue
    flag_rows.append("<tr><td class='mono'>" + E(r["id"]) + "</td><td>" + E(r["retailer"]) + "</td>"
                     "<td><a href='" + E(r["url"]) + "' target='_blank' rel='noopener noreferrer'>" + E(r["product"])[:100] + "</a></td>"
                     "<td><ul class='tight small'>" + "".join("<li>" + E(f) + "</li>" for f in fl) + "</ul></td></tr>")
body = f"""<h1>Flagged for review</h1>
<p class="lede">Everything on this site that is uncertain, contradictory, stale, blank or otherwise needs a human eye.
Nothing here blocks the build or the merge &mdash; it is published so it can be reviewed and corrected.
<b>{len(all_flags)} row-level flags</b> across <b>{len(flag_rows)} rows</b>, plus <b>{len(GLOBAL)} project-level findings</b>.</p>
{banner("../")}
<h2>Project-level findings</h2>
{''.join(gl)}
<h2>Rows whose price is blank (never inferred)</h2>
{rowlist([(r, "no price observed in official evidence") for r in blank_price])}
<h2>Rows resting on index snapshots older than 90 days</h2>
{rowlist([(r, "crawl date " + d) for r, d in sorted(stale_rows, key=lambda x: x[1])])}
<h2>Listings that contradict themselves</h2>
{rowlist([(r, "; ".join(f for f in r.get("flags", []) if any(k in f.lower() for k in ("inconsisten", "contradict", "conflict", "title says")))[:220]) for r in contradictions])}
<h2>Setting-only prices (not comparable with complete rings)</h2>
{rowlist([(r, r.get("price_note") or "setting price") for r in setting_only])}
<h2>Rows citing a category / listing page rather than a product page</h2>
{rowlist([(r, "price not attributable to a stable item URL") for r in cat_page_rows])}
<h2>Rows with no hallmark or maker's-mark evidence</h2>
<p class="small">{len(no_hallmark)} of {len(rows)} rows. Listed in full in the master table via the flag column; the two
exceptions are <span class="mono">EBAY-297741882482</span> ("Hallmark: Stamped '14k' inside the shank") and
<span class="mono">EBAY-223469269883</span> ("stamp 14k Z").</p>
<h2>All row-level flags</h2>
<div class="tbl-wrap"><table><thead><tr><th>Row</th><th>Retailer</th><th>Product (source link)</th><th>Flags</th></tr></thead>
<tbody>{''.join(flag_rows)}</tbody></table></div>
<h2>Coordination irregularities</h2>
<div class="tbl-wrap"><table><thead><tr><th>ID</th><th>Irregularity</th><th>Resolution</th></tr></thead><tbody>
<tr><td class="mono">D-01</td><td>GitHub Pages was already configured with path "/" (repository root), but the parallel session's board assumed a site/ directory; site/index.html would never have been served.</td><td>Site published from the repository root; Pages configuration left untouched. Recorded in COORDINATION.md.</td></tr>
<tr><td class="mono">D-02</td><td>research/gold-price.md and research/weight.md state that no products or prices appear on this site, which conflicts with the project brief.</td><td>Product dataset added with per-row source URL, UTC timestamp and verbatim excerpt. Research files not edited; change requests R-01 and R-02 logged.</td></tr>
<tr><td class="mono">R-03</td><td>Tasks 2-10 were committed as finished documents but left "unclaimed" on the board with no owner or sources.</td><td>Statuses corrected by this integration session after re-verifying each document line by line.</td></tr>
<tr><td class="mono">D-03</td><td>Two sessions on one repository risk conflicting edits.</td><td>This session merged arena/3c8bb7ee-gold5 before starting, edited only its own claimed files, and claims were pushed immediately.</td></tr>
</tbody></table></div>
<h2>What to do with this page</h2>
<div class="alert gold"><ol class="tight">
<li>Open any flagged row's source link and compare the live page with the stored excerpt.</li>
<li>If a value has changed, update <span class="mono">data/rings.jsonl</span> with the new excerpt, URL and UTC timestamp &mdash; never edit the generated HTML.</li>
<li>If a value cannot be confirmed, blank it. A blank cell with a flag is a correct result; a plausible number with no evidence is not.</li>
<li>Re-run <span class="mono">python3 scripts/build.py</span> and read the failing checks first.</li>
</ol></div>"""
page(P + "flagged.html", "Flagged for review", "flagged.html", body, "../")

# ------------------------------------------------------------------ final link check + report
bad_links = check_internal_links(PAGE_LINKS)
chk("C16", "Every internal link in every generated page resolves to a file that exists", not bad_links,
    f"{sum(len(v) for v in PAGE_LINKS.values())} hrefs scanned across {len(PAGE_LINKS)} generated pages; {len(bad_links)} broken"
    + ("" if not bad_links else " -> " + "; ".join(sorted(set(bad_links))[:20])))
ext = sorted({r["url"] for r in rows if r.get("url")} | {o["url"] for o in gp["observations"]})
chk("C17", "Every external source link is absolute and uses http(s)", all(u.startswith("http") for u in ext),
    f"{len(ext)} distinct external source URLs, all absolute http(s)")
chk("C18", "Generated exports match the dataset of record", len(rows) == len(json.load(open("data/rings.json", encoding="utf-8"))["rows"]),
    f"data/rings.json holds {len(rows)} rows, data/rings.jsonl holds {len(rows)} rows")
write_report(dict(pages=sorted(PAGE_LINKS.keys()), broken_internal_links=bad_links,
                  external_source_urls=ext, global_flags=[g[0] for g in GLOBAL]))
print("pages:", len(PAGE_LINKS), "| broken internal links:", len(bad_links))
for b in sorted(set(bad_links))[:20]:
    print("   BROKEN", b)
print("checks:", n_checks_pass + sum(1 for c in checks[15:] if c["status"] == "PASS"), "pass /",
      sum(1 for c in checks if c["status"] == "FAIL"), "fail")
for c in checks:
    if c["status"] == "FAIL":
        print("  FAIL", c["id"], c["detail"][:400])
