# GOLD5 post-merge integration audit — session `d49fe320`

**Check date:** 2026-10-23 UTC  
**Branch:** `arena/d49fe320-gold5`  
**Target commit/site:** `368ddac68ea00d94e4adac68d61b505cab4a362d` (PR #50 merge)  
**Method:** cache-busted GitHub Pages reads (`?v=368ddac`), local combined-tree checks, direct reads of official government, standards, market and seller pages. No product prices were changed.

## Deployment and production pages

- PR #50, [GOLD5: field-level evidence reconciliation and verified dashboard](https://github.com/karagemop466-tech/GOLD5/pull/50), merged at `2026-10-23T20:46:45Z` as `368ddac68ea00d94e4adac68d61b505cab4a362d`.
- Required PR checks `review` and `verify` both succeeded. GitHub Pages run [40021841320](https://github.com/karagemop466-tech/GOLD5/actions/runs/40021841320) succeeded on the merge commit; Pages API reported `status: built` at `2026-10-23T20:47:42Z`.
- Cache-busted production reads succeeded for the [landing page](https://karagemop466-tech.github.io/GOLD5/?v=368ddac), [categories](https://karagemop466-tech.github.io/GOLD5/site/categories.html?v=368ddac), [25-row listings](https://karagemop466-tech.github.io/GOLD5/site/listings.html?v=368ddac), [Flagged for Review](https://karagemop466-tech.github.io/GOLD5/site/flagged.html?v=368ddac), [verification ledger](https://karagemop466-tech.github.io/GOLD5/site/verification.html?v=368ddac), [gold price](https://karagemop466-tech.github.io/GOLD5/site/gold-price.html?v=368ddac), [calculator](https://karagemop466-tech.github.io/GOLD5/site/calculator.html?v=368ddac), [checklist](https://karagemop466-tech.github.io/GOLD5/site/checklist.html?v=368ddac), and [Master Audit](https://karagemop466-tech.github.io/GOLD5/site/master-audit.html?v=368ddac).
- The live landing page places **NO HALLUCINATIONS** at the top, reports 25 listings / 13 sellers, the dated spot quote, 24 open flags and zero checker failures. The live listing page reports 25/25 rows; categories reports seven views. The root pages keep official listing URLs and evidence links in each row.

## H5 close-out — PR #51 and final Pages check

- PR [#51](https://github.com/karagemop466-tech/GOLD5/pull/51) merged from `arena/d49fe320-gold5` to `main` at `2026-10-23T23:56:42Z` as `f4099761ac2932aaa02d8a8b0dbf8fa04eb0640e`. The `review` and `verify` checks passed (runs [40042391493](https://github.com/karagemop466-tech/GOLD5/actions/runs/40042391493) and [40042391400](https://github.com/karagemop466-tech/GOLD5/actions/runs/40042391400)).
- Pages run [40042433195](https://github.com/karagemop466-tech/GOLD5/actions/runs/40042433195) completed successfully on that merge commit; the Pages API reported `built` at `2026-10-23T23:57:10Z`.
- Cache-busted live reads with `?v=f409976` succeeded for the [landing page](https://karagemop466-tech.github.io/GOLD5/?v=f409976), [Flagged for Review](https://karagemop466-tech.github.io/GOLD5/site/flagged.html?v=f409976), [Verification](https://karagemop466-tech.github.io/GOLD5/site/verification.html?v=f409976), and [COORDINATION.md](https://karagemop466-tech.github.io/GOLD5/COORDINATION.md?v=f409976). The canonical root site remained on its explicitly timestamped 4:10 p.m. spot snapshot; the Flagged page still has 24 open and 6 resolved entries and has **not** been updated with the five new D49 requests.

## Combined-tree verification

Full raw outputs are in [`harness_results.txt`](harness_results.txt). All nine prescribed suites passed:

| Suite | Result |
|---|---|
| `python3 scripts/verify.py` | **22/22**; 25 rows, 13 sellers, 30 flags, 11 references; 25 HTTPS sources; all internal links resolve across 19 pages; 65 external URLs registered; 46-check ledger agrees; 10/10 injected errors caught |
| `python3 scripts/independent_audit.py` | **11/11**; arithmetic, all 60 raw-gold cells, all dollar amounts and source tokens recomputed/checked |
| `python3 scripts/audit_b1f2fe3b.py` | **6/6** groups; 38 unified rows; 103 HTML files; 4,186 local links; 4/4 injected errors caught |
| `python3 scripts/review_current.py --check` | **PASS**; 264 records; 92 exact URLs; 6/6 negative tests; checker explicitly labels itself offline/structural |
| `python3 tools/check_hallucinations.py` | **166 PASS / 0 FAIL / 0 WARN / 1 INFO** (duplicate 2.3 g / 14K weight on two different listings; remains flagged for independent confirmation) |
| `python3 tools/check_report.py` | **1,649 checks, 0 failures/warnings** |
| `python3 tools/security_test.py` | **9/9 planted errors caught; clean-state PASS** |
| `(cd verified && python3 scripts/verify.py)` | **896 assertions, 0 failures** |
| `python3 dossier/scripts/build.py` | **18/18; 58 rows; 23 pages; 1,104 references; 0 broken links** |

The test builders rewrote tracked artifacts in the `dossier/`, `verified/reports/`, and prior report scopes; because those paths are owned by completed sessions and this pass was read-only, their generated changes were restored to the committed state. The only new evidence paths are this session's unique `data/` and `verification/evidence/` files.

## Direct source checks and findings

### Official guidance — FTC

[FTC Consumer Advice: Buying Platinum, Gold, and Silver Jewelry](https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry) was fetched directly. It advises researching the seller and obtaining return policies in writing; says to look near the karat mark for the name or U.S. registered trademark behind it; defines “solid gold” as not hollow; and distinguishes gold plating, gold-filled, overlay/RGP, electroplate and vermeil. These checks support the corresponding checklist topics.

[FTC Consumer Advice: Using Credit Cards and Disputing Charges](https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges) says consumers have rights under law, including the right to dispute billing errors. That page does **not** confirm which payment methods any individual jewelry seller accepts.

### Source-scope and payment claims requiring correction

1. **Payment methods are overstated in the canonical prose.** The root checklist says “Every seller reviewed checks out by card or Etsy checkout”; the Seller page's payment summary says cards are accepted by “Every seller reviewed” and says wire/Zelle/gift cards are “Not offered by these sellers.” Canonical data says Solid Gold Jewelers' payment method is **“Not stated; price is quoted by phone”** and the sold Etsy listing's payment is **n/a — item sold**. Its [official product page](https://solidgoldjewelers.net/product/yellow-gold-solitaire-engagement-ring/) says to call for current price and availability, but does not state a payment method. The FTC credit-card page cannot substantiate merchant acceptance. The existing `FL-13` is the relevant source-linked flag; its detail/root Flagged page should include the missing payment method. No H3-owned page or builder file was edited under the exclusive-scope rule.
2. **The weight source does not cover ring-alloy weight.** The checklist's row 4 links to [16 CFR §23.18](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.18). The fetched official eCFR text says §23.18 concerns misrepresentation of a **diamond's** weight and representations in diamond carats/points/fractions. It does not establish a legal duty to publish the metal weight of a ring. The weight request is a project buying criterion; the source label should say so and not imply that §23.18 governs ring-metal grams.
3. **Checklist reputation numbers need direct citations at the row.** The checklist row cites FTC guidance for seller research but reports BBB and ConsumerAffairs numbers. The [seller table](https://karagemop466-tech.github.io/GOLD5/site/sellers.html?v=368ddac) already has the direct [BBB profile](https://www.bbb.org/us/wa/seattle/profile/jewelry-stores/blue-nile-inc-1296-15026564) and [ConsumerAffairs page](https://www.consumeraffairs.com/retail/blue-nile.html), each labeled “prior-session capture.” The checklist row should link those sources directly or direct readers explicitly to that prior-snapshot row.
4. **Use an official U.S. Code link for §297.** The data's §297 reference points to the [Cornell LII mirror](https://www.law.cornell.edu/uscode/text/15/297). An official [GovInfo §297 text](https://www.govinfo.gov/link/uscode/15/297) is available and was fetched; it describes the identifying trademark/name and placement near the quality mark for covered manufacturers/dealers. Prefer GovInfo or label Cornell as a mirror.

These are **change requests**, not silently verified claims. They are recorded with the affected file scopes and official links in `COORDINATION.md` and `data/live_check_d49fe320.json`; this session did not edit the completed H3-owned authoring/build files or generated root pages.

### Timestamped market quote

The official [Kitco live gold page](https://www.kitco.com/charts/gold) was fetched again. It displayed `Oct 23, 2026 - 19:43 NY Time`, with a quote stated as of **7:42 p.m. EDT**: bid **$3,994.90/ozt**, **$128.44/g**. This is newer than the site's selected 4:10 p.m. ET snapshot (**$3,996.10/ozt**, **$128.48/g**). The site calls its values dated snapshots, not a live feed, and existing `FL-19` explains intraday changes; no current catalog or formula was altered without a source-data task. A future data refresh must save the new quote and recompute every spot-derived amount.

### Source references directly checked

- [16 CFR Part 23, eCFR](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23) — eCFR showed “up to date as of 10/21/2026” on this fetch.
- [15 U.S.C. §295, GovInfo](https://www.govinfo.gov/link/uscode/15/295) — official text for gold-fineness standards/tolerances, subject to the covered commerce provisions.
- [15 U.S.C. §297, GovInfo](https://www.govinfo.gov/link/uscode/15/297) — official identifying-trademark text.
- [NIST SP 811, Appendix B.8](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8) — official conversion-factor page; the repository preserves its distinction between NIST's rounded conversion and Kitco's stated `31.1034768 g/ozt` constant.

## No-hallucinations recommendation

The automated checks all pass, but they do not verify semantic fit between every prose statement and every cited page. This pass found payment-method overclaiming and a diamond-weight citation incorrectly used for ring-metal weight despite a green 166-check hallucination suite. **Keep looking for hallucinations:** add semantic checks for payment fields, source-section scope, direct row citations, and stale timestamped spot quotes. Leave unknown payment methods blank, keep them on Flagged for Review, and do not infer them from a phone quote or a generic FTC recommendation.
