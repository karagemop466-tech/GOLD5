# Verification report (auto-generated)

- Run: 2026-10-22 23:23 UTC
- Data as of: 2026-10-22
- Result: **PASS** — 0 error(s), 0 warning(s), 9 checks passed

## Checks passed

- spot.primary gram/oz consistent: 4025.0/oz ≈ 129.41/g (published 129.41)
- spot: primary + 3 cross-checks, all same-day with timestamps
- purity table: fineness & per-ounce values consistent with karat math and primary spot
- entry etsy-1151446373: recompute ratio 3.47 (metal value 279.29) — above melt, consistent
- entry etsy-576343849: recompute ratio 0.84 < 1 → correctly flagged price-below-metal-value
- flags: 12 flags, all entryIds resolve
- sellers: 9 profiles, all dated + sourced
- references: 9 official references, all dated + linked
- html: 31 pages, 473 local links resolve, 223 external links http(s)

## Errors

- none

## Warnings

- none

## Reminder

Recommendation after every review: re-run `python3 scripts/verify.py` and scan the
Flagged for Review page for new hallucination/irregularity signals before publishing.
