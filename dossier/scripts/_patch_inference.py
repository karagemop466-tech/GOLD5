import json
rows=[json.loads(l) for l in open("data/rings.jsonl",encoding="utf-8")]
TITLES={
 "KAY-V-151158805":"PAGE TITLE: Solitaire Engagement Ring 1 Carat Diamond 14K Rose Gold (I/I2) || PAGE H1: Solitaire Engagement Ring Round-Cut Diamond / 1 ct tw / (I/I2) / 14K Rose Gold",
 "KAY-V-622398903":"PAGE TITLE: Princess-Cut Diamond Engagement Ring 1 ct tw 14K Yellow Gold",
 "KAY-V-992322901":"PAGE TITLE: Diamond Engagement Ring 1/2 ct tw Oval 14K White Gold || PAGE H1: Oval-Cut Diamond Engagement Ring / 1/2 ct tw / 14K White Gold",
 "KAY-V-161449006":"PAGE TITLE: Diamond Engagement Ring 5/8 ct tw Oval & Round-cut 14K White Gold (I/I2) || PAGE H1: Oval-Cut Diamond Engagement Ring / 5/8 ct tw / (I/I2) / 14K White Gold",
 "ZAL-V-20308017":"PAGE TITLE / H1: 1/3 CT. T.W. Diamond Engagement Ring in 10K White Gold",
 "ZAL-V-20062136":"PAGE TITLE / H1: 3/4 CT. T.W. Diamond Engagement Ring in 14K Gold",
 "ZAL-V-20308275":"PAGE TITLE / H1: 1/3 CT. T.W. Diamond Engagement Ring in 10K Rose Gold",
 "BN-item-194548":"PAGE TITLE: Solitaire Compass Set Engagement Ring in 14k White Gold",
 "BN-item-195326":"PAGE TITLE: Riviera Pave Diamond Engagement Ring in 14k White Gold (1/6 ct. tw.)",
}
n=0
for r in rows:
    if r["id"] in TITLES and "PAGE TITLE" not in r["evidence"]["excerpt"]:
        r["evidence"]["excerpt"]+=" || "+TITLES[r["id"]]
        r["flags"].append("Karat and metal colour are asserted from the official page TITLE / H1 text, which is reproduced verbatim in the evidence excerpt (added by check C14 remediation).")
        n+=1
    # Brilliant Earth: karat/metal were inferred from the SKU suffix -> withdraw the assertion
    if r["id"].startswith("BE-"):
        r["karat"]=None; r["metal"]=None
        r["metal_claim"]=("NOT ASSERTED. The captured evidence (schema.org JSON-LD on Brilliant Earth's engagement-ring "
                          "listing page) states the product name, SKU, brand, currency and price only. The SKU suffix "
                          "'-14KW' follows a 14K white-gold convention, but the captured text does NOT state the karat or "
                          "the metal colour, so both fields are left blank rather than inferred.")
        f=("KARAT AND METAL LEFT BLANK / UNVERIFIED: inferring '14K white gold' from the SKU suffix '-14KW' would be an "
           "inference, not an observation. The listing page offers 14K/18K white, yellow and rose gold variants, so the "
           "variant must be confirmed on a dedicated product page.")
        if f not in r["flags"]: r["flags"].append(f)
        n+=1
with open("data/rings.jsonl","w",encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
print("patched rows:",n)
