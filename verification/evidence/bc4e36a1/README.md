# Evidence index — session bc4e36a1

Official-source review date: **2026-10-23**. Branch: `arena/bc4e36a1-gold5`.

The machine-readable ledger is [`data/live_check_bc4e36a1.json`](../../../data/live_check_bc4e36a1.json). It contains 46 successful official-page reads: 25 listing pages, 9 seller policy/warranty/contact pages, 11 official references, and one Kitco quote. The canonical verifier compares every listing observation with the published row.

- [Retailer listings and policies](retailers.md)
- [Etsy listings](etsy.md)
- [Gold quote and official references](spot-and-references.md)

## Reading rule

**No hallucinations:** no price, weight, karat, mark, policy, or availability claim is filled in from another listing. A blank is an explicit unverified result. `observed.price` is the numeric value eligible for the canonical price cell; EUR-only pages therefore have `null` USD prices. The sold case study has a displayed sold price but no exact weight and is not a purchase offer.
