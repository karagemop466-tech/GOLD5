# T6 — Seller facts verification (checked 2026-10-22)

## Blue Nile
- Contact: direct fetch of https://www.bluenile.com/contact-us — "Call 1-800-242-2728", "Email us at service@bluenile.com", live chat/WhatsApp, showrooms.
- Returns: direct fetch of https://www.bluenile.com/policies/returns — 30-day money-back; exclusions verbatim (see bluenile.md); 2 complimentary returns/yr; RMA.
- Warranty: direct fetch of https://www.bluenile.com/services/warranty — "Effective Oct 11, 2026", limited lifetime on gold/platinum ≥ $1,000, free resize ≤2 sizes within 6 months.
- Reputation (search snippets of BBB profile pages, 2026-10-22):
  - https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564 — "BBB Accredited since 3/1/1999. Phone: (206) 336-6700. Jewelry Stores in Seattle, WA … Number of Employees: 700"
  - …/complaints — "121 total complaints in the last 3 years. 22 complaints filed in the last 12 months." (structured data on page also lists "BBB Rating": "A+")
  - …/customer-reviews — "1/5 stars — Average of 25 Customer Reviews" (includes a 1-star review dated 09/23/2026 about missed delivery deadlines)
  - https://www.consumeraffairs.com/retail/blue-nile.html — "1.7 … 172 reviews … Cons: Order delays and shipping issues, Inconsistent customer service, Limited return policy"
  - https://www.topconsumerreviews.com/best-jewelry-stores/reviews/blue-nile.php (Oct 2026) — "VERY GOOD … 'A+' rated and accredited by the BBB … just over 100 complaints … last 3 years … 28% of the Trustpilot scores are just 1 star"
  - Excluded (confusingly similar): bbb.org/us/ca/santa-clara/... "Blue Nile … Related Businesses: Signet Jewelers" — different BBB file; NOT used for Blue Nile Inc data.

## Etsy (marketplace)
- Purchase Protection (buyer): https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program (search snippet of official page) — full refund for qualifying orders that don't arrive / arrive damaged / arrive 7+ days late / differ significantly from description.
- Buyer Policy: https://www.etsy.com/legal/buyers/ — "Buyers may receive a full refund for purchases that never arrive, arrive late, arrive damaged, or do not match the listing description."
- Seller-side coverage note: https://www.etsy.com/legal/policy/purchase-protection-program-for-sellers/34509585385 — "Etsy may cover buyer refunds up to $250 on any case arising from a qualified order … effective July 9, 2026" (context only; buyer-facing promise above is what matters to the buyer).
- Individual shops: facts taken from the listing pages fetched in etsy.md (Star Seller status, review scores, return tabs, Klarna/free-shipping statements, description claims).

## Fetch log — retailers EXCLUDED (not verified, therefore not in the table)
| Retailer | Attempt | Result | Disposition |
|----------|---------|--------|-------------|
| Zales | fetch https://www.zales.com/engagement-rings | only chat-widget HTML returned (client-side render; no product/price data) | excluded — flag F9 |
| Kay | fetch https://www.kay.com/engagement-rings | only chat-widget HTML returned (client-side render) | excluded — flag F9 |
| Goldspring | fetch https://www.goldspring.com/collections/wedding-engagement-rings | "yfdpco5.com is blocked … ERR_BLOCKED_BY_CLIENT" | excluded — flag F9 |
| Clean Origins | fetch https://www.cleancleanorigins.com/collections/rings (×2) | "Failed to fetch page" (bot protection) | excluded — flag F9 |
| Icing | fetch https://www.icing.com/collections/engagement-rings | redirect to claires.com homepage (Icing is a Claire's brand; fashion jewelry, not solid gold) | excluded — out of scope |
| Walmart | fetch https://www.walmart.com/search?q=14k+solid+gold+engagement+ring | filter pills + image URLs only, no product cards/prices in served HTML | excluded — flag F9 |
| Blue Nile (wrong URL) | fetch /rings/engagement-rings | 404 → correct URL /engagement-rings fetched successfully | n/a (process note) |

No prices or weights from any of the excluded retailers appear anywhere in the dataset.

## Irregularities
- Blue Nile reputation is genuinely mixed → flag F4 (real business, real contact info, significant complaint volume).
- Blue Nile return exclusions (resized/engraved/custom) → flag F5.
- One Etsy shop (VeraByEden) solicits off-platform contact in listing photos → flag F2.
