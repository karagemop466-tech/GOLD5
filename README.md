# GOLD5 — Solid Gold Engagement Ring Research

A research repo and static dashboard for buying a **gold engagement ring** that can actually be
verified: karat, an explicit "solid gold" statement (not plated / vermeil / filled / overlay / tone),
a hallmark with a **maker's mark** next to the karat stamp, weight in grams, a real seller with real
contact details, a price compared with the gold it contains, a written return policy that covers
resizing, credit-card payment, and an independent jeweller / XRF check on arrival.

**Live site:** <https://karagemop466-tech.github.io/GOLD5/> (GitHub Pages from `main`, path `/`)

## ◆ NO HALLUCINATIONS — the rule this project is built around

**No price, weight, karat, hallmark, policy or date is recorded without a link to the official source
page and the date it was read.** If a value cannot be confirmed it is **left blank and published on
[Flagged for Review](https://karagemop466-tech.github.io/GOLD5/site/flagged.html)** — never guessed,
estimated, averaged, copied from a search snippet, or carried forward as if it were current.

Three mechanisms enforce it:

1. **Provenance on every row.** Each entry carries `checkedOn` and `provenance`.
   `live` = re-fetched and read during a pass on the date shown; `prior` = read on `2026-10-22` and
   **not** re-read since (a `prior` row must be labelled *captured 2026-10-22*, carry an explicit
   "not re-fetched" note, and be itemised in FL-26/27/28 — the checker enforces all three). After pass 4
   on 2026-10-23 **no row is `prior`**: all 25 carry a 2026-10-23 read, and the rows where the value
   changed say so on the row and in the flags (FL-08, FL-26, FL-29).
2. **Arithmetic is computed, never typed.** Fine gold = grams × karat fineness; metal value = fine gold
   × the timestamped Kitco bid. The checker re-derives every figure from the inputs.
3. **After every review pass, run the harnesses.** The pass is not finished until they are green:

```bash
python3 scripts/verify.py              # 21 checks (C1–C20 + N1–N8 negative self-tests)
python3 scripts/audit_b1f2fe3b.py      # 6 cross-site security/anti-hallucination groups
python3 tools/check_report.py          # /report/ + verification/data.json
python3 tools/check_hallucinations.py  # archived /docs/ dataset
cd verified && python3 scripts/verify.py   # session 84be683f suite (896 assertions)
```

## Status — 2026-10-23 pass 4 (session `arena-463d0ea2`)

| | |
|---|---|
| Listings | **25** rows from **13** sellers (21 engagement-ring rows, 3 bands, 1 sold case study); **22** priced, **8** with a published gram weight |
| Re-read live | **25 of 25** rows carry a **2026-10-23** read from the seller's own page — 23 of them in pass 4, the other 2 earlier the same day |
| Carried over | **0** rows still depend on a 2026-10-22 figure; none were silently re-dated |
| Spot used | Kitco bid **$3,996.10/oz = $128.48/g** at **2026-10-23 4:10 p.m. ET** (page body prints $3,995.50 / $128.46 — FL-25). The morning quote ($4,022.50 / $129.33) is kept as dated history |
| Flags | **29** (24 open, 5 resolved — FL-07, FL-24, FL-26, FL-27, FL-28). New: **FL-29** (one listing sold out); FL-26 resolved |
| Official references | **11** (FTC consumer guide, 16 CFR Part 23, 15 U.S.C. § 295 and § 297, NIST, LBMA, Etsy Purchase Protection, JVC, ReportFraud, FTC credit cards) |
| Harness | `scripts/verify.py` **PASS — 21/21, 0 failed, 8/8 negative self-tests**; plus the other 8 harnesses, all PASS |

**What changed in pass 4.**

1. **The spot was re-read in the afternoon and fell $26.40/oz.** Every fine-gold, metal-value and
   price-to-metal figure on the site was recomputed by the build script at $128.48/g. Both the morning
   and afternoon quotes are published with their timestamps.
2. **All seven Etsy listings opened** (pass 3 had been refused with HTTP 500). One price was **wrong and
   is corrected**: ET-4366425533 is **$546.09**, not $547.26. The old figure stays in the audit trail.
3. **One listing is sold out.** ET-576343849 (the 7 g case-study band) now shows "Sorry, this item is
   sold out"; it carries a **SOLD OUT** badge and FL-29, and its $444.80 is labelled a dated observation.
4. **Brilliant Earth served EUR for the Freesia** (€835.00) on a mixed-currency page minutes after the
   Nadia page served USD normally, so BE-1343 now carries FL-08 and its $750 is labelled as the 5:44 a.m.
   reading. **No currency is ever converted in this project.**
5. **Two sessions re-read the same spot page within the hour.** Session `3bf55199` independently
   fetched the 4:10 p.m. ET Kitco page and arrived at the same $3,996.10 / $128.48. This pass keeps that
   quote once, credits both reads in the prior chain, and adds what the other pass did not cover: the
   seven Etsy listings, the price correction, the sold-out listing and the Brilliant Earth EUR render.
6. **A stale derived number was removed from prose.** A note used to hard-code "~$529" of metal value
   computed at an older spot; the note now points at the computed column. The hallucination sweep
   re-derived every hand-written dollar figure in the dataset the same way — one was wrong, and it is fixed.

## The thesis holds

**A 14K or 18K stamp does not prove purity, and in this dataset no listing is documented well enough to
buy without asking the seller for more.** 0 of 25 rows state a maker's mark; 17 publish no gram weight;
16 never say "solid gold"; 7 have no verified return policy; no listing offers an XRF test. The dashboard
leads with that finding rather than with a "best buy".

## What the site contains

| Page | Contents |
|---|---|
| `index.html` | Dashboard: NO HALLUCINATIONS panel, spot with timestamp, bottom-line verdict, stat cards, price/metal findings, category cards and the best-documented rows |
| `site/categories.html` | **Category index** (new): seven views over the same 25 rows with counts, price ranges and links |
| `site/category-*.html` | **Category subpages** (new): solitaires, halo & pavé, 18K, complete rings, settings only, bands, case study — same table layout and source links, no value changed |
| `site/listings.html` | All 25 rows: price, karat, grams, fine gold, metal value, price ÷ metal, solid-gold wording, hallmark + maker's mark, return policy, check date + provenance badge, flags — and a SOLD OUT badge on the one listing that is no longer buyable |
| `site/gold-price.html` | Timestamped 2026-10-23 quote, dated prior-day quotes, per-purity values (10K–24K), raw-gold table by weight |
| `site/calculator.html` | Live gold calculator: grams × karat × spot → fine gold, metal value, price ÷ metal, verdict |
| `site/checklist.html` | The 12-point buying checklist, each point tied to an official source and to what the dataset shows |
| `site/sellers.html` | 13 sellers: contact, returns, warranty, payment, reputation, flags |
| `site/analysis.html` | Median markups, the below-metal case, documentation ranking, completeness scorecard, seller concentration |
| `site/flagged.html` | All 29 flags (24 open, 5 resolved), each with detail, affected rows and links |
| `site/sources.html` | Every source used, with what it was used for and the check date |
| `site/verification.html` | Method, today's fetch log, the earlier captures, corrections made, checker result, unverified list |
| `site/master-audit.html` | Session b1f2fe3b's cross-session audit + XRF/stone-deduction calculator (dated 2026-10-22, preserved) |

**Prices change** — re-check before buying. The original 2026-10-22 quotes are retained as dated
history and are never used in a calculation.

## Build pipeline

```
scripts/author_data.py        ->  site/assets/data.json       (single source of truth)
scripts/site_categories.py    ->  category rules shared by builder and checker
scripts/build_site.py         ->  index.html + site/*.html    (static, stdlib only)
scripts/verify.py             ->  data/check_report_v2.json   (21 checks, exit 1 on failure)
```

```bash
python3 scripts/author_data.py && python3 scripts/build_site.py && python3 scripts/verify.py
```

No frameworks, no external fonts, no third-party JavaScript, no network calls from the site.

## Evidence for this pass

- `data/live_check_2026-10-23.json` — every URL attempted in the 5:44 a.m. ET pass, its status (`ok`,
  `nav_only`, `http_500`, `not_refetched`), the value read, and the failure reason.
- `data/live_check_3bf55199.json` — the parallel 4:10 p.m. ET intraday re-check by session `3bf55199`
  (Kitco $3,996.10 / $128.48 plus four listings re-confirmed unchanged). Its spot figures matched this
  pass independently, which is why the merge kept one quote rather than two.
- `data/live_check_463d0ea2.json` — **this pass**: 22 URLs attempted (20 read, 1 served EUR, 1 sold out,
  0 failures), with the value read and the change against the 2026-10-22 dataset.
- `data/evidence/p4_*.txt` — verbatim pass-4 excerpts for Kitco, Blue Nile, Allurez/Avianne/Jewelry
  Master/Solid Gold Jewelers, Brilliant Earth and all seven Etsy listings.
- `verification/evidence/v2/*.txt` — verbatim excerpts for Kitco, Blue Nile (products + returns),
  Allurez, Avianne, The Jewelry Master, Solid Gold Jewelers, FTC, eCFR and 15 U.S.C. § 295.
- `docs/verification/final-integration-2026-10-23.md` — the integration memo: what was checked, what
  changed, what could not be re-checked, and every checker result.
- `COORDINATION.md` — the shared board: this session's claim, each task's status, the sources used and
  the irregularities logged.

## Archived deliverables (preserved, not modified)

| Session | Delivery | Where |
|---|---|---|
| `638c9614` | 11 rings + sellers/spot/flags, evidence transcripts, checker + builder | `data/`, `docs/`, `tools/` |
| `090bae73` | 14-page checklist-format guide | `index-090bae73.html`, `pages/`, `guide/`, `assets/` |
| `37e8ff42` | First root dashboard (14 listings, 8 pages) | `archive/session-37e8ff42/` |
| `93032b31` | 24-row pass-2 dashboard | `archive/session-93032b31/` |
| `84be683f` | Generated 11-page site + its own builder/checker and CI | `verified/` |
| `60c4b9c3` | Report site, evidence and security tests | `report/`, `verification/` |
| `b1f2fe3b` | Master cross-session audit (38 rows), statutory memos, 12-check audit | `site/master-audit.html`, `scripts/audit_b1f2fe3b.py`, `data/b1f2fe3b_*.json` |
| `3e3fae49` | 58-row dossier site with its own 18-check build | `dossier/` |
| `7cca80c9` | 25-row consolidated dashboard and 15-check harness (base of this pass) | root `index.html`, `site/`, `scripts/` |
| `a255f011` | **This pass**: 2026-10-23 re-verification, 28 flags, category pages, 21-check harness | root site, `scripts/`, `verification/evidence/v2/` |

## Refreshing data

1. Re-open each listing and policy page; record the value, the exact quote, the URL and the date in
   `scripts/author_data.py`. Never overwrite a value with an estimate.
2. Re-read an entry only if you actually see the value on the page; otherwise leave its old date and
   add it to FL-26/27/28.
3. `python3 scripts/author_data.py && python3 scripts/build_site.py && python3 scripts/verify.py`.
4. Commit the regenerated `index.html`, `site/*.html`, `site/assets/data.json`, `site/assets/data.js`,
   `data/check_report_v2.json` and the report in `docs/verification/`.
5. Log the pass in `COORDINATION.md`.

---

<details>
<summary><b>Appendix — previous README (session <code>93032b31</code>, preserved verbatim)</b></summary>

# GOLD5 — gold engagement ring research

A research dashboard for **finding gold engagement rings that can actually be verified**: solid gold (not plated,
filled or vermeil), a stated karat, a hallmark **and** a maker's mark, a published weight in grams, a real seller, a price
that makes sense against the gold market, a usable return window, and a path to independent XRF testing on delivery.

**Live site:** https://karagemop466-tech.github.io/GOLD5/

**Verification suite (this pass):** https://karagemop466-tech.github.io/GOLD5/report/
— 27 listings, 9 sellers, 27 flags, the gold-value calculator, and a per-row evidence trail. Gate:

```bash
python3 tools/build_data.py      # dataset from authored sources
python3 tools/build_report.py    # 9 pages -> report/
python3 tools/check_report.py    # 1,600+ assertions: evidence match, spot, derived, money, links, flags, pass log
python3 tools/security_test.py   # plants 9 errors on purpose; all 9 must be caught
```

### Deliveries preserved in this repo (nothing deleted)

| Path | Owner / purpose |
|---|---|
| `index.html` + root pages (`listings.html`, `sellers.html`, `gold-price.html`, `calculator.html`, `checklist.html`, `analysis.html`, `verification.html`, `flagged.html`, `sources.html`, `archive.html`) | integrated root dashboard (session `93032b31`), with one added nav link to `report/` |
| `report/**` | verification suite: evidence-matched rows, calculator, flags, method + pass log (session `60c4b9c3`) |
| `verified/**` | parallel site with its own checker and JSON dataset (session `84be683f`), live at `/verified/` |
| `docs/**` | earlier documented pass with `tools/check_hallucinations.py` (session `638c9614`) |
| `site/**`, `index-37e8ff42.html`, `pages/**`, `index-090bae73.html` | earlier preserved deliveries |
| `scripts/verify.py` | gate for the root dashboard |

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
— integrated root dashboard, plus this project's verification suite at
https://karagemop466-tech.github.io/GOLD5/report/index.html
(9 pages: dashboard · All listings · By karat · Gold value & calculator · Sellers · Checklist ·
Flagged for review · Sources · Method).

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
| `report/**` | **This pass's site** — dashboard at `report/index.html` + category subpages, calculator, flag page, sources, method. Generated by `tools/build_report.py` from `verification/data.json`. Never edit the HTML by hand; edit the data and rebuild. |
| `index.html` + root pages | The integrated root dashboard of session `93032b31` (Listings, Sellers, Gold price, Calculator, Checklist, Analysis, Verification, Flagged, Sources, Archive). Preserved; this pass only added a nav link to `report/index.html`. |
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

---

## Session `3e3fae49` — the 58-row dossier at `/dossier/` (added 2026-10-23)

**Live:** <https://karagemop466-tech.github.io/GOLD5/dossier/> · an additional independent delivery in an
exclusive directory scope, so nothing above was modified except one additive card on the root
dashboard and this section.

| | |
|---|---|
| Entries | **58** rows in `dossier/data/rings.jsonl` — Zales 9, Kay 7, Blue Nile 10, Brilliant Earth 4, eBay 15, Pandora 7, Amazon 2, Jared 1, Etsy 1 |
| Pages | **23** generated: dashboard, master table, 11 category pages, marketplace, calculator, gold price, checklist, sellers, verification, flagged, sources, research index, repo review |
| Evidence | every row carries a source URL, an ISO-8601 UTC capture timestamp and the **verbatim excerpt** containing the number |
| Tiers | 3 rows `live` (read from a live fetch), 55 rows `snippet` (read from a search index of the official page, crawl date published with the row), blanks are `unverified` |
| Checks | `python3 dossier/scripts/build.py` → **18 checks, 18 PASS, 0 FAIL**, 0 broken internal links |
| Flags | 15 project-level findings **F-01…F-15** plus per-row flags, all with source links on `dossier/pages/flagged.html` |

What this delivery adds that the other suites do not have:

- **Karat and metal colour are verified to the same standard as price.** Checks **C14/C15** require the
  asserted karat and metal colour to appear *literally* in the row's own evidence excerpt. C14 withdrew
  four Brilliant Earth rows' karat/metal to **blank** because the value was only inferable from a
  `-14KW` SKU suffix — inference is treated as a hallucination, not as evidence.
- **16 timestamped gold-price observations for one day**, spanning **$71.50/oz**, each with publisher,
  series basis (spot / December futures / CFD) and capture time, plus the LBMA benchmark methodology
  **live-fetched from lbma.org.uk**. No figure anywhere is quoted as "the LBMA price" because that
  tabulated data is licence-gated (**F-01**). The calculator therefore **pre-fills nothing**.
- **A "not solid gold" category** (7 rows) built from brands' own published material strings — e.g.
  Pandora's JSON-LD "14k Gold-plated Signature metal alloy" — mapped to the FTC/eCFR definitions of
  electroplate, vermeil, gold filled, overlay and flashed, with one **FINAL SALE** row flagged.
- **A red-flag category** (3 rows) of marketplace listings that fail the checklist outright: a
  "No Brand" ring at $1,351.01, a 7.50 ct "solid 14K" ring at **$322.27** (below plausible metal
  value), and a listing whose own title claims both `14k` and "Solid 10k".
- **The repository review itself** (`dossier/pages/repo-review.html`): the state of the repo at session
  start, the Pages configuration and why path `/` means the landing page must live at the repository
  root, and every irregularity found in the parallel work, each with the git/gh command that reproduces it.

Rebuild and re-verify:

```bash
python3 dossier/scripts/build.py    # regenerates all 23 pages + exports, then runs 18 checks
```

The generated exports (`dossier/data/rings.json`, `rings.csv`, `verification-report.json`) are
committed because Pages serves this branch with a legacy build and has no data step. The dataset of
record is `dossier/data/rings.jsonl`; the `_seed_*.py` and `_patch_inference.py` scripts in
`dossier/scripts/` are the re-runnable provenance of every row.

**Known limitation, stated plainly:** the page-fetch proxy failed part-way through collection
(**F-03**), so 55 of 58 rows are `snippet` tier rather than `live`. Each such row says so on its face
and publishes its crawl date. Re-read the live page before paying.
