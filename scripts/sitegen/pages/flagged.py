"""Flagged-for-review page: every irregularity with its source and next action."""
from __future__ import annotations

from collections import Counter

from ..base import badge, esc, ext, layout, load, short_host

SEV_ORDER = {"critical": 0, "warning": 1, "info": 2}


def summary() -> str:
    flags = load("flags.json")["flags"]
    counts = Counter(f["severity"] for f in flags)
    tiles = [
        (str(len(flags)), "items flagged"),
        (str(counts.get("critical", 0)), "critical"),
        (str(counts.get("warning", 0)), "warnings"),
        (str(counts.get("info", 0)), "informational"),
    ]
    return '<div class="stat-grid small">' + "".join(
        f'<div class="stat"><div class="stat-value">{v}</div><div class="stat-label">{esc(l)}</div></div>'
        for v, l in tiles
    ) + "</div>"


def flag_rows() -> str:
    flags = sorted(load("flags.json")["flags"], key=lambda f: (SEV_ORDER[f["severity"]], f["id"]))
    rows = []
    for f in flags:
        affects = ", ".join(f["affects"])
        rows.append(f"""
      <tr id="{esc(f['id'])}">
        <td class="cell-id">{esc(f['id'])}</td>
        <td>{badge(f['severity'].title(), {'critical': 'bad', 'warning': 'warn', 'info': 'muted'}[f['severity']])}</td>
        <td><strong>{esc(f['title'])}</strong><div class="cell-note">{esc(f['detail'])}</div></td>
        <td class="cell-note">{esc(affects)}</td>
        <td>{ext(f['source'], esc(short_host(f['source'])))}</td>
        <td class="cell-note">{esc(f['recommendation'])}</td>
      </tr>""")
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>Affects</th><th>Official source</th><th>What to do</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>"""


def unverified_table() -> str:
    entries = load("entries.json")["entries"]
    rows = []
    for e in entries:
        missing = []
        if e.get("weight_g") is None:
            missing.append("weight (g)")
        if e.get("price_usd") is None:
            missing.append("price")
        if e.get("hallmark") in (None, "", "not-stated"):
            missing.append("hallmark / maker's mark")
        if e["solid_gold"] != "explicit":
            missing.append("“solid gold” wording")
        if not e.get("stock_number"):
            missing.append("stock / style number")
        cell = ", ".join(missing) if missing else "—"
        rows.append(
            f'<tr><td class="cell-id"><a href="../pages/all-rings.html#{esc(e["id"])}">{esc(e["id"])}</a></td>'
            f'<td>{esc(e["seller"])}</td><td>{esc(e["title"])}</td>'
            f'<td class="cell-note">{esc(cell)}</td>'
            f'<td>{ext(e["url"], "official page")}</td></tr>'
        )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>ID</th><th>Seller</th><th>Ring</th><th>Not published by the seller</th><th>Source</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    <p class="fine">These are left blank on purpose. Filling them from a search snippet, an old cached page or an assumption would
    break the no-hallucination rule. Each one is a question to put to the seller in writing.</p>"""


def flagged_page() -> str:
    body = f"""
<section class="page-head">
  <p class="eyebrow">Flagged for review</p>
  <h1>Irregularities, gaps and contradictions</h1>
  <p class="lede">Every item below is a place where the evidence is missing, contradictory or simply notable. None of these
  block publication — they are the exact list of things to resolve before money changes hands.</p>
</section>

{summary()}

<section>
  <h2>Flag register</h2>
  {flag_rows()}
</section>

<section>
  <h2>Unverified fields, row by row</h2>
  {unverified_table()}
</section>

<section class="panel">
  <h3>How these were found</h3>
  <p>Three automated passes run over the data on every build — see <a href="method.html">Method</a> and
  <span class="mono">reports/</span> in the repository:</p>
  <ol class="steps">
    <li><strong>Quote-substring pass:</strong> every recorded value must literally appear inside the quoted evidence captured from the page.</li>
    <li><strong>Arithmetic pass:</strong> recomputes each derived number from its inputs and the recorded spot observation.</li>
    <li><strong>Coverage pass:</strong> lists every field a row is missing, so blanks can never quietly become guesses.</li>
  </ol>
  <p class="fine">Items marked “info” are recorded for completeness. “Warning” items need a written answer from the seller or a
  second source. <strong>“Critical”</strong> items are reserved for anything that could leave you unable to return the ring or that
  contradicts a seller's own published terms — there is one, and it is the reason Costco is not recommended for this purchase
  until it is answered in writing.</p>
</section>
"""
    return layout(
        "../",
        "Flagged for review — GOLD5",
        "Unverified values, contradictions and irregularities found while verifying gold engagement ring listings, each with its official source.",
        "flagged",
        body,
    )
