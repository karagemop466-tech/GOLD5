# L19–L25 — Etsy listings re-read live (session `3dfe4d85`, 2026-10-25)

All seven Etsy listing pages opened successfully this pass (no HTTP 500 class failures). Three rows
show **price drift** versus the 2026-10-23 canonical values — corrected from these captures, not
erased: the superseded figures are carried in the ledger `corrections` list and on the site.

## L19 — ET-4426190660 (unchanged: the 14K variant still shows $1,891.78)

```
# 2.50 CT Radiant Cut Canary Yellow Lab Grown Diamond IGI Certified Engagement Ring, Half Eternity
Pave Ring, 14k Yellow Gold Anniversary Gift
Low in stock, only 1 left
NowPrice:$1,202.08+    Original Price: $2,404.16+    50% off    •    Sale ends in 15:11:39
MATERIAL options:
  925 SILVER ($1,202.08)   10K YELLOW GOLD ($1,686.02)   10K ROSE GOLD ($1,686.02)
  10K WHITE GOLD ($1,686.02)   14K YELLOW GOLD ($1,891.78)   14K ROSE GOLD ($1,891.78)
  14K WHITE GOLD ($1,891.78)   18K YELLOW GOLD ($2,109.58)   18K ROSE GOLD ($2,109.58)
  18K WHITE GOLD ($2,109.58)
"Returns & exchanges accepted" | RAKSHAKJewels Star Seller, 5 out of 5 stars
Description: "Band Width: 1.80 mm Approx. | Band Thickness: 1.60 mm Approx."
"Metal Options: Available in 10K/14K/18K Solid Gold (White, Yellow, Rose Gold) & Platinum."
"From $58/month, or 4 payments at 0% interest with Klarna"
```

NEW this pass: the sale countdown "Sale ends in 15:11:39" is now visible and captured — the
time-left-on-sale gap the pass-4 log asked the next session to close (FL-17 extended). Countdowns are
relative to read time; the absolute end instant is not published, so none is recorded.

## L20 — ET-4366425533 (**corrected: 546.09 → 546.18**)

```
# Emerald Cut E, VVS2 IGI Certified Lab Grown Diamond Engagement Ring: 14K Gold Hidden Halo
Anniversary ring, Perfect Gift
Low in stock, only 1 left
NowPrice:$375.86+    Original Price: $626.44+    40% off    •    Sale ends in 3 days
Material options:
  Silver ($375.86 - $2,274.48)
  10K Yellow Gold ($486.61 - $2,319.78)   10K White Gold ($486.61 - $2,319.78)
  10K Rose Gold ($486.61 - $2,319.78)
  14K Yellow Gold ($546.18 - $2,405.36)   14K White Gold ($546.18 - $2,405.36)
  14K Rose Gold ($546.18 - $2,405.36)
  18K Yellow Gold ($594.00 - $2,445.63)  18K White Gold ($594.00 - $2,445.63)
  18K Rose Gold ($594.00 - $2,445.63)    platinum ($677.90 - $2,427.17)
Centre Diamond Size (IGI Certified): 0.50 CT ($375.86 - $677.90) … 3.00 CT ($2,274.48 - $2,445.63)
Description: "Made with genuine 14k real gold – never plated or filled"
"Metal option: Real solid gold (10K, 14K, 18K), 925 Silver, 950 Platinum"
"Metal stamp: Yes" | "Bandwidth: 1.50 MM" | "Thickness: 1.40 MM"
"Returns & exchanges accepted" · "within 30 days" · "Ships from: United Kingdom" · Free shipping
ForeverForLove Star Seller, 5 out of 5 stars
"From $34/month, or 4 payments at 0% interest with Klarna"
```

14K variant range start moved **$546.09 → $546.18** and top end **$2,404.96 → $2,405.36** versus
the 2026-10-23 read; the silver header now reads $375.86+ / original $626.44+ (2026-10-23:
$375.80+ / $626.34+). The 25%→40% promo and "Sale ends in 3 days" (2026-10-23 read said
"Sale ends in 1 day") confirm FL-17: these prices rotate. No 14K-specific compare-at price is
published — the header original belongs to the silver base variant, so `compareAt` stays blank.

## L21 — ET-1151446373 (unchanged)

```
# 14K Solid Gold Ruby Diamond Ring: Elegant Handmade Engagement Ring
Price:$783.00+    Original Price: $1,044.00+    25% off    •    Limited time sale
Primary color options:
  10K YELLOW GOLD ($783.00)  10K ROSE GOLD ($783.00)  10K WHITE GOLD ($783.00)
  14K YELLOW GOLD ($969.00)  14K ROSE GOLD ($969.00)  14K WHITE GOLD ($969.00)
  18K YELLOW GOLD ($1,233.00) 18K ROSE GOLD ($1,233.00) 18K WHITE GOLD ($1,233.00)
FEATURES: "Material: Solid Gold (not gold plated or gold filled)" · "Karat: 14 K (585)" ·
"Diamond weight: 0.30 ct" · "Ruby weight: 0.90 ct" · "Gold grams: 3.70 gr" · "Made to order"
"All of our items are 14K real gold. We do not use any gold filled, gold plated or gold vermeil items."
Production partner "Vera Atolye, Istanbul, Türkiye" · Ships from "Albany, NY"
Returns: "Returns & exchanges accepted" · "within 7 days" · "Buyers are responsible for return
shipping costs."
"Order today to get by Nov 2-9" | VeraByEden Star Seller, 5 out of 5
```

14K $969.00 unchanged; "Gold grams: 3.70 gr" unchanged (the row that was a *partial* read last pass
because the price block was missing — this pass retrieved both the price block and the description).
Listing image 11 remains the chat-screenshot soliciting off-platform contact (FL-02 unchanged):
"Hi! 2355 Westwood Boulevard #153 Los Angeles CA 90082 USA … Share your contact information with us
on Etsy Message."

## L22 — ET-1566052947 (**corrected: 251.30 → 246.35**)

```
# 14k Solid Yellow Gold Domed Wedding Band | 2mm - 8mm Gold Ring | Classic Dome Comfort Fit
Wedding Band | Men and Women's Engraved Ring
Etsy's Pick · In 20+ carts
NowPrice:$246.35+    Original Price: $379.00+    35% off    •    Sale ends in 1 day
Band width options: 2mm ($246.35 - $382.85) · 3mm ($330.85 - $525.85) · 4mm ($460.85 - $740.35) ·
5mm ($597.35 - $967.85) · 6mm ($740.35 - $1,195.35) · 7mm ($870.35 - $1,409.85) ·
8mm ($1,000.35 - $1,630.85)
Ring size ladder prints $246.35–$1,000.35 at size 2 up to $382.85–$1,630.85 at size 13.5
"Returns & exchanges accepted" | VibrantStone Star Seller, 5 out of 5
```

2026-10-23 canonical: "From $251.30 (2 mm, 30% off $359.00)". 2026-10-25: the 2 mm ladder start is
**$246.35** and the header shows 35% off original **$379.00+**. Price and both header figures
changed; recorded from this capture. No gram weight published on the page (FL-03 unchanged).

## L23 — ET-1433905613 (**corrected: 999.70 → 984.32**)

```
# 14K Solid Gold 8mm White Gold Polished Mens Womens Comfort Fit Dome Wedding Band
NowPrice:$664.32+    Original Price: $1,038.00+    36% off    •    Sale ends in 0:29:08
Arrives soon! Get it by Oct 30-Nov 4
Material options: 10K Gold ($664.32 - $949.12) · 14K Gold ($984.32 - $1,347.84)
Ring size ladder: size 3 ($664.32 - $984.32) … size 13 US ($949.12 - $1,347.84)
"Returns & exchanges accepted" | adelafinejewels Star Seller, 5 out of 5
Personalization offered (engraving text, 0/40 characters)
```

2026-10-23 canonical: 14K $999.70–$1,368.90 (10K $674.70–$963.95), 35% off. This read: 14K
**$984.32–$1,347.84**, 10K **$664.32–$949.12**, **36% off**, header original still $1,038.00+
(which belongs to the 10K base variant → compareAt stays blank for the 14K row). The countdown read
**0:29:08** — under half an hour from expiry at read time; recorded, not projected (FL-17).

## L24 — ET-944684759 (unchanged)

```
# 14k White Gold Classic Wedding Band, Flat Polished Comfort Fit Ring
12 views in the last 24 hours
NowPrice:$195.75+    Original Price: $261.00+    25% off    •    Sale ends in 0:29:08
Width of the Ring: 2mm ($195.75 - $328.50) · 3mm ($337.50 - $580.50) · 4mm ($369.00 - $798.75) ·
5mm ($429.75 - $942.75) · 6mm ($524.25 - $1,158.75)
"Returns & exchanges accepted" | CittaliFineJewelry, 5 out of 5
```

Every ladder figure matches the 2026-10-23 capture exactly; only the countdown (0:29:08) is new.
The description's other-material options note (FL-17) is unchanged: reconfirm the selected metal at
checkout.

## L25 — ET-576343849 (unchanged — still sold out)

```
This item is sold out.
# Fine 14K Solid White Gold Ring - 7g Solid Gold -Size 11- Comfort Fit Wedding Ring Band-Marked 14K
Price:$420.00    Original Price: $525.00
BUTTERFLYWINGVINTAGE · Phoenix, Arizona · 5.0 (802) · 2.1k sales · 12 years on Etsy
Description: "Fine Solid 14K White Gold Wedding/Engagement Band … marked 14K with a maker's mark.
(Please see 4TH photo) … The weight on my postal scale alternates between 6-7 g."
"Was recently Rhodium Plated and in excellent condition" · "Vintage from before 2007"
"I do not offer a refund for the following reasons: Buyers remorse / Changed mind / Return postage"
```

Sold-listing case study only (FL-29). Title 7 g vs description "alternates between 6-7 g" — exact
grams stay blank (FL-01/FL-18). "Marked 14K with a maker's mark" remains a seller statement backed
by a photo, not an assay (FL-14/FL-20). The no-refund list confirms FL-16.
