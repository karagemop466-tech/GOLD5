#!/usr/bin/env python3
"""Build data/live_check_3dfe4d85.json — the 46-check evidence ledger for session 3dfe4d85.

NO HALLUCINATIONS. This script does not invent evidence. It starts from the committed
2026-10-23 ledger written by session ``6d10ac0a`` (``data/live_check_6d10ac0a.json``, itself
overlaid on ``data/live_check_bc4e36a1.json``) and:

* replaces the excerpt / evidence path / result / observed values of the **26** checks this
  session re-opened live on 2026-10-25 (Kitco spot, 23 listing pages fully, 2 policy pages)
  with verbatim transcriptions saved under ``verification/evidence/3dfe4d85/``;
* carries the other **20** checks forward byte-identical to their originals
  (``readBy: <original session> (inherited)`` + an ``inheritedNote`` explaining why their
  date preders the data date) — they are never relabelled as this session's reads;
* moves two of those inherited listing checks (BE-NADIA, BE-SECRET) to explicitly dated
  prior observations, because the pages opened today served EUR and no USD price was
  confirmable — the partial reads are logged in ``partialReads`` with retrieved /
  notRetrieved / effect, exactly as the 2026-10-23 pass did;
* appends ``failures`` so that every fetch error and every page not attempted during the
  proxy outage is published instead of hidden.

Run:  python3 scripts/build_ledger_3dfe4d85.py
"""
from __future__ import annotations

import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "data", "live_check_6d10ac0a.json")
OUT = os.path.join(ROOT, "data", "live_check_3dfe4d85.json")
EV = "verification/evidence/3dfe4d85"

SESSION = "3dfe4d85"
BRANCH = "arena/3dfe4d85-gold5"
CHECKED_ON = "2026-10-25"
INHERIT_NOTES = {
    "bc4e36a1": ("Captured 2026-10-23 by session bc4e36a1 (through the 6d10ac0a ledger). The fetch "
                 "proxy returned SignatureDoesNotMatch for this URL on 2026-10-25, so the check was "
                 "NOT re-opened; it is kept at its original date and is not presented as fresh."),
    "6d10ac0a": ("Captured 2026-10-23 by session 6d10ac0a. The fetch proxy failed for this URL on "
                 "2026-10-25 (or the outage began before it was attempted, which is recorded as not "
                 "attempted), so the check was NOT re-opened; the original date and evidence are kept."),
}

# ----------------------------------------------------------------------------- re-reads
# Observed values below are transcribed from the pages this session opened on 2026-10-25.
# They must equal the canonical row values or scripts/author_data.py refuses to emit JSON.
BN_OBS = dict(grams=None, solidStated=False, hallmarkStated=False, makerMarkStated=False,
              returnsVerified=True, metalConflict=None)

REREADS = {
    "S01": dict(
        evidencePath=f"{EV}/spot.md",
        result="unchanged",
        observed=None,
        sourceExcerpt=(
            "Panel: 'Oct 24, 2026 - 23:14 NY Time'; Bid 3,994.90 USD (-28.20, -0.70%); Ask 3,996.90; "
            "ounce 3,994.90 (-28.20); gram 128.44 (-0.91); Kilo 128,440.99 (-906.65); pennyweight "
            "199.75 (-1.41); tola 1,498.09 (-10.58); tael 4,854.91 (-34.27); Day's Range 3975.10 - "
            "4040.20. 'Prices provided by Kitco Metals Inc. Displayed in U.S. dollars (USD), as of "
            "October 24, 2026 at 11:12 p.m. EDT.' Body text: 'The current price of gold is $3,994.90 "
            "per troy ounce as of October 24, 2026, 11:12 p.m. ET, down $28.40 today.' Purity table "
            "(update stamp 'Updated Oct 23, 2026 - 5:00 PM NY Time'): 24K $3,994.90; 22K $3,662.12; "
            "18K $2,996.18; 14K $2,330.23; 10K $1,664.67. Unit table: per ounce $3,994.90; per gram "
            "$128.44; per 10 grams $1,284.39; per kilo $128,439.02; per pennyweight $199.75; per tola "
            "$1,498.09; per tael $4,854.91. The embedded TradingView XAUUSD widget printed no close "
            "value at all this time (O/H/L/C rendered empty at 23:14:15 UTC-4); on 2026-10-23 the same "
            "widget printed 3,995.810 — disclosed under FL-25 and used nowhere. Week of Friday's "
            "5:00 PM NY close: values identical to the 2026-10-23 7:42 p.m. ET capture under a newer "
            "timestamp; 'A troy ounce is 31.1034768 grams'."
        ),
    ),
    # ---------------- Blue Nile (8/8 re-read; every field matched the canonical row) ----------------
    "L01": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1255, karat=14, **BN_OBS),
        sourceExcerpt=(
            "'$1,255(Setting Price)'; 'Metal Type:14K Yellow Gold'; Stock Number 502250y14; Metal "
            "14K Yellow Gold; Width 1.60mm; financing block 'Or as low as $213/mo for 6months with "
            "the Blue Nile Credit Card for a total payment of$1,280**'. Product Details: 'this 14k "
            "yellow gold solitaire …'. Warranty: 'We warrant all gold and platinum jewelry items with "
            "a purchase price of $1,000 or more from manufacturer's defect.' No gram weight, no "
            "explicit 'solid gold' wording, no karat-stamp or maker's-mark claim."
        ),
    ),
    "L02": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1000, karat=14, **BN_OBS),
        sourceExcerpt=(
            "'$1,000(Setting Price)'; 'Or as low as $170/mo for 6months … total payment of$1,020**'; "
            "Stock Number 501130y14; Metal 14K Yellow Gold; Width 1.80mm; 'Metal Type:14K Yellow Gold'. "
            "Product Details: 'this petite solitaire crafted in 14k gold …'. No grams, no 'solid "
            "gold' sentence, no stamp or maker's-mark claim."
        ),
    ),
    "L03": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=870, karat=14, **BN_OBS),
        sourceExcerpt=(
            "'$870(Setting Price)'; 'Special Financing available with the Blue Nile Credit Card.'; "
            "Stock Number 500000y14; Metal 14K Yellow Gold; Width 1.90mm; Product Details: 'classic "
            "14k yellow gold four-prong solitaire engagement ring with platinum prongs'. No grams, no "
            "'solid gold' sentence, no stamp claims."
        ),
    ),
    "L04": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1500, karat=14, **BN_OBS),
        sourceExcerpt=(
            "'$1,500(Setting Price)'; 'Or as low as $255/mo for 6months … total payment of$1,530**'; "
            "Stock Number 501590w14; Metal 14K White Gold; Width 2.00mm; Rhodium Finish Yes; "
            "'Diamond Type:Natural Diamond' with a lab-grown variant link (item-302867). Product "
            "Details: 'pavé-set diamonds set in 14k white gold'. No grams, no 'solid gold' sentence, "
            "no stamp claims."
        ),
    ),
    "L05": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1800, karat=14, **BN_OBS),
        sourceExcerpt=(
            "'$1,800(Setting Price)'; 'Or as low as $306/mo for 6months … total payment of$1,836**'; "
            "Stock Number 501410y14; Metal 14K Yellow Gold; Width 2.50mm; Product Details: 'French "
            "pavé-set diamonds set in 14k yellow gold'. No grams, no 'solid gold' sentence, no stamp "
            "claims."
        ),
    ),
    "L06": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=2320, **{**BN_OBS, "karat": 18}),
        sourceExcerpt=(
            "'$2,320(Setting Price)'; 'Or as low as $394/mo for 6months … total payment of$2,366**'; "
            "Stock Number 505032y; Metal 18K Yellow Gold; Width 8.45mm; 'Metal Type:18K Yellow Gold'. "
            "No grams, no 'solid gold' sentence, no stamp claims. Note: 18K price sits below the "
            "listing's own carat-range prompt (0.10 - 8.00 Carat) — setting price only."
        ),
    ),
    "L07": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=2210, karat=18, returnsVerified=True, metalConflict=(
            "Title and specification say 18K White Gold; Product Details say 14K Yellow Gold."),
            grams=None, solidStated=False, hallmarkStated=False, makerMarkStated=False),
        sourceExcerpt=(
            "'$2,210(Setting Price)'; 'Or as low as $376/mo for 6months … total payment of$2,254**'; "
            "Stock Number 502820w; Metal 18K White Gold; Width 1.70mm; Rhodium Finish Yes. Product "
            "Details still reads: 'This mesmerizing engagement ring is artfully crafted from warmly "
            "lustrous 14k yellow gold.' — the 18K/14K conflict is unchanged for a third consecutive "
            "pass and stays published as FL-30. Warranty line $1,000-or-more. No grams, no explicit "
            "'solid gold' wording, no stamp or maker's-mark claim."
        ),
    ),
    "L08": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1145, karat=14, **BN_OBS),
        sourceExcerpt=(
            "'$1,145(Setting Price)'; 'Or as low as $195/mo for 6months … total payment of$1,168**'; "
            "Stock Number 502120y14; Metal 14K Yellow Gold; Width 2.40mm; Product Details: 'this "
            "simple and elegant 14K yellow gold setting'. No grams, no 'solid gold' sentence, no "
            "stamp claims."
        ),
    ),
    # ---------------- Brilliant Earth: two rows re-read with the USD cell blank ----------------
    "L09": dict(
        evidencePath=f"{EV}/brilliant-earth.md", result="unchanged",
        observed=dict(price=None, grams=None, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (30-Day-Returns page not reachable for this session on "
                         "2026-10-25 — proxy failure; the product page's 'Free Shipping & Returns' "
                         "line is marketing, recorded as observed)"],
        sourceExcerpt=(
            "Page H1 'Freesia 2mm Solitaire Ring in 14K Yellow Gold'; price line served in EUR: "
            "'€\u200c835.00(Setting Only)'; wizard 'freesia 2mm solitaire-€\u200c835.00'; Ring "
            "Information: Style BE1343-14KY, Metal 14K Yellow Gold, Width 2-1.2 mm, Setting Claw "
            "Prong; banner 'ENDS SOON! Receive a €280.00 Gift Card With Purchase Over €1,150.00' "
            "while the promo image prints 'RECEIVE A USD$250 GIFT CARD WITH PURCHASE OVER USD$1,000' "
            "(mixed-currency render, FL-08); coverage block 'Free Shipping & Returns · Free Lifetime "
            "Warranty · Lifetime Diamond Upgrade · Free 1-Year Resizing'. No USD setting price was "
            "served to this session: the USD cell stays blank (no conversion), EUR recorded as "
            "observation only. No grams, no 'solid gold' sentence, no stamp claims."
        ),
    ),
    "L11": dict(
        evidencePath=f"{EV}/brilliant-earth.md", result="unchanged",
        observed=dict(price=None, grams=None, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (30-Day-Returns page not reachable for this session on "
                         "2026-10-25 — proxy failure; product-page coverage line is marketing)"],
        sourceExcerpt=(
            "Page H1 'Freesia Hidden Halo Diamond Ring in 14K Yellow Gold'; price line served in EUR: "
            "'€\u200c1,350.00(Setting Only)'; Ring Information: Style BE1D3939-14KY, Metal 14K Yellow "
            "Gold, Width 2-1.3 mm, Claw Prong; Accent Gemstones: 14 shared-prong round diamonds, min "
            "0.05 ctw, F/G, SI1. No USD setting price served: USD cell stays blank, no conversion."
        ),
    ),
    # ---------------- Allurez / Avianne / JM / SGJ (4 re-reads, all unchanged) ----------------
    "L13": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1085, grams=5.0, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (Allurez return-policy page not reachable for this session "
                         "on 2026-10-25 — proxy failure; product-page marketing line corroborates "
                         "only)"],
        sourceExcerpt=(
            "'$1,08557% Savings' and '$2,497Everyone Else' (marketing comparison, FL-09, not "
            "recorded as a price); 'Setting only. Center stone sold separately.'; 'Metal: 14k Yellow "
            "Gold'; 'Style number U5882'; 'Gold Weight 5.00 Grams (Approximate)'; Width '2.9mm (Top "
            "Width) 2.3mm (Bottom Width)'; Height '3.5mm (Top Height) 1.7mm (Bottom Height)'; "
            "'Crafted In the USA'; 'Shipping estimate: 10 to 14 business days'; marketing block "
            "'Easy Returns — Return or exchange within 30 days if unsatisfied.' No explicit 'solid "
            "gold' sentence, no karat-stamp claim, no maker's-mark claim."
        ),
    ),
    "L14": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=933, grams=4.8, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (Allurez return-policy page not reachable for this session "
                         "on 2026-10-25 — proxy failure)"],
        sourceExcerpt=(
            "'$93332% Savings' and '$1,373Everyone Else' (marketing comparison, FL-09); 'Setting "
            "only. Center stone sold separately.'; 'Metal: 14k Yellow Gold'; 'Metal Color Yellow "
            "Gold'; 'Style number U170'; 'Gold Weight 4.80 grams (Approximate)'; Width '3.20mm(Top "
            "Width), 2.40mm(Bottom Width)'; 'Crafted In the USA'; 'Please Note The center diamond is "
            "not included in the price of the ring'. No 'solid gold' sentence, no stamp claims."
        ),
    ),
    "L15": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=585, grams=3.58, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (Allurez return-policy page not reachable for this session "
                         "on 2026-10-25 — proxy failure)"],
        sourceExcerpt=(
            "Page H1 'Engraved Floral Solitaire Engagement Ring Setting 14K Yellow Gold'; '$58551% "
            "Savings' and '$1,194Everyone Else' (marketing comparison, FL-09); 'Setting only. Center "
            "stone sold separately.'; 'Metal: 14k Yellow Gold'; 'Style number NG4426'; 'Approximate "
            "Metal Weight 3.58 grams'; 'Crafted In the USA'. Size selector shows size-conditional "
            "surcharges '10.25 (+ $39)10.5 (+ $49)10.75 (+ $69)11 (+ $79)11.25 (+ $89)11.5 (+ $99)' "
            "— the recorded price is the base displayed price; no surcharge variant is blended in. "
            "No 'solid gold' sentence, no stamp claims."
        ),
    ),
    "L16": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=1100, grams=2.3, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "Page H1 '14K Solid Yellow Gold Diamond Solitaire Engagement Ring 0.41 Ctw'; "
            "'**$1,100.00**'; '**10% OFF WITH CODE \"FALL10\"**'; description 'handcrafted in 14k "
            "yellow gold … The frame measures to 4.5 mm in width and weighs 2.3 grams.'; DETAILS "
            "table 'Item Code R25893 … Metal Type 14K Gold … Item Weight 2.3 grams'; "
            "'Returns of unworn and unaltered items accepted within 14 days.'; 'Products delivered "
            "between Wed, 28 Oct and Sun, 01 Nov.'; 'Call Now 1 (332)-244-4038'; showroom '28 W 47th "
            "Street Diamond District · New York, NY'. Title states Solid; FALL10 promo not applied "
            "to the recorded price; returnsVerified stays False — the product page states a 14-day "
            "window but the dedicated policy page was not among this pass's reads."
        ),
    ),
    "L17": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=3020, grams=2.3, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "'Retail Price$6,041.00Special Price$3,020.00' — 3,020.00 recorded, 6,041.00 is the "
            "seller's own comparison (FL-12); 'Availability: In stock — Only 1 left'; 'Style 149700'; "
            "PRODUCT DETAILS 'This beautiful treasure is entirely handcrafted in pure 14KT solid "
            "yellow gold.'; Information table 'Carats: 0.71ctw … Metal Type: 14KT Gold; Metal Weight: "
            "2.3 Grams; Width: mm; Length: mm' (width/length printed empty → not recorded); "
            "'Money Back Guarantee (some restrictions apply)* … return or exchange your purchase "
            "within a 30-day period - no questions asked'; '0% APR or as low as $147/mo with Affirm.'; "
            "phone '1-888-59-JEWEL'. No dedicated return-policy page in this ledger → returnsVerified "
            "False."
        ),
    ),
    "L18": dict(
        evidencePath=f"{EV}/retailers.md", result="unchanged",
        observed=dict(price=None, grams=4.7, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "Page H1 'Yellow Gold Solitaire Engagement Ring'; spec line '14ky, 4.7g, #B02561'; 'SKU: "
            "B02561'; 'Brand: M Michael' recorded as store taxonomy, NOT as a maker's-mark claim; "
            "'Pricing and availability are subject to change.'; 'Call (309) 452-1612 for current "
            "pricing and availability.' — no price on the page, so the USD cell stays blank and "
            "flagged (FL-13); no return policy and no payment method stated."
        ),
    ),
    # ---------------- Etsy (7 re-reads; three prices corrected from these captures) ----------------
    "L19": dict(
        evidencePath=f"{EV}/etsy.md", result="unchanged",
        observed=dict(price=1891.78, grams=None, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        sourceExcerpt=(
            "'NowPrice:$1,202.08+' with 'Original Price: $2,404.16+' and '50% off' and 'Sale ends in "
            "15:11:39' (relative countdown captured — the time-left gap the previous pass asked to "
            "close); MATERIAL options '14K YELLOW GOLD ($1,891.78)', 10K ($1,686.02), 18K "
            "($2,109.58), 925 SILVER ($1,202.08); 'Low in stock, only 1 left'; 'Returns & exchanges "
            "accepted'; 'Band Width: 1.80 mm Approx.'; 'Metal Options: Available in 10K/14K/18K Solid "
            "Gold (White, Yellow, Rose Gold) & Platinum.'; RAKSHAKJEWELS Star Seller, 5/5. The 14K "
            "variant price is unchanged from 2026-10-23; the header compare-at belongs to another "
            "variant, so compareAt stays blank."
        ),
    ),
    "L20": dict(
        evidencePath=f"{EV}/etsy.md", result="corrected",
        observed=dict(price=546.18, grams=None, karat=14, solidStated=True, hallmarkStated=True,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        sourceExcerpt=(
            "'NowPrice:$375.86+' with 'Original Price: $626.44+' and '40% off' and 'Sale ends in 3 "
            "days'; 'Low in stock, only 1 left'; Material option '14K Yellow Gold ($546.18 - "
            "$2,405.36)' (14K White/Rose identical; 10K ($486.61 - $2,319.78); 18K ($594.00 - "
            "$2,445.63); platinum ($677.90 - $2,427.17); Silver ($375.86 - $2,274.48)); Centre "
            "Diamond Size 0.50 CT ($375.86 - $677.90) … 3.00 CT ($2,274.48 - $2,445.63); "
            "'Made with genuine 14k real gold – never plated or filled'; 'Metal stamp: Yes'; "
            "'Bandwidth: 1.50 MM'; 'Thickness: 1.40 MM'; 'Returns & exchanges accepted' · 'within 30 "
            "days'; 'Ships from: United Kingdom' · 'Free shipping'; ForeverForLove Star Seller 5/5. "
            "The 14K variant start moved from $546.09 (2026-10-23) to $546.18 — corrected from this "
            "capture; no 14K-specific compare-at is published, so compareAt stays blank."
        ),
    ),
    "L21": dict(
        evidencePath=f"{EV}/etsy.md", result="unchanged",
        observed=dict(price=969.0, grams=3.7, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        sourceExcerpt=(
            "'Price:$783.00+' · 'Original Price: $1,044.00+' · '25% off' · 'Limited time sale'; "
            "primary-colour options '14K YELLOW GOLD ($969.00)' (10K $783.00, 18K $1,233.00); "
            "FEATURES: 'Material: Solid Gold (not gold plated or gold filled)' · 'Karat: 14 K (585)' · "
            "'Diamond weight: 0.30 ct' · 'Ruby weight: 0.90 ct' · 'Gold grams: 3.70 gr' · 'Made to "
            "order' · 'All of our items are 14K real gold. We do not use any gold filled, gold plated "
            "or gold vermeil items.'; production partner 'Vera Atolye, Istanbul, Türkiye'; ships from "
            "'Albany, NY'; 'within 7 days' returns; VeraByEden Star Seller 5/5. The price block that "
            "was missing from the 2026-10-23 partial read is now read directly: $969.00 confirmed."
        ),
    ),
    "L22": dict(
        evidencePath=f"{EV}/etsy.md", result="corrected",
        observed=dict(price=246.35, grams=None, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        sourceExcerpt=(
            "Page title '14k Solid Yellow Gold Domed Wedding Band | 2mm - 8mm Gold Ring | Classic Dome "
            "Comfort Fit Wedding Band | Men and Women's Engraved Ring'; 'Etsy's Pick' · 'In 20+ "
            "carts'; 'NowPrice:$246.35+' · 'Original Price: $379.00+' · '35% off' · 'Sale ends in 1 "
            "day'; band-width ladder '2mm ($246.35 - $382.85) · 3mm ($330.85 - $525.85) · 4mm "
            "($460.85 - $740.35) · 5mm ($597.35 - $967.85) · 6mm ($740.35 - $1,195.35) · 7mm ($870.35 "
            "- $1,409.85) · 8mm ($1,000.35 - $1,630.85)'; 'Returns & exchanges accepted'; VibrantStone "
            "Star Seller 5/5. The 2mm ladder start moved from $251.30 (2026-10-23, '30% off "
            "$359.00') to $246.35 (2026-10-25, header 35% off $379.00+) — corrected from this capture; "
            "no gram weight published on the page."
        ),
    ),
    "L23": dict(
        evidencePath=f"{EV}/etsy.md", result="corrected",
        observed=dict(price=984.32, grams=None, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        sourceExcerpt=(
            "Page title '14K Solid Gold 8mm White Gold Polished Mens Womens Comfort Fit Dome Wedding "
            "Band'; 'NowPrice:$664.32+' · 'Original Price: $1,038.00+' · '36% off' · 'Sale ends in "
            "0:29:08' (under half an hour from expiry at read time — recorded, not projected); "
            "Material options '10K Gold ($664.32 - $949.12)' and '14K Gold ($984.32 - $1,347.84)'; "
            "size ladder from '3 US ($664.32 - $984.32)' to '13 US ($949.12 - $1,347.84)'; "
            "'Arrives soon! Get it by Oct 30-Nov 4'; 'Returns & exchanges accepted'; adelafinejewels "
            "Star Seller 5/5; optional engraving (0/40 characters). The 14K range moved from "
            "$999.70–$1,368.90 (35% off, 2026-10-23) to $984.32–$1,347.84 (36% off) — corrected from "
            "this capture; the $1,038 header compare-at belongs to the 10K base variant, so compareAt "
            "stays blank for the 14K row."
        ),
    ),
    "L24": dict(
        evidencePath=f"{EV}/etsy.md", result="unchanged",
        observed=dict(price=195.75, grams=None, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        sourceExcerpt=(
            "Page title '14k White Gold Classic Wedding Band, Flat Polished Comfort Fit Ring'; "
            "'NowPrice:$195.75+' · 'Original Price: $261.00+' · '25% off' · 'Sale ends in 0:29:08'; "
            "'12 views in the last 24 hours'; width ladder '2mm ($195.75 - $328.50) · 3mm ($337.50 - "
            "$580.50) · 4mm ($369.00 - $798.75) · 5mm ($429.75 - $942.75) · 6mm ($524.25 - "
            "$1,158.75)'; 'Returns & exchanges accepted'; CittaliFineJewelry 5/5. Every ladder figure "
            "matches the 2026-10-23 capture exactly; the description still lists other materials for "
            "the design, so the selected metal must be reconfirmed at checkout (FL-17)."
        ),
    ),
    "L25": dict(
        evidencePath=f"{EV}/etsy.md", result="unchanged",
        observed=dict(price=420.0, grams=None, karat=14, solidStated=True, hallmarkStated=True,
                      makerMarkStated=True, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "'This item is sold out.'; page title 'Fine 14K Solid White Gold Ring - 7g Solid Gold "
            "-Size 11- Comfort Fit Wedding Ring Band-Marked 14K'; 'Price:$420.00' · 'Original Price: "
            "$525.00'; 'Fine Solid 14K White Gold Wedding/Engagement Band'; 'marked 14K with a "
            "maker's mark. (Please see 4TH photo)'; 'The weight on my postal scale alternates between "
            "6-7 g.'; 'Was recently Rhodium Plated and in excellent condition'; 'Vintage from before "
            "2007'; 'I do not offer a refund for the following reasons: Buyers remorse / Changed mind "
            "/ Return postage'; BUTTERFLYWINGVINTAGE, Phoenix Arizona, 5.0 (802), 2.1k sales, 12 "
            "years. Sold-listing case study (FL-29); displayed $420.00 is not a current offer; title "
            "7 g vs 6-7 g scale range keeps exact grams blank."
        ),
    ),
    # ---------------- policies re-read today ----------------
    "P01": dict(
        evidencePath=f"{EV}/policies.md", result="unchanged", observed=None,
        sourceExcerpt=(
            "'# 30-DAY MONEY BACK GUARANTEE' … 'within 30 days from the shipment date for a full "
            "refund or exchange'; exclusions verbatim 'Personalized jewelry, custom orders, engraved "
            "items, items resized after initial purchase, Diamond Upgrade Program purchases, "
            "clearance items and \"Final Sale\" items are not eligible for return or exchange.'; "
            "'Two complimentary returns are allowed per customer, per year'; 'RMA number is required'; "
            "'The cost to replace a missing diamond grading report is $150'; 'Eligible rings receive "
            "one free resize, up or down two sizes, within 6 months of purchase if the design "
            "permits.' — the canonical BN_RETURNS string is fully re-confirmed today."
        ),
    ),
    "P02": dict(
        evidencePath=f"{EV}/policies.md", result="unchanged", observed=None,
        sourceExcerpt=(
            "'# LIMITED LIFETIME WARRANTY — Effective Oct 11, 2026'; 'Blue Nile warrants gold and "
            "platinum jewelry items with a purchase price of $1,000.00 or more against manufacturing "
            "defects for as long as you own the jewelry.'; non-coverage list (items under $1,000.00, "
            "pearl/silver/alternative-metal jewellery, lost or damaged stones, misuse, loss/theft); "
            "'For up to 6 months … one-time free ring resizing, up or down two sizes if the design "
            "permits'; non-transferable; unauthorised repair voids coverage."
        ),
    ),
}

# The four BE pages opened today but not confirmable in USD → partial reads (rows keep their
# dated 2026-10-23 canonical check; BE-1343/BE-1343HH rows were re-read outright because the
# blank USD cell IS today's observed state).
PARTIALS = [
    dict(
        entryId="BE-NADIA", canonicalCheck="L10",
        url="https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/",
        checkedOn=CHECKED_ON, readBy=SESSION,
        evidencePath=f"{EV}/brilliant-earth.md",
        retrieved=("Page opened 2026-10-25: H1 'Nadia Diamond Ring in 14K Yellow Gold'; price line "
                   "served in EUR only: '€\u200c1,400.00(Setting Only)'; wizard 'nadia-€\u200c1,400.00'; "
                   "Product Details '1.8mm band width', 'Marquise and round diamond accents … (0.06 "
                   "and 0.05 ct. tw.)'; coverage 'Free Shipping & Returns · Free Lifetime Warranty · "
                   "Lifetime Diamond Upgrade · Free 1-Year Resizing'; 'ships by Mon, Nov 16'."),
        notRetrieved=("No USD setting price was served to this session (EUR render, German locale "
                      "strip). The canonical USD price could not be confirmed at today's date."),
        effect=("Corroboration plus a dated EUR observation. The $1,250.00 USD figure remains the "
                "2026-10-23 read (canonical check L10, readBy bc4e36a1 (inherited)) and the row is "
                "now labelled provenance=prior, dated 2026-10-23, flagged FL-08 and FL-33 on the "
                "site. No EUR→USD conversion was performed. Title, karat and band width were "
                "re-confirmed today and match the canonical row exactly."),
    ),
    dict(
        entryId="BE-SECRET", canonicalCheck="L12",
        url="https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/",
        checkedOn=CHECKED_ON, readBy=SESSION,
        evidencePath=f"{EV}/brilliant-earth.md",
        retrieved=("Page opened 2026-10-25: H1 'Secret Halo 1.5mm Diamond Ring in 14K Yellow Gold'; "
                   "price line served in EUR only: '€\u200c1,250.00(Setting Only)'; Ring Information "
                   "Style BE1D13065-14KY, Metal 14K Yellow Gold, Width 1.5 mm, Claw Prong; '13 round "
                   "diamonds (0.06 ct. tw.)'; 'ships by Mon, Nov 16'."),
        notRetrieved=("No USD setting price served (EUR render). The canonical USD price could not be "
                      "confirmed at today's date."),
        effect=("Corroboration plus a dated EUR observation. The $1,090.00 USD figure remains the "
                "2026-10-23 read (canonical check L12, readBy bc4e36a1 (inherited)); row labelled "
                "provenance=prior, dated 2026-10-23, flagged FL-08 and FL-33. No conversion. Title, "
                "karat and 1.5 mm width re-confirmed today and match the canonical row exactly."),
    ),
]

def _failures():
    """One record per URL (seq F1…Fn), grouped by the narrative IDs F1–F6 in the evidence file."""
    raw = [
        ("F1", "proxy-transient-then-recovered",
         "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
         "fetch proxy SignatureDoesNotMatch on the first attempt (~03:26 UTC)",
         "Retried immediately and succeeded; recorded as L25. A proxy error is not a dead link, so this URL is not reported as unreachable."),
        ("F1", "proxy-transient-then-recovered",
         "https://www.bluenile.com/policies/returns",
         "fetch proxy SignatureDoesNotMatch on the first attempt (~03:26 UTC)",
         "Retried immediately and succeeded; recorded as P01, re-confirmed BN_RETURNS verbatim."),
        ("F2", "proxy-transient-then-recovered",
         "https://www.bluenile.com/services/warranty",
         "fetch proxy SignatureDoesNotMatch on two attempts",
         "Succeeded on the third attempt; recorded as P02, including the 'Effective Oct 11, 2026' header."),
        ("F3", "proxy-failed-not-reread",
         "https://www.bluenile.com/contact-us",
         "fetch proxy SignatureDoesNotMatch on 2 attempts",
         "P03 NOT re-read; the 2026-10-23 bc4e36a1 check is kept, labelled inherited, flagged FL-33. No contact detail was re-confirmed today."),
        ("F4", "proxy-failed-not-reread",
         "https://www.brilliantearth.com/30-Day-Returns/",
         "fetch proxy SignatureDoesNotMatch on 2 attempts",
         "P04 NOT re-read; the 2026-10-23 check is kept and labelled inherited (FL-33). The BE product pages opened today display the 'Free Shipping & Returns' coverage line — marketing corroboration only, recorded as such."),
        ("F4", "proxy-failed-not-reread",
         "https://www.brilliantearth.com/customer-service/warranty/#manufacturing_warranty",
         "fetch proxy SignatureDoesNotMatch in a batched attempt",
         "P05 NOT re-read; 2026-10-23 check kept, labelled inherited (FL-33)."),
        ("F4", "not-attempted-after-outage",
         "https://www.brilliantearth.com/contact/",
         "not attempted once the proxy began failing for every URL",
         "P06 NOT re-read; 2026-10-23 check kept, labelled inherited (FL-33). Recorded as not attempted — never dressed up as a failed fetch."),
        ("F5", "proxy-failed-not-reread",
         "https://www.allurez.com/pages/return-policy",
         "fetch proxy SignatureDoesNotMatch on 2 attempts",
         "P07 NOT re-read; 2026-10-23 check kept, labelled inherited (FL-33). The Allurez product pages re-read today show 'Return or exchange within 30 days if unsatisfied' — marketing corroboration, not a policy read."),
        ("F5", "not-attempted-after-outage",
         "https://www.allurez.com/pages/warranty",
         "not attempted once the outage began",
         "P08 NOT re-read; 2026-10-23 check kept, labelled inherited (FL-33)."),
        ("F5", "not-attempted-after-outage",
         "https://www.allurez.com/pages/contact",
         "not attempted once the outage began",
         "P09 NOT re-read; 2026-10-23 check kept, labelled inherited (FL-33)."),
    ]
    refs = [
        ("https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry", "R01", "attempt failed with SignatureDoesNotMatch"),
        ("https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23", "R02", "not attempted after the outage began"),
        ("https://www.govinfo.gov/link/uscode/15/295", "R03", "not attempted after the outage began"),
        ("https://www.law.cornell.edu/cfr/text/16/23.3", "R04", "not attempted after the outage began"),
        ("https://www.govinfo.gov/link/uscode/15/297", "R05", "not attempted after the outage began"),
        ("https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8", "R06", "not attempted after the outage began"),
        ("https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices", "R07", "not attempted after the outage began"),
        ("https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges", "R08", "not attempted after the outage began"),
        ("https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program", "R09", "not attempted after the outage began"),
        ("https://jvclegal.org/mediation-services/", "R10", "not attempted after the outage began"),
        ("https://reportfraud.ftc.gov/", "R11", "not attempted after the outage began"),
    ]
    out = [dict(seq=f"F{i}", group=g, kind=k, url=u, result=r, handling=h)
           for i, (g, k, u, r, h) in enumerate(raw, start=1)]
    for j, (u, rid, how) in enumerate(refs):
        out.append(dict(seq=f"F{len(raw) + 1 + j}", group="F6", kind="proxy-failed" if how.startswith("attempt") else "not-attempted-after-outage",
                        url=u,
                        result=f"{rid}: {how} — the proxy failed for every URL attempted after ~03:30 UTC, including a Blue Nile page that had served normally 20 minutes earlier",
                        handling=f"{rid} NOT re-read on 2026-10-25; the 2026-10-23 check is kept byte-identical, labelled inherited and flagged FL-33. Statutory and regulatory texts do not expire overnight, but the gap is disclosed rather than hidden."))
    return out


FAILURES = _failures()

CORRECTIONS = [
    dict(id="C-20", subject="ET-4366425533 price", before="$546.09 (2026-10-23 14K variant start)",
         after="$546.18 (2026-10-25 '14K Yellow Gold ($546.18 - $2,405.36)')",
         reason="Direct re-read of the official listing page; the seller reprised the 14K ladder.",
         session=SESSION),
    dict(id="C-21", subject="ET-1566052947 price",
         before="$251.30 (2026-10-23 'From $251.30 (2 mm, 30% off $359.00)')",
         after="$246.35 (2026-10-25 'NowPrice:$246.35+'; 2mm ladder starts $246.35; header 35% off "
               "$379.00+)",
         reason="Direct re-read; promo depth and base price both changed.", session=SESSION),
    dict(id="C-22", subject="ET-1433905613 price",
         before="$999.70 (2026-10-23 14K range $999.70–$1,368.90, 35% off)",
         after="$984.32 (2026-10-25 '14K Gold ($984.32 - $1,347.84)', 36% off)",
         reason="Direct re-read; 10K range also moved to $664.32–$949.12.", session=SESSION),
    dict(id="C-23", subject="Spot quote timestamp",
         before="primary quote 'as of October 23, 2026 at 7:42 p.m. EDT' ($3,994.90 / $128.44)",
         after="re-confirmed at 'Oct 24, 2026 - 23:14 NY Time' / 'as of October 24, 2026 at 11:12 "
               "p.m. EDT' — identical $3,994.90 / $128.44 because the market had not reopened after "
               "the Friday 5:00 PM NY close",
         reason="Newer read of the same values; the older capture moves to the dated prior chain. No "
                "derived value changes.", session=SESSION),
]


def main() -> int:
    with open(BASE, encoding="utf-8") as f:
        base = json.load(f)
    ledger = copy.deepcopy(base)

    by_id = {c["id"]: c for c in ledger["checks"]}
    if set(REREADS) - set(by_id):
        sys.exit(f"unknown check ids in REREADS: {sorted(set(REREADS) - set(by_id))}")

    n_reread = 0
    for cid, over in REREADS.items():
        c = by_id[cid]
        c["evidencePath"] = over["evidencePath"]
        c["result"] = over["result"]
        c["sourceExcerpt"] = over["sourceExcerpt"]
        c["checkedOn"] = CHECKED_ON
        c["readBy"] = SESSION
        if "observed" in over:
            if over["observed"] is None:
                c.pop("observed", None)
            else:
                c["observed"] = dict(over["observed"])
            if "inheritedFields" in over:
                c["inheritedFields"] = list(over["inheritedFields"])
            else:
                c.pop("inheritedFields", None)
        c.pop("inheritedNote", None)
        n_reread += 1

    for c in ledger["checks"]:
        if c["id"] in REREADS:
            continue
        first = c.get("firstCapturedBy") or ("6d10ac0a" if c.get("readBy") == "6d10ac0a" else "bc4e36a1")
        c["readBy"] = f"{first} (inherited)"
        c["firstCapturedBy"] = first
        if c["id"] in ("L10", "L12"):
            c["inheritedNote"] = (
                "Captured 2026-10-23 by session bc4e36a1 — the direct USD read of the setting price. "
                "Session 3dfe4d85 opened this exact page again on 2026-10-25, but the page served EUR "
                "(€1,400.00 / €1,250.00) and printed no USD price, so the USD figure could not be "
                "re-confirmed; it is kept at 2026-10-23 as a dated prior observation and the partial "
                "read is logged in partialReads. No conversion was performed.")
        else:
            c["inheritedNote"] = INHERIT_NOTES[first]
        # The two BE rows whose USD price could not be re-confirmed keep their canonical
        # 2026-10-23 check untouched (status read, original evidence) — the EUR observation
        # this session made lives in partialReads so nothing is presented as a fresh read.

    ledger["schemaVersion"] = 1
    ledger["session"] = SESSION
    ledger["branch"] = BRANCH
    ledger["checkedOn"] = CHECKED_ON
    ledger["method"] = (
        "26 of the 46 checks (Kitco spot, 23 listing pages, 2 Blue Nile policy pages) were re-opened "
        "live on 2026-10-25 with fetch_page and transcribed field by field into "
        "verification/evidence/3dfe4d85/ before any canonical value was touched. The remaining 20 "
        "checks — 2 Brilliant Earth listing reads whose USD price was not served today, 7 policy "
        "pages and 11 official references the fetch proxy failed for or that were not attempted "
        "after the outage began — are inherited unchanged from data/live_check_6d10ac0a.json "
        "(2026-10-23) with readBy labels naming the session that actually read them and an "
        "inheritedNote explaining the date. Two partial reads (BE-NADIA, BE-SECRET) and six failure "
        "records (F1–F6) are published below; nothing hidden by the outage is presented as read."
    )
    ledger["timeNote"] = (
        "Only the retrieval date is asserted for fetches. A time is recorded only where the source "
        "itself displayed one (Kitco's panel timestamp 'Oct 24, 2026 - 23:14 NY Time' and its body "
        "sentence 'as of October 24, 2026, 11:12 p.m. ET'). Etsy sale figures are relative "
        "countdowns captured at read time; no absolute expiry instant is recorded because none is "
        "published."
    )
    ledger["noHallucinations"] = (
        "Blank means unverified. A source conflict is published, not resolved by preference. "
        "Inherited reads keep their original dates, evidence ids and paths and are labelled with the "
        "session that actually made them. No EUR figure was converted to USD anywhere. Derived "
        "values are recomputed from the canonical inputs by script and re-checked by "
        "scripts/verify.py, scripts/independent_audit.py and tools/security_test.py."
    )
    n_inherited = len(ledger["checks"]) - n_reread
    ledger["coverage"] = dict(
        listing=25, policy=9, reference=11, spot=1, total=len(ledger["checks"]),
        rereadThisPass=n_reread, inheritedFromEarlierPass=n_inherited,
        partialReads=len(PARTIALS), scopeReads=len(ledger.get("scopeReads", [])),
        failuresLogged=len(FAILURES),
    )
    ledger["inherits"] = dict(
        session="6d10ac0a + bc4e36a1",
        ledger="data/live_check_6d10ac0a.json (overlaying data/live_check_bc4e36a1.json)",
        checkedOn="2026-10-23",
        note=("20 of the 46 checks were captured on 2026-10-23 by earlier sessions and are carried "
              "forward byte-identical with readBy='<session> (inherited)'. They are never relabelled "
              "as this session's reads. 26 checks (1 spot + 23 listings + 2 policies) were re-opened "
              "live by session 3dfe4d85 on 2026-10-25."),
    )
    ledger["corrections"] = CORRECTIONS
    ledger["partialReads"] = PARTIALS
    ledger["failures"] = FAILURES

    # sanity: every listing entry covered exactly once; two inherited listing checks are the BE pair
    listing = [c for c in ledger["checks"] if c.get("kind") == "listing"]
    assert len(listing) == 25 and len({c["entryId"] for c in listing}) == 25
    inh_listings = {c["entryId"] for c in listing if not c.get("readBy", "").startswith(SESSION)}
    assert inh_listings == {"BE-NADIA", "BE-SECRET"}, inh_listings
    assert ledger["coverage"]["total"] == 46

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {OUT}: {ledger['coverage']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
