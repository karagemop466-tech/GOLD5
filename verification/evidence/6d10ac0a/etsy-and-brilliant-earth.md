# Etsy and Brilliant Earth reads — session `6d10ac0a` (2026-10-23)

## L25 — `ET-576343849` · Etsy · BUTTERFLYWINGVINTAGE — **full re-read**

* **Official URL:** <https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1>
* **Result:** unchanged — still **sold out**, exact grams still **not** published.

```
This item is sold out.

Fine 14K Solid White Gold Ring - 7g Solid Gold -Size 11- Comfort Fit Wedding Ring Band-Marked 14K
Price: $420.00
Original Price: $525.00
BUTTERFLYWINGVINTAGE
You can only make an offer when buying a single item

Item details — Highlights
  Handpicked by BUTTERFLYWINGVINTAGE
  Vintage from before 2007
  Materials: White gold, Yellow gold

WELCOME!
I am offering a Fine Solid 14K White Gold Wedding/Engagement Band.
Quality Men's or woman's Comfort Fit Shiny Smooth Finish Wedding Band is marked 14K with a maker's
mark. (Please see 4TH photo). Last photo shows size 11 on the ring sizer. The weight on my postal
scale alternates between 6-7 g.
Was recently Rhodium Plated and in excellent condition
HIGH QUALITY SOLID 14K WHITE GOLD WEDDING BAND
Shipped in a Ring Box

FAQs — Custom and personalised orders
What if item arrives damaged or I misrepresented the item? …
I do not offer a refund for the following reasons:
  Buyers remorse
  Changed mind
  Return postage

Meet your seller — Laura, Owner of BUTTERFLYWINGVINTAGE
BUTTERFLYWINGVINTAGE · Phoenix, Arizona · 5.0 (802) · 2k sales · 12 years on Etsy · 1 shop member
This seller usually responds within a few hours.
Smooth shipping — Has a history of shipping on time with tracking.
Rave reviews — Average review rating is 4.8 or higher.
Etsy Purchase Protection — … we've got your back for all eligible purchases — see program terms
```

| Field | Observed | Canonical | Match |
|---|---|---|---|
| availability | "This item is sold out." | `SOLD OUT — confirmed 2026-10-23` (FL-29) | ✅ |
| price | `$420.00` on the sold-out detail page | 420.00 | ✅ |
| original price | `$525.00` | `compareAt` 525.00 (FL-17) | ✅ |
| grams | **title** says `7g`; **description** says the postal scale "alternates between 6-7 g" | `null` (FL-03) — range not converted | ✅ blank, flagged |
| karat / metal | `14K` white gold | 14 / White Gold | ✅ |
| solid gold stated | **yes** — "Fine Solid 14K White Gold Wedding/Engagement Band" | `solidStated: true` | ✅ |
| karat stamp stated | **yes** — "marked 14K …" | `hallmarkStated: true` | ✅ |
| maker's mark | **seller states it** — "marked 14K with a maker's mark. (Please see 4TH photo)" | `makerMarkStated: true` | ✅ seller statement only |
| returns | seller FAQ refuses refunds for buyer's remorse / changed mind / return postage; item is sold | `returnsVerified: false` (FL-16) | ✅ |

Why the exact weight stays blank: the title asserts `7g` while the seller's own description reports a
scale reading that alternates between 6 and 7 g. Picking either number — or their midpoint, 6.5 g — would
be an inference. The row therefore publishes **no** fine-gold weight, **no** metal value and **no**
below-metal conclusion (FL-01 is retained as *resolved/withdrawn* history, not as a live finding). The
maker's-mark statement is a **seller claim** about a photo, not an assay; it does not satisfy the
checklist's "independent verification" step (FL-20).

---

## Partial read — `ET-1151446373` · Etsy · VeraByEden (corroboration only)

* **Official URL:** <https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant>
* **Status this pass:** the listing **description** was retrieved; the **price block was not present** in
  the retrieved content. The canonical check therefore stays with `bc4e36a1`'s same-day read (L21) and no
  value is upgraded or re-dated by this pass.

```
14K Solid Gold Ruby Diamond Ring: Elegant Handmade Engagement Ring
VeraByEden — Star Seller
Item highlights
  Materials: Rose gold, White gold, Yellow gold
  Made to order
  Gemstone: Ruby

Seller's description — FEATURES
  Yellow gold, white diamond and ruby
  Material: Solid Gold (not gold plated or gold filled)
  Available Gold Color: Yellow gold, rose gold and white gold
  Karat: 14 K (585)
  Diamond weight: 0.30 ct
  Ruby weight: 0.90 ct
  Stone Fragments : 12 Diamonds - 1 Ruby
  Diamond color: F-G Color
  Gold grams: 3.70 gr
  Made to order
  All of our items are 14K real gold. We do not use any gold filled, gold plated or gold vermeil items.
```

Corroboration: `Gold grams: 3.70 gr`, `Karat: 14 K (585)` and the explicit
"Material: Solid Gold (not gold plated or gold filled)" all agree with the canonical row
(`grams 3.7`, `karat 14`, `solidStated true`). **Price was not re-confirmed by this pass** and is
therefore labelled inherited (L21, `bc4e36a1`, 2026-10-23), not re-read.

Note on `Star Seller`: that badge is Etsy's own programme metric (5-star reviews, on-time shipping,
quick replies). It is **not** an assay, a hallmark verification or a purity guarantee, and it is not
recorded as one.

---

## Partial read — `BE-1343` · Brilliant Earth · Freesia 2mm Solitaire Ring (corroboration only)

* **Official URL:** <https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/>
* **Status this pass:** the page loaded and its title was retrieved —
  `Freesia 2mm Solitaire Ring in 14K Yellow Gold | Brilliant Earth` — but the retrieved content chunk
  contained only the site's navigation and a promotional banner, so **no price was read**. The canonical
  check stays with `bc4e36a1`'s same-day read (L09: page served **€835**) and the USD cell stays **blank**
  under FL-08. No EUR→USD conversion was made, and no price was inferred from the banner.

Promotional banner seen on the page (verbatim, **not** a product price):
"ENDS SOON! Receive a $250 Gift Card With Purchase Over $1,000. Use Code GIFT in Cart."
Header phone: `800.691.0952` → <https://www.brilliantearth.com/contact/>.

This is a concrete example of the rule in action: a partially retrieved page yields **no** value, and the
row keeps its blank plus its flag instead of borrowing a number from another currency, another variant or
another session's memory.
