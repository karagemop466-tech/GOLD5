#!/usr/bin/env python3
"""Authoring script for GOLD5 canonical data.

Writes site/assets/data.json. The JSON file is the single source of truth used by
scripts/build_site.py and scripts/verify.py. This script exists so the provenance
comments below travel with the data.

PROVENANCE KEY (pass 5, 2026-10-25)
  live   = read from the official page on the data date (2026-10-25) by THIS session
  prior  = an older dated observation, never presented as current. Two rows are prior
           in this pass: BE-NADIA and BE-SECRET, whose pages were opened again on
           2026-10-25 but served EUR; their USD figures stay the 2026-10-23 reads.
  readBy = the session that actually performed the read:
             3dfe4d85                    -> re-opened live in this pass (2026-10-25)
             bc4e36a1 (inherited) /
             6d10ac0a (inherited)        -> read on 2026-10-23 by that session; carried
                                            forward unchanged with its original evidence
                                            id and path and never relabelled
No value below is estimated or inferred. Blank = null and flagged. No EUR figure is
converted to USD anywhere. The build compares every listing with
data/live_check_3dfe4d85.json (which inherits data/live_check_6d10ac0a.json and
data/live_check_bc4e36a1.json) before emitting JSON, and refuses to write if an
observed value disagrees with the canonical row or if a value this session claims to
have re-read does not appear literally in its own verbatim excerpt.
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "site", "assets", "data.json")

BN_RETURNS = ("(re-confirmed live 2026-10-25, session 3dfe4d85) 30 days from shipment date, original unworn condition, full refund or exchange. "
              "NOT eligible: personalized jewelry, custom orders, engraved items, items resized after "
              "initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. "
              "Two complimentary returns per customer per year; RMA required; $150 fee if a diamond "
              "grading report is not returned. One free resize (up or down two sizes) within 6 months "
              "if the design permits.")
BE_RETURNS = ("(policy page not re-reachable 2026-10-25 — FL-33) Product pages state 'Free Shipping & Returns' and 'Free 1-Year Resizing'. Verified live at "
              "brilliantearth.com/30-Day-Returns/ on 2026-10-23: free returns/exchanges within 30 days of the item "
              "being available for shipment or pickup, unworn and in original condition. Engraved rings may be "
              "returned with a $40 engraving-removal charge; personalized/custom and other published exclusions "
              "apply. Phone return instructions and a free FedEx label are published.")
AL_RETURNS = ("(last read 2026-10-23; the policy page was unreachable for the 2026-10-25 pass — FL-33) Return must ARRIVE at Allurez within 30 days of original shipment; unused, not resized or "
              "altered. Engraved items, custom-made orders, contoured wedding bands, clearance items, "
              "appraisals, gift cards and layaway deposits are non-refundable. Design Your Own rings may be "
              "exchanged only (same or higher value). Buyer pays return shipping; original shipping not "
              "refunded; $300 deduction per missing diamond certificate; refund within 7 business days.")

def e(**kw):
    base = dict(
        id=None, name=None, short=None, sellerId=None, category="engagement-ring",
        karat=14, metalColor="Yellow Gold", price=None, compareAt=None, priceBasis="setting",
        priceNote=None, priceSourceUrl=None, grams=None, gramsText=None, gramsNote=None,
        widthMm=None, solidStated=False, solidQuote=None, hallmarkStated=False, hallmarkQuote=None,
        makerMarkStated=False, metalConflict=None, returns=None, returnUrl=None, returnsVerified=False,
        evidenceId=None, evidencePath=None, url=None, sources=[], checkedOn="2026-10-25", provenance="live", flags=[], notes=[],
        availability=None,
    )
    base.update(kw)
    if base["priceSourceUrl"] is None:
        base["priceSourceUrl"] = base["url"]
    return base

ENTRIES = [
    # ---------------- Blue Nile settings (all 8 re-read live 2026-10-25 this pass) ----------------
    e(id="BN-192506", name="Petite Hidden Halo Solitaire Plus Diamond Engagement Ring, 14K Yellow Gold",
      short="Petite Hidden Halo Solitaire Plus", sellerId="bluenile", karat=14, metalColor="Yellow Gold",
      price=1255, priceBasis="setting", priceNote="$1,255 setting price (center diamond extra); stock 502250y14",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
      returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Direct product page re-read live on 2026-10-25; setting price and product specifications recorded.",
             "Lifetime warranty applies only to items priced $1,000 or more."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21", "FL-06"]),
    e(id="BN-195639", name="Petite Solitaire Engagement Ring, 14k Yellow Gold",
      short="Petite Solitaire", sellerId="bluenile", karat=14, metalColor="Yellow Gold",
      price=1000, priceBasis="setting", priceNote="$1,000 setting price (center diamond extra)",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639",
      returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Direct product page re-read live on 2026-10-25; setting price and product specifications recorded."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21", "FL-06"]),
    e(id="BN-203257", name="Classic Four Prong Solitaire Engagement Ring, 14K Yellow Gold",
      short="Classic Four Prong Solitaire", sellerId="bluenile", karat=14, metalColor="Yellow Gold",
      price=870, priceBasis="setting", priceNote="$870 setting price (center diamond extra); stock 500000y14",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
      widthMm=1.9, returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Product page re-read this pass: $870 (Setting Price), Metal 14K Yellow Gold, Width 1.90mm."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21", "FL-06"]),
    e(id="BN-195326", name="Riviera Pavé Diamond Engagement Ring, 14K White Gold (1/6 ct. tw.)",
      short="Riviera Pavé 1/6 ct. tw.", sellerId="bluenile", karat=14, metalColor="White Gold",
      price=1500, priceBasis="setting", priceNote="$1,500 setting price (center diamond extra)",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326",
      returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Direct product page re-read live on 2026-10-25; setting price and product specifications recorded."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21"]),
    e(id="BN-195871", name="French Pavé Diamond Engagement Ring, 14k Yellow Gold (1/4 ct. tw.)",
      short="French Pavé 1/4 ct. tw.", sellerId="bluenile", karat=14, metalColor="Yellow Gold",
      price=1800, priceBasis="setting", priceNote="$1,800 setting price (center diamond extra); stock 501410y14",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
      widthMm=2.5, returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Product page re-read this pass: $1,800 (Setting Price), 14K Yellow Gold, 2.50mm, 16 diamonds 1/4 ct. tw."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21"]),
    e(id="BN-311132", name="Criss Cross Solitaire Engagement Ring, 18K Yellow Gold (by James Allen)",
      short="Criss Cross Solitaire (James Allen)", sellerId="bluenile", karat=18, metalColor="Yellow Gold",
      price=2320, priceBasis="setting", priceNote="$2,320 setting price (center diamond extra)",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132",
      returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Direct product page re-read live on 2026-10-25; setting price and product specifications recorded."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21"]),
    e(id="BN-203738", name="Floral Marquise Diamond Engagement Ring — metal description conflict",
      short="Floral Marquise — metal conflict", sellerId="bluenile", karat=18, metalColor="White Gold (title/specification)",
      price=2210, priceBasis="setting", priceNote="$2,210 setting price (center diamond extra); metal description is internally conflicting (FL-30)",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738",
      metalConflict="Title and specification say 18K White Gold; Product Details say 14K Yellow Gold.",
      returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Direct product page re-read live: $2,210 Setting Price; title/specification 18K White Gold; Product Details 14K Yellow Gold (FL-30)."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21", "FL-30"]),
    e(id="BN-203348", name="Classic Simple Solitaire Engagement Ring, 14K Yellow Gold",
      short="Classic Simple Solitaire", sellerId="bluenile", karat=14, metalColor="Yellow Gold",
      price=1145, priceBasis="setting", priceNote="$1,145 setting price (center diamond extra); stock 502120y14",
      url="https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-yellow-gold-item-203348",
      widthMm=2.4, returns=BN_RETURNS, returnUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
      notes=["Product page re-read this pass: $1,145 (Setting Price), Stock 502120y14, 14K Yellow Gold, Width 2.40mm."],
      flags=["FL-03", "FL-15", "FL-14", "FL-05", "FL-21", "FL-06"]),

    # ---------------- Brilliant Earth settings ----------------
    e(id="BE-1343", name="Freesia 2mm Solitaire Ring, 14K Yellow Gold (BE1343-14KY)",
      short="Freesia 2mm Solitaire", sellerId="brilliantearth", karat=14, metalColor="Yellow Gold",
      price=None, priceBasis="setting",
      priceNote="USD price not confirmable — the product page served EUR €835.00 (Setting Only) again on 2026-10-25 (FL-08, FL-33); the USD cell stays blank, no conversion (an earlier USD $750 render is a dated observation)",
      url="https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
      widthMm=2.0, returns=BE_RETURNS, returnUrl="https://www.brilliantearth.com/30-Day-Returns/", returnsVerified=True,
      notes=["Opened again 2026-10-25: price line served ‘€\u200c835.00(Setting Only)’; style BE1343-14KY, 14K Yellow Gold, Width 2-1.2 mm, Claw Prong re-confirmed; the USD cell stays blank — no conversion (FL-08, FL-33).",
             "Prior USD $750 and the review count (80 shown on this read) are dated observations, not current claims. The banner printed EUR (€280.00 gift card over €1,150.00) while the promo image block printed ‘USD$250 GIFT CARD … USD$1,000’ — the mixed-currency render is recorded for FL-08."],
      flags=["FL-03", "FL-15", "FL-14", "FL-21", "FL-08"]),
    e(id="BE-NADIA", name="Nadia Diamond Ring, 14K Yellow Gold (BE1D6013)",
      short="Nadia Diamond Ring", sellerId="brilliantearth", karat=14, metalColor="Yellow Gold",
      price=1250, priceBasis="setting", priceNote="$1,250 setting only (center diamond extra) — dated 2026-10-23 USD observation; the 2026-10-25 open served ‘€\u200c1,400.00(Setting Only)’ with no USD price (FL-08, FL-33; no conversion)",
      url="https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/",
      widthMm=1.8, returns=BE_RETURNS, returnUrl="https://www.brilliantearth.com/30-Day-Returns/", returnsVerified=True,
      notes=["Page opened again 2026-10-25: title, 14K Yellow Gold, 1.8mm band, accent details (0.06 and 0.05 ct. tw.) and 143 reviews re-confirmed — but the price line served EUR only, so the $1,250 remains the 2026-10-23 read and this row is labelled prior, never current.",
             "No EUR→USD conversion was performed (FL-08, FL-33)."],
      flags=["FL-03", "FL-15", "FL-14", "FL-21", "FL-08"]),
    e(id="BE-1343HH", name="Freesia Hidden Halo Diamond Ring, 14K Yellow Gold (BE1D3939)",
      short="Freesia Hidden Halo", sellerId="brilliantearth", karat=14, metalColor="Yellow Gold",
      price=None, priceBasis="setting",
      priceNote="USD price not confirmable — the product page served EUR €1,350.00 (Setting Only) again on 2026-10-25 (FL-08, FL-33); prior USD $1,190 seen on the product page 2026-10-22 (dated observation only, no conversion)",
      url="https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/",
      widthMm=2.0, returns=BE_RETURNS, returnUrl="https://www.brilliantearth.com/30-Day-Returns/", returnsVerified=True,
      notes=["Opened again 2026-10-25: ‘€\u200c1,350.00(Setting Only)’, style BE1D3939-14KY, 14K Yellow Gold, Width 2-1.3 mm, 14 shared-prong accents min 0.05 ctw, 31 reviews; USD cell stays blank (FL-08, FL-33). Prior $1,190 USD is a dated observation only."],
      flags=["FL-03", "FL-15", "FL-14", "FL-21", "FL-08"]),
    e(id="BE-SECRET", name="Secret Halo 1.5mm Diamond Ring, 14K Yellow Gold (BE1D13065)",
      short="Secret Halo 1.5mm", sellerId="brilliantearth", karat=14, metalColor="Yellow Gold",
      price=1090, priceBasis="setting", priceNote="$1,090 USD setting only (center diamond extra) — dated 2026-10-23 read; the 2026-10-25 open served ‘€\u200c1,250.00(Setting Only)’ with no USD price (FL-08, FL-33; no conversion)",
      url="https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/",
      widthMm=1.5, returns=BE_RETURNS, returnUrl="https://www.brilliantearth.com/30-Day-Returns/", returnsVerified=True,
      notes=["Direct product page re-read live 2026-10-23: $1,090 USD Setting Only; 14K Yellow Gold; 1.5 mm; 13 accent diamonds 0.06 ct. tw. Opened again 2026-10-25: style BE1D13065-14KY, 1.5 mm and 92 reviews re-confirmed, but the price line served EUR only (€1,250.00) — the USD figure stays the dated 2026-10-23 observation, FL-08 applies again and the row is labelled prior (FL-33)."],
      flags=["FL-03", "FL-15", "FL-14", "FL-21", "FL-08"]),

    # ---------------- Allurez settings (weights published) ----------------
    e(id="AL-5882", name="Filigree Designed Solitaire Engagement Ring Setting, 14K Yellow Gold (U5882)",
      short="Filigree Solitaire Setting", sellerId="allurez", karat=14, metalColor="Yellow Gold",
      price=1085, priceBasis="setting", priceNote="$1,085 setting only (center stone sold separately)",
      url="https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold",
      grams=5.0, gramsText="5.00 grams (approximate)", gramsNote="Seller's published 'Gold Weight 5.00 Grams (Approximate)'",
      returns=AL_RETURNS, returnUrl="https://www.allurez.com/pages/return-policy", returnsVerified=True,
      notes=["Product page re-read live 2026-10-25: $1,085, style U5882, 14k yellow gold, gold weight 5.00 g approx., widths 2.9/2.3 mm — identical to the 2026-10-23 capture.",
             "Page also shows a '$2,497 Everyone Else / 57% Savings' comparison — seller marketing, not used."],
      flags=["FL-15", "FL-14", "FL-09", "FL-10", "FL-18"]),
    e(id="AL-170", name="Antique Engraved Solitaire Engagement Ring Setting, 14k Yellow Gold (U170)",
      short="Antique Engraved Setting", sellerId="allurez", karat=14, metalColor="Yellow Gold",
      price=933, priceBasis="setting", priceNote="$933 setting only (center stone sold separately)",
      url="https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold",
      grams=4.8, gramsText="4.80 grams (approximate)", gramsNote="Seller's published 'Gold Weight 4.80 grams (Approximate)'",
      returns=AL_RETURNS, returnUrl="https://www.allurez.com/pages/return-policy", returnsVerified=True,
      notes=["Product page re-read live 2026-10-25: $933, style U170, 14k yellow gold, gold weight 4.80 g approx., widths 3.20/2.40 mm.",
             "Page also shows a '$1,373 Everyone Else / 32% Savings' comparison — not used."],
      flags=["FL-15", "FL-14", "FL-09", "FL-10", "FL-18"]),
    e(id="AL-4426", name="Engraved Floral Solitaire Engagement Ring Setting, 14K Yellow Gold (NG4426)",
      short="Engraved Floral Setting", sellerId="allurez", karat=14, metalColor="Yellow Gold",
      price=585, priceBasis="setting", priceNote="$585 setting only (center stone sold separately)",
      url="https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold",
      grams=3.58, gramsText="3.58 grams (approximate)", gramsNote="Seller's published 'Approximate Metal Weight 3.58 grams'",
      returns=AL_RETURNS, returnUrl="https://www.allurez.com/pages/return-policy", returnsVerified=True,
      notes=["Product page re-read live 2026-10-25: $585, style NG4426, 14k yellow gold, approximate metal weight 3.58 g.",
             "Page also shows a '$1,194 Everyone Else / 51% Savings' comparison — not used."],
      flags=["FL-15", "FL-14", "FL-09", "FL-10", "FL-18"]),

    # ---------------- Complete rings ----------------
    e(id="AV-25893", name="14K Solid Yellow Gold Diamond Solitaire Engagement Ring, 0.41 Ctw (R25893)",
      short="Diamond Solitaire 0.41 Ctw", sellerId="avianne", karat=14, metalColor="Yellow Gold",
      price=1100, priceBasis="complete", priceNote="$1,100 complete ring including 0.41 ct center diamond",
      url="https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
      grams=2.3, gramsText="2.3 grams", gramsNote="Seller's published 'Item Weight 2.3 grams'", widthMm=4.5,
      solidStated=True, solidQuote="Product title: '14K Solid Yellow Gold'",
      returns="Returns of unworn and unaltered items accepted within 14 days. Full policy page not captured; resize/custom exclusions not confirmed.",
      returnUrl="https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
      notes=["Product page re-read this pass: $1,100.00, item code R25893, 14K Gold, 2.3 grams, 0.41 Ctw, 4.5 mm width, VS2 clarity, G/H color.",
             "Site-wide banner: 10% OFF with code 'FALL10' — recorded price is the listed price before that code."],
      flags=["FL-14", "FL-11"]),
    e(id="JM-149700", name="Brilliant Round Diamond Solitaire Engagement Ring, 14K Yellow Gold (Style 149700)",
      short="Brilliant Round Solitaire 0.71 ctw", sellerId="jewelrymaster", karat=14, metalColor="Yellow Gold",
      price=3020, compareAt=6041, priceBasis="complete", priceNote="$3,020 'Special Price' complete ring including 0.71 ctw diamonds (seller 'Retail Price' $6,041, not used)",
      url="https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
      grams=2.3, gramsText="2.3 grams", gramsNote="Seller's published 'Metal Weight: 2.3 Grams'",
      solidStated=True, solidQuote="Description: 'entirely handcrafted in pure 14KT solid yellow gold'",
      returns="30-day return or exchange under the 'Money Back Guarantee (some restrictions apply)'; the specific restrictions are not stated on the page.",
      returnUrl="https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
      notes=["Product page re-read this pass: Retail Price $6,041.00 / Special Price $3,020.00, style 149700, 0.71 ctw, 14KT gold, 2.3 grams, in stock (only 1 left).",
             "Includes free shipping, gift box and a professional appraisal certificate per the page."],
      flags=["FL-14", "FL-12"]),
    e(id="SGJ-B02561", name="Yellow Gold Solitaire Engagement Ring, 14K Yellow (SKU B02561, brand M Michael)",
      short="Yellow Gold Solitaire (M Michael)", sellerId="solidgoldjewelers", karat=14, metalColor="Yellow Gold",
      price=None, priceBasis="complete", priceNote="No price published — page says 'Call (309) 452-1612 for current pricing and availability.'",
      url="https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
      grams=4.7, gramsText="4.7 g", gramsNote="Page states '14ky, 4.7g, #B02561'",
      returns="No return policy shown on the product page.",
      returnUrl="https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
      notes=["Product page re-read live on 2026-10-23 (session 6d10ac0a, ledger L18): '14ky, 4.7g, #B02561', WooCommerce brand field 'M Michael' (store taxonomy, not a maker's-mark claim), no price shown, 'Call (309) 452-1612 for current pricing and availability.', no payment method stated, no return policy shown."],
      flags=["FL-13", "FL-15", "FL-14", "FL-18", "FL-32"]),

    # ---------------- Etsy listings ----------------
    e(id="ET-4426190660", name="2.50 CT Radiant Canary Lab-Grown Diamond Ring, IGI Certified, 14K Yellow Gold",
      short="2.50 CT Radiant Lab Diamond", sellerId="etsy-rakshakjewels", karat=14, metalColor="Yellow Gold",
      price=1891.78, compareAt=None, priceBasis="complete",
      priceNote="14K Yellow Gold option $1,891.78; 10K $1,686.02; 18K $2,109.58; list starts at $1,202.08 for 925 silver. The header compare-at belongs to another variant, so compareAt is blank.",
      url="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
      widthMm=1.8, solidStated=True,
      solidQuote="Description: 'Metal Options: Available in 10K/14K/18K Solid Gold (White, Yellow, Rose Gold) & Platinum'",
      returns="Returns & exchanges accepted within 14 days; buyer pays return shipping; original condition required.",
      returnUrl="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond", returnsVerified=True,
      notes=["Listing re-read this pass: $1,202.08+ base (925 silver), 14K Yellow Gold $1,891.78 unchanged, 2.50 ct radiant yellow lab-grown diamond (VVS2), 0.32 ctw side stones, band 1.80 mm, IGI certificate offered.",
             "The 2026-10-25 read captured the promo countdown 'Sale ends in 15:11:39' (50% off, original $2,404.16+ at read time) — a relative timer; no absolute expiry is published or recorded (FL-17).",
             "Shop is Etsy 'Star Seller' with a 5/5 listing rating."],
      flags=["FL-03", "FL-16", "FL-17", "FL-14"]),
    e(id="ET-4366425533", name="Emerald Cut E/VVS2 IGI Lab-Grown Diamond Hidden Halo Ring, 14K Gold",
      short="Emerald Cut Hidden Halo", sellerId="etsy-foreverforlove", karat=14, metalColor="Yellow / White / Rose Gold",
      price=546.18, compareAt=None, priceBasis="from", stoneIncluded=True,
      priceNote="14K options $546.18–$2,405.36 by center-diamond size (re-read 2026-10-25; the 2026-10-23 read was $546.09–$2,404.96); list starts at $375.86 for 925 silver (header 40% off $626.44+, 'Sale ends in 3 days'). No 14K-specific compare-at price was published, so compareAt is blank.",
      url="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
      solidStated=True, solidQuote="Description: 'Made with genuine 14k real gold – never plated or filled'",
      hallmarkStated=True, hallmarkQuote="Description: 'Metal stamp: Yes' (no maker's mark stated, no photo)",
      returns="Returns & exchanges accepted within 30 days; buyer pays return shipping; description states a full refund/exchange and a lifetime warranty on manufacturer defects.",
      returnUrl="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown", returnsVerified=True,
      notes=["Listing re-read live on 2026-10-25: the 14K variant start moved $546.09 → $546.18 and the top $2,404.96 → $2,405.36; silver header now $375.86+ (original $626.44+); Metal stamp: Yes; 30-day returns.",
             "Ships from the UK; duties included for US orders per listing description."],
      flags=["FL-03", "FL-16", "FL-17", "FL-14"]),
    e(id="ET-1151446373", name="14K Solid Gold Ruby + 0.30 CT Diamond Halo Ring",
      short="Ruby + Diamond Halo", sellerId="etsy-verabyden", karat=14, metalColor="Yellow / White / Rose Gold",
      price=969.0, compareAt=None, priceBasis="complete",
      priceNote="14K option $969.00; 10K $783.00; 18K $1,233.00. The $1,044 header compare-at belongs to the base variant, so compareAt is blank for the 14K row.",
      url="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
      grams=3.7, gramsText="3.70 g", gramsNote="Seller's description: 'Gold grams: 3.70 gr' — re-verified on the listing page 2026-10-25",
      solidStated=True, solidQuote="Description: 'Material: Solid Gold (not gold plated or gold filled)' and 'Karat: 14 K (585)'",
      returns="Returns within 7 days after receipt; buyer pays return shipping; $20 delivery charge and 10% restocking fee; personalized, colored-enamel, letter and name-specific items excluded.",
      returnUrl="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant", returnsVerified=True,
      notes=["Listing re-read this pass (2026-10-25): $783.00+ (10K), 14K $969.00 unchanged, 0.30 ct diamond + 0.90 ct ruby, 'Gold grams: 3.70 gr', 585 stated; the price block missing from the 2026-10-23 partial read was retrieved today.",
             "Return window is 7 days — shortest of the sellers reviewed.",
             "Ships from Albany, NY; production partner Vera Atolye, Istanbul, Türkiye.",
             "Listing photos include a chat screenshot with an address and a request to share contact details — flagged (FL-02)."],
      flags=["FL-02", "FL-16", "FL-17", "FL-14", "FL-18"]),
    e(id="ET-1566052947", name="14K Solid Yellow Gold Domed Band, 2–8 mm (reference band)",
      short="Domed Band 2–8 mm", sellerId="etsy-vibrantstone", category="band", karat=14, metalColor="Yellow Gold",
      price=246.35, compareAt=379.0, priceBasis="from",
      priceNote="From $246.35 (2 mm ladder start, re-read 2026-10-25; header 35% off $379.00+; the 2026-10-23 read was $251.30 at 30% off $359.00); 3 mm $330.85+, 4 mm $460.85+, 5 mm $597.35+, 6 mm $740.35+, 7 mm $870.35+, 8 mm $1,000.35–$1,630.85",
      url="https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
      solidStated=True, solidQuote="Title: '14k Solid Yellow Gold Domed Wedding Band'",
      returns="Returns & exchanges accepted within 21 days; buyer pays return shipping. Customized bands may not be returnable; altered/used/damaged items may incur fees up to 30% or be ineligible; items exchanged once cannot then be returned.",
      returnUrl="https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band", returnsVerified=True,
      notes=["Listing re-read live on 2026-10-25: the 2 mm start moved $251.30 → $246.35 and the promo deepened (30% → 35% off, header original $379.00+, 'Sale ends in 1 day' at read time); no gram weight published.",
             "The 21-day return window and custom/fee exclusions come from the 2026-10-23 shop-policy capture; the shop policy page was unreachable for this session on 2026-10-25 (FL-33), so it is a dated observation. The listing itself displays 'Returns & exchanges accepted'."],
      flags=["FL-03", "FL-16", "FL-17", "FL-14"]),
    e(id="ET-1433905613", name="14K Solid Gold 8 mm Polished Comfort-Fit Dome Band (reference band)",
      short="Comfort-Fit Dome Band 8 mm", sellerId="etsy-adelafinejewels", category="band", karat=14, metalColor="White Gold",
      price=984.32, compareAt=None, priceBasis="from",
      priceNote="14K options $984.32–$1,347.84 by size (re-read 2026-10-25; 10K $664.32–$949.12); 36% off with 'Sale ends in 0:29:08' captured at read time. The $1,038 header compare-at is for the 10K base variant, so compareAt is blank for 14K. (2026-10-23 read: 14K $999.70–$1,368.90, 35% off.)",
      url="https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
      widthMm=8.0, solidStated=True, solidQuote="Title: '14K Solid Gold 8mm White Gold Polished ... Wedding Band'",
      returns="Returns & exchanges accepted within 14 days; buyer pays return transportation; personalized products are non-refundable.",
      returnUrl="https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished", returnsVerified=True,
      notes=["Listing re-read live on 2026-10-25: the 14K range moved $999.70–$1,368.90 → $984.32–$1,347.84 and the discount deepened 35% → 36%; no gram weight published.",
             "The 14-day return window and personalized-item exclusion come from the 2026-10-23 shop-policy capture (policy page unreachable for this session on 2026-10-25, FL-33); the listing itself shows 'Returns & exchanges accepted'.",
             "A buyer-photo alt text on the page mentions an engraving '585 AFJ' — not a seller statement, so no hallmark or maker's mark is recorded."],
      flags=["FL-03", "FL-16", "FL-17", "FL-14"]),
    e(id="ET-944684759", name="14K White Gold Flat Polished Band, 2–6 mm (reference band)",
      short="Flat Polished Band 2–6 mm", sellerId="etsy-cittali", category="band", karat=14, metalColor="White Gold",
      price=195.75, compareAt=261.0, priceBasis="from",
      priceNote="Listing titled 14K White Gold displays from $195.75 (2 mm, 25% off $261.00); 3 mm $337.50+, 4 mm $369.00+, 5 mm $429.75+, 6 mm $524.25–$1,158.75. Description also lists other materials, so reconfirm the selected metal at checkout.",
      url="https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
      solidStated=True, solidQuote="Description lists '10k, 14k, 18k Solid Gold' options for this design",
      returns="Returns & exchanges accepted within 30 days; buyer pays return shipping; original condition required.",
      returnUrl="https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished", returnsVerified=True,
      notes=["Listing re-read live 2026-10-25: from $195.75, every ladder figure identical to the 2026-10-23 capture; countdown 'Sale ends in 0:29:08' at read time.",
             "The 30-day return window is the 2026-10-23 shop-policy capture (policy page unreachable for this session on 2026-10-25, FL-33); the listing shows 'Returns & exchanges accepted'; description lists multiple materials for the design, so selected metal must be reconfirmed at checkout."],
      flags=["FL-03", "FL-16", "FL-17", "FL-14"]),
    e(id="ET-576343849", name="14K Solid White Gold Band, Size 11 — sold case study (exact weight unresolved)",
      short="Sold band — weight unresolved", sellerId="etsy-butterflywingvintage", category="case-study", karat=14, metalColor="White Gold",
      price=420.0, compareAt=525.0, priceBasis="complete", availability="SOLD OUT — confirmed 2026-10-25",
      priceNote="$420.00 displayed on the sold-out detail page (original $525.00); this is a sold-listing case study, not a current offer",
      url="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
      grams=None, gramsText="Not exact: title says 7 g; description says postal scale alternates between 6–7 g", gramsNote="No exact seller-stated weight; numeric grams and metal value intentionally blank",
      solidStated=True, solidQuote="Title and description: 'Fine Solid 14K White Gold Wedding/Engagement Band'",
      hallmarkStated=True, hallmarkQuote="Description: 'marked 14K with a maker's mark' and directs the buyer to the fourth photo", makerMarkStated=True,
      returns="n/a — item sold; seller FAQ says no refund for buyer's remorse or changed mind.",
      returnUrl="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
      notes=["Sold-out detail page re-read live 2026-10-25: still sold out; $420.00 displayed, original $525.00; not a current offer.",
             "Exact weight and the old below-metal calculation are withdrawn: the title says 7 g but the description says the postal scale alternates between 6–7 g. No range is converted into an exact number (FL-01).",
             "The seller explicitly claims both a 14K stamp and a maker's mark; this remains a seller statement, not an independent assay."],
      flags=["FL-01", "FL-03", "FL-16", "FL-17", "FL-18", "FL-29"]),
]

# ---- sellers -------------------------------------------------------------
SELLERS = [
    dict(id="bluenile", name="Blue Nile", type="Retailer (online)",
         website="https://www.bluenile.com/", contact=["+1-800-242-2728", "service@bluenile.com"],
         contactUrl="https://www.bluenile.com/contact-us",
         returns=BN_RETURNS, returnsUrl="https://www.bluenile.com/policies/returns", returnsVerified=True,
         warranty="Limited lifetime warranty on gold/platinum items priced $1,000 or more (manufacturer defects); one free resize up or down two sizes within 6 months if the design permits; non-resizable styles excluded.",
         warrantyUrl="https://www.bluenile.com/services/warranty",
         payment="Credit card at checkout; Blue Nile credit card financing and Affirm-style monthly options are advertised.",
         reputation=[dict(source="Better Business Bureau profile", value="A+ accredited; 121 complaints in the last 3 years; 22 in the last 12 months; BBB customer reviews average 1/5 (25 reviews)", url="https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564", method="prior-session capture"),
                     dict(source="ConsumerAffairs", value="1.7/5 from 172 reviews", url="https://www.consumeraffairs.com/retail/blue-nile.html", method="prior-session capture")],
         flags=["FL-04", "FL-05", "FL-06"],
         sources=["https://www.bluenile.com/policies/returns", "https://www.bluenile.com/services/warranty",
                  "https://www.bluenile.com/contact-us", "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564",
                  "https://www.consumeraffairs.com/retail/blue-nile.html"],
         notes=["Return policy, contact details and warranty re-read this pass."]),
    dict(id="brilliantearth", name="Brilliant Earth", type="Retailer (online + showrooms)",
         website="https://www.brilliantearth.com/", contact=["800.691.0952"],
         contactUrl="https://www.brilliantearth.com/contact/",
         returns=BE_RETURNS, returnsUrl="https://www.brilliantearth.com/30-Day-Returns/", returnsVerified=True,
         warranty="Free lifetime manufacturing-defect warranty on fine jewelry; wear, gemstone loss, product loss and theft excluded. US/CAN/AUS/UK return labels are free; elsewhere a $50 deposit applies and is refunded for warrantied repairs. Unauthorized repair voids coverage.",
         warrantyUrl="https://www.brilliantearth.com/customer-service/warranty/#manufacturing_warranty",
         payment="Credit card; Affirm monthly payments (0% APR available), Wells Fargo 12-month financing and layaway are advertised.",
         reputation=[dict(source="Product page reviews (Freesia 2mm)", value="4.8/5 from 80 reviews", url="https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/", method="prior-session capture (2026-10-22)")],
         flags=["FL-04"],
         sources=["https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
                  "https://www.brilliantearth.com/30-Day-Returns/"],
         notes=["Return policy verified live 2026-10-23 at /30-Day-Returns/ (30-day window; exclusions published) — see FL-07 (resolved). The policy page was unreachable for the 2026-10-25 pass (proxy failure, FL-33); the product pages opened that day still display the 'Free Shipping & Returns' coverage line."]),
    dict(id="allurez", name="Allurez", type="Retailer (online, made in USA)",
         website="https://www.allurez.com/", contact=["1-800-554-3509", "service@allurez.com"],
         contactUrl="https://www.allurez.com/pages/contact",
         returns=AL_RETURNS, returnsUrl="https://www.allurez.com/pages/return-policy", returnsVerified=True,
         warranty="Complimentary 1-year limited manufacturing-defect warranty for qualifying US purchases after February 2024. Ring sizing is offered except full eternity rings. Missing stones may be replaced, but the new stone's cost is not covered. Wear, loss and unauthorized repair excluded; after one year repair fees plus a $39 shipping charge apply.",
         warrantyUrl="https://www.allurez.com/pages/warranty",
         payment="Credit card; Affirm, Klarna, Shop Pay Installments, Flex Pay and Allurez Layaway (10% down) advertised.",
         reputation=[], flags=["FL-09", "FL-10"],
         sources=["https://www.allurez.com/pages/return-policy", "https://www.allurez.com/pages/warranty",
                  "https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold"],
         notes=["Return policy and contact details re-read this pass."]),
    dict(id="avianne", name="Avianne & Co", type="Retailer (NY showroom + online)",
         website="https://www.avianneandco.com/", contact=["1 (332)-244-4038", "28 W 47th Street, Diamond District, New York, NY"],
         contactUrl="https://www.avianneandco.com/",
         returns="Returns of unworn and unaltered items accepted within 14 days. Full policy page not captured; resize/custom exclusions not confirmed.",
         returnsUrl="https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw", returnsVerified=False,
         warranty="Not stated on the product page.", warrantyUrl=None,
         payment="Credit card; Affirm and Shop Pay installments advertised; promo code FALL10 for 10% off.",
         reputation=[], flags=["FL-04", "FL-11"],
         sources=["https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw"],
         notes=["Contact details and 14-day return notice re-read this pass."]),
    dict(id="jewelrymaster", name="The Jewelry Master (Jewelry Masters)", type="Retailer (online)",
         website="https://www.thejewelrymaster.com/", contact=["1-888-59-JEWEL"],
         contactUrl="https://www.thejewelrymaster.com/",
         returns="30-day 'Money Back Guarantee (some restrictions apply)' — return or exchange within 30 days, no questions asked; the restrictions themselves are not stated on the page.",
         returnsUrl="https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html", returnsVerified=False,
         warranty="Professional appraisal certificate included with purchase; no separate warranty stated.",
         warrantyUrl=None,
         payment="Credit card; Affirm financing advertised.",
         reputation=[], flags=["FL-04", "FL-12"],
         sources=["https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html"],
         notes=["Return terms and contact number re-read this pass."]),
    dict(id="solidgoldjewelers", name="Solid Gold Jewelers", type="Independent jeweler (online + store)",
         website="https://solidgoldjewelers.net/", contact=["(309) 452-1612"],
         contactUrl="https://solidgoldjewelers.net/",
         returns="No return policy shown on the product page.", returnsUrl="https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/", returnsVerified=False,
         warranty="Not stated.", warrantyUrl=None,
         payment="Not stated; price is quoted by phone.",
         reputation=[], flags=["FL-04", "FL-13"],
         sources=["https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/"],
         notes=["Product page re-read this pass; no price and no return terms published."]),
    dict(id="etsy-rakshakjewels", name="RAKSHAKJEWELS (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/RAKSHAKJEWELS", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/RAKSHAKJEWELS",
         returns="Returns & exchanges accepted within 14 days; buyer pays return shipping; original condition required.",
         returnsUrl="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond", returnsVerified=True,
         warranty="Not stated on the listing.", warrantyUrl=None,
         payment="Etsy checkout (cards, PayPal, Klarna); Etsy Purchase Protection applies to eligible orders.",
         reputation=[dict(source="Etsy listing badge", value="Star Seller; 5/5 listing rating", url="https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond", method="prior-session capture (2026-10-22)")],
         flags=["FL-04", "FL-16"], sources=["https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond"],
         notes=["Listing re-read this pass."]),
    dict(id="etsy-foreverforlove", name="ForeverForLove (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/ForeverForLove", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/ForeverForLove",
         returns="Returns & exchanges accepted within 30 days; buyer pays return shipping.",
         returnsUrl="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown", returnsVerified=True,
         warranty="Lifetime warranty on manufacturer defects per the listing description.",
         warrantyUrl="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies.",
         reputation=[dict(source="Etsy listing badge", value="Star Seller; 5/5 listing rating", url="https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown", method="prior-session capture")],
         flags=["FL-04", "FL-16"], sources=["https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown"],
         notes=["Listing re-read live 2026-10-25 (session 3dfe4d85); the shop-level policy was last read 2026-10-23 and was unreachable for this pass (proxy failure — FL-33); see the linked current evidence check."]),
    dict(id="etsy-verabyden", name="VeraByEden (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/VeraByEden", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/VeraByEden",
         returns="Returns within 7 days after receipt; buyer pays return shipping; $20 delivery charge and 10% restocking fee; personalized, colored-enamel, letter and name-specific items excluded.",
         returnsUrl="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant", returnsVerified=True,
         warranty="Not stated on the listing.", warrantyUrl=None,
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies.",
         reputation=[dict(source="Etsy listing badge", value="Star Seller; 5/5 rating", url="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant", method="prior-session capture (2026-10-22)")],
         flags=["FL-02", "FL-04", "FL-16"], sources=["https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"],
         notes=["Return window (7 days) and gold weight (3.70 g) re-read this pass."]),
    dict(id="etsy-vibrantstone", name="VibrantStone (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/VibrantStone", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/VibrantStone",
         returns="Returns & exchanges accepted within 21 days; buyer pays return shipping (original shipping is advertised free). Customized/personalized returns may incur fees; altered, used or damaged items may incur up to 30% fees or be ineligible; an exchanged item cannot be returned.",
         returnsUrl="https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band", returnsVerified=True,
         warranty="Not stated.", warrantyUrl=None,
         payment="Etsy checkout; Etsy Purchase Protection applies.",
         reputation=[dict(source="Etsy listing badge", value="Star Seller; 5/5 listing rating", url="https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band", method="prior-session capture")],
         flags=["FL-04", "FL-16"], sources=["https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band"],
         notes=["Listing re-read live 2026-10-25 (session 3dfe4d85); the shop-level policy was last read 2026-10-23 and was unreachable for this pass (proxy failure — FL-33); see the linked current evidence check."]),
    dict(id="etsy-adelafinejewels", name="adelafinejewels (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/adelafinejewels", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/adelafinejewels",
         returns="Returns & exchanges accepted within 14 days; buyer pays return transportation (free US original shipping); personalized products are non-refundable.",
         returnsUrl="https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished", returnsVerified=True,
         warranty="Not stated.", warrantyUrl=None,
         payment="Etsy checkout; Etsy Purchase Protection applies.",
         reputation=[dict(source="Etsy listing badge", value="Star Seller; 5/5 listing rating", url="https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished", method="prior-session capture")],
         flags=["FL-04", "FL-16"], sources=["https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished"],
         notes=["Listing re-read live 2026-10-25 (session 3dfe4d85); the shop-level policy was last read 2026-10-23 and was unreachable for this pass (proxy failure — FL-33); see the linked current evidence check."]),
    dict(id="etsy-cittali", name="CittaliFineJewelry (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/CittaliFineJewelry", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/CittaliFineJewelry",
         returns="Returns & exchanges accepted within 30 days; buyer pays return shipping.",
         returnsUrl="https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished", returnsVerified=True,
         warranty="Not stated.", warrantyUrl=None,
         payment="Etsy checkout; Klarna advertised; Etsy Purchase Protection applies.",
         reputation=[dict(source="Etsy listing", value="4.9/5 item average", url="https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished", method="prior-session capture")],
         flags=["FL-04", "FL-16"], sources=["https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished"],
         notes=["Listing re-read live 2026-10-25 (session 3dfe4d85); the shop-level policy was last read 2026-10-23 and was unreachable for this pass (proxy failure — FL-33); see the linked current evidence check."]),
    dict(id="etsy-butterflywingvintage", name="BUTTERFLYWINGVINTAGE (Etsy shop)", type="Etsy shop",
         website="https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE", contact=["Contact via Etsy Messages"],
         contactUrl="https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
         returns="n/a — item sold; seller FAQ says no refund for buyer's remorse or changed mind.", returnsUrl="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1", returnsVerified=False,
         warranty="Not stated.", warrantyUrl=None,
         payment="n/a — item sold.",
         reputation=[dict(source="Etsy listing", value="5/5 with 802 shop reviews", url="https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g", method="prior-session capture")],
         flags=["FL-04", "FL-16"], sources=["https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"],
         notes=["Sold-out detail page and seller FAQ re-read live 2026-10-25; the item is still sold and not a current offer."]),
]

# ---- flags ---------------------------------------------------------------
FLAGS = [
    dict(id="FL-01", severity="high", status="resolved", title="Resolved: the below-metal case study relied on an unsupported exact weight",
         detail="The sold Etsy listing's title says 7 g, but its description says a postal scale alternates between 6–7 g. The current sold-out detail page displays $420.00 (original $525.00), not a current offer. Exact grams, fine-gold weight, metal value and the former below-metal conclusion are therefore withdrawn. No range is converted into an exact number; ask for a calibrated weight and independent assay before drawing any conclusion.",
         entryIds=["ET-576343849"]),
    dict(id="FL-02", severity="high", status="open", title="Listing photos solicit off-platform contact",
         detail="VeraByEden listing image 11 is a chat screenshot showing an address (2355 Westwood Boulevard #153, Los Angeles CA) and the text 'Share your contact information with us on Etsy Message.' Off-platform payment or contact can void Etsy Purchase Protection. Keep any purchase on Etsy and pay through Etsy checkout.",
         entryIds=["ET-1151446373"]),
    dict(id="FL-03", severity="medium", status="open", title="Exact gram weight is not published for 18 of 25 rows",
         detail="Without an exact weight you cannot compute gold content or compare price with metal value. These cells are left blank — never estimated. The sold case study has only a 6–7 g scale range, so it is included here as well. Ask the seller in writing for the weight in grams before buying, then verify it on arrival.",
         entryIds=["BN-192506","BN-195639","BN-203257","BN-195326","BN-195871","BN-311132","BN-203738","BN-203348",
                   "BE-1343","BE-NADIA","BE-1343HH","BE-SECRET","ET-4426190660","ET-4366425533","ET-1566052947",
                   "ET-1433905613","ET-944684759","ET-576343849"]),
    dict(id="FL-04", severity="medium", status="open", title="Independent seller reputation not captured for most sellers",
         detail="Only Blue Nile has independent complaint data captured (BBB and ConsumerAffairs). Brilliant Earth shows on-site review scores; Allurez, Avianne, Jewelry Master, Solid Gold Jewelers and the Etsy shops have no independent complaint data in this dataset. Do the check yourself: search the business name plus 'complaint' or 'review', confirm a real phone/address, and look for a BBB profile.",
         entryIds=[]),
    dict(id="FL-05", severity="medium", status="open", title="Blue Nile: resized, engraved and custom rings are not returnable",
         detail="Blue Nile's 30-day money-back guarantee excludes personalized jewelry, custom orders, engraved items, items resized after purchase, Diamond Upgrade purchases, clearance and Final Sale. Returns are capped at two complimentary returns per customer per year, an RMA is required, and a missing diamond grading report costs $150. Do not resize before deciding to keep the ring.",
         entryIds=["BN-192506","BN-195639","BN-203257","BN-195326","BN-195871","BN-311132","BN-203738","BN-203348"]),
    dict(id="FL-06", severity="low", status="open", title="Blue Nile lifetime warranty starts at $1,000; some settings fall below it",
         detail="The limited lifetime warranty covers gold and platinum items with a purchase price of $1,000 or more. Of the Blue Nile settings recorded here, the $870 Classic Four Prong falls below that threshold (the $1,000 Petite Solitaire sits exactly at it), so it does not qualify for the lifetime warranty under the stated terms.",
         entryIds=["BN-203257","BN-195639","BN-192506","BN-203348"]),
    dict(id="FL-07", severity="medium", status="resolved", title="Resolved: Brilliant Earth return policy re-read and wording corrected",
         detail="Verified live 2026-10-23 at https://www.brilliantearth.com/30-Day-Returns/: free returns/exchanges run for 30 days from the item being available for shipment or pickup, with original/unworn condition required. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. All four Brilliant Earth entries link this working official policy.",
         entryIds=["BE-1343","BE-NADIA","BE-1343HH","BE-SECRET"]),
    dict(id="FL-08", severity="low", status="open", title="Brilliant Earth renders serve EUR by geography; USD prices are blank or dated observations",
         detail="On 2026-10-23 BE-1343 served €835 and BE-1343HH served €1,350 (USD cells blank) while BE-NADIA and BE-SECRET served USD directly ($1,250 / $1,090). On the 2026-10-25 re-read ALL FOUR pages served EUR (€835.00, €1,400.00, €1,350.00, €1,250.00), each with the same mixed render: a EUR banner next to a 'USD$250 GIFT CARD … USD$1,000' promo image. BE-NADIA and BE-SECRET therefore revert to dated 2026-10-23 USD observations labelled prior — their prices could not be confirmed today and no EUR figure was converted. The currency is chosen per page/geo at request time, so any USD price on this site is only as current as the render it was read from. Re-read from a USD session before acting.",
         entryIds=["BE-1343","BE-1343HH","BE-NADIA","BE-SECRET"]),
    dict(id="FL-09", severity="low", status="open", title="Allurez shows an 'Everyone Else' comparison price — not used",
         detail="Allurez pages display a '% Savings' figure against an 'Everyone Else' price ($2,497 / $1,373 / $1,194 on the three rings here). That comparison is the seller's own marketing claim and is not independently verified. Only the actual selling price is used in this project.",
         entryIds=["AL-5882","AL-170","AL-4426"]),
    dict(id="FL-10", severity="medium", status="open", title="Allurez: Design Your Own rings are exchange-only",
         detail="Allurez's policy says Design Your Own engagement rings may be exchanged for items of the same or higher value but cannot be refunded. It does not say whether buying a setting on its own counts as 'Design Your Own'. Treat these settings as possibly exchange-only and confirm in writing before buying.",
         entryIds=["AL-5882","AL-170","AL-4426"]),
    dict(id="FL-11", severity="low", status="open", title="Avianne: 14-day window, active promo code, full policy not captured",
         detail="The product page says returns of unworn and unaltered items are accepted within 14 days — shorter than the 30 days common elsewhere. The site also runs a 10% code (FALL10), which is not applied to the recorded price. The full return policy and resize exclusions were not captured. Both statements were re-read on the product page 2026-10-25 (session 3dfe4d85) unchanged; Avianne has no separate policy check in the ledger, so returnsVerified stays False by design.",
         entryIds=["AV-25893"]),
    dict(id="FL-12", severity="low", status="open", title="Jewelry Master: 'Retail Price' is a seller comparison; guarantee restrictions unspecified",
         detail="The page shows a Retail Price of $6,041 against a Special Price of $3,020. The retail figure is the seller's own comparison and is not used in any analysis. The 30-day money-back guarantee says 'some restrictions apply' but does not list them.",
         entryIds=["JM-149700"]),
    dict(id="FL-13", severity="medium", status="open", title="Solid Gold Jewelers: no price, no return policy and no payment method published",
         detail="The product page states '14ky, 4.7g, #B02561' and asks buyers to call (309) 452-1612 for current pricing and availability. No price, no return policy and no payment method appear on the page (re-read 2026-10-23 by session 6d10ac0a, ledger check L18), so all three are left blank. A phone quote would be a new dated seller statement — it must never be back-filled from another listing or another session. Get price, return terms, payment method and the hallmark in writing before sending money.",
         entryIds=["SGJ-B02561"]),
    dict(id="FL-32", severity="medium", status="open", title="Payment methods are seller-advertised, not verified — one seller states none",
         detail="The seller records show a stated payment method for 12 of 13 sellers: credit card is named by Blue Nile, Brilliant Earth, Allurez, Avianne & Co and The Jewelry Master (with Affirm / Klarna / Shop Pay / layaway advertised alongside), and Etsy checkout by the seven Etsy shops. Solid Gold Jewelers states no payment method at all — its page says 'Call (309) 452-1612 for current pricing and availability' (FL-13). These are checkout options advertised on the sellers' own pages on the dates shown, not independently confirmed facts, and no source states that wire transfers, Zelle or gift cards are refused by any of them; the absence of a statement is not evidence of a policy. FTC credit-card guidance establishes a consumer's right to dispute billing errors — it does not verify any merchant's accepted methods. Confirm the method in writing before paying, and treat any request to pay off-platform or by irreversible transfer as a red flag.",
         entryIds=["SGJ-B02561"]),
    dict(id="FL-14", severity="medium", status="open", title="Maker's mark is not stated for 24 of 25 listings",
         detail="FTC guidance says to look near the karat mark for the name or U.S. registered trademark of the company behind it. The sold ET-576343849 description says 'marked 14K with a maker's mark' and points to a photo; that is a seller claim, not an independent assay. The other 24 listings do not state a maker's mark. Ask for close-up photos of both marks and verify them on arrival.",
         entryIds=[]),
    dict(id="FL-15", severity="medium", status="open", title="Listing does not explicitly say 'solid gold' (16 of 25)",
         detail="A karat mark alone does not say whether an item is solid or plated/hollow. FTC guidance defines 'solid gold' as not hollow. Brilliant Earth, Blue Nile and Allurez listings name the metal and karat but do not use the words 'solid gold'; Solid Gold Jewelers shows only '14ky'. These are left unflagged as solid and require written confirmation from the seller. The 9 Etsy/Avianne/Jewelry Master listings that do say solid are recorded with their exact wording.",
         entryIds=["BN-192506","BN-195639","BN-203257","BN-195326","BN-195871","BN-311132","BN-203738","BN-203348",
                   "BE-1343","BE-NADIA","BE-1343HH","BE-SECRET","AL-5882","AL-170","AL-4426","SGJ-B02561"]),
    dict(id="FL-16", severity="low", status="open", title="Etsy return windows vary by shop — one is only 7 days",
         detail="VeraByEden accepts returns within 7 days; RAKSHAKJEWELS and adelafinejewels state 14 days; VibrantStone states 21 days; ForeverForLove and Cittali state 30 days. Fees, personalization exclusions and the sold listing's no-remorse-refund statement still apply. Etsy Purchase Protection covers qualifying non-delivery, damage, late delivery and materially different items, not ordinary buyer's remorse. Check the specific shop policy before ordering.",
         entryIds=["ET-4426190660","ET-4366425533","ET-1151446373","ET-1566052947","ET-1433905613","ET-944684759","ET-576343849"]),
    dict(id="FL-17", severity="low", status="open", title="Etsy prices are promo-dependent and vary by material, size and carat",
         detail="Etsy listings in this set showed discounts at check time and prices change by material (silver/10K/14K/18K), ring size, band width and center-stone carat. Where a header compare-at price belonged to another material or variant, compareAt is blank rather than borrowed. The recorded price is labeled by its actual option or listing basis on the check date. Re-check the live price before buying. PROVEN BY RE-READ: within two days three rows moved — ET-4366425533 14K start $546.09 → $546.18, ET-1566052947 2 mm $251.30 → $246.35 (promo deepening 30% → 35% off), ET-1433905613 14K $999.70 → $984.32 (35% → 36% off). The 2026-10-25 pass also captured the sale countdowns the previous pass asked for — 'Sale ends in 15:11:39', '3 days', '1 day' and two '0:29:08' timers — recorded as relative times only, because no absolute expiry is published.",
         entryIds=["ET-4426190660","ET-4366425533","ET-1151446373","ET-1566052947","ET-1433905613","ET-944684759","ET-576343849"]),
    dict(id="FL-18", severity="low", status="open", title="Gram weights are seller-stated, not independently verified",
         detail="Allurez publishes approximate gold weights; Avianne, Jewelry Master and Solid Gold Jewelers publish single figures; VeraByEden states 'Gold grams: 3.70 gr'. The sold ET-576343849 page gives only a 6–7 g scale range and is not assigned an exact weight. None has been independently weighed. Treat them as claims to be checked with a jeweler's scale and XRF on arrival.",
         entryIds=["AL-5882","AL-170","AL-4426","AV-25893","JM-149700","SGJ-B02561","ET-1151446373","ET-576343849"]),
    dict(id="FL-19", severity="info", status="open", title="Gold spot moves all day — the snapshot is dated",
         detail="Four Kitco captures span two trading sessions: 2026-10-23 alone printed $4,022.50/oz (5:44 a.m. ET), $3,996.10/oz (4:10 p.m. ET) and $3,994.90/oz ($128.44/g, 19:43 NY panel / 7:42 p.m. ET) — a $27.60/oz intraday swing — and the 2026-10-25 re-read still prints $3,994.90/$128.44 under the newer 'Oct 24, 2026 - 23:14 NY Time' panel because the market had not reopened after the Friday 5:00 PM NY close. A quote is a timestamped observation, not a live feed: this site uses one labeled panel bid for every calculation, shows its timestamp, keeps every superseded quote as dated history, and even a same-value re-read is labelled by the session that actually read it. Spot at the moment you buy will differ; use the calculator with a fresh quote.",
         entryIds=[]),
    dict(id="FL-20", severity="info", status="open", title="A 14K or 18K stamp is not proof of purity",
         detail="FTC guidance requires a karat mark plus a maker's mark, but a stamp is a disclosure, not an assay. The only way to know what the metal actually is: have an independent jeweler test it (XRF or another professional method) after delivery, before wearing or resizing. No US law requires the seller to accept a return based on your test, so confirm the return right first.",
         entryIds=[]),
    dict(id="FL-21", severity="info", status="open", title="Setting prices exclude the center diamond",
         detail="Blue Nile and Brilliant Earth prices recorded here are 'Setting Price' / 'Setting Only'. The center stone is sold separately, so price-to-metal ratios are only computed for complete rings. Do not compare a setting with a complete ring as if they were the same purchase.",
         entryIds=["BN-192506","BN-195639","BN-203257","BN-195326","BN-195871","BN-311132","BN-203738","BN-203348",
                   "BE-1343","BE-NADIA","BE-1343HH","BE-SECRET","AL-5882","AL-170","AL-4426"]),
    dict(id="FL-22", severity="low", status="open", title="Retailers excluded rather than guessed",
         detail="Walmart's search results render client-side and served no product cards or prices; two listings found by search (Pompeii3 and marquise-jewelers) were dead. No values were recorded for them. Exclusion is deliberate: blank beats invented.",
         entryIds=[]),
    dict(id="FL-23", severity="info", status="open", title="Earlier sessions' work is preserved in this repo",
         detail="Earlier sessions delivered to this repository. Their sites remain available: 638c9614 at /docs/, 090bae73 at /index-090bae73.html (+ /pages/), 37e8ff42's dashboard at /archive/session-37e8ff42/, 93032b31's 24-row dashboard at /archive/session-93032b31/, 84be683f at /verified/, 60c4b9c3 at /report/ (evidence in /verification/), and the /guide/ checklist site. This consolidated site merges their verified listings and flags; nothing was discarded.",
         entryIds=[]),
    dict(id="FL-24", severity="info", status="resolved", title="Resolved: karat-in-URL and grams-via-snippet flags",
         detail="Earlier flags said the Brilliant Earth karat appeared only in product URLs and that VeraByEden's 3.70 g came from a search snippet. Both were re-checked live: each Brilliant Earth product page states 14K Yellow Gold, and VeraByEden's description states 'Gold grams: 3.70 gr'. The old flags are closed, with the checks recorded on the Verification page.",
         entryIds=["BE-NADIA","BE-1343HH","BE-SECRET","ET-1151446373"]),
    dict(id="FL-25", severity="low", status="open", title="Kitco page shows several nearby numbers in one capture",
         detail="The current capture (2026-10-25 read of the Oct 24 23:14 NY panel, prices stated as of 11:12 p.m. ET) displays a panel bid of $3,994.90 and $128.44/g, an ask of $3,996.90, a body sentence repeating $3,994.90/oz, and two different kilo prints — $128,440.99 in the ticker against $128,439.02 in the page's own unit table — while the purity table carries a Friday 5:00 PM NY update stamp. The embedded widget behaved differently this time: TradingView printed O/H/L/C as empty, whereas on 2026-10-23 the same slot printed an OANDA-style close of 3,995.810 (19:43:05 UTC-4). The superseded 4:10 p.m. ET capture had its own split ($3,996.10 panel vs $3,995.50 body text) and is kept in history. The project uses the panel bid and its per-gram figure for every calculation, publishes the extra prints as a labeled discrepancy, and never mixes quotes from different timestamps, widgets or sources.",
         entryIds=[]),
    dict(id="FL-26", severity="medium", status="resolved", title="Resolved: all seven Etsy listing pages were read live on 2026-10-23",
         detail="An earlier collector returned HTTP 500 for the Etsy pages. This pass opened all seven official listing URLs directly and recorded field-level evidence in data/live_check_bc4e36a1.json (L19–L25). Current prices, stated options and available return terms replace the prior-session labels; the sold listing remains explicitly sold out.",
         entryIds=["ET-4426190660","ET-4366425533","ET-1151446373","ET-1566052947","ET-1433905613","ET-944684759","ET-576343849"]),
    dict(id="FL-27", severity="medium", status="resolved", title="Resolved: all four Brilliant Earth pages were read live",
         detail="A previous collector saw navigation only. The 2026-10-23 direct reads are recorded in data/live_check_bc4e36a1.json (L09–L12): BE-1343 serves €835, BE-NADIA $1,250 USD, BE-1343HH €1,350, and BE-SECRET $1,090 USD. EUR is not converted; the two USD blanks are flagged FL-08.",
         entryIds=["BE-1343","BE-NADIA","BE-1343HH","BE-SECRET"]),
    dict(id="FL-28", severity="low", status="resolved", title="Resolved: both remaining Blue Nile pages were re-read",
         detail="The 2026-10-23 direct reads are recorded in data/live_check_bc4e36a1.json (L07–L08): BN-203738 displays $2,210 with an explicit 18K/14K metal conflict, and BN-203348 displays $1,145, 14K Yellow Gold, stock 502120y14 and 2.40 mm. Both rows carry the current check date. BN-203738 was re-read a second time on 2026-10-23 by session 6d10ac0a (ledger L07, verification/evidence/6d10ac0a/retailers.md): $2,210 Setting Price, stock 502820w, 18K White Gold in the title and specification, 14k yellow gold in Product Details — the conflict is unchanged and still published, not resolved.",
         entryIds=["BN-203738","BN-203348"]),
    dict(id="FL-31", severity="info", status="resolved", title="Resolved: provenance scope of the 2026-10-23 pass (session 6d10ac0a) — superseded by FL-33",
         detail="(Closed by the 2026-10-25 pass: all 25 listing pages and the spot were re-opened then, so this scope note no longer attaches to any row; the current pass's scope — 26 checks re-read, 20 inherited from 2026-10-23, 2 partial reads, 6 failure records — is published as FL-33.) This pass re-opened 9 of the 46 canonical checks live: the Kitco spot plus eight listing pages (BN-203738, AL-5882, AL-170, AL-4426, AV-25893, JM-149700, SGJ-B02561, ET-576343849). Every re-read field matched the canonical row exactly, so the only value that changed is the timestamped spot quote and the numbers derived from it. The other 37 checks — 17 listings, 9 seller policy/contact pages and 11 official references — were read earlier the same day (2026-10-23) by session bc4e36a1 and are carried forward unchanged with their original evidence ids and paths, labelled readBy 'bc4e36a1 (inherited)' rather than being presented as this session's reads. Rows carrying this flag were therefore not re-opened by session 6d10ac0a; their values still come from an official page read on 2026-10-23. Two pages (ET-1151446373, BE-1343) were only partially retrieved this pass and are logged as partial reads; they upgraded nothing.",
         entryIds=[]),
    dict(id="FL-33", severity="info", status="open", title="Provenance scope of the 2026-10-25 pass (session 3dfe4d85)",
         detail="This pass re-opened 26 of the 46 canonical checks live on 2026-10-25: the Kitco spot, all 25 listing pages and the two Blue Nile policy pages (returns, warranty). 21 of the 25 listing rows matched their recorded fields exactly. Three Etsy prices had genuinely moved and were corrected from this pass's own captures (C-20: ET-4366425533 $546.09 → $546.18; C-21: ET-1566052947 $251.30 → $246.35 with the promo deepening 30% → 35%; C-22: ET-1433905613 $999.70 → $984.32 with 35% → 36%). Four Brilliant Earth pages were opened again but served EUR only (€835.00 / €1,400.00 / €1,350.00 / €1,250.00) with no USD price — BE-NADIA and BE-SECRET therefore revert to labelled prior-dated USD observations (this flag's entryIds) and BE-1343 / BE-1343HH keep blank USD cells; nothing was converted (FL-08). The remaining 20 checks — the 2 superseded BE listing reads, 7 seller policy/contact pages and 11 official references — could not be re-opened because the fetch proxy returned SignatureDoesNotMatch (or failed before they were attempted, which is recorded as not attempted); they are carried forward byte-identical with their 2026-10-23 dates, original evidence ids and paths, readBy '<session> (inherited)' labels and an inheritedNote. Nothing inherited is presented as fresh, nothing failed is presented as read, and the seller return-policy text shown on the affected rows is therefore the 2026-10-23 capture. Full log: data/live_check_3dfe4d85.json, verification/evidence/3dfe4d85/ (including failures-and-irregularities.md F1–F6).",
         entryIds=["BE-NADIA","BE-SECRET"]),
    dict(id="FL-29", severity="medium", status="open", title="ET-576343849 is sold out — not a current offer",
         detail="Re-read 2026-10-25: the detail page still says 'This item is sold out.' and displays $420.00 (original $525.00). It cannot be purchased; the price is a labeled sold-listing display only. Earlier $444.80/$556.00 observations remain historical archive material. The title's 7 g and the description's alternating 6–7 g scale range are not an exact weight, so no metal-value conclusion is drawn (FL-01 resolved).",
         entryIds=["ET-576343849"]),
    dict(id="FL-30", severity="high", status="open", title="Blue Nile BN-203738 has an internal metal-description conflict",
         detail="The official page title and specification say 18K White Gold, while Product Details say 14K Yellow Gold — observed identically on 2026-10-23 (twice) and again on 2026-10-25, three sessions in a row. Both statements are preserved on the listing row; neither is silently selected as the truth. Confirm the exact metal, karat and return terms in writing before purchase. No gram weight is published, so no metal-value calculation is made for this row.",
         entryIds=["BN-203738"]),
]

# ---- official / trusted references --------------------------------------
REFERENCES = [
    dict(id="ftc-consumer", title="FTC Consumer Advice — Buying Platinum, Gold, and Silver Jewelry",
         publisher="U.S. Federal Trade Commission", url="https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
         quote="Near the karat quality mark, look for the name or the U.S. registered trademark of the company that will stand behind the mark... If you're thinking about buying a piece of gold jewelry but don't see a trademark along with the karat mark, don't buy it.",
         usedFor="Karat marks, maker's mark rule, solid vs plated/hollow definitions, returns in writing, where to report problems.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="cfr23", title="16 CFR Part 23 — Guides for the Jewelry, Precious Metals, and Pewter Industries",
         publisher="eCFR (Office of the Federal Register)", url="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
         quote="§ 23.3 Misrepresentation as to gold content. § 23.10 Additional guidance for the use of quality marks.",
         usedFor="The regulation behind the FTC consumer guidance; gold-content and quality-mark rules. eCFR displayed 'up to date as of 10/21/2026' on the 2026-10-23 fetch.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="usc295", title="15 U.S.C. § 295 — Standard of fineness of gold articles; deviation",
         publisher="U.S. Code (GovInfo, U.S. Government Publishing Office)", url="https://www.govinfo.gov/link/uscode/15/295",
         quote="...the actual fineness of such gold or alloy shall not be less by more than three one-thousandth parts than the fineness indicated by the mark stamped, branded, engraved, or printed upon any part of such article... and ... shall not be less by more than seven one-thousandth parts, in the case of any other such article...",
         usedFor="The statutory assay tolerance an XRF reading is compared against: 3/1000 solder-free, 7/1000 for the whole article including solder.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="cfr23-3", title="16 CFR § 23.3 — Misrepresentation as to gold content (Cornell LII mirror)",
         publisher="Cornell Legal Information Institute", url="https://www.law.cornell.edu/cfr/text/16/23.3",
         quote="Text of the gold-content misrepresentation rule.",
         usedFor="Readable mirror of § 23.3.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="usc297", title="15 U.S.C. § 297 — Stamping plated articles; identifying trademark",
         publisher="U.S. Government Publishing Office — GovInfo (official U.S. Code text)",
         url="https://www.govinfo.gov/link/uscode/15/297",
         quote="Each identifying trademark or name applied to any article of merchandise in compliance with clause (A) of this subsection shall be applied to that article by the same means as that used in applying the quality mark or stamp appearing thereon, in type or lettering at least as large as that used in such quality mark or stamp, and in a position as close as possible to that quality mark or stamp.",
         usedFor="Statutory basis for a maker's mark next to the quality mark (National Stamping Act), and for the rule that plated / rolled gold plate / gold filled articles may not carry a bare fineness mark: § 297(a) requires words 'plainly indicating that such article or part thereof is made of rolled gold plate, gold plate, or gold electroplate, or is gold filled'.",
         checkedOn="2026-10-23",
         method="live re-read 2026-10-23 (session 6d10ac0a; official GovInfo text, resolved to the GPO 2024 edition PDF USCODE-2024-title15-chap8-sec297.pdf). The Cornell LII page https://www.law.cornell.edu/uscode/text/15/297 is a mirror of the same section and is no longer the cited source. NOT re-opened 2026-10-25 (F6, FL-33) — capture date, not today's.",
         mirrorUrl="https://www.law.cornell.edu/uscode/text/15/297"),
    dict(id="nist-troy", title="NIST SP 811, Appendix B.8 — Factors for units listed alphabetically",
         publisher="National Institute of Standards and Technology", url="https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8",
         quote="NIST Appendix B.8 displays ounce (troy or apothecary) → gram as 3.110348 E+01 (rounded). Kitco separately states the more precise constant: 'A troy ounce is 31.1034768 grams.'",
         usedFor="Troy-ounce conversion disclosure. Calculations retain Kitco's stated 31.1034768 g/ozt constant; NIST's displayed factor is rounded.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; evidence R06); NOT re-opened 2026-10-25 (F6, FL-33) — capture date, not today's"),
    dict(id="lbma", title="LBMA Precious Metal Prices — benchmark administration",
         publisher="London Bullion Market Association", url="https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices",
         quote="The LBMA Gold Price is set twice daily in auctions independently operated and administered by ICE Benchmark Administration Limited (IBA) and commencing at 10:30 and 15:00 London time.",
         usedFor="Why a timestamped benchmark matters; the London benchmark is set twice daily, while retail spot pages update continuously.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="ftc-credit", title="FTC Consumer Advice — Using Credit Cards and Disputing Charges",
         publisher="U.S. Federal Trade Commission", url="https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges",
         quote="Federal law says you have the right to get mistakes fixed promptly... If you have a complaint about the quality of something you bought...",
         usedFor="Why a credit card is safer than an irreversible payment method, and how billing disputes work.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="etsy-pp", title="Etsy Purchase Protection Program",
         publisher="Etsy", url="https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program",
         quote="Full refund for eligible orders that don't arrive, arrive damaged, arrive 7+ days after the estimated delivery window, or differ significantly from the description.",
         usedFor="Marketplace protection limits (not buyer's remorse).",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="jvc", title="Jewelers Vigilance Committee — mediation services",
         publisher="Jewelers Vigilance Committee", url="https://jvclegal.org/mediation-services/",
         quote="Dispute mediation between buyers and jewelers (linked from the FTC article).",
         usedFor="Where to escalate a jewelry dispute.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
    dict(id="reportfraud", title="FTC — ReportFraud.ftc.gov",
         publisher="U.S. Federal Trade Commission", url="https://reportfraud.ftc.gov/",
         quote="Report fraud, scams and bad business practices.",
         usedFor="Reporting a seller.",
         checkedOn="2026-10-23", method="live re-read 2026-10-23 (session bc4e36a1; official reference ledger); NOT re-opened 2026-10-25 — the fetch proxy failed for this pass (F6), so this date is the capture date, not today's (FL-33)"),
]

SPOT = dict(
    primary=dict(source="Kitco Metals Inc. — Live Gold Price", url="https://www.kitco.com/charts/gold",
                 usdPerOz=3994.90, usdPerGram=128.44, asOf="2026-10-24 11:12 p.m. ET", kind="spot bid",
                 panelTime="Oct 24, 2026 - 23:14 NY Time",
                 method="live fetch 2026-10-25 03:14 UTC of the Oct 24, 2026 23:14 NY panel (session 3dfe4d85)",
                 quote="Live Gold Price — Oct 24, 2026 - 23:14 NY Time. Bid 3,994.90 USD (-28.20, -0.70%); Ask 3,996.90; ounce 3,994.90 (-28.20); gram 128.44 (-0.91); Kilo 128,440.99 (-906.65); pennyweight 199.75 (-1.41); tola 1,498.09 (-10.58); tael 4,854.91 (-34.27); Day's Range 3975.10 - 4040.20. 'Prices provided by Kitco Metals Inc. Displayed in U.S. dollars (USD), as of October 24, 2026 at 11:12 p.m. EDT.' Body text: 'The current price of gold is $3,994.90 per troy ounce as of October 24, 2026, 11:12 p.m. ET, down $28.40 today.' The purity table carries its own stamp 'Updated Oct 23, 2026 • 5:00 PM NY Time' — the Friday close carried through the weekend. The embedded TradingView widget printed O/H/L/C empty this time (23:14:15 UTC-4); on 2026-10-23 it printed a close of 3,995.810, and the unit table again shows a kilo of 128,439.02 against 128,440.99 in the ticker; those extra prints are disclosed (FL-25) and are not used in any calculation."),
    priorLeadNote="Values identical to the 2026-10-23 7:42 p.m. ET capture because spot had not reopened after the Friday 5:00 PM NY close; what changed is the timestamp, and this session read it itself.",
    prior=[dict(source="Kitco Metals Inc. — Live Gold Price", url="https://www.kitco.com/charts/gold",
                usdPerOz=3994.90, usdPerGram=128.44, asOf="2026-10-23 7:42 p.m. ET", kind="spot bid",
                method="live fetch (2026-10-23 19:43 NY panel; session 6d10ac0a)",
                note="The previous canonical quote, re-confirmed identically by this pass under the Oct 24 23:14 NY panel timestamp (weekend carry). Kept as dated history; not used in any calculation."),
           dict(source="Kitco Metals Inc. — Live Gold Price", url="https://www.kitco.com/charts/gold",
                usdPerOz=3996.10, usdPerGram=128.48, asOf="2026-10-23 4:10 p.m. ET", kind="spot bid",
                method="live fetch (2026-10-23 16:12 NY panel; integrated sessions 3bf55199 + bc4e36a1)",
                note="Previous 2026-10-23 quote (4:10 p.m. ET); superseded by the 7:42 p.m. ET quote above. Bid fell $1.20/oz between the two captures. Its own body text showed $3,995.50/oz and $128.46/g."),
           dict(source="Kitco Metals Inc. — Live Gold Price", url="https://www.kitco.com/charts/gold",
                usdPerOz=4022.50, usdPerGram=129.33, asOf="2026-10-23 5:44 a.m. ET", kind="spot bid",
                method="live fetch (2026-10-23 5:44 a.m. ET pass, session 77405ae3)",
                note="Earlier 2026-10-23 quote (5:44 a.m. ET); superseded by the two later captures above. Bid fell $26.40/oz intraday to 4:10 p.m. ET and $27.60/oz to 7:42 p.m. ET."),
           dict(source="Kitco Metals Inc. — Live Gold Price (previous session)", url="https://www.kitco.com/charts/gold",
                usdPerOz=4026.90, usdPerGram=129.47, asOf="2026-10-22 7:26 p.m. ET", kind="spot bid",
                method="prior-session capture (session 7cca80c9)",
                note="2026-10-22 close-of-day capture, recorded by the previous pass; superseded by the 2026-10-23 quote above."),
           dict(source="Kitco Metals Inc. — Live Gold Price (earlier capture)", url="https://www.kitco.com/charts/gold",
                usdPerOz=4025.00, usdPerGram=129.41, asOf="2026-10-22 7:10 p.m. ET", kind="spot bid",
                method="prior-session capture (session 37e8ff42)",
                note="Same Kitco page 16 minutes earlier; used by the archived sessions.")],
    crossChecks=[dict(source="CNBC Select (2026-10-22 capture)", url="https://www.cnbc.com/select/the-price-of-gold-today-oct-22-2026/",
                      usdPerOz=4083.82, usdPerGram=None, asOf="2026-10-22 9:00 a.m. ET", kind="spot",
                      method="prior-session capture",
                      note="Prior-day cross-check only. Gold's spot price as of 9:00 a.m. ET was $4,083.82 per ounce, per CNBC's Gold/US Dollar Spot Price."),
                 dict(source="APMEX (2026-10-22 capture)", url="https://www.apmex.com/gold-price",
                      usdPerOz=4077.60, usdPerGram=131.10, asOf="2026-10-22 11:02 a.m. ET", kind="spot",
                      method="prior-session capture",
                      note="Prior-day cross-check only. Gold Spot Price $4,077.60; Per Gram $131.10; Last Updated 10/22/2026 11:02:00 AM ET."),
                 dict(source="Kitco News AM report (2026-10-22)", url="https://www.kitco.com/news/article/2026-10-22/gold-silver-pressured-despite-lower-yields-hormuz-attacks-send-crude-higher",
                      usdPerOz=4086.90, usdPerGram=None, asOf="2026-10-22 morning", kind="spot",
                      method="prior-session capture",
                      note="Spot gold near $4,086.90 an ounce, down $53.40 (1.29%).")],
    notes=["The 2026-10-25 read (2026-10-25 03:14 UTC) shows the bid ticker at $3,994.90 with $128.44/g at the 'Oct 24, 2026 - 23:14 NY Time' panel, a body sentence repeating $3,994.90/oz 'as of October 24, 2026, 11:12 p.m. ET, down $28.40 today', the purity table (stamped 'Updated Oct 23, 2026 • 5:00 PM NY Time') at 24K $3,994.90, and two different kilo prints (128,440.99 ticker vs 128,439.02 unit table). The ticker bid and its own per-gram figure are the numbers used for every calculation; the timestamp is part of the value and the extra prints are disclosed, not mixed in (FL-25). The numbers are identical to the 2026-10-23 7:42 p.m. ET capture because the market has not reopened since the Friday close; that capture now sits in the dated prior chain.",
           "Earlier quotes (2026-10-23 7:42 p.m. ET, 4:10 p.m. ET, 5:44 a.m. ET and the 2026-10-22 pair) are retained only as dated history and are labelled prior. They are not used in any calculation on this site.",
           "This quote was re-read by session 3dfe4d85 on 2026-10-25. No listing-derived number changed because of the spot: the only listing values that moved were three Etsy prices, corrected from their own captures (C-20/C-21/C-22 in the ledger)."],
    purity=dict(fineness={"24K": 0.9999, "22K": 0.9167, "18K": 0.75, "14K": 0.5833, "10K": 0.4167},
                perOz={"24K": 3994.90, "22K": 3662.12, "18K": 2996.18, "14K": 2330.23, "10K": 1664.67},
                source="Kitco 'Gold Value by Purity' table, 2026-10-25 read of the Oct 24 23:14 NY page (session 3dfe4d85; values identical to the 2026-10-23 7:42 p.m. ET capture — the table itself is stamped 'Updated Oct 23, 2026 • 5:00 PM NY Time')"),
)


# ---- 2026-10-25 provenance pass -------------------------------------------
# The field-level read ledger is an input to the canonical build.  Every listing
# must have one current official-source check; the observed values are compared
# before any JSON is emitted.  This prevents a stale provenance loop or a hand
# edit from silently reintroducing a price, weight, or policy conclusion.
SESSION = "3dfe4d85"
PASS_DATE = "2026-10-25"
PRIOR_DATE = "2026-10-23"
INHERITED_LABELS = ("bc4e36a1 (inherited)", "6d10ac0a (inherited)")
SCOPE_FLAG = "FL-33"
LEDGER_PATH = os.path.join(ROOT, "data", "live_check_3dfe4d85.json")
with open(LEDGER_PATH, encoding="utf-8") as _lf:
    LIVE_CHECK = json.load(_lf)
if LIVE_CHECK.get("session") != SESSION:
    raise ValueError("The ledger must belong to this session; rebuild it with scripts/build_ledger_3dfe4d85.py")
if LIVE_CHECK.get("checkedOn") != PASS_DATE or LIVE_CHECK.get("coverage", {}).get("total") != 46:
    raise ValueError("The current 46-check evidence ledger is required for this build")
_LISTING_CHECKS = {c["entryId"]: c for c in LIVE_CHECK["checks"] if c.get("kind") == "listing"}
if set(_LISTING_CHECKS) != {x["id"] for x in ENTRIES} or len(_LISTING_CHECKS) != len(ENTRIES):
    raise ValueError("Evidence ledger listing coverage does not match canonical entries")
_OBSERVED_FIELDS = ("price", "grams", "karat", "solidStated", "hallmarkStated", "makerMarkStated", "returnsVerified")


def _money_tokens(value):
    """Literal spellings a verbatim excerpt must contain for a recorded amount."""
    out = {f"{value:,.2f}", f"{value:,.0f}" if float(value).is_integer() else None, f"{value}"}
    return {t for t in out if t}


for _e in ENTRIES:
    _c = _LISTING_CHECKS[_e["id"]]
    _by = _c.get("readBy")
    if _c.get("status") != "read":
        raise ValueError(f"Listing {_e['id']} lacks a read-status check")
    if _by == SESSION and _c.get("checkedOn") != PASS_DATE:
        raise ValueError(f"Listing {_e['id']}: a check attributed to this session is not dated {PASS_DATE}")
    if _by in INHERITED_LABELS:
        if _c.get("checkedOn") != PRIOR_DATE or not _c.get("inheritedNote"):
            raise ValueError(f"Listing {_e['id']}: inherited check lacks its dated capture or inheritedNote")
    elif _by != SESSION:
        raise ValueError(f"Listing {_e['id']} has no reader attribution")
    _o = _c.get("observed") or {}
    for _field in _OBSERVED_FIELDS:
        if _o.get(_field) != _e.get(_field):
            raise ValueError(f"Observed {_field} mismatch for {_e['id']}: {_o.get(_field)!r} vs {_e.get(_field)!r}")
    if _o.get("metalConflict") != _e.get("metalConflict"):
        raise ValueError(f"Metal-conflict disclosure mismatch for {_e['id']}")
    _excerpt = _c.get("sourceExcerpt") or ""
    # A value this pass re-read must literally appear in the verbatim excerpt it cites.
    if _c.get("readBy") == SESSION:
        if _o.get("price") is not None and not any(t in _excerpt for t in _money_tokens(_o["price"])):
            raise ValueError(f"Re-read price for {_e['id']} is not present in its own evidence excerpt")
        if _o.get("grams") is not None and not any(t in _excerpt for t in (f"{_o['grams']:.2f}", f"{_o['grams']}")):
            raise ValueError(f"Re-read weight for {_e['id']} is not present in its own evidence excerpt")
        if not any(t in _excerpt for t in (f"{_o.get('karat')}K", f"{_o.get('karat')}k", f"{_o.get('karat')}KT")):
            raise ValueError(f"Re-read karat for {_e['id']} is not present in its own evidence excerpt")
    _e["checkedOn"] = _c["checkedOn"]
    _e["provenance"] = "live" if _by == SESSION else "prior"
    _e["readBy"] = _by
    _e["evidenceId"] = _c["id"]
    _e["evidencePath"] = _c["evidencePath"]
    if _by == SESSION:
        _e["notes"].append(f"Re-read live by session {SESSION} on {_c['checkedOn']}: {_c['id']} ({_c['result']}); verbatim excerpt and official URL are linked on the Verification page.")
        if SCOPE_FLAG in _e["flags"]:
            raise ValueError(f"Listing {_e['id']}: a row re-read this pass must not carry {SCOPE_FLAG}")
    else:
        _first = _c.get("firstCapturedBy") or "an earlier session"
        _e["notes"].append(
            f"NOT re-fetched on {PASS_DATE} as a current value: the official page was opened again by session {SESSION} "
            f"but served EUR only (partial read logged in the ledger); the canonical figures stay the {_c['checkedOn']} "
            f"official-source read {_c['id']} ({_c['result']}, captured by session {_first}) — labelled prior, never "
            f"presented as current, no EUR converted (FL-08, {SCOPE_FLAG}).")
        if SCOPE_FLAG not in _e["flags"]:
            _e["flags"].append(SCOPE_FLAG)

_REREAD = sum(1 for _e in ENTRIES if _e.get("readBy") == SESSION)
_INHERITED = len(ENTRIES) - _REREAD
_LIVE_N = sum(1 for _e in ENTRIES if _e["provenance"] == "live")
_PRIOR_N = len(ENTRIES) - _LIVE_N

# The spot quote must be literally present in the spot evidence excerpt re-read this pass.
_SPOT_CHECK = next(c for c in LIVE_CHECK["checks"] if c.get("kind") == "spot")
if _SPOT_CHECK.get("readBy") != SESSION:
    raise ValueError("The spot check must be re-read by this session before its quote becomes primary")
for _token in (f"{SPOT['primary']['usdPerOz']:,.2f}", f"{SPOT['primary']['usdPerGram']:,.2f}"):
    if _token not in (_SPOT_CHECK.get("sourceExcerpt") or ""):
        raise ValueError(f"Canonical spot value {_token} is not present in the spot evidence excerpt")
for _k, _v in SPOT["purity"]["perOz"].items():
    if f"{_v:,.2f}" not in (_SPOT_CHECK.get("sourceExcerpt") or ""):
        raise ValueError(f"Purity value {_k} ${_v:,.2f} is not present in the spot evidence excerpt")

DATA = dict(
    meta=dict(
        project="GOLD5 — Solid Gold Engagement Ring Research",
        asOf=PASS_DATE,
        lastPass="2026-10-25 (session 3dfe4d85: spot + all 25 listings + 2 Blue Nile policies re-read live; 3 Etsy prices corrected from this pass's captures; 20 of 46 checks inherited from 2026-10-23 and labelled)",
        session=SESSION,
        title="Gold engagement rings, verified line by line",
        subtitle="25 listings from 13 sellers · every value tied to the official source page that states it and dated — 23 were re-read live in this pass (2026-10-25) and 2 are inherited prior-dated observations because every Brilliant Earth page served EUR only; 20 of the 46 evidence checks are inherited from the 2026-10-23 ledger and labelled as such · three Etsy prices genuinely moved within two days and were corrected from this pass's own captures · blanks and source conflicts are flagged, never guessed, never converted",
        noHallucinations=("NO HALLUCINATIONS IS THE RULE OF THIS PROJECT. Every price, karat, weight, policy and claim on this site "
                          "was read from the linked official source page on the date shown next to it, and the session that read it is "
                          "named. If a value could not be confirmed, it is left BLANK and published on the Flagged for Review page — "
                          "never inferred, estimated, currency-converted or filled in from a similar listing. Derived numbers "
                          "(fine-gold grams, metal value, price/metal) are computed from verified inputs and recomputed by the "
                          "checker. After every review pass, run python3 scripts/verify.py."),
        checker="python3 scripts/verify.py",
        evidenceLedger="data/live_check_3dfe4d85.json",
        liveCheck=LIVE_CHECK,
        coverage=dict(live=_LIVE_N, prior=_PRIOR_N, liveDate=PASS_DATE, priorDate=PRIOR_DATE,
                      reread=_REREAD, inherited=_INHERITED,
                      rereadSession=SESSION, inheritedSession="bc4e36a1 + 6d10ac0a (2026-10-23)",
                      partialReads=len(LIVE_CHECK.get("partialReads", [])),
                      failuresLogged=len(LIVE_CHECK.get("failures", []))),
        archive=[dict(label="Session 638c9614 — research site at /docs/", path="docs/index.html"),
                 dict(label="Session 090bae73 — checklist guide", path="index-090bae73.html"),
                 dict(label="Session 37e8ff42 — dashboard snapshot", path="archive/session-37e8ff42/index.html"),
                 dict(label="Session 93032b31 — 24-row pass-2 dashboard (superseded, preserved)", path="archive/session-93032b31/index.html"),
                 dict(label="Session 84be683f — generated site at /verified/", path="verified/index.html"),
                 dict(label="Session 60c4b9c3 — report site at /report/", path="report/index.html"),
                 dict(label="Checklist guide at /guide/", path="guide/index.html"),
                 dict(label="Session b1f2fe3b — Master Cross-Session Audit & XRF Assay Calculator (38 unified rows)", path="site/master-audit.html"),
                 dict(label="Session 0c967748 — current-evidence review (blank current fields, R01–R04)", path="review/index.html"),
                 dict(label="Session 3e3fae49 — 58-row dossier at /dossier/ (18/18 anti-hallucination checks)", path="dossier/index.html")],
        counts=dict(entries=len(ENTRIES), sellers=len(SELLERS), flags=len(FLAGS), references=len(REFERENCES)),
    ),
    spot=SPOT, entries=ENTRIES, sellers=SELLERS, flags=FLAGS, references=REFERENCES,
)

with open(OUT, "w") as f:
    json.dump(DATA, f, indent=1, ensure_ascii=False)
    f.write("\n")
print(f"wrote {OUT}: {len(ENTRIES)} entries, {len(SELLERS)} sellers, {len(FLAGS)} flags, {len(REFERENCES)} references")
