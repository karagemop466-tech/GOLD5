# -*- coding: utf-8 -*-
"""
GOLD5 — unified dataset (single source of truth for the generated site).

NO HALLUCINATIONS RULE
----------------------
Every value below was read from the official source URL recorded next to it.
`verifyState` says how it was confirmed:
  "P2"        re-fetched live in verification pass 2 (2026-10-22, evening UTC)
  "prior"     captured from the official page earlier on 2026-10-22 by a previous
              session and NOT re-read in pass 2 (kept, labelled, and flagged)
  "unverified" not confirmable from an official source -> value is None and flagged
Nothing is estimated, inferred or filled in. Derived numbers (pure-gold grams and
metal value) are computed by tools/build_dashboard.py and recomputed by
scripts/verify.py — they are never typed in by hand.

Pass-2 fetch order is recorded in data/live_check.json (sequence numbers, not
invented clock times; the only exact times used anywhere are timestamps printed
on the source pages themselves).
"""

ASOF = "2026-10-22"
PASS = "P2"

META = {
    "project": "GOLD5 — Solid Gold Engagement Ring Research",
    "noHallucinations": (
        "NO HALLUCINATIONS. Every price, weight, karat and policy on this site was read from the "
        "official page linked next to it, on the check date shown. A value we could not confirm is "
        "left BLANK and published on the Flagged for Review page — never guessed, estimated or "
        "inferred. Derived figures (pure-gold grams, metal value, price-to-metal ratio) are computed "
        "from those raw values by script, and recomputed independently by the security check."
    ),
    "asOf": ASOF,
    "pass": PASS,
    "verifiedBy": "Arena agent sessions 37e8ff42 (pass 1) and 93032b31 (pass 2, live re-verification)",
    "verifyCommand": "python3 scripts/verify.py",
    "method": (
        "Each listing URL was opened and the price/karat/weight text on the rendered page was compared "
        "with the dataset. Where a page did not render the value in pass 2 (geo-currency or JS-rendered "
        "variant), the earlier same-day capture is retained and explicitly labelled 'prior capture' and "
        "flagged — it is never presented as re-verified."
    ),
}

# --------------------------------------------------------------------------------------
# GOLD SPOT — primary quote read live in pass 2 from Kitco's own live page.
# --------------------------------------------------------------------------------------
SPOT = {
    "primary": {
        "source": "Kitco Metals Inc. — Live Gold Price (direct page fetch)",
        "url": "https://www.kitco.com/charts/gold",
        "usdPerOz": 4026.90,
        "usdPerGram": 129.47,
        "asOf": "2026-10-22 19:26 NY Time (page footnote: 7:26 p.m. EDT)",
        "kind": "spot bid",
        "verifyState": PASS,
        "note": ("Live panel: Bid 4,026.90 / gram 129.47. The same page's summary line reads "
                 "'$4,027.50 per troy ounce as of October 22, 2026, 7:26 p.m. ET' — a 0.60 USD "
                 "internal difference on the same page (flagged F7)."),
    },
    "crossChecks": [
        {"source": "CNBC Select — gold price today", "url": "https://www.cnbc.com/select/the-price-of-gold-today-oct-22-2026/",
         "usdPerOz": 4083.82, "usdPerGram": None, "asOf": "2026-10-22 9:00 a.m. ET",
         "verifyState": "prior", "kind": "spot", "note": "'$4,083.82 per ounce' as of 9:00 a.m. ET."},
        {"source": "APMEX — gold price", "url": "https://www.apmex.com/gold-price",
         "usdPerOz": 4077.60, "usdPerGram": 131.10, "asOf": "2026-10-22 11:02 a.m. ET",
         "verifyState": "prior", "kind": "spot", "note": "'Gold Spot Price $4,077.60 ... Per Gram $131.10', last updated 10/22/2026 11:02:00 AM ET."},
        {"source": "Kitco News — AM report", "url": "https://www.kitco.com/news/article/2026-10-22/gold-silver-pressured-despite-lower-yields-hormuz-attacks-send-crude-higher",
         "usdPerOz": 4086.90, "usdPerGram": None, "asOf": "2026-10-22 morning",
         "verifyState": "prior", "kind": "spot", "note": "'spot gold was near $4,086.90 an ounce'."},
    ],
    # Kitco "Gold Value by Purity" table, read in the same pass-2 fetch as the bid above.
    "purity": {
        "source": "Kitco — Gold Value by Purity (read in the pass-2 fetch, updated 7:26 PM NY Time)",
        "url": "https://www.kitco.com/charts/gold",
        "verifyState": PASS,
        "perOunce": {"24K": 4026.90, "22K": 3691.46, "18K": 3020.18, "14K": 2348.89, "10K": 1678.01},
        "fineness": {"24K": 0.9999, "22K": 0.9167, "18K": 0.75, "14K": 0.5833, "10K": 0.4167},
        "stamp": {"24K": "999", "22K": "916 / 917", "18K": "750", "14K": "585", "10K": "417"},
    },
    "troyOzGrams": 31.1034768,
    "note": ("Spot moves continuously. This is a dated snapshot, not a live feed. Re-check kitco.com the day you buy. "
             "The calculator lets you type a newer spot price — anything you type is your input, not site data."),
}

# --------------------------------------------------------------------------------------
# SELLERS
# --------------------------------------------------------------------------------------
SELLERS = [
    {
        "id": "bluenile", "name": "Blue Nile", "type": "Established online retailer",
        "website": "https://www.bluenile.com", "phone": "1-800-242-2728", "email": "service@bluenile.com",
        "contactUrl": "https://www.bluenile.com/contact-us",
        "hq": "Seattle, WA (BBB profile); showrooms + virtual appointments",
        "payment": "Credit card; Blue Nile credit-card financing advertised on every product page checked.",
        "returns": {"summary": "30-day money-back guarantee. Excludes personalized, custom, engraved items, items re-sized after purchase, Diamond Upgrade Program, clearance and final sale.",
                    "url": "https://www.bluenile.com/policies/returns", "verifyState": "prior"},
        "warranty": {"summary": "Limited lifetime warranty on gold/platinum items with a purchase price of $1,000 or more (manufacturer's defect); one free resize within 6 months.",
                     "url": "https://www.bluenile.com/services/warranty", "verifyState": PASS},
        "reputation": [
            {"note": "BBB: A+ accredited since 3/1/1999; 121 complaints in 3 years; BBB customer reviews average 1/5 (25 reviews)",
             "url": "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564", "verifyState": "prior"},
            {"note": "ConsumerAffairs: 1.7/5 from 172 reviews (order delays, inconsistent service, limited return policy)",
             "url": "https://www.consumeraffairs.com/retail/blue-nile.html", "verifyState": "prior"},
            {"note": "TopConsumerReviews (Oct 2026): 'VERY GOOD', notes A+ BBB and >100 complaints in 3 years",
             "url": "https://www.topconsumerreviews.com/best-jewelry-stores/reviews/blue-nile.php", "verifyState": "prior"},
        ],
        "sources": ["https://www.bluenile.com/contact-us", "https://www.bluenile.com/policies/returns",
                    "https://www.bluenile.com/services/warranty"],
        "checkedOn": ASOF,
    },
    {
        "id": "brilliantearth", "name": "Brilliant Earth", "type": "Established online retailer",
        "website": "https://www.brilliantearth.com", "phone": "800.691.0952", "email": None,
        "contactUrl": "https://www.brilliantearth.com/contact/",
        "hq": "Showrooms + virtual appointments (per site navigation)",
        "payment": "Credit card; Affirm / Wells Fargo financing and layaway advertised on product pages.",
        "returns": {"summary": "'Free Shipping & Returns' stated on every product page checked; full policy page not read in pass 2.",
                    "url": "https://www.brilliantearth.com/returns/", "verifyState": "unverified"},
        "warranty": {"summary": "Free Lifetime Warranty; Lifetime Diamond Upgrade; Free 1-Year Resizing (stated on product pages).",
                     "url": "https://www.brilliantearth.com/shop-online/", "verifyState": PASS},
        "reputation": [],
        "sources": ["https://www.brilliantearth.com/contact/", "https://www.brilliantearth.com/shop-online/"],
        "checkedOn": ASOF,
    },
    {
        "id": "allurez", "name": "Allurez", "type": "Online retailer / manufacturer (made in USA)",
        "website": "https://www.allurez.com", "phone": None, "email": None,
        "contactUrl": "https://www.allurez.com/pages/contact",
        "hq": "New York, NY (per site); 'Crafted in the USA' on each product page",
        "payment": "Affirm, Klarna, Shop Pay Installments, Flex Pay, Allurez Layaway (10% down, 0% interest).",
        "returns": {"summary": "Return or exchange within 30 days if unsatisfied ('Easy Returns', product page + return-policy page).",
                    "url": "https://www.allurez.com/pages/return-policy", "verifyState": PASS},
        "warranty": {"summary": "Free 1-year limited warranty; paid extensions (2 yr / 10 yr / lifetime). Covers sizing, missing stones, prong tightening, polishing, rhodium.",
                     "url": "https://www.allurez.com/pages/warranty", "verifyState": PASS},
        "reputation": [],
        "sources": ["https://www.allurez.com/pages/contact", "https://www.allurez.com/pages/return-policy",
                    "https://www.allurez.com/pages/warranty"],
        "checkedOn": ASOF,
    },
    {
        "id": "avianne", "name": "Avianne & Co.", "type": "Retailer + NY showroom",
        "website": "https://www.avianneandco.com", "phone": "1 (332) 244-4038", "email": None,
        "contactUrl": "https://www.avianneandco.com/pages/contact",
        "hq": "28 W 47th Street, Diamond District, New York, NY (product page)",
        "payment": "Card checkout; Affirm advertised ('as low as $69/mo or 0% APR').",
        "returns": {"summary": "Returns of unworn and unaltered items accepted within 14 days (stated on the product page).",
                    "url": "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw", "verifyState": PASS},
        "warranty": {"summary": None, "url": None, "verifyState": "unverified"},
        "reputation": [],
        "sources": ["https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw"],
        "checkedOn": ASOF,
    },
    {
        "id": "jewelrymaster", "name": "The Jewelry Master (Jewelry Masters)", "type": "Online retailer",
        "website": "https://www.thejewelrymaster.com", "phone": "1-888-59-JEWEL (1-888-595-3935)", "email": None,
        "contactUrl": "https://www.thejewelrymaster.com/contact/",
        "hq": "Not stated on the page read",
        "payment": "Affirm financing advertised; standard checkout.",
        "returns": {"summary": "'Money Back Guarantee (some restrictions apply)' — return or exchange within a 30-day period, 'no questions asked' (product page).",
                    "url": "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html", "verifyState": PASS},
        "warranty": {"summary": None, "url": None, "verifyState": "unverified"},
        "reputation": [],
        "sources": ["https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html"],
        "checkedOn": ASOF,
    },
    {
        "id": "solidgoldjewelers", "name": "Solid Gold Jewelers", "type": "Independent jeweler (online + phone)",
        "website": "https://solidgoldjewelers.net", "phone": "(309) 452-1612", "email": None,
        "contactUrl": "https://solidgoldjewelers.net/contact/",
        "hq": "Illinois (309 area code; per site)",
        "payment": "Not stated on the product page.",
        "returns": {"summary": None, "url": None, "verifyState": "unverified"},
        "warranty": {"summary": None, "url": None, "verifyState": "unverified"},
        "reputation": [],
        "sources": ["https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/"],
        "checkedOn": ASOF,
    },
    {
        "id": "etsy", "name": "Etsy (marketplace)", "type": "Marketplace — each shop is an independent seller",
        "website": "https://www.etsy.com", "phone": None, "email": None,
        "contactUrl": "https://help.etsy.com/hc/en-us",
        "hq": "Marketplace; shops ship from their own locations (shown on each listing)",
        "payment": "Etsy checkout (cards, PayPal, Klarna). Keep the order on Etsy to keep Purchase Protection.",
        "returns": {"summary": "Per-listing seller policy (7 / 14 / 21 / 30 days observed — check each listing). Etsy Purchase Protection covers non-delivery, damage, 7+ days late, or significant mismatch.",
                    "url": "https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program", "verifyState": "prior"},
        "warranty": {"summary": "Per-seller; several listings state a lifetime warranty on manufacturing defects.", "url": "https://www.etsy.com/legal/buyers/", "verifyState": "prior"},
        "reputation": [],
        "sources": ["https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program", "https://www.etsy.com/legal/buyers/"],
        "checkedOn": ASOF,
    },
    {"id": "etsy-rakshak", "name": "RAKSHAKJEWELS (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/RAKSHAKJEWELS",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/RAKSHAKJEWELS",
     "hq": "Surat, India; ships from India. Star Seller. Shop rating 5.0 (16 reviews), 56 sales, 10 months on Etsy (listing page, pass 2).",
     "payment": "Etsy checkout.", "returns": {"summary": "Returns & exchanges accepted within 14 days; buyer pays return shipping (listing page).",
     "url": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond", "verifyState": PASS},
     "warranty": {"summary": None, "url": None, "verifyState": "unverified"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond"], "checkedOn": ASOF},
    {"id": "etsy-foreverforlove", "name": "ForeverForLove (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/ForeverForLove",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/ForeverForLove",
     "hq": "United Kingdom; ships via Royal Mail / UPS / USPS. Star Seller (listing page, pass 2).",
     "payment": "Etsy checkout; Klarna advertised.", "returns": {"summary": "30-day return/exchange per listing tab and description; buyer pays return shipping.",
     "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown", "verifyState": "prior"},
     "warranty": {"summary": "'Lifetime Warranty' on manufacturer defects per listing description; no replacement of lost center stones.",
     "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown", "verifyState": "prior"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown"], "checkedOn": ASOF},
    {"id": "etsy-vera", "name": "VeraByEden (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/VeraByEden",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/VeraByEden",
     "hq": "Ships from Albany, NY; production partner Vera Atolye, Istanbul, Türkiye (listing page, pass 2). Star Seller.",
     "payment": "Etsy checkout; Klarna advertised.", "returns": {"summary": "Returns & exchanges accepted within 7 days; buyer pays return shipping (listing page, pass 2).",
     "url": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant", "verifyState": PASS},
     "warranty": {"summary": None, "url": None, "verifyState": "unverified"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"], "checkedOn": ASOF},
    {"id": "etsy-vibrant", "name": "VibrantStone (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/VibrantStone",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/VibrantStone",
     "hq": "Handcrafted in Los Angeles, CA; ships from Los Angeles (listing page, pass 2). Star Seller; Etsy's Pick.",
     "payment": "Etsy checkout; Klarna advertised.", "returns": {"summary": "Returns & exchanges accepted within 21 days; buyer pays return shipping; up to 30% restocking fee on altered/used items; exchanged items no longer returnable (listing page, pass 2).",
     "url": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band", "verifyState": PASS},
     "warranty": {"summary": None, "url": None, "verifyState": "unverified"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band"], "checkedOn": ASOF},
    {"id": "etsy-adela", "name": "adelafinejewels (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/adelafinejewels",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/adelafinejewels", "hq": "Star Seller (prior capture).",
     "payment": "Etsy checkout.", "returns": {"summary": "Per-listing seller policy (not re-read in pass 2).",
     "url": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished", "verifyState": "prior"},
     "warranty": {"summary": None, "url": None, "verifyState": "unverified"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished"], "checkedOn": ASOF},
    {"id": "etsy-cittali", "name": "CittaliFineJewelry (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/CittaliFineJewelry",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/CittaliFineJewelry",
     "hq": "Offers brass replica home try-on (prior capture).",
     "payment": "Etsy checkout; Klarna advertised.", "returns": {"summary": "Returns & exchanges accepted within 30 days (Etsy tab, prior capture).",
     "url": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished", "verifyState": "prior"},
     "warranty": {"summary": None, "url": None, "verifyState": "unverified"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished"], "checkedOn": ASOF},
    {"id": "etsy-butterfly", "name": "BUTTERFLYWINGVINTAGE (Etsy shop)", "type": "Etsy shop", "website": "https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
     "phone": None, "email": None, "contactUrl": "https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
     "hq": "Shop 5.0 with 802 reviews (prior capture). The case-study listing is no longer available (pass 2).",
     "payment": "n/a — item unavailable.", "returns": {"summary": "n/a — item unavailable at pass 2.", "url": None, "verifyState": PASS},
     "warranty": {"summary": None, "url": None, "verifyState": "unverified"}, "reputation": [],
     "sources": ["https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"], "checkedOn": ASOF},
]

# --------------------------------------------------------------------------------------
# LISTINGS — every row carries its official URL. `verifyState` per row.
# --------------------------------------------------------------------------------------
LISTINGS = [
    # ---------------- Blue Nile: all re-fetched live in pass 2 ----------------
    dict(id="bn-192506", name="Petite Hidden Halo Solitaire Plus Diamond Engagement Ring", sellerId="bluenile",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
         price=1255, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 502250y14 shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=1.6, stockNumber="502250y14", centerStone="Sold separately (0.20–8.00 ct)",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="bn-195639", name="Petite Solitaire Engagement Ring", sellerId="bluenile",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639",
         price=1000, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 501130y14 shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=1.8, stockNumber="501130y14", centerStone="Sold separately (0.20–8.00 ct)",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="bn-203257", name="Classic Four Prong Solitaire Engagement Ring", sellerId="bluenile",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
         price=870, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 500000y14 shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=1.9, stockNumber="500000y14", centerStone="Sold separately (0.20–8.00 ct)",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="bn-195326", name="Riviera Pavé Diamond Engagement Ring, 1/6 ct. tw.", sellerId="bluenile",
         category="engagement-ring", karat=14, metalColor="White Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326",
         price=1500, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 501590w14 shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=2.0, stockNumber="501590w14", centerStone="Sold separately (0.20–8.00 ct); 18 pavé diamonds 1/6 ct tw",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="bn-195871", name="French Pavé Diamond Engagement Ring, 1/4 ct. tw.", sellerId="bluenile",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
         price=1800, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 501410y14 shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=2.5, stockNumber="501410y14", centerStone="Sold separately (0.20–8.00 ct); 16 pavé diamonds 1/4 ct tw",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="bn-311132", name="Criss Cross Solitaire Engagement Ring by James Allen", sellerId="bluenile",
         category="engagement-ring", karat=18, metalColor="Yellow Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132",
         price=2320, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 505032y shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=8.45, stockNumber="505032y", centerStone="Sold separately (0.10–8.00 ct)",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="bn-203738", name="Floral Marquise Diamond Engagement Ring", sellerId="bluenile",
         category="engagement-ring", karat=18, metalColor="White Gold",
         url="https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738",
         price=2210, priceLabel="Setting price", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Stock number 502820w shown; hallmark/maker's-mark photo not shown in listing",
         returns="30-day money-back guarantee; resized/engraved/custom excluded", returnsUrl="https://www.bluenile.com/policies/returns",
         payment="Credit card; Blue Nile credit card financing advertised",
         widthMm=1.7, stockNumber="502820w", centerStone="Sold separately (0.20–8.00 ct)",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only", "metal-text-contradiction"]),

    # ---------------- Brilliant Earth ----------------
    dict(id="be-freesia-2mm", name="Freesia 2mm Solitaire Ring (BE1343-14KY)", sellerId="brilliantearth",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
         price=750, priceLabel="Setting only (center stone sold separately)", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Style number BE1343-14KY shown; hallmark photo not shown",
         returns="Free shipping & returns (policy page not read in pass 2)", returnsUrl="https://www.brilliantearth.com/returns/",
         payment="Credit card; Affirm / Wells Fargo financing and layaway advertised",
         widthMm=2.0, stockNumber="BE1343-14KY", centerStone="Sold separately", reviews="80 reviews on listing",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="be-nadia", name="Nadia Diamond Ring (BE1D6013-14KY)", sellerId="brilliantearth",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/",
         price=1250, priceLabel="Setting only (center stone sold separately)", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Style number BE1D6013-14KY shown; hallmark photo not shown",
         returns="Free shipping & returns (policy page not read in pass 2)", returnsUrl="https://www.brilliantearth.com/returns/",
         payment="Credit card; Affirm / Wells Fargo financing and layaway advertised",
         widthMm=1.8, stockNumber="BE1D6013-14KY", centerStone="Sold separately", reviews="5.0 (143 reviews)",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"],
         note="Earlier capture had no karat for this row; pass 2 confirmed 14K Yellow Gold and 1.8 mm width on the product page."),
    dict(id="be-freesia-hidden", name="Freesia Hidden Halo Diamond Ring (BE1D3939-14KY)", sellerId="brilliantearth",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/",
         price=1190, priceLabel="Setting only (center stone sold separately)", priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Style number BE1D3939-14KY shown; hallmark photo not shown",
         returns="Free shipping & returns (policy page not read in pass 2)", returnsUrl="https://www.brilliantearth.com/returns/",
         payment="Credit card; Affirm / Wells Fargo financing and layaway advertised",
         widthMm=2.0, stockNumber="BE1D3939-14KY", centerStone="Sold separately", reviews="31 reviews on listing",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only"]),
    dict(id="be-secret-halo-15", name="Secret Halo 1.5mm Diamond Ring (BE1D13065-14KY)", sellerId="brilliantearth",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/",
         price=None, priceLabel="Pass 2: page rendered in EUR (€1,250.00, setting only). USD price NOT confirmed — left blank.",
         priceBasis="setting-only",
         grams=None, gramsNote="Weight in grams is not published on the product page.",
         solid=None, hallmark="Style number BE1D13065-14KY shown; hallmark photo not shown",
         returns="Free shipping & returns (policy page not read in pass 2)", returnsUrl="https://www.brilliantearth.com/returns/",
         payment="Credit card; Affirm / Wells Fargo financing and layaway advertised",
         widthMm=1.5, stockNumber="BE1D13065-14KY", centerStone="Sold separately", reviews="92 reviews on listing",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "setting-only", "usd-price-unverified"],
         note="An earlier same-day capture recorded $1,090; the pass-2 fetch was geo-priced in EUR, so the USD figure is not restated here."),

    # ---------------- Allurez ----------------
    dict(id="al-u5882", name="Filigree Designed Solitaire Engagement Ring Setting (U5882)", sellerId="allurez",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold",
         price=1085, priceLabel="Setting only; center stone sold separately", priceBasis="setting-only",
         grams=5.00, gramsNote="'Gold Weight 5.00 Grams (Approximate)' — seller-stated, not independently weighed.",
         solid=None, hallmark="Style number U5882 shown; hallmark/maker's mark not shown",
         returns="Return or exchange within 30 days", returnsUrl="https://www.allurez.com/pages/return-policy",
         payment="Affirm, Klarna, Shop Pay, Flex Pay, layaway",
         widthMm=2.9, stockNumber="U5882", centerStone="Sold separately",
         verifyState=PASS, flags=["hallmark-not-shown", "setting-only", "seller-stated-weight"]),
    dict(id="al-u170", name="Antique Engraved Solitaire Engagement Ring Setting (U170)", sellerId="allurez",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold",
         price=933, priceLabel="Setting only; center stone sold separately", priceBasis="setting-only",
         grams=4.80, gramsNote="'Gold Weight 4.80 grams (Approximate)' — seller-stated, not independently weighed.",
         solid=None, hallmark="Style number U170 shown; hallmark/maker's mark not shown",
         returns="Return or exchange within 30 days", returnsUrl="https://www.allurez.com/pages/return-policy",
         payment="Affirm, Klarna, Shop Pay, Flex Pay, layaway",
         widthMm=3.2, stockNumber="U170", centerStone="Sold separately",
         verifyState=PASS, flags=["hallmark-not-shown", "setting-only", "seller-stated-weight"]),
    dict(id="al-ng4426", name="Engraved Floral Solitaire Engagement Ring Setting (NG4426)", sellerId="allurez",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold",
         price=585, priceLabel="Setting only; center stone sold separately", priceBasis="setting-only",
         grams=3.58, gramsNote="'Approximate Metal Weight 3.58 grams' — seller-stated, not independently weighed.",
         solid=None, hallmark="Style number NG4426 shown; hallmark/maker's mark not shown",
         returns="Return or exchange within 30 days", returnsUrl="https://www.allurez.com/pages/return-policy",
         payment="Affirm, Klarna, Shop Pay, Flex Pay, layaway",
         widthMm=None, stockNumber="NG4426", centerStone="Sold separately",
         verifyState=PASS, flags=["hallmark-not-shown", "setting-only", "seller-stated-weight"]),

    # ---------------- Avianne ----------------
    dict(id="av-r25893", name="14K Solid Yellow Gold Diamond Solitaire Engagement Ring, 0.41 Ctw (R25893)", sellerId="avianne",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
         price=1100.00, priceLabel="Complete ring, 0.41 ct center diamond included", priceBasis="complete",
         grams=2.3, gramsNote="'Item Weight 2.3 grams' + description 'weighs 2.3 grams' — seller-stated.",
         solid="Title '14K Solid Yellow Gold'; description 'handcrafted in 14k yellow gold'",
         hallmark=None, hallmarkNote="No hallmark or maker's mark shown in the listing details",
         returns="Returns of unworn and unaltered items accepted within 14 days", returnsUrl="https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
         payment="Card checkout; Affirm advertised",
         widthMm=4.5, stockNumber="R25893", centerStone="Included: 0.41 ct, VS2, G/H",
         verifyState=PASS, flags=["hallmark-not-shown", "seller-stated-weight", "short-return-window"]),

    # ---------------- The Jewelry Master ----------------
    dict(id="jm-149700", name="Brilliant Round Diamond Solitaire Engagement Ring, 0.71 ctw (Style 149700)", sellerId="jewelrymaster",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
         price=3020.00, priceLabel="'Special Price' (page also shows 'Retail Price $6,041.00' — retail not used)", priceBasis="complete",
         grams=2.3, gramsNote="'Metal Weight: 2.3 Grams' — seller-stated.",
         solid="Description: 'entirely handcrafted in pure 14KT solid yellow gold'",
         hallmark=None, hallmarkNote="No hallmark or maker's mark shown in the listing details",
         returns="30-day money-back guarantee (some restrictions apply)", returnsUrl="https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
         payment="Standard checkout; Affirm advertised",
         widthMm=None, stockNumber="149700", centerStone="Included: 0.71 ctw, SI1, G-H",
         verifyState=PASS, flags=["hallmark-not-shown", "seller-stated-weight", "retail-vs-sale-price"]),

    # ---------------- Solid Gold Jewelers ----------------
    dict(id="sgj-b02561", name="Yellow Gold Solitaire Engagement Ring (SKU B02561, brand M Michael)", sellerId="solidgoldjewelers",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
         price=None, priceLabel="No price on page: 'Call (309) 452-1612 for current pricing and availability.'", priceBasis="unpriced",
         grams=4.7, gramsNote="'14ky, 4.7g, #B02561' — seller-stated.",
         solid=None, hallmark=None, hallmarkNote="SKU #B02561 shown; no hallmark photo",
         returns=None, returnsUrl=None, payment="Not stated on the product page",
         widthMm=None, stockNumber="B02561", centerStone="Not stated",
         verifyState=PASS, flags=["no-price", "hallmark-not-shown", "seller-stated-weight", "returns-unstated"]),

    # ---------------- Etsy ----------------
    dict(id="etsy-4426190660", name="2.50 CT Radiant Canary Lab-Grown Diamond, IGI Certified — 14K Yellow Gold", sellerId="etsy-rakshak",
         category="engagement-ring", karat=14, metalColor="Yellow Gold",
         url="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
         price=1891.78, priceLabel="14K Yellow Gold option (base 925 silver $1,202.08; 10K $1,686.02; 18K $2,109.58; was $2,404.16, 50% off)", priceBasis="complete",
         grams=None, gramsNote="No gram weight published; band 1.80 mm x 1.60 mm stated.",
         solid="'Metal Options: Available in 10K/14K/18K Solid Gold (White, Yellow, Rose Gold) & Platinum'",
         hallmark=None, hallmarkNote="No hallmark photo; IGI certificate offered for the center stone",
         returns="Returns & exchanges accepted within 14 days; buyer pays return shipping", returnsUrl="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies",
         widthMm=1.8, stockNumber=None, centerStone="Included: 2.50 ct IGI lab-grown + 0.32 ctw sides",
         reviews="Shop 5.0 (16 reviews), 56 sales, 10 months on Etsy; no reviews on this item yet",
         verifyState=PASS, flags=["no-gram-weight", "hallmark-not-shown", "sale-price-expires", "ships-from-india"]),
    dict(id="etsy-4366425533", name="Emerald Cut E/VVS2 IGI Lab-Grown Hidden Halo — 14K Gold", sellerId="etsy-foreverforlove",
         category="engagement-ring", karat=14, metalColor="Yellow / White / Rose Gold",
         url="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
         price=547.26, priceLabel="14K options from $547.26 (base 925 silver $376.61, was $627.68, 40% off; sale ends ~1 day)", priceBasis="variant-from",
         grams=None, gramsNote="No gram weight published; band 1.50 x 1.40 mm stated.",
         solid="Description: 'Made with genuine 14k real gold – never plated or filled'; 'Metal stamp: Yes'",
         hallmark="Seller states 'Metal stamp: Yes' (no photo shown)", hallmarkNote=None,
         returns="Returns & exchanges accepted within 30 days; buyer pays return shipping", returnsUrl="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies",
         widthMm=1.5, stockNumber=None, centerStone="Included by carat option (0.50–3.00 CT)",
         reviews="Star Seller",
         verifyState=PASS, flags=["no-gram-weight", "variant-price", "sale-price-expires", "cross-border-shipping"],
         note="Base (silver) price, original price and 40% discount were re-read in pass 2. The 14K variant figure is an earlier same-day capture and is labelled 'prior'."),
    dict(id="etsy-1151446373", name="14K Solid Gold Ruby + 0.30 ct Diamond Halo Ring", sellerId="etsy-vera",
         category="engagement-ring", karat=14, metalColor="Yellow / White / Rose Gold",
         url="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
         price=969.00, priceLabel="14K option $969.00 (10K $783.00; 18K $1,233.00; was $1,044.00, 25% off) — prior capture", priceBasis="variant-from",
         grams=3.70, gramsNote="'Gold grams: 3.70 gr' in the listing description (re-read in pass 2).",
         solid="'Material: Solid Gold (not gold plated or gold filled)'; 'Karat: 14 K (585)'",
         hallmark=None, hallmarkNote="No hallmark photo; karat stated as 585 in the description",
         returns="Returns & exchanges accepted within 7 days; buyer pays return shipping", returnsUrl="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies",
         widthMm=None, stockNumber=None, centerStone="Included: 0.30 ct diamonds + 0.90 ct ruby",
         reviews="Star Seller",
         verifyState=PASS, flags=["hallmark-not-shown", "seller-stated-weight", "short-return-window", "sale-price-expires"],
         note="Karat, solid-gold statement, 3.70 g weight and the 7-day return window were re-read in pass 2; the price is an earlier same-day capture (labelled 'prior')."),
    dict(id="etsy-1566052947", name="14K Solid Yellow Gold Domed Band, 2–8 mm (reference band)", sellerId="etsy-vibrant",
         category="band", karat=14, metalColor="Yellow Gold",
         url="https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
         price=251.30, priceLabel="2 mm size 3, now $251.30 (was $359.00, 30% off); 8 mm up to $1,742.30", priceBasis="variant-from",
         grams=None, gramsNote="No gram weight published for any width.",
         solid="Title '14k Solid Yellow Gold'; description '14k Solid Gold Classic Domed Wedding Bands'",
         hallmark=None, hallmarkNote="No hallmark photo shown",
         returns="Returns & exchanges accepted within 21 days; up to 30% restocking fee on altered/used items", returnsUrl="https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies",
         widthMm=2.0, stockNumber=None, centerStone="n/a (plain band)",
         reviews="Star Seller; Etsy's Pick; 5.0",
         verifyState=PASS, flags=["no-gram-weight", "variant-price", "sale-price-expires", "restocking-fee"]),
    dict(id="etsy-1433905613", name="14K Solid Gold 8 mm Polished Comfort-Fit Dome Band (reference band)", sellerId="etsy-adela",
         category="band", karat=14, metalColor="White Gold",
         url="https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
         price=999.70, priceLabel="14K options $999.70–$1,368.90 by size (10K $674.70–$963.95; was $1,038.00, 35% off) — prior capture", priceBasis="variant-from",
         grams=None, gramsNote="No gram weight published.",
         solid="Title '14K Solid Gold'; 10K/14K options",
         hallmark=None, hallmarkNote="No hallmark photo; a buyer photo describes engraving '585 AFJ' on a similar band",
         returns="Per-listing seller policy (not re-read in pass 2)", returnsUrl="https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
         payment="Etsy checkout; Etsy Purchase Protection applies",
         widthMm=8.0, stockNumber=None, centerStone="n/a (plain band)",
         reviews="Star Seller (prior capture)",
         verifyState="prior", flags=["no-gram-weight", "variant-price", "sale-price-expires", "prior-capture"]),
    dict(id="etsy-944684759", name="14K White Gold Flat Polished Band, 2–6 mm (reference band)", sellerId="etsy-cittali",
         category="band", karat=14, metalColor="White Gold",
         url="https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
         price=195.75, priceLabel="From $195.75 (2 mm, 25% off $261.00) — prior capture", priceBasis="variant-from",
         grams=None, gramsNote="No gram weight published; thickness 1.10 mm stated.",
         solid="Description lists '10k, 14k, 18k Solid Gold' options for this design",
         hallmark=None, hallmarkNote="No hallmark photo shown",
         returns="Returns & exchanges accepted within 30 days (prior capture)", returnsUrl="https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies",
         widthMm=2.0, stockNumber=None, centerStone="n/a (plain band)",
         reviews="4.9 item rating (prior capture)",
         verifyState="prior", flags=["no-gram-weight", "variant-price", "prior-capture"]),
    dict(id="etsy-576343849", name="14K Solid White Gold 7 g Band, Size 11 — CASE STUDY (no longer available)", sellerId="etsy-butterfly",
         category="case-study", karat=14, metalColor="White Gold",
         url="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g",
         price=444.80, priceLabel="Price from a search snippet ($444.80, was $556.00); listing no longer available in pass 2", priceBasis="complete",
         grams=7.0, gramsNote="'7g Solid Gold' in the listing title — seller-stated.",
         solid="Title: 'Fine 14K Solid White Gold Ring - 7g Solid Gold ... Marked 14K'",
         hallmark="'Marked 14K' in title (no photo reviewed)", hallmarkNote=None,
         returns=None, returnsUrl=None, payment="n/a — item unavailable",
         widthMm=None, stockNumber=None, centerStone="n/a",
         reviews="Shop 5.0, 802 reviews (prior capture)",
         verifyState=PASS, flags=["price-below-metal-value", "sold-at-check", "price-from-search-snippet", "hallmark-not-shown"]),
]

# --------------------------------------------------------------------------------------
# FLAGS — irregularities. Every flag links the page where the finding was observed.
# --------------------------------------------------------------------------------------
FLAGS = [
    dict(id="F1", severity="high", title="Price is BELOW the computed gold metal value (classic fraud signal)",
         detail=("Case study etsy-576343849: a 7 g '14K solid' band listed at $444.80. At the verified pass-2 Kitco spot, "
                 "7 g x 58.33% = 4.083 g of pure gold, which at the verified spot is worth more than the asking price. The price is ~84% of melt value. No legitimate "
                 "jeweler sells solid gold below melt. The listing is now unavailable — retained as an example of the check."),
         entries=["etsy-576343849"], source="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"),
    dict(id="F2", severity="high", title="VeraByEden listing photos show off-platform contact solicitation",
         detail=("One listing photo is a chat screenshot asking the buyer to 'Share your contact information with us on Etsy Message' "
                 "with a map pin in Los Angeles. Moving an order off-platform removes Etsy Purchase Protection and weakens card "
                 "chargeback evidence. Keep the order inside Etsy; treat unsolicited off-platform requests as a red flag."),
         entries=["etsy-1151446373"], source="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"),
    dict(id="F3", severity="medium", title="Gram weight is not published for most listings",
         detail=("16 of the 24 listings do not publish a gram weight, so the price-vs-metal test cannot be computed for them. "
                 "Per project rule the cell is left blank. Action: ask the seller for the weight in grams in writing before "
                 "purchase, then have an independent jeweler weigh and XRF-test the ring on arrival."),
         entries=[], source="listing pages linked in the Listings table"),
    dict(id="F4", severity="medium", title="Blue Nile's reputation is mixed — check the complaint record yourself",
         detail=("BBB: A+ accredited since 1999, but 121 complaints in 3 years and a 1/5 customer-review average (25 reviews). "
                 "ConsumerAffairs: 1.7/5 from 172 reviews citing delays and a limited return policy. TopConsumerReviews (Oct 2026) "
                 "rates it 'VERY GOOD'. A real business with real contact details — buy with a credit card and keep the 30-day window."),
         entries=[], source="https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564"),
    dict(id="F5", severity="medium", title="Blue Nile returns exclude resized, engraved and custom items",
         detail=("30-day money-back guarantee, BUT personalized, custom and engraved items, items re-sized after purchase, "
                 "Diamond Upgrade Program purchases, clearance and final-sale items are not eligible. The free resize therefore "
                 "ends return eligibility — confirm the ring size before ordering."),
         entries=[], source="https://www.bluenile.com/policies/returns"),
    dict(id="F6", severity="low", title="VeraByEden gold weight is seller-stated only",
         detail=("'Gold grams: 3.70 gr' is in the seller's description (re-read in pass 2). It is the seller's claim, not an "
                 "independent measurement. Weigh and XRF-test on arrival."),
         entries=["etsy-1151446373"], source="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"),
    dict(id="F7", severity="low", title="Spot price moves all day — the page itself shows two figures",
         detail=("At the pass-2 read the Kitco live panel showed a 4,026.90 bid while the same page's summary sentence said "
                 "$4,027.50 (7:26 p.m. ET). Earlier same-day quotes ranged 4,025.00-4,086.90. Re-check the spot the day you buy "
                 "and re-run the calculator."),
         entries=[], source="https://www.kitco.com/charts/gold"),
    dict(id="F8", severity="low", title="Etsy prices are variant prices and the promos expire",
         detail=("Etsy listings price by width / ring size / metal / center-stone carat, and the discounts are time-limited "
                 "(observed at pass 2: 'sale ends in 19:00:07', 'sale ends in 1 day', 'sale ends in 3 days'). The table records "
                 "the exact option read, at the time read. Re-check at checkout."),
         entries=["etsy-4426190660", "etsy-4366425533", "etsy-1151446373", "etsy-1566052947", "etsy-1433905613", "etsy-944684759"],
         source="listing pages linked in the Listings table"),
    dict(id="F9", severity="low", title="Retailers we could not verify were EXCLUDED, not guessed",
         detail=("Zales and Kay serve client-side-rendered pages with no product data in the HTML, Goldspring blocked the fetch, "
                 "Clean Origins failed, and Icing redirects to Claire's (fashion jewelry, out of scope). No prices or weights were "
                 "invented for them; they are simply absent."),
         entries=[], source="fetch log in data/live_check.json"),
    dict(id="F10", severity="info", title="Setting-only prices are not comparable to complete-ring prices",
         detail=("All 7 Blue Nile rows, all 3 Allurez rows and all 4 Brilliant Earth rows are SETTING prices — the center "
                 "diamond is sold separately (Blue Nile lists 0.20-8.00 ct compatible stones). Etsy, Avianne and Jewelry Master rows "
                 "include the center stone. Compare accordingly."),
         entries=[], source="https://www.bluenile.com/engagement-rings"),
    dict(id="F11", severity="info", title="A 14K/18K stamp alone does not prove purity",
         detail=("FTC: 'Near the karat quality mark, look for the name or the U.S. registered trademark of the company that will "
                 "stand behind the mark... If you're thinking about buying a piece of gold jewelry but don't see a trademark along "
                 "with the karat mark, don't buy it.' The stamp is a claim; independent testing (XRF) after delivery is the proof."),
         entries=[], source="https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry"),
    dict(id="F12", severity="info", title="Earlier sessions' work is preserved as archives (nothing deleted)",
         detail=("Three parallel sessions delivered to this repo. Their sites are kept byte-for-byte and linked from the Archive "
                 "page: /docs/ (11 verified listings + verbatim evidence files + its own checker), /pages/ + index-090bae73.html "
                 "(13-page checklist guide), and /guide/ (checklist site from PR #4, 13 pages + research notes). This dashboard "
                 "is the single integrated view; the archives are for traceability."),
         entries=[], source="https://github.com/karagemop466-tech/GOLD5"),
    dict(id="F13", severity="medium", title="Blue Nile 18K ring page contradicts itself on the metal",
         detail=("The Floral Marquise product page is titled 'in 18k White Gold' and its specification block says 'Metal 18K White "
                 "Gold / Stock Number 502820w', but the Product Details paragraph says the ring is 'crafted from warmly lustrous 14k "
                 "yellow gold'. We record the specification (18K White Gold) because it matches the title and stock number, and flag "
                 "the contradiction. Ask the seller in writing before buying."),
         entries=["bn-203738"], source="https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738"),
    dict(id="F14", severity="medium", title="Brilliant Earth Secret Halo page served a EUR price at re-check",
         detail=("The pass-2 fetch of the Secret Halo 1.5mm page rendered 'EUR 1,250.00 (Setting Only)' with a European currency "
                 "selector active, even though the URL is the US 14K yellow gold product. The USD price could not be confirmed, so "
                 "the USD cell is blank. An earlier same-day capture recorded $1,090 — not restated as verified. Re-open with a US "
                 "session and record the USD price before buying."),
         entries=["be-secret-halo-15"], source="https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/"),
    dict(id="F15", severity="medium", title="Etsy return windows vary per listing — 7, 14, 21 and 30 days observed",
         detail=("Pass 2 read the actual windows: VeraByEden 7 days, RAKSHAKJEWELS 14 days, VibrantStone 21 days, Cittali 30 days "
                 "(prior). A short window can expire before an independent jeweler sees the ring. Check the tab on the exact listing "
                 "before paying, and get the policy in writing."),
         entries=["etsy-1151446373", "etsy-4426190660", "etsy-1566052947", "etsy-944684759"],
         source="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"),
    dict(id="F16", severity="low", title="RAKSHAKJEWELS listing has no item reviews (shop rating is not the item rating)",
         detail=("Pass 2 shows 'Be the first to review this item' for listing 4426190660; the 5.0 rating belongs to the shop "
                 "(16 reviews, 56 sales, 10 months on Etsy). Do not read a shop rating as a product rating."),
         entries=["etsy-4426190660"], source="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond"),
    dict(id="F17", severity="low", title="The 7 g case-study listing is now unavailable (sold)",
         detail=("Pass 2 re-fetched the URL: Etsy serves the 'unavailable listing' page with recommendation tiles. The $444.80 price "
                 "therefore remains a search-snippet value and is labelled as such; the below-melt finding (F1) still illustrates "
                 "the test."),
         entries=["etsy-576343849"], source="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"),
    dict(id="F18", severity="low", title="Several policy pages are earlier same-day captures, not re-read in pass 2",
         detail=("Blue Nile's detailed return exclusions, ForeverForLove's 30-day terms, Cittali's and adela's listing policies, and "
                 "the Etsy Purchase Protection text were captured earlier on 2026-10-22 and are labelled 'prior capture'. They are "
                 "not presented as re-verified. Sellers can change policies — re-read the page before buying."),
         entries=[], source="https://www.bluenile.com/policies/returns"),
    dict(id="F19", severity="info", title="Seller-stated weights are claims, not measurements",
         detail=("Allurez, Avianne, Jewelry Master, Solid Gold Jewelers and VeraByEden publish gram weights in the listing. Those are "
                 "the sellers' own figures. The only proof of weight and purity is an independent jeweler's scale and XRF test after "
                 "delivery, before wearing or resizing."),
         entries=["al-u5882", "al-u170", "al-ng4426", "av-r25893", "jm-149700", "sgj-b02561", "etsy-1151446373"],
         source="listing pages linked in the Listings table"),
]

# --------------------------------------------------------------------------------------
# REFERENCES — official guidance used by the checklist.
# --------------------------------------------------------------------------------------
REFERENCES = [
    dict(id="ftc-consumer", title="FTC Consumer Advice — Buying Platinum, Gold, and Silver Jewelry",
         url="https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry", verifyState=PASS,
         what=("Karat system (18K = 18 parts gold + 6 parts other metal; 14K = 14 parts + 10 parts); 'solid gold' means the item "
               "isn't hollow; the trademark rule ('If you don't see a trademark along with the karat mark, don't buy it'); "
               "definitions of gold plated, gold filled, gold overlay, RGP, gold electroplate, vermeil, gold flashed; get refund and "
               "return policies in writing; where to report problems (ReportFraud.ftc.gov, state AG, JVC mediation).")),
    dict(id="cfr23", title="16 CFR Part 23 — Guides for the Jewelry, Precious Metals, and Pewter Industries (eCFR)",
         url="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23", verifyState="prior",
         what="The regulation behind the FTC jewelry guides, including gold-content misrepresentation rules and quality marking."),
    dict(id="cfr23-3", title="16 CFR § 23.3 — Misrepresentation as to gold content (Cornell LII)",
         url="https://www.law.cornell.edu/cfr/text/16/23.3", verifyState="prior",
         what="Text of the rule on misrepresenting the gold content of an industry product."),
    dict(id="cfr23-10", title="16 CFR § 23.10 — Marking requirements (National Stamping Act reference)",
         url="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.10", verifyState="prior",
         what="Quality-mark rules, including the requirement that a quality mark be accompanied by the maker's mark or trademark."),
    dict(id="nist", title="NIST — Precious Metals Conversion Information",
         url="https://www.nist.gov/document/precious-metals-conversion-information-march2015pdf", verifyState="prior",
         what="Unit conversions used here: 1 troy ounce = 31.1034768 grams; 1 pennyweight = 1.55517384 g."),
    dict(id="lbma", title="LBMA — Gold price benchmark",
         url="https://www.lbma.org.uk/prices-and-data/lbma-gold-price", verifyState="prior",
         what="The London benchmark price; an independent reference alongside the Kitco dealer quote used for the calculator."),
    dict(id="kitco", title="Kitco — Live gold price and 'Gold Value by Purity' table",
         url="https://www.kitco.com/charts/gold", verifyState=PASS,
         what="Primary spot snapshot and the per-karat per-ounce values used on the Gold Price page."),
    dict(id="etsy-pp", title="Etsy — Purchase Protection Program",
         url="https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program", verifyState="prior",
         what="Buyer cover for orders that don't arrive, arrive damaged, arrive 7+ days late, or differ significantly from the description."),
    dict(id="jvc", title="Jewelers Vigilance Committee — mediation services",
         url="https://jvclegal.org/mediation-services/", verifyState="prior",
         what="Dispute mediation between consumers and jewelers (linked from the FTC article)."),
    dict(id="reportfraud", title="FTC — ReportFraud.ftc.gov",
         url="https://reportfraud.ftc.gov/", verifyState="prior", what="Where to report a jewelry purchase problem."),
]

# Checklist: the 12 points the buyer asked for, each tied to a reference and to what we found.
CHECKLIST = [
    ("Gold purity (karat)", "Confirm 10K / 14K / 18K and what it means: 14K = 14/24 gold, 18K = 18/24.",
     "ftc-consumer", "Observed range across the 24 listings: 14K and 18K only. Karat is recorded per row with its source."),
    ("Solid gold", "The listing must say solid gold — not plated, vermeil, gold-filled, overlay or gold-tone. FTC: 'solid gold' means not hollow.",
     "ftc-consumer", "9 listings state 'solid' explicitly. The rest are silent — silence is not proof, so those cells are blank and flagged."),
    ("Hallmark + maker's mark", "A karat stamp is not enough: FTC says look for the maker's name or trademark next to it, and if it is missing, don't buy.",
     "ftc-consumer", "No listing in this dataset shows a hallmark photo with a maker's mark. That is the single biggest gap — flagged on every row."),
    ("Weight in grams", "A legitimate seller can provide the ring's weight in grams.",
     "nist", "8 listings publish a gram weight; 16 do not — left blank, flagged F3. Weights published by sellers are claims (F19)."),
    ("Seller reputation", "Search the business name plus 'complaint' and 'review'; verify real contact details.",
     "ftc-consumer", "Phone/email captured where published. Blue Nile has a real but mixed record (F4). Etsy shops show shop ratings, not item ratings (F16)."),
    ("Price vs. gold value", "Compute pure gold grams x current spot; an unusually cheap price is a red flag.",
     "kitco", "Computed for every row with a weight. One case study priced below melt (F1). The rest sit above metal value, as expected."),
    ("Return policy", "Confirm you can return after inspecting it; check exclusions on resized/custom rings.",
     "ftc-consumer", "Blue Nile excludes resized/engraved/custom (F5). Etsy windows differ per listing: 7 / 14 / 21 / 30 days (F15)."),
    ("Payment", "Use a credit card for purchase protection; avoid irreversible methods.",
     "reportfraud", "All sellers checked accept card payment; several push financing (Affirm/Klarna) which changes your dispute route."),
    ("Documentation", "Keep the listing, receipt, description and every purity claim the seller made.",
     "ftc-consumer", "This site keeps the source URL and check date for every row — save the same pages yourself at checkout."),
    ("Independent verification on arrival", "Before wearing or resizing, have an independent jeweler verify purity and weight.",
     "jvc", "Plan this before you buy: a resize can void the return window (F5)."),
    ("XRF testing", "Ask for XRF (or another professional assay); do not rely on the stamp.",
     "cfr23-3", "No listing offers an XRF report. Budget for a test on arrival; the stamp alone is a claim (F11)."),
    ("If the seller won't let you verify or return it — don't buy", "Refusal to allow independent verification or a return is disqualifying.",
     "ftc-consumer", "Solid Gold Jewelers publishes no price and no return policy — treat as unusable until the seller answers in writing (flagged)."),
]
