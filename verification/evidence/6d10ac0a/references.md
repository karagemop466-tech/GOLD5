# Official-source scope reads — session `6d10ac0a` (2026-10-23)

Two official sources were re-opened live this pass because session `d49fe320`'s post-merge audit
(PR #52) logged change requests saying the canonical site's **citation scope** was wrong. Both reads
below are verbatim. They are recorded in the ledger as `scopeReads` (they do not replace any of the 46
canonical checks except R05, which is re-read and re-pointed to the official GovInfo text).

---

## SR-01 — 16 CFR § 23.18 (eCFR) — what the section actually covers

* **Official URL:** <https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.18>
* **Retrieved:** 2026-10-23 by session `6d10ac0a`.
* **Page state (verbatim):** "This content is from the eCFR and is authoritative but unofficial.
  Displaying title 16, up to date as of 10/21/2026. Title 16 was last amended 10/19/2026."
  Authority: "15 U.S.C. 45, 46." Source: "83 FR 40667, Aug. 16, 2018, unless otherwise noted."
  Official published edition link on the page: "View the PDF for 16 CFR 23.18" →
  `https://www.govinfo.gov/link/cfr/16/23?link-type=pdf&sectionnum=18&year=mostrecent`.

Verbatim section text as retrieved:

> **§ 23.18 Misrepresentation of weight and "total weight."**
>
> (a) It is unfair or deceptive to misrepresent the weight of a diamond.
>
> (b) It is unfair or deceptive to use the word "point" or any abbreviation in any representation,
> advertising, marking, or labeling to describe the weight of a diamond, unless the weight is also
> stated as decimal parts of a carat (e.g., 25 points or .25 carat).
>
> A carat is a standard unit of weight for a diamond and is equivalent to 200 milligrams (1⁄5 gram).
> A point is one one-hundredth (1/100) of a carat.
>
> (c) If diamond weight is stated as decimal pa[rt of a carat …] *(retrieved chunk ends mid-subsection)*

**Finding (CR-D49-02 confirmed):** § 23.18 governs **diamond** weight representations — carat, point and
"total weight" claims. It does **not** require a seller to disclose the gram weight of a ring's gold
alloy, and it is not the legal basis for this project's "ask for grams" criterion. The checklist row has
been reworded: asking for the metal weight in grams is **this project's buying criterion** (supported by
FTC advice to get the facts in writing), and § 23.18 is cited only for what it actually says — that
misrepresenting diamond weight, or using "points" without decimal carats, is unfair or deceptive. That
matters here because 15 of the 25 rows are settings whose price excludes the center stone, so a
diamond-weight claim is exactly where a buyer can be misled.

---

## SR-02 — 15 U.S.C. § 297 (GovInfo, official U.S. Code text) — the maker's-mark rule

* **Official URL used:** <https://www.govinfo.gov/link/uscode/15/297>
* **Resolved to (verbatim from the fetch):**
  `https://www.govinfo.gov/content/pkg/USCODE-2024-title15/pdf/USCODE-2024-title15-chap8-sec297.pdf`
  — the U.S. Government Publishing Office's official 2024 edition U.S. Code text.
* **Retrieved:** 2026-10-23 by session `6d10ac0a`.

Verbatim text as retrieved:

> **§ 297. Stamping plated articles**
>
> **(a) Words "sterling" or "coin" forbidden** — In the case of articles of merchandise made in whole or
> in part of an inferior metal, having deposited or plated thereon or brazed or otherwise affixed thereto
> a plating, covering, or sheet composed of gold or silver … and known in the market as rolled gold plate,
> gold plate, gold filled, silver plate, or gold or silver electroplate, or by any similar designation …
> no such article, nor any tag, card, or label attached thereto, nor any box, package, cover, or wrapper
> in which such article is encased or inclosed, shall be stamped, branded, engraved, or imprinted with any
> word or mark usually employed to indicate the fineness of gold, unless such word or mark be accompanied
> by other words, plainly indicating that such article or part thereof is made of rolled gold plate, gold
> plate, or gold electroplate, or is gold filled, as the case may be …
>
> **(b) Identifying trademark** — Whenever any person, firm, corporation, or association, being a
> manufacturer or dealer subject to section 294 of this title — (1) applies or causes to be applied to any
> article of merchandise intended for sale or customarily sold as a complete product to consumers in any
> State, by stamping, branding, engraving, or otherwise, any quality mark or stamp indicating or
> purporting to indicate that such article is made in whole or in part of gold or silver or of an alloy of
> either such metal; or (2) imports into any State any such article of merchandise bearing any such
> quality mark or stamp … shall — **(A)** Apply or cause to be applied to that article a trademark of such
> persons, which has been duly registered or applied for registration under the laws of the United States
> within thirty days after an article bearing the trademark is placed in commerce or imported into the
> United States, or the name of such person; and **(B)** if such article of merchandise is composed of two
> or more parts which are complete in themselves but which are not identical in quality, and any one of
> such parts bears such a quality mark or stamp, apply or cause to be applied to each other part of that
> article of merchandise a quality mark or stamp of like pattern and size disclosing the quality of that
> other part.
>
> Each identifying trademark or name applied to any article of merchandise in compliance with clause (A)
> of this subsection shall be applied to that article by the same means as that used in applying the
> quality mark or stamp appearing thereon, in type or lettering at least as large as that used in such
> quality mark or stamp, and **in a position as close as possible to that quality mark or stamp**. For the
> purposes of this subsection, the term "State" includes the Commonwealth of Puerto Rico, the Virgin
> Islands, Guam, American Samoa, and the District of Columbia.
>
> *(June 13, 1906, ch. 3289, § 4, 34 Stat. 261; Pub. L. 87–354, § 1, Oct. 4, 1961, 75 Stat. 775;
> Pub. L. 91–366, § 1(e), July 31, 1970, 84 Stat. 691.)*

**Finding (CR-D49-04 implemented):** the canonical reference for § 297 now points at this **official
GovInfo U.S. Code text** instead of the Cornell LII mirror. The Cornell page
<https://www.law.cornell.edu/uscode/text/15/297> remains a legitimate mirror and is named as such in the
reference's method note; it is no longer the cited source. The statutory language above is the basis for
the checklist's hallmark rule: a quality mark (e.g. "14K") must be accompanied by the **manufacturer's or
dealer's registered trademark or name**, applied by the same means, in lettering at least as large, and
**as close as possible** to the quality mark. It also confirms why "gold filled", "rolled gold plate" and
"electroplate" items may not carry a bare fineness mark — the wording this project screens listings
against.

**Not claimed:** neither § 297 nor the FTC guides require a seller to publish a photograph of the stamp,
to state the gram weight of the alloy, or to accept a return after an independent assay. Those remain
this project's buying criteria, labelled as such on the checklist.

---

## Payment-scope note (CR-D49-01)

Session `d49fe320` also re-read
<https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges> and
<https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/> and recorded that FTC
credit-card guidance establishes **consumer** dispute rights, not which methods a given merchant accepts,
and that the Solid Gold Jewelers page states **no** payment method at all (it says "Call (309) 452-1612
for current pricing and availability"). Solid Gold Jewelers was independently re-read by this session
(ledger check L18, [`retailers.md`](retailers.md)) and confirms that: no price and no payment method are
published. The canonical seller record already said "Not stated; price is quoted by phone." — the site's
**prose** was what overstated it, and the prose is corrected in this pass (checklist payment row, sellers
payment table, and new flag FL-32).
