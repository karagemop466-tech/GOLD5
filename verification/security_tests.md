# Security / hallucination tests — does the gate actually catch a fabricated value?

A checker that has only ever passed is not evidence of anything. So the gate is tested by
**planting errors on purpose** and requiring it to fail. Run it yourself:

```bash
python3 tools/security_test.py
```

Latest run (2026-10-22, this pass):

| # | Planted error | Result | What the checker said |
|---|---|---|---|
| 1 | A01 price changed from $1,085 to $999 in the dataset | **CAUGHT** | `A01: price 999 has no token containing it` · `prose mentions an amount not on the captured page (999.00)` · `computed price/metal multiple 2.65x missing` |
| 2 | A07 (Blue Nile, no weight published) given an invented `4.2 g` | **CAUGHT** | `A07: weight 4.2 has no token containing '4.2'` · `computed fine gold 2.45 g missing from the site` |
| 3 | A row pointed at a flag id that does not exist (`G-MADE-UP`) | **CAUGHT** | `A01: references unknown flag G-MADE-UP` |
| 4 | A09's EUR price text quietly replaced with `$950.00` | **CAUGHT** | `A09: prose mentions an amount not on the captured page (950.00)` |
| 5 | The evidence token for "2.3 grams" deleted | **CAUGHT** | `A05: weight 2.3 has no token containing '2.3'` |
| 6 | A product URL swapped for `https://example.com/fake-ring` | **CAUGHT** | `URL outside the official allowlist` |
| 7 | A hand-typed `$999.99` inserted straight into `index.html` | **CAUGHT** | `index.html: renders an amount that is not traceable to data ($999.99)` |

**7 of 7 planted errors caught; clean state passes** (1,617 checks, 0 failures).

Two of these tests were added *because an earlier version of the checker missed them*:

- Test 4 initially passed. The money audit had trusted any amount that appeared anywhere in
  `verification/data.json`, so editing `priceText` by hand slipped through. Fixed by requiring every
  amount written in a row's prose to also exist on that row's captured page.
- Test 6 initially exposed that a dataset URL only had to look like a URL. Fixed with the
  official-domain allowlist.

That is the point of the exercise: the checker is tested against its own blind spots, not just run.

## What the checker enforces (10 groups)

1. **Schema** — required fields on every row, no duplicate ids, no zero/negative prices or weights.
2. **Evidence match** — every recorded value must appear **verbatim** in the saved capture of the page
   named by the row (`verification/evidence/*.txt`, or the prior-session capture for B rows).
3. **Domain allowlist** — every URL must belong to a seller's own domain or an official body.
4. **Spot arithmetic** — per-gram and per-karat figures must reconcile with the published per-ounce quote.
5. **Derived values** — fine gold, metal value, troy ounces and price/metal are recomputed from the raw
   inputs and must be present exactly on the rendered site.
6. **Money audit** — every `$`/`€` amount in the HTML must trace to a published price, a quoted
   reference, or a recomputation.
7. **Link integrity** — every local `href`/`src` and every in-page anchor must resolve.
8. **Flag cross-references** — both directions (row → flag, flag → row) must resolve.
9. **Disclosure** — every page must carry the no-hallucinations notice.
10. **Pass log** — every pass recorded as rendered must actually appear on the Method page.

## What the checker cannot do

It cannot tell you whether a seller is **lying**. It proves the site faithfully reproduces what the
seller's page said on the capture date — nothing more. That is why the hallmarks are blank, why the
weights are blank where the seller publishes none, and why the checklist ends with an independent
jeweler and an XRF reading.
