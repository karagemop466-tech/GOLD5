import json, io
LIVE = "2026-10-22T23:16:00Z"
LIVE2 = "2026-10-22T23:20:00Z"
SNIP = "2026-10-22T23:27:00Z"

rows = []
def r(**kw):
    base = dict(id=None, retailer=None, seller=None, product=None, url=None, category=None,
                karat=None, metal=None, metal_claim=None, stone=None, price_usd=None,
                price_note=None, list_price_usd=None, currency="USD", weight_grams=None,
                width_mm=None, stock_number=None, captured_at=None, return_policy=None,
                evidence=dict(tier=None, excerpt=None, source_url=None, observed_at=None,
                              page_date=None), flags=[], notes=None)
    base.update(kw); rows.append(base)

# ---------------- LIVE-FETCH VERIFIED ----------------
r(id="BN-502120w14", retailer="Blue Nile", product="Classic Simple Solitaire Engagement Ring in 14k White Gold",
  url="https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-white-gold-item-195730",
  category="solitaire", karat="14K", metal="14K White Gold", metal_claim="14K White Gold (stated on page)",
  stone="Setting only - center diamond not included", price_usd=1145.00, price_note="Setting Price",
  width_mm="2.40", stock_number="502120w14", captured_at=LIVE,
  return_policy="Free returns (stated on product page); Limited Lifetime Warranty on gold items priced $1,000+",
  evidence=dict(tier="live", excerpt="$1,145(Setting Price) ... Metal Type:14K White Gold ... Stock Number 502120w14 ... Width 2.40mm ... Rhodium Finish Yes",
                source_url="https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-white-gold-item-195730",
                observed_at=LIVE, page_date=None),
  flags=["Setting-only price: center diamond NOT included", "Metal weight in grams NOT published on page"],
  notes="Page also states Free Overnight Shipping, Free Returns, and a Limited Lifetime Warranty for gold jewelry with a purchase price of $1,000 or more.")

r(id="KAY-V-993154400", retailer="Kay Jewelers", product="Round-Cut Diamond Engagement Ring 5/8 ct tw 14K White Gold",
  url="https://www.kay.com/diamond-engagement-ring-58-ct-tw-14k-white-gold/p/V-993154400",
  category="halo-pave", karat="14K", metal="14K White Gold", metal_claim="14K White Gold (stated on page)",
  stone="Diamond, 5/8 ct tw (natural)", price_usd=629.99, list_price_usd=2099.99,
  price_note="Discounted Price; page shows 70% Off", captured_at=LIVE,
  return_policy="Free and easy 30-day returns (stated on product page)",
  evidence=dict(tier="live", excerpt="Discounted Price $629.99  Original Price was $2,099.99 70% Off ... 5/8 ct tw ... 14K White Gold ... Free and easy 30-day returns",
                source_url="https://www.kay.com/diamond-engagement-ring-58-ct-tw-14k-white-gold/p/V-993154400",
                observed_at=LIVE, page_date=None),
  flags=["70% off list price - verify the discount is not a permanent 'was' price", "Metal weight in grams NOT published on page"],
  notes="Complete ring (diamonds included), not a setting-only price.")

r(id="ETSY-4470385318", retailer="Etsy (marketplace)", seller="SolithDiamond",
  product="14K Gold Round Diamond Solitaire Engagement Ring, 0.50 Ct Classic Bridal Promise Ring",
  url="https://www.etsy.com/listing/4470385318/14k-gold-round-diamond-solitaire",
  category="solitaire", karat="14K", metal="14K solid white / yellow / rose gold (buyer selects)",
  metal_claim="Variants named '14K Solid White Gold', '14K Solid YellowGold', '14K Solid Rose Gold'",
  stone="Natural diamond 0.50 ct (per listing title)", price_usd=2250.00,
  price_note="From $2,250.00 (size 3 US) to $2,660.00 (size 13 US) - price varies by ring size",
  captured_at=LIVE2, return_policy="Returns & exchanges accepted (stated on listing page)",
  evidence=dict(tier="live", excerpt="Price:$2,250.00+ ... Low in stock, only 5 left ... Returns & exchanges accepted ... 3 US ($2,250.00) ... 13 US ($2,660.00) ... 14K Solid White Gold / 14K Solid YellowGold / 14K Solid Rose Gold",
                source_url="https://www.etsy.com/listing/4470385318/14k-gold-round-diamond-solitaire",
                observed_at=LIVE2, page_date=None),
  weight_grams=None,
  flags=["MARKETPLACE: third-party seller, not the platform - verify seller independently",
         "Price varies by ring size; $2,250.00 is the lowest variant",
         "Gold weight (2.44 g) appears in an index snippet of this listing but was NOT confirmed by live fetch - left blank in the verified column"],
  notes="Search index snippet for this same listing URL reports 'Gold Weight: 2.44 grams' and 'Metal Purity: 14K'. Treated as UNVERIFIED until confirmed on the live page.")

# ---------------- SNIPPET TIER: ZALES ----------------
zales = [
 ("ZAL-V-20050176","1 CT. T.W. Diamond Engagement Ring in 14K Gold","https://www.zales.com/1-ct-tw-diamond-engagement-ring-14k-gold/p/V-20050176","14K","14K Yellow Gold","Diamond 1 ct tw",3429.30,4899.00,"30% Off","solitaire",
  "Discounted Price $3,429.30 Orig Original Price $4,899.00 ... 30% Off ... Select Your Metal: Yellow Gold"),
 ("ZAL-V-20365272","2 CT. T.W. Diamond Engagement Ring in 14K Gold (I/I2)","https://www.zales.com/2-ct-tw-diamond-engagement-ring-14k-gold-ii2/p/V-20365272","14K","14K Yellow Gold","Diamond 2 ct tw (I/I2)",3750.00,7499.99,"50% Off","halo-pave",
  "Discounted Price $3,750.00 Original Price $7,499.99 ... Metal: 14K Yellow Gold"),
 ("ZAL-V-20308017","1/3 CT. T.W. Diamond Engagement Ring in 10K White Gold","https://www.zales.com/13-ct-tw-diamond-engagement-ring-10k-white-gold/p/V-20308017","10K","10K White Gold","Diamond 1/3 ct tw",909.30,1299.00,"30% Off","halo-pave",
  "Discounted Price $909.30 Original Price $1,299.00 ... 30% Off ... Metal: White Gold"),
 ("ZAL-V-19957449","1/5 CT. Diamond Solitaire Engagement Ring in 10K Gold","https://www.zales.com/15-ct-diamond-solitaire-engagement-ring-10k-gold/p/V-19957449","10K","10K Yellow Gold","Diamond 1/5 ct, round",719.20,899.00,"20% Off","solitaire",
  "Discounted Price $719.20 Original Price $899.00 ... 20% Off ... Metal: 10K Yellow Gold"),
 ("ZAL-V-20097139","1 CT. T.W. Diamond Engagement Ring in 14K White Gold","https://www.zales.com/1-ct-tw-diamond-engagement-ring-14k-white-gold/p/V-20097139","14K","14K White Gold","Diamond 1 ct tw",1251.60,3129.00,"60% Off","halo-pave",
  "Discounted Price $1,251.60 Original Price $3,129.00 ... 60% Off"),
 ("ZAL-V-20062136","3/4 CT. T.W. Diamond Engagement Ring in 14K Gold","https://www.zales.com/34-ct-tw-diamond-engagement-ring-14k-gold/p/V-20062136","14K","14K Yellow Gold","Diamond 3/4 ct tw",3079.30,4399.00,"30% Off","solitaire",
  "Discounted Price $3,079.30 Original Price $4,399.00 ... 30% Off ... Metal: Yellow Gold"),
 ("ZAL-V-15246515","1 CT. Certified Diamond Solitaire Engagement Ring in 14K Gold (I/I2)","https://www.zales.com/1-ct-certified-diamond-solitaire-engagement-ring-14k-gold-ii2/p/V-15246515","14K","14K Yellow Gold","Certified diamond 1 ct (I/I2)",3999.99,None,None,"solitaire",
  "$3,999.99 ... 14K Yellow Gold"),
 ("ZAL-V-20312322","2-1/2 CT. T.W. Diamond Engagement Ring in 14K White Gold","https://www.zales.com/212-ct-tw-diamond-engagement-ring-14k-white-gold/p/V-20312322","14K","14K White Gold","Diamond 2-1/2 ct tw",7499.99,12499.99,"40% Off","halo-pave",
  "Discounted Price $7,499.99 Original Price $12,499.99 ... 40% Off ... Metal: 14K White Gold"),
 ("ZAL-V-20308275","1/3 CT. T.W. Diamond Engagement Ring in 10K Rose Gold","https://www.zales.com/13-ct-tw-diamond-engagement-ring-10k-rose-gold/p/V-20308275","10K","10K Rose Gold","Diamond 1/3 ct tw",909.35,1399.00,"35% Off","halo-pave",
  "Discounted Price $909.35 Original Price $1,399.00 ... 35% Off ... Metal: Rose Gold"),
]
for i,(pid,name,url,k,metal,stone,price,lst,off,cat,exc) in enumerate(zales):
    fl = ["Price from search-index snippet of the official zales.com page; NOT re-confirmed by live fetch (fetch proxy outage at capture time)",
          "Metal weight in grams NOT published"]
    nt = None
    if pid == "ZAL-V-15246515":
        fl.append("PRICE CONFLICT: a second index snapshot of this same product URL shows $3,114.30 with title grade (J/I2), while this snapshot shows $3,999.99 with grade (I/I2). Confirm on the live page before purchase.")
        nt = "Two different indexed prices/grades for one product URL - see Flagged for Review (F-05)."
    r(id=pid, retailer="Zales", product=name, url=url, category=cat, karat=k, metal=metal,
      metal_claim=metal+" (stated in listing)", stone=stone, price_usd=price, list_price_usd=lst,
      price_note=(off+" shown on page") if off else None, captured_at=SNIP,
      evidence=dict(tier="snippet", excerpt=exc, source_url=url, observed_at=SNIP, page_date=None),
      flags=fl, notes=nt)

# ---------------- SNIPPET TIER: KAY ----------------
kay = [
 ("KAY-V-151158805","Solitaire Engagement Ring 1 Carat Diamond 14K Rose Gold (I/I2)","https://www.kay.com/solitaire-engagement-ring-1-carat-diamond-14k-rose-gold-ii2/p/V-151158805","14K","14K Rose Gold","Diamond 1 ct tw (I/I2)",1199.99,3999.99,"70% Off","solitaire",
  "Discounted Price $1,199.99 Original Price was $3,999.99 70% Off ... Metal Rose Gold"),
 ("KAY-V-622398903","Princess-Cut Diamond Engagement Ring 1 ct tw 14K Yellow Gold","https://www.kay.com/princesscut-diamond-engagement-ring-1-ct-tw-14k-yellow-gold/p/V-622398903","14K","14K Yellow Gold","Princess-cut diamond 1 ct tw",1959.99,2799.99,"30% Off","solitaire",
  "Discounted Price $1,959.99 Original Price $2,799.99 ... 30% Off"),
 ("KAY-V-992880601","Now + Forever Oval Diamond Engagement Ring 1/2 ct tw 14K Rose Gold","https://www.kay.com/now-forever-oval-diamond-engagement-ring-12-ct-tw-14k-rose-gold/p/V-992880601","14K","14K Rose Gold","Oval diamond 1/2 ct tw",1649.99,2199.99,"25% Off","solitaire",
  "Discounted Price $1,649.99 Original Price was $2,199.99 25% Off ... Metal Rose Gold ... Shape Oval ... Carat Weight 1/2"),
 ("KAY-V-992322901","Diamond Engagement Ring 1/2 ct tw Oval 14K White Gold","https://www.kay.com/diamond-engagement-ring-12-ct-tw-oval-14k-white-gold/p/V-992322901","14K","14K White Gold","Oval diamond 1/2 ct tw",479.99,1599.99,"70% Off","solitaire",
  "Discounted Price $479.99 Original Price was $1,599.99 70% Off"),
 ("KAY-V-394026506","Now + Forever Lab-Grown Diamonds Round-Cut Solitaire Engagement Ring 1 ct tw 14K White Gold (F/SI2)","https://www.kay.com/labgrown-diamonds-by-kay-solitaire-engagement-ring-1-ct-tw-14k-white-gold-fsi2/p/V-394026506","14K","14K White Gold","Lab-grown diamond 1 ct tw (F/SI2), independently certified",1799.99,None,None,"solitaire",
  "Discounted Price $1,799.99 ... Crafted in 14K White Gold ... Certified Lab-Grown Diamond: Yes"),
 ("KAY-V-161449006","Diamond Engagement Ring 5/8 ct tw Oval & Round-cut 14K White Gold (I/I2)","https://www.kay.com/diamond-engagement-ring-58-ct-tw-oval-roundcut-14k-white-gold-ii2/p/V-161449006","14K","14K White Gold","Oval + round diamonds 5/8 ct tw (I/I2)",879.99,2199.99,"60% Off","halo-pave",
  "Discounted Price $879.99 Original Price was $2,199.99 60% Off"),
 ("KAY-V-861518900","KAY Signature Collection Oval-Cut Lab-Grown Diamond Engagement Ring 2-1/2 ct tw 14K White Gold","https://www.kay.com/kay-signature-collection-ovalcut-labgrown-diamond-engagement-ring-212-ct-tw-14k-white-gold/p/V-861518900","14K","14K White Gold","Lab-grown diamond 2-1/2 ct tw, independently certified",3999.99,None,None,"halo-pave",
  "$3,999.99 - 14K white gold ... Total lab-grown diamond weight is 2 1/2 carats ... Independently certified"),
]
for pid,name,url,k,metal,stone,price,lst,off,cat,exc in kay:
    r(id=pid, retailer="Kay Jewelers", product=name, url=url, category=cat, karat=k, metal=metal,
      metal_claim=metal+" (stated in listing)", stone=stone, price_usd=price, list_price_usd=lst,
      price_note=(off+" shown on page") if off else None, captured_at=SNIP,
      evidence=dict(tier="snippet", excerpt=exc, source_url=url, observed_at=SNIP, page_date=None),
      flags=["Price from search-index snippet of the official kay.com page; NOT re-confirmed by live fetch (fetch proxy outage at capture time)",
             "Metal weight in grams NOT published"])

# ---------------- SNIPPET TIER: BLUE NILE ----------------
bn = [
 ("BN-item-194360","Classic Four-Prong Solitaire Engagement Ring in 14k White Gold","https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-white-gold-item-194360","14K","14K White Gold",650.00,"solitaire",
  "$650(Setting Price) ... Metal Type:  14K White Gold"),
 ("BN-item-20315","Petite Solitaire Engagement Ring in 14k White Gold","https://www.bluenile.com/engagement-rings/design-your-own-ring/14k-white-gold-engagement-ring_20315","14K","14K White Gold",1000.00,"solitaire",
  "$1,000(Setting Price) ... Metal Type:14K White Gold"),
 ("BN-item-195326","Riviera Pave Diamond Engagement Ring in 14k White Gold (1/6 ct. tw.)","https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326","14K","14K White Gold",1500.00,"halo-pave",
  "$1,500(Setting Price) ... Metal Type:14K White Gold ... Diamond Type:Natural Diamond"),
 ("BN-item-147412","Men's Ridged Solitaire Engagement Ring in 14k White Gold","https://www.bluenile.com/engagement-rings/design-your-own-ring/mens-ridged-solitaire-engagement-ring-in-14k-white-gold-item-147412","14K","14K White Gold",1530.00,"mens",
  "$1,530(Setting Price) ... Metal Type:14K White Gold"),
 ("BN-item-203274","Classic Pear Shaped Sapphire Engagement Ring in 14k White Gold","https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-pear-shaped-sapphire-engagement-ring-in-14k-white-gold-item-203274","14K","14K White Gold",1090.00,"gemstone",
  "$1,090(Setting Price) ... Metal Type:  14K White Gold"),
 ("BN-item-20373","Tapered Cathedral Solitaire Engagement Ring in 14k White Gold","https://www.bluenile.com/build-your-own-ring/diamond-14k-white-gold-engagement-ring-setting_20373","14K","14K White Gold",1240.00,"solitaire",
  "$1,240(Setting Price) ... Metal Type:14K White Gold"),
 ("BN-item-194548","Solitaire Compass Set Engagement Ring in 14k White Gold","https://www.bluenile.com/engagement-rings/design-your-own-ring/east-west-solitaire-engagement-ring-in-14k-white-gold-item-194548","14K","14K White Gold",784.00,"solitaire",
  "$1,045$784(Setting Price) ... -25%"),
 ("BN-item-193624","Petite Three-Stone Diamond Engagement Ring in 14k White Gold","https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-three-stone-diamond-engagement-ring-in-14k-white-gold-item-193624","14K","14K White Gold",1950.00,"three-stone",
  "$1,950(Setting Price) ... Metal Type:14K White Gold ... Diamond Type:Natural Diamond"),
 ("BN-item-304465","Diamond Filigree Vintage-Style Engagement Ring In 14K White Gold By James Allen","https://www.bluenile.com/engagement-rings/design-your-own-ring/diamond-filigree-vintage-style-engagement-ring-in-14k-white-gold-by-james-allen-item-304465","14K","14K White Gold",1825.00,"vintage",
  "$1,825(Setting Price) ... Metal Type:14K White Gold"),
 ("BN-item-146887","Men's Brushed Finish Diamond Channel Engagement Ring in 14k White Gold (1/4 ct. tw.)","https://www.bluenile.com/engagement-rings/design-your-own-ring/mens-brushed-finish-diamond-channel-engagement-ring-in-14k-white-gold-1-4-ct-tw-item-146887","14K","14K White Gold",3815.00,"mens",
  "$3,815(Setting Price) ... Metal Type:  14K White Gold"),
]
for pid,name,url,k,metal,price,cat,exc in bn:
    lst = 1045.00 if pid=="BN-item-194548" else None
    r(id=pid, retailer="Blue Nile", product=name, url=url, category=cat, karat=k, metal=metal,
      metal_claim=metal+" (stated in listing)", stone="Setting only unless stated - center stone not included",
      price_usd=price, list_price_usd=lst, price_note="Setting Price", captured_at=SNIP,
      evidence=dict(tier="snippet", excerpt=exc, source_url=url, observed_at=SNIP, page_date=None),
      flags=["Setting-only price: center stone NOT included",
             "Price from search-index snippet of the official bluenile.com page; NOT re-confirmed by live fetch (fetch proxy outage at capture time)",
             "Metal weight in grams NOT published"])

# ---------------- SNIPPET TIER: BRILLIANT EARTH (JSON-LD on official listing page) ----------------
be = [
 ("BE1D2016-14KW","Olympia Three-Quarter Coverage Diamond Ring","https://www.brilliantearth.com/engagement-rings/shop-all/",2450.00,"halo-pave",
  '{"name":"Olympia Three-Quarter Coverage Diamond Ring",...,"sku":"BE1D2016-14KW","brand":"Brilliant Earth","offers":{"priceCurrency":"USD","price":"2450","itemCondition":"https://schema.org/NewCondition","availability":"https://schema.org/InStock"}}'),
 ("BE1D305-14KW","Demi Three-Quarter Coverage Diamond Ring (1/3 ct. tw.)","https://www.brilliantearth.com/engagement-rings/shop-all/",1090.00,"halo-pave",
  '{"name":"Demi Three-Quarter Coverage Diamond Ring (1/3 ct. tw.)",...,"sku":"BE1D305-14KW","offers":{"priceCurrency":"USD","price":"1090"}}'),
 ("BE1D54-14KW","Petite Twisted Vine Diamond Ring (1/8 ct. tw.)","https://www.brilliantearth.com/engagement-rings/shop-all/",950.00,"vintage",
  '{"name":"Petite Twisted Vine Diamond Ring (1/8 ct. tw.)",...,"sku":"BE1D54-14KW","offers":{"priceCurrency":"USD","price":"950"}}'),
 ("BE1D378-14KW","Versailles Half Coverage Diamond Ring (1/3 ct. tw.)","https://www.brilliantearth.com/engagement-rings/shop-all/",1390.00,"halo-pave",
  '{"name":"Versailles Half Coverage Diamond Ring (1/3 ct. tw.)",...,"sku":"BE1D378-14KW","offers":{"priceCurrency":"USD","price":"1390"}}'),
]
for sku,name,url,price,cat,exc in be:
    r(id="BE-"+sku, retailer="Brilliant Earth", product=name+" (14K White Gold variant)", url=url,
      category=cat, karat="14K", metal="14K White Gold (per SKU suffix -14KW)",
      metal_claim="SKU suffix '-14KW' indicates 14K White Gold; page lists 14K/18K white, yellow and rose gold options",
      stone="Setting - accent diamonds included, center stone chosen separately", price_usd=price,
      price_note="Structured product data (schema.org offers.price) embedded in the official listing page",
      captured_at="2026-10-22T23:22:00Z",
      evidence=dict(tier="snippet", excerpt=exc, source_url=url, observed_at="2026-10-22T23:22:00Z",
                    page_date="2026-10-19 (search index reports this listing page was crawled 2026-10-19)"),
      flags=["URL is the category listing page, NOT a dedicated product page - a per-product URL must be confirmed",
             "Price taken from schema.org JSON-LD embedded in the official page via the search index (crawled 2026-10-19); not re-confirmed by live fetch",
             "Metal weight in grams NOT published"])

with open("data/rings.jsonl","w",encoding="utf-8") as f:
    for x in rows:
        f.write(json.dumps(x, ensure_ascii=False)+"\n")
print("rows:", len(rows))
print("live:", sum(1 for x in rows if x["evidence"]["tier"]=="live"))
print("snippet:", sum(1 for x in rows if x["evidence"]["tier"]=="snippet"))
