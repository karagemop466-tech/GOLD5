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


## Merge note — `main` integration (2026-10-22)

`main` advanced past this branch's base while this pass was running (PRs #9–#14 added four more sites
and a 24-row root dashboard). The merge was resolved as a **union**: this session's 25-row build is the
root dashboard, and `93032b31`'s 24-row dashboard is preserved byte-for-byte at
`archive/session-93032b31/` with its CSS, data and working links. `verified/`, `report/`,
`verification/`, `guide/`, `docs/`, `pages/` and `index-37e8ff42.html` are untouched and still live.
See `COORDINATION.md` for the full conflict and resolution record.

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
| `93032b31` | 24-row pass-2 dashboard (superseded by this consolidation, preserved verbatim) | `archive/session-93032b31/` |
| `84be683f` | Generated 11-page site + its own builder/checker and CI | `verified/` |
| `60c4b9c3` | Report site, evidence and security tests | `report/`, `verification/` |
| `090bae73` | Checklist guide (14 pages) | `guide/`, `index-090bae73.html`, `pages/` |

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

---

<details>
<summary><b>Appendix — previous README (session <code>93032b31</code>, preserved verbatim)</b></summary>

# GOLD5 — gold engagement ring research

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

**Live site (GitHub Pages):** https://karagemop466-tech.github.io/GOLD5/
— landing dashboard + 8 subpages (All listings · By karat · Gold value & calculator · Sellers ·
Checklist · Flagged for review · Sources · Method).

## ◆ NO HALLUCINATIONS — the rule of this project

> Every price, weight, karat, hallmark claim and policy on the site was read from the **seller's own
> page** (or an official regulator) on the date shown, and the exact text that was on the page is
> stored in [`verification/evidence/`](./verification/evidence). A value that could not be confirmed
> is **blank and flagged** on the [Flagged for review page](https://karagemop466-tech.github.io/GOLD5/report/flagged.html).
> Nothing is estimated, inferred, or currency-converted.

The rule is enforced mechanically, not by good intentions:

```bash
python3 tools/check_report.py --record   # 10 check groups, ~1,600 assertions, exit 1 on any failure
python3 tools/security_test.py           # plants 7 fake values; all must be caught
```


`check_report.py` re-finds every recorded value as a literal string inside the saved capture of the
page, recomputes every calculated number, audits every dollar amount rendered in the HTML, checks
link integrity and flag cross-references, and fails the build otherwise. See
[`verification/security_tests.md`](./verification/security_tests.md) for the planted-error results
and the two blind spots it originally had.

## What is here

| Path | What it is |
|---|---|
| `index.html`, `report/**` | **This pass's site** — dashboard, category subpages, calculator, flag page, sources, method. Generated by `tools/build_report.py` from `verification/data.json`. Never edit the HTML by hand; edit the data and rebuild. |
| `verification/data.json` | Single source for the new site: 27 listings, 9 sellers, 7 reference documents, 26 flags, the spot snapshot. Every value carries `tokens` — the literal strings that must exist in its evidence file. |
| `verification/evidence/*.txt` | Verbatim captures with source URL and UTC timestamp, one file per page. |
| `verification/passes.json` | Verification pass log, rendered on the Method page. |
| `tools/build_data.py` | Writes `verification/data.json` (provenance, tokens, derived logic). |
| `tools/build_report.py` | Builds the site. Also preserves the previous root dashboard at `index-37e8ff42.html` on first run. |
| `tools/check_report.py` | The no-hallucination gate. |
| `tools/security_test.py` | Negative tests for the gate. |
| `index-37e8ff42.html`, `site/**` | Previous root dashboard (session 37e8ff42), preserved byte-for-byte. |
| `docs/**` | Session 638c9614's site (11 listings + its own evidence store + `tools/check_hallucinations.py`). |
| `index-090bae73.html`, `pages/**`, `assets/**` | Session 090bae73's checklist guide. |
| `COORDINATION.md` | Shared task board — read this first if another session is working. |

## Data discipline

- **Provenance A** — 12 rows re-read live in this pass (2026-10-22 23:26 → 2026-10-23 00:07 UTC).
- **Provenance B** — 15 rows captured earlier the same UTC day by another session; the verbatim
  quote is in this repo and the row is labelled B because it was not re-opened in this pass.
- **Price text** is stored exactly as the seller rendered it (e.g. `Special Price$3,020.00`), so you
  can match the table against the page.
- **Derived numbers** are always `weight × karat ÷ 24` for fine gold and `fine gold × spot/gram` for
  metal value, at the verified Kitco snapshot of **$129.47/g** (2026-10-22 19:26 NY), with the
  formula printed next to the table and a calculator on the Gold value page.
- **Gold spot disagrees with itself**: Kitco's page showed 4,026.90 / 4,027.50 / 4,028.21 per ounce in
  one capture. The lowest per-gram figure is used so computed metal values are conservative.

## Refreshing

1. Re-open the source link. Copy the new verbatim text into `verification/evidence/<page>.txt`
   (URL + UTC timestamp), update `tokens` and values in `tools/build_data.py`.
2. `python3 tools/build_data.py && python3 tools/build_report.py`
3. `python3 tools/check_report.py --record` → fix any FAIL, rebuild, re-run.
4. Log the pass and any irregularity in `COORDINATION.md`.

The older deliverables have their own checkers (`python3 scripts/verify.py`,
`python3 tools/check_hallucinations.py`) — run the one matching the data you touched.
### Parallel delivery preserved from session `84be683f`

| Path | What it is |
|---|---|
| `verified/index.html`, `verified/pages/*.html`, `verified/assets/*` | That session's own site (dashboard, all-rings, 18k, complete-rings, prices, sellers, flagged, method, checklist) |
| `verified/data/*.json` | Its table data (entries, sellers, flags, gold prices, checklist, meta) |
| `verified/scripts/verify.py` | Its own hallucination + link + arithmetic checker — run it for `verified/` data |
| `site/assets/data.js` | Single-source data for the earlier root dashboard (now archived as `index-37e8ff42.html`) |
| `.github/workflows/ci.yml` | CI added by that session |

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

Nothing in `verified/` was edited by this pass; it is served at `/verified/`.



</details>
