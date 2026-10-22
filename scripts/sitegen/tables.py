"""Ring tables, toolbars and evidence blocks."""
from __future__ import annotations

from .base import badge, esc, ext, load, short_host, usd

SORT_KEYS = {
    "price-asc": "p",
    "price-desc": "p",
    "seller": "s",
    "karat": "k",
}


def flag_map() -> dict:
    return {f["id"]: f for f in load("flags.json")["flags"]}


def flag_chips(ids: list[str], prefix: str) -> str:
    lookup = flag_map()
    chips = []
    for fid in ids:
        item = lookup.get(fid)
        if not item:
            continue
        chips.append(
            f'<a class="chip chip-{esc(item["severity"])}" href="{prefix}pages/flagged.html#{esc(fid)}" '
            f'title="{esc(item["title"])}">{esc(fid)}</a>'
        )
    return "".join(chips) if chips else badge("none", "ok")


def spot() -> dict:
    data = load("gold-prices.json")
    ref = next(o for o in data["observations"] if o["id"] == data["reference_id"])
    return ref


def gold_value(entry: dict) -> float | None:
    """Spot value of the ring's fine-gold content. Needs both weight and karat."""
    weight = entry.get("weight_g")
    karat = entry.get("karat")
    if weight is None or not karat:
        return None
    ref = spot()
    per_gram = ref["usd_per_troy_oz"] / load("gold-prices.json")["troy_ounce_grams"]
    return weight * (karat / 24.0) * per_gram


def value_cell(entry: dict) -> str:
    value = gold_value(entry)
    if value is None:
        return (
            badge("needs weight", "warn")
            + '<div class="cell-note">cannot price fine gold without grams — F-004</div>'
        )
    return f'<span class="num">{usd(value, 0)}</span><div class="cell-note">melt value at spot, not resale</div>'


def solid_cell(entry: dict) -> str:
    if entry["solid_gold"] == "explicit":
        quote = next((e["quote"] for e in entry["evidence"] if e["field"] == "solid_gold"), "")
        return badge("Explicit", "ok") + f'<div class="cell-note">“{esc(quote)}”</div>'
    return badge("Not stated", "warn") + '<div class="cell-note">karat only — F-006</div>'


def weight_cell(entry: dict) -> str:
    if entry.get("weight_g") is None:
        return badge("— unverified", "warn") + '<div class="cell-note">no gram weight published</div>'
    return f'<span class="num">{entry["weight_g"]:g} g</span> ' + badge("verified", "ok")


def price_cell(entry: dict) -> str:
    if entry.get("price_usd") is None:
        return badge("— unverified", "warn") + f'<div class="cell-note">{esc(entry["price_basis"])}</div>'
    return (
        f'<span class="amount" data-price="{entry["price_usd"]}">{usd(entry["price_usd"])}</span>'
        f'<div class="cell-note">{esc(entry["price_basis"])}</div>'
    )


def hallmark_cell(entry: dict) -> str:
    if entry.get("hallmark") in (None, "", "not-stated"):
        return badge("Not stated", "warn")
    return esc(entry["hallmark"])


def evidence_details(entry: dict) -> str:
    rows = "".join(
        f'<li><span class="q-field">{esc(e["field"])}</span>'
        f'<q>{esc(e["quote"])}</q></li>'
        for e in entry["evidence"]
    )
    capture = esc(entry["capture_method"]).replace("_", " ")
    return (
        '<details class="evidence"><summary>Evidence &amp; source capture</summary>'
        f'<ul class="quotes">{rows}</ul>'
        f'<p class="fine">Captured {esc(entry["checked_on"])} via {capture} from '
        f'{ext(entry["url"], esc(short_host(entry["url"])))}.</p>'
        '</details>'
    )


def ring_row(entry: dict, prefix: str) -> str:
    search = " ".join(
        [
            entry["id"],
            entry["title"],
            entry["seller"],
            entry["metal"],
            entry["stone"],
            entry["category"],
            " ".join(entry.get("tags", [])),
        ]
    ).lower()
    price = entry.get("price_usd")
    price_attr = "" if price is None else f"{price:.2f}"
    return f"""      <tr class="ring-row" id="{esc(entry['id'])}" data-karat="{esc(entry.get('karat') or '')}" data-solid="{esc(entry['solid_gold'])}"
          data-price="{price_attr}" data-seller="{esc(entry['seller'])}" data-search="{esc(search)}">
        <td class="cell-id"><a href="#{esc(entry['id'])}">{esc(entry['id'])}</a></td>
        <td class="cell-ring">
          <div class="ring-title">{ext(entry['url'], esc(entry['title']))}</div>
          <div class="cell-note">{esc(entry['type'])} · {esc(entry['gold_color'])} gold</div>
          {evidence_details(entry)}
        </td>
        <td>{esc(entry['seller'])}</td>
        <td><span class="num">{esc(entry['karat'])}K</span><div class="cell-note">{esc(entry['metal'])}</div></td>
        <td>{solid_cell(entry)}</td>
        <td>{hallmark_cell(entry)}</td>
        <td>{weight_cell(entry)}</td>
        <td>{price_cell(entry)}</td>
        <td>{value_cell(entry)}</td>
        <td class="cell-flags">{flag_chips(entry.get('flags', []), prefix)}</td>
      </tr>"""


HEADER = """      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Ring &amp; official source</th>
          <th scope="col">Seller</th>
          <th scope="col">Karat</th>
          <th scope="col">“Solid gold” wording</th>
          <th scope="col">Hallmark</th>
          <th scope="col">Weight</th>
          <th scope="col">Price (USD)</th>
          <th scope="col">Fine-gold value at spot</th>
          <th scope="col">Flags</th>
        </tr>
      </thead>"""


def toolbar() -> str:
    return """
    <div class="toolbar" data-tools>
      <label class="tool grow"><span>Search</span>
        <input class="tool-search" type="search" placeholder="Ring, seller, ID, stone…" autocomplete="off"></label>
      <label class="tool"><span>Karat</span>
        <select class="tool-karat"><option value="">All</option><option value="14">14K</option><option value="18">18K</option></select></label>
      <label class="tool"><span>Gold wording</span>
        <select class="tool-solid"><option value="">All</option>
          <option value="explicit">Explicit “solid gold”</option>
          <option value="not-stated">Not stated</option></select></label>
      <label class="tool"><span>Price</span>
        <select class="tool-price"><option value="">All</option>
          <option value="0-1000">Under $1,000</option>
          <option value="1000-2000">$1,000–$2,000</option>
          <option value="2000-3000">$2,000–$3,000</option>
          <option value="3000-9999999">$3,000 and up</option>
          <option value="unverified">Unverified</option></select></label>
      <label class="tool"><span>Sort</span>
        <select class="tool-sort"><option value="">Default</option>
          <option value="price-asc">Price ↑</option><option value="price-desc">Price ↓</option>
          <option value="seller">Seller A–Z</option><option value="karat">Karat ↑</option></select></label>
      <button class="tool-reset" type="button">Reset</button>
    </div>
    <p class="table-status" data-table-status aria-live="polite"></p>"""


def ring_table(entries: list[dict], prefix: str, table_id: str = "rings") -> str:
    rows = "\n".join(ring_row(e, prefix) for e in entries)
    return f"""{toolbar()}
    <div class="table-wrap">
    <table class="data-table" id="{esc(table_id)}">
{HEADER}
      <tbody>
{rows}
      </tbody>
    </table>
    </div>
    <p class="fine">Blank cells and “unverified” badges mean the seller did not publish that value on the captured page.
    They were not estimated. Each row links to the official product page; expand “Evidence &amp; source capture” for the exact quoted text.</p>"""
