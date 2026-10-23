/* generated from data.json by scripts/build_site.py — do not edit by hand */
window.GOLD5_DATA = {
 "meta": {
  "project": "GOLD5 — Solid Gold Engagement Ring Research",
  "asOf": "2026-10-23",
  "lastPass": "2026-10-23 (bc4e36a1 field-level live verification; integrated Kitco refresh from 3bf55199)",
  "session": "bc4e36a1",
  "title": "Gold engagement rings, verified line by line",
  "subtitle": "25 listings from 13 sellers · all 25 rows re-read live on 2026-10-23 · every value tied to the official source page that states it · blanks and source conflicts are flagged, never guessed",
  "noHallucinations": "NO HALLUCINATIONS IS THE RULE OF THIS PROJECT. Every price, karat, weight, policy and claim on this site was read from the linked official source page on the date shown next to it. If a value could not be confirmed, it is left BLANK and published on the Flagged for Review page — never inferred, estimated or filled in from a similar listing. Derived numbers (fine-gold grams, metal value, price/metal) are computed from verified inputs and recomputed by the checker. After every review pass, run python3 scripts/verify.py.",
  "checker": "python3 scripts/verify.py",
  "evidenceLedger": "data/live_check_bc4e36a1.json",
  "liveCheck": {
   "schemaVersion": 1,
   "session": "bc4e36a1",
   "branch": "arena/bc4e36a1-gold5",
   "checkedOn": "2026-10-23",
   "method": "Official URLs were opened with fetch_page and read at field level. Source excerpts were transcribed into this ledger before canonical values were changed. No missing value was inferred; EUR was not converted to USD; sold and variant prices are labeled by their actual basis.",
   "timeNote": "Only the retrieval date is asserted for fetches. A time is recorded only when the source itself displayed it (notably Kitco).",
   "noHallucinations": "Blank means unverified. A source conflict is published, not resolved by preference. Derived values must be recomputed from the canonical inputs.",
   "coverage": {
    "listing": 25,
    "policy": 9,
    "reference": 11,
    "spot": 1,
    "total": 46
   },
   "checks": [
    {
     "seq": 1,
     "id": "S01",
     "kind": "spot",
     "subject": "Kitco live gold quote",
     "url": "https://www.kitco.com/charts/gold",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Panel: Oct 23, 2026 16:12 NY; bid $3,996.10/oz; ask $3,998.10; gram $128.48; prices stated as of 4:10 p.m. EDT. Purity table: 24K $3,996.10; 22K $3,663.22; 18K $2,997.08; 14K $2,330.93; 10K $1,665.17. Separate body text showed $3,995.50/oz and $128.46/g; those body figures are not mixed into the panel quote."
    },
    {
     "seq": 2,
     "id": "L01",
     "kind": "listing",
     "entryId": "BN-192506",
     "subject": "Blue Nile Petite Hidden Halo Solitaire Plus",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1255,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$1,255 Setting Price; 14K Yellow Gold; stock 502250y14. No gram weight, explicit solid-gold wording, karat-stamp claim or maker's mark published. Return terms are read from the linked official policy."
    },
    {
     "seq": 3,
     "id": "L02",
     "kind": "listing",
     "entryId": "BN-195639",
     "subject": "Blue Nile Petite Solitaire",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1000,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$1,000 Setting Price; stock 501130y14; 14K Yellow Gold; width 1.80 mm. No gram weight or stamp/maker-mark statement published."
    },
    {
     "seq": 4,
     "id": "L03",
     "kind": "listing",
     "entryId": "BN-203257",
     "subject": "Blue Nile Classic Four Prong Solitaire",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 870,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$870 Setting Price; stock 500000y14; 14K Yellow Gold; width 1.90 mm. No gram weight published."
    },
    {
     "seq": 5,
     "id": "L04",
     "kind": "listing",
     "entryId": "BN-195326",
     "subject": "Blue Nile Riviera Pave",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1500,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$1,500 Setting Price; 14K White Gold; 1/6 ct. tw. No gram weight or stamp/maker-mark statement published."
    },
    {
     "seq": 6,
     "id": "L05",
     "kind": "listing",
     "entryId": "BN-195871",
     "subject": "Blue Nile French Pave",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1800,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$1,800 Setting Price; stock 501410y14; 14K Yellow Gold; width 2.50 mm; 16 round diamonds, 1/4 ct. tw. No gram weight published."
    },
    {
     "seq": 7,
     "id": "L06",
     "kind": "listing",
     "entryId": "BN-311132",
     "subject": "Blue Nile Criss Cross Solitaire",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 2320,
      "grams": null,
      "karat": 18,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$2,320 Setting Price; 18K Yellow Gold; by James Allen. No gram weight or stamp/maker-mark statement published."
    },
    {
     "seq": 8,
     "id": "L07",
     "kind": "listing",
     "entryId": "BN-203738",
     "subject": "Blue Nile Floral Marquise metal conflict",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "flagged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 2210,
      "grams": null,
      "karat": 18,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true,
      "metalConflict": "Title and specification say 18K White Gold; Product Details say 14K Yellow Gold."
     },
     "sourceExcerpt": "$2,210 Setting Price. The page title and specification identify 18K White Gold, but the Product Details text says 14K Yellow Gold. Both statements are preserved; neither is silently preferred."
    },
    {
     "seq": 9,
     "id": "L08",
     "kind": "listing",
     "entryId": "BN-203348",
     "subject": "Blue Nile Classic Simple Solitaire",
     "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-yellow-gold-item-203348",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1145,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$1,145 Setting Price; stock 502120y14; 14K Yellow Gold; width 2.40 mm. No gram weight published."
    },
    {
     "seq": 10,
     "id": "L09",
     "kind": "listing",
     "entryId": "BE-1343",
     "subject": "Brilliant Earth Freesia 2mm Solitaire",
     "url": "https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "blanked",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": null,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true,
      "displayedCurrency": "EUR",
      "displayedPrice": "€835 setting only"
     },
     "sourceExcerpt": "Direct product page displays €835 Setting Only, style BE1343-14KY, 14K Yellow Gold, width 2–1.2 mm. No current USD price was read, so the USD cell is blank and no conversion is made."
    },
    {
     "seq": 11,
     "id": "L10",
     "kind": "listing",
     "entryId": "BE-NADIA",
     "subject": "Brilliant Earth Nadia Diamond Ring",
     "url": "https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1250,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true,
      "displayedCurrency": "USD"
     },
     "sourceExcerpt": "$1,250 USD Setting Only; 14K Yellow Gold; 1.8 mm band. No gram weight published."
    },
    {
     "seq": 12,
     "id": "L11",
     "kind": "listing",
     "entryId": "BE-1343HH",
     "subject": "Brilliant Earth Freesia Hidden Halo",
     "url": "https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "blank-retained",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": null,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true,
      "displayedCurrency": "EUR",
      "displayedPrice": "€1,350 setting only"
     },
     "sourceExcerpt": "Direct product page displays €1,350 Setting Only; 14K Yellow Gold; width 2–1.3 mm; 14 accent diamonds totaling 0.05 ct. tw. USD remains blank; no conversion."
    },
    {
     "seq": 13,
     "id": "L12",
     "kind": "listing",
     "entryId": "BE-SECRET",
     "subject": "Brilliant Earth Secret Halo",
     "url": "https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1090,
      "grams": null,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true,
      "displayedCurrency": "USD"
     },
     "sourceExcerpt": "Direct product page now displays $1,090 USD Setting Only; 14K Yellow Gold; 1.5 mm; 13 accent diamonds totaling 0.06 ct. tw. The direct USD observation replaces the prior blank."
    },
    {
     "seq": 14,
     "id": "L13",
     "kind": "listing",
     "entryId": "AL-5882",
     "subject": "Allurez Filigree Solitaire Setting",
     "url": "https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1085,
      "grams": 5.0,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$1,085 setting only; style U5882; 14k yellow gold; Gold Weight 5.00 Grams (Approximate). Seller weight is not independently weighed."
    },
    {
     "seq": 15,
     "id": "L14",
     "kind": "listing",
     "entryId": "AL-170",
     "subject": "Allurez Antique Engraved Setting",
     "url": "https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 933,
      "grams": 4.8,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$933 setting only; style U170; 14k yellow gold; Gold Weight 4.80 grams (Approximate). Seller weight is not independently weighed."
    },
    {
     "seq": 16,
     "id": "L15",
     "kind": "listing",
     "entryId": "AL-4426",
     "subject": "Allurez Engraved Floral Setting",
     "url": "https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 585,
      "grams": 3.58,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "$585 setting only; style NG4426; 14k yellow gold; Approximate Metal Weight 3.58 grams. Seller weight is not independently weighed."
    },
    {
     "seq": 17,
     "id": "L16",
     "kind": "listing",
     "entryId": "AV-25893",
     "subject": "Avianne Diamond Solitaire",
     "url": "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 1100,
      "grams": 2.3,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": false
     },
     "sourceExcerpt": "$1,100 complete ring; item R25893; 14K Solid Yellow Gold; Item Weight 2.3 grams; 0.41 ct center diamond, VS2/G–H. Product page states 14-day returns for unworn/unaltered items; full policy was not captured."
    },
    {
     "seq": 18,
     "id": "L17",
     "kind": "listing",
     "entryId": "JM-149700",
     "subject": "Jewelry Master Brilliant Round Solitaire",
     "url": "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": 3020,
      "grams": 2.3,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": false
     },
     "sourceExcerpt": "Special Price $3,020; seller Retail Price $6,041 is not used; style 149700; 0.71 ctw; entirely handcrafted in pure 14KT solid yellow gold; Metal Weight 2.3 Grams. Thirty-day guarantee says some restrictions apply without listing them."
    },
    {
     "seq": 19,
     "id": "L18",
     "kind": "listing",
     "entryId": "SGJ-B02561",
     "subject": "Solid Gold Jewelers Solitaire",
     "url": "https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "blank-retained",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "observed": {
      "price": null,
      "grams": 4.7,
      "karat": 14,
      "solidStated": false,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": false
     },
     "sourceExcerpt": "Page states 14ky, 4.7g, #B02561 and asks buyers to call (309) 452-1612 for current pricing and availability. No price or return policy is published; price remains blank."
    },
    {
     "seq": 20,
     "id": "L19",
     "kind": "listing",
     "entryId": "ET-4426190660",
     "subject": "RAKSHAKJEWELS Radiant Lab Diamond Ring",
     "url": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 1891.78,
      "grams": null,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "14K Yellow Gold option $1,891.78; $1,202.08+ header is the silver option. Current title/description identify a 2.50-ct canary-yellow IGI lab-grown diamond, not moissanite. Returns and exchanges accepted within 14 days; buyer pays return shipping."
    },
    {
     "seq": 21,
     "id": "L20",
     "kind": "listing",
     "entryId": "ET-4366425533",
     "subject": "ForeverForLove Emerald Hidden Halo Ring",
     "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 546.09,
      "grams": null,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": true,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "14K Yellow/White/Rose Gold options range $546.09–$2,404.96 by center-diamond size; base/header starts at $375.80 for silver. Description says genuine 14k real gold, never plated or filled; Metal stamp: Yes. Returns within 30 days; buyer pays return shipping. No per-variant original price was read, so compare-at is blank."
    },
    {
     "seq": 22,
     "id": "L21",
     "kind": "listing",
     "entryId": "ET-1151446373",
     "subject": "VeraByEden Ruby and Diamond Halo Ring",
     "url": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 969,
      "grams": 3.7,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "14K option $969; $783+ header is 10K. Material: Solid Gold (not plated or filled); Karat 14 K (585); Gold grams 3.70 gr. Return within 7 days after receipt; $20 delivery charge and 10% restocking fee; buyer pays return shipping; personalized and listed custom items excluded."
    },
    {
     "seq": 23,
     "id": "L22",
     "kind": "listing",
     "entryId": "ET-1566052947",
     "subject": "VibrantStone Domed Band",
     "url": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 251.3,
      "grams": null,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "Listing titled 14k Solid Yellow Gold displays from $251.30; width-dependent ranges run through $1,742.30. Returns/exchanges within 21 days; customized bands and altered/used/damaged items may be excluded or incur fees up to 30%; buyer pays return shipping. No gram weight published."
    },
    {
     "seq": 24,
     "id": "L23",
     "kind": "listing",
     "entryId": "ET-1433905613",
     "subject": "adelafinejewels Comfort-Fit Dome Band",
     "url": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 999.7,
      "grams": null,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "14K Gold options $999.70–$1,368.90 by size; 10K options $674.70–$963.95; 8 mm white-gold band. Returns/exchanges accepted within 14 days; personalized products non-refundable; buyer pays return transportation. No gram weight or maker's mark stated."
    },
    {
     "seq": 25,
     "id": "L24",
     "kind": "listing",
     "entryId": "ET-944684759",
     "subject": "CittaliFineJewelry Flat Polished Band",
     "url": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 195.75,
      "grams": null,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": false,
      "makerMarkStated": false,
      "returnsVerified": true
     },
     "sourceExcerpt": "Listing titled 14k White Gold displays from $195.75 for 2 mm; width/size ranges run through $1,158.75. Description says the design is available in 10k, 14k and 18k solid gold and other materials, so the selected metal must be reconfirmed at checkout. Returns/exchanges accepted within 30 days; buyer pays return shipping."
    },
    {
     "seq": 26,
     "id": "L25",
     "kind": "listing",
     "entryId": "ET-576343849",
     "subject": "BUTTERFLYWINGVINTAGE sold band case study",
     "url": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
     "observed": {
      "price": 420,
      "grams": null,
      "karat": 14,
      "solidStated": true,
      "hallmarkStated": true,
      "makerMarkStated": true,
      "returnsVerified": false,
      "availability": "sold out"
     },
     "sourceExcerpt": "Sold-out detail page displays Price $420.00 and Original Price $525.00; this is not a current offer. Title says 7g, but description says the postal scale alternates between 6–7 g, so exact grams and metal value are blank. Description says marked 14K with a maker's mark and points to the fourth photo. Seller does not offer refunds for buyer's remorse or changed mind."
    },
    {
     "seq": 27,
     "id": "P01",
     "kind": "policy",
     "subject": "Blue Nile returns",
     "url": "https://www.bluenile.com/policies/returns",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Eligible original/unworn returns within 30 days of shipment; RMA required; two complimentary returns per customer/year. Personalized/custom/engraved/post-purchase-resized, Diamond Upgrade, clearance and final-sale items excluded. Missing grading report costs $150."
    },
    {
     "seq": 28,
     "id": "P02",
     "kind": "policy",
     "subject": "Blue Nile warranty and resizing",
     "url": "https://www.bluenile.com/services/warranty",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Limited lifetime manufacturing-defect warranty for gold/platinum items priced $1,000 or more; exclusions published. One free resize up/down two sizes within 6 months if design permits; non-resizable styles excluded."
    },
    {
     "seq": 29,
     "id": "P03",
     "kind": "policy",
     "subject": "Blue Nile contact",
     "url": "https://www.bluenile.com/contact-us",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Official contact page lists 1-800-242-2728 and service@bluenile.com, plus chat and showroom options."
    },
    {
     "seq": 30,
     "id": "P04",
     "kind": "policy",
     "subject": "Brilliant Earth returns",
     "url": "https://www.brilliantearth.com/30-Day-Returns/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Free 30-day returns/exchanges run from availability for shipment or pickup; original/unworn condition required. Engraved rings may be returned with a $40 engraving-removal charge. Personalized/custom and other published exclusions apply; free FedEx label instructions are provided."
    },
    {
     "seq": 31,
     "id": "P05",
     "kind": "policy",
     "subject": "Brilliant Earth manufacturing warranty",
     "url": "https://www.brilliantearth.com/customer-service/warranty/#manufacturing_warranty",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Free lifetime manufacturing-defect warranty on fine jewelry; wear, gemstone loss, product loss and theft excluded. US/CAN/AUS/UK customers receive free return labels; elsewhere a $50 deposit applies and is refunded for warrantied repairs. Unauthorized repair voids coverage."
    },
    {
     "seq": 32,
     "id": "P06",
     "kind": "policy",
     "subject": "Brilliant Earth contact",
     "url": "https://www.brilliantearth.com/contact/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Official contact page lists 800.691.0952 and store/virtual-appointment links."
    },
    {
     "seq": 33,
     "id": "P07",
     "kind": "policy",
     "subject": "Allurez returns",
     "url": "https://www.allurez.com/pages/return-policy",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Returns must arrive within 30 days of original shipment and require RMA; customer pays return shipping; original shipping is nonrefundable; approved refunds issue within 7 business days. Design Your Own rings are exchange-only under the published terms."
    },
    {
     "seq": 34,
     "id": "P08",
     "kind": "policy",
     "subject": "Allurez warranty",
     "url": "https://www.allurez.com/pages/warranty",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "corrected",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Complimentary 1-year limited manufacturing-defect warranty for qualifying US purchases after February 2024. Ring sizing is offered except full eternity rings. Missing stones may be replaced, but the cost of the new stone is not covered. Wear, loss and unauthorized repair excluded; after one year repair fees plus a $39 shipping charge apply."
    },
    {
     "seq": 35,
     "id": "P09",
     "kind": "policy",
     "subject": "Allurez contact",
     "url": "https://www.allurez.com/pages/contact",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
     "sourceExcerpt": "Official contact page lists 800.554.3509, outside-US 646.627.7353, and service@allurez.com."
    },
    {
     "seq": 36,
     "id": "R01",
     "kind": "reference",
     "referenceId": "ftc-consumer",
     "subject": "FTC jewelry buying guidance",
     "url": "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Near the karat quality mark, look for the name or US registered trademark of the company behind it; if there is no trademark with the karat mark, FTC says do not buy. Solid gold means not hollow. Return policies should be obtained in writing."
    },
    {
     "seq": 37,
     "id": "R02",
     "kind": "reference",
     "referenceId": "cfr23",
     "subject": "eCFR 16 CFR Part 23",
     "url": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "eCFR displays Title 16 up to date as of 10/21/2026 and last amended 10/19/2026. Part 23 includes §23.3 gold content, §23.10 quality marks and §23.18 weight representations."
    },
    {
     "seq": 38,
     "id": "R03",
     "kind": "reference",
     "referenceId": "usc295",
     "subject": "15 USC 295 gold fineness tolerance",
     "url": "https://www.govinfo.gov/link/uscode/15/295",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Actual fineness may not be more than three one-thousandth parts below the mark on the tested solder-free part; for the entire article including solder, seven one-thousandth parts applies to articles other than watchcases or flatware."
    },
    {
     "seq": 39,
     "id": "R04",
     "kind": "reference",
     "referenceId": "cfr23-3",
     "subject": "16 CFR 23.3 gold-content representations",
     "url": "https://www.law.cornell.edu/cfr/text/16/23.3",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Misrepresenting the presence, quantity or karat fineness of gold is unfair or deceptive. The rule also says hollow-center products should not be described as solid gold."
    },
    {
     "seq": 40,
     "id": "R05",
     "kind": "reference",
     "referenceId": "usc297",
     "subject": "15 USC 297 identifying trademark",
     "url": "https://www.law.cornell.edu/uscode/text/15/297",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Section 297(b) requires the identifying trademark or name to be applied by the same means, at least as large, and as close as possible to the quality mark."
    },
    {
     "seq": 41,
     "id": "R06",
     "kind": "reference",
     "referenceId": "nist-troy",
     "subject": "NIST troy-ounce conversion",
     "url": "https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Appendix B.8 lists ounce (troy or apothecary) to gram as 3.110348 E+01 (rounded display). The calculator retains Kitco's more precise stated 31.1034768 g/ozt constant and labels that source separately."
    },
    {
     "seq": 42,
     "id": "R07",
     "kind": "reference",
     "referenceId": "lbma",
     "subject": "LBMA precious-metal benchmark process",
     "url": "https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "LBMA Gold Price is set twice daily in IBA-administered auctions commencing at 10:30 and 15:00 London time."
    },
    {
     "seq": 43,
     "id": "R08",
     "kind": "reference",
     "referenceId": "ftc-credit",
     "subject": "FTC credit-card disputes",
     "url": "https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "FTC explains the right to dispute billing errors and separately addresses complaints about the quality of goods and services."
    },
    {
     "seq": 44,
     "id": "R09",
     "kind": "reference",
     "referenceId": "etsy-pp",
     "subject": "Etsy Purchase Protection",
     "url": "https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Full refund for qualifying orders that do not arrive, arrive damaged, arrive 7+ days after the maximum estimated delivery window, or differ significantly from description/photos. Other dissatisfaction is directed to the seller's return policy."
    },
    {
     "seq": 45,
     "id": "R10",
     "kind": "reference",
     "referenceId": "jvc",
     "subject": "JVC jewelry-dispute mediation",
     "url": "https://jvclegal.org/mediation-services/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "JVC offers a jewelry-purchase dispute mediation program for consumers and trade members; acceptance depends on resources, eligible submissions, viable claims and supporting evidence."
    },
    {
     "seq": 46,
     "id": "R11",
     "kind": "reference",
     "referenceId": "reportfraud",
     "subject": "FTC Report Fraud",
     "url": "https://reportfraud.ftc.gov/",
     "status": "read",
     "checkedOn": "2026-10-23",
     "result": "unchanged",
     "evidencePath": "verification/evidence/bc4e36a1/spot-and-references.md",
     "sourceExcerpt": "Official portal for reporting fraud, scams and bad business practices; reports are shared with law-enforcement partners, but FTC does not resolve individual reports."
    }
   ],
   "corrections": [
    {
     "id": "C-01",
     "subject": "Kitco quote",
     "before": "$4,022.50/oz and $129.33/g at 5:44 a.m. ET",
     "after": "$3,996.10/oz and $128.48/g from the 16:12 NY panel, with source prices as of 4:10 p.m. EDT",
     "reason": "New official-page observation; every derived value must use the same panel quote."
    },
    {
     "id": "C-02",
     "subject": "BE-1343",
     "before": "$750 USD",
     "after": "USD blank; current page displays €835",
     "reason": "Do not convert currency or carry forward a stale USD observation."
    },
    {
     "id": "C-03",
     "subject": "BE-1343HH",
     "before": "USD blank with prior $1,190 observation",
     "after": "USD remains blank; current page displays €1,350",
     "reason": "No current USD price was read."
    },
    {
     "id": "C-04",
     "subject": "BE-SECRET",
     "before": "USD blank after an EUR response",
     "after": "$1,090 USD from the direct product page",
     "reason": "A current direct USD observation now exists."
    },
    {
     "id": "C-05",
     "subject": "ET-4366425533",
     "before": "$547.26 from 14K options",
     "after": "$546.09 from 14K options; upper range $2,404.96",
     "reason": "Current variant ranges changed; unrelated header compare-at was removed rather than inferred."
    },
    {
     "id": "C-06",
     "subject": "ET-576343849",
     "before": "$444.80 and exact 7 g used for a below-metal case study",
     "after": "$420 sold-listing display; exact grams blank because the description says 6–7 g; maker's mark claim recorded",
     "reason": "The old calculation relied on a snippet and an exact weight the seller did not state. The below-metal conclusion is withdrawn."
    },
    {
     "id": "C-07",
     "subject": "BN-203738",
     "before": "18K White Gold presented without the conflicting body text",
     "after": "Title/specification 18K White Gold and Product Details 14K Yellow Gold published together with a conflict flag",
     "reason": "A source conflict must be visible, not silently resolved."
    },
    {
     "id": "C-08",
     "subject": "Etsy provenance and variant labels",
     "before": "Seven rows marked prior after collector HTTP 500 responses; several header compare-at prices were attached to 14K prices",
     "after": "All seven listing pages read live; return windows added where stated; mismatched compare-at values blanked",
     "reason": "Direct pages now exposed variant and policy fields. A header price for another material is not evidence for a 14K compare-at value."
    },
    {
     "id": "C-09",
     "subject": "Return and warranty wording",
     "before": "Brilliant Earth engraved items described as not eligible; Allurez missing-stone wording could imply the stone cost was covered",
     "after": "Brilliant Earth $40 engraving-removal charge and Allurez new-stone cost exclusion stated explicitly",
     "reason": "Official policy pages contradicted the shorthand."
    }
   ]
  },
  "coverage": {
   "live": 25,
   "prior": 0,
   "liveDate": "2026-10-23",
   "priorDate": null
  },
  "archive": [
   {
    "label": "Session 638c9614 — research site at /docs/",
    "path": "docs/index.html"
   },
   {
    "label": "Session 090bae73 — checklist guide",
    "path": "index-090bae73.html"
   },
   {
    "label": "Session 37e8ff42 — dashboard snapshot",
    "path": "archive/session-37e8ff42/index.html"
   },
   {
    "label": "Session 93032b31 — 24-row pass-2 dashboard (superseded, preserved)",
    "path": "archive/session-93032b31/index.html"
   },
   {
    "label": "Session 84be683f — generated site at /verified/",
    "path": "verified/index.html"
   },
   {
    "label": "Session 60c4b9c3 — report site at /report/",
    "path": "report/index.html"
   },
   {
    "label": "Checklist guide at /guide/",
    "path": "guide/index.html"
   },
   {
    "label": "Session b1f2fe3b — Master Cross-Session Audit & XRF Assay Calculator (38 unified rows)",
    "path": "site/master-audit.html"
   },
   {
    "label": "Session 0c967748 — current-evidence review (blank current fields, R01–R04)",
    "path": "review/index.html"
   },
   {
    "label": "Session 3e3fae49 — 58-row dossier at /dossier/ (18/18 anti-hallucination checks)",
    "path": "dossier/index.html"
   }
  ],
  "counts": {
   "entries": 25,
   "sellers": 13,
   "flags": 30,
   "references": 11
  }
 },
 "spot": {
  "primary": {
   "source": "Kitco Metals Inc. — Live Gold Price",
   "url": "https://www.kitco.com/charts/gold",
   "usdPerOz": 3996.1,
   "usdPerGram": 128.48,
   "asOf": "2026-10-23 4:10 p.m. ET",
   "kind": "spot bid",
   "method": "live fetch (2026-10-23 4:10 p.m. ET panel; integrated sessions 3bf55199 + bc4e36a1)",
   "quote": "Live Gold Price — Oct 23, 2026 - 16:12 NY Time. Bid 3,996.10 USD (-26.90, -0.67%); Ask 3,998.10; gram 128.48 (-0.86); Kilo 128,479.57; pennyweight 199.81. 'Prices provided by Kitco Metals Inc. ... as of October 23, 2026 at 4:10 p.m. EDT.' Body text: 'The current price of gold is $3,995.50 per troy ounce as of October 23, 2026, 4:10 p.m. ET, down $27.80 today.'"
  },
  "prior": [
   {
    "source": "Kitco Metals Inc. — Live Gold Price",
    "url": "https://www.kitco.com/charts/gold",
    "usdPerOz": 4022.5,
    "usdPerGram": 129.33,
    "asOf": "2026-10-23 5:44 a.m. ET",
    "kind": "spot bid",
    "method": "live fetch (2026-10-23 5:44 a.m. ET pass, session 77405ae3)",
    "note": "Previous 2026-10-23 quote (5:44 a.m. ET); superseded by 4:10 p.m. ET quote above. Bid fell $26.40/oz intraday."
   },
   {
    "source": "Kitco Metals Inc. — Live Gold Price (previous session)",
    "url": "https://www.kitco.com/charts/gold",
    "usdPerOz": 4026.9,
    "usdPerGram": 129.47,
    "asOf": "2026-10-22 7:26 p.m. ET",
    "kind": "spot bid",
    "method": "prior-session capture (session 7cca80c9)",
    "note": "2026-10-22 close-of-day capture, recorded by the previous pass; superseded by the 2026-10-23 quote above."
   },
   {
    "source": "Kitco Metals Inc. — Live Gold Price (earlier capture)",
    "url": "https://www.kitco.com/charts/gold",
    "usdPerOz": 4025.0,
    "usdPerGram": 129.41,
    "asOf": "2026-10-22 7:10 p.m. ET",
    "kind": "spot bid",
    "method": "prior-session capture (session 37e8ff42)",
    "note": "Same Kitco page 16 minutes earlier; used by the archived sessions."
   }
  ],
  "crossChecks": [
   {
    "source": "CNBC Select (2026-10-22 capture)",
    "url": "https://www.cnbc.com/select/the-price-of-gold-today-oct-22-2026/",
    "usdPerOz": 4083.82,
    "usdPerGram": null,
    "asOf": "2026-10-22 9:00 a.m. ET",
    "kind": "spot",
    "method": "prior-session capture",
    "note": "Prior-day cross-check only. Gold's spot price as of 9:00 a.m. ET was $4,083.82 per ounce, per CNBC's Gold/US Dollar Spot Price."
   },
   {
    "source": "APMEX (2026-10-22 capture)",
    "url": "https://www.apmex.com/gold-price",
    "usdPerOz": 4077.6,
    "usdPerGram": 131.1,
    "asOf": "2026-10-22 11:02 a.m. ET",
    "kind": "spot",
    "method": "prior-session capture",
    "note": "Prior-day cross-check only. Gold Spot Price $4,077.60; Per Gram $131.10; Last Updated 10/22/2026 11:02:00 AM ET."
   },
   {
    "source": "Kitco News AM report (2026-10-22)",
    "url": "https://www.kitco.com/news/article/2026-10-22/gold-silver-pressured-despite-lower-yields-hormuz-attacks-send-crude-higher",
    "usdPerOz": 4086.9,
    "usdPerGram": null,
    "asOf": "2026-10-22 morning",
    "kind": "spot",
    "method": "prior-session capture",
    "note": "Spot gold near $4,086.90 an ounce, down $53.40 (1.29%)."
   }
  ],
  "notes": [
   "The 2026-10-23 4:10 p.m. ET capture shows the bid ticker at $3,996.10 with $128.48/g, the page's own 'Gold Price Today' table at $3,995.50/oz and $128.46/g, and the purity calculator's 24K line at $3,996.10. The ticker bid and its per-gram figure are the numbers used for every calculation; the timestamp is part of the value. Intraday move from $4,022.50 at 5:44 a.m. ET to $3,996.10 at 4:10 p.m. ET was -$26.40/oz (-0.66%).",
   "Earlier quotes (5:44 a.m. ET and 2026-10-22) are retained only as dated history and are labelled prior-day. They are not used in any calculation on this site."
  ],
  "purity": {
   "fineness": {
    "24K": 0.9999,
    "22K": 0.9167,
    "18K": 0.75,
    "14K": 0.5833,
    "10K": 0.4167
   },
   "perOz": {
    "24K": 3996.1,
    "22K": 3663.22,
    "18K": 2997.08,
    "14K": 2330.93,
    "10K": 1665.17
   },
   "source": "Kitco 'Gold Value by Purity' table, same 2026-10-23 4:10 p.m. ET page capture"
  }
 },
 "entries": [
  {
   "id": "BN-192506",
   "name": "Petite Hidden Halo Solitaire Plus Diamond Engagement Ring, 14K Yellow Gold",
   "short": "Petite Hidden Halo Solitaire Plus",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1255,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,255 setting price (center diamond extra); stock 502250y14",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L01",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21",
    "FL-06"
   ],
   "notes": [
    "Direct product page re-read live on 2026-10-23; setting price and product specifications recorded.",
    "Lifetime warranty applies only to items priced $1,000 or more.",
    "Current official-source read: L01 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-195639",
   "name": "Petite Solitaire Engagement Ring, 14k Yellow Gold",
   "short": "Petite Solitaire",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1000,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,000 setting price (center diamond extra)",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L02",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21",
    "FL-06"
   ],
   "notes": [
    "Direct product page re-read live on 2026-10-23; setting price and product specifications recorded.",
    "Current official-source read: L02 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-203257",
   "name": "Classic Four Prong Solitaire Engagement Ring, 14K Yellow Gold",
   "short": "Classic Four Prong Solitaire",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 870,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$870 setting price (center diamond extra); stock 500000y14",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 1.9,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L03",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-four-prong-solitaire-engagement-ring-in-14k-yellow-gold-item-203257",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21",
    "FL-06"
   ],
   "notes": [
    "Product page re-read this pass: $870 (Setting Price), Metal 14K Yellow Gold, Width 1.90mm.",
    "Current official-source read: L03 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-195326",
   "name": "Riviera Pavé Diamond Engagement Ring, 14K White Gold (1/6 ct. tw.)",
   "short": "Riviera Pavé 1/6 ct. tw.",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "White Gold",
   "price": 1500,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,500 setting price (center diamond extra)",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L04",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21"
   ],
   "notes": [
    "Direct product page re-read live on 2026-10-23; setting price and product specifications recorded.",
    "Current official-source read: L04 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-195871",
   "name": "French Pavé Diamond Engagement Ring, 14k Yellow Gold (1/4 ct. tw.)",
   "short": "French Pavé 1/4 ct. tw.",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1800,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,800 setting price (center diamond extra); stock 501410y14",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 2.5,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L05",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-14k-yellow-gold-1-4-ct-tw-item-195871",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21"
   ],
   "notes": [
    "Product page re-read this pass: $1,800 (Setting Price), 14K Yellow Gold, 2.50mm, 16 diamonds 1/4 ct. tw.",
    "Current official-source read: L05 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-311132",
   "name": "Criss Cross Solitaire Engagement Ring, 18K Yellow Gold (by James Allen)",
   "short": "Criss Cross Solitaire (James Allen)",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 18,
   "metalColor": "Yellow Gold",
   "price": 2320,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$2,320 setting price (center diamond extra)",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L06",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21"
   ],
   "notes": [
    "Direct product page re-read live on 2026-10-23; setting price and product specifications recorded.",
    "Current official-source read: L06 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-203738",
   "name": "Floral Marquise Diamond Engagement Ring — metal description conflict",
   "short": "Floral Marquise — metal conflict",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 18,
   "metalColor": "White Gold (title/specification)",
   "price": 2210,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$2,210 setting price (center diamond extra); metal description is internally conflicting (FL-30)",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": "Title and specification say 18K White Gold; Product Details say 14K Yellow Gold.",
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L07",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21",
    "FL-30"
   ],
   "notes": [
    "Direct product page re-read live: $2,210 Setting Price; title/specification 18K White Gold; Product Details 14K Yellow Gold (FL-30).",
    "Current official-source read: L07 (flagged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BN-203348",
   "name": "Classic Simple Solitaire Engagement Ring, 14K Yellow Gold",
   "short": "Classic Simple Solitaire",
   "sellerId": "bluenile",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1145,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,145 setting price (center diamond extra); stock 502120y14",
   "priceSourceUrl": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-yellow-gold-item-203348",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 2.4,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "evidenceId": "L08",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-yellow-gold-item-203348",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-05",
    "FL-21",
    "FL-06"
   ],
   "notes": [
    "Product page re-read this pass: $1,145 (Setting Price), Stock 502120y14, 14K Yellow Gold, Width 2.40mm.",
    "Current official-source read: L08 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BE-1343",
   "name": "Freesia 2mm Solitaire Ring, 14K Yellow Gold (BE1343-14KY)",
   "short": "Freesia 2mm Solitaire",
   "sellerId": "brilliantearth",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": null,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "USD price not confirmable — direct product page served EUR €835 setting only on 2026-10-23 (FL-08); prior USD $750 is a dated observation only, no conversion",
   "priceSourceUrl": "https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 2.0,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Product pages state 'Free Shipping & Returns' and 'Free 1-Year Resizing'. Verified live at brilliantearth.com/30-Day-Returns/ on 2026-10-23: free returns/exchanges within 30 days of the item being available for shipment or pickup, unworn and in original condition. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. Phone return instructions and a free FedEx label are published.",
   "returnUrl": "https://www.brilliantearth.com/30-Day-Returns/",
   "returnsVerified": true,
   "evidenceId": "L09",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-21",
    "FL-08"
   ],
   "notes": [
    "Direct product page re-read live: €835 Setting Only, style BE1343-14KY, 14K Yellow Gold, width 2–1.2 mm; current USD price blank (FL-08).",
    "Prior $750 USD and 80 reviews at 4.8/5 are dated observations, not current claims.",
    "Current official-source read: L09 (blanked); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BE-NADIA",
   "name": "Nadia Diamond Ring, 14K Yellow Gold (BE1D6013)",
   "short": "Nadia Diamond Ring",
   "sellerId": "brilliantearth",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1250,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,250 setting only (center diamond extra)",
   "priceSourceUrl": "https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 1.8,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Product pages state 'Free Shipping & Returns' and 'Free 1-Year Resizing'. Verified live at brilliantearth.com/30-Day-Returns/ on 2026-10-23: free returns/exchanges within 30 days of the item being available for shipment or pickup, unworn and in original condition. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. Phone return instructions and a free FedEx label are published.",
   "returnUrl": "https://www.brilliantearth.com/30-Day-Returns/",
   "returnsVerified": true,
   "evidenceId": "L10",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-21"
   ],
   "notes": [
    "Product page re-read this pass: $1,250 (Setting Only), 14K Yellow Gold, 1.8mm band; 143 reviews shown.",
    "Current official-source read: L10 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BE-1343HH",
   "name": "Freesia Hidden Halo Diamond Ring, 14K Yellow Gold (BE1D3939)",
   "short": "Freesia Hidden Halo",
   "sellerId": "brilliantearth",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": null,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "USD price not confirmable — product page served EUR €1,350.00 on 2026-10-23 (FL-08); prior USD $1,190 seen on the product page 2026-10-22 (dated observation only, no conversion)",
   "priceSourceUrl": "https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 2.0,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Product pages state 'Free Shipping & Returns' and 'Free 1-Year Resizing'. Verified live at brilliantearth.com/30-Day-Returns/ on 2026-10-23: free returns/exchanges within 30 days of the item being available for shipment or pickup, unworn and in original condition. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. Phone return instructions and a free FedEx label are published.",
   "returnUrl": "https://www.brilliantearth.com/30-Day-Returns/",
   "returnsVerified": true,
   "evidenceId": "L11",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-21",
    "FL-08"
   ],
   "notes": [
    "Direct product page re-read live: €1,350 Setting Only, style BE1D3939-14KY, 14K Yellow Gold, 2–1.3 mm, 14 accent diamonds 0.05 ct. tw.; USD remains blank (FL-08). Prior $1,190 USD is a dated observation only.",
    "Current official-source read: L11 (blank-retained); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "BE-SECRET",
   "name": "Secret Halo 1.5mm Diamond Ring, 14K Yellow Gold (BE1D13065)",
   "short": "Secret Halo 1.5mm",
   "sellerId": "brilliantearth",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1090,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,090 USD setting only (center diamond extra), read directly on the product page 2026-10-23; an earlier €1,250 EUR response is dated history, not converted",
   "priceSourceUrl": "https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 1.5,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Product pages state 'Free Shipping & Returns' and 'Free 1-Year Resizing'. Verified live at brilliantearth.com/30-Day-Returns/ on 2026-10-23: free returns/exchanges within 30 days of the item being available for shipment or pickup, unworn and in original condition. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. Phone return instructions and a free FedEx label are published.",
   "returnUrl": "https://www.brilliantearth.com/30-Day-Returns/",
   "returnsVerified": true,
   "evidenceId": "L12",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-15",
    "FL-14",
    "FL-21"
   ],
   "notes": [
    "Direct product page re-read live: $1,090 USD Setting Only; 14K Yellow Gold; 1.5 mm; 13 accent diamonds 0.06 ct. tw. This direct USD observation replaces the prior EUR-only blank; the earlier €1,250 EUR response remains dated history and FL-08 no longer applies to this row.",
    "Current official-source read: L12 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "AL-5882",
   "name": "Filigree Designed Solitaire Engagement Ring Setting, 14K Yellow Gold (U5882)",
   "short": "Filigree Solitaire Setting",
   "sellerId": "allurez",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1085,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$1,085 setting only (center stone sold separately)",
   "priceSourceUrl": "https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold",
   "grams": 5.0,
   "gramsText": "5.00 grams (approximate)",
   "gramsNote": "Seller's published 'Gold Weight 5.00 Grams (Approximate)'",
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Return must ARRIVE at Allurez within 30 days of original shipment; unused, not resized or altered. Engraved items, custom-made orders, contoured wedding bands, clearance items, appraisals, gift cards and layaway deposits are non-refundable. Design Your Own rings may be exchanged only (same or higher value). Buyer pays return shipping; original shipping not refunded; $300 deduction per missing diamond certificate; refund within 7 business days.",
   "returnUrl": "https://www.allurez.com/pages/return-policy",
   "returnsVerified": true,
   "evidenceId": "L13",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-15",
    "FL-14",
    "FL-09",
    "FL-10",
    "FL-18"
   ],
   "notes": [
    "Product page re-read this pass: $1,085, style U5882, 14k yellow gold, gold weight 5.00 g approx., widths 2.9/2.3 mm.",
    "Page also shows a '$2,497 Everyone Else / 57% Savings' comparison — seller marketing, not used.",
    "Current official-source read: L13 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "AL-170",
   "name": "Antique Engraved Solitaire Engagement Ring Setting, 14k Yellow Gold (U170)",
   "short": "Antique Engraved Setting",
   "sellerId": "allurez",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 933,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$933 setting only (center stone sold separately)",
   "priceSourceUrl": "https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold",
   "grams": 4.8,
   "gramsText": "4.80 grams (approximate)",
   "gramsNote": "Seller's published 'Gold Weight 4.80 grams (Approximate)'",
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Return must ARRIVE at Allurez within 30 days of original shipment; unused, not resized or altered. Engraved items, custom-made orders, contoured wedding bands, clearance items, appraisals, gift cards and layaway deposits are non-refundable. Design Your Own rings may be exchanged only (same or higher value). Buyer pays return shipping; original shipping not refunded; $300 deduction per missing diamond certificate; refund within 7 business days.",
   "returnUrl": "https://www.allurez.com/pages/return-policy",
   "returnsVerified": true,
   "evidenceId": "L14",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.allurez.com/products/antique-engraved-solitaire-engagement-ring-setting-14k-yellow-gold",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-15",
    "FL-14",
    "FL-09",
    "FL-10",
    "FL-18"
   ],
   "notes": [
    "Product page re-read this pass: $933, style U170, 14k yellow gold, gold weight 4.80 g approx., widths 3.20/2.40 mm.",
    "Page also shows a '$1,373 Everyone Else / 32% Savings' comparison — not used.",
    "Current official-source read: L14 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "AL-4426",
   "name": "Engraved Floral Solitaire Engagement Ring Setting, 14K Yellow Gold (NG4426)",
   "short": "Engraved Floral Setting",
   "sellerId": "allurez",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 585,
   "compareAt": null,
   "priceBasis": "setting",
   "priceNote": "$585 setting only (center stone sold separately)",
   "priceSourceUrl": "https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold",
   "grams": 3.58,
   "gramsText": "3.58 grams (approximate)",
   "gramsNote": "Seller's published 'Approximate Metal Weight 3.58 grams'",
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Return must ARRIVE at Allurez within 30 days of original shipment; unused, not resized or altered. Engraved items, custom-made orders, contoured wedding bands, clearance items, appraisals, gift cards and layaway deposits are non-refundable. Design Your Own rings may be exchanged only (same or higher value). Buyer pays return shipping; original shipping not refunded; $300 deduction per missing diamond certificate; refund within 7 business days.",
   "returnUrl": "https://www.allurez.com/pages/return-policy",
   "returnsVerified": true,
   "evidenceId": "L15",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.allurez.com/products/floral-solitaire-engagement-ring-14k-yellow-gold",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-15",
    "FL-14",
    "FL-09",
    "FL-10",
    "FL-18"
   ],
   "notes": [
    "Product page re-read this pass: $585, style NG4426, 14k yellow gold, approximate metal weight 3.58 g.",
    "Page also shows a '$1,194 Everyone Else / 51% Savings' comparison — not used.",
    "Current official-source read: L15 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "AV-25893",
   "name": "14K Solid Yellow Gold Diamond Solitaire Engagement Ring, 0.41 Ctw (R25893)",
   "short": "Diamond Solitaire 0.41 Ctw",
   "sellerId": "avianne",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1100,
   "compareAt": null,
   "priceBasis": "complete",
   "priceNote": "$1,100 complete ring including 0.41 ct center diamond",
   "priceSourceUrl": "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
   "grams": 2.3,
   "gramsText": "2.3 grams",
   "gramsNote": "Seller's published 'Item Weight 2.3 grams'",
   "widthMm": 4.5,
   "solidStated": true,
   "solidQuote": "Product title: '14K Solid Yellow Gold'",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns of unworn and unaltered items accepted within 14 days. Full policy page not captured; resize/custom exclusions not confirmed.",
   "returnUrl": "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
   "returnsVerified": false,
   "evidenceId": "L16",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-14",
    "FL-11"
   ],
   "notes": [
    "Product page re-read this pass: $1,100.00, item code R25893, 14K Gold, 2.3 grams, 0.41 Ctw, 4.5 mm width, VS2 clarity, G/H color.",
    "Site-wide banner: 10% OFF with code 'FALL10' — recorded price is the listed price before that code.",
    "Current official-source read: L16 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "JM-149700",
   "name": "Brilliant Round Diamond Solitaire Engagement Ring, 14K Yellow Gold (Style 149700)",
   "short": "Brilliant Round Solitaire 0.71 ctw",
   "sellerId": "jewelrymaster",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 3020,
   "compareAt": 6041,
   "priceBasis": "complete",
   "priceNote": "$3,020 'Special Price' complete ring including 0.71 ctw diamonds (seller 'Retail Price' $6,041, not used)",
   "priceSourceUrl": "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
   "grams": 2.3,
   "gramsText": "2.3 grams",
   "gramsNote": "Seller's published 'Metal Weight: 2.3 Grams'",
   "widthMm": null,
   "solidStated": true,
   "solidQuote": "Description: 'entirely handcrafted in pure 14KT solid yellow gold'",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "30-day return or exchange under the 'Money Back Guarantee (some restrictions apply)'; the specific restrictions are not stated on the page.",
   "returnUrl": "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
   "returnsVerified": false,
   "evidenceId": "L17",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-14",
    "FL-12"
   ],
   "notes": [
    "Product page re-read this pass: Retail Price $6,041.00 / Special Price $3,020.00, style 149700, 0.71 ctw, 14KT gold, 2.3 grams, in stock (only 1 left).",
    "Includes free shipping, gift box and a professional appraisal certificate per the page.",
    "Current official-source read: L17 (unchanged); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "SGJ-B02561",
   "name": "Yellow Gold Solitaire Engagement Ring, 14K Yellow (SKU B02561, brand M Michael)",
   "short": "Yellow Gold Solitaire (M Michael)",
   "sellerId": "solidgoldjewelers",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": null,
   "compareAt": null,
   "priceBasis": "complete",
   "priceNote": "No price published — page says 'Call (309) 452-1612 for current pricing and availability.'",
   "priceSourceUrl": "https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
   "grams": 4.7,
   "gramsText": "4.7 g",
   "gramsNote": "Page states '14ky, 4.7g, #B02561'",
   "widthMm": null,
   "solidStated": false,
   "solidQuote": null,
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "No return policy shown on the product page.",
   "returnUrl": "https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
   "returnsVerified": false,
   "evidenceId": "L18",
   "evidencePath": "verification/evidence/bc4e36a1/retailers.md",
   "url": "https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-13",
    "FL-15",
    "FL-14",
    "FL-18"
   ],
   "notes": [
    "Product page re-read this pass: '14ky, 4.7g, #B02561', brand M Michael, no price shown, call for pricing.",
    "Current official-source read: L18 (blank-retained); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "ET-4426190660",
   "name": "2.50 CT Radiant Canary Lab-Grown Diamond Ring, IGI Certified, 14K Yellow Gold",
   "short": "2.50 CT Radiant Lab Diamond",
   "sellerId": "etsy-rakshakjewels",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 1891.78,
   "compareAt": null,
   "priceBasis": "complete",
   "priceNote": "14K Yellow Gold option $1,891.78; 10K $1,686.02; 18K $2,109.58; list starts at $1,202.08 for 925 silver. The header compare-at belongs to another variant, so compareAt is blank.",
   "priceSourceUrl": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 1.8,
   "solidStated": true,
   "solidQuote": "Description: 'Metal Options: Available in 10K/14K/18K Solid Gold (White, Yellow, Rose Gold) & Platinum'",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns & exchanges accepted within 14 days; buyer pays return shipping; original condition required.",
   "returnUrl": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
   "returnsVerified": true,
   "evidenceId": "L19",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-16",
    "FL-17",
    "FL-14"
   ],
   "notes": [
    "Listing re-read this pass: $1,202.08+ base (925 silver), 14K Yellow Gold $1,891.78, 2.50 ct radiant yellow lab-grown diamond (VVS2), 0.32 ctw side stones, band 1.80 mm, IGI certificate offered.",
    "Shop is Etsy 'Star Seller' with a 5/5 listing rating.",
    "Current official-source read: L19 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "ET-4366425533",
   "name": "Emerald Cut E/VVS2 IGI Lab-Grown Diamond Hidden Halo Ring, 14K Gold",
   "short": "Emerald Cut Hidden Halo",
   "sellerId": "etsy-foreverforlove",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow / White / Rose Gold",
   "price": 546.09,
   "compareAt": null,
   "priceBasis": "from",
   "priceNote": "14K options $546.09–$2,404.96 by center-diamond size; list starts at $375.80 for 925 silver. No 14K-specific compare-at price was published, so compareAt is blank.",
   "priceSourceUrl": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": true,
   "solidQuote": "Description: 'Made with genuine 14k real gold – never plated or filled'",
   "hallmarkStated": true,
   "hallmarkQuote": "Description: 'Metal stamp: Yes' (no maker's mark stated, no photo)",
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns & exchanges accepted within 30 days; buyer pays return shipping; description states a full refund/exchange and a lifetime warranty on manufacturer defects.",
   "returnUrl": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
   "returnsVerified": true,
   "evidenceId": "L20",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-16",
    "FL-17",
    "FL-14"
   ],
   "notes": [
    "Listing re-read live on 2026-10-23: 14K options $546.09–$2,404.96; silver header $375.80+; Metal stamp: Yes; 30-day returns.",
    "Ships from the UK; duties included for US orders per listing description.",
    "Current official-source read: L20 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null,
   "stoneIncluded": true
  },
  {
   "id": "ET-1151446373",
   "name": "14K Solid Gold Ruby + 0.30 CT Diamond Halo Ring",
   "short": "Ruby + Diamond Halo",
   "sellerId": "etsy-verabyden",
   "category": "engagement-ring",
   "karat": 14,
   "metalColor": "Yellow / White / Rose Gold",
   "price": 969.0,
   "compareAt": null,
   "priceBasis": "complete",
   "priceNote": "14K option $969.00; 10K $783.00; 18K $1,233.00. The $1,044 header compare-at belongs to the base variant, so compareAt is blank for the 14K row.",
   "priceSourceUrl": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
   "grams": 3.7,
   "gramsText": "3.70 g",
   "gramsNote": "Seller's description: 'Gold grams: 3.70 gr' — verified on the listing page this pass",
   "widthMm": null,
   "solidStated": true,
   "solidQuote": "Description: 'Material: Solid Gold (not gold plated or gold filled)' and 'Karat: 14 K (585)'",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns within 7 days after receipt; buyer pays return shipping; $20 delivery charge and 10% restocking fee; personalized, colored-enamel, letter and name-specific items excluded.",
   "returnUrl": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
   "returnsVerified": true,
   "evidenceId": "L21",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-02",
    "FL-16",
    "FL-17",
    "FL-14",
    "FL-18"
   ],
   "notes": [
    "Listing re-read this pass: $783.00+ (10K), 14K $969.00, 0.30 ct diamond + 0.90 ct ruby, 3.70 g gold, 585 stated.",
    "Return window is 7 days — shortest of the sellers reviewed.",
    "Ships from Albany, NY; production partner Vera Atolye, Istanbul, Türkiye.",
    "Listing photos include a chat screenshot with an address and a request to share contact details — flagged (FL-02).",
    "Current official-source read: L21 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "ET-1566052947",
   "name": "14K Solid Yellow Gold Domed Band, 2–8 mm (reference band)",
   "short": "Domed Band 2–8 mm",
   "sellerId": "etsy-vibrantstone",
   "category": "band",
   "karat": 14,
   "metalColor": "Yellow Gold",
   "price": 251.3,
   "compareAt": 359.0,
   "priceBasis": "from",
   "priceNote": "From $251.30 (2 mm, 30% off $359.00); 3 mm $363.30+, 4 mm $496.30+, 5 mm $643.30+, 6 mm $797.30+, 7 mm $944.30+, 8 mm $1,091.30–$1,742.30",
   "priceSourceUrl": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": true,
   "solidQuote": "Title: '14k Solid Yellow Gold Domed Wedding Band'",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns & exchanges accepted within 21 days; buyer pays return shipping. Customized bands may not be returnable; altered/used/damaged items may incur fees up to 30% or be ineligible; items exchanged once cannot then be returned.",
   "returnUrl": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
   "returnsVerified": true,
   "evidenceId": "L22",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-16",
    "FL-17",
    "FL-14"
   ],
   "notes": [
    "Listing re-read live: from $251.30; 14K solid yellow gold; 21-day return window and custom/fee exclusions confirmed; no gram weight published.",
    "Current official-source read: L22 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "ET-1433905613",
   "name": "14K Solid Gold 8 mm Polished Comfort-Fit Dome Band (reference band)",
   "short": "Comfort-Fit Dome Band 8 mm",
   "sellerId": "etsy-adelafinejewels",
   "category": "band",
   "karat": 14,
   "metalColor": "White Gold",
   "price": 999.7,
   "compareAt": null,
   "priceBasis": "from",
   "priceNote": "14K options $999.70–$1,368.90 by size (10K $674.70–$963.95); 35% off. The $1,038 header compare-at is for the 10K base variant, so compareAt is blank for 14K.",
   "priceSourceUrl": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": 8.0,
   "solidStated": true,
   "solidQuote": "Title: '14K Solid Gold 8mm White Gold Polished ... Wedding Band'",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns & exchanges accepted within 14 days; buyer pays return transportation; personalized products are non-refundable.",
   "returnUrl": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
   "returnsVerified": true,
   "evidenceId": "L23",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-16",
    "FL-17",
    "FL-14"
   ],
   "notes": [
    "Listing re-read live: 14K options $999.70–$1,368.90; 14-day return window and personalized-item exclusion confirmed; no gram weight published.",
    "A buyer-photo alt text on the page mentions an engraving '585 AFJ' — not a seller statement, so no hallmark or maker's mark is recorded.",
    "Current official-source read: L23 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "ET-944684759",
   "name": "14K White Gold Flat Polished Band, 2–6 mm (reference band)",
   "short": "Flat Polished Band 2–6 mm",
   "sellerId": "etsy-cittali",
   "category": "band",
   "karat": 14,
   "metalColor": "White Gold",
   "price": 195.75,
   "compareAt": 261.0,
   "priceBasis": "from",
   "priceNote": "Listing titled 14K White Gold displays from $195.75 (2 mm, 25% off $261.00); 3 mm $337.50+, 4 mm $369.00+, 5 mm $429.75+, 6 mm $524.25–$1,158.75. Description also lists other materials, so reconfirm the selected metal at checkout.",
   "priceSourceUrl": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
   "grams": null,
   "gramsText": null,
   "gramsNote": null,
   "widthMm": null,
   "solidStated": true,
   "solidQuote": "Description lists '10k, 14k, 18k Solid Gold' options for this design",
   "hallmarkStated": false,
   "hallmarkQuote": null,
   "makerMarkStated": false,
   "metalConflict": null,
   "returns": "Returns & exchanges accepted within 30 days; buyer pays return shipping; original condition required.",
   "returnUrl": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
   "returnsVerified": true,
   "evidenceId": "L24",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-03",
    "FL-16",
    "FL-17",
    "FL-14"
   ],
   "notes": [
    "Listing re-read live: from $195.75; 30-day return window confirmed; description lists multiple materials for the design, so selected metal must be reconfirmed at checkout.",
    "Current official-source read: L24 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": null
  },
  {
   "id": "ET-576343849",
   "name": "14K Solid White Gold Band, Size 11 — sold case study (exact weight unresolved)",
   "short": "Sold band — weight unresolved",
   "sellerId": "etsy-butterflywingvintage",
   "category": "case-study",
   "karat": 14,
   "metalColor": "White Gold",
   "price": 420.0,
   "compareAt": 525.0,
   "priceBasis": "complete",
   "priceNote": "$420.00 displayed on the sold-out detail page (original $525.00); this is a sold-listing case study, not a current offer",
   "priceSourceUrl": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
   "grams": null,
   "gramsText": "Not exact: title says 7 g; description says postal scale alternates between 6–7 g",
   "gramsNote": "No exact seller-stated weight; numeric grams and metal value intentionally blank",
   "widthMm": null,
   "solidStated": true,
   "solidQuote": "Title and description: 'Fine Solid 14K White Gold Wedding/Engagement Band'",
   "hallmarkStated": true,
   "hallmarkQuote": "Description: 'marked 14K with a maker's mark' and directs the buyer to the fourth photo",
   "makerMarkStated": true,
   "metalConflict": null,
   "returns": "n/a — item sold; seller FAQ says no refund for buyer's remorse or changed mind.",
   "returnUrl": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
   "returnsVerified": false,
   "evidenceId": "L25",
   "evidencePath": "verification/evidence/bc4e36a1/etsy.md",
   "url": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
   "sources": [],
   "checkedOn": "2026-10-23",
   "provenance": "live",
   "flags": [
    "FL-01",
    "FL-03",
    "FL-16",
    "FL-17",
    "FL-18",
    "FL-29"
   ],
   "notes": [
    "Sold-out detail page re-read live: $420.00 displayed, original $525.00; not a current offer.",
    "Exact weight and the old below-metal calculation are withdrawn: the title says 7 g but the description says the postal scale alternates between 6–7 g. No range is converted into an exact number (FL-01).",
    "The seller explicitly claims both a 14K stamp and a maker's mark; this remains a seller statement, not an independent assay.",
    "Current official-source read: L25 (corrected); evidence excerpt and URL are linked on the Verification page."
   ],
   "availability": "SOLD OUT — confirmed 2026-10-23"
  }
 ],
 "sellers": [
  {
   "id": "bluenile",
   "name": "Blue Nile",
   "type": "Retailer (online)",
   "website": "https://www.bluenile.com/",
   "contact": [
    "+1-800-242-2728",
    "service@bluenile.com"
   ],
   "contactUrl": "https://www.bluenile.com/contact-us",
   "returns": "30 days from shipment date, original unworn condition, full refund or exchange. NOT eligible: personalized jewelry, custom orders, engraved items, items resized after initial purchase, Diamond Upgrade Program purchases, clearance and Final Sale items. Two complimentary returns per customer per year; RMA required; $150 fee if a diamond grading report is not returned. One free resize (up or down two sizes) within 6 months if the design permits.",
   "returnsUrl": "https://www.bluenile.com/policies/returns",
   "returnsVerified": true,
   "warranty": "Limited lifetime warranty on gold/platinum items priced $1,000 or more (manufacturer defects); one free resize up or down two sizes within 6 months if the design permits; non-resizable styles excluded.",
   "warrantyUrl": "https://www.bluenile.com/services/warranty",
   "payment": "Credit card at checkout; Blue Nile credit card financing and Affirm-style monthly options are advertised.",
   "reputation": [
    {
     "source": "Better Business Bureau profile",
     "value": "A+ accredited; 121 complaints in the last 3 years; 22 in the last 12 months; BBB customer reviews average 1/5 (25 reviews)",
     "url": "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564",
     "method": "prior-session capture"
    },
    {
     "source": "ConsumerAffairs",
     "value": "1.7/5 from 172 reviews",
     "url": "https://www.consumeraffairs.com/retail/blue-nile.html",
     "method": "prior-session capture"
    }
   ],
   "flags": [
    "FL-04",
    "FL-05",
    "FL-06"
   ],
   "sources": [
    "https://www.bluenile.com/policies/returns",
    "https://www.bluenile.com/services/warranty",
    "https://www.bluenile.com/contact-us",
    "https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564",
    "https://www.consumeraffairs.com/retail/blue-nile.html"
   ],
   "notes": [
    "Return policy, contact details and warranty re-read this pass."
   ]
  },
  {
   "id": "brilliantearth",
   "name": "Brilliant Earth",
   "type": "Retailer (online + showrooms)",
   "website": "https://www.brilliantearth.com/",
   "contact": [
    "800.691.0952"
   ],
   "contactUrl": "https://www.brilliantearth.com/contact/",
   "returns": "Product pages state 'Free Shipping & Returns' and 'Free 1-Year Resizing'. Verified live at brilliantearth.com/30-Day-Returns/ on 2026-10-23: free returns/exchanges within 30 days of the item being available for shipment or pickup, unworn and in original condition. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. Phone return instructions and a free FedEx label are published.",
   "returnsUrl": "https://www.brilliantearth.com/30-Day-Returns/",
   "returnsVerified": true,
   "warranty": "Free lifetime manufacturing-defect warranty on fine jewelry; wear, gemstone loss, product loss and theft excluded. US/CAN/AUS/UK return labels are free; elsewhere a $50 deposit applies and is refunded for warrantied repairs. Unauthorized repair voids coverage.",
   "warrantyUrl": "https://www.brilliantearth.com/customer-service/warranty/#manufacturing_warranty",
   "payment": "Credit card; Affirm monthly payments (0% APR available), Wells Fargo 12-month financing and layaway are advertised.",
   "reputation": [
    {
     "source": "Product page reviews (Freesia 2mm)",
     "value": "4.8/5 from 80 reviews",
     "url": "https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
     "method": "prior-session capture (2026-10-22)"
    }
   ],
   "flags": [
    "FL-04"
   ],
   "sources": [
    "https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
    "https://www.brilliantearth.com/30-Day-Returns/"
   ],
   "notes": [
    "Return policy verified live 2026-10-23 at /30-Day-Returns/ (30-day window; exclusions published) — see FL-07 (resolved)."
   ]
  },
  {
   "id": "allurez",
   "name": "Allurez",
   "type": "Retailer (online, made in USA)",
   "website": "https://www.allurez.com/",
   "contact": [
    "1-800-554-3509",
    "service@allurez.com"
   ],
   "contactUrl": "https://www.allurez.com/pages/contact",
   "returns": "Return must ARRIVE at Allurez within 30 days of original shipment; unused, not resized or altered. Engraved items, custom-made orders, contoured wedding bands, clearance items, appraisals, gift cards and layaway deposits are non-refundable. Design Your Own rings may be exchanged only (same or higher value). Buyer pays return shipping; original shipping not refunded; $300 deduction per missing diamond certificate; refund within 7 business days.",
   "returnsUrl": "https://www.allurez.com/pages/return-policy",
   "returnsVerified": true,
   "warranty": "Complimentary 1-year limited manufacturing-defect warranty for qualifying US purchases after February 2024. Ring sizing is offered except full eternity rings. Missing stones may be replaced, but the new stone's cost is not covered. Wear, loss and unauthorized repair excluded; after one year repair fees plus a $39 shipping charge apply.",
   "warrantyUrl": "https://www.allurez.com/pages/warranty",
   "payment": "Credit card; Affirm, Klarna, Shop Pay Installments, Flex Pay and Allurez Layaway (10% down) advertised.",
   "reputation": [],
   "flags": [
    "FL-09",
    "FL-10"
   ],
   "sources": [
    "https://www.allurez.com/pages/return-policy",
    "https://www.allurez.com/pages/warranty",
    "https://www.allurez.com/products/filigree-designed-solitaire-engagement-ring-setting-14k-yellow-gold"
   ],
   "notes": [
    "Return policy and contact details re-read this pass."
   ]
  },
  {
   "id": "avianne",
   "name": "Avianne & Co",
   "type": "Retailer (NY showroom + online)",
   "website": "https://www.avianneandco.com/",
   "contact": [
    "1 (332)-244-4038",
    "28 W 47th Street, Diamond District, New York, NY"
   ],
   "contactUrl": "https://www.avianneandco.com/",
   "returns": "Returns of unworn and unaltered items accepted within 14 days. Full policy page not captured; resize/custom exclusions not confirmed.",
   "returnsUrl": "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw",
   "returnsVerified": false,
   "warranty": "Not stated on the product page.",
   "warrantyUrl": null,
   "payment": "Credit card; Affirm and Shop Pay installments advertised; promo code FALL10 for 10% off.",
   "reputation": [],
   "flags": [
    "FL-04",
    "FL-11"
   ],
   "sources": [
    "https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-ctw"
   ],
   "notes": [
    "Contact details and 14-day return notice re-read this pass."
   ]
  },
  {
   "id": "jewelrymaster",
   "name": "The Jewelry Master (Jewelry Masters)",
   "type": "Retailer (online)",
   "website": "https://www.thejewelrymaster.com/",
   "contact": [
    "1-888-59-JEWEL"
   ],
   "contactUrl": "https://www.thejewelrymaster.com/",
   "returns": "30-day 'Money Back Guarantee (some restrictions apply)' — return or exchange within 30 days, no questions asked; the restrictions themselves are not stated on the page.",
   "returnsUrl": "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html",
   "returnsVerified": false,
   "warranty": "Professional appraisal certificate included with purchase; no separate warranty stated.",
   "warrantyUrl": null,
   "payment": "Credit card; Affirm financing advertised.",
   "reputation": [],
   "flags": [
    "FL-04",
    "FL-12"
   ],
   "sources": [
    "https://www.thejewelrymaster.com/brilliant-round-diamond-solitaire-engagement-ring-14k-yellow-gold-149700.html"
   ],
   "notes": [
    "Return terms and contact number re-read this pass."
   ]
  },
  {
   "id": "solidgoldjewelers",
   "name": "Solid Gold Jewelers",
   "type": "Independent jeweler (online + store)",
   "website": "https://solidgoldjewelers.net/",
   "contact": [
    "(309) 452-1612"
   ],
   "contactUrl": "https://solidgoldjewelers.net/",
   "returns": "No return policy shown on the product page.",
   "returnsUrl": "https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
   "returnsVerified": false,
   "warranty": "Not stated.",
   "warrantyUrl": null,
   "payment": "Not stated; price is quoted by phone.",
   "reputation": [],
   "flags": [
    "FL-04",
    "FL-13"
   ],
   "sources": [
    "https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/"
   ],
   "notes": [
    "Product page re-read this pass; no price and no return terms published."
   ]
  },
  {
   "id": "etsy-rakshakjewels",
   "name": "RAKSHAKJEWELS (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/RAKSHAKJEWELS",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/RAKSHAKJEWELS",
   "returns": "Returns & exchanges accepted within 14 days; buyer pays return shipping; original condition required.",
   "returnsUrl": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
   "returnsVerified": true,
   "warranty": "Not stated on the listing.",
   "warrantyUrl": null,
   "payment": "Etsy checkout (cards, PayPal, Klarna); Etsy Purchase Protection applies to eligible orders.",
   "reputation": [
    {
     "source": "Etsy listing badge",
     "value": "Star Seller; 5/5 listing rating",
     "url": "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond",
     "method": "prior-session capture (2026-10-22)"
    }
   ],
   "flags": [
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/4426190660/250ct-yellow-radiant-moissanite-diamond"
   ],
   "notes": [
    "Listing re-read this pass."
   ]
  },
  {
   "id": "etsy-foreverforlove",
   "name": "ForeverForLove (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/ForeverForLove",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/ForeverForLove",
   "returns": "Returns & exchanges accepted within 30 days; buyer pays return shipping.",
   "returnsUrl": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
   "returnsVerified": true,
   "warranty": "Lifetime warranty on manufacturer defects per the listing description.",
   "warrantyUrl": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
   "payment": "Etsy checkout; Klarna advertised; Etsy Purchase Protection applies.",
   "reputation": [
    {
     "source": "Etsy listing badge",
     "value": "Star Seller; 5/5 listing rating",
     "url": "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown",
     "method": "prior-session capture"
    }
   ],
   "flags": [
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/4366425533/15-carat-e-vvs2-igi-certified-lab-grown"
   ],
   "notes": [
    "Listing and shop policy re-read live on 2026-10-23; see the linked current evidence check."
   ]
  },
  {
   "id": "etsy-verabyden",
   "name": "VeraByEden (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/VeraByEden",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/VeraByEden",
   "returns": "Returns within 7 days after receipt; buyer pays return shipping; $20 delivery charge and 10% restocking fee; personalized, colored-enamel, letter and name-specific items excluded.",
   "returnsUrl": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
   "returnsVerified": true,
   "warranty": "Not stated on the listing.",
   "warrantyUrl": null,
   "payment": "Etsy checkout; Klarna advertised; Etsy Purchase Protection applies.",
   "reputation": [
    {
     "source": "Etsy listing badge",
     "value": "Star Seller; 5/5 rating",
     "url": "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
     "method": "prior-session capture (2026-10-22)"
    }
   ],
   "flags": [
    "FL-02",
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant"
   ],
   "notes": [
    "Return window (7 days) and gold weight (3.70 g) re-read this pass."
   ]
  },
  {
   "id": "etsy-vibrantstone",
   "name": "VibrantStone (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/VibrantStone",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/VibrantStone",
   "returns": "Returns & exchanges accepted within 21 days; buyer pays return shipping (original shipping is advertised free). Customized/personalized returns may incur fees; altered, used or damaged items may incur up to 30% fees or be ineligible; an exchanged item cannot be returned.",
   "returnsUrl": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
   "returnsVerified": true,
   "warranty": "Not stated.",
   "warrantyUrl": null,
   "payment": "Etsy checkout; Etsy Purchase Protection applies.",
   "reputation": [
    {
     "source": "Etsy listing badge",
     "value": "Star Seller; 5/5 listing rating",
     "url": "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band",
     "method": "prior-session capture"
    }
   ],
   "flags": [
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/1566052947/14k-solid-yellow-gold-domed-wedding-band"
   ],
   "notes": [
    "Listing and shop policy re-read live on 2026-10-23; see the linked current evidence check."
   ]
  },
  {
   "id": "etsy-adelafinejewels",
   "name": "adelafinejewels (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/adelafinejewels",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/adelafinejewels",
   "returns": "Returns & exchanges accepted within 14 days; buyer pays return transportation (free US original shipping); personalized products are non-refundable.",
   "returnsUrl": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
   "returnsVerified": true,
   "warranty": "Not stated.",
   "warrantyUrl": null,
   "payment": "Etsy checkout; Etsy Purchase Protection applies.",
   "reputation": [
    {
     "source": "Etsy listing badge",
     "value": "Star Seller; 5/5 listing rating",
     "url": "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished",
     "method": "prior-session capture"
    }
   ],
   "flags": [
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/1433905613/14k-solid-gold-8mm-white-gold-polished"
   ],
   "notes": [
    "Listing and shop policy re-read live on 2026-10-23; see the linked current evidence check."
   ]
  },
  {
   "id": "etsy-cittali",
   "name": "CittaliFineJewelry (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/CittaliFineJewelry",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/CittaliFineJewelry",
   "returns": "Returns & exchanges accepted within 30 days; buyer pays return shipping.",
   "returnsUrl": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
   "returnsVerified": true,
   "warranty": "Not stated.",
   "warrantyUrl": null,
   "payment": "Etsy checkout; Klarna advertised; Etsy Purchase Protection applies.",
   "reputation": [
    {
     "source": "Etsy listing",
     "value": "4.9/5 item average",
     "url": "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished",
     "method": "prior-session capture"
    }
   ],
   "flags": [
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/944684759/14k-white-gold-band-flat-polished"
   ],
   "notes": [
    "Listing and shop policy re-read live on 2026-10-23; see the linked current evidence check."
   ]
  },
  {
   "id": "etsy-butterflywingvintage",
   "name": "BUTTERFLYWINGVINTAGE (Etsy shop)",
   "type": "Etsy shop",
   "website": "https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
   "contact": [
    "Contact via Etsy Messages"
   ],
   "contactUrl": "https://www.etsy.com/shop/BUTTERFLYWINGVINTAGE",
   "returns": "n/a — item sold; seller FAQ says no refund for buyer's remorse or changed mind.",
   "returnsUrl": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1",
   "returnsVerified": false,
   "warranty": "Not stated.",
   "warrantyUrl": null,
   "payment": "n/a — item sold.",
   "reputation": [
    {
     "source": "Etsy listing",
     "value": "5/5 with 802 shop reviews",
     "url": "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g",
     "method": "prior-session capture"
    }
   ],
   "flags": [
    "FL-04",
    "FL-16"
   ],
   "sources": [
    "https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-mens-ring-7g"
   ],
   "notes": [
    "Sold-out detail page and seller FAQ re-read live on 2026-10-23; the item is sold and not a current offer."
   ]
  }
 ],
 "flags": [
  {
   "id": "FL-01",
   "severity": "high",
   "status": "resolved",
   "title": "Resolved: the below-metal case study relied on an unsupported exact weight",
   "detail": "The sold Etsy listing's title says 7 g, but its description says a postal scale alternates between 6–7 g. The current sold-out detail page displays $420.00 (original $525.00), not a current offer. Exact grams, fine-gold weight, metal value and the former below-metal conclusion are therefore withdrawn. No range is converted into an exact number; ask for a calibrated weight and independent assay before drawing any conclusion.",
   "entryIds": [
    "ET-576343849"
   ]
  },
  {
   "id": "FL-02",
   "severity": "high",
   "status": "open",
   "title": "Listing photos solicit off-platform contact",
   "detail": "VeraByEden listing image 11 is a chat screenshot showing an address (2355 Westwood Boulevard #153, Los Angeles CA) and the text 'Share your contact information with us on Etsy Message.' Off-platform payment or contact can void Etsy Purchase Protection. Keep any purchase on Etsy and pay through Etsy checkout.",
   "entryIds": [
    "ET-1151446373"
   ]
  },
  {
   "id": "FL-03",
   "severity": "medium",
   "status": "open",
   "title": "Exact gram weight is not published for 18 of 25 rows",
   "detail": "Without an exact weight you cannot compute gold content or compare price with metal value. These cells are left blank — never estimated. The sold case study has only a 6–7 g scale range, so it is included here as well. Ask the seller in writing for the weight in grams before buying, then verify it on arrival.",
   "entryIds": [
    "BN-192506",
    "BN-195639",
    "BN-203257",
    "BN-195326",
    "BN-195871",
    "BN-311132",
    "BN-203738",
    "BN-203348",
    "BE-1343",
    "BE-NADIA",
    "BE-1343HH",
    "BE-SECRET",
    "ET-4426190660",
    "ET-4366425533",
    "ET-1566052947",
    "ET-1433905613",
    "ET-944684759",
    "ET-576343849"
   ]
  },
  {
   "id": "FL-04",
   "severity": "medium",
   "status": "open",
   "title": "Independent seller reputation not captured for most sellers",
   "detail": "Only Blue Nile has independent complaint data captured (BBB and ConsumerAffairs). Brilliant Earth shows on-site review scores; Allurez, Avianne, Jewelry Master, Solid Gold Jewelers and the Etsy shops have no independent complaint data in this dataset. Do the check yourself: search the business name plus 'complaint' or 'review', confirm a real phone/address, and look for a BBB profile.",
   "entryIds": []
  },
  {
   "id": "FL-05",
   "severity": "medium",
   "status": "open",
   "title": "Blue Nile: resized, engraved and custom rings are not returnable",
   "detail": "Blue Nile's 30-day money-back guarantee excludes personalized jewelry, custom orders, engraved items, items resized after purchase, Diamond Upgrade purchases, clearance and Final Sale. Returns are capped at two complimentary returns per customer per year, an RMA is required, and a missing diamond grading report costs $150. Do not resize before deciding to keep the ring.",
   "entryIds": [
    "BN-192506",
    "BN-195639",
    "BN-203257",
    "BN-195326",
    "BN-195871",
    "BN-311132",
    "BN-203738",
    "BN-203348"
   ]
  },
  {
   "id": "FL-06",
   "severity": "low",
   "status": "open",
   "title": "Blue Nile lifetime warranty starts at $1,000; some settings fall below it",
   "detail": "The limited lifetime warranty covers gold and platinum items with a purchase price of $1,000 or more. Of the Blue Nile settings recorded here, the $870 Classic Four Prong falls below that threshold (the $1,000 Petite Solitaire sits exactly at it), so it does not qualify for the lifetime warranty under the stated terms.",
   "entryIds": [
    "BN-203257",
    "BN-195639",
    "BN-192506",
    "BN-203348"
   ]
  },
  {
   "id": "FL-07",
   "severity": "medium",
   "status": "resolved",
   "title": "Resolved: Brilliant Earth return policy re-read and wording corrected",
   "detail": "Verified live 2026-10-23 at https://www.brilliantearth.com/30-Day-Returns/: free returns/exchanges run for 30 days from the item being available for shipment or pickup, with original/unworn condition required. Engraved rings may be returned with a $40 engraving-removal charge; personalized/custom and other published exclusions apply. All four Brilliant Earth entries link this working official policy.",
   "entryIds": [
    "BE-1343",
    "BE-NADIA",
    "BE-1343HH",
    "BE-SECRET"
   ]
  },
  {
   "id": "FL-08",
   "severity": "low",
   "status": "open",
   "title": "Two Brilliant Earth pages serve EUR; current USD price is blank",
   "detail": "On 2026-10-23 BE-1343 served €835 and BE-1343HH served €1,350, both Setting Only. Their USD price cells are blank — no conversion, no guess. BE-NADIA directly served $1,250 USD and BE-SECRET directly served $1,090 USD, so those two rows are not in this flag. Prior USD observations remain dated notes only.",
   "entryIds": [
    "BE-1343",
    "BE-1343HH"
   ]
  },
  {
   "id": "FL-09",
   "severity": "low",
   "status": "open",
   "title": "Allurez shows an 'Everyone Else' comparison price — not used",
   "detail": "Allurez pages display a '% Savings' figure against an 'Everyone Else' price ($2,497 / $1,373 / $1,194 on the three rings here). That comparison is the seller's own marketing claim and is not independently verified. Only the actual selling price is used in this project.",
   "entryIds": [
    "AL-5882",
    "AL-170",
    "AL-4426"
   ]
  },
  {
   "id": "FL-10",
   "severity": "medium",
   "status": "open",
   "title": "Allurez: Design Your Own rings are exchange-only",
   "detail": "Allurez's policy says Design Your Own engagement rings may be exchanged for items of the same or higher value but cannot be refunded. It does not say whether buying a setting on its own counts as 'Design Your Own'. Treat these settings as possibly exchange-only and confirm in writing before buying.",
   "entryIds": [
    "AL-5882",
    "AL-170",
    "AL-4426"
   ]
  },
  {
   "id": "FL-11",
   "severity": "low",
   "status": "open",
   "title": "Avianne: 14-day window, active promo code, full policy not captured",
   "detail": "The product page says returns of unworn and unaltered items are accepted within 14 days — shorter than the 30 days common elsewhere. The site also runs a 10% code (FALL10), which is not applied to the recorded price. The full return policy and resize exclusions were not captured.",
   "entryIds": [
    "AV-25893"
   ]
  },
  {
   "id": "FL-12",
   "severity": "low",
   "status": "open",
   "title": "Jewelry Master: 'Retail Price' is a seller comparison; guarantee restrictions unspecified",
   "detail": "The page shows a Retail Price of $6,041 against a Special Price of $3,020. The retail figure is the seller's own comparison and is not used in any analysis. The 30-day money-back guarantee says 'some restrictions apply' but does not list them.",
   "entryIds": [
    "JM-149700"
   ]
  },
  {
   "id": "FL-13",
   "severity": "medium",
   "status": "open",
   "title": "Solid Gold Jewelers: no price and no return policy published",
   "detail": "The product page states '14ky, 4.7g, #B02561' and asks buyers to call (309) 452-1612 for current pricing and availability. No price and no return policy appear on the page, so both are left blank. Get price, return terms and the hallmark in writing.",
   "entryIds": [
    "SGJ-B02561"
   ]
  },
  {
   "id": "FL-14",
   "severity": "medium",
   "status": "open",
   "title": "Maker's mark is not stated for 24 of 25 listings",
   "detail": "FTC guidance says to look near the karat mark for the name or U.S. registered trademark of the company behind it. The sold ET-576343849 description says 'marked 14K with a maker's mark' and points to a photo; that is a seller claim, not an independent assay. The other 24 listings do not state a maker's mark. Ask for close-up photos of both marks and verify them on arrival.",
   "entryIds": []
  },
  {
   "id": "FL-15",
   "severity": "medium",
   "status": "open",
   "title": "Listing does not explicitly say 'solid gold' (16 of 25)",
   "detail": "A karat mark alone does not say whether an item is solid or plated/hollow. FTC guidance defines 'solid gold' as not hollow. Brilliant Earth, Blue Nile and Allurez listings name the metal and karat but do not use the words 'solid gold'; Solid Gold Jewelers shows only '14ky'. These are left unflagged as solid and require written confirmation from the seller. The 9 Etsy/Avianne/Jewelry Master listings that do say solid are recorded with their exact wording.",
   "entryIds": [
    "BN-192506",
    "BN-195639",
    "BN-203257",
    "BN-195326",
    "BN-195871",
    "BN-311132",
    "BN-203738",
    "BN-203348",
    "BE-1343",
    "BE-NADIA",
    "BE-1343HH",
    "BE-SECRET",
    "AL-5882",
    "AL-170",
    "AL-4426",
    "SGJ-B02561"
   ]
  },
  {
   "id": "FL-16",
   "severity": "low",
   "status": "open",
   "title": "Etsy return windows vary by shop — one is only 7 days",
   "detail": "VeraByEden accepts returns within 7 days; RAKSHAKJEWELS and adelafinejewels state 14 days; VibrantStone states 21 days; ForeverForLove and Cittali state 30 days. Fees, personalization exclusions and the sold listing's no-remorse-refund statement still apply. Etsy Purchase Protection covers qualifying non-delivery, damage, late delivery and materially different items, not ordinary buyer's remorse. Check the specific shop policy before ordering.",
   "entryIds": [
    "ET-4426190660",
    "ET-4366425533",
    "ET-1151446373",
    "ET-1566052947",
    "ET-1433905613",
    "ET-944684759",
    "ET-576343849"
   ]
  },
  {
   "id": "FL-17",
   "severity": "low",
   "status": "open",
   "title": "Etsy prices are promo-dependent and vary by material, size and carat",
   "detail": "Etsy listings in this set showed discounts at check time and prices change by material (silver/10K/14K/18K), ring size, band width and center-stone carat. Where a header compare-at price belonged to another material or variant, compareAt is blank rather than borrowed. The recorded price is labeled by its actual option or listing basis on the check date. Re-check the live price before buying.",
   "entryIds": [
    "ET-4426190660",
    "ET-4366425533",
    "ET-1151446373",
    "ET-1566052947",
    "ET-1433905613",
    "ET-944684759",
    "ET-576343849"
   ]
  },
  {
   "id": "FL-18",
   "severity": "low",
   "status": "open",
   "title": "Gram weights are seller-stated, not independently verified",
   "detail": "Allurez publishes approximate gold weights; Avianne, Jewelry Master and Solid Gold Jewelers publish single figures; VeraByEden states 'Gold grams: 3.70 gr'. The sold ET-576343849 page gives only a 6–7 g scale range and is not assigned an exact weight. None has been independently weighed. Treat them as claims to be checked with a jeweler's scale and XRF on arrival.",
   "entryIds": [
    "AL-5882",
    "AL-170",
    "AL-4426",
    "AV-25893",
    "JM-149700",
    "SGJ-B02561",
    "ET-1151446373",
    "ET-576343849"
   ]
  },
  {
   "id": "FL-19",
   "severity": "info",
   "status": "open",
   "title": "Gold spot moves all day — the snapshot is dated",
   "detail": "The current 2026-10-23 Kitco panel shows $3,996.10/oz and $128.48/g, while nearby body text shows $3,995.50/oz and $128.46/g; earlier captures are retained as dated history. This site uses one labeled panel bid for every calculation and shows the timestamp. Spot at the moment you buy will differ; use the calculator with a fresh quote.",
   "entryIds": []
  },
  {
   "id": "FL-20",
   "severity": "info",
   "status": "open",
   "title": "A 14K or 18K stamp is not proof of purity",
   "detail": "FTC guidance requires a karat mark plus a maker's mark, but a stamp is a disclosure, not an assay. The only way to know what the metal actually is: have an independent jeweler test it (XRF or another professional method) after delivery, before wearing or resizing. No US law requires the seller to accept a return based on your test, so confirm the return right first.",
   "entryIds": []
  },
  {
   "id": "FL-21",
   "severity": "info",
   "status": "open",
   "title": "Setting prices exclude the center diamond",
   "detail": "Blue Nile and Brilliant Earth prices recorded here are 'Setting Price' / 'Setting Only'. The center stone is sold separately, so price-to-metal ratios are only computed for complete rings. Do not compare a setting with a complete ring as if they were the same purchase.",
   "entryIds": [
    "BN-192506",
    "BN-195639",
    "BN-203257",
    "BN-195326",
    "BN-195871",
    "BN-311132",
    "BN-203738",
    "BN-203348",
    "BE-1343",
    "BE-NADIA",
    "BE-1343HH",
    "BE-SECRET",
    "AL-5882",
    "AL-170",
    "AL-4426"
   ]
  },
  {
   "id": "FL-22",
   "severity": "low",
   "status": "open",
   "title": "Retailers excluded rather than guessed",
   "detail": "Walmart's search results render client-side and served no product cards or prices; two listings found by search (Pompeii3 and marquise-jewelers) were dead. No values were recorded for them. Exclusion is deliberate: blank beats invented.",
   "entryIds": []
  },
  {
   "id": "FL-23",
   "severity": "info",
   "status": "open",
   "title": "Earlier sessions' work is preserved in this repo",
   "detail": "Earlier sessions delivered to this repository. Their sites remain available: 638c9614 at /docs/, 090bae73 at /index-090bae73.html (+ /pages/), 37e8ff42's dashboard at /archive/session-37e8ff42/, 93032b31's 24-row dashboard at /archive/session-93032b31/, 84be683f at /verified/, 60c4b9c3 at /report/ (evidence in /verification/), and the /guide/ checklist site. This consolidated site merges their verified listings and flags; nothing was discarded.",
   "entryIds": []
  },
  {
   "id": "FL-24",
   "severity": "info",
   "status": "resolved",
   "title": "Resolved: karat-in-URL and grams-via-snippet flags",
   "detail": "Earlier flags said the Brilliant Earth karat appeared only in product URLs and that VeraByEden's 3.70 g came from a search snippet. Both were re-checked live: each Brilliant Earth product page states 14K Yellow Gold, and VeraByEden's description states 'Gold grams: 3.70 gr'. The old flags are closed, with the checks recorded on the Verification page.",
   "entryIds": [
    "BE-NADIA",
    "BE-1343HH",
    "BE-SECRET",
    "ET-1151446373"
   ]
  },
  {
   "id": "FL-25",
   "severity": "low",
   "status": "open",
   "title": "Kitco page shows several nearby numbers in one capture",
   "detail": "The 2026-10-23 capture displayed a panel bid of $3,996.10 and $128.48/g, an ask of $3,998.10, and separate body text of $3,995.50/oz and $128.46/g. The project uses the panel bid and its per-gram figure for every calculation, preserves the body figures as a labeled discrepancy, and never mixes quotes from different timestamps.",
   "entryIds": []
  },
  {
   "id": "FL-26",
   "severity": "medium",
   "status": "resolved",
   "title": "Resolved: all seven Etsy listing pages were read live on 2026-10-23",
   "detail": "An earlier collector returned HTTP 500 for the Etsy pages. This pass opened all seven official listing URLs directly and recorded field-level evidence in data/live_check_bc4e36a1.json (L19–L25). Current prices, stated options and available return terms replace the prior-session labels; the sold listing remains explicitly sold out.",
   "entryIds": [
    "ET-4426190660",
    "ET-4366425533",
    "ET-1151446373",
    "ET-1566052947",
    "ET-1433905613",
    "ET-944684759",
    "ET-576343849"
   ]
  },
  {
   "id": "FL-27",
   "severity": "medium",
   "status": "resolved",
   "title": "Resolved: all four Brilliant Earth pages were read live",
   "detail": "A previous collector saw navigation only. The 2026-10-23 direct reads are recorded in data/live_check_bc4e36a1.json (L09–L12): BE-1343 serves €835, BE-NADIA $1,250 USD, BE-1343HH €1,350, and BE-SECRET $1,090 USD. EUR is not converted; the two USD blanks are flagged FL-08.",
   "entryIds": [
    "BE-1343",
    "BE-NADIA",
    "BE-1343HH",
    "BE-SECRET"
   ]
  },
  {
   "id": "FL-28",
   "severity": "low",
   "status": "resolved",
   "title": "Resolved: both remaining Blue Nile pages were re-read",
   "detail": "The 2026-10-23 direct reads are recorded in data/live_check_bc4e36a1.json (L07–L08): BN-203738 displays $2,210 with an explicit 18K/14K metal conflict, and BN-203348 displays $1,145, 14K Yellow Gold, stock 502120y14 and 2.40 mm. Both rows carry the current check date.",
   "entryIds": [
    "BN-203738",
    "BN-203348"
   ]
  },
  {
   "id": "FL-29",
   "severity": "medium",
   "status": "open",
   "title": "ET-576343849 is sold out — not a current offer",
   "detail": "The 2026-10-23 sold-out detail page says 'Sorry, this item is sold out' / 'Sold' and displays $420.00 (original $525.00). It cannot be purchased; the price is a labeled sold-listing display only. Earlier $444.80/$556.00 observations remain historical archive material. The title's 7 g and the description's alternating 6–7 g scale range are not an exact weight, so no metal-value conclusion is drawn (FL-01 resolved).",
   "entryIds": [
    "ET-576343849"
   ]
  },
  {
   "id": "FL-30",
   "severity": "high",
   "status": "open",
   "title": "Blue Nile BN-203738 has an internal metal-description conflict",
   "detail": "The official page title and specification say 18K White Gold, while Product Details say 14K Yellow Gold. Both statements are preserved on the listing row; neither is silently selected as the truth. Confirm the exact metal, karat and return terms in writing before purchase. No gram weight is published, so no metal-value calculation is made for this row.",
   "entryIds": [
    "BN-203738"
   ]
  }
 ],
 "references": [
  {
   "id": "ftc-consumer",
   "title": "FTC Consumer Advice — Buying Platinum, Gold, and Silver Jewelry",
   "publisher": "U.S. Federal Trade Commission",
   "url": "https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry",
   "quote": "Near the karat quality mark, look for the name or the U.S. registered trademark of the company that will stand behind the mark... If you're thinking about buying a piece of gold jewelry but don't see a trademark along with the karat mark, don't buy it.",
   "usedFor": "Karat marks, maker's mark rule, solid vs plated/hollow definitions, returns in writing, where to report problems.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "cfr23",
   "title": "16 CFR Part 23 — Guides for the Jewelry, Precious Metals, and Pewter Industries",
   "publisher": "eCFR (Office of the Federal Register)",
   "url": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
   "quote": "§ 23.3 Misrepresentation as to gold content. § 23.10 Additional guidance for the use of quality marks.",
   "usedFor": "The regulation behind the FTC consumer guidance; gold-content and quality-mark rules. eCFR displayed 'up to date as of 10/21/2026' on the 2026-10-23 fetch.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "usc295",
   "title": "15 U.S.C. § 295 — Standard of fineness of gold articles; deviation",
   "publisher": "U.S. Code (GovInfo, U.S. Government Publishing Office)",
   "url": "https://www.govinfo.gov/link/uscode/15/295",
   "quote": "...the actual fineness of such gold or alloy shall not be less by more than three one-thousandth parts than the fineness indicated by the mark stamped, branded, engraved, or printed upon any part of such article... and ... shall not be less by more than seven one-thousandth parts, in the case of any other such article...",
   "usedFor": "The statutory assay tolerance an XRF reading is compared against: 3/1000 solder-free, 7/1000 for the whole article including solder.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "cfr23-3",
   "title": "16 CFR § 23.3 — Misrepresentation as to gold content (Cornell LII mirror)",
   "publisher": "Cornell Legal Information Institute",
   "url": "https://www.law.cornell.edu/cfr/text/16/23.3",
   "quote": "Text of the gold-content misrepresentation rule.",
   "usedFor": "Readable mirror of § 23.3.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "usc297",
   "title": "15 U.S.C. § 297 — Stamping plated articles; identifying trademark",
   "publisher": "U.S. Code (Cornell LII)",
   "url": "https://www.law.cornell.edu/uscode/text/15/297",
   "quote": "...shall apply or cause to be applied to that article a trademark... in a position as close as possible to that quality mark or stamp.",
   "usedFor": "Statutory basis for a maker's mark next to the quality mark (National Stamping Act).",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "nist-troy",
   "title": "NIST SP 811, Appendix B.8 — Factors for units listed alphabetically",
   "publisher": "National Institute of Standards and Technology",
   "url": "https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8",
   "quote": "NIST Appendix B.8 displays ounce (troy or apothecary) → gram as 3.110348 E+01 (rounded). Kitco separately states the more precise constant: 'A troy ounce is 31.1034768 grams.'",
   "usedFor": "Troy-ounce conversion disclosure. Calculations retain Kitco's stated 31.1034768 g/ozt constant; NIST's displayed factor is rounded.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; evidence R06)"
  },
  {
   "id": "lbma",
   "title": "LBMA Precious Metal Prices — benchmark administration",
   "publisher": "London Bullion Market Association",
   "url": "https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices",
   "quote": "The LBMA Gold Price is set twice daily in auctions independently operated and administered by ICE Benchmark Administration Limited (IBA) and commencing at 10:30 and 15:00 London time.",
   "usedFor": "Why a timestamped benchmark matters; the London benchmark is set twice daily, while retail spot pages update continuously.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "ftc-credit",
   "title": "FTC Consumer Advice — Using Credit Cards and Disputing Charges",
   "publisher": "U.S. Federal Trade Commission",
   "url": "https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges",
   "quote": "Federal law says you have the right to get mistakes fixed promptly... If you have a complaint about the quality of something you bought...",
   "usedFor": "Why a credit card is safer than an irreversible payment method, and how billing disputes work.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "etsy-pp",
   "title": "Etsy Purchase Protection Program",
   "publisher": "Etsy",
   "url": "https://help.etsy.com/hc/en-us/articles/7471925990807-Etsy-s-Purchase-Protection-Program",
   "quote": "Full refund for eligible orders that don't arrive, arrive damaged, arrive 7+ days after the estimated delivery window, or differ significantly from the description.",
   "usedFor": "Marketplace protection limits (not buyer's remorse).",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "jvc",
   "title": "Jewelers Vigilance Committee — mediation services",
   "publisher": "Jewelers Vigilance Committee",
   "url": "https://jvclegal.org/mediation-services/",
   "quote": "Dispute mediation between buyers and jewelers (linked from the FTC article).",
   "usedFor": "Where to escalate a jewelry dispute.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  },
  {
   "id": "reportfraud",
   "title": "FTC — ReportFraud.ftc.gov",
   "publisher": "U.S. Federal Trade Commission",
   "url": "https://reportfraud.ftc.gov/",
   "quote": "Report fraud, scams and bad business practices.",
   "usedFor": "Reporting a seller.",
   "checkedOn": "2026-10-23",
   "method": "live re-read 2026-10-23 (session bc4e36a1; official reference ledger)"
  }
 ]
};
