# T4 — Etsy listings verification (checked 2026-10-22)

Capture method: **direct page fetches** of etsy.com listing pages (server-rendered).
Etsy marketplace facts: Purchase Protection buyer program — https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program
("full refund for qualifying orders when your item: Doesn't arrive / Arrives damaged / Arrives 7+ days after the maximum estimated delivery date … / Differs significantly from the item description"); Buyer Policy — https://www.etsy.com/legal/buyers/.

## Engagement rings
### etsy-4426190660 — RAKSHAKJEWELS (Star Seller, 5.0)
URL: https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond
- "NowPrice:$1,202.08+ … Original Price: $2,404.16+ … 50% off … Low in stock, only 1 left"
- Material options verbatim: "925 SILVER ($1,202.08) · 10K YELLOW GOLD ($1,686.02) · … · 14K YELLOW GOLD ($1,891.78) · … · 18K YELLOW GOLD ($2,109.58)"
- "2.50 CT (± 0.03 CT) Approx. … Color: YELLOW … Clarity: VVS2 … IGI Certified"; "Band Width: 1.80 mm Approx."
- "Metal Options: Available in 10K/14K/18K Solid Gold (White, Yellow, Rose Gold) & Platinum"
- "Returns & exchanges accepted" (Etsy tab)
- Recorded: price 1891.78 (14K YG option), original 2404.16, width 1.80 mm. Grams not published → blank/F3.

### etsy-4366425533 — ForeverForLove (Star Seller, 5.0)
URL: https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown
- "NowPrice:$376.61+ … Original Price: $627.68+ … 40% off … Only 1 left and in 1 cart"
- Options verbatim: "Silver ($376.61 - $2,278.99) … 14K Yellow Gold ($547.26 - $2,410.13) … 18K … ($595.18 - $2,450.48) … platinum ($679.24 - $2,431.99)"
- Description: "Made with genuine 14k real gold – never plated or filled"; "Metal stamp: Yes"; "Bandwidth: 1.50 MM … Thickness: 1.40 MM"
- "Returns & exchanges — Accepted within 30 days — Buyers are responsible for return shipping costs."
- Recording note: recorded price = 14K minimum (0.50 CT at $547.26), the smallest 14K configuration — the $376.61 "from" price is the silver option and is noted as such.

### etsy-1151446373 — VeraByEden (Star Seller, 5.0)
URL: https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant
- "Price:$783.00+ … Original Price: $1,044.00+ … 25% off"
- Options verbatim: "10K YELLOW GOLD ($783.00) … 14K YELLOW GOLD ($969.00) … 18K YELLOW GOLD ($1,233.00)"
- "Returns & exchanges accepted"
- Grams: "Gold grams: 3.70 gr" appears in the listing's Highlights **as captured by the search index** (our direct fetch did not render that section) → recorded with note + flag F6. Highlights also state (snippet): "Material: Solid Gold (not gold plated or gold filled) … Karat: 14 K (585) … Diamond weight: 0.30 ct … Ruby weight: 0.90 ct".
- **Irregularity (flag F2):** listing photos include a chat screenshot with map pin "2355 Westwood Boulevard #153 Los Angeles CA 90082 USA" and text "Can you give me your address for delivery? … Share your contact information with us on Etsy Message." Off-platform fulfillment bypasses purchase protection.

## Reference bands
### etsy-1566052947 — VibrantStone (Star Seller, 5.0, "Etsy's Pick", "Handcrafted in Los Angeles")
URL: https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band
- "NowPrice:$251.30+ … Original Price: $359.00+ … 30% off"
- Width options verbatim: "2mm ($251.30 - $391.30) · 3mm ($363.30 - $566.30) · 4mm ($496.30 - $783.30) · 5mm ($643.30 - $1,021.30) · 6mm ($797.30 - $1,259.30) · 7mm ($944.30 - $1,497.30) · 8mm ($1,091.30 - $1,742.30)"
- Grams not published → blank/F3.

### etsy-1433905613 — adelafinejewels (Star Seller, 5.0)
URL: https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished
- "NowPrice:$674.70+ … Original Price: $1,038.00+ … 35% off"
- Options verbatim: "10K Gold ($674.70 - $963.95) · 14K Gold ($999.70 - $1,368.90)"
- Buyer-photo alt text on page: "the interior of the ring features the engraved text 585 AFJ, indicating the metal purity and maker's mark" (photo of this design family — noted as evidence a 585+maker mark exists, not as the ring's own photo).

### etsy-944684759 — CittaliFineJewelry (item avg 4.9)
URL: https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished
- "NowPrice:$195.75+ … Original Price: $261.00+ … 25% off"
- Width options verbatim: "2mm ($195.75 - $328.50) … 6mm ($524.25 - $1,158.75)"
- Description: "Materials: Sterling Silver, Gold Vermeil, 10k, 14k, 18k Solid Gold" (design family); "Thickness: 1.10mm"
- "Returns & exchanges — Accepted within 30 days"
- Note for buyers: same design is also sold as vermeil/silver elsewhere — buy THIS 14K listing URL only.

## Case study (sold at check time)
### etsy-576343849 — BUTTERFLYWINGVINTAGE (802 reviews, 5.0)
URL: https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g
- Direct fetch (2026-10-22): page shows "Sorry, this item is sold out / Sold".
- Price per **search snippet of the listing page**: "Price: $444.80 / Original Price: $556.00 / (20% Off)"; title: "Fine 14K Solid White Gold Ring - 7g Solid Gold -size 11- Comfort Fit Wedding Ring Band-Marked 14K".
- Metal test (recomputed by scripts/verify.py): 7 g × 0.5833 × $129.41 = $528.43 → price ratio 0.84 → **below melt** → flag F1 (classic red flag; retained as case study).

## Irregularities
- F1 (below-melt case study), F2 (off-platform photos), F6 (grams via snippet), F8 (variable promo pricing), F11 (stamp ≠ proof).
