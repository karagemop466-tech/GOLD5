"""Method page: the verification protocol and the pass log."""
from __future__ import annotations

import json
from pathlib import Path

from ..base import esc, ext, layout, load

ROOT = Path(__file__).resolve().parents[3]


PASSES = [
    ("quote", "Every recorded value is a literal substring of the quote captured from the page.", "A remembered or invented price cannot survive this pass."),
    ("arith", "Every derived figure recomputes from its inputs and the recorded spot observation.", "Catches arithmetic drift and any price below its own melt value."),
    ("coverage", "Every blank or unstated field is tied to a flag on that row.", "Stops a blank from being quietly filled later."),
    ("money", "Every $ amount rendered in the HTML traces to data or to a printed formula.", "Catches a stray price that exists only in the page template."),
    ("flags", "Flag ids resolve and point at real data rows.", "No orphan or dangling findings."),
    ("links", "Internal links and anchors resolve; external URLs are https and well formed.", "No dead navigation; optional live fetch runs in CI."),
    ("checklist", "A checklist item is marked covered only when coverage is complete.", "The scorecard cannot overstate what the web proves."),
    ("build", "Committed HTML is byte-identical to a fresh build from data/.", "The published site cannot diverge from the verified data."),
]


def pass_log() -> str:
    rows = "".join(
        f'<tr><td><span class="mono">{esc(name)}</span></td><td>{esc(what)}</td><td class="cell-note">{esc(why)}</td></tr>'
        for name, what, why in PASSES
    )
    return f"""
    <div class="table-wrap">
      <table class="data-table compact">
        <thead><tr><th>Pass</th><th>What it proves</th><th>Why it matters</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="fine">The result of the most recent run is published as machine-readable JSON and as a Markdown summary in the repository's
    <span class="mono">reports/</span> directory, and the same eight passes run in CI on every push. The pass table above is fixed
    text on purpose, so that the page cannot disagree with a build.</p>"""


def method_page() -> str:
    meta = load("meta.json")
    entries = load("entries.json")["entries"]
    flags = load("flags.json")["flags"]
    body = f"""
<section class="page-head">
  <p class="eyebrow">Method</p>
  <h1>How every line was verified</h1>
  <p class="lede">This site is the output of a repeatable process, not a set of opinions. Here is exactly what “verified” means
  in this project, what it does not mean, and how to re-run the checks yourself.</p>
</section>

<section class="rule-card">
  <h2>The no-hallucination rule, restated</h2>
  <p>{esc(meta['no_hallucination_rule'])}</p>
</section>

<section>
  <h2>Protocol</h2>
  <ol class="steps wide">
    <li><strong>Capture, don't recall.</strong> Each product page is fetched on the verification date; the price, metal, width, stock
      number and stone data are copied as display strings, together with the surrounding text as a quote.</li>
    <li><strong>One quote per field.</strong> A value is stored only if that value is a literal substring of the quoted evidence.
      The verifier enforces this mechanically — a remembered price cannot pass.</li>
    <li><strong>Policies are quoted, not summarised.</strong> Return windows and exclusions come from the retailer's own policy page,
      including the sentence about resized and personalised items.</li>
    <li><strong>Contact details are text on the seller's site.</strong> Phone numbers and emails are copied from the page; if a page
      does not show one, the field is empty and a flag is raised (F-011).</li>
    <li><strong>Nothing is inferred.</strong> No weight, hallmark or “solid gold” claim is derived from karat, brand name or price.</li>
    <li><strong>Arithmetic is explicit.</strong> Derived values print their formula and the exact spot observation they used.</li>
    <li><strong>Blanks are findings.</strong> A missing value becomes a row in the Flagged register with the action needed.</li>
  </ol>
</section>

<section>
  <h2>Pass log — this review</h2>
  <p>Eight automated passes run after every review and on every push.</p>
  {pass_log()}
</section>

<section>
  <h2>What “verified” does and does not mean</h2>
  <div class="two-col">
    <div class="panel">
      <h3>It does mean</h3>
      <ul class="steps">
        <li>The value was published on that official page on {esc(meta['verified_on_display'])}.</li>
        <li>The exact sentence is stored and shown on the row.</li>
        <li>You can re-open the link and check it yourself.</li>
      </ul>
    </div>
    <div class="panel panel-warn">
      <h3>It does not mean</h3>
      <ul class="steps">
        <li>That the ring is authentic — that needs a physical test (XRF) by an independent jeweler.</li>
        <li>That the price is current — re-check it on the live page.</li>
        <li>That the seller's marketing claim about purity is true.</li>
        <li>That a karat stamp proves the alloy; a stamp can be counterfeit.</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <h2>Scope and limits of this pass</h2>
  <ul class="steps">
    <li>{len(entries)} entries from five retailers were captured. This is a research shortlist, not the market.</li>
    <li>{len(flags)} flagged items. The structural gap is the missing hallmark or maker's mark (F-005) on every row; gram weights are
      published for only two rows (F-004).</li>
    <li>Search snippets and cached prices were rejected as evidence wherever a live page could be read instead (F-002, F-003,
      F-013, F-016). Where a snippet is the only captured text, the capture method says so on the row.</li>
    <li>All pages are static HTML generated from <span class="mono">data/*.json</span>. Rebuilding without changing the data must
      produce byte-identical files, which the CI checks.</li>
  </ul>
</section>

<section>
  <h2>Reproduce it</h2>
  <pre class="code"><code>python3 scripts/build_site.py      # regenerate the site from data/
python3 scripts/build_site.py --check   # fail if the committed HTML is stale
python3 scripts/verify.py         # quote, arithmetic, coverage and link passes
python3 scripts/verify.py --links # also re-fetch every URL and report HTTP status</code></pre>
  <p class="fine">Latest machine-readable report: {ext('https://github.com/karagemop466-tech/GOLD5/blob/main/reports/verification.json', 'reports/verification.json')} ·
  human summary: {ext('https://github.com/karagemop466-tech/GOLD5/blob/main/reports/verification.md', 'reports/verification.md')}.</p>
</section>
"""
    return layout(
        "../",
        "Method and verification passes — GOLD5",
        "The no-hallucination protocol, the automated verification passes and the limits of what “verified” means on this site.",
        "method",
        body,
    )
