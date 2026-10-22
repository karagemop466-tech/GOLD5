# GOLD5 — Solid Gold Engagement Ring Research

Research project to **find gold engagement rings** that meet a strict online-buying checklist
(solid gold, karat, hallmark + maker's mark, weight in grams, seller reputation, price vs. gold
value, return/resize policy, payment protection, documentation, independent XRF test).

Three parallel agent sessions each delivered work for this project. **All of it is preserved**
(union merge — see the merge notes in [COORDINATION.md](./COORDINATION.md)):

| Session | Site (live) | Data | Checker |
|---|---|---|---|
| `37e8ff42` (final integration, PR #5) | **repo root** — https://karagemop466-tech.github.io/GOLD5/ (landing dashboard: Listings, Gold Price, Calculator, Checklist, Sellers, Flagged for Review, Sources) | [site/assets/data.js](./site/assets/data.js) (strict JSON) | `python3 scripts/verify.py` |
| `638c9614` (PR #1/#2) | `docs/` — https://karagemop466-tech.github.io/GOLD5/docs/ (Dashboard, Rings, Calculator, Analysis, Sellers, Checklist, Flagged for Review, Verification, Sources) | [data/rings.json](./data/rings.json), `sellers.json`, `spot.json`, `flags.json` + verbatim `data/evidence/*.txt` | `python3 tools/check_hallucinations.py` |
| `090bae73` (PR #3) | Checklist-format guide — landing preserved at [index-090bae73.html](./index-090bae73.html) + 13 subpages under `pages/` (gold purity, solid gold, hallmark, weight, seller reputation, price, returns, payment, documentation, upon-arrival, XRF, calculator, flagged) | content in-page, cited to official sources | cited per page |

All sessions captured data from official pages on 2026-10-22 and **independently corroborate the
same Kitco spot snapshot** ($4,025.00/oz bid, $129.41/g, 7:10 p.m. EDT).

## ◆ NO HALLUCINATIONS RULE (applies to everything)
No price, weight, karat, hallmark, policy, or claim is recorded without a link to the **official
source page** and a check date. Anything not confirmable from an official source is **left blank
and flagged** on the respective "Flagged for Review" page — never guessed, estimated or inferred.
"Calculated" values are arithmetic on verified inputs (`weight × spot/gram × karat/24`).
**After every review pass run the checker** and record it in COORDINATION.md:
- `python3 scripts/verify.py` (root site + data)
- `python3 tools/check_hallucinations.py --log "what I reviewed"` (docs/ site + data)

## Layout
| Path | What |
|---|---|
| `index.html`, `site/**` | Landing dashboard + subpages of session 37e8ff42 (this integration) |
| `site/assets/data.js` | Single-source data for the root site (strict JSON) |
| `verified/scripts/verify.py` | Hallucination + link + arithmetic pass for the root site/data |
| `docs/verification/*.md` | Per-source verification notes with exact quotes & URLs (session 37e8ff42) |
| `index-090bae73.html`, `pages/*.html`, `assets/` | Checklist-format site of session 090bae73 (preserved) |
| `data/rings.json`, `sellers.json`, `spot.json`, `flags.json` | Table data for the `docs/` site (shared output — edited only by the integration session) |
| `data/evidence/*.txt` | Verbatim excerpts + source URL + capture date for every value (session 638c9614) |
| `tools/check_hallucinations.py` | Security check: every value must appear verbatim in evidence; blanks must be flagged; every `$` on the site must be sourced or registered as calculated; links must resolve |
| `tools/build_site.py` | Generates the static site into `docs/` (standard library only) and runs the check |
| `docs/` | GitHub Pages site of session 638c9614 |
| `COORDINATION.md` | Shared task board for all sessions |

## Refreshing data
1. Re-open each listing, copy the new verbatim text into the session's evidence store
   (`data/evidence/<id>.txt` for the docs/ site; quote+URL entries in `site/assets/data.js` +
   `docs/verification/*.md` for the root site).
2. Run the matching checker → fix any FAIL.
3. For the docs/ site: `python3 tools/build_site.py` → commit `data/` and `docs/`.
4. Update the log in [COORDINATION.md](./COORDINATION.md).

---

## Session `arena-84be683f` — verified-methodology site at `/verified/`

**Live site:** https://karagemop466-tech.github.io/GOLD5/verified/
**Flagged for review:** https://karagemop466-tech.github.io/GOLD5/verified/pages/flagged.html
**Verified:** 22 October 2026 (UTC) · **Session:** `arena-84be683f`
**Scope:** this delivery lives entirely under `verified/` and owns no file outside it (the one exception is the additive link
added to the root dashboard, logged in COORDINATION.md).

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
| `verified/index.html` | Landing dashboard: rule, scorecard, spot references, analysis, top findings |
| `verified/pages/all-rings.html` | Every entry in one filterable, sortable table |
| `verified/pages/solitaires.html`, `halo-pave.html`, `18k.html`, `complete-rings.html`, `gold-bands.html` | Category subpages |
| `verified/pages/sellers.html` | Contact details, return windows, exclusions, payment evidence per seller |
| `verified/pages/prices.html` | Captured spot quotes, raw-gold tables by weight/karat, calculator, price-vs-melt analysis |
| `verified/pages/method.html` | The verification protocol and the seven automated passes |
| `verified/pages/flagged.html` | Every irregularity and every unverified field, with its source and next action |
| `verified/data/*.json` | The single source of truth for all rendered content |
| `verified/scripts/build_site.py`, `verified/scripts/sitegen/` | Deterministic static-site generator |
| `verified/scripts/verify.py` | Anti-hallucination harness (quote, arithmetic, coverage, money, flags, links, checklist, build) |
| `verified/reports/` | Latest machine-readable and human-readable verification report |

## Data model

`verified/data/entries.json` — one object per ring:

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
cd verified
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

Parallel sessions coordinate through [COORDINATION.md](COORDINATION.md). Session `arena-84be683f` claimed its tasks on 2026-10-22 while three earlier sessions were already merged; it therefore
works only inside `verified/` and records its work as a union addition to the shared board.
