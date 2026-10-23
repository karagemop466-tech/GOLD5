# Current evidence review — 2026-10-23

No current prices are asserted. No new merchant facts were verified.

## Scope

`scripts/review_current.py` reads nine explicitly enumerated product datasets, including
both the dossier JSON and JSONL exports. All 264 stored records are accounted for in
91 exact-URL groups. These are not 264 unique products or 91 authenticated rings.
Each group's `origins` lists the original file, one-based row and recorded ID.
Different URLs are never assumed to be the same item. Labels/categories are historical.
Checklist and seller-only datasets are not product records and remain linked in the
existing dashboard. Earlier evidence is preserved, not rewritten or silently endorsed.

## Verification limits

Merchant, government, standards and gold-price hosts are outside this session's allowed
network destinations. A direct Blue Nile probe failed with `SSL_ERROR_SYSCALL`.
This does not mean the merchant is down. No external product link availability or
source content is claimed to have been verified. All current factual fields are null,
including derived values and assay/marking claims. Current page-check dates are null;
the review date is the repository audit date, not an official-source access date.

R01–R04 are published at `flagged.html` with every affected source URL.
The archived calculator remains a historical/scenario tool, not a current valuation.
Official merchant information would only establish seller claims, not physical purity.

## Reproduce after every review

```sh
python3 scripts/review_current.py
python3 scripts/review_current.py --check
```

The check fails for unsupported current prices, derived amounts, a false verified
status, fabricated source-check date, unsafe source URL or unflagged record (six
mutation tests). It also checks all stored records are represented, output sync,
local links, escaping at render time, and absence of executable elements in the
new review pages. It does not claim to detect every hallucination. Review evidence
manually or with an independent official-source retrieval before upgrading any field.
Legacy suite output from this session is in `test-results.txt`.
