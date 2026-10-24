# Retailer re-reads — session `6d10ac0a` (2026-10-23)

Seven canonical listing pages were opened directly with `fetch_page` and read at field level this pass.
Every observed value below **matched** the canonical row, so nothing was upgraded, blanked or re-dated.
Where a field's official source is a *different* page than the one re-read here (a separate return-policy
page), that is stated explicitly and the field is marked **inherited** from `bc4e36a1`'s same-day capture.

---

## L13 — `AL-5882` · Allurez · Filigree Designed Solitaire Engagement Ring Setting 14K Yellow Gold

* **Official URL:** <https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold>
* **Result:** unchanged.

Verbatim from the page:

```
Filigree Designed Solitaire Engagement Ring Setting 14K Yellow Gold
$1,085   57% Savings
$2,497   Everyone Else
Setting only. Center stone sold separately.
Metal: 14k Yellow Gold
Style number  U5882
Engagement Ring Information
  Metal        14k Yellow Gold
  Gender       Women's
  Width        2.9mm (Top Width) 2.3mm (Bottom Width)
  Height       3.5mm (Top Height) 1.7mm (Bottom Height)
  Gold Weight  5.00 Grams (Approximate)
Please Note  The center stone is not included in the price of the ring.
Crafted In the USA
Shipping estimate: 10 to 14 business days
```

Page footer/marketing block (verbatim): "Easy Returns — Enjoy lifetime-quality jewelry and exceptional
service. Return or exchange within 30 days if unsatisfied." Header links: "Made in USA", "Easy Returns"
→ `https://www.allurez.com/pages/return-policy`, "Free Shipping".

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | `$1,085` (setting only) | 1085 | ✅ |
| grams | `5.00 Grams (Approximate)` | 5.0 (`gramsText` "5.00 grams (approximate)") | ✅ |
| karat / metal | `14k Yellow Gold` | 14 / Yellow Gold | ✅ |
| solid gold stated | **no** explicit "solid gold" wording on the page | `solidStated: false` (FL-15) | ✅ |
| karat stamp claim | none published | `hallmarkStated: false` (FL-14) | ✅ |
| maker's mark | none published | `makerMarkStated: false` (FL-14) | ✅ |
| returns | **inherited** — the official policy page was not re-read this pass | `returnsVerified: true` (bc4e36a1 P-check) | inherited |

Not used as data: the `$2,497 "Everyone Else"` figure is a marketing comparison (FL-09) and is not
recorded as a price. The `57% Savings` claim is the seller's own arithmetic.

---

## L14 — `AL-170` · Allurez · Antique Engraved Solitaire Engagement Ring Setting 14k Yellow Gold

* **Official URL:** <https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold>
* **Result:** unchanged.

```
Antique Engraved Solitaire Engagement Ring Setting 14k Yellow Gold
$933   32% Savings
$1,373 Everyone Else
Setting only. Center stone sold separately.
Metal: 14k Yellow Gold
Style number  U170
Engagement Ring Information
  Metal        14k Yellow Gold
  Metal Color  Yellow Gold
  Gender       Women's
  Width        3.20mm(Top Width), 2.40mm(Bottom Width)
  Gold Weight  4.80 grams (Approximate)
Please Note  The center diamond is not included in the price of the ring
Crafted In the USA
```

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | `$933` (setting only) | 933 | ✅ |
| grams | `4.80 grams (Approximate)` | 4.8 | ✅ |
| karat / metal | `14k Yellow Gold` | 14 / Yellow Gold | ✅ |
| solid / stamp / maker's mark | none published | all `false` (FL-15, FL-14) | ✅ |
| returns | **inherited** (policy page not re-read this pass) | `returnsVerified: true` | inherited |

---

## L15 — `AL-4426` · Allurez · Engraved Floral Solitaire Engagement Ring Setting 14K Yellow Gold

* **Official URL:** <https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold>
* **Result:** unchanged. (The canonical short name on this site is "Floral Solitaire"; the page's own H1
  is "Engraved Floral Solitaire Engagement Ring Setting 14K Yellow Gold".)

```
Engraved Floral Solitaire Engagement Ring Setting 14K Yellow Gold
$585   51% Savings
$1,194 Everyone Else
Setting only. Center stone sold separately.
Metal: 14k Yellow Gold
Style number  NG4426
Engagement Ring Information
  Metal                     14k Yellow Gold
  Gender                    Women's
  Approximate Metal Weight  3.58 grams
Crafted In the USA
```

Size-conditional surcharges displayed on this page (verbatim from the size selector):
`10.25 (+ $39) 10.5 (+ $49) 10.75 (+ $69) 11 (+ $79) 11.25 (+ $89) 11.5 (+ $99)`.
The canonical price is the **base displayed price** and is labelled as such; no surcharge variant is
recorded as the row price (variant prices are exactly the kind of value this project refuses to blend).

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | `$585` (setting only, base size) | 585 | ✅ |
| grams | `Approximate Metal Weight 3.58 grams` | 3.58 | ✅ |
| karat / metal | `14k Yellow Gold` | 14 / Yellow Gold | ✅ |
| solid / stamp / maker's mark | none published | all `false` (FL-15, FL-14) | ✅ |
| returns | **inherited** (policy page not re-read this pass) | `returnsVerified: true` | inherited |

---

## L16 — `AV-25893` · Avianne & Co · 14K Solid Yellow Gold Diamond Solitaire Engagement Ring 0.41 Ctw

* **Official URL:** <https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw>
  (the page redirected to the same product with `?variant=21168491167803` appended)
* **Result:** unchanged.

```
14K Solid Yellow Gold Diamond Solitaire Engagement Ring 0.41 Ctw
$1,100.00
Gold Color - Yellow     Ring Size - 4.5 … 14
10% OFF WITH CODE "FALL10"
Call Now 1 (332)-244-4038

DESCRIPTION:
This elegant diamond solitaire engagement ring is handcrafted in 14k yellow gold. The center is prong
set with one brilliant round cut diamond which weighs 0.41 carats. The frame measures to 4.5 mm in
width and weighs 2.3 grams.

DETAILS:
  Item Code             R25893
  Diamond Carat Weight  0.41 Ctw
  Diamond Clarity       VS2
  Diamond Color         G, H
  Metal Color           Yellow
  Metal Type            14K Gold
  Item Weight           2.3 grams

Returns of unworn and unaltered items accepted within 14 days.
Visit Our NY Showroom — 28 W 47th Street, Diamond District · New York, NY
Products delivered between Mon, 26 Oct and Fri, 30 Oct.
```

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | `$1,100.00` (complete ring, 0.41 ct center stone) | 1100 | ✅ |
| grams | `Item Weight 2.3 grams` | 2.3 | ✅ |
| karat / metal | `Metal Type 14K Gold`, `Metal Color Yellow` | 14 / Yellow Gold | ✅ |
| solid gold stated | **yes** — product title "14K **Solid** Yellow Gold" | `solidStated: true` | ✅ |
| karat stamp / maker's mark | none published | `hallmarkStated: false`, `makerMarkStated: false` (FL-14) | ✅ |
| returns | on-page line only: "Returns of unworn and unaltered items accepted within 14 days." | `returnsVerified: false` (FL-11) | ✅ |

Not applied: the `FALL10` 10% coupon banner. The recorded price is the displayed price **without** the
promo, exactly as flagged (FL-11).

**Irregularity worth noting (logged, not resolved):** the title says "**Solid**" while the DETAILS table
says only "14K Gold". A title claim is a seller statement, not an assay — the row keeps FL-20
("stamp ≠ proof") guidance and no upgrade is made.

---

## L17 — `JM-149700` · The Jewelry Master · Brilliant Round Diamond Solitaire Engagement Ring 14K Yellow Gold

* **Official URL:** <https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html>
* **Result:** unchanged.

```
Brilliant Round Diamond Solitaire Engagement Ring 14K Yellow Gold
Retail Price $6,041.00    Special Price $3,020.00
Availability: In stock    Only 1 left
Style  149700

PRODUCT DETAILS
This beautiful treasure is entirely handcrafted in pure 14KT solid yellow gold. This engagement ring is
wreathed with prong set brilliant round diamonds and bezel set brilliant round diamonds weighing 0.71
carats. All of the stones are a blinding white G-H color and SI1 clarity.
FREE Shipping, a Gift Box, and a Professional Appraisal Certificate, accompanies each purchase.

Information
  Carats:      0.71ctw
  Stones:      Brilliant Round Diamonds
  Clarity:     SI1
  Color:       G-H
  Setting:     Prong / Bezel
  Metal Type:  14KT Gold
  Metal Weight: 2.3 Grams
  Width:  mm     Length:  mm      (both blank on the page)

Money Back Guarantee (some restrictions apply)*
… you can simply return or exchange your purchase within a 30-day period - no questions asked.
… Jewelry Masters "No Questions Asked," 30-Day return policy.
```

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | `Special Price $3,020.00` (complete ring) | 3020 | ✅ |
| compare-at | `Retail Price $6,041.00` | 6041 (FL-12 retail compare price) | ✅ |
| grams | `Metal Weight: 2.3 Grams` | 2.3 | ✅ |
| karat / metal | `Metal Type: 14KT Gold`, "pure 14KT solid yellow gold" | 14 / Yellow Gold | ✅ |
| solid gold stated | **yes** — "entirely handcrafted in pure 14KT solid yellow gold" | `solidStated: true` | ✅ |
| karat stamp / maker's mark | none published; `Width`/`Length` fields are empty on the page | `false` / `false` (FL-14) | ✅ |
| returns | on-page 30-day guarantee; the "some restrictions apply" list is **not** stated on the page | `returnsVerified: false` | ✅ |

**Irregularity (logged):** this is the only row where two different listings from two different sellers
state the identical `2.3 grams / 14K` combination (with `AV-25893`). The informational check
`tools/check_hallucinations.py` C9 keeps flagging it. Both pages were independently re-read this pass
and both still print 2.3 g, so the duplicate is **real on both pages**, not a transcription error. It
remains open for review rather than being dismissed.

---

## L18 — `SGJ-B02561` · Solid Gold Jewelers · Yellow Gold Solitaire Engagement Ring

* **Official URL:** <https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/>
* **Result:** unchanged — still **no published price**.

```
Yellow Gold Solitaire Engagement Ring
14ky, 4.7g, #B02561
Pricing and availability are subject to change.
SKU: B02561
Categories: Mountings, Rings, Yellow Gold    Tag: Rings
Brand: M Michael
Yellow Gold Solitaire Engagement Ring  quantity  Add to cart
Call (309) 452-1612 for current pricing and availability.
```

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | **none published** — "Call (309) 452-1612 for current pricing and availability." | `null` (FL-13) | ✅ blank, flagged |
| grams | `4.7g` in the page's own spec line | 4.7 (`gramsText` "4.7 g") | ✅ |
| karat / metal | `14ky` (site shorthand for 14K yellow) | 14 / Yellow Gold | ✅ |
| solid gold stated | the shop name and category say "Solid Gold"; the **product page** states no explicit "solid gold" sentence | `solidStated: false` (FL-15) | ✅ |
| karat stamp / maker's mark | none published | `false` / `false` (FL-14) | ✅ |
| returns | no return policy shown on the product page | `returnsVerified: false` (FL-13) | ✅ |

**Observation, deliberately NOT recorded as data:** the page carries a WooCommerce `Brand: M Michael`
taxonomy line. That is the store's brand filter, **not** a statement that the ring is stamped with a
maker's mark, so `makerMarkStated` stays `false` and the row keeps FL-14. Recommended follow-up: ask the
seller by phone whether the piece carries a karat stamp plus a registered manufacturer's mark, and record
the answer as a seller statement with its date.

---

## L07 — `BN-203738` · Blue Nile · Floral Marquise Diamond Engagement Ring in 18k White Gold

* **Official URL:** <https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738>
* **Result:** unchanged, **including the metal conflict (FL-30)**.

```
Floral Marquise Diamond Engagement Ring in 18k White Gold
$2,210 (Setting Price)
Or as low as $376/mo for 6 months with the Blue Nile Credit Card for a total payment of $2,254**
Metal Type: 18K White Gold
Stock Number  502820w
Metal         18K White Gold
Width         1.70mm
Rhodium Finish Yes
Natural Diamond Information — Round: Quantity 2, Total Carat 1/20, G-H, VS2-SI1, Prong
Natural Diamond Information — Marquise: Quantity 4, Total Carat 1/10, G-H, VS2-SI1, Prong

Product Details
This mesmerizing engagement ring is artfully crafted from warmly lustrous 14k yellow gold. It features
marquise-cut diamonds surrounding the center stone, creating a romantic floral-inspired effect.

Limited Lifetime Warranty
We warrant all gold and platinum jewelry items with a purchase price of $1,000 or more from
manufacturer's defect. Limitations Apply.
Free Overnight Shipping · Returns Policy
```

| Field | Observed | Canonical | Match |
|---|---|---|---|
| price | `$2,210 (Setting Price)` | 2210 | ✅ |
| grams | none published | `null` (FL-03) | ✅ blank, flagged |
| karat | title + specification `18K White Gold`; **Product Details says `14k yellow gold`** | 18 with `metalConflict` (FL-30) | ✅ conflict published, not resolved |
| solid gold stated | no explicit "solid gold" wording | `solidStated: false` (FL-15) | ✅ |
| karat stamp / maker's mark | none published | `false` / `false` (FL-14) | ✅ |
| returns | **inherited** — `https://www.bluenile.com/policies/returns` was not re-read this pass | `returnsVerified: true` | inherited |

The conflict is left exactly as published: a buyer must resolve 18K-vs-14K with Blue Nile **before**
purchase, because the two metals differ by 16.67 percentage points of fine gold and therefore by the
melt value of the setting.
