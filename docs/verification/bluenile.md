# T3 — Blue Nile verification (checked 2026-10-22)

Capture method: **direct page fetches** of bluenile.com (server-rendered category + product pages).
Category page: https://www.bluenile.com/engagement-rings ("1,451 Results").

## Entries (price verified on the linked page)
| ID | Entry | Price | Verified on |
|----|-------|-------|-------------|
| bn-192506 | Petite Hidden Halo Solitaire Plus, 14K YG (stock 502250y14, 1.60mm) | $1,255 setting price | product page item-192506: "$1,255(Setting Price)"; "Or as low as $213/mo for 6months with the Blue Nile Credit Card" |
| bn-195639 | Petite Solitaire, 14K YG | $1,000 setting price | category page: "Petite Solitaire Engagement Ring in 14k Yellow Gold $1,000(Setting Price)" |
| bn-203257 | Classic Four Prong Solitaire, 14K YG (stock 500000y14, 1.90mm) | $870 setting price | product page item-203257: "$870(Setting Price)"; "classic 14k yellow gold four-prong solitaire engagement ring with platinum prongs" |
| bn-195326 | Riviera Pavé (1/6 ct tw), 14K WG | $1,500 setting price | category page: "Riviera Pavé Diamond Engagement Ring in 14k White Gold (1/6 ct. tw.) $1,500(Setting Price)" |
| bn-195871 | French Pavé (1/4 ct tw), 14K YG (stock 501410y14, 2.50mm, 16 stones G-H VS2-SI1) | $1,800 setting price | product page item-195871: "$1,800(Setting Price)" |
| bn-311132 | Criss Cross Solitaire, 18K YG (by James Allen) | $2,320 setting price | category page: "Criss Cross Solitaire Engagement Ring In 18K Yellow Gold By James Allen $2,320(Setting Price)" |
| bn-203738 | Floral Marquise, 18K WG | $2,210 setting price | category page: "Floral Marquise Diamond Engagement Ring in 18k White Gold $2,210(Setting Price)" |

**Gram weights: not published on any product page** → left blank + flag F3 (rule: never infer).
**Hallmarks:** product pages show stock numbers (e.g. 502250y14) but no stamp photos → hallmark
notes state exactly that; maker's mark blank.

## Seller facts
- Contact (https://www.bluenile.com/contact-us, direct fetch): "Call 1-800-242-2728", "Email us at service@bluenile.com", live chat, WhatsApp, showrooms ("Visit a Showroom / Find Location").
- Returns (https://www.bluenile.com/policies/returns, direct fetch): "30-DAY MONEY BACK GUARANTEE … return eligible items in their original, unworn condition within 30 days from the shipment date"; exclusions verbatim: "Personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance items and 'Final Sale' items are not eligible"; "Two complimentary returns are allowed per customer, per year"; "The cost to replace a missing diamond grading report is $150 and is the direct fee paid the original diamond assessment institution to re-grade that diamond." → flag F5.
- Warranty (https://www.bluenile.com/services/warranty, direct fetch): "Effective Oct 11, 2026 … Limited Lifetime Warranty … gold and platinum jewelry items with a purchase price of $1,000.00 or more against manufacturing defects"; "one-time free ring resizing, up or down two sizes" within 6 months.
- Reputation (search snippets of BBB profile pages, 2026-10-22): BBB A+ "Accredited since 3/1/1999", "(206) 336-6700", "~700 employees", Seattle WA; complaints page: "121 total complaints in the last 3 years. 22 complaints filed in the last 12 months."; customer-reviews page: "Average of 25 Customer Reviews" at 1/5. ConsumerAffairs: "1.7 … 172 reviews". TopConsumerReviews (Oct 2026): "VERY GOOD … A+ rated and accredited by the BBB … just over 100 complaints … last 3 years". → flag F4.
  - Note: a separate BBB profile at bbb.org/us/ca/santa-clara/... (Blue Nile, Signet Jewelers-related) was **not** used — different file; recorded here to prevent confusion.

## Irregularities
- Setting prices only — center diamond extra (0.20–8.00 ct selectable) → flag F10 (not a defect; comparability note).
- "Blue Nile value prop TBD. Learn More" appears verbatim on two product pages (live A/B-test artifact) — no data impact; noted as a site-quality observation.
