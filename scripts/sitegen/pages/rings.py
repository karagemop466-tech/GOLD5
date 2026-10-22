"""Ring listing pages: the full table and the category subpages."""
from __future__ import annotations

from ..base import badge, esc, layout, load, usd
from ..tables import ring_table, spot

CATEGORY_GROUPS = {
    "solitaire-setting": ["solitaire-setting"],
    "halo-pave-setting": ["halo-pave-setting"],
    "18k-gold": ["18k-gold"],
    "complete-ring": ["complete-ring", "solid-gold-band"],
}

CATEGORY_META = {
    "solitaire-setting": (
        "Solitaire settings",
        "Single-stone settings, sold without the centre stone",
        "A solitaire holds one centre stone in prongs. Every entry here is a setting-only price, so the diamond is extra — "
        "compare these against each other, never against a complete ring.",
        "solitaire",
    ),
    "halo-pave-setting": (
        "Halo &amp; pavé settings",
        "Settings with diamond accents on the head or band",
        "Halo and pavé settings add small diamonds, which raise the price without adding gold. The carat totals shown are for "
        "the accent stones only and are stated by the retailer for a 1 ct. centre stone.",
        "halo",
    ),
    "18k-gold": (
        "18K gold",
        "75% fine gold — the highest karat in this shortlist",
        "18K gold is 18/24 = 75% fine gold, versus 58.3% for 14K. That is a real metal-content difference, and it is the only "
        "karat in this shortlist above 14K that a mainstream retailer publishes a price for.",
        "18k",
    ),
    "complete-ring": (
        "Complete rings",
        "Rings sold with their stones, ready to wear",
        "These rows are complete rings rather than settings, so the listed price includes the stone. That makes them the only "
        "rows where price can be compared with the metal content on a like-for-like basis.",
        "complete",
    ),
}


def summary_strip(entries: list[dict]) -> str:
    priced = [e["price_usd"] for e in entries if e.get("price_usd") is not None]
    weighed = [e for e in entries if e.get("weight_g") is not None]
    explicit = [e for e in entries if e["solid_gold"] == "explicit"]
    karats = sorted({e["karat"] for e in entries if e.get("karat")})
    flags = sorted({f for e in entries for f in e.get("flags", [])})
    price_text = f"{usd(min(priced))} – {usd(max(priced))}" if priced else "unverified"
    tiles = [
        (str(len(entries)), "entries"),
        (price_text, "captured price range" if priced else "no verified price"),
        (" / ".join(f"{k}K" for k in karats) or "—", "karats"),
        (f"{len(explicit)}/{len(entries)}", "say “solid gold”"),
        (f"{len(weighed)}/{len(entries)}", "publish a gram weight"),
        (str(len(flags)), "distinct flags raised"),
    ]
    return '<div class="stat-grid small">' + "".join(
        f'<div class="stat"><div class="stat-value">{esc(v)}</div><div class="stat-label">{esc(l)}</div></div>'
        for v, l in tiles
    ) + "</div>"


def all_rings_page() -> str:
    entries = load("entries.json")["entries"]
    ref = spot()
    body = f"""
<section class="page-head">
  <p class="eyebrow">All entries</p>
  <h1>Every gold ring entry, one table</h1>
  <p class="lede">{len(entries)} rings from five retailers. Each row links to the official product page and stores the exact
  quoted text behind every value. Filter, sort, and expand a row's evidence before you trust a number.</p>
</section>

{summary_strip(entries)}

<section>
  {ring_table(entries, '../')}
</section>

<section class="panel">
  <h3>How to read this table</h3>
  <ul class="steps">
    <li><strong>Karat</strong> is copied from the listing's metal field. It is the seller's claim, not a test result.</li>
    <li><strong>“Solid gold” wording</strong> is “Explicit” only when the page uses the phrase. A karat alone does not exclude plating or vermeil.</li>
    <li><strong>Weight</strong> is only shown if the seller published grams. None did, so every weight cell is blank and flagged (F-004).</li>
    <li><strong>Fine-gold value at spot</strong> is grams × karat/24 × {usd(ref['usd_per_troy_oz'], 2)}/oz ÷ 31.1034768. It is melt value, not resale value, and it needs a weight — so it is empty here.</li>
    <li><strong>Flags</strong> link to the <a href="../pages/flagged.html">Flagged for review</a> page with the source and the recommended action.</li>
  </ul>
</section>
"""
    return layout(
        "../",
        "All gold ring entries — GOLD5",
        "Full table of sourced gold engagement ring entries with karat, solid-gold wording, hallmark, weight, price and flags.",
        "all",
        body,
    )


def category_page(key: str) -> str:
    all_entries = load("entries.json")["entries"]
    wanted = CATEGORY_GROUPS[key]
    entries = [e for e in all_entries if e["category"] in wanted]
    title, subtitle, blurb, active = CATEGORY_META[key]
    body = f"""
<section class="page-head">
  <p class="eyebrow">Category</p>
  <h1>{title}</h1>
  <p class="lede">{esc(subtitle)}. {esc(blurb)}</p>
</section>

{summary_strip(entries)}

<section>
  {ring_table(entries, '../', table_id='rings-' + key)}
</section>

<section class="panel">
  <h3>Before you buy from this category</h3>
  <ul class="steps">
    <li>Ask for the exact gram weight for the size you are ordering — the metal content drives the value, and no listing here published it.</li>
    <li>Request a photo of the inside of the band showing the karat stamp and the maker's mark (F-005).</li>
    <li>Confirm in writing that the metal is solid, not plated or vermeil (F-006).</li>
    <li>Check the return exclusions for resized and personalised items on the <a href="sellers.html">Sellers</a> page before you let anyone size it.</li>
  </ul>
</section>
"""
    return layout(
        "../",
        f"{title.replace('&amp;', 'and')} — GOLD5",
        f"{subtitle}: sourced entries with price, karat, solid-gold wording and flags.",
        active,
        body,
    )
