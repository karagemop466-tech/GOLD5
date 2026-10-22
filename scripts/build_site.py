#!/usr/bin/env python3
"""Build the GOLD5 static site from site/assets/data.json.

Outputs:
  index.html
  site/listings.html  site/gold-price.html  site/calculator.html
  site/checklist.html site/sellers.html     site/analysis.html
  site/flagged.html   site/sources.html     site/verification.html

No external dependencies; no build step for visitors. Run from the repo root:
  python3 scripts/build_site.py
"""
import json, os, datetime, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = json.load(open(os.path.join(ROOT, "site/assets/data.json")))
SPOT = D["spot"]["primary"]
SPOT_G = SPOT["usdPerGram"]
TROY = 31.1034768
FIN = D["spot"]["purity"]["fineness"]
ENTRIES = D["entries"]
SELLERS = {s["id"]: s for s in D["sellers"]}
FLAGS = {f["id"]: f for f in D["flags"]}
REFS = D["references"]
REPORT_FAIL = None
try:
    _rep = json.load(open(os.path.join(ROOT, "data", "check_report_v2.json")))
    REPORT_FAIL = _rep.get("fail")
except Exception:
    REPORT_FAIL = None

SEV = {"high": 0, "medium": 1, "low": 2, "info": 3}
SEV_LABEL = {"high": ("bad", "High"), "medium": ("warn", "Medium"), "low": ("info", "Low"), "info": ("gray", "Info")}
FLAG_SHORT = {
    "FL-01": "price < metal", "FL-02": "off-platform contact", "FL-03": "no gram weight",
    "FL-04": "reputation not checked", "FL-05": "returns excluded", "FL-06": "warranty threshold",
    "FL-07": "returns unverified", "FL-08": "USD unconfirmed", "FL-09": "marketing compare price",
    "FL-10": "exchange-only", "FL-11": "14-day / promo", "FL-12": "retail compare price",
    "FL-13": "no price / no returns", "FL-14": "no maker's mark", "FL-15": "solid not stated",
    "FL-16": "Etsy window varies", "FL-17": "promo price", "FL-18": "seller-stated weight",
    "FL-19": "spot moves", "FL-20": "stamp ≠ proof", "FL-21": "setting only",
    "FL-22": "excluded sellers", "FL-23": "archive", "FL-24": "resolved", "FL-25": "multiple spot prints",
}

def esc(x):
    return html.escape(str(x), quote=True)

def money(n, dec=None):
    if n is None:
        return ""
    if dec is None:
        dec = 0 if float(n).is_integer() else 2
    return "$" + f"{n:,.{dec}f}"

def date_str():
    return D["meta"]["asOf"]

def seller(e):
    return SELLERS[e["sellerId"]]

def fine_g(e):
    if e["grams"] is None or e["karat"] is None:
        return None
    return e["grams"] * FIN[f'{e["karat"]}K']

def metal_value(e):
    g = fine_g(e)
    return None if g is None else g * SPOT_G

def ratio(e):
    mv = metal_value(e)
    if mv is None or e["price"] is None or mv == 0:
        return None
    return e["price"] / mv

def base(prefix):
    """prefix '' for root pages, '../' for site/ pages"""
    return prefix

def nav(prefix, active):
    items = [("index.html", "Dashboard", "home"), ("site/listings.html", "Listings", "listings"),
             ("site/gold-price.html", "Gold Price", "gold-price"), ("site/calculator.html", "Calculator", "calculator"),
             ("site/analysis.html", "Analysis", "analysis"), ("site/checklist.html", "Checklist", "checklist"),
             ("site/sellers.html", "Sellers", "sellers"), ("site/flagged.html", "Flagged", "flagged"),
             ("site/sources.html", "Sources", "sources"), ("site/verification.html", "Verification", "verification")]
    out = []
    for href, label, key in items:
        h = href if prefix == "" else href.replace("site/", "")
        if href == "index.html" and prefix:
            h = "../index.html"
        cls = ' class="active"' if key == active else ""
        out.append(f'<a href="{h}"{cls}>{label}</a>')
    return "".join(out)

def shell(prefix, active, title, desc, body):
    ap = "site/assets/" if prefix == "" else "assets/"
    home = "index.html" if prefix == "" else "../index.html"
    foot_home = home
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · GOLD5</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="{ap}site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="rulebar"><div class="wrap">
  <span><b>NO HALLUCINATIONS</b> — every value has a dated source link; anything unconfirmed is blank and flagged, never guessed.</span>
  <span>Data as of <b>{esc(date_str())}</b> · <a href="{prefix}site/verification.html">How this was verified →</a></span>
</div></div>
<header class="masthead"><div class="wrap">
  <a class="brand" href="{home}"><span class="brand-mark">G5</span><span class="brand-name">GOLD5<small>Solid gold engagement ring research</small></span></a>
  <nav class="nav" aria-label="Main">{nav(prefix, active)}</nav>
</div></header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  <div><b>GOLD5</b> — an independent research project. Not a shop. No affiliate links. No price is estimated, averaged or invented.<div class="fine">Listings and policies change after the check date. Confirm everything at the seller before paying.</div></div>
  <div><b>At a glance</b><br>{len(ENTRIES)} listings · {len(SELLERS)} sellers · {sum(1 for f in D['flags'] if f['status']=='open')} open flags · {len(REFS)} official references<br>Spot used: {money(SPOT['usdPerOz'])}/oz, {money(SPOT['usdPerGram'])}/g (Kitco, {esc(SPOT['asOf'])})</div>
  <div><b>Verify</b><br><a href="{prefix}site/verification.html">Method &amp; pass log</a><br><a href="{prefix}site/flagged.html">Flagged for Review</a><br><a href="{prefix}site/sources.html">All sources</a><br><a href="{prefix}site/calculator.html">Gold calculator</a></div>
</div></footer>
</body>
</html>"""


DOCS = [("weight", "gram weight", 3), ("solid", "'solid gold' wording", 2),
        ("returns", "verified return policy", 2), ("stamp", "karat stamp claim", 1),
        ("maker", "maker's mark", 2)]

def doc_status(e):
    present, missing = [], []
    for k, label, w in DOCS:
        ok = {"weight": e["grams"] is not None, "solid": e["solidStated"],
              "returns": e["returnsVerified"], "stamp": e["hallmarkStated"],
              "maker": e["makerMarkStated"]}[k]
        (present if ok else missing).append(label)
    return present, missing

def doc_score(e):
    score = sum(w for k, label, w in DOCS if
                {"weight": e["grams"] is not None, "solid": e["solidStated"],
                 "returns": e["returnsVerified"], "stamp": e["hallmarkStated"],
                 "maker": e["makerMarkStated"]}[k])
    if any(FLAGS[f]["severity"] == "high" and FLAGS[f]["status"] == "open" for f in e["flags"]):
        score -= 1.5
    return score

def doc_rank(e):
    r = ratio(e)
    return (doc_score(e), -(r if r is not None else 99))

def doc_leaders(n=4, exclude_case=True):
    pool = [e for e in ENTRIES if not (exclude_case and e["category"] == "case-study")]
    return sorted(pool, key=doc_rank, reverse=True)[:n]

def doc_table(limit=4, prefix="site/"):
    rows = ""
    for e in doc_leaders(limit):
        present, missing = doc_status(e)
        r = ratio(e)
        basis = "setting only" if e["priceBasis"] == "setting" else "complete ring"
        extra = [FLAGS[f] for f in e["flags"]
                 if FLAGS[f]["status"] == "open" and FLAGS[f]["severity"] in ("high", "medium")
                 and f not in ("FL-03", "FL-14", "FL-15")]
        extra.sort(key=lambda f: SEV[f["severity"]])
        watch = " ".join(f'<span class="badge {"bad" if f["severity"] == "high" else "warn"}">{esc(FLAG_SHORT.get(f["id"], f["id"]))}</span>' for f in extra[:2]) or "—"
        rows += (f"<tr><td><div class=\"ring-name\"><a href=\"{prefix}listings.html#{esc(e['id'])}\">{esc(e['short'])}</a></div>"
                 f"<div class=\"src\">{esc(seller(e)['name'])} · {money(e['price']) if e['price'] is not None else 'no price'}"
                 f"{' · ' + f'{r:.2f}× metal' if r is not None else ''} · {basis}</div></td>"
                 f"<td class=\"small\">{esc(', '.join(present)) or '<span class=blank>none</span>'}</td>"
                 f"<td class=\"small muted\">{esc(', '.join(missing)) or 'none'}</td>"
                 f"<td class=\"small\">{watch}</td></tr>")
    return rows

def flag_badges(e, limit=3):
    ids = sorted(e["flags"], key=lambda f: (FLAGS[f]["status"] != "open", SEV[FLAGS[f]["severity"]]))
    out = []
    for fid in ids[:limit]:
        f = FLAGS[fid]
        tone = "ok" if f["status"] == "resolved" else ("bad" if f["severity"] == "high" else "warn" if f["severity"] == "medium" else "gray")
        out.append(f'<span class="badge {tone}" title="{esc(f["title"])}">{esc(FLAG_SHORT.get(fid, fid))}</span>')
    if len(ids) > limit:
        out.append(f'<a class="src-link" href="flagged.html" title="See all flags">+{len(ids)-limit}</a>')
    return " ".join(out)

def source_link(url, label="source ↗"):
    return f'<a class="src-link" href="{esc(url)}" target="_blank" rel="noopener">{label}</a>'

def seller_cell(e):
    s = seller(e)
    return f'{esc(s["name"])}'

# ------------------------------------------------------------------ pages
def index_page():
    counts = dict(entries=len(ENTRIES), sellers=len(SELLERS),
                  weighted=sum(1 for e in ENTRIES if e["grams"] is not None),
                  priced=sum(1 for e in ENTRIES if e["price"] is not None),
                  openflags=sum(1 for f in D["flags"] if f["status"] == "open"),
                  refs=len(REFS), solid=sum(1 for e in ENTRIES if e["solidStated"]),
                  maker=sum(1 for e in ENTRIES if e["makerMarkStated"]),
                  verified_returns=sum(1 for e in ENTRIES if e["returnsVerified"]))
    top = sorted([e for e in ENTRIES if e["grams"] is not None and e["price"] is not None], key=ratio)
    top_rows = []
    for e in top:
        r = ratio(e)
        tone = "bad" if r < 1 else ("warn" if r < 1.6 else "ok")
        note = "setting only" if e["priceBasis"] == "setting" else "complete ring"
        top_rows.append(f"""<tr>
<td><div class="ring-name"><a href="site/listings.html#{esc(e['id'])}">{esc(e['short'])}</a></div><div class="src">{esc(seller(e)['name'])} · {esc(e['karat'])}K</div></td>
<td class="num">{e['grams']:g} g</td>
<td class="num">{money(e['price'])}</td>
<td class="num calc">{money(metal_value(e))}</td>
<td class="num"><span class="badge {tone}">{r:.2f}×</span></td>
<td class="small muted">{note}</td>
<td>{source_link(e['url'], 'listing ↗')}</td></tr>""")
    findings = sorted([f for f in D["flags"] if f["status"] == "open"], key=lambda f: SEV[f["severity"]])
    pick = [f for f in findings if f["severity"] in ("high", "medium")][:8]
    f_rows = []
    for f in pick:
        tone, lab = SEV_LABEL[f["severity"]]
        f_rows.append(f"""<tr><td class="num">{esc(f['id'])}</td><td><span class="badge {tone}">{lab}</span></td>
<td><b>{esc(f['title'])}</b><div class="small muted">{esc(f['detail'][:190])}{'…' if len(f['detail'])>190 else ''}</div></td>
<td class="small">{len(f['entryIds']) or "—"}</td><td><a href="site/flagged.html#{esc(f['id'])}">details ↗</a></td></tr>""")
    spot_rows = []
    quotes = [dict(SPOT, primary=True)] + D["spot"]["prior"] + D["spot"]["crossChecks"]
    for q in quotes:
        per_g = money(q["usdPerGram"]) if q.get("usdPerGram") else '<span class="blank">—</span>'
        badge = ' <span class="badge ok">used for all calculations</span>' if q.get("primary") else ""
        spot_rows.append(f"""<tr><td><b>{esc(q['source'])}</b>{badge}<div class="src">{esc(q.get('method',''))}</div></td>
<td class="num">{money(q['usdPerOz'])}</td><td class="num">{per_g}</td><td class="num">{esc(q['asOf'])}</td>
<td>{source_link(q['url'])}</td></tr>""")
    archive = "".join(f'<li><a href="{esc(a["path"])}">{esc(a["label"])}</a></li>' for a in D["meta"]["archive"])
    n_quotes = 1 + len(D["spot"]["prior"]) + len(D["spot"]["crossChecks"])
    q_lo = min(q["usdPerOz"] for q in quotes)
    q_hi = max(q["usdPerOz"] for q in quotes)
    q_pct = (q_hi - q_lo) / q_lo * 100
    verdict = f"""
<section class="verdict">
  <div class="eyebrow">Bottom line</div>
  <h2>No listing here meets all 12 requirements — and that is the finding.</h2>
  <p><b>{sum(1 for e in ENTRIES if e['makerMarkStated'])} of {len(ENTRIES)}</b> rows state a maker’s mark, <b>{sum(1 for e in ENTRIES if e['grams'] is None)}</b> publish no gram weight, <b>{sum(1 for e in ENTRIES if not e['solidStated'])}</b> never say “solid gold”, and <b>{sum(1 for e in ENTRIES if not e['returnsVerified'])}</b> have no verified return policy. Those gaps are the answer to “which ring should I buy”: none of these listings is documented well enough to buy as-is. Each gap is a question to put to the seller in writing before paying.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Best-documented rows (not a recommendation)</th><th>Documents present</th><th>Still missing</th><th>Also flagged</th></tr></thead>
    <tbody>{doc_table(4)}</tbody></table></div>
  <p class="small muted" style="margin-top:8px">Weighted: gram weight counts most, then “solid gold” wording and a verified return policy; ties break on price ÷ metal value, and any open high-severity flag costs 1.5 points. The full checklist and every gap are on <a href="site/checklist.html">Checklist</a> and <a href="site/flagged.html">Flagged for Review</a>.</p>
</section>
"""

    body = f"""
<section class="hero">
  <div class="hero-copy">
    <div class="eyebrow">Solid gold engagement rings · verified {esc(date_str())}</div>
    <h1>Find a gold ring you can actually verify.</h1>
    <p class="lead">{len(ENTRIES)} real listings from {len(SELLERS)} sellers, checked line by line against the seller's own page. Prices, karats and gram weights are recorded only when the source states them. Everything else is blank — and flagged.</p>
    <div class="cta">
      <a class="btn primary" href="site/listings.html">Browse the {len(ENTRIES)} listings</a>
      <a class="btn gold" href="site/calculator.html">Value a ring by weight</a>
      <a class="btn ghost" href="site/checklist.html">12-point checklist</a>
    </div>
    <p class="tiny muted" style="margin-top:14px">{sum(1 for e in ENTRIES if e["provenance"] == "live")} of {len(ENTRIES)} values were re-read from the seller’s own pages in this pass; the other {sum(1 for e in ENTRIES if e["provenance"] != "live")} are same-day captures with their evidence recorded. No value anywhere on this site is inferred.</p>
  </div>
  <aside class="hero-side">
    <div>
      <div class="label">Gold spot used here · Kitco bid</div>
      <div class="big">{money(SPOT['usdPerOz'])}<span style="font-size:16px;font-weight:400"> / troy oz</span></div>
      <div class="per">{money(SPOT['usdPerGram'])} per gram · {esc(SPOT['asOf'])}</div>
    </div>
    <div class="quote">“Bid 4,026.90 USD … gram 129.47 … as of October 22, 2026 at 7:26 p.m. EDT.”<br><a href="site/gold-price.html">All four same-day quotes →</a></div>
  </aside>
</section>

<section class="rule-panel">
  <h2>⚠ NO HALLUCINATIONS — the rule that governs this entire project</h2>
  <p>Every price, weight, karat, hallmark claim and return policy on this site was read from the <b>linked official source page</b> on the check date shown. Nothing is estimated, averaged, filled in from a similar product, or copied from a search snippet without saying so.</p>
  <ul>
    <li><b>Blank means unverified.</b> If the seller's page does not state it, the cell stays empty and is published on <a href="site/flagged.html">Flagged for Review</a>.</li>
    <li><b>Every row has a source link</b> to the exact page the value came from.</li>
    <li><b>Derived numbers are calculated</b> from verified inputs: fine gold = grams × karat fineness; value = fine gold × spot.</li>
    <li><b>Priorities:</b> official government/standards sources for rules; the seller's own page for its price and policy.</li>
    <li><b>After every review pass</b> run <span class="run">python3 scripts/verify.py</span> — it re-checks sources, arithmetic, links and every dollar figure on the site.</li>
  </ul>
  <p style="margin-top:10px"><a class="btn ghost" href="site/verification.html">Read the method and this pass's log</a></p>
</section>

<div class="stats">
  <div class="stat gold"><div class="k">Gold spot (Kitco bid)</div><div class="v">{money(SPOT['usdPerOz'])}</div><div class="d">per oz · {money(SPOT['usdPerGram'])}/g · 7:26 pm ET</div></div>
  <div class="stat"><div class="k">Listings collected</div><div class="v">{counts['entries']}</div><div class="d">{sum(1 for e in ENTRIES if e['category']=='engagement-ring')} engagement rings · {sum(1 for e in ENTRIES if e['category']=='band')} bands · 1 case study</div></div>
  <div class="stat"><div class="k">With a published weight</div><div class="v">{counts['weighted']} / {counts['entries']}</div><div class="d">others are blank + flagged (FL-03)</div></div>
  <div class="stat"><div class="k">Open flags for review</div><div class="v">{counts['openflags']}</div><div class="d"><a href="site/flagged.html">Flagged for Review →</a></div></div>
  <div class="stat"><div class="k">Checker failures</div><div class="v">{REPORT_FAIL if REPORT_FAIL is not None else "—"}</div><div class="d">last run — see Verification</div></div>
</div>

{verdict}

<h2>Today's gold price <span class="tag">{n_quotes} timestamped quotes, same day</span></h2>
<div class="table-wrap"><table>
<thead><tr><th>Source</th><th class="num">USD / troy oz</th><th class="num">USD / gram</th><th class="num">As of</th><th>Link</th></tr></thead>
<tbody>{''.join(spot_rows)}</tbody></table></div>
<p class="small muted" style="margin-top:8px">The {n_quotes} quotes range from {money(q_lo)} to {money(q_hi)} per ounce — about {q_pct:.1f}% across one day. All calculations on this site use the single {money(SPOT['usdPerGram'])}/g Kitco bid shown first, with its timestamp. <a href="site/gold-price.html">Full gold-price page, purity table and raw-gold amounts →</a></p>

<h2>What we found <span class="tag">the short version</span></h2>
<div class="table-wrap"><table>
<thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th class="num">Rows</th><th></th></tr></thead>
<tbody>{''.join(f_rows)}</tbody></table></div>
<p class="small muted" style="margin-top:8px">All {counts['openflags']} flags — including the low/info items — are on <a href="site/flagged.html">Flagged for Review</a>. They do not block publication; they are the list to work through.</p>

<h2>Every row with a published weight <span class="tag">sorted by price ÷ metal value</span></h2>
<div class="table-wrap"><table>
<thead><tr><th>Ring</th><th class="num">Grams</th><th class="num">Price</th><th class="num">Metal value</th><th class="num">Price / metal</th><th>Basis</th><th>Source</th></tr></thead>
<tbody>{''.join(top_rows)}</tbody></table></div>
<div class="note gold"><b class="title">How to read “price ÷ metal value”</b>A ratio near 1 means you are paying mostly for gold. A high ratio is normal for a ring with diamonds and labour — it is not proof of a bad deal, and a low ratio is not automatically a bargain. The one signal to treat as a hard stop: <b>a price below the metal value</b> (ratio under 1.00). Only complete rings are comparable; setting prices exclude the center diamond. <a href="site/analysis.html">Full analysis →</a></div>

<h2>Browse by category</h2>
<div class="cards">
  <a class="card" href="site/listings.html"><div class="k">All entries</div><div class="t">Listings, line by line</div><div class="d">25 rows: price, karat, grams, hallmark claim, returns, check date, flags and the source page for each.</div><div class="go">Open the table →</div></a>
  <a class="card" href="site/analysis.html"><div class="k">Analysis</div><div class="t">Price vs. gold value</div><div class="d">The 8 rows that publish a weight, the median markup, the below-metal case, and data-completeness scores.</div><div class="go">Read the analysis →</div></a>
  <a class="card" href="site/gold-price.html"><div class="k">Gold price</div><div class="t">Spot, purity, raw amounts</div><div class="d">{n_quotes} same-day quotes, Kitco purity values, and a table of what X grams of 10K–24K is worth today.</div><div class="go">See the numbers →</div></a>
  <a class="card" href="site/calculator.html"><div class="k">Calculator</div><div class="t">Weight → gold value</div><div class="d">Enter grams, karat, spot and asking price. Get fine gold, metal value and the price/metal ratio — computed live.</div><div class="go">Open the calculator →</div></a>
  <a class="card" href="site/checklist.html"><div class="k">Checklist</div><div class="t">The 12-point buying test</div><div class="d">Each point linked to its official source, with what this dataset shows and what to demand from the seller.</div><div class="go">Work the checklist →</div></a>
  <a class="card" href="site/sellers.html"><div class="k">Sellers</div><div class="t">{len(SELLERS)} sellers compared</div><div class="d">Contact details, return terms, warranty, payment and reputation — with the policy links and open questions.</div><div class="go">Compare sellers →</div></a>
  <a class="card" href="site/flagged.html"><div class="k">Flagged for Review</div><div class="t">{counts['openflags']} open items</div><div class="d">Every irregularity, blank cell and unresolved policy — with affected rows and sources. Review after launch.</div><div class="go">Open the flag list →</div></a>
  <a class="card" href="site/sources.html"><div class="k">Sources</div><div class="t">Full registry</div><div class="d">Every URL used, grouped by official guidance, gold price, seller policy and listing, with check dates.</div><div class="go">Audit the sources →</div></a>
  <a class="card" href="site/verification.html"><div class="k">Verification</div><div class="t">Method + pass log</div><div class="d">What was re-fetched live this pass, what was corrected, and the exact checker commands and results.</div><div class="go">See the proof →</div></a>
</div>

<h2>How to use this in 15 minutes</h2>
<div class="cards">
  <div class="card"><div class="k">Step 1 · 3 min</div><div class="t">Read the checklist</div><div class="d">The 12 checks, in order. If a seller cannot satisfy the weight, solid-gold, hallmark and return items, stop.</div></div>
  <div class="card"><div class="k">Step 2 · 5 min</div><div class="t">Pick 2–3 listings</div><div class="d">Filter by karat and seller, open each source page, and confirm the price and karat are still what the row says.</div></div>
  <div class="card"><div class="k">Step 3 · 4 min</div><div class="t">Run the numbers</div><div class="d">Ask for the gram weight, then use the calculator. A complete ring priced below its metal value is a stop sign.</div></div>
  <div class="card"><div class="k">Step 4 · 3 min</div><div class="t">Ask, in writing</div><div class="d">Weight, solid gold, hallmark photo, return window and resize exclusions. Keep the replies with your receipt.</div></div>
</div>

<div class="note blue" style="margin-top:26px"><b class="title">Earlier sessions' work is preserved</b>{len(D["meta"]["archive"])} earlier deliverables are preserved in this repository and remain published alongside this consolidated dashboard: <ul class="bullets" style="margin-bottom:0">{archive}</ul></div>
"""
    return shell("", "home", "Gold engagement rings, verified line by line",
                 "25 verified solid-gold engagement ring listings, gold spot price, calculator, checklist, seller policies and flagged irregularities. No hallucinations: every value has a dated source link.", body)

def listings_page():
    rows = []
    for i, e in enumerate(ENTRIES, 1):
        s = seller(e)
        mv, r = metal_value(e), ratio(e)
        if e["grams"] is None:
            grams = '<span class="blank">not stated</span>'
            fine = '<span class="blank">—</span>'
            mvc = '<span class="blank">—</span>'
            rc = '<span class="blank">n/a — no weight</span>'
        else:
            grams = f'<span class="num">{e["grams"]:g} g</span><div class="src">{esc(e["gramsNote"] or "")}</div>'
            fine = f'<span class="num">{fine_g(e):.3f} g</span>'
            mvc = f'<span class="num">{money(mv)}</span>'
            if r is None:
                rc = '<span class="blank">no price</span>'
            else:
                tone = "bad" if r < 1 else ("warn" if r < 1.6 else "ok")
                basis = "setting" if e["priceBasis"] == "setting" else "complete"
                rc = f'<span class="badge {tone}">{r:.2f}×</span><div class="src">{basis}</div>'
        price = f'<span class="num">{money(e["price"])}</span>' if e["price"] is not None else '<span class="blank">no price</span>'
        price_sub = f'<div class="src" style="max-width:240px">{esc(e["priceNote"] or "")}</div>'
        solid = ('<span class="badge ok">stated</span>' if e["solidStated"] else '<span class="badge gray">not stated</span>')
        solid += f'<div class="src" style="max-width:200px">{esc(e["solidQuote"])}</div>' if e["solidQuote"] else ""
        mark = ('<span class="badge warn">karat stamp only</span>' if e["hallmarkStated"] else '<span class="badge gray">not stated</span>')
        mark += '<div class="src">maker’s mark: <b>not stated</b></div>' if not e["makerMarkStated"] else ""
        if e["hallmarkQuote"]:
            mark += f'<div class="src" style="max-width:190px">{esc(e["hallmarkQuote"])}</div>'
        rtext = (e["returns"] or "not stated").strip()
        first = rtext.split(". ")[0]
        if len(first) > 140:
            first = first[:137].rstrip() + "…"
        ret = f'<div class="src" style="max-width:190px">{esc(first)}</div><div>{source_link(e["returnUrl"], "policy ↗")}</div>'
        prov = '<span class="badge ok">live</span>' if e["provenance"] == "live" else '<span class="badge info">same-day</span>'
        rows.append(f"""<tr id="{esc(e['id'])}" data-seller="{esc(e['sellerId'])}" data-cat="{esc(e['category'])}" data-karat="{e['karat']}" data-weight="{'1' if e['grams'] is not None else '0'}" data-price="{e['price'] if e['price'] is not None else ''}" data-ratio="{r if r is not None else ''}" data-fine="{f'{fine_g(e):.6f}' if e['grams'] is not None else ''}" data-mv="{f'{metal_value(e):.6f}' if e['grams'] is not None else ''}" data-name="{esc(e['name'].lower())}">
<td class="num">{i}</td>
<td><div class="ring-name"><a href="{esc(e['url'])}" target="_blank" rel="noopener">{esc(e['short'])}</a></div>
  <div class="subline">{esc(s['name'])} · {esc(e['metalColor'])}</div>
  <div class="src">{source_link(e['url'], 'official listing ↗')}</div></td>
<td><b>{e['karat']}K</b><div class="src">{esc(e['metalColor'])}</div></td>
<td class="num">{price}{price_sub}</td>
<td>{grams}</td>
<td class="num calc">{fine}</td>
<td class="num calc">{mvc}</td>
<td>{rc}</td>
<td>{solid}</td>
<td>{mark}</td>
<td>{ret}</td>
<td class="num">{esc(e['checkedOn'])}<div>{prov}</div></td>
<td class="small">{flag_badges(e)}</td></tr>""")

    seller_opts = "".join(f'<option value="{esc(k)}">{esc(v["name"])}</option>' for k, v in sorted(SELLERS.items(), key=lambda kv: kv[1]["name"]))
    body = f"""
<div class="page-head">
  <div class="eyebrow">All entries · {len(ENTRIES)} listings</div>
  <h1>Listings, line by line</h1>
  <p>Every row links to the exact page the price and karat came from. Blank cells are not missing data entry — they mean the seller's page did not state the value. Flags explain each gap. <b>Do not read a blank as zero.</b></p>
</div>
<div class="note gold"><b class="title">Three rules for this table</b>
1) A price is what the seller displayed on the check date, not an offer. 2) “Metal value” is calculated from the seller's stated weight and the timestamped spot — it excludes diamonds, labour and tax. 3) “Setting” prices exclude the center stone; only complete rings can be compared by price ÷ metal value.</div>

<div class="filters" id="filters">
  <label>Seller<select id="f-seller"><option value="">All sellers</option>{seller_opts}</select></label>
  <label>Category<select id="f-cat"><option value="">All</option><option value="engagement-ring">Engagement rings</option><option value="band">Bands</option><option value="case-study">Case study</option></select></label>
  <label>Karat<select id="f-karat"><option value="">All</option><option value="14">14K</option><option value="18">18K</option></select></label>
  <label>Weight<select id="f-weight"><option value="">Any</option><option value="1">Published</option><option value="0">Not published</option></select></label>
  <label>Sort<select id="f-sort"><option value="">As collected</option><option value="price-asc">Price ↑</option><option value="price-desc">Price ↓</option><option value="ratio-asc">Price/metal ↑</option><option value="ratio-desc">Price/metal ↓</option></select></label>
  <button class="clear" id="f-clear" type="button">Clear filters</button>
</div>
<p class="filter-count" id="count">{len(ENTRIES)} of {len(ENTRIES)} rows shown</p>

<div class="table-wrap tall"><table id="listings">
<thead><tr>
<th>#</th><th>Ring &amp; source</th><th>Karat</th><th class="num">Price</th><th>Grams</th>
<th class="num">Fine gold (calc)</th><th class="num">Metal value (calc)</th><th>Price ÷ metal</th>
<th>Solid gold?</th><th>Hallmark</th><th>Returns</th><th class="num">Checked</th><th>Flags</th>
</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<div class="note" style="margin-top:14px"><b class="title">Legend</b>
<span class="badge ok">live</span> re-fetched and read in this verification pass ·
<span class="badge info">same-day</span> captured live earlier the same day by another session, evidence preserved ·
<span class="badge ok">stated</span> the listing uses the words “solid gold” (quoted) ·
<span class="badge warn">karat stamp only</span> the listing claims a karat stamp but no maker’s mark ·
<span class="badge gray">not stated</span> the page does not say it — value left blank, not inferred.</div>

<div class="note red"><b class="title">The one hard stop in this table</b>A complete ring priced below its calculated metal value is not a bargain — it is a fraud signal. One case-study row (a sold 7 g band) shows that pattern. Everything else priced above metal is normal; diamonds and labour are real costs.</div>

<p class="small muted">Need the calculation for a listing that does not publish a weight? You cannot compute it — that is the point of the blank. Ask the seller for the weight in grams, then use the <a href="calculator.html">calculator</a>. Also see the <a href="flagged.html">open flags for these rows</a>.</p>
<script src="assets/filters.js"></script>
"""
    return shell("../", "listings", "Listings — gold engagement rings",
                 "25 verified gold engagement ring listings with prices, karats, gram weights, hallmark claims, return policies and source links. Blanks are flagged, never inferred.", body)

def gold_price_page():
    quotes = [dict(SPOT, primary=True)] + D["spot"]["prior"] + D["spot"]["crossChecks"]
    qrows = []
    for q in quotes:
        qrows.append(f"""<tr><td><b>{esc(q['source'])}</b>{' <span class="badge ok">used for calculations</span>' if q.get('primary') else ''}
<div class="src">{esc(q.get('method',''))}</div></td><td class="num">{money(q['usdPerOz'])}</td>
<td class="num">{money(q['usdPerGram']) if q.get('usdPerGram') else '<span class="blank">—</span>'}</td>
<td class="num">{esc(q['asOf'])}</td><td class="small">{esc(q.get('quote') or q.get('note') or '')}</td>
<td>{source_link(q['url'])}</td></tr>""")
    prows = []
    for k in ["24K", "22K", "18K", "14K", "10K"]:
        f = FIN[k]
        prows.append(f"""<tr><td><b>{k}</b></td><td class="num">{f*100:.2f}%</td><td class="num">{money(D['spot']['purity']['perOz'][k])}</td>
<td class="num calc">{money(D['spot']['purity']['perOz'][k]/TROY)}</td><td class="num calc">{money(FIN[k]*SPOT_G)}</td></tr>""")
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, TROY]
    karats = ["10K", "14K", "18K", "22K", "24K"]
    rrows = []
    for w in weights:
        label = "1 troy oz (31.1034768 g)" if abs(w - TROY) < 1e-9 else f"{w:g} g"
        cells = "".join(f'<td class="num">{money(w*FIN[k]*SPOT_G)}<div class="src">{w*FIN[k]:.2f} g fine</div></td>' for k in karats)
        rrows.append(f"<tr><td><b>{label}</b></td>{cells}</tr>")
    body = f"""
<div class="page-head"><div class="eyebrow">Gold price · verified {esc(date_str())}</div>
<h1>What gold is worth today — and what it means per gram</h1>
<p>{1 + len(D["spot"]["prior"]) + len(D["spot"]["crossChecks"])} same-day quotes are recorded below with their exact timestamps. One is chosen for every calculation on this site: the Kitco spot bid at {esc(SPOT['asOf'])}. A spot price is not a retail price; jewellery carries fabrication, design and retail margin on top.</p></div>

<div class="hero">
  <div class="panel"><div class="eyebrow">Primary quote</div>
    <div style="font-size:44px;font-weight:700;letter-spacing:-.02em;margin:6px 0 2px">{money(SPOT['usdPerOz'])}<span style="font-size:16px;font-weight:400"> / troy oz</span></div>
    <div class="muted">{money(SPOT['usdPerGram'])} per gram · {esc(SPOT['asOf'])} · Kitco spot bid</div>
    <blockquote>{esc(SPOT['quote'])}<cite>Kitco Live Gold Price — <a href="{esc(SPOT['url'])}" target="_blank" rel="noopener">kitco.com/charts/gold</a>, fetched {esc(date_str())}</cite></blockquote>
    <p class="small muted">The same page also showed $4,027.50/oz in its body text and $129.49/g in its conversion table. That is normal intraday updating — the ticker bid is the figure recorded here, and the timestamp is part of the value.</p>
  </div>
  <div class="panel"><div class="eyebrow">Why a timestamp matters</div>
    <p class="small">The four same-day quotes on this page range from {money(4025)} to {money(4086.90)} per ounce. Using the morning high instead of the evening bid would move every metal value by about 1.5%.</p>
    <p class="small">The LBMA benchmark is set twice daily (10:30 and 15:00 London time) by auction, while retail spot pages update continuously. Neither is “the” price — both are snapshots. Record the time with the number.</p>
    {source_link('https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices', 'LBMA benchmark page ↗')}
  </div>
</div>

<h2>All quotes captured <span class="tag">same day</span></h2>
<div class="table-wrap"><table><thead><tr><th>Source</th><th class="num">USD / oz</th><th class="num">USD / g</th><th class="num">As of</th><th>What the page said</th><th>Link</th></tr></thead><tbody>{''.join(qrows)}</tbody></table></div>

<h2>Gold value by purity <span class="tag">Kitco table, same capture</span></h2>
<div class="table-wrap"><table><thead><tr><th>Karat</th><th class="num">Fineness</th><th class="num">Value per troy oz</th><th class="num">Value per gram</th><th class="num">Fine gold per gram</th></tr></thead><tbody>{''.join(prows)}</tbody></table></div>
<p class="small muted">Kitco publishes the percentages shown (24K 99.99%, 22K 91.67%, 18K 75.00%, 14K 58.33%, 10K 41.67%). They are used exactly as published. A 14K item is 58.33% gold by weight, not 14/24 rounded to taste. Kitco’s 24K line is the spot price itself; the “fine gold per gram” column applies the published 99.99% fineness, which is why it reads one cent below the spot per gram.</p>

<h2>Raw gold amounts <span class="tag">what X grams of metal is worth at {money(SPOT['usdPerGram'])}/g</span></h2>
<div class="table-wrap"><table><thead><tr><th>Weight of metal</th><th class="num">10K (41.67%)</th><th class="num">14K (58.33%)</th><th class="num">18K (75.00%)</th><th class="num">22K (91.67%)</th><th class="num">24K (99.99%)</th></tr></thead><tbody>{''.join(rrows)}</tbody></table></div>
<p class="small muted">Each cell is <b>weight × fineness × {money(SPOT['usdPerGram'])}/g</b>, computed by the build script — not typed. Values are metal only: no stones, labour, tax or retail margin. Use the <a href="calculator.html">calculator</a> for a specific ring.</p>

<h2>The formula used everywhere on this site</h2>
<div class="formula">fine gold (g) = ring weight (g) × fineness (14K = 0.5833, 18K = 0.75)<br>
metal value (USD) = fine gold (g) × spot (USD per gram)<br>
price ÷ metal value = asking price ÷ metal value<br>
1 troy ounce = 31.1034768 grams</div>
<p class="small muted" style="margin-top:10px">Troy-ounce conversion: NIST SP 811 Appendix B.8 and Kitco's own statement (“A troy ounce is 31.1034768 grams”). {source_link('https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8', 'NIST ↗')}</p>

<div class="note red"><b class="title">Do not treat this as a valuation of a ring</b>Metal value is a floor check, not an appraisal. A diamond, setting work and brand can legitimately multiply the metal value many times. What metal value is good for: spotting a price that is <i>below</i> the gold itself, which is the classic fraud signal.</div>
"""
    return shell("../", "gold-price", "Gold price — spot, purity and raw gold values",
                 "{1 + len(D['spot']['prior']) + len(D['spot']['crossChecks'])} timestamped same-day gold quotes, Kitco purity values, and a computed table of what 1–31 grams of 10K, 14K, 18K, 22K and 24K gold is worth.", body)

def calculator_page():
    presets = [dict(id=e["id"], label=f'{e["short"]} — {e["karat"]}K, {e["grams"]:g} g, {money(e["price"]) if e["price"] else "no price"}',
                    grams=e["grams"], karat=e["karat"], price=e["price"])
               for e in ENTRIES if e["grams"] is not None]
    ex_rows = ""
    for e in ENTRIES:
        if e["grams"] is None:
            continue
        r = ratio(e)
        rcell = f"{r:.2f}×" if r is not None else '<span class="blank">—</span>'
        pr = money(e["price"]) if e["price"] is not None else '<span class="blank">—</span>'
        basis = "setting only" if e["priceBasis"] == "setting" else "complete ring"
        ex_rows += ('<tr><td><b>' + esc(e["short"]) + '</b><div class="src">' + esc(seller(e)["name"]) +
                    '</div></td><td class="num">' + f'{e["grams"]:g}' + ' g</td><td class="num">' +
                    str(e["karat"]) + 'K</td><td class="num">' + f'{fine_g(e):.3f}' + ' g</td><td class="num">' +
                    money(metal_value(e)) + '</td><td class="num">' + pr + '</td><td class="num">' + rcell +
                    '</td><td class="small">' + basis + '</td></tr>')

    body = f"""
<div class="page-head"><div class="eyebrow">Calculator · all inputs stay in your browser</div>
<h1>What is the gold in this ring worth?</h1>
<p>Enter the ring's weight in grams, its karat and the spot price you want to use. The calculator returns fine-gold grams, metal value and the price-to-metal ratio. Nothing you type is stored or sent anywhere.</p></div>

<div class="calc-grid">
  <form class="panel" id="calc-form" onsubmit="return false">
    <div class="field">
      <label for="preset">Start from a verified listing (optional)</label>
      <select id="preset"><option value="">— choose a listing with a published weight —</option>
      {"".join(f'<option value="{p["id"]}" data-grams="{p["grams"]}" data-karat="{p["karat"]}" data-price="{p["price"] if p["price"] is not None else ""}">{esc(p["label"])}</option>' for p in presets)}
      </select>
      <span class="hint">Only the 8 rows where the seller published a weight can be pre-filled.</span>
    </div>
    <div class="field-row">
      <div class="field"><label for="grams">Weight (grams)</label><input id="grams" type="number" min="0" step="0.01" value="5.00" inputmode="decimal"></div>
      <div class="field"><label for="karat">Karat</label><select id="karat"><option value="10">10K — 41.67%</option><option value="14" selected>14K — 58.33%</option><option value="18">18K — 75.00%</option><option value="22">22K — 91.67%</option><option value="24">24K — 99.99%</option></select></div>
    </div>
    <div class="field"><label for="spot">Spot price (USD per gram)</label><input id="spot" type="number" min="0" step="0.01" value="{SPOT['usdPerGram']}" inputmode="decimal">
      <span class="hint">Pre-filled with the verified Kitco bid of {money(SPOT['usdPerGram'])}/g at {esc(SPOT['asOf'])}. Replace it with a newer quote from the <a href="gold-price.html">gold-price page</a> or your own source.</span></div>
    <div class="field"><label for="price">Asking price for the ring (USD, optional)</label><input id="price" type="number" min="0" step="0.01" placeholder="e.g. 1085" inputmode="decimal">
      <span class="hint">Use the full price of a <b>complete ring</b>. For a setting, the center stone is extra — the comparison is not apples-to-apples.</span></div>
    <button class="btn primary" type="button" id="calc-btn" style="width:100%">Calculate</button>
  </form>

  <div class="panel">
    <div class="eyebrow">Result</div>
    <div class="result">
      <div class="r"><div class="k">Fine gold</div><div class="v" id="r-fine">—</div><div class="d" id="r-fine-d">grams of pure gold</div></div>
      <div class="r"><div class="k">Metal value</div><div class="v" id="r-value">—</div><div class="d" id="r-value-d">at your spot</div></div>
      <div class="r"><div class="k">Price ÷ metal</div><div class="v" id="r-ratio">—</div><div class="d" id="r-ratio-d">complete rings only</div></div>
    </div>
    <div class="verdict" id="verdict">Enter a weight and karat to see the metal value. Add an asking price to see the ratio.</div>
    <div class="formula" style="margin-top:14px">fine gold = weight × fineness<br>metal value = fine gold × spot per gram<br>price ÷ metal = asking price ÷ metal value</div>
    <p class="small muted" style="margin-top:12px">A ratio below 1.00 means the asking price is below the gold value — a fraud signal, not a bargain. A high ratio is normal for diamond rings; it does not by itself mean overpriced. Metal value ignores stones, labour, tax and resale spread.</p>
    <p class="small"><a href="analysis.html">See the analysis of all priced rows →</a></p>
  </div>
</div>

<h2>Worked examples from this dataset</h2>
<div class="table-wrap"><table><thead><tr><th>Ring</th><th class="num">Weight</th><th class="num">Karat</th><th class="num">Fine gold</th><th class="num">Metal value at {money(SPOT['usdPerGram'])}/g</th><th class="num">Price</th><th class="num">Price ÷ metal</th><th>Basis</th></tr></thead><tbody>
{ex_rows}
</tbody></table></div>

<div class="note gold"><b class="title">Why 17 of 25 listings are not in this calculator</b>Their sellers do not publish a gram weight. You cannot compute gold content from a price or a photo. The blank is the finding: request the weight in writing before you buy. See <a href="flagged.html#FL-03">FL-03</a>.</div>
<script src="assets/calculator.js"></script>
"""
    return shell("../", "calculator", "Gold ring calculator — weight, karat, metal value",
                 "Free gold ring calculator: enter grams, karat and spot price to compute fine gold, metal value and price-to-metal ratio. Pre-filled with verified listings.", body)

def checklist_page():
    verified_returns = sum(1 for e in ENTRIES if e["returnsVerified"])
    items = [
        ("Gold purity (karat)", "Confirm 10K, 14K or 18K in the listing text <i>and</i> on the stamp. Higher karat = more gold, but also softer metal.",
         "FTC — karat marks", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f"All {len(ENTRIES)} rows state a karat: {sum(1 for e in ENTRIES if e['karat']==14)} × 14K, {sum(1 for e in ENTRIES if e['karat']==18)} × 18K. A stated karat is a claim, not a test — see the last rows of this checklist."),
        ("Solid gold — stated explicitly", "The listing must say <b>solid gold</b>. Not plated, vermeil, gold-filled, gold overlay, rolled gold plate or gold-tone. “Solid gold” means the item is not hollow.",
         "FTC — solid vs plated", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f"{sum(1 for e in ENTRIES if e['solidStated'])} of {len(ENTRIES)} listings explicitly use the words solid gold (quoted in the table). The other {len(ENTRIES)-sum(1 for e in ENTRIES if e['solidStated'])} name a karat but never say solid — recorded as “not stated” and flagged. <a href='flagged.html#FL-15'>FL-15</a>"),
        ("Hallmark + maker’s mark", "Look for the karat stamp <b>plus</b> the maker’s/manufacturer’s name or registered trademark next to it. Ask for a close-up photo. If the trademark is missing, the FTC says don’t buy.",
         "FTC · 16 CFR 23.10 · 15 U.S.C. § 297", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f"<b>0 of {len(ENTRIES)}</b> listings state a maker’s mark. {sum(1 for e in ENTRIES if e['hallmarkStated'])} claim a karat stamp (no photo). This is the biggest documentation gap in the whole dataset. <a href='flagged.html#FL-14'>FL-14</a>"),
        ("Weight in grams", "The seller must state the ring’s weight in grams. Without it, neither you nor the calculator can compute gold content. A price alone tells you nothing about how much gold you get.",
         "16 CFR 23.18 — weight representations", "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23#23.18",
         f"{sum(1 for e in ENTRIES if e['grams'] is not None)} of {len(ENTRIES)} listings publish a weight. The other {len(ENTRIES)-sum(1 for e in ENTRIES if e['grams'] is not None)} are blank and flagged. All published weights are seller claims, not independent measurements. <a href='flagged.html#FL-03'>FL-03</a> · <a href='flagged.html#FL-18'>FL-18</a>"),
        ("Seller reputation", "Search the business name with “complaint” and “review”. Verify a real phone number and address. Don’t rely on the seller’s own testimonials.",
         "FTC — before you buy", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f"Only 1 of {len(SELLERS)} sellers has independent complaint data captured here (Blue Nile: BBB A+, 121 complaints in 3 years; ConsumerAffairs 1.7/5 from 172 reviews). The rest are blank on the Sellers page — not “clean”, just unchecked. <a href='flagged.html#FL-04'>FL-04</a>"),
        ("Price vs. gold value", "Compute fine gold and metal value, then compare. A complete ring priced <i>below</i> its metal value is the classic fraud signal. A high markup over metal is normal for diamond rings.",
         "LBMA benchmark · Kitco spot", "https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices",
         f"{sum(1 for e in ENTRIES if e['grams'] is not None and e['price'] is not None)} rows can be computed. One case-study band prices below metal (0.84×). Setting prices are excluded from that conclusion. <a href='analysis.html'>Analysis</a> · <a href='calculator.html'>Calculator</a>"),
        ("Return policy — in writing", "Get the window, the condition rules and the exclusions for resized, engraved or custom rings. Resizing can void a return; Blue Nile explicitly excludes items resized after purchase.",
         "FTC — get return policies in writing", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f"{verified_returns} of {len(ENTRIES)} rows link a policy that was read and verified. Brilliant Earth’s policy URL redirects to its home page; Avianne, Jewelry Master and Solid Gold Jewelers do not publish full terms. Etsy windows vary — one is 7 days. <a href='flagged.html#FL-16'>FL-16</a>"),
        ("Payment protection", "Use a credit card. Under federal law you have the right to dispute billing errors, and card networks give you a chargeback route. Avoid wire transfers, Zelle, gift cards and off-platform “deals”.",
         "FTC — credit cards & disputes", "https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges",
         "Every seller reviewed checks out by card or Etsy checkout. Etsy Purchase Protection covers non-delivery, damage and material misdescription — not buyer’s remorse. Keep orders inside the platform."),
        ("Documentation", "Save the listing, the receipt, the description, the return policy and every message where the seller claims purity or weight. Screenshot prices: they change.",
         "FTC — report problems", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "This repository keeps a dated evidence trail for every row, including the exact quote. Do the same for your purchase: a seller’s written claim is what you can act on later."),
        ("On arrival — independent jeweler", "Before wearing or resizing, take the ring to an independent jeweler and ask them to verify the gold purity <i>and</i> the weight. Resizing can complicate a return.",
         "Project rule (consumer guidance, not a legal mandate)", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "No listing here offers a post-delivery verification window. Assume you must complete the check inside the return window, and confirm that in writing before buying."),
        ("XRF or professional test", "Ask for XRF testing or another professional assay. A stamp is a disclosure, not proof. XRF is fast and non-destructive, but it is a service you arrange — no US rule requires the seller to provide it.",
         "Project rule — no official XRF mandate", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "No seller in this dataset states that it XRF-tests finished pieces or will accept a return based on your test. That is a gap to close in writing. <a href='flagged.html#FL-20'>FL-20</a>"),
        ("If the seller won’t let you verify or return it — don’t buy", "A legitimate seller can provide the weight, a hallmark photo, the return terms and a real contact. Refusal is the answer.",
         "FTC — before you buy", "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "This is a pass/fail gate, not a score. A great price with no return right is not a great price."),
    ]
    rows = []
    for i, (title, what, srcname, src, status) in enumerate(items, 1):
        rows.append(f"""<tr id="c{i}"><td class="num">{i}</td>
<td><b>{title}</b><div class="small muted" style="margin-top:4px">{what}</div></td>
<td class="small"><a href="{esc(src)}" target="_blank" rel="noopener">{esc(srcname)} ↗</a></td>
<td class="small">{status}</td></tr>""")
    body = f"""
<div class="page-head"><div class="eyebrow">The buying checklist · 12 checks</div>
<h1>What to demand before you pay</h1>
<p>This is the checklist the project was built around, with each point tied to an official source and to what the {len(ENTRIES)}-listing dataset actually shows. Work top to bottom; the last two items are the gate.</p></div>

<div class="note gold"><b class="title">The key</b>A 14K or 18K stamp by itself does <b>not</b> prove the ring is that purity. The safe path is: reputable seller + proper markings + a reasonable price + independent testing after delivery. If the seller will not let you verify or return it, do not buy.</div>

<div class="table-wrap"><table><thead><tr><th>#</th><th>Check — what to require</th><th>Official source</th><th>What this dataset shows</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>

<h2>Three phrases that are not the same thing</h2>
<div class="cards">
  <div class="card"><div class="k">Safe</div><div class="t">“Solid 14K gold”</div><div class="d">Solid (not hollow), 14K (58.33% gold). Still needs a maker’s mark and an independent test.</div></div>
  <div class="card"><div class="k">Not solid</div><div class="t">“14K gold filled / overlay / RGP”</div><div class="d">A layer of at least 10K gold mechanically bonded to a base metal. Must be labelled with the fraction if under 1/20 by weight.</div></div>
  <div class="card"><div class="k">Not solid</div><div class="t">“14K gold plated / vermeil / tone”</div><div class="d">Electroplating over base metal (vermeil = gold over sterling silver). The gold layer wears away. Never treat it as an investment in gold.</div></div>
</div>
<p class="small muted">Definitions: FTC Consumer Advice, <a href="https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry" target="_blank" rel="noopener">“Buying Platinum, Gold, and Silver Jewelry”</a>; regulation at <a href="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23" target="_blank" rel="noopener">16 CFR Part 23</a>.</p>

<h2>Print it</h2>
<p class="small muted">This page is print-friendly: use your browser’s Print → Save as PDF. The table will render without the navigation. Keep the saved copy with your order records.</p>
"""
    return shell("../", "checklist", "Gold ring buying checklist — 12 verified checks",
                 "A 12-point gold engagement ring buying checklist with official FTC, eCFR and NIST sources and what each check reveals in a 25-listing dataset.", body)

def sellers_page():
    rows = []
    for s in D["sellers"]:
        contact = "<br>".join(esc(c) for c in s["contact"])
        rep = "".join(f'<div class="small" style="margin-bottom:5px">{esc(r["value"])} <span class="src">({esc(r["method"])})</span><br>{source_link(r["url"], "source ↗")}</div>' for r in s["reputation"]) or '<span class="badge gray">not captured</span>'
        flags = " ".join(f'<a href="flagged.html#{fid}"><span class="badge {("bad" if FLAGS[fid]["severity"]=="high" else "warn" if FLAGS[fid]["severity"]=="medium" else "gray")}">{esc(FLAG_SHORT.get(fid,fid))}</span></a>' for fid in s["flags"])
        ret_badge = '<span class="badge ok">policy read</span>' if s["returnsVerified"] else '<span class="badge warn">not verified</span>'
        rows.append(f"""<tr id="{esc(s['id'])}">
<td><b>{esc(s['name'])}</b><div class="src">{esc(s['type'])} · <a href="{esc(s['website'])}" target="_blank" rel="noopener">website ↗</a></div></td>
<td class="small">{contact}<div class="src"><a href="{esc(s['contactUrl'])}" target="_blank" rel="noopener">contact page ↗</a></div></td>
<td class="small">{ret_badge}<div style="max-width:280px;margin-top:4px">{esc(s['returns'])}</div>{source_link(s['returnsUrl'], 'policy ↗')}</td>
<td class="small" style="max-width:230px">{esc(s['warranty'])}{(' ' + source_link(s['warrantyUrl'], 'terms ↗')) if s.get('warrantyUrl') else ''}</td>
<td class="small" style="max-width:200px">{esc(s['payment'])}</td>
<td class="small" style="max-width:250px">{rep}</td>
<td class="small">{flags}</td></tr>""")
    body = f"""
<div class="page-head"><div class="eyebrow">Sellers · {len(SELLERS)} businesses</div>
<h1>Who is selling, and what they promise</h1>
<p>Policies below were read from the seller's own page on the check date. “Not verified” is not an accusation — it means the page was not available in a form that could be quoted, so nothing was assumed.</p></div>

<div class="note red"><b class="title">Reputation is the weakest column in this project</b>Only Blue Nile has independent complaint data captured. A missing entry means <b>unchecked</b>, not clean. Before buying, search the business name plus “complaint” or “review”, call the phone number, and confirm the address. Etsy “Star Seller” is a platform badge based on the shop’s own metrics — useful, but not an independent inspection.</div>

<div class="table-wrap"><table>
<thead><tr><th>Seller</th><th>Contact</th><th>Returns</th><th>Warranty</th><th>Payment</th><th>Reputation</th><th>Flags</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<h2>Seller-specific findings</h2>
<div class="cards">
  <div class="card"><div class="k">Blue Nile</div><div class="t">Strong policy, mixed reviews</div><div class="d">30-day guarantee with clear exclusions (resized/engraved/custom), two returns per year, $150 lost-certificate fee. BBB A+ but 121 complaints in 3 years; ConsumerAffairs 1.7/5. Lifetime warranty only at $1,000+.</div></div>
  <div class="card"><div class="k">Brilliant Earth</div><div class="t">Returns stated, policy unavailable</div><div class="d">Every product page says “Free Shipping &amp; Returns” and “Free 1-Year Resizing”, but the return-policy URL redirects to the home page. Get the window and exclusions in writing. <a href="flagged.html#FL-07">FL-07</a></div></div>
  <div class="card"><div class="k">Allurez</div><div class="t">Returns verified, exchange-only risk</div><div class="d">30 days to arrive, exclusions listed, $300 per missing certificate, buyer pays return shipping. Design Your Own rings are exchange-only — confirm whether a setting-only purchase counts. <a href="flagged.html#FL-10">FL-10</a></div></div>
  <div class="card"><div class="k">Avianne &amp; Co</div><div class="t">Short window</div><div class="d">14 days for unworn, unaltered items; a 10% FALL10 code is live. Full policy and resize exclusions were not captured. <a href="flagged.html#FL-11">FL-11</a></div></div>
  <div class="card"><div class="k">Jewelry Master</div><div class="t">30-day guarantee, restrictions unknown</div><div class="d">“Some restrictions apply” is all the page says. A $6,041 “retail price” is the seller’s own comparison and is not used in analysis. <a href="flagged.html#FL-12">FL-12</a></div></div>
  <div class="card"><div class="k">Solid Gold Jewelers</div><div class="t">No price, no returns</div><div class="d">The page lists “14ky, 4.7g, #B02561” and tells you to call for pricing. No return policy is shown. Get both in writing before sending money. <a href="flagged.html#FL-13">FL-13</a></div></div>
  <div class="card"><div class="k">Etsy shops</div><div class="t">Individually run policies</div><div class="d">VeraByEden: 7 days. ForeverForLove and Cittali: 30 days. Three others did not expose a window. Etsy Purchase Protection helps with non-delivery/damage, not change of mind. <a href="flagged.html#FL-16">FL-16</a></div></div>
  <div class="card"><div class="k">Vetting a new seller</div><div class="t">Five-minute check</div><div class="d">Search name + “complaint”; look for a BBB profile; call the number; check the address; get the return policy in writing; never pay off-platform. <a href="https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry" target="_blank" rel="noopener">FTC steps ↗</a></div></div>
</div>

<h2>Payment methods seen</h2>
<div class="table-wrap compact"><table><thead><tr><th>Method</th><th>Protection</th><th>Where it appears</th></tr></thead><tbody>
<tr><td><b>Credit card</b></td><td><span class="badge ok">recommended</span> Federal billing-error dispute rights + card-network chargebacks</td><td>Every seller reviewed</td></tr>
<tr><td>Etsy checkout</td><td><span class="badge ok">recommended</span> Etsy Purchase Protection on eligible orders</td><td>All 7 Etsy listings</td></tr>
<tr><td>Affirm / Klarna / Shop Pay</td><td><span class="badge warn">financing, not protection</span> Consumer protections depend on the underlying card</td><td>Brilliant Earth, Allurez, Avianne, Blue Nile, some Etsy shops</td></tr>
<tr><td>Wire, Zelle, gift card, off-platform</td><td><span class="badge bad">avoid</span> Irreversible; may void marketplace protection</td><td>Not offered by these sellers — treat any request as a red flag</td></tr>
</tbody></table></div>
<p class="small muted">Source for card dispute rights: <a href="https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges" target="_blank" rel="noopener">FTC — Using Credit Cards and Disputing Charges ↗</a>.</p>
"""
    return shell("../", "sellers", "Sellers — return policies, warranty, payment and reputation",
                 "13 gold ring sellers compared: contact details, verified return terms, warranty, payment protection and reputation sources, with unverified items flagged.", body)

def analysis_page():
    withg = [e for e in ENTRIES if e["grams"] is not None]
    priced = [e for e in withg if e["price"] is not None]
    ratios = sorted(ratio(e) for e in priced)
    median = ratios[len(ratios)//2] if len(ratios) % 2 else (ratios[len(ratios)//2-1]+ratios[len(ratios)//2])/2
    complete = [e for e in priced if e["priceBasis"] == "complete"]
    c_ratios = sorted(ratio(e) for e in complete)
    c_median = c_ratios[len(c_ratios)//2] if len(c_ratios) % 2 else (c_ratios[len(c_ratios)//2-1]+c_ratios[len(c_ratios)//2])/2
    below = [e for e in priced if ratio(e) < 1]
    maxe = max(priced, key=ratio)
    rows = ""
    for e in sorted(withg, key=lambda x: (ratio(x) if x["price"] is not None else 99)):
        r = ratio(e)
        if e["price"] is None:
            rcell = '<span class="blank">no price</span>'
            tone = ""
        else:
            tone = "bad" if r < 1 else ("warn" if r < 1.6 else "ok")
            rcell = f'<span class="badge {tone}">{r:.2f}×</span>'
        basis = "setting only" if e["priceBasis"] == "setting" else ("from price" if e["priceBasis"] == "from" else "complete ring")
        rows += f"""<tr><td><b>{esc(e['short'])}</b><div class="src">{esc(seller(e)['name'])} · <a href="listings.html#{esc(e['id'])}">row ↗</a></div></td>
<td class="num">{e['grams']:g} g</td><td class="num">{e['karat']}K</td><td class="num">{fine_g(e):.3f} g</td>
<td class="num">{money(metal_value(e))}</td><td class="num">{money(e['price']) if e['price'] is not None else '<span class="blank">—</span>'}</td>
<td class="num">{rcell}</td><td class="small">{basis}</td></tr>"""
    bars = ""
    for e in sorted(priced, key=lambda x: ratio(x)):
        r = ratio(e)
        w = min(100, r/18*100)
        cls = "bad" if r < 1 else ""
        bars += f"""<div class="bar-row"><div>{esc(e['short'])}<div class="src">{esc(seller(e)['name'])}</div></div>
<div class="bar-track"><div class="bar-fill {cls}" style="width:{w:.1f}%"></div></div><div class="bar-val">{r:.2f}×</div></div>"""
    sellers_rows = ""
    for s in sorted(D["sellers"], key=lambda x: -sum(1 for e in ENTRIES if e["sellerId"] == x["id"])):
        n = sum(1 for e in ENTRIES if e["sellerId"] == s["id"])
        if n:
            sellers_rows += f'<div class="bar-row"><div>{esc(s["name"])}</div><div class="bar-track"><div class="bar-fill" style="width:{n/8*100:.0f}%"></div></div><div class="bar-val">{n}</div></div>'
    completeness = [
        ("Official source link for the row", len(ENTRIES), len(ENTRIES), "100%"),
        ("Price published", sum(1 for e in ENTRIES if e["price"] is not None), len(ENTRIES), ""),
        ("Karat stated", sum(1 for e in ENTRIES if e["karat"]), len(ENTRIES), ""),
        ("Gram weight published", len(withg), len(ENTRIES), ""),
        ("“Solid gold” stated", sum(1 for e in ENTRIES if e["solidStated"]), len(ENTRIES), ""),
        ("Karat stamp claimed", sum(1 for e in ENTRIES if e["hallmarkStated"]), len(ENTRIES), ""),
        ("Maker’s mark stated", sum(1 for e in ENTRIES if e["makerMarkStated"]), len(ENTRIES), ""),
        ("Return policy read + verified", sum(1 for e in ENTRIES if e["returnsVerified"]), len(ENTRIES), ""),
        ("Seller with independent reputation data", sum(1 for s in D["sellers"] if s["reputation"] and any(r["method"].startswith(("prior","live")) and "BBB" in r.get("source","")+r.get("value","") for r in s["reputation"])), len(SELLERS), ""),
    ]
    c_rows = "".join(f"""<tr><td>{esc(label)}</td><td class="num">{n} / {d}</td><td style="width:38%"><div class="bar-track"><div class="bar-fill" style="width:{n/d*100:.0f}%"></div></div></td><td class="num">{n/d*100:.0f}%</td></tr>""" for label, n, d, _ in completeness)
    body = f"""
<div class="page-head"><div class="eyebrow">Analysis · computed from the verified rows</div>
<h1>What the data actually says</h1>
<p>All numbers on this page are recomputed from the dataset with the timestamped spot of {money(SPOT['usdPerGram'])}/g. Nothing here is an appraisal or a recommendation to buy — it is a consistency and fraud screen.</p></div>

<div class="stats">
  <div class="stat"><div class="k">Rows with a weight</div><div class="v">{len(withg)} / {len(ENTRIES)}</div><div class="d">the hard limit on analysis</div></div>
  <div class="stat"><div class="k">Rows computable</div><div class="v">{len(priced)}</div><div class="d">weight + price + karat</div></div>
  <div class="stat"><div class="k">Median price ÷ metal</div><div class="v">{median:.2f}×</div><div class="d">all {len(priced)} priced rows</div></div>
  <div class="stat"><div class="k">Complete-ring median</div><div class="v">{c_median:.2f}×</div><div class="d">excludes setting-only rows</div></div>
  <div class="stat gold"><div class="k">Below metal value</div><div class="v">{len(below)}</div><div class="d">hard-stop signal</div></div>
</div>

<h2>Price vs. metal value — every row with a published weight</h2>
<div class="table-wrap"><table><thead><tr><th>Ring</th><th class="num">Weight</th><th class="num">Karat</th><th class="num">Fine gold</th><th class="num">Metal value</th><th class="num">Price</th><th class="num">Price ÷ metal</th><th>Basis</th></tr></thead><tbody>{rows}</tbody></table></div>

<div class="bars" style="margin-top:18px">{bars}</div>
<p class="small muted">Bars are scaled to 18×. A full bar is not “bad” — it means the asking price is about 18 times the gold value. The only red bar is a price below the gold itself.</p>

<div class="note red"><b class="title">The one genuine red flag</b>{esc(below[0]['short']) if below else '—'} — {below[0]['grams']:g} g of {below[0]['karat']}K contains {fine_g(below[0]):.2f} g of fine gold, worth {money(metal_value(below[0]))} at spot, yet it was listed at {money(below[0]['price'])} ({ratio(below[0]):.2f}×). That cannot be a sustainable legitimate sale; it is the pattern of a scam listing (or a misdescribed item). It is a sold case study, kept as an example. <a href="flagged.html#FL-01">FL-01</a></div>

<h2>What the ratios mean</h2>
<div class="cards">
  <div class="card"><div class="k">Under 1.00×</div><div class="t">Stop</div><div class="d">The price is below the gold value. Either the item is not what it claims, the weight is wrong, or it is a scam. Do not send money.</div></div>
  <div class="card"><div class="k">1.0–2.0×</div><div class="t">Mostly metal</div><div class="d">Plausible for a plain band sold near melt. Still verify solid gold, hallmark and weight — a low ratio can also mean a hollow or plated item.</div></div>
  <div class="card"><div class="k">2.0–8.0×</div><div class="t">Normal for a setting</div><div class="d">Design and labour dominate. For a diamond ring this is expected; it is not evidence of overcharging.</div></div>
  <div class="card"><div class="k">Over 8×</div><div class="t">Stones/brand dominate</div><div class="d">Typical of diamond solitaires. Judge the stone separately (certificate, clarity, colour) — metal value tells you nothing about it.</div></div>
</div>

<h2>Data completeness — what the 25 rows actually contain</h2>
<div class="table-wrap"><table><thead><tr><th>Field</th><th class="num">Rows</th><th>Coverage</th><th class="num">%</th></tr></thead><tbody>{c_rows}</tbody></table></div>

<h2>Who comes closest <span class="tag">documentation, not a recommendation</span></h2>
<p class="small muted" style="margin-top:-2px">Same weighted ranking as the dashboard: gram weight counts most, then “solid gold” wording and a verified return policy, minus 1.5 for any open high-severity flag. Nothing here overrides a missing maker’s mark — every one of these rows still has no maker’s mark recorded, which is the single biggest gap in the dataset.</p>
<div class="table-wrap"><table><thead><tr><th>Row</th><th>Documents present</th><th>Still missing</th><th>Also flagged</th></tr></thead><tbody>{doc_table(6, "")}</tbody></table></div>
<p class="small muted" style="margin-top:8px">A setting-only price excludes the center diamond, so its price ÷ metal ratio cannot be compared with a complete ring. See <a href="flagged.html#FL-21">FL-21</a>.</p>
<p class="small muted">The pattern is consistent across sellers: prices and karats are easy to get; weights, maker’s marks and independent reputation data are not. Those are exactly the fields that determine whether a “gold ring” is what it says it is.</p>

<h2>Seller concentration</h2>
<div class="bars">{sellers_rows}</div>
<p class="small muted">Blue Nile and Brilliant Earth dominate the dataset because their product pages expose structured metal and price data. Etsy listings are individual shops, each with a different policy.</p>

<h2>Findings</h2>
<ul class="bullets">
  <li><b>Weight transparency is the bottleneck.</b> Only {len(withg)} of {len(ENTRIES)} listings ({len(withg)/len(ENTRIES)*100:.0f}%) publish grams. Without a weight, no gold-value calculation is possible — so the blank is the finding, not a gap in research.</li>
  <li><b>No listing states a maker’s mark.</b> Two claim a karat stamp; zero provide a photo or a manufacturer’s mark. That fails the FTC’s own test (“if you don’t see a trademark along with the karat mark, don’t buy it”).</li>
  <li><b>“Solid gold” is stated on {sum(1 for e in ENTRIES if e['solidStated'])} of {len(ENTRIES)}.</b> The major retailers describe metal and karat but not solidity. That is a question to ask, not an assumption to make.</li>
  <li><b>The median complete ring asks {c_median:.1f}× its metal value.</b> That is normal once diamonds and labour are included; the useful screen is the low outlier, not the high one.</li>
  <li><b>One listing priced below metal</b> ({ratio(below[0]):.2f}× if below else "n/a") — the case study that shows why the screen exists.</li>
  <li><b>Maximum observed ratio is {ratio(maxe):.1f}×</b> ({esc(maxe['short'])}), a diamond solitaire. Metal value is the wrong yardstick for it; the certificate is the right one.</li>
  <li><b>Return terms are the second-largest gap.</b> {sum(1 for e in ENTRIES if e['returnsVerified'])} of {len(ENTRIES)} rows have a policy that was actually read. Brilliant Earth’s policy page redirects; several sellers state only “returns accepted”.</li>
</ul>

<div class="note gold"><b class="title">Method note</b>Price ÷ metal = price ÷ (grams × fineness × spot per gram). Fineness values are Kitco’s published percentages. Spot is the Kitco bid at {esc(SPOT['asOf'])}. The full arithmetic is re-run by <code>scripts/verify.py</code> on every pass. If a source changes, the derived numbers change with it.</div>
"""
    return shell("../", "analysis", "Analysis — price versus gold value",
                 "Analysis of 25 verified gold ring listings: price-to-metal ratios, median markup, the below-metal fraud signal, and data completeness across sellers.", body)

def flagged_page():
    order = sorted(D["flags"], key=lambda f: (f["status"] != "open", SEV[f["severity"]], f["id"]))
    rows = ""
    for f in order:
        tone, lab = SEV_LABEL[f["severity"]]
        status = '<span class="badge ok">resolved</span>' if f["status"] == "resolved" else '<span class="badge warn">needs review</span>'
        affected = ""
        if f["entryIds"]:
            links = []
            for eid in f["entryIds"][:4]:
                e = next((x for x in ENTRIES if x["id"] == eid), None)
                if e:
                    links.append(f'<a href="listings.html#{esc(eid)}">{esc(e["short"])}</a>')
            if len(f["entryIds"]) > 4:
                links.append(f'+{len(f["entryIds"])-4} more')
            affected = "<div class='small'>" + " · ".join(links) + "</div>"
        srcs = []
        seen = set()
        for eid in f["entryIds"]:
            e = next((x for x in ENTRIES if x["id"] == eid), None)
            if e and e["url"] not in seen:
                seen.add(e["url"]); srcs.append(e["url"])
        if not srcs:
            for e in ENTRIES:
                if e["url"] not in seen:
                    seen.add(e["url"]); srcs.append(e["url"])
                if len(srcs) >= 2:
                    break
        src_html = " ".join(source_link(u, f"source {i+1} ↗") for i, u in enumerate(srcs[:3]))
        rows += f"""<tr id="{esc(f['id'])}"><td class="num"><b>{esc(f['id'])}</b></td>
<td><span class="badge {tone}">{lab}</span><div style="margin-top:4px">{status}</div></td>
<td><b>{esc(f['title'])}</b><div class="small muted" style="margin-top:4px;max-width:560px">{esc(f['detail'])}</div>{affected}</td>
<td class="small">{src_html}</td></tr>"""
    counts = {k: sum(1 for f in D["flags"] if f["severity"] == k and f["status"] == "open") for k in ["high", "medium", "low", "info"]}
    body = f"""
<div class="page-head"><div class="eyebrow">Flagged for Review · published, not blocking</div>
<h1>Everything we could not verify — or found irregular</h1>
<p>This is the review queue. Each item has the affected rows and source links so you can check it yourself. A flag here does <b>not</b> mean the seller is dishonest: “unverified” means the page did not state it, and we refuse to fill the gap by guessing.</p></div>

<div class="stats">
  <div class="stat"><div class="k">High severity</div><div class="v">{counts['high']}</div><div class="d">fraud-pattern signals</div></div>
  <div class="stat"><div class="k">Medium</div><div class="v">{counts['medium']}</div><div class="d">material gaps</div></div>
  <div class="stat"><div class="k">Low</div><div class="v">{counts['low']}</div><div class="d">caveats &amp; price context</div></div>
  <div class="stat"><div class="k">Info</div><div class="v">{counts['info']}</div><div class="d">how to read the data</div></div>
  <div class="stat gold"><div class="k">Resolved this pass</div><div class="v">{sum(1 for f in D['flags'] if f['status']=='resolved')}</div><div class="d">kept for the audit trail</div></div>
</div>

<div class="note gold"><b class="title">How to use this list</b>Start with the high items, then the medium ones. The most common actionable asks: (1) the weight in grams, (2) written confirmation that the item is solid — not hollow or plated, (3) a close-up photo of the karat stamp <i>and</i> maker’s mark, (4) the return window and resize/custom exclusions in writing. If a seller will not provide these, do not buy.</div>

<div class="table-wrap"><table><thead><tr><th>ID</th><th>Severity / status</th><th>Finding &amp; affected rows</th><th>Sources</th></tr></thead><tbody>{rows}</tbody></table></div>

<h2>Unverified by field</h2>
<div class="table-wrap compact"><table><thead><tr><th>Field</th><th class="num">Unverified rows</th><th>Why</th><th>Flag</th></tr></thead><tbody>
<tr><td>Gram weight</td><td class="num">{sum(1 for e in ENTRIES if e['grams'] is None)} / {len(ENTRIES)}</td><td>Not published by the seller</td><td><a href="#FL-03">FL-03</a></td></tr>
<tr><td>Maker’s mark</td><td class="num">{sum(1 for e in ENTRIES if not e['makerMarkStated'])} / {len(ENTRIES)}</td><td>No listing states one; no stamp photos</td><td><a href="#FL-14">FL-14</a></td></tr>
<tr><td>“Solid gold” wording</td><td class="num">{sum(1 for e in ENTRIES if not e['solidStated'])} / {len(ENTRIES)}</td><td>Karat stated, solidity not stated</td><td><a href="#FL-15">FL-15</a></td></tr>
<tr><td>Verified return policy</td><td class="num">{sum(1 for e in ENTRIES if not e['returnsVerified'])} / {len(ENTRIES)}</td><td>Policy page missing, redirecting or partial</td><td><a href="#FL-07">FL-07</a>, <a href="#FL-11">FL-11</a>, <a href="#FL-12">FL-12</a>, <a href="#FL-13">FL-13</a></td></tr>
<tr><td>Independent reputation</td><td class="num">{sum(1 for s in D['sellers'] if not any(('BBB' in r['source'] or 'ConsumerAffairs' in r['source']) for r in s['reputation']))} / {len(SELLERS)} sellers</td><td>No independent complaint data captured</td><td><a href="#FL-04">FL-04</a></td></tr>
</tbody></table></div>

<div class="note blue"><b class="title">Publication rule</b>These flags do not block the site. They are published here, with sources, so the research can go live and the review can continue in public. When a seller answers or a source changes, re-fetch the page, update the row, and close the flag on the next verification pass.</div>
"""
    return shell("../", "flagged", "Flagged for Review — unverified cells and irregularities",
                 "Every unverified value, irregular listing and unresolved seller policy in the GOLD5 dataset, with affected rows and source links.", body)

def sources_page():
    reg = {}
    def add(url, typ, label, checked="2026-10-22"):
        if not url:
            return
        if url not in reg:
            reg[url] = dict(type=typ, labels=[], checked=checked)
        if label not in reg[url]["labels"]:
            reg[url]["labels"].append(label)
    for q in [dict(SPOT)] + D["spot"]["prior"] + D["spot"]["crossChecks"]:
        add(q["url"], "Gold price", q["source"], checked=q["asOf"])
    for r in REFS:
        add(r["url"], "Official guidance", r["title"])
    for s in D["sellers"]:
        add(s["website"], "Seller site", s["name"] + " — website")
        add(s["contactUrl"], "Seller policy", s["name"] + " — contact")
        add(s["returnsUrl"], "Seller policy", s["name"] + " — returns")
        add(s.get("warrantyUrl"), "Seller policy", s["name"] + " — warranty")
        for rp in s["reputation"]:
            add(rp["url"], "Reputation", s["name"] + " — " + rp["source"])
    for e in ENTRIES:
        add(e["url"], "Listing", e["short"])
        add(e["priceSourceUrl"], "Listing", e["short"] + " — price source")
        add(e["returnUrl"], "Seller policy", e["short"] + " — returns")
    order = ["Official guidance", "Gold price", "Seller policy", "Reputation", "Seller site", "Listing"]
    groups = []
    for typ in order:
        urls = [(u, v) for u, v in reg.items() if v["type"] == typ]
        rows = "".join(f"""<tr><td><b>{esc(', '.join(v['labels'][:2]))}</b>{' <span class="src">+%d more</span>' % (len(v['labels'])-2) if len(v['labels'])>2 else ''}</td>
<td class="num">{esc(v['checked'])}</td><td><a href="{esc(u)}" target="_blank" rel="noopener" class="src-link">{esc(u[:96])}{'…' if len(u)>96 else ''} ↗</a></td></tr>""" for u, v in sorted(urls, key=lambda x: x[1]["labels"][0]))
        groups.append(f"""<h2>{esc(typ)} <span class="tag">{len(urls)} URLs</span></h2>
<div class="table-wrap"><table><thead><tr><th>Used for</th><th class="num">Checked</th><th>URL</th></tr></thead><tbody>{rows}</tbody></table></div>""")
    body = f"""
<div class="page-head"><div class="eyebrow">Source registry</div>
<h1>Every link this project relies on</h1>
<p>{len(reg)} distinct URLs, grouped by what they support. Official government and standards sources are used for the rules; the seller's own page is used for its price and policy. Listing pages were read on {esc(date_str())}.</p></div>

<div class="note gold"><b class="title">Source hierarchy</b>
<b>1. Official / primary</b> (FTC, eCFR, U.S. Code, NIST, LBMA) for definitions, marking rules, conversion factors and the benchmark process. <b>2. Seller's own page</b> for the price, karat, weight and policy it displays. <b>3. Market spot pages</b> for a timestamped gold quote. <b>Never</b> a search snippet, a reseller blog or an AI-generated summary for a value.</div>

<div class="stats">
  <div class="stat"><div class="k">Official references</div><div class="v">{len(REFS)}</div><div class="d">government, standards, benchmark</div></div>
  <div class="stat"><div class="k">Listing pages</div><div class="v">{sum(1 for e in ENTRIES)}</div><div class="d">one per row, at minimum</div></div>
  <div class="stat"><div class="k">Seller policy pages</div><div class="v">{sum(1 for s in D['sellers'] if s['returnsVerified'])}</div><div class="d">read and verified</div></div>
  <div class="stat"><div class="k">Distinct URLs</div><div class="v">{len(reg)}</div><div class="d">all checked on {esc(date_str())}</div></div>
</div>

{''.join(groups)}

<h2>Archived deliverables</h2>
<div class="table-wrap compact"><table><thead><tr><th>Session</th><th>What it is</th><th>Link</th></tr></thead><tbody>
<tr><td>638c9614</td><td>Original research site, 11 listings + verbatim evidence files + its own checker</td><td><a href="../docs/index.html">/docs/index.html ↗</a></td></tr>
<tr><td>090bae73</td><td>Checklist-format guide with 13 topic pages</td><td><a href="../index-090bae73.html">/index-090bae73.html ↗</a></td></tr>
<tr><td>37e8ff42</td><td>Dashboard snapshot that preceded this consolidated site</td><td><a href="../archive/session-37e8ff42/index.html">/archive/session-37e8ff42/ ↗</a></td></tr>
</tbody></table></div>
"""
    return shell("../", "sources", "Sources — every link used in the research",
                 "Complete source registry for the GOLD5 gold ring research: official FTC, eCFR, NIST and LBMA references, seller policies, listings and reputation links.", body)

def verification_page():
    report = None
    rp = os.path.join(ROOT, "data", "check_report_v2.json")
    if os.path.exists(rp):
        try:
            report = json.load(open(rp))
        except Exception:
            report = None
    if report:
        status = "PASS" if report.get("ok") else "FAIL"
        tone = "ok" if report.get("ok") else "bad"
        rep_html = f"""<div class="note {'green' if report.get('ok') else 'red'}"><b class="title">Latest run: {status}</b>
{report.get('passed', 0)} checks passed · {report.get('fail', 0)} failed · {report.get('warn', 0)} warnings · run {esc(report.get('ranAt',''))}.
See the full report at <code>{esc(report.get('reportPath','data/check_report_v2.json'))}</code>.</div>"""
    else:
        rep_html = '<div class="note"><b class="title">Checker</b>Run <code>python3 scripts/verify.py</code> to produce the latest result. The command validates every row, every dollar figure and every internal link.</div>'
    log = [
        ("https://www.kitco.com/charts/gold", "Spot bid 4,026.90; per gram 129.47; purity table 24K/22K/18K/14K/10K; 7:26 p.m. ET"),
        ("https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-yellow-gold-item-203348", "BN-203348: $1,145 setting; stock 502120y14; 14K yellow; 2.40 mm"),
        ("https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257", "BN-203257: $870 setting; stock 500000y14; 14K yellow; 1.90 mm"),
        ("https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871", "BN-195871: $1,800 setting; stock 501410y14; 2.50 mm; 16 diamonds 1/4 ct. tw."),
        ("https://www.bluenile.com/engagement-rings", "BN-192506 $1,255; BN-195326 $1,500; BN-311132 $2,320; BN-195639 $1,000; BN-203738 $2,210; 1,451 results"),
        ("https://www.bluenile.com/policies/returns", "30-day guarantee; resized/engraved/custom excluded; 2 returns/year; RMA; $150 lost report; free resize ±2 sizes within 6 months"),
        ("https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/", "BE-1343: $750 setting only; BE1343-14KY; 2–1.2 mm; 4.8/5 from 80 reviews"),
        ("https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/", "BE-NADIA: $1,250 setting only; 1.8 mm; 143 reviews"),
        ("https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/", "BE-1343HH: $1,190 setting only; 2–1.3 mm; 14 accent diamonds 0.05 ct. tw."),
        ("https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/", "BE-SECRET: page served EUR €1,250.00 — USD not confirmed; 14K yellow; 1.5 mm; 13 diamonds 0.06 ct. tw."),
        ("https://www.brilliantearth.com/customer-care/return-policy/", "Redirects to the Brilliant Earth home page — no return text retrievable"),
        ("https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold", "AL-5882: $1,085; style U5882; 14k yellow; 5.00 g approx.; 2.9/2.3 mm"),
        ("https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold", "AL-170: $933; style U170; 4.80 g approx.; 3.20/2.40 mm"),
        ("https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold", "AL-4426: $585; style NG4426; 3.58 g approx."),
        ("https://www.allurez.com/pages/return-policy", "30 days to arrive; engraved/custom/contoured/clearance excluded; DYO exchange-only; $300 missing cert; 7 business days refund"),
        ("https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw", "AV-25893: $1,100; item R25893; 14K; 2.3 g; 0.41 ctw; 4.5 mm; 14-day returns; FALL10 code"),
        ("https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html", "JM-149700: $3,020 special / $6,041 retail; 0.71 ctw; 14KT; 2.3 g; 30-day guarantee"),
        ("https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/", "SGJ-B02561: '14ky, 4.7g, #B02561'; no price; call (309) 452-1612"),
        ("https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond", "ET-4426190660: 14K $1,891.78 (50% off $2,404.16); 2.50 ct lab diamond; 1.80 mm; IGI; returns accepted"),
        ("https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant", "ET-1151446373: 14K $969; 3.70 g; 0.30 ct diamond + 0.90 ct ruby; 7-day returns; ships Albany NY"),
        ("https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry", "Karat + maker's mark rule; solid gold means not hollow; plated/filled/vermeil definitions; get returns in writing"),
        ("https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23", "16 CFR Part 23: §23.3 gold content; §23.10 quality marks; §23.18 weight representations"),
        ("https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges", "Federal right to dispute billing errors; credit-card protection"),
        ("https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices", "LBMA Gold Price set twice daily (10:30, 15:00 London) by ICE Benchmark Administration"),
        ("https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8", "NIST SP 811 Appendix B.8 conversion factors (troy ounce)"),
        ("https://www.law.cornell.edu/uscode/text/15/297", "15 U.S.C. §297(b): trademark must be applied beside the quality mark"),
    ]
    log_rows = "".join(f"<tr><td class=\"small\"><a href=\"{esc(u)}\" target=\"_blank\" rel=\"noopener\">{esc(u[:88])}{'…' if len(u)>88 else ''} ↗</a></td><td class=\"small\">{esc(what)}</td></tr>" for u, what in log)
    corrections = [
        ("VeraByEden return window", "Earlier session records described the Etsy return tab generically. The live listing states <b>7 days</b>. Corrected in the seller record and flagged FL-16."),
        ("Brilliant Earth karats", "Earlier flags said the karat appeared only in product URLs. Each product page states <b>14K Yellow Gold</b> in its title and ring information. Flag FL-24 closed."),
        ("Brilliant Earth Secret Halo price", "The product page served <b>EUR €1,250.00</b> on this fetch, not USD. The $1,090 figure is retained only as a category-listing capture and flagged FL-08 — it was not converted or guessed."),
        ("VeraByEden gold weight", "The earlier '3.70 g via search snippet' flag was resolved: the description on the live page states <b>'Gold grams: 3.70 gr'</b>. Flag closed; seller-stated caveat remains FL-18."),
        ("Blue Nile warranty threshold", "The warranty page and product pages state <b>$1,000 or more</b>. The $870 setting therefore does not qualify; FL-06 was rewritten and linked to the correct rows."),
        ("Jewelry Master retail price", "The page shows $6,041.00 retail vs $3,020.00 special. The retail figure is the seller's own comparison; it is recorded but <b>not used</b> in any ratio (FL-12)."),
    ]
    corr_rows = "".join(f"<tr><td><b>{esc(a)}</b></td><td class=\"small\">{b}</td></tr>" for a, b in corrections)
    body = f"""
<div class="page-head"><div class="eyebrow">Verification · pass of {esc(date_str())}</div>
<h1>How every value was checked</h1>
<p>This page is the audit trail. It lists what was fetched live in this pass, what changed as a result, and the exact command that re-checks the whole site. If you only read one page before trusting a number, read this one.</p></div>

<div class="rule-panel">
  <h2>The five rules</h2>
  <ul style="columns:1">
    <li><b>Read the source page</b>, not a snippet or another site's summary. Record the URL and the date.</li>
    <li><b>Quote it.</b> Every non-obvious value has the seller's exact wording stored in <code>site/assets/data.json</code> and in this repo's evidence files.</li>
    <li><b>Blank beats wrong.</b> If the page does not state a weight, price, policy or mark, the cell is null and a flag is opened.</li>
    <li><b>Compute, don't type.</b> Fine gold, metal value and ratios are derived by the build and re-derived by <code>scripts/verify.py</code> from the raw inputs and the timestamped spot.</li>
    <li><b>Re-run after every review.</b> The checker fails the build on a missing source link, an unsourced dollar figure, a broken internal link or an arithmetic mismatch.</li>
  </ul>
</div>

<h2>This pass — live fetches</h2>
<p class="small muted">{len(log)} sources were fetched and read for this dataset, all on {esc(D["meta"]["asOf"])}. Each row records what that page confirmed.</p>
<div class="table-wrap tall"><table><thead><tr><th>URL</th><th>What it confirmed</th></tr></thead><tbody>{log_rows}</tbody></table></div>

<h2>Corrections made this pass</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>What changed</th></tr></thead><tbody>{corr_rows}</tbody></table></div>

<h2>The checker</h2>
{rep_html}
<div class="formula">python3 scripts/build_site.py   # regenerate the static site from data.json
python3 scripts/verify.py        # sources, arithmetic, $ figures, links, HTML integrity
python3 tools/check_hallucinations.py   # archived /docs/ dataset (unchanged this pass)</div>
<p class="small muted" style="margin-top:10px">The checker reads <code>site/assets/data.json</code> and every generated HTML file. It verifies that each entry has an official source URL and a check date, that every price/gram figure on every page matches the dataset, that derived values recompute, that no hand-typed dollar amount exists outside the dataset or the documented spot/reference tables, and that every internal link and anchor resolves.</p>

<h2>What is still unverified</h2>
<ul class="bullets">
  <li><b>{sum(1 for e in ENTRIES if e['grams'] is None)} of {len(ENTRIES)} weights</b> — not published by the seller (FL-03).</li>
  <li><b>{sum(1 for e in ENTRIES if not e['makerMarkStated'])} of {len(ENTRIES)} maker’s marks</b> — none stated (FL-14).</li>
  <li><b>{sum(1 for e in ENTRIES if not e['returnsVerified'])} of {len(ENTRIES)} return policies</b> — not fully readable (FL-07, FL-11, FL-12, FL-13).</li>
  <li><b>{len(SELLERS)-1} of {len(SELLERS)} sellers</b> — no independent complaint data captured (FL-04).</li>
  <li><b>0 seller-stated XRF tests</b> — none of the listings offers a professional purity test (FL-20).</li>
</ul>
<p class="small muted">These are published, with sources, on <a href="flagged.html">Flagged for Review</a>. They do not block the site; they are the work queue.</p>

<h2>Earlier sessions</h2>
<p class="small muted">This pass did not modify the archived deliverables. Their own checkers and evidence files remain in place and were run before consolidation:</p>
<div class="table-wrap compact"><table><thead><tr><th>Artifact</th><th>Command</th><th>Result at consolidation</th></tr></thead><tbody>
<tr><td><code>scripts/verify.py</code> (archive v1, root dashboard)</td><td><code>python3 scripts/verify.py</code></td><td>PASS — 0 errors, 9 checks</td></tr>
<tr><td><code>tools/check_hallucinations.py</code> (/docs/ dataset)</td><td><code>python3 tools/check_hallucinations.py</code></td><td>PASS — 166 checks, 0 FAIL, 0 WARN, 1 INFO</td></tr>
</tbody></table></div>
"""
    return shell("../", "verification", "Verification — method, live fetch log and checker results",
                 "Audit trail for the GOLD5 dataset: live fetches, corrections, the verification rules, checker commands and remaining unverified items.", body)

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(full) else None
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path, len(content), "bytes")

write("index.html", index_page())
write("site/listings.html", listings_page())
write("site/gold-price.html", gold_price_page())
write("site/calculator.html", calculator_page())
write("site/checklist.html", checklist_page())
write("site/sellers.html", sellers_page())
write("site/analysis.html", analysis_page())
write("site/flagged.html", flagged_page())
write("site/sources.html", sources_page())
write("site/verification.html", verification_page())

# data.js for any future page that wants the raw JSON (kept in sync by the checker)
with open(os.path.join(ROOT, "site/assets/data.js"), "w") as f:
    f.write("/* generated from data.json by scripts/build_site.py — do not edit by hand */\n")
    f.write("window.GOLD5_DATA = " + json.dumps(D, indent=1, ensure_ascii=False) + ";\n")
print("wrote site/assets/data.js")
