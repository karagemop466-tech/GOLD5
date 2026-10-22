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
| T2 | Verify gold spot price from official sources (dated quotes) | in progress | 37e8ff42 | `site/assets/data.js` (spot section), `docs/verification/gold-price.md` |
| T3 | Collect & verify Blue Nile 14K/18K engagement-ring listings + seller facts | in progress | 37e8ff42 | `site/assets/data.js` (blue-nile entries), `docs/verification/bluenile.md` |
| T4 | Collect & verify Etsy solid-gold listings (grams + price + hallmark) | unclaimed | 37e8ff42 | `site/assets/data.js` (etsy entries), `docs/verification/etsy.md` |
| T5 | Collect & verify Walmart 14K solid gold listings (if fetchable) | unclaimed | 37e8ff42 | `site/assets/data.js` (walmart entries), `docs/verification/walmart.md` |
| T6 | Verify seller facts: contact, return policy, payment, reputation links | unclaimed | 37e8ff42 | `site/assets/data.js` (sellers), `docs/verification/sellers.md` |
| T7 | Reference material: checklist, karat/fineness, XRF, FTC hallmark guidance (linked) | unclaimed | 37e8ff42 | `docs/verification/references.md`, site page content for guides |
| T8 | Build GitHub Pages site (index + subpages + calculator + styles) | unclaimed | 37e8ff42 | `index.html`, `site/**` (non-data), `assets/**` |
| T9 | Hallucination/security verification harness + run passes | unclaimed | 37e8ff42 | `scripts/verify.py`, `docs/verification/report.md` |
| T10 | **Integration (final)**: merge data, re-verify line by line, build check, enable Pages, PR + merge, log | unclaimed | 37e8ff42 | `COORDINATION.md` (log section), Pages config |

## Cross-session file requests
(none yet — log any request to edit another session's files here)

## Log
- 2026-10-22 (UTC): `37e8ff42` created board, claimed T1–T10 scopes above. T1 done.
- Note: repo started empty (single `GOLD` commit with README only); no prior work to reconcile.

## Verification policy (applies to ALL sessions)
1. A value is recorded **only** after it is read from the source page (direct fetch) or a search
   result that quotes the source page (snippet) — and the source URL is recorded next to it.
2. `checkedOn` date is recorded for every cell group; stale prices are re-checked before publish.
3. Derived numbers (gold content, gold value) are computed by `scripts/verify.py` from raw inputs —
   never typed by hand, and recomputed at every pass.
4. Anything not confirmable from an official source → blank + `flagged: true` on the Flagged for
   Review page.
