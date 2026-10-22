import json
SNIP="2026-10-22T23:36:00Z"
rows=[]
def r(**kw):
    base=dict(id=None,retailer=None,seller=None,product=None,url=None,category=None,karat=None,metal=None,
              metal_claim=None,stone=None,price_usd=None,price_note=None,list_price_usd=None,currency="USD",
              weight_grams=None,width_mm=None,stock_number=None,captured_at=SNIP,return_policy=None,
              evidence=dict(tier="snippet",excerpt=None,source_url=None,observed_at=SNIP,page_date=None),
              flags=[],notes=None)
    base.update(kw); rows.append(base)

NOTGOLD=["NOT SOLID GOLD: the brand's own page states this item is gold-plated over a base alloy. Included as a documented red-flag example so it is never mistaken for a solid-gold engagement ring.",
         "Price from search-index snippet of the official us.pandora.net page; NOT re-confirmed by live fetch (fetch proxy outage at capture time)"]

r(id="PANDORA-162999C01", retailer="Pandora", product="Sparkling Band Ring",
  url="https://us.pandora.net/en/rings/band-rings/sparkling-band-ring/162999C01.html",
  category="not-solid-gold", karat="n/a - plating only", metal="14k Gold-plated Signature metal alloy",
  metal_claim="Brand's own structured data: material = '14k Gold-plated Signature metal alloy, No Other Material'",
  stone="Cubic zirconia (clear)", price_usd=75.00,
  evidence=dict(tier="snippet", excerpt='{"name":"Sparkling Band Ring","brand":{"name":"Pandora"},"offers":{"priceCurrency":"USD","price":75,"availability":"https://schema.org/InStock"},"color":"Clear","material":"14k Gold-plated Signature metal alloy, No Other Material"}',
                source_url="https://us.pandora.net/en/rings/band-rings/sparkling-band-ring/162999C01.html", observed_at=SNIP, page_date=None),
  flags=NOTGOLD,
  notes="Strongest possible disproof example: the seller's OWN machine-readable product data says the material is a gold-plated alloy with 'No Other Material'. Under FTC guidance this item must not be described as solid gold.")

r(id="PANDORA-168421C01", retailer="Pandora", product="Elevated Heart Ring",
  url="https://us.pandora.net/en/rings/elevated-heart-ring/168421C01.html",
  category="not-solid-gold", karat="n/a - plating only", metal="14k Gold-plated Signature metal alloy",
  metal_claim="Brand's own structured data: material = '14k Gold-plated Signature metal alloy, No Other Material'",
  stone="Clear (cubic zirconia)", price_usd=130.00,
  evidence=dict(tier="snippet", excerpt='## 14k gold plating $130.00 Elevated Heart Ring ... {"name":"Elevated Heart Ring","brand":{"name":"Pandora"},"offers":{"priceCurrency":"USD","price":130,"availability":"https://schema.org/InStock"},"material":"14k Gold-plated Signature metal alloy, No Other Material"}',
                source_url="https://us.pandora.net/en/rings/elevated-heart-ring/168421C01.html", observed_at=SNIP, page_date="2025-02-24 (index crawl date reported by search - ~20 months old)"),
  flags=NOTGOLD+["STALE INDEX: crawled 2025-02-24",
                 "PRICE CONFLICT: Pandora's own '14k Gold-Plated Jewelry For Women' page (/en/jewelry/gold-plated/) lists the same 'Elevated Heart Ring' at $125.00 while the product page shows $130.00 - see Flagged for Review (F-06)"],
  notes="Same product, two different prices on two official Pandora pages in the search index. A concrete demonstration that a price must be re-read on the live product page at checkout.")

r(id="PANDORA-163799C01", retailer="Pandora", product="Double Band Ring",
  url="https://us.pandora.net/en/rings/promise-rings/double-band-ring/163799C01.html",
  category="not-solid-gold", karat="n/a - plating only", metal="14k gold-plated",
  metal_claim="Page header states '14k gold plating'; copy: 'A 14k gold-plated double band...'",
  stone="Cubic zirconia", price_usd=130.00,
  evidence=dict(tier="snippet", excerpt="## 14k gold plating $130.00 Double Band Ring ... A 14k gold-plated double band features one polished band parallel to a second band set with sparkling pave. ... Cubic zirconia",
                source_url="https://us.pandora.net/en/rings/promise-rings/double-band-ring/163799C01.html", observed_at=SNIP, page_date=None),
  flags=NOTGOLD+["Sold under Pandora's 'promise rings' category - a plated ring marketed in a bridal-adjacent category"])

r(id="PANDORA-169591C00", retailer="Pandora", product="Pandora ME Ring",
  url="https://us.pandora.net/en/rings/rings/band-rings/pandora-me-ring/169591C00.html",
  category="not-solid-gold", karat="n/a - plating only", metal="14k gold-plated",
  metal_claim="Page states '14k gold plating'; copy: 'This 14k gold-plated ring features grooved lines...'",
  stone="None", price_usd=50.00,
  evidence=dict(tier="snippet", excerpt="## 14k gold plating $50.00 ... This 14k gold-plated ring features grooved lines that add instant dimension",
                source_url="https://us.pandora.net/en/rings/rings/band-rings/pandora-me-ring/169591C00.html", observed_at=SNIP, page_date=None),
  flags=NOTGOLD)

r(id="PANDORA-163986C00", retailer="Pandora", product="Engravable Bar Ring",
  url="https://us.pandora.net/en/rings/stackable-rings/engravable-bar-ring/163986C00.html",
  category="not-solid-gold", karat="n/a - plating only", metal="14k gold-plated",
  metal_claim="Copy: 'Crafted in 14k gold plating, this ring features a blank bar canvas ready to customize with an engraving.'",
  stone="None", price_usd=80.00,
  evidence=dict(tier="snippet", excerpt="## 14k gold plating $80.00 Engravable Bar Ring ... Crafted in 14k gold plating, this ring features a blank bar canvas ready to customize with an engraving. ... 14k gold plating",
                source_url="https://us.pandora.net/en/rings/stackable-rings/engravable-bar-ring/163986C00.html", observed_at=SNIP, page_date="2026-07-28 (index crawl date reported by search)"),
  flags=NOTGOLD+["Engraved/personalised items are commonly excluded from returns - check the seller's written policy (checklist item)"])

r(id="PANDORA-189591C00", retailer="Pandora", product="FINAL SALE - Pandora ME Ring",
  url="https://us.pandora.net/en/rings/stackable-rings/final-sale---pandora-me-ring/189591C00.html",
  category="not-solid-gold", karat="n/a - plating only", metal="14k rose gold-plated",
  metal_claim="Page states '14k rose gold plating'", stone="None",
  price_usd=25.00, list_price_usd=50.00, price_note="'$25.00 / $50.00 Save 50%' and titled FINAL SALE",
  evidence=dict(tier="snippet", excerpt="## 14k rose gold plating $25.00 $50.00 Save 50% ... FINAL SALE - Pandora ME Ring",
                source_url="https://us.pandora.net/en/rings/stackable-rings/final-sale---pandora-me-ring/189591C00.html", observed_at=SNIP, page_date=None),
  flags=NOTGOLD+["RETURN RISK: item is explicitly marked 'FINAL SALE', which normally means no return. The checklist requires a return right after inspection - this listing fails it."])

r(id="PANDORA-CAT-GP-ENGAGEMENT", retailer="Pandora", product="Category page: GOLD PLATED ENGAGEMENT RINGS (3 products at $125.00, $125.00, $135.00)",
  url="https://us.pandora.net/en/rings/engagement-rings/gold-plated/",
  category="not-solid-gold", karat="n/a - plating only", metal="Gold plated (category filter: 'gold-plated')",
  metal_claim="Pandora's own category is named 'GOLD PLATED ENGAGEMENT RINGS'",
  stone="Not stated in captured excerpt", price_usd=125.00,
  price_note="Category page shows three prices ($125.00, $125.00, $135.00); $125.00 recorded as the lowest observed on the page",
  evidence=dict(tier="snippet", excerpt="# GOLD PLATED ENGAGEMENT RINGS $125.00 $125.00 $135.00",
                source_url="https://us.pandora.net/en/rings/engagement-rings/gold-plated/", observed_at=SNIP, page_date=None),
  flags=NOTGOLD+["CATEGORY-LEVEL EVIDENCE: the URL is a category page, not one product page. Individual product names/URLs were NOT captured, so the three prices cannot be attributed to specific items. Treat as UNVERIFIED at item level.",
                 "KEY FINDING: a major brand sells 'engagement rings' that are gold plated, not solid gold. Searching the word 'engagement ring' alone will surface these."],
  notes="This row exists to prove the checklist point that the words 'engagement ring' do not imply solid gold. The item-level prices are deliberately NOT asserted.")

# ---------------- AMAZON ----------------
r(id="AMAZON-B081166CZD", retailer="Amazon (marketplace)", product="14K Solid Gold 1 Ct. Round Cut Cubic Zirconia CZ Wedding Engagement Ring (Yellow Gold)",
  url="https://www.amazon.com/Gold-Zirconia-Wedding-Engagement-Yellow/dp/B081166CZD",
  category="marketplace", karat="14K", metal="Yellow gold, 14K stamped",
  metal_claim="Seller's own specification block: 'Metal: Yellow Gold / Standard: 14K Stamped Gold / Real Gold: No gold plated or filled'",
  stone="Cubic zirconia (NOT a diamond); stone weight 1 carat; total diamond weight field says '1 cttw'",
  price_usd=None, price_note=None, weight_grams=2.7, width_mm="2.5", captured_at=SNIP,
  evidence=dict(tier="snippet", excerpt="14K Solid Gold 1 Ct. Round Cut Cubic Zirconia CZ Wedding Engagement Ring (Yellow Gold) ... Metal type: Yellow Gold ... Gem type: Cubic Zirconia ... Metal: Yellow Gold / Standard: 14K Stamped Gold / Real Gold: No gold plated or filled / Width: 2.5MM / Average Weight: 2.7gr.",
                source_url="https://www.amazon.com/Gold-Zirconia-Wedding-Engagement-Yellow/dp/B081166CZD", observed_at=SNIP, page_date=None),
  flags=["PRICE LEFT BLANK / UNVERIFIED: no price appeared in the captured evidence for this ASIN. It is NOT estimated.",
         "MARKETPLACE: sold by a third-party seller on Amazon; seller identity and return policy must be verified on the live page",
         "Inconsistent product data: 'Gem type: Cubic Zirconia' but the specification block also reports 'Total Diamond Weight: 1 cttw' - a CZ stone described with a diamond-weight field",
         "Weight is described as 'Average Weight', i.e. not the actual weight of the shipped ring",
         "'Ring Size: Adjustable' is unusual for a solid gold ring and should be questioned"],
  notes="Gram weight IS published (2.7 g average), so the calculator can be demonstrated on this row, but no price is asserted anywhere in this dataset for it.")

r(id="AMAZON-B07QJSZ8QX", retailer="Amazon (marketplace)", seller="Manufacturer listed as Clara Pucci",
  product="14K Solid Gold Engagement Ring for Women | 0.755 cttw Moissanite",
  url="https://www.amazon.com/dp/B07QJSZ8QX",
  category="marketplace", karat="14K", metal="Rose gold (metal type stated as Rose Gold)",
  metal_claim="Seller copy: '14K SOLID ROSE GOLD CONSTRUCTION - Not plated or filled. Real 14K gold engagement ring...' and 'Professional hallmarking certified'",
  stone="Moissanite, 0.755 cttw, 35 stones, round cut (NOT a diamond)",
  price_usd=None, weight_grams=1.72, captured_at=SNIP,
  return_policy="Seller copy claims '30-day returns guaranteed' and a 'certificate of authenticity' - verify on the live Amazon page",
  evidence=dict(tier="snippet", excerpt="14K Solid Gold Engagement Ring for Women | 0.755 cttw Moissanite ... Metal type: Rose Gold ... Metal weight: 1.72 grams ... Total Diamond Weight: 0.76 carat ... Number Of Stones: 35 ... Manufacturer: Clara Pucci ... 14K SOLID ROSE GOLD CONSTRUCTION - Not plated or filled ... Professional hallmarking certified ... 30-day returns guaranteed ... certificate of authenticity",
                source_url="https://www.amazon.com/-/he/%D7%A1%D7%95%D7%9C%D7%99%D7%98%D7%A8-%D7%9E%D7%95%D7%90%D7%A1%D7%A0%D7%99%D7%98-%D7%90%D7%99%D7%93%D7%99%D7%90%D7%9C%D7%99-%D7%90%D7%99%D7%A8%D7%95%D7%A1%D7%99%D7%9F-%D7%A0%D7%99%D7%A9%D7%95%D7%90%D7%99%D7%9F/dp/B07QJSZ8QX", observed_at=SNIP, page_date=None),
  flags=["PRICE LEFT BLANK / UNVERIFIED: no price appeared in the captured evidence. It is NOT estimated.",
         "LOCALE VARIANT: the indexed page is a Hebrew-locale rendering of the same ASIN. Item specifics (including the 1.72 g metal weight) were read from that page; the canonical US URL is recorded here and must be re-checked.",
         "Title says '14K Solid Gold' while the metal type field says 'Rose Gold' and the copy says '14K SOLID ROSE GOLD' - the generic title omits the colour, a common source of buyer confusion",
         "Center stone is MOISSANITE, not diamond, despite a 'Total Diamond Weight' field being populated (0.76 carat)",
         "MARKETPLACE: verify the seller, not just the brand name"],
  notes="Weight IS published (1.72 g metal weight) so gold content can be computed; price is deliberately left blank because no price was observed in official evidence.")

with open("data/rings.jsonl","a",encoding="utf-8") as f:
    for x in rows: f.write(json.dumps(x,ensure_ascii=False)+"\n")
print("appended",len(rows))
