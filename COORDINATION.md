# COORDINATION.md — Shared Task Board (GOLD5)

Project: find & verify **solid gold engagement rings** online. Every table row needs a source
link to an official site; unconfirmable values are left **blank + flagged**, never inferred.
**NO HALLUCINATIONS** — no price, weight, or claim may appear without a cited source + check date.

## Session registry

| Session ID | Branch | Started (UTC) | Notes |
|---|---|---|---|
| `37e8ff42` | `arena/37e8ff42-gold5` | 2026-10-22 | Primary session. Platform (Arena) enforces this single session branch, so task sub-branches `session-37e8ff42/<task>` are not possible; non-overlapping file scopes below are used instead. Logged here as required. |

## Task board

Status: `unclaimed` | `in progress` | `done` | `needs review`
(`needs review` = published on the site's "Flagged for Review" page; does not block work.)

| ID | Task | Status | Owner | File scope (exclusive) |
|---|---|---|---|---|
| T1 | Create COORDINATION.md task board + baseline docs | done | 37e8ff42 | `COORDINATION.md`, `README.md` |
| T2 | Verify gold spot price from official sources (dated quotes) | done | 37e8ff42 | `site/assets/data.js` (spot section), `docs/verification/gold-price.md` |
| T3 | Collect & verify Blue Nile 14K/18K engagement-ring listings + seller facts | done | 37e8ff42 | `site/assets/data.js` (blue-nile entries), `docs/verification/bluenile.md` |
| T4 | Collect & verify Etsy solid-gold listings (grams + price + hallmark) | done | 37e8ff42 | `site/assets/data.js` (etsy entries), `docs/verification/etsy.md` |
| T5 | Collect & verify Walmart 14K solid gold listings (if fetchable) | done (negative) | 37e8ff42 | `docs/verification/sellers.md` (fetch log) |
| T6 | Verify seller facts: contact, return policy, payment, reputation links | done | 37e8ff42 | `site/assets/data.js` (sellers), `docs/verification/sellers.md` |
| T7 | Reference material: checklist, karat/fineness, FTC hallmark guidance (linked) | done | 37e8ff42 | `docs/verification/references.md`, site page content for guides |
| T8 | Build GitHub Pages site (index + subpages + calculator + styles) | done | 37e8ff42 | `index.html`, `site/**` (non-data), `assets/**` |
| T9 | Hallucination/security verification harness + run passes | done | 37e8ff42 | `scripts/verify.py`, `docs/verification/report.md` |
| T10 | **Integration (final)**: merge data, re-verify line by line, build check, enable Pages, PR + merge, log | in progress | 37e8ff42 | `COORDINATION.md` (log section), Pages config |

## T5 note (negative result)
Walmart search HTML serves no product cards/prices (client-rendered); excluded per policy, logged in
`docs/verification/sellers.md`. No Walmart data appears anywhere — nothing was guessed.

## Cross-session file requests
(none yet — log any request to edit another session's files here)

## Log
- 2026-10-22 (UTC): `37e8ff42` created board, claimed T1–T10 scopes above. T1 done.
- Note: repo started empty (single `GOLD` commit with README only); no prior work to reconcile.
- 2026-10-22 (UTC) T2 done: 4 same-day spot quotes (Kitco primary $4,025.00 bid @7:10pm ET direct fetch;
  CNBC $4,083.82 9am ET; APMEX $4,077.60 11:02am ET; Kitco news ~$4,086.90 morning) — spread 1.54%,
  gram/oz math checked. Sources: kitco.com/charts/gold, cnbc.com/select, apmex.com/gold-price, kitco.com news.
- 2026-10-22 (UTC) T3 done: 7 Blue Nile 14K/18K settings verified on product/category pages
  ($870–$2,320, all "setting price"); returns policy (30-day, resized/engraved/custom excluded),
  warranty (eff. 2026-10-11, lifetime ≥$1,000, free resize ≤6mo), contact (1-800-242-2728,
  service@bluenile.com), BBB (A+ since 1999, 121 complaints/3yr, BBB reviews 1/5×25,
  ConsumerAffairs 1.7/5×172). Gram weights not published → blank + F3.
- 2026-10-22 (UTC) T4 done: 8 Etsy shops / 7 active listings + 1 sold case study verified on
  listing pages (RAKSHAKJEWELS 14K $1,891.78 IGI 2.50ct; ForeverForLove 14K from $547.26;
  VeraByEden 14K $969.00 + 3.70g via snippet + off-platform-photos flag F2; VibrantStone from $251.30;
  adelafinejewels 14K $999.70+; Cittali from $195.75; case study 7g 14K at $444.80 = 0.84× melt → F1).
- 2026-10-22 (UTC) T6/T7 done: seller profiles + official references (FTC consumer article fetched
  direct; 16 CFR Part 23 eCFR; Cornell LII §23.3; FTC FRN PDF; Etsy Purchase Protection; JVC;
  ReportFraud).
- 2026-10-22 (UTC) T8/T9 done: site built (8 pages, data-driven, calculator, no build step, no
  external deps). Harness `scripts/verify.py`: PASS 0 errors / 9 checks (sources, dates, domain
  allowlist, spot math, purity math, derived-ratio recompute, flag cross-refs, local link integrity).
  DOM smoke test: 20/20 passed.

## Verification policy (applies to ALL sessions)
1. A value is recorded **only** after it is read from the source page (direct fetch) or a search
   result that quotes the source page (snippet) — and the source URL is recorded next to it.
2. `checkedOn` date is recorded for every cell group; stale prices are re-checked before publish.
3. Derived numbers (gold content, gold value) are computed by `scripts/verify.py` from raw inputs —
   never typed by hand, and recomputed at every pass.
4. Anything not confirmable from an official source → blank + `flagged: true` on the Flagged for
   Review page.
