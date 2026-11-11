# Partial review, 2026-11-11 UTC

No hallucinations: these are source observations, not authentication or complete market coverage. Product pages BN-192506, BN-203738 and AL-4426, the Blue Nile and Allurez policy pages, and Kitco were read through `fetch_page` on 2026-11-11. First rendered chunks supplied the quoted observations; additional chunks were not systematically audited. The product and policy sources are linked next to each row on `index.html`.

- BN-192506: page rendered `$1,255$1,004(Setting Price)`, `-20%`, `Metal Type:14K Yellow Gold`. It described the center stone separately. The promotional quote is a snapshot, not a promise.
- BN-203738: `$2,210$1,768(Setting Price)`, `Metal Type:18K White Gold`, but Product Details say “crafted from warmly lustrous 14k yellow gold.” The conflict is unresolved.
- AL-4426: `$585`, “Setting only. Center stone sold separately.” and “Approximate Metal Weight 3.58 grams”; seller also lists size-dependent surcharges. An approximate weight is not an assay.
- Kitco: panel `Nov 11, 2026 - 2:55 NY Time`, bid `4,059.30`, gram `130.51`, footnote `November 11, 2026 at 2:54 a.m. EST`; body `$4,058.90` per ounce as of `2:54 a.m. ET`. Do not reconcile the distinct values by assumption.
- Blue Nile `/policies/returns` includes standard and holiday terms and exclusions; Allurez `/pages/return-policy` includes 30-day arrival and Design Your Own exchange terms. Neither determines the eligibility of a particular purchase without confirming all conditions.
- `/returns` at Blue Nile and `/business-guidance/resources/jewelry-guides` at FTC returned a rendered not-found page despite `fetch_page` reporting success. No policy or authority claim was derived from them.

The existing 25-row canonical dataset and other datasets were not fully re-read in this session. Historical passes remain attributed to their original sessions and must not be presented as this session's verification. Unchecked fields are blank in the partial review. Run automated checks after any review and actively seek errors; tests do not establish current truth, availability, seller trustworthiness, or physical purity.
