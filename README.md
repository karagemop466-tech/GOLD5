# GOLD5 — Solid Gold Engagement Ring Research

A research dashboard for **finding gold engagement rings that can actually be verified**: solid gold (not plated,
filled or vermeil), a stated karat, a hallmark **and** a maker's mark, a published weight in grams, a real seller, a price
that makes sense against the gold market, a usable return window, and a path to independent XRF testing on delivery.

**Live site:** https://karagemop466-tech.github.io/GOLD5/

## ⚠ NO HALLUCINATIONS — the rule this project runs on

> Every price, weight, karat and policy on the site was read from the **official page linked next to it**, on the check
> date shown. If a value could not be confirmed from an official source it is **left blank** and published on the
> **Flagged for review** page — never guessed, estimated or inferred. Derived numbers (pure-gold grams, metal value,
> price-to-metal ratio) are computed by script from raw values and **recomputed independently by the security check**.

This statement sits at the top of every page. The check that enforces it is re-runnable by anyone:

```bash
python3 scripts/verify.py          # dashboard: provenance, arithmetic, money traceability, links, negative tests
python3 tools/check_hallucinations.py   # preserved docs/ archive: every value must appear verbatim in its evidence file
```

`scripts/verify.py` fails the build if a value has no source, if a blank cell is not flagged, if a derived number does not
recompute, if a dollar amount in the HTML cannot be traced to the dataset, or if a local link is broken. It also runs
**negative tests**: fabricated prices, fabricated weights and hand-typed dollar figures are injected on purpose and must
all be caught (currently 6/6). **Run it after every review** and log the result in `COORDINATION.md`.

## What the site contains

| Page | What it is |
|---|---|
| `index.html` | Landing dashboard: the no-hallucination statement, the dated gold spot, headline counts, the best-documented candidates, and the category cards |
| `listings.html` | **All 24 rows** in one filterable table: price, karat, weight, solid-gold claim, hallmark, return policy, width, verification state, flags and the official source link |
| `sellers.html` | 14 seller profiles: contact details, return policy, warranty, payment, reputation links, and what is missing |
| `gold-price.html` | The dated spot snapshot, same-day cross-checks, and the per-karat value table with fineness and stamps |
| `calculator.html` | Weight × karat × spot → pure gold grams, troy ounces, metal value and price-to-metal ratio; loads any verified listing |
| `checklist.html` | The 12-point buying checklist, each point tied to an official source and to what the data shows |
| `analysis.html` | Findings: the hallmark gap, withheld weights, the below-melt case study, setting-vs-complete pricing, return windows |
| `verification.html` | The audit trail: what pass 2 re-fetched, what matched, what could not be read, and the checker output |
| `flagged.html` | **Flagged for review** — 19 findings plus every blank cell and the reason it is blank |
| `sources.html` | The full source registry: every URL, what it backs, when it was read |
| `archive.html` | Earlier sessions' sites, preserved unchanged |

## Data

- `tools/data_unified.py` — the authored dataset (24 listings, 14 sellers, 19 flags, 10 official references, 12 checklist points). Every value carries its source URL and verification state (`P2` = re-fetched live in pass 2, `prior` = earlier same-day capture, labelled as such).
- `tools/build_dashboard.py` — generates `data/unified.json`, `site/assets/data.js`, `site/assets/dashboard.css` and all 11 pages. Refuses to build if the data breaks the contract (blank value without a flag, unknown seller, bad karat, duplicate id).
- `data/unified.json` — the machine-readable dataset the checker validates.
- `data/live_check.json` — the pass-2 fetch log (what was requested, what it returned, what did not render).
- `data/check_status.json` — the latest checker run; `docs/verification/pass2-report.md` — its report.

#### Current state (2026-10-22, pass 2)

| Metric | Value |
|---|---|
| Listings | 24 (20 engagement rings, 3 reference bands, 1 case study) |
| Sellers | 14 (6 retailers + Etsy + 7 Etsy shops) |
| Rows with a published gram weight | 8 |
| Rows with a published price | 22 |
| Rows with hallmark **and** maker's-mark proof | 0 — no listing shows it |
| Below-melt listings | 1 (case study, flagged F1) |
| Primary gold spot | $4,026.90/oz · $129.47/g at 19:26 NY, 2026-10-22 (Kitco) |
| Checker | PASS — 0 errors, 0 warnings, 4 cross-check notes, negative tests 6/6 |

Prices and promos move; every row shows its check date. Re-read the listing before buying.

## Archives (nothing from earlier sessions was deleted)

| Path | Origin |
|---|---|
| `docs/` | Session 638c9614 — 11 verified listings, verbatim evidence files, its own dashboard and checker |
| `pages/` + `index-090bae73.html` | Session 090bae73 — 13-page checklist-format guide |
| `guide/` | Session 3c8bb7ee (PR #4) — checklist site + research notes, preserved with its relative links intact |
| `site/listings.html` … | Session 37e8ff42's earlier dashboard pages, kept working against `site/assets/data-legacy.js` with an "archived view" banner |

## Refreshing the data

1. Open each listing and read the price, karat, weight and return window **from the page**.
2. Update `tools/data_unified.py` (value + `verifyState` + source URL). If a page does not render a value, leave it blank and flag it.
3. `python3 tools/build_dashboard.py && python3 scripts/verify.py`
4. `python3 tools/check_hallucinations.py` (archive check)
5. Record the pass, the sources and any irregularities in `COORDINATION.md`, then commit.

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

