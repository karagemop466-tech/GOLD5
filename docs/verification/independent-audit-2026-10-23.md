# Independent verification audit — session `arena-60a26527` (2026-10-23)

**Scope:** a fresh, independent verification of the root dashboard suite (`index.html` +
`site/*.html`, source of truth `site/assets/data.json`: 25 entries, 13 sellers, 28 flags,
11 references) **after** the 2026-10-23 refresh merged in PRs #33–#38 (sessions `0c967748`,
`887435c2`, `a255f011`). This audit deliberately does **not** import or reuse the project's own
checkers; it re-derives every number from the raw inputs with its own arithmetic and cross-checks
the rendered HTML, so a bug in one of the project's checkers cannot hide a bad value.

**Method:** `python3 scripts/independent_audit.py` — 11 checks (A1–A10 + A2b). Exit 1 on any FAIL.

**State audited:** `main` @ `30fddc1` (PR #38). Spot **$4,022.50/oz = $129.33/g** at
2026-10-23 5:44 a.m. ET (Kitco bid, live re-fetch); 12 rows re-read live on 2026-10-23, 13 rows
retain their 2026-10-22 capture date (labelled `prior`); 19 pages (dashboard + `categories.html`
+ 7 category subpages + 9 existing).

**Baseline (untouched tree):** all eight project harnesses PASS — `scripts/verify.py` 21/21 ·
`scripts/review_current.py --check` PASS · `scripts/audit_b1f2fe3b.py` 6/6 groups (103 pages,
4,057 links) · `tools/check_report.py` PASS · `tools/check_hallucinations.py` 166/0 FAIL ·
`tools/security_test.py` 9/9 planted errors · `dossier/scripts/build.py` 18/18 · `verified/` 896/0.

## Results — 11 pass, 0 fail

| Check | What it proves | Result |
|---|---|---|
| A1 | spot $/oz ÷ 31.1034768 = $/g (`$4,022.50/oz → $129.3264/g`, recorded `$129.33/g`) | PASS |
| A2 | per-purity per-oz = usdPerOz × fineness (24K/22K/18K/14K/10K) | PASS |
| A2b | all 60 raw-gold cells (weight × fineness × $129.33/g) appear on `gold-price.html` | PASS |
| A3 | fine gold = grams × karat/24, recomputed for all 8 weighted rows | PASS |
| A4 | metal value = fine gold × $129.33/g, recomputed | PASS |
| A5 | price-to-metal ratio = price ÷ metal value, recomputed | PASS |
| A6 | every `$` figure on all 19 root pages traces to a dataset value or a recomputation | PASS |
| A7 | every entry source/return URL is https | PASS |
| A8 | all 25 entries carry an official https source URL and a check date | PASS |
| A9 | every recorded price/gram/karat token is backed by a verbatim capture | PASS |
| A10 | landing page carries the NO HALLUCINATIONS banner and the asOf date | PASS |

## Findings

**No hallucination was found.** Every spot, purity, fine-gold, metal-value and ratio figure
recomputes exactly; every dollar figure on every root page traces to a dataset value or a
recomputation (including the category medians, the raw-gold table, and the Kitco body-text daily
change); every row has an official https source and a check date; every recorded price/gram/karat
token appears in a saved verbatim capture.

**Prior finding resolved:** an earlier draft of this audit (run on the pre-refresh 2026-10-22 data)
flagged `ET-944684759`'s `priceNote` variant prices ($337.50 / $369.00 / $429.75) as not present in
the saved evidence. The 2026-10-23 refresh (session `a255f011`) re-read the listing and the
`priceNote` now carries only values backed by the `docs/verification/etsy.md` capture; A9 passes for
all 25 entries. The finding is closed.

**Informational (not a defect):** the gold-price per-purity table renders per-oz as
`round(fineness × $129.33/g, 2) × 31.1034768`, while `data.json` stores `usdPerOz × fineness`
directly; the two differ by < $0.07. Both derive from the verified spot and karat fineness, and the
rendered table shows the "g fine" column so a reader can reproduce it.

**Data freshness:** every value is dated 2026-10-22 or 2026-10-23. The build sandbox can only reach
GitHub / npm / PyPI, so seller hosts cannot be re-fetched from here; the site labels each row's
provenance (`live 2026-10-23` / `captured 2026-10-22`). Re-read each listing before buying.

## Conclusion
The final 2026-10-23 integration is internally consistent and free of hallucinations under an
independent recomputation. The single prior finding is resolved. No change to the dataset or site is
required by this audit.

Re-run anytime: `python3 scripts/independent_audit.py`.
