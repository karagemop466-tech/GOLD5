/* GOLD5 data — single source of truth (strict JSON).
   RULE: no value may exist without a source URL + check date (see docs/verification/).
   Verified by scripts/verify.py — run after every review. NO HALLUCINATIONS. */
window.GOLD5_DATA = {
  "meta": {
    "project": "GOLD5 — Solid Gold Engagement Ring Research",
    "noHallucinations": "NO HALLUCINATIONS: every value below was read from the cited source on the cited date. Blank = could not be verified from an official source (flagged on /site/flagged.html). Nothing is inferred.",
    "asOf": "2026-10-22",
    "checkedBy": "session 37e8ff42 (Arena agent)",
    "verifyCommand": "python3 scripts/verify.py"
  },
  "spot": {
    "primary": {
      "source": "Kitco (direct page fetch)",
      "url": "https://www.kitco.com/charts/gold",
      "usdPerOz": 4025.0,
      "usdPerGram": 129.41,
      "asOf": "2026-10-22 7:10 p.m. ET",
      "kind": "spot bid",
      "note": "Page also states: 'The current price of gold is $4,024.60 per troy ounce as of October 22, 2026, 7:10 p.m. ET' and shows bid 4,025.00 / gram 129.41."
    },
    "crossChecks": [
      {
        "source": "CNBC Select (search snippet of page)",
        "url": "https://www.cnbc.com/select/the-price-of-gold-today-oct-22-2026/",
        "usdPerOz": 4083.82,
        "usdPerGram": null,
        "asOf": "2026-10-22 9:00 a.m. ET",
        "kind": "spot",
        "note": "'Gold's spot price ... today as of 9:00 a.m. ET is $4,083.82 per ounce, according to CNBC's Gold/US Dollar Spot Price.'"
      },
      {
        "source": "APMEX (search snippet of page)",
        "url": "https://www.apmex.com/gold-price",
        "usdPerOz": 4077.6,
        "usdPerGram": 131.1,
        "asOf": "2026-10-22 11:02 a.m. ET",
        "kind": "spot",
        "note": "'Gold Spot Price $4,077.60 USD ... Gold Price Per Ounce $4,077.60 ... Per Gram $131.10 ... Last Updated: 10/22/2026 11:02:00 AM ET'."
      },
      {
        "source": "Kitco News AM Report (search snippet of article)",
        "url": "https://www.kitco.com/news/article/2026-10-22/gold-silver-pressured-despite-lower-yields-hormuz-attacks-send-crude-higher",
        "usdPerOz": 4086.9,
        "usdPerGram": null,
        "asOf": "2026-10-22 morning reading",
        "kind": "spot",
        "note": "'At the latest verified morning price reading, spot gold was near $4,086.90 an ounce, down $53.40, or 1.29%'."
      }
    ],
    "purityValues": {
      "source": "Kitco 'Gold Value by Purity' table (direct page fetch, updated Oct 22, 2026 7:11 PM NY)",
      "url": "https://www.kitco.com/charts/gold",
      "perOunce": {
        "24K": 4025.0,
        "22K": 3689.72,
        "18K": 3018.75,
        "14K": 2347.78,
        "10K": 1677.22
      },
      "fineness": {
        "24K": 0.9999,
        "22K": 0.9167,
        "18K": 0.75,
        "14K": 0.5833,
        "10K": 0.4167
      }
    }
  },
  "entries": [
    {
      "id": "bn-192506",
      "name": "Petite Hidden Halo Solitaire Plus — 14K Yellow Gold",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
      "solidGold": "Listing states 'Metal: 14K Yellow Gold' (setting; center stone sold separately)",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 1255,
      "priceLabel": "Setting price, $1,255 (center diamond extra)",
      "originalPrice": null,
      "stockNumber": "502250y14",
      "widthMm": 1.6,
      "hallmark": "Stock number shown (502250y14); hallmark photo not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card; Blue Nile credit card financing advertised on product page",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "bn-195639",
      "name": "Petite Solitaire — 14K Yellow Gold",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639",
      "solidGold": "Listing states 'Petite Solitaire Engagement Ring in 14k Yellow Gold' (setting)",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 1000,
      "priceLabel": "Setting price, $1,000 (as shown on category page)",
      "originalPrice": null,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card (site checkout)",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "bn-203257",
      "name": "Classic Four Prong Solitaire — 14K Yellow Gold",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
      "solidGold": "Listing states 'Metal: 14K Yellow Gold'; description: 'classic 14k yellow gold four-prong solitaire engagement ring'",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 870,
      "priceLabel": "Setting price, $870 (center diamond extra)",
      "originalPrice": null,
      "stockNumber": "500000y14",
      "widthMm": 1.9,
      "hallmark": "Stock number shown (500000y14); hallmark photo not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card; special financing advertised on product page",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "bn-195326",
      "name": "Riviera Pavé (1/6 ct. tw.) — 14K White Gold",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "White Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326",
      "solidGold": "Listing states 'Riviera Pavé Diamond Engagement Ring in 14k White Gold (1/6 ct. tw.)' (setting)",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 1500,
      "priceLabel": "Setting price, $1,500 (as shown on category page; center diamond extra)",
      "originalPrice": null,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card (site checkout)",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "bn-195871",
      "name": "French Pavé (1/4 ct. tw.) — 14K Yellow Gold",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
      "solidGold": "Listing states 'Metal: 14K Yellow Gold'; description: 'French pavé-set diamonds set in 14k yellow gold'",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 1800,
      "priceLabel": "Setting price, $1,800 (center diamond extra)",
      "originalPrice": null,
      "stockNumber": "501410y14",
      "widthMm": 2.5,
      "hallmark": "Stock number shown (501410y14); hallmark photo not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card; Blue Nile credit card financing advertised on product page",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "bn-311132",
      "name": "Criss Cross Solitaire — 18K Yellow Gold (by James Allen)",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 18,
      "metalColor": "Yellow Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132",
      "solidGold": "Listing states 'Criss Cross Solitaire Engagement Ring In 18K Yellow Gold By James Allen' (setting)",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 2320,
      "priceLabel": "Setting price, $2,320 (as shown on category page; center diamond extra)",
      "originalPrice": null,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card (site checkout)",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "bn-203738",
      "name": "Floral Marquise — 18K White Gold",
      "sellerId": "bluenile",
      "category": "engagement-ring",
      "karat": 18,
      "metalColor": "White Gold",
      "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738",
      "solidGold": "Listing states 'Floral Marquise Diamond Engagement Ring in 18k White Gold' (setting)",
      "grams": null,
      "gramsNote": "Weight in grams not published on product page",
      "price": 2210,
      "priceLabel": "Setting price, $2,210 (as shown on category page; center diamond extra)",
      "originalPrice": null,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "30-day money-back guarantee; resized/engraved/custom items excluded",
      "returnUrl": "https://www.bluenile.com/policies/returns",
      "payment": "Credit card (site checkout)",
      "reviewScore": null,
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/engagement-rings"
      ]
    },
    {
      "id": "etsy-4426190660",
      "name": "2.50 CT Radiant Canary Lab-Grown Diamond, IGI Certified — 14K Yellow Gold",
      "sellerId": "etsy-rakshakjewels",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow Gold",
      "url": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
      "solidGold": "Description: 'Metal Options: Available in 10K/14K/18K Solid Gold (White, Yellow, Rose Gold) & Platinum'; '100% GENUINE, IGI CERTIFIED LAB-GROWN DIAMOND'",
      "grams": null,
      "gramsNote": "Weight in grams not published on listing page (band width 1.80 mm stated)",
      "price": 1891.78,
      "priceLabel": "14K Yellow Gold option $1,891.78 (from $1,202.08 for 925 silver; 10K $1,686.02; 18K $2,109.58); 50% off promo, original $2,404.16+",
      "originalPrice": 2404.16,
      "stockNumber": null,
      "widthMm": 1.8,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "'Returns & exchanges accepted' (Etsy tab on listing)",
      "returnUrl": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
      "payment": "Etsy checkout (card, PayPal, Klarna via Etsy); Etsy Purchase Protection applies",
      "reviewScore": "5.0 (listing page; Star Seller)",
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond"
      ]
    },
    {
      "id": "etsy-4366425533",
      "name": "Emerald Cut E/VVS2 IGI Lab-Grown, Hidden Halo — 14K Gold (0.50–3.00 CT options)",
      "sellerId": "etsy-foreverforlove",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow / White / Rose Gold",
      "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
      "solidGold": "Description: 'Made with genuine 14k real gold – never plated or filled'; 'Metal stamp: Yes'",
      "grams": null,
      "gramsNote": "Weight in grams not published on listing page (band 1.50 mm x 1.40 mm stated)",
      "price": 547.26,
      "priceLabel": "14K options $547.26–$2,410.13 by carat (0.50 CT from $547.26); listing from $376.61 (925 silver); 40% off promo, original $627.68+",
      "originalPrice": 627.68,
      "stockNumber": null,
      "widthMm": 1.5,
      "hallmark": "Seller states 'Metal stamp: Yes' (no photo shown)",
      "makerMark": null,
      "returnPolicy": "'Returns & exchanges accepted within 30 days' (Etsy tab); description: 30-day full refund/exchange, lifetime warranty on manufacturer defects",
      "returnUrl": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
      "payment": "Etsy checkout; Klarna installments advertised; ships free to US (Royal Mail)",
      "reviewScore": "5.0 (listing page; Star Seller)",
      "status": "verified",
      "flags": [
        "no-gram-weight",
        "cross-border-shipping"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown"
      ]
    },
    {
      "id": "etsy-1151446373",
      "name": "14K Solid Gold Ruby + 0.30 CT Diamond Halo Ring",
      "sellerId": "etsy-vera.by.eden",
      "category": "engagement-ring",
      "karat": 14,
      "metalColor": "Yellow / White / Rose Gold",
      "url": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
      "solidGold": "Highlights (via search snippet of listing): 'Material: Solid Gold (not gold plated or gold filled) Karat: 14 K (585)'; title '14K Solid Gold'",
      "grams": 3.7,
      "gramsNote": "'Gold grams: 3.70 gr' per listing Highlights (captured via search snippet of the listing page; confirm on live listing)",
      "price": 969.0,
      "priceLabel": "14K options $969.00 (10K $783.00; 18K $1,233.00); 25% off promo, original $1,044.00+",
      "originalPrice": 1044.0,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing (karat 585 stated in highlights)",
      "makerMark": null,
      "returnPolicy": "'Returns & exchanges accepted' (listing page)",
      "returnUrl": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
      "payment": "Etsy checkout; Etsy Purchase Protection applies",
      "reviewScore": "5.0 (listing page; Star Seller)",
      "status": "verified",
      "flags": [
        "off-platform-contact-in-listing-photos",
        "grams-from-search-snippet"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"
      ]
    },
    {
      "id": "etsy-1566052947",
      "name": "14K Solid Yellow Gold Domed Band, 2–8 mm (reference band)",
      "sellerId": "etsy-vibrantstone",
      "category": "band-reference",
      "karat": 14,
      "metalColor": "Yellow Gold",
      "url": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
      "solidGold": "Title '14k Solid Yellow Gold Domed Wedding Band'; made to order, handcrafted in Los Angeles",
      "grams": null,
      "gramsNote": "Weight in grams not published on listing page",
      "price": 251.3,
      "priceLabel": "From $251.30 (2 mm, 30% off $359.00); by width: 3 mm $363.30+, 4 mm $496.30+, 5 mm $643.30+, 6 mm $797.30+, 7 mm $944.30+, 8 mm $1,091.30–$1,742.30",
      "originalPrice": 359.0,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "Etsy Purchase Protection applies; shop return terms per Etsy tab on listing",
      "returnUrl": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
      "payment": "Etsy checkout; Etsy Purchase Protection applies",
      "reviewScore": "5.0 (listing page; Star Seller; Etsy's Pick)",
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band"
      ]
    },
    {
      "id": "etsy-1433905613",
      "name": "14K Solid Gold 8 mm Polished Comfort-Fit Dome Band (reference band)",
      "sellerId": "etsy-adelafinejewels",
      "category": "band-reference",
      "karat": 14,
      "metalColor": "White Gold",
      "url": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
      "solidGold": "Title '14K Solid Gold 8mm White Gold Polished ... Wedding Band'; 10K/14K options",
      "grams": null,
      "gramsNote": "Weight in grams not published on listing page",
      "price": 999.7,
      "priceLabel": "14K options $999.70–$1,368.90 by size (10K $674.70–$963.95); 35% off promo, original $1,038.00+",
      "originalPrice": 1038.0,
      "stockNumber": null,
      "widthMm": 8.0,
      "hallmark": "Not shown in listing (a buyer photo alt-text on page describes engraving '585 AFJ' on a similar band)",
      "makerMark": null,
      "returnPolicy": "Etsy Purchase Protection applies; shop return terms per Etsy tab on listing",
      "returnUrl": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
      "payment": "Etsy checkout; Etsy Purchase Protection applies",
      "reviewScore": "5.0 (listing page; Star Seller)",
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished"
      ]
    },
    {
      "id": "etsy-944684759",
      "name": "14K White Gold Flat Polished Band, 2–6 mm (reference band)",
      "sellerId": "etsy-cittali",
      "category": "band-reference",
      "karat": 14,
      "metalColor": "White Gold",
      "url": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
      "solidGold": "Title '14k White Gold Classic Wedding Band'; description lists '10k, 14k, 18k Solid Gold' options for this design (also made in vermeil/silver on other listings)",
      "grams": null,
      "gramsNote": "Weight in grams not published on listing page (thickness 1.10 mm stated)",
      "price": 195.75,
      "priceLabel": "From $195.75 (2 mm, 25% off $261.00); by width: 3 mm $337.50+, 4 mm $369.00+, 5 mm $429.75+, 6 mm $524.25–$1,158.75",
      "originalPrice": 261.0,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "Not shown in listing",
      "makerMark": null,
      "returnPolicy": "'Returns & exchanges accepted within 30 days' (Etsy tab)",
      "returnUrl": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
      "payment": "Etsy checkout; Klarna advertised; Etsy Purchase Protection applies",
      "reviewScore": "4.9 (item average, listing page)",
      "status": "verified",
      "flags": [
        "no-gram-weight"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished"
      ]
    },
    {
      "id": "etsy-576343849",
      "name": "14K Solid White Gold 7 g Band, Size 11 — CASE STUDY (sold out at check)",
      "sellerId": "etsy-butterflywingvintage",
      "category": "case-study",
      "karat": 14,
      "metalColor": "White Gold",
      "url": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g",
      "solidGold": "Title: 'Fine 14K Solid White Gold Ring - 7g Solid Gold - Size 11 - Comfort Fit Wedding Ring Band - Marked 14K'",
      "grams": 7.0,
      "gramsNote": "'7g Solid Gold' per listing title (page currently shows 'Sold'; price from search snippet of the listing page)",
      "price": 444.8,
      "priceLabel": "Listed price at snippet time: $444.80 (original $556.00, 20% off); page now shows Sold — retained as pricing case study",
      "originalPrice": 556.0,
      "stockNumber": null,
      "widthMm": null,
      "hallmark": "'Marked 14K' per title (no photo reviewed)",
      "makerMark": null,
      "returnPolicy": "n/a (sold out at check)",
      "returnUrl": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g",
      "payment": "n/a (sold out at check)",
      "reviewScore": "5.0 / 802 reviews (shop, listing page)",
      "status": "flagged",
      "flags": [
        "price-below-metal-value",
        "sold-at-check",
        "price-from-search-snippet"
      ],
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"
      ]
    }
  ],
  "sellers": [
    {
      "id": "bluenile",
      "name": "Blue Nile",
      "website": "https://www.bluenile.com",
      "phone": "1-800-242-2728 (US)",
      "email": "service@bluenile.com",
      "hqNote": "BBB profile lists Seattle, WA; phone (206) 336-6700; ~700 employees; BBB file opened 3/1/1999",
      "contactUrl": "https://www.bluenile.com/contact-us",
      "bbb": {
        "rating": "A+ (BBB Accredited since 3/1/1999)",
        "complaints3yr": 121,
        "complaints12mo": "22 (per BBB page snippet)",
        "bbbReviewAvg": "1/5 (25 customer reviews on BBB)",
        "url": "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564",
        "checkedOn": "2026-10-22",
        "via": "search snippets of BBB profile pages"
      },
      "otherReputation": [
        {
          "note": "ConsumerAffairs: 1.7/5 from 172 reviews (cons: order delays, inconsistent service, limited return policy)",
          "url": "https://www.consumeraffairs.com/retail/blue-nile.html",
          "checkedOn": "2026-10-22"
        },
        {
          "note": "TopConsumerReviews Oct 2026: 'VERY GOOD', notes A+ BBB and >100 complaints in 3 years",
          "url": "https://www.topconsumerreviews.com/best-jewelry-stores/reviews/blue-nile.php",
          "checkedOn": "2026-10-22"
        }
      ],
      "returnPolicy": {
        "summary": "30-day money-back guarantee (full refund/exchange, original unworn condition). Exclusions: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program, clearance, Final Sale. 2 complimentary returns/customer/year; RMA required. $150 fee if a lab grading report is lost.",
        "url": "https://www.bluenile.com/policies/returns",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Limited lifetime warranty on gold/platinum items priced $1,000+ (manufacturing defects). One free resize up/down 2 sizes within 6 months (design permitting). Excludes: <$1,000 items, silver/pearl/alternative metals, lost stones, abuse/wear, theft. Effective Oct 11, 2026.",
        "url": "https://www.bluenile.com/services/warranty",
        "checkedOn": "2026-10-22"
      },
      "payment": "Credit card at checkout; Blue Nile credit card financing advertised on product pages.",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.bluenile.com/contact-us",
        "https://www.bluenile.com/policies/returns",
        "https://www.bluenile.com/services/warranty",
        "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564"
      ]
    },
    {
      "id": "etsy",
      "name": "Etsy (marketplace)",
      "website": "https://www.etsy.com",
      "phone": null,
      "email": null,
      "hqNote": "Marketplace; individual shop sellers operate the listings",
      "contactUrl": "https://help.etsy.com/hc/en-us",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "Per-listing seller return policy (30-day tabs shown on listings checked). Etsy Purchase Protection: full refund for qualifying orders that don't arrive, arrive damaged, arrive 7+ days after the estimated delivery window, or differ significantly from the description.",
        "url": "https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Per-seller (several checked listings state lifetime warranty on manufacturer defects)",
        "url": "https://www.etsy.com/legal/buyers/",
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout (cards, PayPal, Klarna, etc.); keep orders inside the platform to keep purchase protection.",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program",
        "https://www.etsy.com/legal/buyers/"
      ]
    },
    {
      "id": "etsy-vibrantstone",
      "name": "VibrantStone (Etsy shop)",
      "website": "https://www.etsy.com/shop/VibrantStone",
      "phone": null,
      "email": null,
      "hqNote": "Handcrafted in Los Angeles (per listing description); Star Seller",
      "contactUrl": "https://www.etsy.com/shop/VibrantStone",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "Per-listing; Etsy Purchase Protection applies",
        "url": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Not stated on listing",
        "url": null,
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band"
      ]
    },
    {
      "id": "etsy-adelafinejewels",
      "name": "adelafinejewels (Etsy shop)",
      "website": "https://www.etsy.com/shop/adelafinejewels",
      "phone": null,
      "email": null,
      "hqNote": "Star Seller",
      "contactUrl": "https://www.etsy.com/shop/adelafinejewels",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "Per-listing; Etsy Purchase Protection applies",
        "url": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Not stated on listing",
        "url": null,
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished"
      ]
    },
    {
      "id": "etsy-cittali",
      "name": "CittaliFineJewelry (Etsy shop)",
      "website": "https://www.etsy.com/shop/CittaliFineJewelry",
      "phone": null,
      "email": null,
      "hqNote": "Offers brass replica home try-on; ethically sourced (Kimberley Process) per listing",
      "contactUrl": "https://www.etsy.com/shop/CittaliFineJewelry",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "Returns & exchanges accepted within 30 days (Etsy tab); buyer pays return shipping",
        "url": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Not stated on listing",
        "url": null,
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout; Klarna advertised",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished"
      ]
    },
    {
      "id": "etsy-foreverforlove",
      "name": "ForeverForLove (Etsy shop)",
      "website": "https://www.etsy.com/shop/ForeverForLove",
      "phone": null,
      "email": null,
      "hqNote": "Ships from UK (Royal Mail / UPS / USPS); Star Seller; custom design service",
      "contactUrl": "https://www.etsy.com/shop/ForeverForLove",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "30-day return/exchange per listing tab & description; buyer responsible for return shipping; duties included for US orders per listing",
        "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "'Full refund guarantee / Lifetime Warranty' per listing description (manufacturer defects; no replacement of missing center stones)",
        "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout; Klarna advertised; 'pay flexibly, ships when fully paid' per description",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown"
      ]
    },
    {
      "id": "etsy-vera.by.eden",
      "name": "VeraByEden (Etsy shop)",
      "website": "https://www.etsy.com/shop/VeraByEden",
      "phone": null,
      "email": null,
      "hqNote": "Star Seller; listing photos show a chat referencing '2355 Westwood Boulevard #153 Los Angeles CA 90082 USA' and asking buyers to share contact/address info",
      "contactUrl": "https://www.etsy.com/shop/VeraByEden",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "'Returns & exchanges accepted' (listing page)",
        "url": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Not stated on listing",
        "url": null,
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"
      ]
    },
    {
      "id": "etsy-rakshakjewels",
      "name": "RAKSHAKJEWELS (Etsy shop)",
      "website": "https://www.etsy.com/shop/RAKSHAKJEWELS",
      "phone": null,
      "email": null,
      "hqNote": "Star Seller; IGI certificates offered for center stones",
      "contactUrl": "https://www.etsy.com/shop/RAKSHAKJEWELS",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "'Returns & exchanges accepted' (Etsy tab on listing)",
        "url": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Not stated on listing",
        "url": null,
        "checkedOn": "2026-10-22"
      },
      "payment": "Etsy checkout",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond"
      ]
    },
    {
      "id": "etsy-butterflywingvintage",
      "name": "BUTTERFLYWINGVINTAGE (Etsy shop)",
      "website": "https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
      "phone": null,
      "email": null,
      "hqNote": "802 reviews, 5.0 (listing page at check time; item sold)",
      "contactUrl": "https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
      "bbb": null,
      "otherReputation": [],
      "returnPolicy": {
        "summary": "n/a (item sold out at check)",
        "url": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g",
        "checkedOn": "2026-10-22"
      },
      "warranty": {
        "summary": "Not stated",
        "url": null,
        "checkedOn": "2026-10-22"
      },
      "payment": "n/a",
      "checkedOn": "2026-10-22",
      "sources": [
        "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"
      ]
    }
  ],
  "references": [
    {
      "id": "ftc-consumer",
      "title": "FTC Consumer Advice — Buying Platinum, Gold, and Silver Jewelry",
      "url": "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
      "points": [
        "14K = 14 parts gold + 10 parts other metal",
        "Look for a maker's name/trademark next to the karat mark — 'If you don't see a trademark along with the karat mark, don't buy it'",
        "Definitions of solid gold, gold plated, gold filled, gold overlay, RGP, gold electroplate, vermeil, gold flashed",
        "Get refund/return policies in writing",
        "Report problems to ReportFraud.ftc.gov / state AG / JVC mediation"
      ],
      "checkedOn": "2026-10-22",
      "method": "direct fetch"
    },
    {
      "id": "cfr23",
      "title": "16 CFR Part 23 — Guides for the Jewelry, Precious Metals, and Pewter Industries (eCFR)",
      "url": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
      "points": [
        "§23.3 Misrepresentation as to gold content",
        "Quality-marking rules for gold karat designations"
      ],
      "checkedOn": "2026-10-22",
      "method": "search snippet (official eCFR)"
    },
    {
      "id": "cfr23-3",
      "title": "16 CFR § 23.3 (Cornell LII)",
      "url": "https://www.law.cornell.edu/cfr/text/16/23.3",
      "points": [
        "Text of the gold-content misrepresentation rule"
      ],
      "checkedOn": "2026-10-22",
      "method": "search result (official law mirror)"
    },
    {
      "id": "ftc-frn",
      "title": "FTC Federal Register notice — Jewelry Guides (PDF)",
      "url": "https://www.ftc.gov/system/files/documents/federal_register_notices/2015/12/151228jewelryguidesfrn.pdf",
      "points": [
        "Acceptable karat marking examples ('14 Karat Gold', '14 Kt. Gold')"
      ],
      "checkedOn": "2026-10-22",
      "method": "search snippet (official FTC PDF)"
    },
    {
      "id": "kitco-purity",
      "title": "Kitco — Gold Value by Purity table",
      "url": "https://www.kitco.com/charts/gold",
      "points": [
        "24K 99.99% / 22K 91.67% / 18K 75.00% / 14K 58.33% / 10K 41.67%",
        "Per-ounce values at spot (see gold price page)"
      ],
      "checkedOn": "2026-10-22",
      "method": "direct fetch"
    },
    {
      "id": "etsy-pp",
      "title": "Etsy — Purchase Protection Program (buyer)",
      "url": "https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program",
      "points": [
        "Full refund if item doesn't arrive, arrives damaged, arrives 7+ days late, or differs significantly from description"
      ],
      "checkedOn": "2026-10-22",
      "method": "search snippet (official Etsy help)"
    },
    {
      "id": "etsy-buyers",
      "title": "Etsy — Buyer Policy",
      "url": "https://www.etsy.com/legal/buyers/",
      "points": [
        "Buyer protections & case outcomes"
      ],
      "checkedOn": "2026-10-22",
      "method": "search snippet (official Etsy)"
    },
    {
      "id": "jvc",
      "title": "Jewelers Vigilance Committee — mediation services",
      "url": "https://jvclegal.org/mediation-services/",
      "points": [
        "Dispute mediation between buyers and jewelers (linked from FTC article)"
      ],
      "checkedOn": "2026-10-22",
      "method": "linked from FTC article"
    },
    {
      "id": "reportfraud",
      "title": "FTC — ReportFraud.gov",
      "url": "https://reportfraud.ftc.gov/",
      "points": [
        "Where to report jewelry purchase fraud"
      ],
      "checkedOn": "2026-10-22",
      "method": "linked from FTC article"
    }
  ],
  "flags": [
    {
      "id": "F1",
      "severity": "high",
      "title": "Price is BELOW computed gold metal value (classic fraud signal)",
      "detail": "Case study listing (etsy-576343849): 7 g '14K solid' band listed at $444.80. At the verified Kitco spot of $129.41/g (2026-10-22), 7 g × 58.33% = 4.083 g gold ≈ $528 metal value. Price = ~84% of metal value. No legitimate jeweler sells solid gold below melt. Shop had 802 reviews, yet the pattern matches known gold-jewelry scams. Item is sold out now; kept as an example.",
      "entryIds": [
        "etsy-576343849"
      ],
      "source": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g",
      "status": "open"
    },
    {
      "id": "F2",
      "severity": "high",
      "title": "VeraByEden listing photos show off-platform contact solicitation",
      "detail": "One listing photo is a chat screenshot with a map pin at '2355 Westwood Boulevard #153 Los Angeles CA 90082 USA' and text: 'Can you give me your address for delivery? ... Share your contact information with us on Etsy Message.' Moving an order off-platform bypasses Etsy Purchase Protection and card chargeback paths. Keep any order inside Etsy; treat unsolicited off-platform requests as a red flag.",
      "entryIds": [
        "etsy-1151446373"
      ],
      "source": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
      "status": "open"
    },
    {
      "id": "F3",
      "severity": "medium",
      "title": "Gram weight not published — price-vs-metal check impossible for most rows",
      "detail": "Blue Nile (7 rows) and 3 Etsy band listings do not publish gram weight on the product page. Per the project rule the cell is left blank and flagged. Action: ask the seller for weight in grams before purchase; on arrival, have an independent jeweler weigh and XRF-test.",
      "entryIds": [
        "bn-192506",
        "bn-195639",
        "bn-203257",
        "bn-195326",
        "bn-195871",
        "bn-311132",
        "bn-203738",
        "etsy-1566052947",
        "etsy-1433905613",
        "etsy-944684759",
        "etsy-4426190660",
        "etsy-4366425533"
      ],
      "source": "listing pages linked in the table",
      "status": "open"
    },
    {
      "id": "F4",
      "severity": "medium",
      "title": "Blue Nile reputation is mixed",
      "detail": "BBB: A+ accredited since 1999, but 121 complaints in 3 years (22 in last 12 months per page) and BBB customer-review average 1/5 (25 reviews). ConsumerAffairs: 1.7/5 (172 reviews) citing order delays and limited return policy. TopConsumerReviews (Oct 2026) rates 'VERY GOOD'. A reputable, real business with real contact info — but review the complaint record and buy with a credit card.",
      "entryIds": [],
      "source": "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564",
      "status": "open"
    },
    {
      "id": "F5",
      "severity": "medium",
      "title": "Blue Nile return policy excludes resized, engraved and custom items",
      "detail": "30-day money-back guarantee, BUT: 'Personalized jewelry, custom orders, engraved items, items re-sized after initial purchase, Diamond Upgrade program purchases, Clearance, and Final Sale items are not eligible.' The one free resize (within 6 months) therefore ends return eligibility — check sizing carefully (ring sizer offered).",
      "entryIds": [
        "bn-192506",
        "bn-195639",
        "bn-203257",
        "bn-195326",
        "bn-195871",
        "bn-311132",
        "bn-203738"
      ],
      "source": "https://www.bluenile.com/policies/returns",
      "status": "open"
    },
    {
      "id": "F6",
      "severity": "medium",
      "title": "VeraByEden 'Gold grams: 3.70 gr' captured via search snippet, not full-page fetch",
      "detail": "The weight appears in the listing's Highlights section as captured by the search index; our direct page fetch did not render that section. Treat 3.70 g as seller-claimed, verify on the live listing, and confirm by independent weighing.",
      "entryIds": [
        "etsy-1151446373"
      ],
      "source": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
      "status": "open"
    },
    {
      "id": "F7",
      "severity": "low",
      "title": "Gold spot price moves — same-day range across sources was $4,025–$4,087/oz",
      "detail": "Kitco (7:10 p.m. ET) $4,025.00 bid; CNBC 9 a.m. ET $4,083.82; APMEX 11:02 a.m. ET $4,077.60; Kitco news morning ~$4,086.90. All four agree within ~1.6%. Re-check the spot price the day you buy; re-run the calculator.",
      "entryIds": [],
      "source": "https://www.kitco.com/charts/gold",
      "status": "open"
    },
    {
      "id": "F8",
      "severity": "low",
      "title": "Listed prices vary by size/width/carat/metal — table shows the verified entry price",
      "detail": "Etsy listings are variable-price (size/width/center-stone options). We record the exact option prices we read (e.g., RAKSHAKJEWELS 14K YG $1,891.78; ForeverForLove 14K from $547.26 at 0.50 CT). Promo discounts were active at check time ('sale ends in ...'). Re-verify at checkout.",
      "entryIds": [
        "etsy-4426190660",
        "etsy-4366425533",
        "etsy-1151446373",
        "etsy-1566052947",
        "etsy-1433905613",
        "etsy-944684759"
      ],
      "source": "listing pages linked in the table",
      "status": "open"
    },
    {
      "id": "F9",
      "severity": "low",
      "title": "Several major retailers could not be machine-verified and were EXCLUDED (not guessed)",
      "detail": "Zales, Kay (client-side rendered — no product data in HTML), Goldspring (blocked), Clean Origins (fetch failed), Icing (redirects to Claire's — fashion jewelry, out of scope). Rather than hallucinate their prices/weights, they are excluded. If a session later can verify them, add rows with sources.",
      "entryIds": [],
      "source": "fetch attempts logged in docs/verification/sellers.md",
      "status": "open"
    },
    {
      "id": "F10",
      "severity": "info",
      "title": "Blue Nile settings are 'setting prices' — center diamond sold separately",
      "detail": "All seven Blue Nile rows are setting-only prices ($870–$2,320). The total ring price depends on the chosen center stone (0.20–8.00 ct). Not comparable to Etsy rows, which include the center stone.",
      "entryIds": [
        "bn-192506",
        "bn-195639",
        "bn-203257",
        "bn-195326",
        "bn-195871",
        "bn-311132",
        "bn-203738"
      ],
      "source": "https://www.bluenile.com/engagement-rings",
      "status": "open"
    },
    {
      "id": "F11",
      "severity": "info",
      "title": "A 14K/18K stamp alone does not prove purity",
      "detail": "Per the project checklist and FTC guidance: the stamp is a claim; the maker's mark must accompany it; final verification is independent testing (XRF) after delivery. FTC: 'If you don't see a trademark along with the karat mark, don't buy it.'",
      "entryIds": [],
      "source": "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
      "status": "open"
    },
    {
      "id": "F12",
      "severity": "info",
      "title": "A second session's site + dataset coexist in this repo (both preserved)",
      "detail": "Parallel session 638c9614 (PR #1, merged first) delivered its own verified site at /docs/ (11 listings from Brilliant Earth, Blue Nile, Allurez, Avianne, The Jewelry Master, Solid Gold Jewelers) with data/ + tools/ + verbatim evidence files. Its work was NOT discarded during the merge — it is served at https://karagemop466-tech.github.io/GOLD5/docs/ and this site is the landing page. Both sessions independently captured the same Kitco spot snapshot ($4,025.00 bid, 2026-10-22 7:10 p.m. EDT), which corroborates both datasets. Review both Flagged for Review pages.",
      "entryIds": [],
      "source": "https://github.com/karagemop466-tech/GOLD5",
      "status": "open"
    }
  ]
};
