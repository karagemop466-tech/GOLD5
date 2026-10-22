#!/usr/bin/env python3
"""Generate the GitHub Pages site into docs/ from data/*.json.  Standard library only.
Pipeline: build pages -> run hallucination check -> build Verification page -> re-check -> exit 1 on FAIL.
"""
import sys, os, json, html, shutil, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import goldlib as G
import check_hallucinations as C

e = html.escape
REG = set()
def M(x):
    """format + register a CALCULATED dollar amount (so the checker knows it is derived, not typed in)."""
    REG.add("{:.2f}".format(x)); return G.money(x)

spot = G.load("spot.json"); rings = G.load("rings.json"); sellers = G.load("sellers.json"); flags = G.load("flags.json")
SM = {s["id"]: s for s in sellers}; FM = {f["id"]: f for f in flags}
OZ, GPO = spot["usd_per_troy_oz_bid"], spot["grams_per_troy_oz"]
PG = G.per_gram(OZ, GPO)
CAP = spot["captured_date"]
REPO = "https://github.com/karagemop466-tech/GOLD5"

NAV = [("index.html", "Dashboard"), ("rings.html", "Rings"), ("calculator.html", "Calculator"), ("analysis.html", "Analysis"),
       ("sellers.html", "Sellers"), ("checklist.html", "Checklist"), ("flagged.html", "Flagged for Review"),
       ("verification.html", "Verification"), ("sources.html", "Sources")]

CSS = """
:root{--bg:#f6f4ee;--card:#fff;--ink:#1d1d1f;--mut:#6b6b70;--gold:#b8860b;--gold2:#f3e3a6;--line:#e4dfd0;--red:#b3261e;--amb:#8a5a00;--grn:#1b6e3a;--blu:#1f4e8c}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}
a{color:var(--blu)}header{background:#1d1a12;color:#fff;position:sticky;top:0;z-index:5}
.bar{max-width:1200px;margin:0 auto;padding:10px 20px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.brand{font-weight:700;color:var(--gold2);margin-right:14px;text-decoration:none}
nav a{color:#ddd;text-decoration:none;padding:6px 10px;border-radius:6px;font-size:14px}nav a:hover{background:#3a3524}nav a.on{background:var(--gold);color:#fff}
main{max-width:1200px;margin:0 auto;padding:22px 20px 60px}h1{margin:.2em 0 .1em;font-size:28px}h2{margin-top:1.6em;font-size:20px}
.sub{color:var(--mut);margin:0 0 18px}.nh{background:#fff7d6;border:2px solid var(--gold);border-radius:10px;padding:14px 18px;margin:0 0 20px}
.nh b.t{color:#7a5200;letter-spacing:.04em}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}.card .k{color:var(--mut);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em}
.card .v{font-size:26px;font-weight:700}.card small{color:var(--mut)}a.card{text-decoration:none;color:inherit}a.card:hover{border-color:var(--gold)}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#faf6e6;position:sticky;top:0;white-space:nowrap;cursor:default}
tr:last-child td{border-bottom:0}td.n,th.n{text-align:right;white-space:nowrap}.blank{color:var(--red);font-style:italic;font-size:12.5px}
.badge{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;font-weight:600;white-space:nowrap}
.b-unverified{background:#fde7e5;color:var(--red)}.b-irregularity{background:#ffe9c7;color:var(--amb)}.b-needs{background:#e3ecfa;color:var(--blu)}.b-ok{background:#def3e5;color:var(--grn)}
.calc{color:var(--mut);font-size:12px}.flagl a{margin-right:4px;font-size:12px}input,select{font:inherit;padding:7px 9px;border:1px solid #cfc8b0;border-radius:6px;background:#fff}
.form{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
.form label{display:block;font-size:12.5px;color:var(--mut);margin-bottom:3px}.form input,.form select{width:100%}.out{font-size:22px;font-weight:700}
ul.cl{list-style:none;padding:0}ul.cl li{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin-bottom:8px}
.fil{margin:0 0 10px;width:100%;max-width:380px}footer{color:var(--mut);font-size:12.5px;margin-top:30px}code{background:#efe9d3;padding:1px 5px;border-radius:4px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}.pre{white-space:pre-wrap}
"""

def page(fname, title, body, sub=""):
    nav = "".join(f'<a href="{h}" class="{"on" if h==fname else ""}">{e(t)}</a>' for h, t in NAV)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — GOLD5 Gold Engagement Ring Finder</title><link rel="stylesheet" href="style.css"></head><body>
<header><div class="bar"><a class="brand" href="index.html">◆ GOLD5</a><nav>{nav}</nav></div></header>
<main><h1>{e(title)}</h1><p class="sub">{sub}</p>{body}
<footer>Data snapshot captured {CAP} (UTC date). Source code &amp; raw evidence: <a href="{REPO}">{REPO.replace('https://','')}</a>. Every figure is traceable to a linked seller page — see <a href="verification.html">Verification</a>.</footer></main></body></html>"""

NOHALL = f"""<div class="nh"><b class="t">◆ NO HALLUCINATIONS RULE</b><br>
Every price, weight, karat and policy on this site was copied from the linked <b>official seller page</b> on the capture date ({CAP}).
Anything that could not be confirmed there is <b>left blank and flagged <span class="badge b-unverified">unverified</span></b> — nothing is guessed, estimated or inferred.
Values labelled <span class="calc">calculated</span> are plain arithmetic on verified inputs, with the formula shown.
Prices change and gold moves every few seconds: <b>re-check the listing before you buy</b>.
A <a href="verification.html">hallucination check</a> runs after every review pass — and you should run it again too (<code>python3 tools/check_hallucinations.py</code>).</div>"""

BLANK = '<span class="blank">blank — unverified</span>'
def val(x, fmt=lambda v: e(str(v))):
    return BLANK if x is None else fmt(x)
def link(u, t="source ↗"): return f'<a href="{e(u)}" rel="noopener" target="_blank">{e(t)}</a>'
def status_badge(s):
    c = {"unverified": "b-unverified", "irregularity": "b-irregularity", "needs review": "b-needs"}.get(s, "b-ok")
    return f'<span class="badge {c}">{e(s)}</span>'

def ring_calc(r):
    gv = G.gold_value(r["weight_g"], r["karat"], OZ, GPO)
    ratio = (r["price_usd"] / gv) if (gv and r["price_usd"] is not None) else None
    return gv, ratio

# ---------------- rings ----------------
def rings_table(compact=False):
    rows = []
    for r in rings:
        s = SM[r["seller_id"]]; gv, ratio = ring_calc(r)
        src, cap = G.evidence_meta(r["evidence"])
        fl = " ".join(f'<a href="flagged.html#{e(f)}" title="{e(FM[f]["title"])}">{e(f)}</a>' for f in r["flags"])
        solid = f'Yes — “{e(r["solid_quote"])}”' if r["solid_stated"] else '<span class="blank">not stated on page</span>'
        rows.append(f"""<tr id="{r['id']}"><td><b>{r['id']}</b></td><td>{e(s['name'])}</td><td>{e(r['name'])}<br>{link(r['url'],'view listing ↗')}</td>
<td class="n">{val(r['price_text'])}</td><td>{e(r['price_basis'])}</td><td class="n">{val(r['karat'], lambda v: f'{v}K')}</td>
<td class="n">{val(r['weight_text'])}</td><td>{solid}</td><td><span class="blank">not stated on page</span></td>
<td class="n">{(M(gv)+'<br><span class="calc">calculated</span>') if gv is not None else BLANK}</td>
<td class="n">{(f'{ratio:.2f}×<br><span class="calc">calculated</span>') if ratio is not None else BLANK}</td>
<td>{cap}</td><td>{link(r.get('price_source_url') or r['url'],'price source ↗')}</td><td class="flagl">{fl}</td></tr>""")
    head = "<tr><th>ID</th><th>Seller</th><th>Ring / listing</th><th class='n'>Price (USD)</th><th>Price basis</th><th class='n'>Karat</th><th class='n'>Weight</th><th>“Solid gold” stated?</th><th>Hallmark + maker’s mark</th><th class='n'>Gold value @ spot</th><th class='n'>Price ÷ gold value</th><th>Captured</th><th>Official source</th><th>Flags</th></tr>"
    return f'<div class="tw"><table id="rt"><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'

FILTER_JS = """<script>function f(i,t){var q=document.getElementById(i).value.toLowerCase();document.querySelectorAll('#'+t+' tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''})}</script>"""

def p_rings():
    return page("rings.html", "All Ring Listings",
        NOHALL + f"""<input class="fil" id="q" placeholder="Filter by seller, ring, ID…" oninput="f('q','rt')">{rings_table()}{FILTER_JS}
<h2>How to read this table</h2><ul>
<li><b>Blank — unverified</b> means the seller’s page did not state that value (or it could not be confirmed). It is never filled in. See <a href="flagged.html">Flagged for Review</a>.</li>
<li><b>Gold value @ spot (calculated)</b> = weight (g) × Kitco spot per gram ({M(PG)}/g from {G.money(OZ)}/oz, {CAP}) × karat ÷ 24. Only shown when the listing states both weight and karat. It is <i>melt value of the gold only</i> — stones, labor and retail margin are not included.</li>
<li><b>Price ÷ gold value</b> is only meaningful for <i>setting-only</i> rows. Rows that include diamonds also pay for the stones.</li>
<li>Weights marked “Approximate” are the seller’s own approximations; confirm on a scale after delivery.</li></ul>""",
        "All entries, one row each, every row linked to the seller’s own page.")

# ---------------- calculator ----------------
def p_calc():
    purity = "".join(f"<tr><td>{k}</td><td class='n'>{v}</td><td class='n'>{pct}</td></tr>" for (k, v), pct in
        zip(spot["kitco_value_by_purity_per_oz"].items(), ["99.99%", "91.67%", "75.00%", "58.33%", "41.67%"]))
    data = [{"id": r["id"], "name": r["name"], "w": r["weight_g"], "k": r["karat"], "p": r["price_usd"]} for r in rings]
    return page("calculator.html", "Gold Weight & Value Calculator", NOHALL + f"""
<p>Gold content and melt value of a ring: <b>weight (g) × (spot per troy oz ÷ {spot['grams_per_troy_oz_text']} g) × karat ÷ 24</b>. The spot field starts at the Kitco snapshot below
({CAP}, {e(spot['kitco_timestamp'])}). <b>Anything you type is your own input, not verified site data.</b> For a newer spot price use <a href="{spot['source_url']}" target="_blank" rel="noopener">kitco.com</a>.</p>
<div class="form">
<div><label>Gold spot (USD per troy oz)</label><input id="spot" type="number" step="0.01" value="{OZ:.2f}"></div>
<div><label>Karat</label><select id="kt"><option>10</option><option selected>14</option><option>18</option><option>22</option><option>24</option></select></div>
<div><label>Ring weight</label><input id="wt" type="number" step="0.01" placeholder="from the listing"></div>
<div><label>Weight unit</label><select id="un"><option value="1">grams</option><option value="1.55517384">pennyweight (dwt)</option><option value="31.1034768">troy ounce</option></select></div>
<div><label>Asking price (USD, optional)</label><input id="ask" type="number" step="0.01" placeholder="from the listing"></div></div>
<div class="grid" style="margin-top:12px">
<div class="card"><div class="k">Pure gold in ring</div><div class="out" id="o1">—</div></div>
<div class="card"><div class="k">Gold (melt) value</div><div class="out" id="o2">—</div></div>
<div class="card"><div class="k">Asking price ÷ gold value</div><div class="out" id="o3">—</div></div>
<div class="card"><div class="k">Asking price − gold value</div><div class="out" id="o4">—</div></div></div>
<p class="calc">Calculated in your browser. Red flag: an asking price <i>below</i> the gold value of a ring that is claimed to be solid gold. A price near or above it is normal (labor, stones, margin) and proves nothing about authenticity — verify with XRF.</p>
<h2>Kitco snapshot — gold value by purity (1 troy oz)</h2>
<div class="tw"><table><thead><tr><th>Purity</th><th class="n">Value (USD)</th><th class="n">Kitco purity %</th></tr></thead><tbody>{purity}</tbody></table></div>
<p>Source: {link(spot['source_url'],'Kitco live gold price ↗')} · bid {G.money(OZ)}/oz · captured {CAP}, {e(spot['kitco_timestamp'])} · evidence <a href="evidence/spot_kitco.txt">spot_kitco.txt</a>. Kitco notes: “Estimated metal value only, retail premiums may apply to physical products.” See flag <a href="flagged.html#G-SPOT-DUAL">G-SPOT-DUAL</a>.</p>
<h2>Listings in this project, re-priced at the spot you enter</h2>
<div class="tw"><table id="ct"><thead><tr><th>ID</th><th>Ring</th><th class="n">Karat</th><th class="n">Weight (g)</th><th class="n">Price</th><th class="n">Gold value</th><th class="n">Price ÷ value</th></tr></thead><tbody></tbody></table></div>
<script>
var G={spot['grams_per_troy_oz']},D={json.dumps(data)};
function fm(x){{return '$'+x.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}})}}
function calc(){{var s=+spot.value,k=+kt.value,w=+wt.value*+un.value,a=+ask.value;
 if(!(s>0&&w>0)){{o1.textContent=o2.textContent=o3.textContent=o4.textContent='—'}}else{{var pure=w*k/24,v=pure*s/G;o1.textContent=pure.toFixed(3)+' g';o2.textContent=fm(v);
 if(a>0){{o3.textContent=(a/v).toFixed(2)+'×';o4.textContent=fm(a-v)}}else{{o3.textContent=o4.textContent='—'}}}}
 var h='';D.forEach(function(r){{var v=(r.w&&r.k&&s>0)?r.w*(s/G)*r.k/24:null;h+='<tr><td>'+r.id+'</td><td>'+r.name+'</td><td class="n">'+(r.k?r.k+'K':'<span class="blank">blank — unverified</span>')+'</td><td class="n">'+(r.w!=null?r.w:'<span class="blank">blank — unverified</span>')+'</td><td class="n">'+(r.p!=null?fm(r.p):'<span class="blank">blank — unverified</span>')+'</td><td class="n">'+(v!=null?fm(v):'<span class="blank">blank</span>')+'</td><td class="n">'+((v&&r.p!=null)?(r.p/v).toFixed(2)+'×':'<span class="blank">blank</span>')+'</td></tr>'}});
 document.querySelector('#ct tbody').innerHTML=h}}
['spot','kt','wt','un','ask'].forEach(function(i){{document.getElementById(i).addEventListener('input',calc)}});calc();
</script>""", "Check what the gold in a ring is worth before you pay.")

# ---------------- analysis ----------------
def p_analysis():
    n = len(rings); priced = [r for r in rings if r["price_usd"] is not None]
    w = [r for r in rings if r["weight_g"] is not None]; solid = [r for r in rings if r["solid_stated"]]
    k = [r for r in rings if r["karat"] is not None]
    both = [r for r in priced if r["weight_g"] is not None and r["karat"] is not None]
    calc_rows = sorted(both, key=lambda r: r["price_usd"] / ring_calc(r)[0])
    trs = ""
    for r in calc_rows:
        gv, ratio = ring_calc(r); pure = r["weight_g"] * r["karat"] / 24
        stones = "setting only" if "Setting only" in r["price_basis"] else "includes diamonds"
        trs += f"<tr><td><a href='rings.html#{r['id']}'>{r['id']}</a></td><td>{e(SM[r['seller_id']]['name'])}</td><td>{e(r['name'])}</td><td>{e(stones)}</td><td class='n'>{r['price_text']}</td><td class='n'>{r['weight_text']}</td><td class='n'>{pure:.3f} g</td><td class='n'>{M(gv)}</td><td class='n'>{ratio:.2f}×</td><td class='n'>{M(r['price_usd']/pure)}/g</td><td>{link(r['url'],'source ↗')}</td></tr>"
    below = [r for r in both if r["price_usd"] < ring_calc(r)[0]]
    settings = [r for r in calc_rows if "Setting only" in r["price_basis"]]
    s_txt = ""
    if settings:
        lo, hi = ring_calc(settings[0])[1], ring_calc(settings[-1])[1]
        s_txt = f"<li>Among the {len(settings)} setting-only rings with a stated weight, price is <b>{lo:.2f}× to {hi:.2f}×</b> the calculated gold value (calculated).</li>"
    both_ids = ", ".join(r["id"] for r in both)
    return page("analysis.html", "Analysis & Findings", NOHALL + f"""
<h2>Coverage of the checklist across {n} captured listings</h2>
<div class="grid">
<div class="card"><div class="k">Price on page</div><div class="v">{len(priced)}/{n}</div><small>{', '.join(r['id'] for r in rings if r['price_usd'] is None)} has none</small></div>
<div class="card"><div class="k">Karat confirmed in page text</div><div class="v">{len(k)}/{n}</div><small>BE listing-only rows blank</small></div>
<div class="card"><div class="k">Weight in grams stated</div><div class="v">{len(w)}/{n}</div><small>checklist: seller must provide</small></div>
<div class="card"><div class="k">“Solid gold” explicitly stated</div><div class="v">{len(solid)}/{n}</div><small>{', '.join(r['id'] for r in solid)}</small></div>
<div class="card"><div class="k">Hallmark + maker’s mark stated</div><div class="v">0/{n}</div><small>no listing states stamps</small></div></div>
<h2>Findings</h2><ul>
<li><b>No listing satisfied the full checklist on its page alone.</b> Not one states a hallmark plus maker’s mark, and only {len(solid)} of {n} say “solid gold”. For every ring these are questions to put to the seller <i>in writing</i> before buying.</li>
<li><b>Weight is a major gap.</b> {n-len(w)} of {n} listings give no weight in grams, so gold content cannot be checked against price.</li>
{s_txt}
<li>Of the {len(both)} rings with price, weight and karat ({both_ids}), <b>{len(below)} priced below the calculated gold value</b>{'' if below else ' — so the “unusually cheap vs. gold weight” red flag was not triggered here. That does not prove purity: a stamp or a sensible price never does; only independent XRF testing does'}.</li>
<li><b>Return policies differ on resizing.</b> Blue Nile and Allurez both make resized/altered items non-returnable; Blue Nile includes one free resize within 6 months. Do not resize before your independent jeweler has tested the ring. Details on <a href="sellers.html">Sellers</a>.</li>
<li><b>Marketing price claims are not evidence.</b> Allurez (“Everyone Else” price) and The Jewelry Master (“Retail Price”) show comparison prices. They are excluded from all calculations — see <a href="flagged.html#F-ALLUREZ-REF">F-ALLUREZ-REF</a> and <a href="flagged.html#F-JM-RETAIL">F-JM-RETAIL</a>.</li>
<li><b>Gold is volatile.</b> Spot moves continuously; other sites’ quotes from earlier on {CAP} (unverified snippets) are listed under <a href="flagged.html#G-SPOT-XCHECK">G-SPOT-XCHECK</a>. Every “calculated” number here scales with the Kitco snapshot used ({G.money(OZ)}/oz) — use the <a href="calculator.html">calculator</a> for a fresh spot.</li></ul>
<h2>Price vs. gold content (rings with stated price, weight and karat)</h2>
<div class="tw"><table><thead><tr><th>ID</th><th>Seller</th><th>Ring</th><th>Basis</th><th class="n">Price</th><th class="n">Weight</th><th class="n">Pure gold</th><th class="n">Gold value (calc)</th><th class="n">Price ÷ value</th><th class="n">Price per g of pure gold (calc)</th><th>Source</th></tr></thead><tbody>{trs}</tbody></table></div>
<p class="calc">Formulas: pure gold g = weight × karat ÷ 24; gold value = pure gold g × ({G.money(OZ)} ÷ {spot['grams_per_troy_oz_text']}) ; ratios are price ÷ gold value. Inputs are the verified values on the <a href="rings.html">Rings</a> page and the Kitco snapshot. Rings that include diamonds (R09, R10) pay for stones too, so their ratio is not comparable to setting-only rows.</p>
<h2>Recommended next steps</h2><ol>
<li>Run the hallucination check again (<code>python3 tools/check_hallucinations.py</code>) and read <a href="flagged.html">Flagged for Review</a>.</li>
<li>For any ring you like: get <b>written</b> weight in grams, “solid gold” confirmation, photos of the karat + maker’s stamps, and the full return policy including resize/custom exclusions.</li>
<li>Re-check the price and the gold spot on the day you buy; pay by credit card.</li>
<li>On arrival and <b>before wearing or resizing</b>: independent jeweler — weigh it and run XRF; keep the listing, receipt and seller claims (see <a href="checklist.html">Checklist</a>).</li></ol>""",
        "Derived only from the verified rows. Blank cells are excluded, never estimated.")

# ---------------- sellers ----------------
def p_sellers():
    trs = ""
    for s in sellers:
        ct = "<br>".join(f"{e(c['text'])} {link(c['source'],'↗')}" for c in s["contact"])
        rings_ = ", ".join(f"<a href='rings.html#{r['id']}'>{r['id']}</a>" for r in rings if r["seller_id"] == s["id"])
        badge = status_badge("verified") if s["returns_verified"] else status_badge("unverified")
        trs += f"<tr><td><b>{e(s['name'])}</b><br>{link(s['home'],'official site ↗')}</td><td>{rings_}</td><td>{ct}</td><td>{e(s['returns_summary'])}</td><td>{badge}<br>{link(s['returns_url'],'policy source ↗')}</td><td><span class='blank'>blank — unverified</span> <a href='flagged.html#G-REVIEWS'>G-REVIEWS</a></td></tr>"
    return page("sellers.html", "Sellers, Contacts & Return Policies", NOHALL + f"""<div class="tw"><table><thead><tr><th>Seller</th><th>Rings</th><th>Contact (as shown on official site)</th><th>Return policy — incl. resize/custom exclusions</th><th>Status / source</th><th>Independent reviews &amp; complaints</th></tr></thead><tbody>{trs}</tbody></table></div>
<p>Independent review/complaint research is <b>not done</b>: it can’t be confirmed from a seller’s own site, and this project doesn’t guess. Manual review starting points: <a href="https://www.bbb.org/" rel="noopener" target="_blank">bbb.org</a> is NOT linked per seller because no BBB page was captured.</p>""".replace('<a href="https://www.bbb.org/" rel="noopener" target="_blank">bbb.org</a> is NOT linked per seller because no BBB page was captured.', "look up each business on the Better Business Bureau, your state attorney general’s complaint database and independent review sites, and confirm the business address and phone. Tracked as <a href='flagged.html#G-REVIEWS'>G-REVIEWS</a>."),
        "Policies quoted from each seller’s own site on the capture date.")

# ---------------- checklist ----------------
CHECK = [
 ("Gold purity", "Confirm the karat — 10K, 14K, 18K, etc. Higher karat = more gold.", "Karat column. Blank where the page didn’t state it."),
 ("Solid gold", "Listing must explicitly say solid gold — not plated, vermeil, gold-filled, gold overlay or gold-tone.", "“Solid gold stated?” column quotes the page. Most rows: not stated."),
 ("Hallmark", "Look for a 10K/14K/18K stamp plus a maker’s/manufacturer’s mark.", "No listing states stamps — ask for photos; confirm on arrival."),
 ("Weight", "Check the ring’s weight in grams. A legitimate seller should be able to provide it.", "Weight column; blank = ask the seller."),
 ("Seller reputation", "Research independent reviews and complaints; verify real contact information.", "Contacts shown from official sites; reviews NOT researched (G-REVIEWS)."),
 ("Price", "Compare the price with the ring’s gold weight and current gold value. Unusually cheap = red flag.", "Calculator + Analysis page, using the dated Kitco snapshot."),
 ("Return policy", "Make sure you can return it after inspecting it. Check exclusions on resized/custom rings.", "Sellers page quotes each policy where captured."),
 ("Payment", "Prefer a credit card for purchase protection. Avoid irreversible payment methods.", "Not verified per seller (G-PAYMENT)."),
 ("Documentation", "Keep the listing, receipt, description and seller’s claims about gold purity.", "Save the listing page (PDF/screenshot) and emails on the day you buy."),
 ("Upon arrival", "Before wearing/resizing, take it to an independent jeweler to verify purity and weight.", "Your step — do not resize first."),
 ("Best verification", "Ask for XRF testing or another professional purity test; don’t rely only on the stamp.", "Your step."),
 ("Walk-away rule", "If the seller won’t let you independently verify/return it: don’t buy it.", "Applies to every row."),
]
def p_check():
    li = "".join(f'<li><label><input type="checkbox" data-k="{i}"> <b>{e(a)}.</b> {e(b)}</label><br><span class="calc">In this project: {e(c)}</span></li>' for i, (a, b, c) in enumerate(CHECK))
    return page("checklist.html", "Online Buying Checklist", NOHALL + f"""<p><b>Key point:</b> a 14K or 18K stamp by itself does <b>not</b> prove purity. Safest path: reputable seller + proper markings + reasonable price + independent testing after delivery.
Ticks are saved only in your browser.</p><ul class="cl">{li}</ul>
<script>document.querySelectorAll('input[data-k]').forEach(function(c){{var k='gold5-'+c.dataset.k;c.checked=localStorage.getItem(k)==='1';c.onchange=function(){{localStorage.setItem(k,c.checked?'1':'0')}}}})</script>""",
        "Your checklist, with how each point is handled in this project.")

# ---------------- flagged ----------------
def p_flagged():
    used = {}
    for r in rings:
        for f in r["flags"]: used.setdefault(f, []).append(r)
    order = {"irregularity": 0, "unverified": 1, "needs review": 2}
    trs = ""
    for f in sorted(flags, key=lambda x: (order.get(x["status"], 9), x["id"])):
        aff = ", ".join(f"<a href='rings.html#{r['id']}'>{r['id']}</a> {link(r['url'],'↗')}" for r in used.get(f["id"], [])) or "—"
        lk = " ".join(link(u, "source ↗") for u in f["links"]) or "—"
        trs += f"<tr id='{f['id']}'><td><b>{f['id']}</b></td><td>{status_badge(f['status'])}</td><td><b>{e(f['title'])}</b><br>{e(f['detail'])}</td><td>{aff}</td><td>{lk}</td></tr>"
    cnt = {s: sum(1 for f in flags if f["status"] == s) for s in order}
    return page("flagged.html", "Flagged for Review", NOHALL + f"""
<p>These items do <b>not</b> block publication. Each is an <span class="badge b-unverified">unverified</span> value, an <span class="badge b-irregularity">irregularity</span> found while checking, or an item that <span class="badge b-needs">needs review</span>. Source links are provided for manual review — tell the project owner which ones to change.</p>
<div class="grid"><div class="card"><div class="k">Irregularities</div><div class="v">{cnt['irregularity']}</div></div><div class="card"><div class="k">Unverified</div><div class="v">{cnt['unverified']}</div></div><div class="card"><div class="k">Needs review</div><div class="v">{cnt['needs review']}</div></div></div>
<br><div class="tw"><table><thead><tr><th>ID</th><th>Status</th><th>What was found</th><th>Affected rings (listing link)</th><th>Source links</th></tr></thead><tbody>{trs}</tbody></table></div>""",
        "Unverified values, irregularities and open questions — with source links for manual review.")

# ---------------- sources ----------------
def p_sources():
    rows = []
    for p in sorted(glob.glob(os.path.join(G.EVID, "*.txt"))):
        n = os.path.basename(p)[:-4]; src, cap = G.evidence_meta(n)
        rows.append(f"<tr><td class='mono'>{n}</td><td>{link(src, src.replace('https://',''))}</td><td>{cap}</td><td><a href='evidence/{n}.txt'>verbatim excerpt</a></td></tr>")
    return page("sources.html", "Sources & Evidence", NOHALL + f"""<p>Every number on the site is checked against these saved verbatim excerpts by the hallucination check. Raw data: <a href="data/rings.json">rings.json</a>, <a href="data/sellers.json">sellers.json</a>, <a href="data/spot.json">spot.json</a>, <a href="data/flags.json">flags.json</a>.</p>
<div class="tw"><table><thead><tr><th>Evidence ID</th><th>Official page</th><th>Captured</th><th>Saved text</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="calc">Capture method: live page text fetched on the capture date. Three evidence files (<code>spot_crosscheck_snippets</code>, <code>bn_snippet_only</code>, and the two <code>dead_*</code> files) record items that could NOT be confirmed; nothing from them is used in a table value.</p>""",
        "Where every value came from.")

# ---------------- verification (needs check result) ----------------
def p_verif(R):
    hp = os.path.join(G.DATA, "pass_history.json")
    hist = json.load(open(hp)) if os.path.exists(hp) else []
    hr = "".join(f"<tr><td>{h['date']}</td><td>{e(h['label'])}</td><td class='n'>{h['passed']}</td><td class='n'>{h['fail']}</td><td class='n'>{h['warn']}</td><td class='n'>{h['info']}</td></tr>" for h in hist) or "<tr><td colspan=6>none</td></tr>"
    items = "".join(f"<tr><td>{i['level']}</td><td>{i['check']}</td><td>{e(i['message'])}</td></tr>" for i in R.items) or "<tr><td colspan=3>No findings — all checks passed.</td></tr>"
    state = "PASS" if R.count("FAIL") == 0 else "FAIL"
    return page("verification.html", "Verification & Hallucination Checks", NOHALL + f"""
<div class="grid"><div class="card"><div class="k">Latest check</div><div class="v">{state}</div><small>{CAP}</small></div><div class="card"><div class="k">Checks passed</div><div class="v">{R.npass}</div></div>
<div class="card"><div class="k">Fail</div><div class="v">{R.count('FAIL')}</div></div><div class="card"><div class="k">Warn / Info</div><div class="v">{R.count('WARN')} / {R.count('INFO')}</div></div></div>
<h2>What the hallucination check enforces</h2><ol>
<li><b>C1</b> every ring row links to an official page on its own seller’s domain;</li><li><b>C2</b> every saved evidence excerpt records its source URL and capture date (stale after {C.STALE_DAYS} days = warning);</li>
<li><b>C3</b> every price, karat, weight and “solid” claim appears <i>verbatim</i> in the saved evidence — an invented number fails the build;</li>
<li><b>C4</b> every blank value carries an “unverified” flag — nothing is filled in;</li><li><b>C5</b> the spot price and Kitco purity table match the saved Kitco text and k/24 arithmetic;</li>
<li><b>C6</b> seller contacts appear in evidence;</li><li><b>C7</b> every $ amount printed on every page is either in evidence or a registered calculation — typed-in numbers fail;</li>
<li><b>C8</b> all internal links and anchors resolve, and every external link is a known source URL;</li><li><b>C9</b> sanity checks: below-melt prices, implausible weights, duplicate URLs, identical specs across listings.</li></ol>
<p><b>Recommendation:</b> run it after <i>every</i> review or data change: <code>python3 tools/check_hallucinations.py --log "what I reviewed"</code>, then rebuild with <code>python3 tools/build_site.py</code>. A passing check shows internal consistency with the saved excerpts; it cannot prove the seller’s page is truthful, so also use the source links and the in-person XRF test.</p>
<p class="calc">Limit: the check cannot re-fetch seller sites from the build sandbox. Live-page verification was done at capture time; re-run the capture before relying on a price.</p>
<h2>Findings from the latest run</h2><div class="tw"><table><thead><tr><th>Level</th><th>Check</th><th>Message</th></tr></thead><tbody>{items}</tbody></table></div>
<h2>Pass history</h2><div class="tw"><table><thead><tr><th>Date</th><th>Review pass</th><th class="n">Passed</th><th class="n">Fail</th><th class="n">Warn</th><th class="n">Info</th></tr></thead><tbody>{hr}</tbody></table></div>""",
        "Every review pass ends with the hallucination check.")

# ---------------- index ----------------
def p_index():
    n = len(rings)
    nopen = len(flags)
    cards = [("rings.html", "Rings", f"All {n} captured listings in one table with source links."), ("calculator.html", "Calculator", "Weight × karat × spot = gold value."),
             ("analysis.html", "Analysis", "Price vs gold content, coverage and findings."), ("sellers.html", "Sellers", "Contacts and return / resize policies."),
             ("checklist.html", "Checklist", "Your buying checklist, tick-able."), ("flagged.html", "Flagged for Review", f"{nopen} open items with source links."),
             ("verification.html", "Verification", "Hallucination checks and pass history."), ("sources.html", "Sources", "Every official page and saved excerpt.")]
    cd = "".join(f'<a class="card" href="{h}"><div class="k">{e(t)}</div><div style="margin-top:4px">{e(d)}</div></a>' for h, t, d in cards)
    return page("index.html", "Gold Engagement Ring Finder", NOHALL + f"""
<div class="grid">
<div class="card"><div class="k">Gold spot (Kitco bid)</div><div class="v">{G.money(OZ)}</div><small>per troy oz · {CAP} · {e(spot['kitco_timestamp'].split(' (')[0])}<br>{M(PG)}/g (calculated) · {link(spot['source_url'],'Kitco ↗')}</small></div>
<div class="card"><div class="k">Listings captured</div><div class="v">{n}</div><small>{sum(1 for r in rings if r['price_usd'] is not None)} with a price · {len(sellers)} sellers</small></div>
<div class="card"><div class="k">Weight stated</div><div class="v">{sum(1 for r in rings if r['weight_g'] is not None)}/{n}</div><small>grams, on the listing</small></div>
<div class="card"><div class="k">“Solid gold” stated</div><div class="v">{sum(1 for r in rings if r['solid_stated'])}/{n}</div><small>explicit wording only</small></div>
<div class="card"><div class="k">Hallmark + maker’s mark</div><div class="v">0/{n}</div><small>none stated on any listing</small></div>
<div class="card"><div class="k">Flagged for review</div><div class="v">{nopen}</div><small><a href="flagged.html">see all</a></small></div></div>
<h2>Explore</h2><div class="grid">{cd}</div>
<h2>Bottom line</h2><p>No listing proved on its own page that it is solid, correctly stamped gold. Treat every row as <b>a lead to verify</b>: get the weight in grams, “solid gold” and stamp confirmation in writing, read the return policy for resize/custom exclusions, pay by credit card, and have an independent jeweler run <b>XRF testing before wearing or resizing</b>. If the seller won’t allow independent verification or return — don’t buy.</p>
<p class="calc">Recommended after each review: run the hallucination check — <a href="verification.html">how</a>.</p>""",
        "A simple dashboard of verified gold engagement ring listings, with the gold math.")

def build():
    os.makedirs(G.DOCS, exist_ok=True)
    for stale in glob.glob(os.path.join(G.DOCS, "*.html")): os.remove(stale)
    open(os.path.join(G.DOCS, "style.css"), "w").write(CSS)
    open(os.path.join(G.DOCS, ".nojekyll"), "w").write("")
    for sub, src in (("evidence", G.EVID), ("data", G.DATA)):
        d = os.path.join(G.DOCS, sub); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for p in glob.glob(os.path.join(src, "*.*")):
            if sub == "data" and os.path.basename(p) in ("computed_amounts.json",): continue
            shutil.copy(p, d)
    W = lambda n, c: open(os.path.join(G.DOCS, n), "w", encoding="utf-8").write(c)
    W("index.html", p_index()); W("rings.html", p_rings()); W("calculator.html", p_calc()); W("analysis.html", p_analysis())
    W("sellers.html", p_sellers()); W("checklist.html", p_check()); W("flagged.html", p_flagged()); W("sources.html", p_sources())
    json.dump(sorted(REG), open(os.path.join(G.DATA, "computed_amounts.json"), "w"))
    W("verification.html", "<html></html>")   # placeholder so link checks see the file
    R = C.run(with_site=True)
    W("verification.html", p_verif(R))
    json.dump(sorted(REG), open(os.path.join(G.DATA, "computed_amounts.json"), "w"))
    R2 = C.run(with_site=True)   # final authority: includes the verification page
    for i in R2.items: print(f"[{i['level']:4}] {i['check']}: {i['message']}")
    print(f"BUILD: passed={R2.npass} fail={R2.count('FAIL')} warn={R2.count('WARN')} info={R2.count('INFO')}")
    return R2

if __name__ == "__main__":
    R = build()
    sys.exit(1 if R.count("FAIL") else 0)
