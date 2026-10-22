# GOLD5 — Gold engagement ring research

**Live site:** https://karagemop466-tech.github.io/GOLD5/
**Flagged for review:** https://karagemop466-tech.github.io/GOLD5/pages/flagged.html
**Verified:** 22 October 2026 (UTC) · **Session:** `arena-84be683f`

A source-linked shortlist of gold engagement rings from five retailers, built to a strict rule:

> **No hallucination rule — no price, weight, karat, hallmark, policy or contact detail appears on the site unless it was read
> from an official page and quoted verbatim.** If a seller did not publish a value, the cell stays blank and the row is flagged
> as unverified. Nothing is inferred, remembered, or carried over from a search snippet.

Every row links to the official product page, stores the exact quoted text behind each value, and carries a flag for anything the
checklist requires that the listing does not publish.

---

## What is here

| Path | Contents |
|---|---|
| `index.html` | Landing dashboard: rule, scorecard, spot references, analysis, top findings |
| `pages/all-rings.html` | Every entry in one filterable, sortable table |
| `pages/solitaires.html`, `halo-pave.html`, `18k.html`, `complete-rings.html`, `gold-bands.html` | Category subpages |
| `pages/sellers.html` | Contact details, return windows, exclusions, payment evidence per seller |
| `pages/prices.html` | Captured spot quotes, raw-gold tables by weight/karat, calculator, price-vs-melt analysis |
| `pages/method.html` | The verification protocol and the seven automated passes |
| `pages/flagged.html` | Every irregularity and every unverified field, with its source and next action |
| `data/*.json` | The single source of truth for all rendered content |
| `scripts/build_site.py`, `scripts/sitegen/` | Deterministic static-site generator |
| `scripts/verify.py` | Anti-hallucination harness (quote, arithmetic, coverage, money, flags, links, checklist, build) |
| `reports/` | Latest machine-readable and human-readable verification report |

## Data model

`data/entries.json` — one object per ring:

```json
{
  "id": "RS-960952",
  "seller": "Ross-Simons",
  "url": "https://www.ross-simons.com/products/960952",
  "checked_on": "2026-10-22",
  "karat": 14,
  "solid_gold": "not-stated",
  "hallmark": "not-stated",
  "weight_g": 1.3,
  "price_usd": 399.0,
  "stock_number": "960952",
  "evidence": [{ "field": "weight_g", "quote": "Gold Weight 1.3 grams" }],
  "flags": ["F-005", "F-006"]
}
```

A value is legitimate only if it is a literal substring of its `quote`. `scripts/verify.py` enforces that mechanically, so a
remembered or invented number cannot reach the site.

## Run it

```bash
python3 scripts/build_site.py         # regenerate HTML from data/
python3 scripts/build_site.py --check # fail if committed HTML is stale
python3 scripts/verify.py             # run all eight passes
python3 scripts/verify.py --links     # also re-fetch every external URL
```

No dependencies beyond Python 3.11. The site is static HTML, CSS and a small amount of vanilla JS.

## What the data shows

- **12 entries, 5 sellers, 17 flags.** Prices captured on 2026-10-22; gold spot reference $4,028.10/oz
  ([Gold-API](https://api.gold-api.com/price/XAU)), cross-checked against
  [APMEX](https://www.apmex.com/gold-price) and the [World Gold Council](https://www.gold.org/goldhub/data/gold-prices).
- **Only 2 of 12 listings publish a gram weight** (both Ross-Simons plain gold rings). So the checklist's price-versus-gold test
  can only be run on those two: the 1.3 g dome ring at $399 is **4.06×** its metal value, the 1.7 g filigree ring at $499 is
  **3.89×**. Both are normal retail multiples; neither is suspiciously cheap.
- **0 of 12 listings state a hallmark or maker's mark**, and only the two Mejuri rows say "solid gold" explicitly. Karat alone
  does not exclude plating, vermeil or filled metal.
- **Same setting, two alloys:** Brilliant Earth's Fleur solitaire is $1,350 in 14K and $1,550 in 18K — $200 (14.8%) for the
  extra fine gold, with no weight published to check it against.
- **Costco is the one critical flag:** its official return policy says "Precious metals are non-refundable" while its jewelry FAQ
  says jewelry can be returned. Until that is resolved in writing, it fails the checklist's return-policy requirement.

## Sources

Retailer product and policy pages are linked inline on every row and in `data/sellers.json`. The spot-price observation, its
timestamp and its URL are stored in `data/gold-prices.json`. Independent complaints are not republished as ratings; each seller
links to its BBB search page for manual review.

## Limits

This is research, not an appraisal, not financial advice, and not a guarantee of authenticity. Prices change without notice.
A karat stamp does not prove an alloy, which is why the recommended final step is an independent jeweler's weight check and
XRF test before the ring is worn or resized.

## Coordination

Parallel sessions coordinate through [COORDINATION.md](COORDINATION.md). Session `arena-84be683f` created the board on
2026-10-22, claimed every task, and is also the integration session (no other session, branch, PR or issue existed).
