"""Gold price reference, raw-gold equivalents and the calculator."""
from __future__ import annotations

from ..base import esc, ext, layout, load, usd
from ..tables import spot

OZ = 31.1034768


def reference_table() -> str:
    data = load("gold-prices.json")
    rows = "".join(
        f'<tr><td>{esc(o["provider"])}</td><td class="num">{usd(o["usd_per_troy_oz"], 2)}</td>'
        f'<td class="num">{usd(o["usd_per_troy_oz"] / OZ, 2)}</td>'
        f'<td class="mono">{esc(o["quote_timestamp"])}</td><td>{ext(o["url"], "open source")}</td></tr>'
        for o in data["observations"]
    )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>Source</th><th>USD / troy oz</th><th>USD / gram (÷ {OZ})</th><th>Quote timestamp</th><th>Link</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""


def raw_gold_table() -> str:
    ref = spot()
    per_gram = ref["usd_per_troy_oz"] / OZ
    weights = [1, 2, 3, 5, 7, 10, 15, 20, 30]
    rows = []
    for w in weights:
        cells = "".join(f'<td class="num">{usd(w * (k / 24) * per_gram, 2)}</td>' for k in (10, 14, 18, 24))
        rows.append(f'<tr><td class="num">{w} g</td>{cells}</tr>')
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>Raw weight</th><th>10K (41.7%)</th><th>14K (58.3%)</th><th>18K (75.0%)</th><th>24K (99.9%)</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    <p class="fine">Fine-gold melt value = weight × (karat ÷ 24) × {usd(per_gram, 2)}/g, using the {esc(ref['provider'])}
    quote of {usd(ref['usd_per_troy_oz'], 2)}/oz captured {esc(ref['captured_at_utc'][:16].replace('T', ' '))} UTC.
    These are metal-only values: they ignore labour, setting, design, duty and retail margin, and they are not resale offers.</p>"""


def implied_table() -> str:
    entries = [e for e in load("entries.json")["entries"] if e.get("price_usd") is not None]
    ref = spot()
    per_gram = ref["usd_per_troy_oz"] / OZ
    rows = []
    for e in entries:
        fine = e["price_usd"] / per_gram
        rows.append(
            f'<tr><td><a href="../pages/all-rings.html#{esc(e["id"])}">{esc(e["id"])}</a></td>'
            f'<td>{esc(e["title"])}</td><td class="num">{usd(e["price_usd"])}</td>'
            f'<td class="num">{fine:.2f} g</td>'
            f'<td class="cell-note">{esc(e["price_basis"])}</td></tr>'
        )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>ID</th><th>Ring</th><th>Captured price</th><th>Fine gold the price equals at spot</th><th>Price covers</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    <p class="fine"><strong>This is not the ring's weight.</strong> It divides the asking price by the spot value of one gram of pure gold,
    which answers a different question: if you spent this money on raw metal instead, how much fine gold would it buy? A setting
    price that buys only a gram or two of metal is normal, because labour and design dominate. Once a seller publishes the actual
    gram weight, the same division in reverse becomes a real “is this unusually cheap?” test.</p>"""


def calculator() -> str:
    ref = spot()
    return f"""
<section class="panel calc" id="calculator" data-spot="{ref['usd_per_troy_oz']}">
  <h2>Gold value calculator</h2>
  <p>Weights are yours to enter — the tool does not guess them. Spot is fixed at the captured
  {usd(ref['usd_per_troy_oz'], 2)}/oz ({esc(ref['quote_timestamp'])}), so results are a check against that snapshot, not a live quote.</p>
  <form class="calc-form" onsubmit="return false;">
    <label class="tool"><span>Ring weight (g)</span><input id="calc-grams" type="number" min="0" step="0.01" value="3" inputmode="decimal"></label>
    <label class="tool"><span>Karat</span>
      <select id="calc-karat"><option value="10">10K — 41.7%</option><option value="14" selected>14K — 58.3%</option><option value="18">18K — 75.0%</option><option value="22">22K — 91.7%</option><option value="24">24K — 99.9%</option></select></label>
    <label class="tool"><span>Price paid (USD, optional)</span><input id="calc-price" type="number" min="0" step="1" placeholder="e.g. 1255" inputmode="decimal"></label>
  </form>
  <div class="calc-out" aria-live="polite">
    <div class="stat"><div class="stat-value" id="out-fine">—</div><div class="stat-label">fine gold in the ring (g)</div></div>
    <div class="stat"><div class="stat-value" id="out-value">—</div><div class="stat-label">melt value at captured spot</div></div>
    <div class="stat"><div class="stat-value" id="out-mult">—</div><div class="stat-label">price ÷ melt value</div></div>
  </div>
  <p class="fine" id="out-note">Enter the weight the seller gives you in writing. A multiplier below about 1 means the price is at or
  under the metal value — treat that as a red flag, because labour and setting cost money. Multipliers of roughly 2–4 are typical
  for retail settings; this is a sanity check, not an appraisal.</p>
</section>"""


def prices_page() -> str:
    ref = spot()
    body = f"""
<section class="page-head">
  <p class="eyebrow">Gold price &amp; calculator</p>
  <h1>What the gold in a ring is actually worth</h1>
  <p class="lede">Three independent spot quotes captured on the same day, the raw-gold equivalents for common weights and karats,
  and a calculator that stays honest: it only computes with a weight you supply.</p>
</section>

<section>
  <h2>Spot references captured</h2>
  {reference_table()}
</section>

<section>
  <h2>Raw gold value by weight and karat</h2>
  {raw_gold_table()}
</section>

{calculator()}

<section>
  <h2>What the captured prices equal in raw gold</h2>
  <p>A cross-check on asking prices. Read the caveat under the table before drawing conclusions.</p>
  {implied_table()}
</section>

<section class="panel panel-warn">
  <h3>Why this shortlist cannot yet answer “is it unusually cheap?”</h3>
  <p>The checklist says to compare the price with the ring's gold weight. That needs a gram figure, and
  <strong>none of the {len(load('entries.json')['entries'])} listings published one</strong> in the page text captured here
  (flag F-004). Until a seller puts the weight in writing, a price-per-gram claim would be invented — so this page shows the
  arithmetic you can run, and leaves the comparison open.</p>
  <p>Gold spot on {esc(ref['captured_at_utc'][:10])} was {usd(ref['usd_per_troy_oz'], 2)}/oz. Any figure on this site is tied to that
  timestamp; re-open {ext(ref['url'], 'the source')} before relying on it.</p>
</section>
"""
    return layout(
        "../",
        "Gold price and calculator — GOLD5",
        "Captured gold spot references, raw-gold value tables by weight and karat, and a calculator that requires a seller-confirmed weight.",
        "prices",
        body,
    )
