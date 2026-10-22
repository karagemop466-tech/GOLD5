import json
SNIP="2026-10-22T23:40:00Z"
rows=[]
def r(**kw):
    base=dict(id=None,retailer=None,seller=None,product=None,url=None,category=None,karat=None,metal=None,
              metal_claim=None,stone=None,price_usd=None,price_note=None,list_price_usd=None,currency="USD",
              weight_grams=None,width_mm=None,stock_number=None,captured_at=SNIP,return_policy=None,
              evidence=dict(tier="snippet",excerpt=None,source_url=None,observed_at=SNIP,page_date=None),
              flags=[],notes=None)
    base.update(kw); rows.append(base)

NO_PRICE=["PRICE LEFT BLANK / UNVERIFIED: no price appeared in the captured evidence for this listing. Per project rule it is NOT estimated or inferred.",
          "MARKETPLACE: individual third-party seller - verify seller reputation, contact details and return policy independently",
          "Price from search-index snippet of the official ebay.com item page; NOT re-confirmed by live fetch (fetch proxy outage at capture time)"]

r(id="EBAY-126886617045", retailer="eBay (marketplace)",
  product="14K White Gold Diamond Halo Engagement Ring - 0.94 CTW (Kay Jewelers)",
  url="https://www.ebay.com/itm/126886617045", category="halo-pave", karat="14K", metal="14K white gold",
  metal_claim="Item specifics: Metal Weight 3.8dwt / 5.90 Grams; brand identified as Kay Jewelers in the listing title",
  stone="Natural diamond; total carat weight 1.12 ctw; 85 secondary stones; secondary stone clarity SI1-SI2",
  weight_grams=5.90, captured_at=SNIP,
  evidence=dict(tier="snippet", excerpt="14K White Gold Diamond Halo Engagement Ring - 0.94 CTW (Kay Jewelers) ... Main Stone Creation: Natural ... Secondary Stone Diamond Clarity Grade: SI1 - SI2 ... Metal Weight: 3.8dwt / 5.90 Grams ... Total Carat Weight: 1.12ctw ... Secondary Stone Quantity: 85",
                source_url="https://www.ebay.com/itm/126886617045", observed_at=SNIP, page_date="2025-02-09 (index crawl date reported by search - ~20 months old)"),
  flags=NO_PRICE+["STALE INDEX: crawled 2025-02-09",
                   "Title says 0.94 CTW while item specifics say Total Carat Weight 1.12ctw - internal inconsistency in the listing",
                   "Weight published in BOTH pennyweight and grams, which allows a unit-conversion cross-check (3.8 dwt x 1.55517384 g/dwt = 5.9097 g, consistent with the stated 5.90 g)"],
  notes="Best weight-documentation example in the dataset: the seller gives 3.8 dwt AND 5.90 g, and the two agree under the NIST pennyweight conversion. This is what the checklist means by 'a legitimate seller should be able to provide the weight'.")

r(id="EBAY-297741882482", retailer="eBay (marketplace)",
  product="14k White Gold Engagement Ring 0.60ctw Diamond E/F Color Size 8.25",
  url="https://www.ebay.com/itm/297741882482", category="solitaire", karat="14K", metal="14K white gold",
  metal_claim="Seller states: 'Hallmark: Stamped \"14k\" inside the shank'; 'Total Gross Weight: 3.91 grams'",
  stone="Center diamond 0.38 ct natural round brilliant, Excellent cut, SI2 clarity, E/F colour; total 0.60 ctw",
  weight_grams=3.91, captured_at=SNIP,
  evidence=dict(tier="snippet", excerpt="Total Gross Weight: 3.91 grams. Hallmark: Stamped '14k' inside the shank. Center Diamond: 0.38 ct natural round brilliant - Excellent cut, Si2 clarity, E/F color.",
                source_url="https://www.ebay.com/itm/297741882482", observed_at=SNIP, page_date="2026-08-31 (index crawl date reported by search)"),
  flags=NO_PRICE+["Weight is described as GROSS weight (includes the diamonds), so pure-gold content computed from it is a slight over-estimate of metal-only weight",
                   "Seller reports a '14k' stamp but no maker's mark is mentioned - 15 U.S.C. 297 expects a trademark alongside the quality mark"],
  notes="Explicitly documents the hallmark location ('stamped 14k inside the shank'), which is exactly what the checklist asks a buyer to look for. No maker's mark is evidenced, so it only partially satisfies the hallmark item.")

r(id="EBAY-117329699772", retailer="eBay (marketplace)",
  product="14K White Gold Round Diamond Engagement Ring w/ Diamond Accents Milgrain sz 6.5 (Kay Jewelers)",
  url="https://www.ebay.com/itm/117329699772", category="vintage", karat="14K", metal="14K white gold",
  metal_claim="Seller states the ring 'weighs 5.4 gram' and that 'paperwork of original purchase included'",
  stone="Radiant-cut white diamond main stone with 34 diamond accents, totalling 0.80 carats, natural; semi-mount setting; band width 2.9mm at bottom; main stone 5.6mm x 4.8mm",
  weight_grams=5.4, width_mm="2.9 (at bottom of shank)", captured_at=SNIP,
  evidence=dict(tier="snippet", excerpt="This 14K White Gold Round Diamond Engagement Ring with Diamond Accents and Milgrain by Kay Jewelers ... a radiant cut white diamond as the main stone with 34 diamond accents, totaling .80 carats of natural diamond creation ... The band width of 2.9mm at bottom and main stone dimensions of 5.6mm x 4.8mm ... this beautiful piece weighs 5.4 gram, paperwork of original purchase included.",
                source_url="https://www.ebay.com/itm/117329699772", observed_at=SNIP, page_date=None),
  flags=NO_PRICE+["Title says 'Round Diamond' but the description says the main stone is 'radiant cut' - contradictory cut claim",
                   "Original purchase paperwork is claimed but not shown in the captured excerpt"],
  notes="Documentation positive: the seller offers the original purchase paperwork, which supports the checklist item on keeping documentation. The cut contradiction is still a reason to verify in person.")

r(id="EBAY-223469269883", retailer="eBay (marketplace)",
  product="14k White Solid Gold Wedding Band Ring by Zales, 12 Full Cut Diamonds 0.48 CTW",
  url="https://www.ebay.com/itm/223469269883", category="plain-band", karat="14K", metal="14K white gold",
  metal_claim="Seller states: 'Ring weights 1.9 grams stamp 14k Z size 7'; item specifics Metal Purity 14k, Brand Zales, Metal White Gold",
  stone="12 prong-set diamonds, 0.48 CTW, colour K-M, clarity SI2, cut Good, natural",
  weight_grams=1.9, captured_at=SNIP,
  evidence=dict(tier="snippet", excerpt="14k White Gold Wedding Band Ring by Zales 12 Diamonds 0.48 CTW. Ring weights 1.9 grams stamp 14k Z size 7 ans 12 prong set clean 0.48 CTW diamonds. ... Style: Wedding band ... Metal: White Gold ... Metal Purity: 14k ... Brand: Zales ... Sizable: Yes",
                source_url="https://www.ebay.com/itm/223469269883", observed_at=SNIP, page_date="2026-01-29 (index crawl date reported by search)"),
  flags=NO_PRICE+["Title says '14k White Solid Gold' but the captured description says 'stamp 14k Z' - the 'Z' is the Zales maker/quality mark, worth confirming in photos",
                   "'Sizable: Yes' - confirm in writing whether resizing voids the return right (checklist item)"],
  notes="A rare example of a listing that shows the karat stamp AND a maker mark ('Z' for Zales) plus a gram weight - three of the checklist's marking/weight items in one listing.")

r(id="JARED-V-993930609", retailer="Jared", product="Lab-Grown Diamond Engagement Ring 2 ct tw Round 14K White Gold",
  url="https://www.jared.com/labgrown-diamond-engagement-ring-2-ct-tw-round-14k-white-gold/p/V-993930609",
  category="halo-pave", karat="14K", metal="14K white gold",
  metal_claim="Official spec block: Metal Type: Gold; Metal Color: White; Metal Finish: Rhodium; Gold Karat: 14K; Rhodium Color: White",
  stone="Lab-grown round diamond, 2 ct tw total (centre 1-1/2 ct), F colour, SI2 clarity, independently certified",
  stock_number="Item #: 238222501", price_usd=None, captured_at=SNIP,
  evidence=dict(tier="snippet", excerpt="Fashioned in 14K white gold, the total lab-grown diamond weight of the ring is 2 carats. The lab-grown diamonds are independently certified. Item #: 238222501 ... Metal Type: Gold ... Metal Color: White ... Metal Finish: Rhodium ... Gold Karat: 14K ... Ring Style: Engagement Ring ... Standard Ring Size: 7.0 ... Height: 11 mm",
                source_url="https://www.jared.com/labgrown-diamond-engagement-ring-2-ct-tw-round-14k-white-gold/p/V-993930609", observed_at=SNIP, page_date=None),
  flags=["PRICE LEFT BLANK / UNVERIFIED: the captured evidence for this jared.com page contains the full specification block but NO price. It is NOT estimated.",
         "Gram weight NOT published by the retailer",
         "White gold is rhodium-finished per the retailer's own spec block - a plated surface finish over the gold alloy, which is normal but should be understood before purchase"])

# --- enrich existing rows with officially published spec blocks found in this pass ---
patch = {
 "ZAL-V-20050176": ("Official Zales spec block for this item: Total Weight (CT. T.W.) 1; Center Stone T.W. 1/2; Color I; Clarity I1; Stone Type Diamond; Stone Shape Round; Stone Class Natural; Metal Type Gold; Metal Color Yellow; Metal Finish Polished; Gold Karat 14K; Rhodium Yes.",
   ["KEY FINDING: Zales publishes karat, metal colour, finish and stone grades but does NOT publish the ring's weight in grams on the product page - the buyer must request it."]),
 "ZAL-V-20097139": ("Official Zales spec block: Total Weight (CT. T.W.) 1; Center Stone T.W. 1/2; Color I; Clarity I2; Stone Shape Round; Metal Type Gold; Metal Color White; Metal Finish Polished; Gold Karat: 14K; Rhodium: Yes; Ring Style: Solitaire with Side Accent. Page also states: 'This item is electroplated with rhodium or finished with an e-coating. These finishes may wear off with frequent use.'",
   ["Retailer discloses that the white-gold item is electroplated with rhodium or e-coated and that the finish may wear off - relevant to the 'plated' wording in the checklist (this is a surface finish on a solid gold alloy, NOT gold plating over base metal)."]),
 "KAY-V-992880601": ("Official Kay spec block: Total Weight (CT. T.W.) 1/2; Center Stone T.W. 1/5; Color I; Clarity I1; Stone Type Diamond; Stone Shape Oval; Stone Setting Prong; Metal Type Gold; Metal Color Rose; Metal Finish Rhodium; Gold Karat 14K; Rhodium Color White; Ring Style Engagement Ring; Standard Ring Size 7.0; Height 10.2 mm.",
   ["KEY FINDING: Kay publishes karat and metal colour but does NOT publish the ring's weight in grams - the buyer must request it."]),
}
out=[]
for line in open("data/rings.jsonl",encoding="utf-8"):
    x=json.loads(line)
    if x["id"] in patch:
        note,extra=patch[x["id"]]
        x["metal_claim"]=(x.get("metal_claim") or "")+" | "+note
        for e in extra:
            if e not in x["flags"]: x["flags"].append(e)
        x["evidence"]["excerpt"]+=" || SPEC BLOCK: "+note
        x["evidence"]["observed_at"]="2026-10-22T23:40:00Z"
    out.append(x)
with open("data/rings.jsonl","w",encoding="utf-8") as f:
    for x in out: f.write(json.dumps(x,ensure_ascii=False)+"\n")
    for x in rows: f.write(json.dumps(x,ensure_ascii=False)+"\n")
print("appended",len(rows),"patched",len(patch))
