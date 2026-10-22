"""Seller due-diligence page."""
from __future__ import annotations

from ..base import badge, esc, ext, layout, load

STATUS = {
    "verified": ("verified", "ok"),
    "verified-with-warning": ("verified, with a warning", "warn"),
    "partial": ("partly verified", "warn"),
    "unverified": ("unverified", "bad"),
    "lookup-not-evaluated": ("link only", "muted"),
    "not-stated-on-listings": ("not stated", "warn"),
    "explicit-on-listings": ("explicit on listings", "ok"),
}


def st(key: str) -> str:
    label, kind = STATUS.get(key, (key, "muted"))
    return badge(label, kind)


def seller_cards() -> str:
    sellers = load("sellers.json")["sellers"]
    out = []
    for s in sellers:
        c, r, p = s["contact"], s["returns"], s["payment"]
        contact_bits = []
        if c.get("phone"):
            contact_bits.append(f'<span class="mono">{esc(c["phone"])}</span>')
        if c.get("email"):
            contact_bits.append(ext("mailto:" + c["email"], esc(c["email"]), "mono"))
        contact_bits.append(ext(c["contact_page"], "contact page"))
        out.append(f"""
    <article class="panel seller-card" id="{esc(s['id'])}">
      <header class="seller-head">
        <h3>{ext(s['site'], esc(s['name']))}</h3>
        <div class="badges">{st(c['status'])} {st(r['status'])}</div>
      </header>
      <dl class="kv">
        <dt>Contact</dt><dd>{' · '.join(contact_bits)}</dd>
        <dt>Return window</dt><dd><strong>{esc(r['window'])}</strong> {ext(r['url'], 'policy page')}</dd>
        <dt>Return exclusions</dt><dd>{esc(r['exclusions_evidence'])}</dd>
        <dt>Extra terms</dt><dd>{esc(r['extra_terms_evidence'])}</dd>
        <dt>Resizing</dt><dd>{esc(r.get('resizing_evidence') or 'not captured on the policy page')}</dd>
        <dt>Payment</dt><dd>{st(p['status'])} {esc(p['summary'])}</dd>
        <dt>Solid-gold wording</dt><dd>{esc(s['solid_gold_policy']['note'])}</dd>
        <dt>Independent complaints</dt><dd>{ext(s['reputation']['bbb_search'], 'Search this seller on BBB')} — no rating or complaint count is republished here.</dd>
      </dl>
      <details class="evidence"><summary>Quoted evidence</summary>
        <ul class="quotes">
          <li><span class="q-field">contact</span><q>{esc(c['evidence'])}</q></li>
          <li><span class="q-field">returns</span><q>{esc(r['evidence'])}</q></li>
          <li><span class="q-field">payment</span><q>{esc(p['evidence'])}</q></li>
        </ul>
        <p class="fine">Sources: {ext(c['source'], 'contact capture')} · {ext(r['url'], 'returns policy')} · {ext(p['source'], 'payment capture')}.
        Capture method: {esc(c['capture_method']).replace('_', ' ')}.</p>
      </details>
    </article>""")
    return "".join(out)


def comparison_matrix() -> str:
    sellers = load("sellers.json")["sellers"]
    rows = []
    for s in sellers:
        rows.append(
            f'<tr><td>{ext(s["site"], esc(s["name"]))}</td>'
            f'<td>{badge("yes", "ok") if s["contact"]["status"] == "verified" else badge("incomplete", "warn")}</td>'
            f'<td>{esc(s["returns"]["window"])}</td>'
            f'<td>{badge("yes", "ok") if "resized" in s["returns"]["exclusions_evidence"] or "altered" in s["returns"]["exclusions_evidence"] else badge("not captured", "warn")}</td>'
            f'<td>{st(s["payment"]["status"])}</td>'
            f'<td>{st(s["solid_gold_policy"]["status"])}</td></tr>'
        )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>Seller</th><th>Contact verified</th><th>Return window</th><th>Resized/altered → no return</th><th>Payment methods</th><th>“Solid gold” on listings</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>"""


def sellers_page() -> str:
    body = f"""
<section class="page-head">
  <p class="eyebrow">Sellers</p>
  <h1>Seller due diligence</h1>
  <p class="lede">Contact details, return terms and payment evidence for the five retailers in this shortlist, copied from their own
  policy pages. Where a detail could not be confirmed it says so instead of guessing.</p>
</section>

<section>
  <h2>Side-by-side</h2>
  {comparison_matrix()}
</section>

<section>
  <h2>Seller records</h2>
  {seller_cards()}
</section>

<section class="panel panel-warn">
  <h3>What every one of these policies has in common</h3>
  <p>Each retailer excludes <strong>resized or altered</strong> rings, and most exclude <strong>engraved or personalised</strong>
  items, from returns. That directly changes your order of operations:</p>
  <ol class="steps">
    <li>Order the correct size the first time, and do not accept a free resize before inspecting.</li>
    <li>Inspect the stamp, weight and purity with an independent jeweler <em>while the ring is still returnable</em>.</li>
    <li>Keep the grading report — Blue Nile charges $150 to replace a missing diamond report.</li>
    <li>Pay by credit card so a misdescribed item can be disputed.</li>
  </ol>
</section>

<section>
  <h2>About independent reviews</h2>
  <p>This project links each seller's BBB search page rather than republishing star ratings. Ratings and complaint counts change
  daily, are not primary evidence about a specific ring, and copying one would violate the no-hallucination rule as of a later
  reading. Open the links yourself and check the number of closed complaints, not just the letter grade.</p>
</section>
"""
    return layout(
        "../",
        "Seller due diligence — GOLD5",
        "Contact details, return windows, exclusions and payment evidence for Blue Nile, Brilliant Earth, Mejuri, Ross-Simons and Costco.",
        "sellers",
        body,
    )
