# GOLD5 — Solid Gold Engagement Ring Research

A research repo and static dashboard for buying a **gold engagement ring** that can actually be
verified: karat, an explicit "solid gold" statement (not plated / vermeil / filled / overlay / tone),
a hallmark with a **maker's mark** next to the karat stamp, weight in grams, a real seller with real
contact details, a price compared with the gold it contains, a written return policy that covers
resizing, credit-card payment, and an independent jeweller / XRF check on arrival.

**Live site:** <https://karagemop466-tech.github.io/GOLD5/> (root, GitHub Pages from `main`)

The core finding is the thesis: **a 14K or 18K stamp does not prove purity, and in this dataset no
listing is documented well enough to buy without asking the seller for more.** 0 of 25 rows state a
maker's mark; 17 publish no weight; 16 never say "solid gold". The dashboard leads with that.

## ◆ NO HALLUCINATIONS RULE

No price, weight, karat, hallmark, policy or date is recorded without a link to the **official source
page** and a check date. Anything not confirmable is **blank and flagged** on
[Flagged for Review](https://karagemop466-tech.github.io/GOLD5/site/flagged.html) — never guessed,
estimated, or copied from a search snippet. Derived values are arithmetic on verified inputs
(fine gold = grams × karat fineness; metal value = fine gold × spot at a timestamped quote).

Every review pass ends with the checkers:

```bash
python3 scripts/verify.py             # 15 checks over data + the generated 10-page site
python3 tools/check_hallucinations.py  # 166 checks over the archived docs/ dataset
```

`scripts/verify.py` fails on: a listing without an https source link, a blank cell without its flag,
arithmetic that does not recompute, a missing/broken internal link or anchor, an unregistered external
link, a dollar figure that is not dataset-sourced or computed, a `data.js`/`data.json` mismatch, a
template placeholder, malformed HTML, a missing no-hallucinations banner, or a security regression
(http:// link, `_blank` without `rel=noopener`, frame, third-party script, posting form).

## What the site contains

| Page | Contents |
|---|---|
| `index.html` | Dashboard: spot price with timestamp, bottom-line verdict, 5 stat cards, price/metal findings, purity table, and the best-documented rows |
| `site/listings.html` | All **25 listings** from **13 sellers**, filterable/sortable, with price, karat, grams, fine gold, metal value, price ÷ metal, solid-gold wording, hallmark + maker's mark, return policy, check date, provenance and flags |
| `site/gold-price.html` | Four timestamped same-day quotes, per-purity values (10K–24K), and a raw-gold table by weight |
| `site/calculator.html` | Live gold calculator: grams × karat × spot → fine gold, metal value, price ÷ metal, verdict; presets from the dataset |
| `site/checklist.html` | The 12-point buying checklist, each point tied to an official source and to what the dataset shows |
| `site/sellers.html` | 13 sellers: contact, returns, warranty, payment, reputation, flags |
| `site/analysis.html` | Median markups, the below-metal case, documentation ranking, completeness scorecard, seller concentration |
| `site/flagged.html` | All 25 flags (24 open, 1 resolved), each with detail and links |
| `site/sources.html` | Every source used, with what it was used for and the check date |
| `site/verification.html` | Method, the live fetch log, corrections made, and the latest checker result |

Prices, karats and weights are what the seller displayed on the check date. **Prices change** — re-check
before buying. Spot used for every calculation: Kitco bid **$4,026.90/oz = $129.47/g** at
2026-10-22 7:26 p.m. ET; three earlier same-day quotes ($4,025.00, $4,077.60, $4,083.82) are recorded
for comparison.

## Build pipeline

```
scripts/author_data.py     ->  site/assets/data.json      (single source of truth)
scripts/build_site.py      ->  index.html + site/*.html   (static, stdlib only)
scripts/verify.py          ->  data/check_report_v2.json  (15 checks, exit 1 on failure)
```

```bash
python3 scripts/author_data.py
python3 scripts/build_site.py
python3 scripts/verify.py
```

No frameworks, no external fonts, no third-party JavaScript, no network calls from the site.

## Archived deliverables (preserved, not modified)

| Session | Delivery | Where |
|---|---|---|
| `638c9614` | 11 rings + sellers/spot/flags, evidence transcripts, checker + builder | `data/`, `docs/`, `tools/` |
| `090bae73` | 14-page checklist-format guide | `index-090bae73.html`, `pages/`, `assets/` |
| `37e8ff42` | First root dashboard (14 listings, 8 pages) | `archive/session-37e8ff42/` |
| `7cca80c9` | This consolidation: 25 listings, 13 sellers, 10 pages, 15-check harness | root `index.html`, `site/`, `scripts/` |

All sessions captured data on 2026-10-22 and corroborate the same Kitco spot snapshot. Merges were
resolved as unions — no session's content was discarded. See `COORDINATION.md` for the full board,
claims, handoffs and PR history.

## Refreshing data

1. Re-open each listing and policy page; update `scripts/author_data.py` with the new value, the exact
   quote, the URL and the check date. Never overwrite a value with an estimate.
2. `python3 scripts/author_data.py && python3 scripts/build_site.py && python3 scripts/verify.py`.
3. Commit the regenerated `index.html`, `site/*.html`, `site/assets/data.json`, `site/assets/data.js`,
   `data/check_report_v2.json` and the report in `docs/verification/`.
4. Log the pass in `COORDINATION.md` (what changed, what failed, which flags opened or resolved).
