# GOLD5 — Solid Gold Engagement Ring Research

A research repository and static dashboard for buying a **gold engagement ring** that can actually be
verified: karat, an explicit "solid gold" statement (not plated / vermeil / filled / overlay / tone),
a hallmark with a **maker's mark** next to the karat stamp, weight in grams, a real seller with real
contact details, a sourced price, a written return policy, credit-card payment, and an independent
jeweller / XRF check on arrival.

**Live site:** <https://karagemop466-tech.github.io/GOLD5/> (GitHub Pages from `main`, path `/`)

## ◆ NO HALLUCINATIONS — the rule this project is built around

**No price, weight, karat, hallmark, policy or date is recorded without a link to the official source
page and the date it was read.** If a value cannot be confirmed it is **left blank and published on
[Flagged for Review](https://karagemop466-tech.github.io/GOLD5/site/flagged.html)** — never guessed,
estimated, averaged, copied from a search snippet, converted from another currency, or carried forward
as if it were current. A seller's statement is labeled as a statement, not as an independent assay.

The current canonical build enforces this in four ways:

1. **Field-level provenance.** All 25 canonical rows were re-read on `2026-10-23`. Each row carries
   `checkedOn`, `provenance`, an official URL, and an evidence ID/path. No canonical row is silently
   carried as a prior capture. Historical quotes and observations remain explicitly dated.
2. **A 46-check evidence ledger.** `data/live_check_bc4e36a1.json` contains 25 listing checks, 9
   policy/contact checks, 11 official-reference checks and 1 Kitco spot check. The authoring script
   compares observed price, grams, karat, solidity, hallmark, maker-mark and return fields with every
   canonical row before emitting JSON. Human-readable excerpts are in `verification/evidence/bc4e36a1/`.
3. **Computed arithmetic and visible conflicts.** Fine gold = exact grams × published fineness; metal
   value = fine gold × the timestamped Kitco bid. No exact weight is inferred from the sold listing's
   6–7 g range. BN-203738's 18K title/specification versus 14K Product Details conflict is shown as
   **FL-30**, not silently resolved.
4. **Security and hallucination hunting after every review.** The canonical checker, independent
   audit, cross-site audit, current-evidence review, report checker, hallucination checker, planted
   security tests, verified archive and dossier are all run before publication. Suspicious values stay
   on Flagged for Review; a green script is not proof of a seller's physical claims.

## Status — 2026-10-23 field-level pass (session `bc4e36a1`)

| | |
|---|---|
| Canonical listings | **25** rows from **13** sellers: 21 engagement-ring rows, 3 bands, 1 sold case study |
| Displayed prices | **22** rows, including the clearly labeled sold-listing display; 3 price cells remain blank (2 EUR-only Brilliant Earth pages and Solid Gold Jewelers) |
| Exact weights | **7** rows; **18** are blank or have only an unsupported range. No range is converted into an exact weight |
| Documentation | **9** explicit solid-gold statements, **2** karat-stamp claims, **1** seller-stated maker's mark, **21** read return policies |
| Spot used | Kitco panel bid **$3,996.10/oz = $128.48/g**, source panel `16:12 NY`, prices stated as of **2026-10-23 4:10 p.m. ET**. Separate body text showed **$3,995.50/oz = $128.46/g** and is disclosed, not mixed into calculations |
| Flags | **30** total: **24 open**, **6 resolved**. Resolved flags remain visible for the audit trail |
| Evidence | **46/46** current checks read; all 25 canonical listings have official links and evidence paths |
| Canonical checker | **PASS — 22/22**, including **10/10** injected-error tests |

### Material corrections in this pass

- Kitco calculations use the new `$3,996.10/oz` / `$128.48/g` panel quote; prior quotes remain dated
  history. Every derived metal value is regenerated.
- Brilliant Earth `BE-1343` serves **€835** and `BE-1343HH` serves **€1,350**; their USD cells are blank.
  `BE-NADIA` is **$1,250** and `BE-SECRET` is now directly **$1,090** USD. No EUR-to-USD conversion is made.
- Etsy `ET-4366425533` is **$546.09–$2,404.96** for 14K options; the unrelated header compare-at value
  is blank. Other variant compare-at values are retained only when they belong to the same displayed
  base variant.
- Etsy `ET-576343849` is explicitly **sold out** and displays **$420** (original **$525**). Its title
  says 7 g but the description says a postal scale alternates between **6–7 g**, so exact grams,
  fine-gold weight, metal value and the former below-metal conclusion are withdrawn. The seller's
  14K/maker's-mark statement is recorded as a claim only.
- Return and warranty wording was corrected from the official Blue Nile, Brilliant Earth and Allurez
  policy pages, including Brilliant Earth's `$40` engraving-removal charge and Allurez's new-stone
  cost exclusion.
- The unified 38-row export and Master Audit now use the primary spot for their primary-spot columns;
  the older recheck quote is separately labeled history.

## What the site contains

| Page | Contents |
|---|---|
| `index.html` | Clean landing dashboard: prominent no-hallucinations rule, current spot, findings, documentation gaps, category links and source-backed weighted rows |
| `site/categories.html` | Category index: seven labeled views over the same 25 rows with counts, price ranges and links |
| `site/category-*.html` | Solitaires, halo & pavé, 18K, complete rings, settings only, bands and the sold case study; same readable table and official links |
| `site/listings.html` | All 25 rows: displayed price/basis, karat, exact grams or blank reason, fine-gold and metal-value calculations, solidity, hallmark/maker statements, returns, check date, evidence and flags |
| `site/gold-price.html` | Timestamped current and historical quotes, Kitco purity values and computed raw-gold table |
| `site/calculator.html` | Browser-only grams × karat × spot calculator; only exact-weight rows can be pre-filled |
| `site/checklist.html` | The 12-point buying checklist with official guidance and current dataset gaps |
| `site/sellers.html` | 13 sellers: contact, return terms, warranty, payment, reputation and flags |
| `site/analysis.html` | Recomputed ratios, medians, an empty-safe below-metal screen, completeness and seller concentration |
| `site/flagged.html` | All 30 flags, affected rows, source links, resolved corrections and remaining review work |
| `site/sources.html` | Source registry grouped by official guidance, gold price, seller policy, reputation and listing |
| `site/verification.html` | Ledger-driven 46-check log, excerpts, evidence files, corrections, checker commands and unresolved fields |
| `site/master-audit.html` | Updated unified 38-row cross-session audit and XRF/stone-deduction calculator; primary and historical spot labels are distinct |

## Build and verification pipeline

```text
scripts/author_data.py        -> site/assets/data.json       (ledger-validated canonical data)
scripts/site_categories.py    -> category rules shared by builder and checker
scripts/build_site.py         -> index.html + canonical site/*.html + data.js
scripts/audit_b1f2fe3b.py     -> unified 38-row catalog + cross-site audit report
scripts/review_current.py     -> deterministic offline current-evidence review
scripts/verify.py             -> data/check_report_v2.json   (22 checks, exit 1 on failure)
scripts/independent_audit.py  -> independent arithmetic/evidence/money audit
```

Run the canonical rebuild and every review harness from the repository root:

```bash
python3 scripts/author_data.py
python3 scripts/build_site.py
python3 scripts/verify.py
python3 scripts/independent_audit.py
python3 scripts/audit_b1f2fe3b.py
python3 scripts/review_current.py --check
python3 tools/check_hallucinations.py
python3 tools/check_report.py
python3 tools/security_test.py
(cd verified && python3 scripts/verify.py)
python3 dossier/scripts/build.py
```

Latest results from this pass:

| Harness | Result |
|---|---|
| `scripts/verify.py` | **PASS 22/22**, C1–C21 plus N1–N10; 19 pages, 65 registered external URLs |
| `scripts/independent_audit.py` | **PASS 11/11**; all 25 rows' price/gram/karat tokens backed by evidence |
| `scripts/audit_b1f2fe3b.py` | **PASS 6/6 groups**; 38 unified rows, 103 HTML pages, 4,186 local links, 4/4 injected errors caught |
| `scripts/review_current.py --check` | **PASS**; 264 records, 92 exact source URLs, 6/6 negative tests |
| `tools/check_hallucinations.py` | **166 passed, 0 FAIL, 0 WARN**; one informational duplicate-weight note retained for review |
| `tools/check_report.py` | **PASS**, 1,649 checks, 0 failures/warnings |
| `tools/security_test.py` | **9/9 planted errors caught**, clean-state PASS |
| `verified/scripts/verify.py` | **896 assertions, 0 failures** |
| `dossier/scripts/build.py` | **18/18 checks**, 58 rows, 23 pages, 1,104 references, 0 broken links |

The archived informational note concerns two different historical listings that both state 2.3 g / 14K;
it is not hidden or converted into a failure. Continue checking it against each seller's own evidence.

## Evidence for this pass

- `data/live_check_bc4e36a1.json` — canonical 46-check ledger, observed fields, official URLs,
  excerpts and nine explicit corrections.
- `verification/evidence/bc4e36a1/README.md` — scope and no-hallucinations method.
- `verification/evidence/bc4e36a1/retailers.md` — Blue Nile, Brilliant Earth, Allurez, Avianne,
  Jewelry Master, Solid Gold Jewelers and policy/contact excerpts.
- `verification/evidence/bc4e36a1/etsy.md` — all seven Etsy listing reads, variants, returns and the
  sold-out detail page.
- `verification/evidence/bc4e36a1/spot-and-references.md` — Kitco and all 11 official/trusted references.
- `data/live_check_77405ae3.json` and other dated ledgers — preserved history, not silently treated as
  the current pass.
- `data/live_check_463d0ea2.json` and `data/live_check_ea49572b.json` — later parallel pass-4 reads;
  their evidence is retained alongside this ledger. They independently confirm the $1,090 BE-SECRET
  USD read, the Etsy price/availability changes and the BE-1343/BE-1343HH EUR renders. Where a later
  record proposed an unsupported exact sold-band weight, the canonical row remains blank.
- `data/evidence/p4_*.txt`, `docs/verification/pass4-2026-10-23.md` and
  `docs/verification/pass4-ea49572b-2026-10-23.md` — the parallel sessions' verbatim excerpts and memos.
- `docs/verification/consolidation-2026-10-23.md` — generated canonical checker report.
- `COORDINATION.md` — shared task board, claims, integration results, irregularities and publication record.

## Refreshing data safely

1. Re-open each official listing and policy page. Record the exact URL, date, observed fields and
   excerpt in a new or updated evidence ledger before changing canonical values.
2. Never infer a missing price, weight, hallmark, return window or currency conversion. Leave it blank,
   add the appropriate flag, and publish the manual-review link.
3. Update `scripts/author_data.py` only from that evidence. Its ledger comparison must pass before it
   can emit JSON. Keep sold, setting-only, from/variant and complete-ring price bases distinct.
4. Rebuild all derived outputs, run every harness above, inspect the diff for stale claims, and run the
   security/hallucination checks again after any correction.
5. Commit small logical changes, run `git pull --rebase` before each push, update `COORDINATION.md`,
   and record the PR/merge/Pages result. Flagged research items do not block merging; a broken site does.

## Archived deliverables (preserved)

Earlier deliveries remain in `docs/`, `dossier/`, `report/`, `verified/`, `guide/`, `review/` and
`archive/` with their own evidence and checkers. They are historical or parallel views, not a reason
to overwrite the canonical evidence trail. The current-evidence `review/` output is regenerated when
its enumerated input URLs change; its blank-current-fields methodology remains intentionally separate.

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
