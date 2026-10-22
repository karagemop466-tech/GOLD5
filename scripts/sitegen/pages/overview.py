"""Landing page: the rule, the scorecard, the state of the evidence."""
from __future__ import annotations

from ..base import badge, esc, ext, layout, load, usd
from ..tables import gold_value, spot

STATUS_BADGE = {
    "covered": ("Online — covered", "ok"),
    "gap": ("Gap — needs your action", "warn"),
    "offline": ("Offline step", "muted"),
}


def stat_tiles() -> str:
    entries = load("entries.json")["entries"]
    sellers = load("sellers.json")["sellers"]
    flags = load("flags.json")["flags"]
    priced = [e for e in entries if e.get("price_usd") is not None]
    weighed = [e for e in entries if e.get("weight_g") is not None]
    ref = spot()
    tiles = [
        (str(len(entries)), "ring entries", "all from official product pages"),
        (str(len(sellers)), "sellers", f"{sum(1 for s in sellers if s['contact']['status'] == 'verified')} with contact info verified"),
        (f"{len(weighed)}/{len(entries)}", "have a gram weight", "weight is the missing key metric"),
        (f"{len(priced)}/{len(entries)}", "have a verified price", "rest marked unverified"),
        (str(len(flags)), "flagged items", "published on the Flagged page"),
        (usd(ref["usd_per_troy_oz"], 2), "per troy oz (spot ref)", f"captured {ref['captured_at_utc'][:16].replace('T', ' ')} UTC"),
    ]
    return "".join(
        f'<div class="stat"><div class="stat-value">{v}</div><div class="stat-label">{esc(l)}</div>'
        f'<div class="stat-note">{esc(n)}</div></div>'
        for v, l, n in tiles
    )


def scorecard() -> str:
    items = load("checklist.json")["items"]
    rows = []
    for item in items:
        label, kind = STATUS_BADGE[item["status"]]
        rows.append(
            f'<tr><td class="cell-id">{esc(item["id"])}</td><td>{esc(item["requirement"])}</td>'
            f'<td>{badge(label, kind)}</td><td>{esc(item["online"])}</td>'
            f'<td class="cell-note">{esc(item["note"])}</td></tr>'
        )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>#</th><th>Checklist requirement</th><th>Status</th><th>What the web lets us confirm</th><th>Note</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    <p class="fine">Statuses are assigned mechanically: “covered” only when an official page supplied the value for every row it applies to;
    “gap” when at least one row is missing it. Nothing is marked covered on a seller's marketing claim alone.</p>"""


def price_strip() -> str:
    data = load("gold-prices.json")
    rows = "".join(
        f'<tr><td>{esc(o["provider"])}</td><td class="num">{usd(o["usd_per_troy_oz"], 2)}</td>'
        f'<td class="mono">{esc(o["quote_timestamp"])}</td><td>{ext(o["url"], esc(o["url"].split("//")[-1][:44]))}</td></tr>'
        for o in data["observations"]
    )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>Source</th><th>USD / troy oz</th><th>Quote timestamp (as published)</th><th>Official link</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""


def top_findings() -> str:
    flags = load("flags.json")["flags"]
    priority = ["F-004", "F-005", "F-006", "F-002", "F-007", "F-009"]
    lookup = {f["id"]: f for f in flags}
    items = []
    for fid in priority:
        f = lookup[fid]
        items.append(
            f'<li><a class="chip chip-{esc(f["severity"])}" href="pages/flagged.html#{esc(fid)}">{esc(fid)}</a> '
            f'<strong>{esc(f["title"])}</strong> — {esc(f["detail"])}</li>'
        )
    return f'<ul class="finding-list">{"".join(items)}</ul>'


def overview_page() -> str:
    meta = load("meta.json")
    entries = load("entries.json")["entries"]
    body = f"""
<section class="hero">
  <p class="eyebrow">Independent buying research · verified {esc(meta['verified_on_display'])}</p>
  <h1>Gold engagement rings: sourced, weighed, and honestly flagged</h1>
  <p class="lede">A working shortlist of gold engagement rings sold by five established retailers, checked line by line
  against their own product and policy pages. Every row carries the official link, the exact quoted text and a flag
  where the seller does not publish something the checklist requires.</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="pages/all-rings.html">See all {len(entries)} entries</a>
    <a class="btn" href="pages/flagged.html">Flagged for review</a>
    <a class="btn" href="pages/prices.html">Gold calculator</a>
  </div>
</section>

<section class="rule-card" aria-labelledby="rule-title">
  <h2 id="rule-title">The no-hallucination rule</h2>
  <p><strong>No price, weight, karat, hallmark, policy or contact detail appears on this site unless it was read from an
  official page and quoted verbatim.</strong> Values are never inferred, rounded from memory, or carried over from a
  search snippet. If a seller does not publish a value, the cell stays blank and the row is flagged as unverified.</p>
  <ul class="rule-list">
    <li><strong>One source per claim.</strong> Each table cell traces to a URL and a quote you can open yourself.</li>
    <li><strong>Arithmetic is labelled.</strong> The only computed number is fine-gold value at spot: grams × karat/24 × spot per gram, with the spot observation and timestamp printed.</li>
    <li><strong>Blank beats wrong.</strong> {len([e for e in entries if e.get('weight_g') is None])} of {len(entries)} rows have no gram weight because no listing published one. That is a finding, not a gap to fill in.</li>
    <li><strong>Re-checked at review time.</strong> Every review pass re-runs the hallucination checks described on the <a href="pages/method.html">Method</a> page.</li>
  </ul>
</section>

<section>
  <h2>At a glance</h2>
  <div class="stat-grid">{stat_tiles()}</div>
</section>

<section>
  <h2>Gold spot price references used</h2>
  <p>Three independent quotes captured within minutes of each other on {esc(meta['verified_on_display'])}. The calculator uses the
  <strong>{esc(spot()['provider'])}</strong> value ({usd(spot()['usd_per_troy_oz'], 2)}/oz).</p>
  {price_strip()}
  <p class="fine">Gold moves continuously; these are point-in-time observations, not current market data. LBMA benchmark tables are
  licence-only, so the LBMA auction price itself is not republished here.</p>
</section>

<section>
  <h2>Checklist scorecard</h2>
  <p>Your twelve buying requirements, scored against what the web evidence actually supports for this shortlist.</p>
  {scorecard()}
</section>

<section>
  <h2>Most important findings</h2>
  {top_findings()}
  <p><a class="btn" href="pages/flagged.html">Open all {len(load('flags.json')['flags'])} flagged items</a></p>
</section>

<section>
  <h2>What this means for buying</h2>
  <div class="two-col">
    <div class="panel">
      <h3>Safe path</h3>
      <ol class="steps">
        <li>Pick a row whose seller has verified contact details and a written return window.</li>
        <li>Message the seller for the <strong>gram weight</strong>, the <strong>hallmark + maker's mark</strong>, and written
          confirmation the ring is <strong>solid 14K/18K gold</strong> (not plated, vermeil, filled or overlay).</li>
        <li>Run the numbers in the <a href="pages/prices.html">calculator</a> against the captured spot price.</li>
        <li>Pay by <strong>credit card</strong>; keep the listing, the messages and the receipt.</li>
        <li>Before wearing or resizing, take it to an independent jeweler for a weight check and <strong>XRF</strong> purity test.</li>
      </ol>
    </div>
    <div class="panel panel-warn">
      <h3>Walk away if…</h3>
      <ul class="steps">
        <li>The seller will not state the gram weight in writing.</li>
        <li>The listing says “gold” but not the karat, or the price sits far below the fine-gold value at spot.</li>
        <li>Returns are excluded for resized or custom work and you have not confirmed the size.</li>
        <li>Payment must be irreversible (wire, crypto, gift card, peer-to-peer app).</li>
        <li>No one will let you have the ring independently tested.</li>
      </ul>
    </div>
  </div>
</section>
"""
    return layout("", "GOLD5 — Gold engagement rings, sourced and verified", 
                  "Independent, source-linked research on gold engagement rings: karat, solid-gold wording, hallmark, weight, price, returns and flagged gaps.",
                  "overview", body)
