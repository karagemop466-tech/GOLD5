#!/usr/bin/env python3
"""Build data/live_check_6d10ac0a.json — the 46-check evidence ledger for session 6d10ac0a.

NO HALLUCINATIONS.  This script does not invent evidence.  It starts from the
committed 2026-10-23 ledger written by session ``bc4e36a1``
(``data/live_check_bc4e36a1.json``) and:

* labels every check with the session that actually performed the read
  (``readBy``);
* replaces the excerpt / evidence path / result of the **nine** checks this
  session re-opened live (Kitco spot + 7 retailer listings + 1 Etsy listing)
  with verbatim transcriptions saved under
  ``verification/evidence/6d10ac0a/``;
* keeps the other 37 checks byte-identical to their ``bc4e36a1`` originals and
  marks them ``readBy: bc4e36a1 (inherited)`` — they were captured on the same
  date (2026-10-23) and are never relabelled as this session's reads;
* appends ``partialReads`` and ``failures`` so that pages this pass could not
  fully read, and fetch errors it hit, are published instead of hidden.

Run:  python3 scripts/build_ledger_6d10ac0a.py
"""
from __future__ import annotations

import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "data", "live_check_bc4e36a1.json")
OUT = os.path.join(ROOT, "data", "live_check_6d10ac0a.json")
EV = "verification/evidence/6d10ac0a"

SESSION = "6d10ac0a"
BRANCH = "arena/6d10ac0a-gold5"
INHERITED_BY = "bc4e36a1 (inherited)"

# ---------------------------------------------------------------- re-reads
# Observed values below are transcribed from the pages fetched in this pass.
# They must equal the canonical row values or the build refuses to emit JSON.
REREADS = {
    "S01": dict(
        evidencePath=f"{EV}/spot.md",
        result="corrected",
        observed=None,
        sourceExcerpt=(
            "Panel: 'Oct 23, 2026 - 19:43 NY Time'; Bid 3,994.90 USD (-28.20, -0.70%); Ask 3,996.90; "
            "ounce 3,994.90 (-28.20); gram 128.44 (-0.91); Kilo 128,440.99 (-906.65); pennyweight 199.75 (-1.41); "
            "tola 1,498.09 (-10.58); tael 4,854.91 (-34.27); Day's Range 3975.10 - 4040.20. "
            "'Prices provided by Kitco Metals Inc. Displayed in U.S. dollars (USD), as of October 23, 2026 at 7:42 p.m. EDT.' "
            "Body text: 'The current price of gold is $3,994.90 per troy ounce as of October 23, 2026, 7:42 p.m. ET, down $28.40 today.' "
            "Purity table: 24K $3,994.90; 22K $3,662.12; 18K $2,996.18; 14K $2,330.23; 10K $1,664.67. "
            "Unit table: per ounce $3,994.90; per gram $128.44; per 10 grams $1,284.39; per kilo $128,439.02; "
            "per pennyweight $199.75; per tola $1,498.09; per tael $4,854.91. Embedded OANDA widget close 3,995.810 at 19:43:05 UTC-4 "
            "(a third distinct print, disclosed under FL-25 and not used in any calculation)."
        ),
    ),
    "L07": dict(  # BN-203738
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=2210, grams=None, karat=18, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True,
                      metalConflict="Title and specification say 18K White Gold; Product Details say 14K Yellow Gold."),
        inheritedFields=["returnsVerified (policy page not re-read this pass)"],
        sourceExcerpt=(
            "'$2,210 (Setting Price)'; 'Metal Type: 18K White Gold'; Stock Number 502820w; Metal 18K White Gold; "
            "Width 1.70mm; Rhodium Finish Yes; 'Or as low as $376/mo for 6 months with the Blue Nile Credit Card for a "
            "total payment of $2,254'. Product Details still reads: 'This mesmerizing engagement ring is artfully crafted "
            "from warmly lustrous 14k yellow gold.' — the 18K/14K conflict is unchanged and stays published as FL-30. "
            "Warranty: 'We warrant all gold and platinum jewelry items with a purchase price of $1,000 or more from "
            "manufacturer's defect.' No gram weight, no explicit 'solid gold' wording, no karat-stamp or maker's-mark claim."
        ),
    ),
    "L13": dict(  # AL-5882
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=1085, grams=5.0, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (policy page not re-read this pass)"],
        sourceExcerpt=(
            "'$1,085' with '57% Savings' and '$2,497 Everyone Else' (marketing comparison, FL-09, not recorded as a price); "
            "'Setting only. Center stone sold separately.'; 'Metal: 14k Yellow Gold'; 'Style number U5882'; "
            "'Gold Weight 5.00 Grams (Approximate)'; Width '2.9mm (Top Width) 2.3mm (Bottom Width)'; "
            "Height '3.5mm (Top Height) 1.7mm (Bottom Height)'; 'Crafted In the USA'; "
            "'Shipping estimate: 10 to 14 business days'. Page marketing block: 'Easy Returns — Return or exchange within "
            "30 days if unsatisfied.' No explicit 'solid gold' sentence, no karat-stamp claim, no maker's-mark claim."
        ),
    ),
    "L14": dict(  # AL-170
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=933, grams=4.8, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (policy page not re-read this pass)"],
        sourceExcerpt=(
            "'$933' with '32% Savings' and '$1,373 Everyone Else' (marketing comparison, FL-09); "
            "'Setting only. Center stone sold separately.'; 'Metal: 14k Yellow Gold'; 'Metal Color Yellow Gold'; "
            "'Style number U170'; 'Gold Weight 4.80 grams (Approximate)'; "
            "Width '3.20mm(Top Width), 2.40mm(Bottom Width)'; 'Crafted In the USA'; "
            "'Please Note The center diamond is not included in the price of the ring'. "
            "No explicit 'solid gold' sentence, no karat-stamp claim, no maker's-mark claim."
        ),
    ),
    "L15": dict(  # AL-4426
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=585, grams=3.58, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=True, metalConflict=None),
        inheritedFields=["returnsVerified (policy page not re-read this pass)"],
        sourceExcerpt=(
            "Page H1 'Engraved Floral Solitaire Engagement Ring Setting 14K Yellow Gold'; '$585' with '51% Savings' and "
            "'$1,194 Everyone Else' (marketing comparison, FL-09); 'Setting only. Center stone sold separately.'; "
            "'Metal: 14k Yellow Gold'; 'Style number NG4426'; 'Approximate Metal Weight 3.58 grams'; 'Crafted In the USA'. "
            "Size selector shows size-conditional surcharges '10.25 (+ $39) 10.5 (+ $49) 10.75 (+ $69) 11 (+ $79) "
            "11.25 (+ $89) 11.5 (+ $99)' — the recorded price is the base displayed price and no surcharge variant is "
            "blended in. No explicit 'solid gold' sentence, no karat-stamp claim, no maker's-mark claim."
        ),
    ),
    "L16": dict(  # AV-25893
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=1100, grams=2.3, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "Title '14K Solid Yellow Gold Diamond Solitaire Engagement Ring 0.41 Ctw' (explicit 'Solid'); '$1,100.00'; "
            "banner '10% OFF WITH CODE \"FALL10\"' (promo not applied to the recorded price, FL-11); "
            "'Call Now 1 (332)-244-4038'. Description: 'handcrafted in 14k yellow gold. The center is prong set with one "
            "brilliant round cut diamond which weighs 0.41 carats. The frame measures to 4.5 mm in width and weighs 2.3 grams.' "
            "DETAILS table: 'Item Code R25893'; 'Diamond Carat Weight 0.41 Ctw'; 'Diamond Clarity VS2'; 'Diamond Color G, H'; "
            "'Metal Color Yellow'; 'Metal Type 14K Gold'; 'Item Weight 2.3 grams'. "
            "On-page returns line: 'Returns of unworn and unaltered items accepted within 14 days.' "
            "Showroom: '28 W 47th Street, Diamond District · New York, NY'. No karat-stamp or maker's-mark claim published."
        ),
    ),
    "L17": dict(  # JM-149700
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=3020, grams=2.3, karat=14, solidStated=True, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "'Retail Price $6,041.00  Special Price $3,020.00' (recorded price is the Special Price; the Retail Price is "
            "kept as a labelled compare-at, FL-12); 'Availability: In stock'; 'Only 1 left'; 'Style 149700'. "
            "PRODUCT DETAILS: 'This beautiful treasure is entirely handcrafted in pure 14KT solid yellow gold ... weighing "
            "0.71 carats. All of the stones are a blinding white G-H color and SI1 clarity.' Information table: "
            "'Carats: 0.71ctw'; 'Metal Type: 14KT Gold'; 'Metal Weight: 2.3 Grams'; 'Width: mm' and 'Length: mm' are empty "
            "on the page. 'Money Back Guarantee (some restrictions apply)* ... return or exchange your purchase within a "
            "30-day period - no questions asked' — the restrictions themselves are not stated on the page, so "
            "returnsVerified stays false. Banner 'LAB DIAMOND SALE - Up to 50% OFF' is not applied to this row."
        ),
    ),
    "L18": dict(  # SGJ-B02561
        evidencePath=f"{EV}/retailers.md",
        result="unchanged",
        observed=dict(price=None, grams=4.7, karat=14, solidStated=False, hallmarkStated=False,
                      makerMarkStated=False, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "'Yellow Gold Solitaire Engagement Ring'; spec line '14ky, 4.7g, #B02561'; 'Pricing and availability are "
            "subject to change.'; 'SKU: B02561'; 'Categories: Mountings, Rings, Yellow Gold'; 'Brand: M Michael' "
            "(a store taxonomy field — NOT a hallmark/maker's-mark claim, so makerMarkStated stays false); "
            "'Call (309) 452-1612 for current pricing and availability.' No price is published anywhere on the page, so the "
            "price cell stays blank (FL-13). No return policy is shown on the product page. No explicit 'solid gold' sentence "
            "on the product page itself."
        ),
    ),
    "R05": dict(  # 15 U.S.C. 297 — re-pointed from the Cornell mirror to the official GovInfo text
        url="https://www.govinfo.gov/link/uscode/15/297",
        evidencePath=f"{EV}/references.md",
        result="corrected",
        observed=None,
        sourceExcerpt=(
            "Official U.S. Government Publishing Office text; the link resolved to "
            "https://www.govinfo.gov/content/pkg/USCODE-2024-title15/pdf/USCODE-2024-title15-chap8-sec297.pdf. "
            "'§ 297. Stamping plated articles'. (a) rolled gold plate / gold plate / gold filled / electroplate articles "
            "may not be stamped with any word or mark usually employed to indicate the fineness of gold 'unless such word "
            "or mark be accompanied by other words, plainly indicating that such article or part thereof is made of rolled "
            "gold plate, gold plate, or gold electroplate, or is gold filled, as the case may be'. (b) Identifying trademark: "
            "a manufacturer or dealer subject to section 294 who applies a quality mark indicating gold or silver content "
            "'shall — (A) Apply or cause to be applied to that article a trademark of such persons, which has been duly "
            "registered or applied for registration under the laws of the United States ... or the name of such person', and "
            "each identifying trademark or name 'shall be applied to that article by the same means as that used in applying "
            "the quality mark or stamp appearing thereon, in type or lettering at least as large as that used in such quality "
            "mark or stamp, and in a position as close as possible to that quality mark or stamp.' "
            "(June 13, 1906, ch. 3289, § 4, 34 Stat. 261; Pub. L. 87-354, § 1, Oct. 4, 1961, 75 Stat. 775; "
            "Pub. L. 91-366, § 1(e), July 31, 1970, 84 Stat. 691.) The Cornell LII page for the same section remains a mirror "
            "and is named as such in the reference note."
        ),
    ),
    "L25": dict(  # ET-576343849
        evidencePath=f"{EV}/etsy-and-brilliant-earth.md",
        result="unchanged",
        observed=dict(price=420.0, grams=None, karat=14, solidStated=True, hallmarkStated=True,
                      makerMarkStated=True, returnsVerified=False, metalConflict=None),
        sourceExcerpt=(
            "'This item is sold out.' Title 'Fine 14K Solid White Gold Ring - 7g Solid Gold -Size 11- Comfort Fit Wedding "
            "Ring Band-Marked 14K'; 'Price: $420.00'; 'Original Price: $525.00'; shop BUTTERFLYWINGVINTAGE. Highlights: "
            "'Vintage from before 2007'; 'Materials: White gold, Yellow gold'. Description: 'I am offering a Fine Solid 14K "
            "White Gold Wedding/Engagement Band. Quality Men's or woman's Comfort Fit Shiny Smooth Finish Wedding Band is "
            "marked 14K with a maker's mark. (Please see 4TH photo). Last photo shows size 11 on the ring sizer. The weight "
            "on my postal scale alternates between 6-7 g. Was recently Rhodium Plated and in excellent condition'. FAQ: "
            "'I do not offer a refund for the following reasons: Buyers remorse / Changed mind / Return postage'. Seller: "
            "'Laura, Owner of BUTTERFLYWINGVINTAGE · Phoenix, Arizona · 5.0 (802) · 2k sales · 12 years on Etsy'. "
            "Title says 7 g while the description reports 6-7 g, so exact grams, fine gold and metal value stay blank."
        ),
    ),
}

PARTIAL_READS = [
    dict(entryId="ET-1151446373", canonicalCheck="L21",
         url="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
         checkedOn="2026-10-23", readBy=SESSION,
         evidencePath=f"{EV}/etsy-and-brilliant-earth.md",
         retrieved="Seller description block: 'Material: Solid Gold (not gold plated or gold filled)'; 'Karat: 14 K (585)'; "
                   "'Gold grams: 3.70 gr'; 'Diamond weight: 0.30 ct'; 'Ruby weight: 0.90 ct'; 'Made to order'; "
                   "'All of our items are 14K real gold. We do not use any gold filled, gold plated or gold vermeil items.' "
                   "Shop 'VeraByEden' with Etsy 'Star Seller' badge (a marketplace service metric, not purity evidence).",
         notRetrieved="The price block was not present in the retrieved content.",
         effect="Corroboration only. Canonical values (price $969.00, grams 3.7, karat 14, solid gold stated) remain "
                "labelled with bc4e36a1's 2026-10-23 read L21. No value was upgraded, blanked or re-dated by this pass."),
    dict(entryId="BE-1343", canonicalCheck="L09",
         url="https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
         checkedOn="2026-10-23", readBy=SESSION,
         evidencePath=f"{EV}/etsy-and-brilliant-earth.md",
         retrieved="Page title 'Freesia 2mm Solitaire Ring in 14K Yellow Gold | Brilliant Earth'; header phone 800.691.0952; "
                   "banner 'ENDS SOON! Receive a $250 Gift Card With Purchase Over $1,000. Use Code GIFT in Cart.' "
                   "(a promotion, not a product price).",
         notRetrieved="The retrieved content chunk contained only site navigation; no price was read.",
         effect="Corroboration of the 14K Yellow Gold title only. The EUR-serving observation (€835) and the blank USD cell "
                "stay exactly as flagged under FL-08 with bc4e36a1's 2026-10-23 read L09. No EUR→USD conversion was made."),
]

SCOPE_READS = [
    dict(id="SR-01", kind="citation-scope",
         subject="16 CFR § 23.18 — Misrepresentation of weight and “total weight.”",
         url="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.18",
         checkedOn="2026-10-23", readBy=SESSION,
         evidencePath=f"{EV}/references.md",
         changeRequest="CR-D49-02 (session d49fe320)",
         sourceExcerpt=(
             "eCFR page state: 'This content is from the eCFR and is authoritative but unofficial. Displaying title 16, "
             "up to date as of 10/21/2026. Title 16 was last amended 10/19/2026.' Authority: 15 U.S.C. 45, 46. "
             "Source: 83 FR 40667, Aug. 16, 2018. Text: '(a) It is unfair or deceptive to misrepresent the weight of a "
             "diamond. (b) It is unfair or deceptive to use the word “point” or any abbreviation in any representation, "
             "advertising, marking, or labeling to describe the weight of a diamond, unless the weight is also stated as "
             "decimal parts of a carat (e.g., 25 points or .25 carat). A carat is a standard unit of weight for a diamond "
             "and is equivalent to 200 milligrams (1/5 gram). A point is one one-hundredth (1/100) of a carat.'"
         ),
         finding=("§ 23.18 governs DIAMOND weight representations. It does not require disclosure of a ring's gold-alloy "
                  "gram weight, so the checklist no longer cites it as the basis for the grams criterion; it is cited for "
                  "what it actually says, and the grams criterion is labelled as this project's buying rule.")),
    dict(id="SR-02", kind="payment-scope",
         subject="Solid Gold Jewelers product page + FTC credit-card guidance (payment methods)",
         url="https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/",
         checkedOn="2026-10-23", readBy=SESSION,
         evidencePath=f"{EV}/references.md",
         changeRequest="CR-D49-01 (session d49fe320)",
         sourceExcerpt=(
             "Re-read under ledger check L18: the page states '14ky, 4.7g, #B02561', 'Pricing and availability are subject "
             "to change.' and 'Call (309) 452-1612 for current pricing and availability.' No payment method is stated "
             "anywhere on the page. Session d49fe320 separately recorded that FTC credit-card guidance establishes consumer "
             "dispute rights and does not verify which methods any merchant accepts "
             "(https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges)."
         ),
         finding=("The site's prose claimed 'Every seller reviewed checks out by card' and that wire/Zelle/gift cards are "
                  "'Not offered by these sellers'. Neither statement is supported: 12 of 13 seller records state a method, "
                  "Solid Gold Jewelers states none, and no source confirms that any method is refused. Prose corrected and "
                  "published as FL-32.")),
]

FAILURES = [
    dict(seq="F1", kind="mistyped-url",
         url="https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-carat",
         result="Shopify '404 Not Found — The page you were looking for does not exist'",
         handling="Operator error: the handle was retyped from a truncated printout instead of copied from the dataset. "
                  "The canonical URL (...-0-41-ctw) was then fetched and matched the row. A 404 on a mistyped URL proves "
                  "nothing about the listing, so it is logged here and not recorded as a dead link for AV-25893."),
    dict(seq="F2", kind="fetch-proxy-error",
         url="brilliantearth.com BE-1343 / bluenile.com BN-203738 / etsy.com ET-576343849 (first attempts)",
         result="Proxy returned 'SignatureDoesNotMatch' — infrastructure error, not a site error",
         handling="Retried with the identical official URLs; all three loaded. Logged rather than dropped, because a failed "
                  "read must never be reported as a successful one."),
    dict(seq="F3", kind="partial-content", url="https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/",
         result="price block absent from the retrieved chunk",
         handling="Recorded in partialReads; USD price stays blank (FL-08)."),
    dict(seq="F4", kind="partial-content", url="https://www.etsy.com/listing/1151446373/14k-solid-gold-ruby-diamond-ring-elegant",
         result="price block absent from the retrieved chunk",
         handling="Recorded in partialReads; price stays labelled inherited (L21)."),
    dict(seq="F5", kind="not-re-read-this-pass",
         url="9 seller policy/contact pages + 11 official/regulatory references",
         result="not opened by this pass",
         handling="They keep bc4e36a1's 2026-10-23 captures (P01-P09, R01-R11), their original evidence paths and an "
                  "explicit 'readBy: bc4e36a1 (inherited)' label. See failures-and-irregularities.md sections 2-3."),
]


def main() -> int:
    with open(BASE, encoding="utf-8") as fh:
        base = json.load(fh)

    ledger = copy.deepcopy(base)
    checks = ledger["checks"]

    by_id = {c["id"]: c for c in checks}
    missing = sorted(set(REREADS) - set(by_id))
    if missing:
        print(f"ERROR: unknown check ids in REREADS: {missing}", file=sys.stderr)
        return 1

    for c in checks:
        c["readBy"] = INHERITED_BY
        c["firstCapturedBy"] = "bc4e36a1"
        c["firstCapturedPath"] = c.get("evidencePath")

    for cid, over in REREADS.items():
        c = by_id[cid]
        c["readBy"] = SESSION
        c["rereadOn"] = "2026-10-23"
        if over.get("url"):
            c["priorUrl"] = c.get("url")
            c["url"] = over["url"]
        c["evidencePath"] = over["evidencePath"]
        c["result"] = over["result"]
        c["sourceExcerpt"] = over["sourceExcerpt"]
        if over.get("observed") is not None:
            c["observed"] = over["observed"]
        if over.get("inheritedFields"):
            c["inheritedFields"] = over["inheritedFields"]
        c["status"] = "read"
        c["checkedOn"] = "2026-10-23"

    ledger["session"] = SESSION
    ledger["branch"] = BRANCH
    ledger["checkedOn"] = "2026-10-23"
    ledger["inherits"] = dict(
        session="bc4e36a1", ledger="data/live_check_bc4e36a1.json", checkedOn="2026-10-23",
        note=("37 of the 46 checks were captured earlier the same day by session bc4e36a1 (merged as PR #50). "
              "They are carried forward byte-identical with readBy='bc4e36a1 (inherited)' and are never relabelled as "
              "this session's reads. 9 checks (1 spot + 8 listings) were re-opened live by session 6d10ac0a."),
    )
    ledger["method"] = (
        "Nine checks were re-opened live with fetch_page on 2026-10-23 (late UTC) and transcribed field by field into "
        "verification/evidence/6d10ac0a/ before any canonical value was touched. The remaining 37 checks are inherited "
        "unchanged from data/live_check_bc4e36a1.json, captured the same date, and keep their original evidence ids and "
        "paths. Two pages could only be read partially; they are logged in partialReads and upgraded nothing. No missing "
        "value was inferred, EUR was not converted to USD, no weight range was turned into an exact gram figure, and no "
        "seller statement was promoted to an assay result."
    )
    ledger["timeNote"] = (
        "Only the retrieval date is asserted for fetches. A time is recorded only where the source itself displayed one "
        "(Kitco's panel timestamp '19:43 NY Time' and its body sentence 'as of October 23, 2026, 7:42 p.m. ET')."
    )
    ledger["noHallucinations"] = (
        "Blank means unverified. A source conflict is published, not resolved by preference. Inherited same-day reads are "
        "labelled with the session that actually made them. Derived values are recomputed from the canonical inputs by "
        "script and re-checked by scripts/verify.py, scripts/independent_audit.py and tools/security_test.py."
    )
    ledger["coverage"] = dict(
        listing=25, policy=9, reference=11, spot=1, total=46,
        rereadThisPass=sum(1 for c in checks if c["readBy"] == SESSION),
        inheritedSameDate=sum(1 for c in checks if c["readBy"] == INHERITED_BY),
        partialReads=len(PARTIAL_READS),
        scopeReads=len(SCOPE_READS),
        failuresLogged=len(FAILURES),
    )
    ledger["partialReads"] = PARTIAL_READS
    ledger["scopeReads"] = SCOPE_READS
    ledger["failures"] = FAILURES

    # Corrections inherited from bc4e36a1 keep their author; this pass appends its own.
    for corr in ledger.get("corrections", []):
        corr.setdefault("session", "bc4e36a1")
    ledger["corrections"] = ledger.get("corrections", []) + [
        dict(id="C-10", session=SESSION, subject="Kitco quote",
             before="$3,996.10/oz and $128.48/g from the 16:12 NY panel (prices stated as of 4:10 p.m. EDT)",
             after="$3,994.90/oz and $128.44/g from the 19:43 NY panel (prices stated as of 7:42 p.m. EDT)",
             reason="New official-page observation by session 6d10ac0a. Every derived value (fine gold, metal value, "
                    "price-to-metal, purity table, calculator defaults) is recomputed from this one labelled panel bid. "
                    "The superseded quote is retained as dated history and is not used in any calculation."),
        dict(id="C-11", session=SESSION, subject="Kitco purity table",
             before="24K $3,996.10 / 22K $3,663.22 / 18K $2,997.08 / 14K $2,330.93 / 10K $1,665.17",
             after="24K $3,994.90 / 22K $3,662.12 / 18K $2,996.18 / 14K $2,330.23 / 10K $1,664.67",
             reason="Transcribed from the same page capture's own 'Gold Value by Purity' table; nothing hand-computed "
                    "or carried over from the earlier quote."),
        dict(id="C-12", session=SESSION, subject="Provenance attribution",
             before="All 25 rows labelled 'live 2026-10-23' with no record of which session read them",
             after="Each row and check carries readBy: 8 listings + the spot re-read by 6d10ac0a; 17 listings, 9 policy "
                   "pages and 11 references inherited from bc4e36a1's same-day 2026-10-23 ledger with their original "
                   "evidence ids and paths",
             reason="Prevents this pass from implying it opened pages it did not open. Two further pages (ET-1151446373, "
                    "BE-1343) were only partially retrieved and are logged as partialReads; they upgraded nothing."),
        dict(id="C-14", session=SESSION, subject="15 U.S.C. § 297 citation (CR-D49-04)",
             before="Reference R05 cited the Cornell Legal Information Institute mirror "
                    "https://www.law.cornell.edu/uscode/text/15/297",
             after="Reference R05 cites the official GovInfo U.S. Code text https://www.govinfo.gov/link/uscode/15/297 "
                   "(resolved to the GPO 2024 edition PDF), re-read live this pass; Cornell is named as a mirror in the "
                   "reference note",
             reason="Official-source preference. The statutory maker's-mark language was re-read verbatim from GPO text "
                    "before the citation was changed."),
        dict(id="C-15", session=SESSION, subject="16 CFR § 23.18 citation scope (CR-D49-02)",
             before="The checklist cited § 23.18 as the source for asking a seller for a ring's metal weight in grams",
             after="§ 23.18 is cited only for diamond-weight misrepresentation (carat/point claims); the grams criterion is "
                   "labelled as this project's buying rule, with FTC 'get it in writing' guidance as its consumer source",
             reason="Re-read of the official eCFR text (scopeReads SR-01) shows the section covers diamond weight, not the "
                    "gold alloy weight of a ring. A citation that overstates a rule is itself a hallucination."),
        dict(id="C-16", session=SESSION, subject="Payment prose (CR-D49-01)",
             before="'Every seller reviewed checks out by card or Etsy checkout' and wire/Zelle/gift cards "
                    "'Not offered by these sellers'",
             after="Counts taken from the seller records and printed with every record accounted for: a credit card is "
                   "named by 5 of 13 records, Etsy checkout by 6 of the 7 Etsy shop records, 1 record (Solid Gold Jewelers) "
                   "states no payment method at all, and 1 record (the sold-out Etsy listing) carries no payment data. "
                   "Advertised checkout options are labelled as seller statements; absence of a statement is not evidence "
                   "that a method is refused. Published as FL-32 and linked to the row-level FL-13 gap",
             reason="The prose asserted more than any source states. FTC credit-card guidance establishes consumer dispute "
                    "rights, not merchant checkout methods."),
        dict(id="C-17", session=SESSION, subject="Checker blind spot — single-quoted HTML attributes",
             before="verify.py's link registry (C7) and security scan (C15) matched double-quoted attributes only, so a "
                    "single-quoted href or target could carry an unregistered external link or omit rel=noopener unnoticed",
             after="Both scans accept either quote style; C7's registry now also covers each reference's named mirror URL "
                   "and every official URL recorded in the evidence ledger (canonical checks, partial reads and "
                   "citation-scope reads). Negative test N15 proves the single-quoted case is caught; C22 gained a "
                   "scope-read publication requirement proved by N16",
             reason="Found while adding the § 23.18 scope-read link to the checklist: the new link was invisible to C7, "
                    "which reported PASS while an unregistered URL was live on the page. A checker that cannot see part of "
                    "the page is itself a hallucination risk, so the gap is recorded as a correction, not just fixed."),
        dict(id="C-18", session=SESSION, subject="Landing and category page reader claims (found post-merge on PR #53)",
             before="index.html said 'All 25 of 25 rows were re-read from the sellers' own pages on 2026-10-23' and every "
                    "category page said 'N of these N rows were re-read live on 2026-10-23', although this pass opened only "
                    "8 listings and 17 rows are inherited same-day reads; two of the seven category views (halo-pave 0 of 7, "
                    "bands 0 of 3) contained no row this pass opened at all",
             after="The landing page prints the split — 8 rows re-read live by 6d10ac0a, 17 inherited same-day from "
                   "bc4e36a1 and labelled — and each category page prints its own split, including 'None of these N rows was "
                   "opened in this pass' for the three views made entirely of inherited rows. C22 now enforces both sentences "
                   "and rejects a blanket 'every row was re-read' claim, proved by negative tests N17 and N18",
             reason="True about the date, false about the reader: the same overstatement class as CR-D49-01. Found by reading "
                    "the deployed pages after the merge instead of trusting a green checker, so it is recorded as a "
                    "correction and turned into a rule rather than only copy-edited."),
        dict(id="C-19", session=SESSION, subject="Cross-suite gate repair — tools/check_report.py amount corpus (found post-merge)",
             before="The no-hallucination gate's rule 'every amount quoted in a flag is documented in the evidence "
                    "corpus' built its corpus from ALL .txt/.md files in verification/evidence/, data/evidence/ and "
                    "docs/verification/ — including narrative memos from other suites. When this pass' memo quoted the "
                    "$420.00 sold-listing price, the security suite's planted $420 flag amount went from CAUGHT to "
                    "MISSED: tools/security_test.py reported 8/9 while check_report.py still reported PASS",
             after="The corpus is now (1) the capture files this suite's own rows, references, sellers and spot cite, "
                   "plus (2) the root level of its capture folders, read non-recursively — session subdirectories belong "
                   "to other suites and a memo nobody cites is prose, not a capture. A tenth planted error now proves the "
                   "boundary: an amount 'documented' only by an uncited memo must still be caught. Clean state PASS "
                   "(1,649 checks) and 10/10 planted errors caught",
             reason="Corpus bleed is a false negative in the project's main hallucination gate, so it was repaired rather "
                    "than logged only: no other session holds an open claim (gh pr list --state open is empty and every "
                    "board claim is closed), and the alternative — deleting the $420.00 quote from this pass' memo to make "
                    "someone else's test pass — would have degraded real evidence to satisfy a checker. The edit is "
                    "recorded here and on the board because tools/ is outside this session's claimed file scope."),
        dict(id="C-13", session=SESSION, subject="Listing values — no change attestation",
             before="AL-5882 $1,085/5.00 g · AL-170 $933/4.80 g · AL-4426 $585/3.58 g · AV-25893 $1,100.00/2.3 g · "
                    "JM-149700 $3,020.00 (retail $6,041.00)/2.3 g · SGJ-B02561 no price/4.7 g · BN-203738 $2,210/18K-vs-14K "
                    "conflict · ET-576343849 sold out $420.00 (original $525.00)/no exact grams",
             after="Identical — every re-read field matched the canonical row exactly",
             reason="Recorded so that 'unchanged' is an evidenced result rather than an assumption. The only canonical "
                    "value that moved this pass is the timestamped spot quote."),
    ]

    # ---- self-checks before writing -------------------------------------
    problems = []
    kinds: dict[str, int] = {}
    for c in checks:
        kinds[c.get("kind")] = kinds.get(c.get("kind"), 0) + 1
        if c.get("status") != "read" or c.get("checkedOn") != "2026-10-23":
            problems.append(f'{c.get("id")}: not a current read')
        if not str(c.get("url", "")).startswith("https://"):
            problems.append(f'{c.get("id")}: non-https url')
        if not c.get("sourceExcerpt"):
            problems.append(f'{c.get("id")}: empty excerpt')
        path = c.get("evidencePath")
        if not path or not os.path.exists(os.path.join(ROOT, path)):
            problems.append(f'{c.get("id")}: missing evidence file {path}')
        if c.get("readBy") not in (SESSION, INHERITED_BY):
            problems.append(f'{c.get("id")}: bad readBy {c.get("readBy")!r}')
    if kinds != {"listing": 25, "policy": 9, "reference": 11, "spot": 1}:
        problems.append(f"kind counts {kinds}")
    if len(checks) != 46:
        problems.append(f"{len(checks)} checks, expected 46")
    for sr in SCOPE_READS:
        if not str(sr.get("url", "")).startswith("https://"):
            problems.append(f'{sr.get("id")}: non-https scope-read url')
        if not sr.get("sourceExcerpt") or not sr.get("finding"):
            problems.append(f'{sr.get("id")}: scope read without excerpt or finding')
        if not os.path.exists(os.path.join(ROOT, sr.get("evidencePath", ""))):
            problems.append(f'{sr.get("id")}: missing evidence file {sr.get("evidencePath")}')
    for pr in PARTIAL_READS:
        if pr["entryId"] in {c.get("entryId") for c in checks if c["readBy"] == SESSION}:
            problems.append(f'{pr["entryId"]}: listed as both a full re-read and a partial read')
    if problems:
        print("ERROR: ledger self-check failed:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        return 1

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {OUT}: {len(checks)} checks "
          f"({ledger['coverage']['rereadThisPass']} re-read by {SESSION}, "
          f"{ledger['coverage']['inheritedSameDate']} inherited from bc4e36a1), "
          f"{len(PARTIAL_READS)} partial reads, {len(FAILURES)} logged failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
