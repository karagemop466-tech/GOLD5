# Evidence — session `6d10ac0a` (2026-10-23, late-UTC pass)

Branch: `arena/6d10ac0a-gold5` · Claim: `COORDINATION.md` → **V1–V5** · Ledger: [`data/live_check_6d10ac0a.json`](../../../data/live_check_6d10ac0a.json)

## Scope of this pass

This is a **same-day follow-up** to session `bc4e36a1`'s 46-check field-level pass (captured earlier on
2026-10-23 and merged as PR #50). Nothing in that pass is overwritten or relabelled.

| Group | Checks | Read by `6d10ac0a` this pass | Inherited from `bc4e36a1` (same date, 2026-10-23) |
|---|---|---|---|
| Spot | 1 | **1** (Kitco, new quote) | 0 |
| Listings | 25 | **8** | 17 |
| Seller policy / contact | 9 | 0 | 9 |
| Official references | 11 | 0 | 11 |
| **Total** | **46** | **9** | **37** |

Two additional **partial reads** were made this pass and are logged as corroboration only — they do
**not** replace the canonical check and did **not** upgrade any value:

1. `ET-1151446373` — the listing description (grams, karat, solid-gold statement) was retrieved, but the
   price block was not present in the retrieved content, so the row keeps the `bc4e36a1` capture.
2. `BE-1343` — the page loaded (title confirms 14K Yellow Gold) but the retrieved chunk contained only
   site navigation, so the EUR/USD question stays exactly as flagged (FL-08); the USD cell stays blank.

## Method (no hallucinations)

* Every official URL was opened with `fetch_page` and read at field level. Excerpts below are
  **verbatim transcriptions** of what the page displayed, including the seller's own marketing wording.
* Only the retrieval **date** is asserted for product pages. A **time** is recorded only where the source
  itself displayed one (Kitco's panel timestamp and body sentence).
* No missing value was inferred, estimated, averaged or converted between currencies. EUR is not
  converted to USD. A weight **range** is never turned into an exact gram figure.
* A seller's statement is recorded as a **statement**, never as an independent assay or XRF result.
* Derived numbers (fine gold, metal value, price-to-metal, purity table) are recomputed **by script**
  from the verified inputs — see `scripts/author_data.py` — and re-checked by `scripts/verify.py`,
  `scripts/independent_audit.py` and `tools/security_test.py`.
* Failures are logged, not hidden: see [`failures-and-irregularities.md`](failures-and-irregularities.md).

## Files

| File | Contents |
|---|---|
| [`spot.md`](spot.md) | Kitco live gold panel re-read: new primary quote, purity table, unit table, body sentence |
| [`retailers.md`](retailers.md) | Allurez ×3, Avianne & Co, The Jewelry Master, Solid Gold Jewelers, Blue Nile 203738 |
| [`etsy-and-brilliant-earth.md`](etsy-and-brilliant-earth.md) | Etsy sold-out listing full read + the two partial reads |
| [`failures-and-irregularities.md`](failures-and-irregularities.md) | Fetch failures, a mistyped-URL 404, and items recommended for further hunting |
