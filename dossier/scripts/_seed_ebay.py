import json
SNIP="2026-10-22T23:31:00Z"
rows=[]
def r(**kw):
    base=dict(id=None,retailer=None,seller=None,product=None,url=None,category=None,karat=None,metal=None,
              metal_claim=None,stone=None,price_usd=None,price_note=None,list_price_usd=None,currency="USD",
              weight_grams=None,width_mm=None,stock_number=None,captured_at=SNIP,return_policy=None,
              evidence=dict(tier="snippet",excerpt=None,source_url=None,observed_at=SNIP,page_date=None),
              flags=[],notes=None)
    base.update(kw); rows.append(base)

def eb(**kw):
    kw.setdefault("retailer","eBay (marketplace)")
    base_flags=["MARKETPLACE: individual third-party seller - verify seller reputation, contact details and return policy independently",
                "Price from search-index snippet of the official ebay.com item page; NOT re-confirmed by live fetch (fetch proxy outage at capture time)"]
    kw["flags"]=base_flags+kw.get("extra_flags",[])
    kw.pop("extra_flags",None)
    r(**kw)

eb(id="EBAY-117322068337", product="14K SOLID GOLD .47 ct. Natural Diamond Engagement Wedding Ring Set, Size 6.75",
   url="https://www.ebay.com/itm/117322068337", category="bridal-set", karat="14K", metal="14K solid yellow gold",
   metal_claim="Seller states: '14K SOLID YELLOW GOLD diamond bridal set. It weighs 3.8 grams.'",
   stone="Natural diamond, total carat weight 0.25-0.49 ctw (item specifics)", price_usd=599.95,
   price_note="'US $599.95 or Best Offer' - Best Offer means price is negotiable",
   weight_grams=3.8, seller="Brand listed as CRESCENDO (item specifics)",
   evidence=dict(tier="snippet", excerpt="Pictured is a 14K SOLID YELLOW GOLD diamond bridal set. It weighs 3.8 grams. ... US $599.95 or Best Offer ... Metal: Yellow Gold ... Total Carat Weight: 0.25 ctw - 0.49 ctw ... Brand: CRESCENDO ... Setting Style: Solitaire with Accents",
                 source_url="https://www.ebay.com/itm/117322068337", observed_at=SNIP, page_date="2026-09-25 (index crawl date reported by search)"),
   notes="Seller publishes gram weight - satisfies the checklist 'weight in grams' item. Hallmark/maker's mark not evidenced on the listing page.")

eb(id="EBAY-306024152911", product="Beautiful Solid 14k Rose Gold Solitaire Diamond Engagement Promise Ring sz 7.25",
   url="https://www.ebay.com/itm/306024152911", category="solitaire", karat="14K", metal="14K solid rose gold",
   metal_claim="Seller states: 'Marked: \"585\" (585=14k gold)'; item specifics Metal Purity: 14k, Metal: Rose Gold",
   stone="Diamond 0.20 ct, round", price_usd=339.99, weight_grams=2.0, seller="Brand: Unbranded (item specifics)",
   evidence=dict(tier="snippet", excerpt='Marked: "585" (585=14k gold). Diamond: 20pts or 0.20ct. Weight: 2.0 grams. ... {"name":"Beautiful Solid 14k Rose Gold Solitaire Diamond Engagement Promise Ring sz 7.25","offers":{"priceCurrency":"USD","price":"339.99"}} ... US $339.99 ... Metal Purity: 14k',
                 source_url="https://www.ebay.com/itm/306024152911", observed_at=SNIP, page_date="2025-10-14 (index crawl date reported by search - over 12 months old)"),
   extra_flags=["STALE INDEX: search engine reports this page was crawled 2025-10-14; the $339.99 price may no longer be current",
                "Brand listed as 'Unbranded' - no maker's mark evidenced"],
   notes="Price is embedded in schema.org JSON-LD on the official eBay item page (offers.price = 339.99, priceCurrency USD), which is the strongest machine-readable form of the seller's own price claim.")

eb(id="EBAY-236302217681", product="14k solid gold ring Engagement - Anillo en oro compromiso 14 kilates autentico",
   url="https://www.ebay.com/itm/236302217681", category="plain-band", karat="14K", metal="14K yellow gold",
   metal_claim="Item specifics: Metal Purity 14k; Metal Yellow Gold; Main Stone: No Stone",
   stone="No stone (plain gold band)", price_usd=421.88, seller="Brand: Unbranded (item specifics); Condition: New with packaging",
   evidence=dict(tier="snippet", excerpt="US $421.88 ... Condition: New with packaging ... Brand: Unbranded ... Ring Size: 7 ... Type: Engagement Ring ... Metal Purity: 14k ... Metal: Yellow Gold ... Main Stone: No Stone",
                 source_url="https://www.ebay.com/itm/236302217681", observed_at=SNIP, page_date="2026-04-30 (index crawl date reported by search)"),
   extra_flags=["Gram weight NOT published - ask the seller before buying",
                "No maker's/hallmark evidence on the listing page",
                "Brand 'Unbranded'"],
   notes="Plain solid-gold engagement band with no stone: the simplest case for the melt-value calculator, but the seller does not publish the gram weight, so gold content cannot be computed from this listing alone.")

eb(id="EBAY-236156740362", product="14k SOLID Gold Diamond Ring .50 TCW Sz 13 Modernist Design 5.6Gr.",
   url="https://www.ebay.com/itm/236156740362", category="vintage", karat="14K", metal="14K solid yellow gold",
   metal_claim="Title states '14k SOLID Gold'; description states 'Total weight of the ring is: 5.6 grams.'",
   stone="Diamonds 0.54 TCW combined (6 x 0.24 TCW + 2 x 0.30 TCW) per seller description", price_usd=2600.00,
   price_note="'US $2,600.00 or Best Offer'", weight_grams=5.6, seller="Brand: Unbranded (item specifics)",
   evidence=dict(tier="snippet", excerpt="There are 6 diamonds adding to a total carat weight of 0.24 TCW and 2 central diamonds adding to a total carat weight of 0.30 TCW, for a total combined carat weight of 0.54 TCW. Total weight of the ring is: 5.6 grams. ... US $2,600.00 or Best Offer",
                 source_url="https://www.ebay.com/itm/236156740362", observed_at=SNIP, page_date="2025-11-19 (index crawl date reported by search - over 11 months old)"),
   extra_flags=["STALE INDEX: crawled 2025-11-19; price and availability may have changed",
                "Title says '.50 TCW' but the description totals 0.54 TCW - internal inconsistency in the seller's own listing"],
   notes="Gram weight published (5.6 g) so gold content can be computed. Note the carat-weight discrepancy between title and description - a documentation red flag.")

eb(id="EBAY-387266085584", product="14K Solid White Gold 3 Ct IGI Lab-Grown E-F/VS Diamond Solitaire Engagement Ring",
   url="https://www.ebay.com/itm/387266085584", category="solitaire", karat="14K", metal="14K solid white gold",
   metal_claim="Title states '14K Solid White Gold'", stone="3 ct IGI-certified lab-grown diamond, E-F colour / VS clarity",
   price_usd=2479.99, price_note="'US $2,479.99'; page also shows '$2,440.99 with coupon code'",
   evidence=dict(tier="snippet", excerpt="14K Solid White Gold 3 Ct IGI Lab-Grown E-F/VS Diamond Solitaire Engagement Ring ... US $2,479.99 ... $2,440.99 with coupon code Price details",
                 source_url="https://www.ebay.com/itm/387266085584", observed_at=SNIP, page_date="2026-10-16 (index crawl date reported by search - 6 days before capture)"),
   extra_flags=["Gram weight NOT published", "IGI certificate referenced in title only - certificate number/report not evidenced in the captured excerpt"])

eb(id="EBAY-318634765232", product="Solid 14K Gold 3-Stone Engagement Ring 2.35 Carat Round Lab-Grown Diamond E SI1",
   url="https://www.ebay.com/itm/318634765232", category="three-stone", karat="14K", metal="Solid 14K gold",
   metal_claim="Item specifics: Metal Purity 14K", stone="2.35 ct round lab-grown diamond, E colour / SI1 clarity",
   price_usd=2392.92, list_price_usd=5777.60, price_note="'US $2,392.92 or Best Offer'; list price US $5,777.60 shown as 59% off",
   evidence=dict(tier="snippet", excerpt="Solid 14K Gold 3-Stone Engagement Ring 2.35 Carat Round Lab-Grown Diamond E SI1 ... US $2,392.92 or Best Offer ... List price US $5,777.60 (59% off) ... Metal Purity: 14K ... Ring Size: 6.5 (Free Resizing) ... Country of Origin: United States",
                 source_url="https://www.ebay.com/itm/318634765232", observed_at=SNIP, page_date="2026-08-12 (index crawl date reported by search)"),
   extra_flags=["Gram weight NOT published", "59% off a seller-supplied 'list price' - the reference price is set by the seller, not an independent market",
                "'Free Resizing' offered - confirm in writing whether a resized ring is still returnable (checklist item)"])

eb(id="EBAY-377449988374", product="Solitaire Engagement Ring Solid 14K Gold 2.96 CT Round Lab-Grown Diamond G SI1",
   url="https://www.ebay.com/itm/377449988374", category="solitaire", karat="14K", metal="Solid 14K gold",
   metal_claim="Item specifics: Metal Purity 14K", stone="2.96 ct round lab-grown diamond, G colour / SI1 clarity, Excellent cut",
   price_usd=3190.86, list_price_usd=6158.50, price_note="'US $3,190.86 or Best Offer'; page itemises List price US $6,158.50 (48% off) -US $2,967.64, Shipping FREE, Estimated total US $3,190.86",
   evidence=dict(tier="snippet", excerpt="Solitaire Engagement Ring Solid 14K Gold 2.96 CT Round Lab-Grown Diamond G SI1 ... US $3,190.86 or Best Offer ... List price US $6,158.50 (48% off) ... Item price US $3,190.86 ... Estimated total US $3,190.86 ... Metal Purity: 1 4K G old ... Country of Origin: United States",
                 source_url="https://www.ebay.com/itm/377449988374", observed_at=SNIP, page_date="2026-10-09 (index crawl date reported by search)"),
   extra_flags=["Gram weight NOT published", "48% off a seller-supplied list price"])

eb(id="EBAY-366418663601", product="14K Solid Gold Oval Cut Moissanite Engagement Ring, Dainty Side Proposal Ring",
   url="https://www.ebay.com/itm/366418663601", category="gemstone", karat="14K", metal="14K solid gold",
   metal_claim="Title states '14K Solid Gold'", stone="Moissanite (NOT a diamond)", price_usd=1262.91,
   list_price_usd=1419.00, price_note="'US $1,262.91 or Best Offer'; Was US $1,419.00 (11% off), described by eBay as 'Recent sales price provided by the seller'",
   evidence=dict(tier="snippet", excerpt="14K Solid Gold Oval Cut Moissanite Engagement Ring, Dainty Side Proposal Ring ... US $1,262.91 or Best Offer ... Was US $1,419.00 (11% off) What does this price mean? Recent sales price provided by the seller",
                 source_url="https://www.ebay.com/itm/366418663601", observed_at=SNIP, page_date="2026-09-27 (index crawl date reported by search)"),
   extra_flags=["Center stone is MOISSANITE, not diamond - do not compare its price with diamond rings",
                "Gram weight NOT published",
                "eBay itself labels the 'Was' price as 'Recent sales price provided by the seller' - i.e. the discount reference is seller-supplied"],
   notes="Useful example of eBay's own disclosure that a strikethrough price is seller-supplied rather than independently verified.")

# ---- RED FLAG ROWS (still official ebay.com pages, but the listing claims are internally inconsistent / implausible) ----
eb(id="EBAY-162731672251", product="Sale GoLD 14k ring 3 carat Round solid wide thick Engagement 6 ! ask 7 5 8 9",
   url="https://www.ebay.com/itm/162731672251", category="red-flag", karat="14K (claimed in title only)",
   metal="Claimed 14k yellow gold; item specifics list Metal: Yellow Gold, Brand: No Brand",
   metal_claim="Karat claimed in the title only; no hallmark, maker's mark or gram weight evidenced",
   stone="Ambiguous - title says '3 carat Round' without stating whether that is a diamond, a simulant, or a gold-weight description",
   price_usd=1351.01, price_note="'US $1,351.01 or Best Offer'",
   evidence=dict(tier="snippet", excerpt="Sale GoLD 14k ring 3 carat Round solid wide thick Engagement 6 ! ask 7 5 8 9 ... US $1,351.01 or Best Offer ... Condition ... Brand: No Brand ... Metal: Yellow Gold",
                 source_url="https://www.ebay.com/itm/162731672251", observed_at=SNIP, page_date="2026-01-30 (index crawl date reported by search)"),
   extra_flags=["RED FLAG - ambiguous title: '3 carat' is not identified as diamond, simulant or gold weight",
                "RED FLAG - 'No Brand': no maker's mark, which 15 U.S.C. 297 / 16 CFR 23.10 expect alongside a karat quality mark",
                "RED FLAG - no gram weight published, so gold content cannot be checked against the price",
                "RED FLAG - inconsistent capitalisation and multiple ring sizes in one listing ('6 ! ask 7 5 8 9')"],
   notes="Included deliberately as a training example of a listing that fails several checklist items at once. Do NOT buy without independent verification.")

eb(id="EBAY-BN7024729510-LUX750", product="Luxury 7.50 Ct Oval Cut Lab Grown Diamond Engagement Ring Solid 14K Yellow Gold",
   url="https://www.ebay.com/b/mens-14k-solid-gold-diamond-ring/bn_7024729510", category="red-flag",
   karat="14K (claimed in title only)", metal="Claimed solid 14K yellow gold",
   metal_claim="Title claims 'Solid 14K Yellow Gold'; no hallmark, maker's mark or gram weight in the captured excerpt",
   stone="Claimed 7.50 ct oval lab-grown diamond", price_usd=322.27, list_price_usd=495.80,
   price_note="'$322.27 Was: $495.80 or Best Offer'", seller="Listed as Unbranded, New (Other)",
   evidence=dict(tier="snippet", excerpt="Luxury 7.50 Ct Oval Cut Lab Grown Diamond Engagement Ring Solid 14K Yellow Gold New (Other) - Unbranded $322.27 Was: $495.80 was - US $495.80 or Best Offer Free shipping 70 watching",
                 source_url="https://www.ebay.com/b/mens-14k-solid-gold-diamond-ring/bn_7024729510", observed_at=SNIP, page_date=None),
   extra_flags=["RED FLAG - implausible price: a 7.50 ct lab-grown diamond ring in solid 14K gold offered at $322.27",
                "RED FLAG - URL is an eBay CATEGORY page, not a single item page: the individual listing URL and seller must be confirmed before any purchase",
                "RED FLAG - condition 'New (Other)' and 'Unbranded'",
                "UNVERIFIED - price is shown on an aggregate category page; it is not attributable to a stable item URL"],
   notes="Price-to-claim ratio is the single strongest fraud signal in this dataset. Kept as a documented red-flag example, NOT as a recommended purchase.")

eb(id="EBAY-BN7024729510-KARATCONFLICT", product="Mens 14k Gold Diamond Band Engagement Wedding Ring 1CT Natural Diamond Solid 10k",
   url="https://www.ebay.com/b/mens-14k-solid-gold-diamond-ring/bn_7024729510", category="red-flag",
   karat="CONFLICTING: title says 14k and also says 'Solid 10k'", metal="Claimed gold; karat contradictory",
   metal_claim="The seller's own title contains two different karat claims ('14k' and 'Solid 10k')",
   stone="Claimed 1 ct natural diamond", price_usd=4046.74, seller="Brand New, Authenticity Guarantee shown in listing strip",
   evidence=dict(tier="snippet", excerpt="Mens 14k Gold Diamond Band Engagement Wedding Ring 1CT Natural Diamond Solid 10k Brand New $4,046.74 Free shipping 4 watching Authenticity Guarantee",
                 source_url="https://www.ebay.com/b/mens-14k-solid-gold-diamond-ring/bn_7024729510", observed_at=SNIP, page_date=None),
   extra_flags=["RED FLAG - self-contradictory karat claim in the seller's own title (14k vs 10k)",
                "RED FLAG - URL is an eBay CATEGORY page, not a single item page",
                "Per 16 CFR 23.3 it is unfair or deceptive to misrepresent gold content; a contradictory karat claim should be treated as a stop signal"],
   notes="Demonstrates why the checklist says a karat stamp or claim alone does not prove purity: here the claim contradicts itself before the item even arrives.")

with open("data/rings.jsonl","a",encoding="utf-8") as f:
    for x in rows: f.write(json.dumps(x,ensure_ascii=False)+"\n")
print("appended",len(rows))
