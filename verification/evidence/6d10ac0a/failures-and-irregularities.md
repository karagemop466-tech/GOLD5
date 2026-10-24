# Failures and irregularities — session `6d10ac0a` (2026-10-23)

Nothing in this file was used to fill a value. Every item is published so the next reviewer can see
exactly where this pass stopped short.

## 1. Fetch failures (retried, then logged)

| # | Target | What happened | Outcome |
|---|---|---|---|
| F1 | `https://www.avianneandco.com/products/14k-solid-yellow-gold-diamond-solitaire-engagement-ring-0-41-carat` | Returned Shopify's **"404 Not Found — The page you were looking for does not exist"** | **Operator error, caught by the source:** this URL was mistyped from a truncated printout of the dataset (the real handle ends `-0-41-ctw`). The correct canonical URL was then fetched successfully and matched. Lesson recorded: **always copy the URL from the dataset, never retype it** — a 404 on a mistyped URL proves nothing about the listing. |
| F2 | Brilliant Earth `BE-1343`, Blue Nile `BN-203738`, Etsy `ET-576343849` (first attempts) | The fetch proxy returned `SignatureDoesNotMatch` (an Alibaba Cloud OSS signature error returned by the fetch proxy) — an infrastructure error, not a site error | Retried with the same official URL; all three then loaded. The failures are logged here rather than being silently dropped, because a failed read must never be reported as a successful one. |
| F3 | Brilliant Earth `BE-1343` (successful load) | Retrieved content chunk contained **only navigation**; the price block was not in it | Recorded as a **partial read**. USD price stays blank (FL-08); the `bc4e36a1` same-day observation (page served €835) is retained with its own date and evidence path. |
| F4 | Etsy `ET-1151446373` (successful load) | Description retrieved; **price block not present** in the retrieved chunk | Recorded as a **partial read**. Weight/karat/solid-gold wording corroborated; price stays labelled inherited (L21). |

## 2. Pages re-read this pass that were **not** re-read at policy level

The 9 seller policy/contact checks (Blue Nile returns, Brilliant Earth returns/shipping, Allurez return
policy and warranty, Avianne contact, Jewelry Master shipping/returns, Solid Gold Jewelers contact, Etsy
Purchase Protection, Etsy shop pages) were **not** re-opened this pass. They keep `bc4e36a1`'s 2026-10-23
capture, evidence IDs `P01–P09` and their original evidence paths, and the ledger labels them
`readBy: bc4e36a1 (inherited)`. Two product pages re-read here display their own return wording
(Allurez "Return or exchange within 30 days if unsatisfied", Avianne "Returns of unworn and unaltered
items accepted within 14 days"), which **corroborates** but does not replace the policy-page reads;
`returnsVerified` for those rows is therefore marked inherited, not re-confirmed.

## 3. Official references

All 11 official/regulatory references (FTC Consumer Advice, 16 CFR Part 23, 16 CFR § 23.3,
15 U.S.C. § 295, 15 U.S.C. § 297, NIST SP 811 App. B.8, LBMA, FTC credit-card/dispute guidance, Etsy
Purchase Protection, JVC mediation, ReportFraud.ftc.gov) keep `bc4e36a1`'s 2026-10-23 reads
(`R01–R11`) and are labelled inherited in this pass's ledger. They are stable government/standards pages
whose quoted text is reproduced verbatim in `verification/evidence/bc4e36a1/spot-and-references.md` and
`verification/evidence/v2/ftc_ecfr_usc295_2026-10-23.txt`. Recommended for the next pass: re-open
16 CFR § 23.3 and 15 U.S.C. § 295 first, because the checklist's tolerance wording (-3‰ / -7‰) is quoted
from them.

## 4. Irregularities recommended for continued hunting

1. **`BN-203738` metal conflict (FL-30)** — the same page still says `18K White Gold` in the title and
   specification and `14k yellow gold` in Product Details. Unresolved on the source; published as a
   conflict. Do not average or pick a side.
2. **Duplicate `2.3 g / 14K`** across `AV-25893` (Avianne) and `JM-149700` (Jewelry Master). Both pages
   were re-read this pass and both still print 2.3 g, so the duplicate is real on both sources. The
   informational checker note stays open.
3. **Kitco prints three different numbers on one page** (panel bid `$3,994.90`, body sentence
   `$3,994.90` "as of 7:42 p.m. ET", embedded OANDA widget close `3,995.810`, plus a kilo figure that
   disagrees with itself: `128,440.99` in the ticker vs `128,439.02` in the unit table). Only the panel
   bid and its own per-gram figure are used; the rest are disclosed (FL-25).
4. **`SGJ-B02561`** still publishes **no price** — only "Call (309) 452-1612 for current pricing and
   availability." A phone quote would be a new, dated seller statement; it must not be back-filled from
   any other source.
5. **Allurez size surcharges** (`+$39` … `+$99` on `AL-4426` for sizes ≥ 10.25) mean the displayed price
   is size-dependent. The row keeps the base displayed price and its basis label; variant prices are not
   blended in.
6. **`Brand: M Michael`** on `SGJ-B02561` is a store taxonomy field, **not** a hallmark/maker's-mark
   claim. `makerMarkStated` stays `false`.
7. **Etsy `Star Seller`** badges (e.g. VeraByEden) are marketplace service metrics, not purity evidence.
8. **Promo banners** (Avianne `FALL10` 10% off, Brilliant Earth `$250 gift card` with code `GIFT`,
   Jewelry Master "LAB DIAMOND SALE - Up to 50% OFF", Blue Nile "Up to 30% Off Select Styles") were
   visible on pages re-read this pass. **No** recorded price includes a coupon, and no banner figure is
   recorded as a product price.
