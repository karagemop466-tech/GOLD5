#!/usr/bin/env python3
"""Builds the GOLD5 dashboard site from verification/data.json.

Output: report/index.html (landing) + report/*.html + report/assets/*. The repo-root index.html belongs
to the integrated dashboard and is never written by this script.
No external dependencies, no build step, no framework — plain HTML/CSS/JS so GitHub Pages
serves it as-is. Every money string rendered here is either (a) the seller's own price text
copied from the source page, or (b) computed from weight x karat x spot by the formula shown
on every page. tools/check_report.py re-derives (b) independently and fails on any stray value.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "verification", "data.json")
OUTDIR = os.path.join(ROOT, "report")

TROY = 31.1034768
FINE = {10: 10 / 24, 14: 14 / 24, 18: 18 / 24, 22: 22 / 24, 24: 1.0}

with open(DATA, encoding="utf-8") as f:
    D = json.load(f)

PASSES_FILE = os.path.join(ROOT, "verification", "passes.json")
PASSES = []
if os.path.exists(PASSES_FILE):
    with open(PASSES_FILE, encoding="utf-8") as f:
        PASSES = json.load(f)["passes"]

SPOT = D["spot"]["usdPerGramUsed"]
LIST = D["listings"]
SELLERS = {s["id"]: s for s in D["sellers"]}
FLAGS = {f["id"]: f for f in D["flags"]}


def esc(s):
    return html.escape(str(s), quote=True)


def money(x, dp=2):
    return "${:,.{}f}".format(x, dp)


def derived(r):
    """All computed numbers for one listing, or None where an input is missing."""
    if r["weightG"] is None or r["karat"] is None:
        return None
    fine = r["weightG"] * FINE[r["karat"]]
    melt = fine * SPOT
    troy = r["weightG"] / TROY
    price = r["priceUsd"]
    return {
        "fine": fine,
        "melt": melt,
        "troy": troy,
        "perFine": (price / fine) if price else None,
        "premium": (price / melt) if price else None,
        "pricePerGram": (price / r["weightG"]) if price else None,
    }


def score(r):
    """How many of the 6 machine-checkable checklist criteria this row satisfies."""
    s = 0
    s += 1 if r["karat"] else 0
    s += 1 if r["solidStated"] else 0
    s += 1 if r["hallmarkStated"] else 0
    s += 1 if r["weightG"] is not None else 0
    s += 1 if r["priceUsd"] is not None else 0
    seller = SELLERS.get(r["sellerId"], {})
    s += 1 if seller.get("returnsVerified") else 0
    return s


for r in LIST:
    r["_d"] = derived(r)
    r["_score"] = score(r)

STATS = {
    "n": len(LIST),
    "provenanceA": sum(1 for r in LIST if r["provenance"] == "A"),
    "withPrice": sum(1 for r in LIST if r["priceUsd"] is not None),
    "withWeight": sum(1 for r in LIST if r["weightG"] is not None),
    "solid": sum(1 for r in LIST if r["solidStated"]),
    "hallmark": sum(1 for r in LIST if r["hallmarkStated"]),
    "computable": sum(1 for r in LIST if r["_d"] and r["priceUsd"]),
    "flags": len(D["flags"]),
    "sellers": len(D["sellers"]),
    "refs": len(D["references"]),
    "fullPass": sum(1 for r in LIST if r["_score"] == 6),
}

# --------------------------------------------------------------------------- shared chrome
NAV = [
    ("index.html", "Dashboard"),
    ("listings.html", "All listings"),
    ("karat.html", "By karat"),
    ("value.html", "Gold value &amp; calculator"),
    ("sellers.html", "Sellers"),
    ("checklist.html", "Checklist"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    ("method.html", "Method"),
]


def chrome(active, prefix, title, subtitle, body):
    """prefix is "" for pages inside report/ (all pages now live there)."""
    assets = (prefix + "report/assets/") if prefix else "assets/"
    links = []
    for href, label in NAV:
        target = prefix + href
        cls = ' class="on"' if href == active else ""
        links.append(f'<a href="{target}"{cls}>{label}</a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · GOLD5</title>
<meta name="description" content="Verified solid-gold engagement ring research. Every value links to the official source page. No hallucinations.">
<link rel="stylesheet" href="{assets}style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{prefix}index.html"><span class="dot"></span>GOLD5<span class="brand-sub">gold ring research</span></a>
    <nav class="nav">{''.join(links)}</nav>
  </div>
</header>
<div class="rulebar"><div class="wrap"><strong>No hallucinations.</strong> Every price, weight, karat and policy below was read from the linked official page on the date shown. Anything unconfirmed is blank and flagged. <a href="{prefix}method.html">How this is enforced →</a></div></div>
<main id="main" class="wrap">
  <h1>{title}</h1>
  <p class="lede">{subtitle}</p>
{body}
</main>
<footer class="foot"><div class="wrap">
  <p><strong>GOLD5</strong> · data as of {esc(D['meta']['asOf'])} · session {esc(D['meta']['session'])} · spot: {esc(D['spot']['source'])} {money(D['spot']['usdPerGramUsed'])}/g ({esc(D['spot']['capturedUtc'])})</p>
  <p>This is research, not advice. Verify the stamp and purity with an independent jeweler (ask for XRF) before wearing or resizing. Prices and policies change — re-open the source link before acting.</p>
  <p class="small">Older dashboards kept for the record: <a href="{prefix}../index-37e8ff42.html">previous root dashboard</a> · <a href="{prefix}../docs/index.html">docs/ site</a> · <a href="{prefix}../index-090bae73.html">checklist guide</a></p>
</div></footer>
<script src="{assets}app.js"></script>
</body></html>
"""


def pill(text, kind="neutral"):
    return f'<span class="pill {kind}">{text}</span>'


def flag_links(ids):
    out = []
    for fid in ids:
        f = FLAGS.get(fid)
        if not f:
            continue
        out.append(f'<a class="flag f-{f["severity"]}" href="flagged.html#{fid}" title="{esc(f["title"])}">{fid.replace("G-", "")}</a>')
    return "".join(out)


def yn(v, yes="yes", no="not stated"):
    if v is True:
        return f'<span class="yes">{yes}</span>'
    if v is False:
        return f'<span class="no">{no}</span>'
    return '<span class="blank">blank</span>'


def prov_tag(p):
    return '<span class="prov prov-A">A · re-read today</span>' if p == "A" else '<span class="prov prov-B">B · prior capture</span>'


def value_or_blank(v, suffix=""):
    return f"{v}{suffix}" if v not in (None, "") else '<span class="blank">—</span>'


def table(headers, rows, cls="tbl", tid=None):
    idattr = f' id="{tid}"' if tid else ""
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="scroll"><table class="{cls}"{idattr}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


# --------------------------------------------------------------------------- pages
def page_index():
    top = max(r["_score"] for r in LIST)
    best = sorted([r for r in LIST if r["_score"] == top], key=lambda r: r["id"])
    triple = [r for r in LIST if r["solidStated"] and r["weightG"] is not None and r["priceUsd"] is not None]
    STATS["triple"] = len(triple)
    STATS["bestScore"] = max(r["_score"] for r in LIST)
    cards = f"""
<section class="hero">
  <div class="kpis">
    <div class="kpi"><div class="k">Listings catalogued</div><div class="v">{STATS['n']}</div><div class="s">{STATS['provenanceA']} re-read live today</div></div>
    <div class="kpi"><div class="k">Pass every checklist test</div><div class="v">{STATS['fullPass']}</div><div class="s">of {STATS['n']} — see why</div></div>
    <div class="k">Weight published</div><div class="v">{STATS['withWeight']}</div><div class="s">seller-published gram weights</div></div>
    <div class="kpi"><div class="k">"Solid gold" stated</div><div class="v">{STATS['solid']}</div><div class="s">the rest never say it</div></div>
    <div class="kpi"><div class="k">Flagged for review</div><div class="v">{STATS['flags']}</div><div class="s">irregularities, not hidden</div></div>
  </div>
  <div class="notice">
    <h2>The rule this project runs on: no hallucinations</h2>
    <p>Every price, weight, karat, hallmark claim and return term on this site was read from the <b>seller's own page</b> on the date shown, and the exact text that was on the page is stored in <code>verification/evidence/</code>. If a value could not be confirmed, the cell is <b>blank</b> and the row carries a flag — never an estimate, never a "typical" number, never a currency conversion.</p>
    <p>A checker enforces it: <code>python3 tools/check_report.py</code> re-finds every recorded value in the saved page text, re-derives every calculated number, and fails the build on any amount that is not traceable. It is run after every review, and the result is published on the <a href="method.html">Method</a> page.</p>
  </div>
</section>

<section>
<h2>What we found, in one paragraph</h2>
<p class="callout">Of {STATS['n']} gold ring listings examined, <b>none</b> satisfies every requirement in the buying checklist — the best row clears {STATS['bestScore']} of the 6 machine-checkable tests. The blocking gaps are consistent across every seller: <b>not one listing states a hallmark together with a maker's mark</b>, and <b>{STATS['n'] - STATS['withWeight']} of {STATS['n']} publish no gram weight</b>, so the price-versus-gold-value test cannot even be run from the page. Only <b>{STATS['triple']}</b> listings state "solid gold" <i>and</i> publish both a weight and a price.</p>
</section>

<section>
<h2>Shortlist — every row where a weight and a price are both published</h2>
<p class="note">These are the only rows where the metal arithmetic is possible at all. The "Solid" column is the checklist's second test: only a row that says <i>solid</i> can clear it, and {STATS['triple']} of these do.</p>
{table(
    ["Listing", "Seller", "Karat", "Weight", "Price (as published)", "Solid stated", "Fine gold", "Metal value at spot", "Price ÷ metal value", "Score"],
    [[f'<a href="{esc(r["url"])}" rel="noopener">{esc(r["name"])}</a><br><span class="tiny">{prov_tag(r["provenance"])} · {esc(r["id"])}</span>',
      esc(SELLERS[r["sellerId"]]["name"]), f'{r["karat"]}K', f'{r["weightG"]:.2f} g' + (" (approx.)" if r["weightApprox"] else ""),
      esc(r["priceText"]), yn(r["solidStated"], "yes", "no"),
      f'{r["_d"]["fine"]:.2f} g', money(r["_d"]["melt"]), f'{r["_d"]["premium"]:.2f}×', f'{r["_score"]}/6']
     for r in LIST if r["_d"] and r["priceUsd"]],
)}
<p class="note">Ordered as catalogued. A row with "Solid stated: no" is not a rejection of the ring — it means the seller never made the claim, so the claim cannot be verified from the page.</p>
<div class="callout" style="margin:18px 0"><h3 style="margin:0 0 8px">Read the top rows with the seller check beside them</h3>
<p style="margin:0">The four highest-scoring rows (A01–A04) are Allurez settings. Allurez is BBB-accredited, A+, since 2/24/2011 — and its BBB complaints page also shows <b>49 complaints in the last 3 years</b> and <b>8 in the last 12 months</b> (23 product issues, 13 service or repair, 7 delivery). Its "Design Your Own" engagement rings are <b>exchange-only</b>, so a refund is not the remedy if the ring is not what you expected. That is why the score reads the listing, not the seller: <a href="flagged.html#G-ALLUREZ-COMPLAINTS">G-ALLUREZ-COMPLAINTS</a> · <a href="flagged.html#G-EXCHANGE-ONLY">G-EXCHANGE-ONLY</a>.</p></div>

<p class="note">"Price ÷ metal value" is arithmetic, not a verdict: it compares the asking price with the gold content alone. Stones, labour and brand sit on top of that, so a high multiple is normal for a diamond ring and is <i>not</i> evidence of overcharging. The direction that matters for fraud is the other one — a price <b>below</b> the metal value. No row in this catalogue is below it.</p>
</section>

<section>
<h2>Today's gold price (the number every calculation uses)</h2>
<div class="spotgrid">
  <div class="spotcard">
    <div class="k">Spot bid, per troy ounce</div><div class="v">{money(D['spot']['bidUsdPerOz'])}</div>
    <div class="s">Kitco · page clock {esc(D['spot']['pageClock'])}</div>
  </div>
  <div class="spotcard">
    <div class="k">Used for all maths, per gram</div><div class="v">{money(D['spot']['usdPerGramUsed'])}</div>
    <div class="s">lowest per-gram figure Kitco displayed in that capture</div>
  </div>
</div>
<p class="note">Kitco's page displayed four different ounce figures and two gram figures within the same minute (see <a href="flagged.html#G-SPOT-SPREAD">G-SPOT-SPREAD</a>). The lowest per-gram figure is used so computed metal values are conservative. <a href="value.html">Full spot table, per-karat values and the calculator →</a></p>
</section>

<section>
<h2>Pages</h2>
<div class="cards">
  <a class="card" href="listings.html"><div class="k">All listings</div><div class="d">{STATS['n']} rows: karat, weight, price, fine gold, metal value, hallmark status, return terms, source link, flags.</div></a>
  <a class="card" href="karat.html"><div class="k">By karat</div><div class="d">14K vs 18K side by side, with what each karat means and the fineness used.</div></a>
  <a class="card" href="value.html"><div class="k">Gold value &amp; calculator</div><div class="d">Raw gold in any ring: weight → fine grams → troy ounces → dollars. Editable spot.</div></a>
  <a class="card" href="sellers.html"><div class="k">Sellers</div><div class="d">{STATS['sellers']} sellers: contact details, return terms quoted, payment, reputation, what is still unknown.</div></a>
  <a class="card" href="checklist.html"><div class="k">Checklist</div><div class="d">The 12 buying tests, each with the official rule behind it and how the catalogue scores.</div></a>
  <a class="card" href="flagged.html"><div class="k">Flagged for review</div><div class="d">{STATS['flags']} irregularities and blanks, each with the source link and what would resolve it.</div></a>
  <a class="card" href="sources.html"><div class="k">Sources</div><div class="d">Every official page used, with the quote and the timestamp of the capture.</div></a>
  <a class="card" href="method.html"><div class="k">Method</div><div class="d">How verification works, the checks that ran, and what this project still cannot tell you.</div></a>
</div>
</section>

<section>
<h2>Closest to the checklist</h2>
<p class="note">Highest score in the catalogue: <b>{STATS['bestScore']} of 6</b>. Nobody reaches six, because six needs a published hallmark <i>and</i> a published weight <i>and</i> a stated solid-gold claim <i>and</i> a verified return policy on the same row. The three rows below are simply the best-scoring ones in table order — they are not recommendations.</p>
{table(["Listing", "What it gets right", "What still blocks it"],
  [[f'<a href="{esc(r["url"])}" rel="noopener">{esc(r["name"])}</a><br><span class="tiny">{esc(r["id"])} · {r["_score"]}/6</span>',
    ("seller states solid gold; " if r["solidStated"] else "seller does <b>not</b> state solid gold; ")
    + f'publishes {r["weightG"]:.2f} g; price {esc(r["priceText"])}; '
    + ("return policy verified." if SELLERS[r["sellerId"]]["returnsVerified"] else "return policy not fully verified."),
    ("<b>no hallmark or maker's mark stated.</b> " if not r["hallmarkStated"] else "")
    + ("Metal is not claimed to be solid. " if not r["solidStated"] else "")
    + f'Ask for an XRF reading and a photo of the stamp before paying.']
   for r in best[:3]],
)}
</section>
"""
    return chrome("index.html", "", "Gold engagement rings, verified line by line",
                  "A working shortlist of gold engagement rings, built only from what sellers actually publish — with the blanks left blank.", cards)


def page_listings():
    rows = []
    for r in LIST:
        d = r["_d"]
        rows.append([
            f'<span class="idtag">{esc(r["id"])}</span>',
            f'<a href="{esc(r["url"])}" rel="noopener">{esc(r["name"])}</a>'
            + (f'<br><span class="tiny">style {esc(r["styleNumber"])}</span>' if r.get("styleNumber") else "")
            + f'<br><span class="tiny">{prov_tag(r["provenance"])} · checked {esc(r["checkedOn"])}</span>',
            esc(SELLERS[r["sellerId"]]["name"]),
            f'{r["karat"]}K' if r["karat"] else '<span class="blank">—</span>',
            (f'{r["weightG"]:.2f} g' + ('<span class="tiny"> approx.</span>' if r["weightApprox"] else "")) if r["weightG"] is not None else '<span class="blank">—</span>',
            esc(r["priceText"]) if r["priceUsd"] is not None else f'<span class="blank">{esc(r["priceText"])}</span>',
            f'{d["fine"]:.2f} g' if d else '<span class="blank">—</span>',
            money(d["melt"]) if d else '<span class="blank">—</span>',
            f'{d["premium"]:.2f}×' if d and d["premium"] else '<span class="blank">—</span>',
            yn(r["solidStated"], "solid stated", "not stated"),
            yn(r["hallmarkStated"], "stated", "not stated"),
            f'{r["_score"]}/6',
            flag_links(r["flags"]),
        ])
    body = f"""
<div class="toolbar">
  <input id="q" type="search" placeholder="Filter by seller, name, karat, flag…" aria-label="Filter rows">
  <label class="chk"><input id="onlyWeight" type="checkbox"> only rows with a published weight</label>
  <span class="count" id="count"></span>
</div>
{table(["ID", "Listing", "Seller", "Karat", "Weight", "Price (seller's text)", "Fine gold", "Metal value", "Price ÷ metal", "Solid", "Hallmark", "Score", "Flags"],
       rows, tid="listings")}
<p class="note">Prices are the seller's own strings (e.g. "Special Price$3,020.00") so you can match them against the page; the <b>Metal value</b> column is arithmetic — weight × karat ÷ 24 × {money(SPOT)}/g. Hover any flag code to read it, click to jump to the entry on <a href="flagged.html">Flagged for review</a>. "Score" counts the 6 machine-checkable criteria: karat, solid stated, hallmark stated, weight, price, seller return policy verified.</p>
<p class="note">Every row links to the seller's product page. If a cell is blank, the seller did not publish it and this project did not guess it — the flag column says which decision it blocks.</p>
"""
    return chrome("listings.html", "", "All listings", f"{STATS['n']} gold ring listings, each with its source link and the exact price text from the page.", body)


def page_karat():
    groups = {}
    for r in LIST:
        groups.setdefault(r["karat"], []).append(r)
    blocks = []
    explain = {
        14: ("14K", "58.33% gold (585 parts per 1,000). The US mass-market standard: harder wearing than 18K, and the karat stamp reads 14K / 585.", 14 / 24),
        18: ("18K", "75.00% gold (750 parts per 1,000). Softer, richer colour, 28.6% more gold per gram than 14K.", 18 / 24),
        None: ("Karat not stated", "These listings were priced from a category page where no karat was shown. Blank by rule.", None),
    }
    for k in [14, 18, None]:
        if k not in groups:
            continue
        label, blurb, fin = explain[k]
        rows = []
        for r in sorted(groups[k], key=lambda x: (x["priceUsd"] is None, x["priceUsd"] or 0)):
            d = r["_d"]
            rows.append([
                f'<a href="{esc(r["url"])}" rel="noopener">{esc(r["name"])}</a><br><span class="tiny">{esc(r["id"])} · {prov_tag(r["provenance"])}</span>',
                esc(SELLERS[r["sellerId"]]["name"]),
                (f'{r["weightG"]:.2f} g' if r["weightG"] is not None else '<span class="blank">—</span>'),
                esc(r["priceText"]) if r["priceUsd"] is not None else '<span class="blank">blank</span>',
                money(d["melt"]) if d else '<span class="blank">—</span>',
                f'{d["premium"]:.2f}×' if d and d["premium"] else '<span class="blank">—</span>',
                f'{d["pricePerGram"] and money(d["pricePerGram"])} <span class="tiny">per gram of gold</span>' if d and d["pricePerGram"] else '<span class="blank">—</span>',
            ])
        fin_line = f'<p class="note">Fineness used: <b>{fin:.4f}</b> (karat ÷ 24) — identical to the 58.33% / 75.00% figures in Kitco\'s per-purity table.</p>' if fin else ""
        blocks.append(f"""
<section>
<h2>{label}</h2>
<p>{blurb}</p>
{fin_line}
{table(["Listing", "Seller", "Weight", "Price (seller's text)", "Metal value at {}/g".format(money(SPOT)), "Price ÷ metal", "Price per gram"], rows)}
</section>""")
    body = "".join(blocks) + """
<section>
<h2>What the karat comparison shows — and what it does not</h2>
<p>Allurez sells the same filigree design in 14K (style U5882) and 18K (style U5885). The 14K page lists 5.00 g at $1,085; the 18K page lists 5.90 g at $1,316. That is <b>+$231 for +0.90 g of metal and a higher karat</b>, i.e. most of the difference is accounted for by the extra gold, not by a karat premium. But note the style numbers differ, so this is a same-family comparison, not the same SKU in two metals — recorded as <a href="flagged.html#G-18K-DIFFERENT-SKU">G-18K-DIFFERENT-SKU</a>.</p>
<p>The Brilliant Earth Freesia is the one true same-SKU pair (BE1343-14KY / BE1343-18KY), but its 18K page was served in euros at capture, so no USD comparison is published here. Converting it would be an inference.</p>
</section>"""
    return chrome("karat.html", "", "By karat", "14K and 18K listings, grouped, with the fineness each karat actually means.", body)


def page_value():
    rows = []
    for r in sorted([x for x in LIST if x["_d"]], key=lambda x: -(x["_d"]["fine"])):
        d = r["_d"]
        rows.append([
            f'<a href="{esc(r["url"])}" rel="noopener">{esc(r["name"])}</a><br><span class="tiny">{esc(r["id"])}</span>',
            f'{r["karat"]}K',
            f'{r["weightG"]:.2f} g',
            f'{d["fine"]:.4f} g',
            f'{d["troy"]:.4f} oz',
            money(d["melt"]),
            esc(r["priceText"]) if r["priceUsd"] is not None else '<span class="blank">blank</span>',
            f'{d["premium"]:.2f}×' if d["premium"] else '<span class="blank">—</span>',
            money(d["perFine"]) if d["perFine"] else '<span class="blank">—</span>',
        ])
    purity = D["spot"]["purityPerOz"]
    prows = [[f"{k}K", f'{int(k)/24:.4f}', f'{int(k)/24*100:.2f}%', money(purity[k]), money(purity[k] / TROY)]
             for k in ["24", "22", "18", "14", "10"]]
    body = f"""
<section>
<h2>The spot price, exactly as published</h2>
{table(["Karat", "Fineness", "Gold content", "Value of 1 troy oz", "Value of 1 gram"], prows)}
<p class="note">Upstream: {esc(D['spot']['source'])} — <a href="{esc(D['spot']['url'])}" rel="noopener">kitco.com/charts/gold</a>, captured {esc(D['spot']['capturedUtc'])}. Page clock: {esc(D['spot']['pageClock'])}. Kitco publishes its per-purity table at its own spot, so these rows are quoted, not recalculated.</p>
<p class="note"><b>Why the page shows two different numbers:</b> {esc(D['spot']['note'])}</p>
</section>

<section>
<h2>Raw gold in every listing that publishes a weight</h2>
{table(["Listing", "Karat", "Ring weight", "Fine gold", "Troy ounces of gold", "Metal value", "Price", "Price ÷ metal", "Price per fine gram"], rows)}
<p class="note"><b>Formulas.</b> Fine gold (g) = weight (g) × karat ÷ 24. Metal value (USD) = fine gold (g) × {money(SPOT)}/g. Troy ounces = weight ÷ 31.1034768. Every number in this table is recomputed by the checker, never typed.</p>
<p class="note">Metal value is <i>not</i> what the ring is worth: it is the gold content valued at spot, before stones, making charges, hallmarking, retailer margin and tax. It is the floor that lets you see whether a price is absurd.</p>
</section>

<section>
<h2>Calculator — gold weight → raw gold → dollars</h2>
<div class="calc">
  <div class="calc-row">
    <label>Ring weight (grams)<input id="cw" type="number" min="0" step="0.01" value="5" inputmode="decimal"></label>
    <label>Karat<select id="ck">
      <option value="10">10K</option><option value="14" selected>14K</option>
      <option value="18">18K</option><option value="22">22K</option><option value="24">24K</option>
    </select></label>
    <label>Spot (USD per gram)<input id="cs" type="number" min="0" step="0.01" value="{SPOT}" inputmode="decimal"></label>
    <label>Price asked (USD, optional)<input id="cp" type="number" min="0" step="0.01" placeholder="e.g. 1085" inputmode="decimal"></label>
  </div>
  <div class="calc-out" id="cout" aria-live="polite"></div>
  <p class="note">The spot field is pre-filled with <b>{money(SPOT)}/g</b> — the verified Kitco figure from {esc(D['spot']['capturedUtc'])}, not a live feed. If you type a newer spot from kitco.com, that is <b>your</b> input, not site data, and the results below immediately become your own calculation. Nothing you type is stored or sent anywhere.</p>
</div>
</section>

<section>
<h2>Worked example, from the catalogue</h2>
<p>Allurez U5882 publishes <b>5.00 g (approximate)</b> of 14K at <b>$1,085</b>.</p>
<ol class="steps">
  <li>Fine gold = 5.00 × 14 ÷ 24 = <b>2.9167 g</b></li>
  <li>Metal value = 2.9167 g × {money(SPOT)} = <b>{money(5.00 * 14 / 24 * SPOT)}</b></li>
  <li>Price ÷ metal value = 1085 ÷ {money(5.00 * 14 / 24 * SPOT)} = <b>{1085 / (5.00 * 14 / 24 * SPOT):.2f}×</b></li>
  <li>So {money(1085 - 5.00 * 14 / 24 * SPOT)} of the price is <i>not</i> gold — diamond-free setting, labour, margin. Whether that is fair is a judgement; the arithmetic is not.</li>
</ol>
</section>
"""
    return chrome("value.html", "", "Gold value & calculator", "What the gold in a ring is actually worth at today's verified spot — and how to compute it yourself.", body)


def page_sellers():
    blocks = []
    for s in D["sellers"]:
        contact = "".join(
            f'<li>{esc(c["text"])} — <a href="{esc(c["source"])}" rel="noopener">source</a>'
            + ("" if c.get("verified") else ' <span class="tiny">(number seen on page, contact page not opened)</span>') + "</li>"
            for c in s["contact"])
        rep = "".join(f'<li>{esc(x["text"])} — <a href="{esc(x["source"])}" rel="noopener">source</a></li>' for x in s["reputation"])
        rep_block = f'<ul class="tight">{rep}</ul>' if rep else f'<p class="blankline">{esc(s["reputationNote"] or "No independent reputation source verified.")}</p>'
        blocks.append(f"""
<section class="seller" id="{esc(s["id"])}">
  <h2>{esc(s["name"])} <span class="tag">{esc(s["type"])}</span></h2>
  <div class="twocol">
    <div>
      <h3>Contact</h3><ul class="tight">{contact}</ul>
      <h3>Returns — {"verified" if s["returnsVerified"] else "NOT fully verified"}</h3>
      <p>{esc(s["returnsSummary"])}</p>
      <p class="tiny"><a href="{esc(s["returnsUrl"])}" rel="noopener">{esc(s["returnsUrl"])}</a></p>
      <h3>Payment</h3><p>{esc(s["payment"])}</p>
    </div>
    <div>
      <h3>Independent reputation</h3>{rep_block}
      <h3>Open flags</h3><p>{flag_links(s["flags"]) or "none"}</p>
    </div>
  </div>
  <p class="tiny">Manual review, as the FTC recommends: <a href="https://www.google.com/search?q={esc(s["name"].replace(" ", "+"))}+complaints+reviews" rel="noopener">search “{esc(s["name"])} complaints reviews”</a> · <a href="https://www.bbb.org/search?find_country=USA&amp;find_text={esc(s["name"])}" rel="noopener">BBB search</a></p>
</section>""")
    body = "".join(blocks)
    return chrome("sellers.html", "", "Sellers", "Contact details, return terms — quoted, not paraphrased — and what is still unknown about each seller.", body)


def page_checklist():
    crit = [
        ("1", "Gold purity: confirm the karat", "The karat mark tells you how much pure gold the piece contains; 18K is 18 parts gold, 14K is 14 parts.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f'{sum(1 for r in LIST if r["karat"])} of {STATS["n"]} rows',
         "Every listed karat was read from the seller's page. Three Brilliant Earth rows are blank because only the category listing was read."),
        ("2", "Solid gold — the listing must say it", "'Solid gold' means the item is not hollow; 16 CFR 23.3 forbids describing a hollow item as solid.",
         "https://www.law.cornell.edu/cfr/text/16/23.3",
         f'{STATS["solid"]} of {STATS["n"]} rows',
         "The other rows merely name the metal. A karat stamp alone does not prove solidity — and one Etsy listing in this catalogue sells vermeil in the same design family."),
        ("3", "Hallmark plus a maker's mark", "Look for the name or U.S. registered trademark beside the karat mark; the National Stamping Act requires the maker's mark with a quality mark.",
         "https://www.law.cornell.edu/cfr/text/16/23.10",
         f'{STATS["hallmark"]} of {STATS["n"]} rows',
         "One row has a seller *claim* in its title ('Marked 14K'), with no photo. No listing shows a stamp. This can only be closed in person."),
        ("4", "Weight in grams", "A legitimate seller can tell you the weight; without it the price-vs-gold check is impossible.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f'{STATS["withWeight"]} of {STATS["n"]} rows',
         "Three of those are Allurez figures the seller labels 'Approximate'. Ask for the weight in writing before ordering."),
        ("5", "Seller reputation", "The FTC's own advice: search the seller's name with 'complaint' or 'review'; get policies in writing.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f'{sum(1 for x in D["sellers"] if x["reputation"])} of {len(D["sellers"])} sellers',
         "Blue Nile (BBB A+, accredited since 1999, with complaint-themed review excerpts), VeraByEden (Star Seller, 4.9 from 2.1k reviews) and BUTTERFLYWINGVINTAGE (802 five-star reviews, but sold out) have verified reputation data. The rest are blank, not assumed good."),
        ("6", "Price versus gold value", "Compare the asking price with the gold content valued at spot. Below metal value is the fraud signal; far above needs stones to explain it.",
         "https://www.kitco.com/charts/gold",
         f'{STATS["computable"]} of {STATS["n"]} rows',
         "Only rows with both a price and a weight can be tested. None is below metal value. High multiples are expected on diamond rings and are not proof of overcharging."),
        ("7", "Return policy, including resized/custom exclusions", "Get the refund and return policy in writing before buying; check the exclusions for resized and custom pieces.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         f'{sum(1 for x in D["sellers"] if x["returnsVerified"])} of {len(D["sellers"])} sellers verified',
         "Blue Nile, Allurez, VeraByEden and Etsy's marketplace programme are verified. Allurez's own 'Design Your Own' rings are exchange-only; VeraByEden charges a 10% restocking fee within 7 days."),
        ("8", "Payment: use a credit card", "A credit card gives a chargeback path that irreversible methods do not.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "partial",
         "Every seller advertises financing (Affirm, Klarna, Shop Pay, Wells Fargo, layaway) but none of the captured pages lists its accepted payment methods. Card use is implied in refund wording, not confirmed."),
        ("9", "Keep the documentation", "Save the listing, receipt, description and the seller's purity claims — they are your evidence if the ring is not as described.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "advice",
         "This repo stores the verbatim page text of every row (verification/evidence/), which is the same discipline: keep what the page said, with the date."),
        ("10", "On arrival: independent jeweler", "Before wearing or resizing, have an independent jeweler read the stamp and weigh the ring. A hallmark is a claim struck in metal; only an inspection turns it into evidence.",
         "https://www.law.cornell.edu/cfr/text/16/23.10",
         "not yet applicable",
         "No purchase has been made in this project, so nothing here is a completed inspection. This test is the project's own control, not a rule the seller is legally bound to offer."),
        ("11", "Best verification: XRF", "A stamp is a claim; XRF or another professional assay is evidence.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "not yet applicable",
         "Ask specifically for XRF and for the measured weight in grams, and keep the printout with the receipt."),
        ("12", "If the seller will not allow verification or return, do not buy", "No independent verification plus no return right leaves you with no remedy.",
         "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         "decision rule",
         "Applied here: rows with an unpublished return policy or an exchange-only policy are flagged rather than recommended."),
    ]
    rows = []
    for num, title, why, src, status, note in crit:
        rows.append([num, f'<b>{title}</b><br><span class="tiny">{why} <a href="{src}" rel="noopener">official source</a></span>',
                     f'<span class="badge">{status}</span>', esc(note)])
    body = f"""
<section>
<h2>The 12 tests, and how this catalogue scores on each</h2>
{table(["#", "Test (with the rule behind it)", "Coverage", "What that means here"], rows)}
</section>
<section>
<h2>Bottom line</h2>
<p class="callout">Nothing in this catalogue is buyable on the strength of its listing alone. The listing can tell you the karat, sometimes the weight, and the return terms. It cannot tell you whether the ring is solid, whether it is hallmarked, or whether the gold is the karat claimed — those need the physical ring, a jeweler, and an XRF reading. What this catalogue does is remove the guesswork from everything that <i>can</i> be read, and mark the rest clearly.</p>
</section>
"""
    return chrome("checklist.html", "", "The buying checklist", "Twelve tests, the official rule behind each, and exactly how far the published data gets you.", body)


def page_flagged():
    order = {"high": 0, "medium": 1, "low": 2}
    blocks = []
    for f in sorted(D["flags"], key=lambda x: (order[x["severity"]], x["id"])):
        srcs = " · ".join(f'<a href="{esc(u)}" rel="noopener">{esc(u)}</a>' for u in f["sources"])
        ids = ", ".join(f'<a href="listings.html">{esc(i)}</a>' for i in f["listingIds"]) if f["listingIds"] else "—"
        blocks.append(f"""
<section class="flagblock" id="{esc(f["id"])}">
  <h2><span class="sev s-{esc(f["severity"])}">{esc(f["severity"])}</span> {esc(f["title"])}</h2>
  <p>{esc(f["detail"])}</p>
  <p class="tiny">Affects: {ids}</p>
  <p class="tiny">Sources: {srcs}</p>
</section>""")
    body = f"""
<p class="lede">These are the irregularities found while verifying. None of them blocks publication — they are published <i>because</i> they are open. Each one says what is unknown and what would settle it.</p>
<section>
<h2>Index</h2>
<ul class="tight">
{''.join(f'<li><a href="#{esc(f["id"])}">{esc(f["id"])}</a> — {esc(f["title"])} <span class="sev s-{esc(f["severity"])}">{esc(f["severity"])}</span></li>' for f in sorted(D["flags"], key=lambda x: (order[x["severity"]], x["id"])))}
</ul>
</section>
{''.join(blocks)}
<section>
<h2>Withdrawn from a previous pass</h2>
<p>The earlier dashboard in this repo published an Etsy band as selling below its metal value. The price behind that claim came from a search snippet; the live listing is sold out and shows no price. It is withdrawn here — see <a href="#G-PRICE-BLANK-SOLD">G-PRICE-BLANK-SOLD</a>. The older pages are preserved for the record at <a href="../index-37e8ff42.html">index-37e8ff42.html</a> and <a href="../docs/index.html">docs/</a>.</p>
</section>
"""
    return chrome("flagged.html", "", "Flagged for review", f"{STATS['flags']} irregularities, each with its source and the evidence that would close it.", body)


def page_sources():
    rows = []
    prod = sorted({x["url"] for x in LIST})
    for r in D["references"]:
        quotes = "<br>".join(f'“{esc(q)}”' for q in r["quotes"])
        rows.append([
            f'<a href="{esc(r["url"])}" rel="noopener">{esc(r["title"])}</a><br><span class="tiny">{esc(r["publisher"])}</span>',
            quotes,
            esc(r["usedFor"]),
            esc(r["verified"]) + (f'<br><span class="tiny">{esc(r["evidence"])}</span>' if r.get("evidence") else ""),
        ])
    prows = [[f'<a href="{esc(u)}" rel="noopener">{esc(u)}</a>', "product / listing page"] for u in prod]
    srows = [[f'<a href="{esc(s["home"])}" rel="noopener">{esc(s["home"])}</a>', esc(s["name"])] for s in D["sellers"]]
    body = f"""
<section>
<h2>Official rules and reference pages</h2>
{table(["Source", "What it says (verbatim)", "Used for", "Captured"], rows)}
</section>
<section>
<h2>Seller pages used for rows</h2>
{table(["URL", "Type"], prows)}
</section>
<section>
<h2>Seller home pages</h2>
{table(["URL", "Seller"], srows)}
</section>
<p class="note">Every quote above was copied from the page on the date shown and is also stored verbatim in <code>verification/evidence/</code>, so you can diff the published table against what the page actually said.</p>
"""
    return chrome("sources.html", "", "Sources", "The official pages behind every rule and every row — with the exact quote used.", body)


def page_method():
    pass_rows = []
    for p in PASSES:
        p["rendered"] = True
        pass_rows.append([p["n"], esc(p["when"]), esc(p["what"]), f'{p["checks"]}', f'{p["fail"]}', f'{p["warn"]}',
                          esc(p.get("note", ""))])
    body = f"""
<section>
<h2>The rule</h2>
<p class="callout">{esc(D['meta']['rule'])}</p>
<p>Practically: a value is written down only if it was read off the seller's own page (or an official regulator's page) at a known time, and the exact text is saved in this repository. Derived numbers are never typed — the builder computes them and the checker recomputes them independently.</p>
</section>

<section>
<h2>How verification works here</h2>
<table class="tbl">
<thead><tr><th>Check</th><th>What it does</th></tr></thead>
<tbody>
<tr><td>Evidence match</td><td>For every row, each recorded value must appear <b>verbatim</b> in the saved capture of that page (a "token"). A number that is not in the capture fails the build.</td></tr>
<tr><td>Arithmetic</td><td>Fine gold, metal value, troy ounces, price-per-gram and the price ÷ metal multiple are recomputed from the raw inputs by the checker and compared with what the site renders.</td></tr>
<tr><td>Domain allowlist</td><td>Every link in the dataset must belong to a seller's real domain or an official body (FTC, eCFR/Cornell LII, BBB, Etsy Help, Kitco). A link to an unknown domain fails.</td></tr>
<tr><td>Money audit</td><td>Every dollar amount that appears in the generated HTML must trace back to a seller's published price, a reference quote, or a recomputed value. A hand-typed price fails.</td></tr>
<tr><td>Link integrity</td><td>Every internal link and anchor on every page must resolve to a file or id in the built site.</td></tr>
<tr><td>Flag cross-reference</td><td>Every flag referenced by a row must exist, and every listing id a flag mentions must exist.</td></tr>
</tbody>
</table>
<p class="note">Run it yourself: <code>python3 tools/check_report.py</code>. It prints a per-check summary and exits non-zero on failure. The pass log below is generated from the run.</p>
</section>

<section>
<h2>Verification passes</h2>
{table(["#", "When (UTC)", "Scope", "Checks", "Fail", "Warn", "Note"], pass_rows) if pass_rows else "<p class='blankline'>No pass recorded yet.</p>"}
</section>

<section>
<h2>Provenance labels used in the tables</h2>
<ul class="tight">
<li><b>A</b> — re-read live in this pass ({D['meta']['provenanceLegend']['A']})</li>
<li><b>B</b> — {esc(D['meta']['provenanceLegend']['B'])}</li>
</ul>
<p>15 of 27 rows are B. That is deliberate transparency, not a claim of equal confidence: a B row's price could have changed since capture. The source link is one click away for exactly that reason.</p>
</section>

<section>
<h2>Limitations you should hold in mind</h2>
<ul class="tight">
<li><b>Stamps cannot be seen online.</b> No seller in this catalogue publishes a hallmark photo. The FTC's own advice — don't buy gold jewellery without a maker's mark next to the karat — can only be satisfied in person.</li>
<li><b>Weights are mostly unpublished.</b> {STATS['n'] - STATS['withWeight']} of {STATS['n']} rows have no seller-published weight, so their gold value is unknown, not zero.</li>
<li><b>Prices are snapshots.</b> Etsy listings carry timed promotions ("25% off · Limited time sale"); the recorded figure is what the page showed at capture.</li>
<li><b>Reputation is thin.</b> Only two sellers have an independent source verified here; the rest are blank rather than assumed.</li>
<li><b>No currency conversion, ever.</b> When Brilliant Earth served the 18K page in euros, the USD cell was left blank.</li>
<li><b>Not financial or legal advice.</b> Verify with an independent jeweler, ask for XRF, and keep the paperwork.</li>
</ul>
</section>

<section>
<h2>Archive — earlier passes in this repo</h2>
<p>Three earlier deliveries are preserved unmodified: <a href="../index-37e8ff42.html">index-37e8ff42.html</a> (the previous root dashboard), <a href="../site/listings.html">site/</a> (its subpages) and <a href="../docs/index.html">docs/</a> (a parallel session's site). This pass adds <code>verification/</code>, <code>report/</code> and this dashboard; nothing from those sessions was edited or deleted.</p>
</section>
"""
    return chrome("method.html", "", "Method & passes", "How the no-hallucination rule is enforced mechanically, and what this project still cannot tell you.", body)


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    return full


# The root index.html is the integrated dashboard (owned by the final integration session);
# this suite's landing page is report/index.html, so a rebuild never touches the root page.
write("report/index.html", page_index())
write("report/listings.html", page_listings())
write("report/karat.html", page_karat())
write("report/value.html", page_value())
write("report/sellers.html", page_sellers())
write("report/checklist.html", page_checklist())
write("report/flagged.html", page_flagged())
write("report/sources.html", page_sources())
write("report/method.html", page_method())
with open(PASSES_FILE, "w", encoding="utf-8") as f:
    json.dump({"passes": PASSES}, f, indent=1)
print(f"built 9 pages (pass log: {len(PASSES)})")
