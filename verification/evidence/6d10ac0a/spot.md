# S01 — Kitco live gold price re-read (session `6d10ac0a`, 2026-10-23)

* **Official URL:** <https://www.kitco.com/charts/gold>
* **Retrieved:** 2026-10-23 (this pass, late UTC) with `fetch_page`; page rendered in USD.
* **Result:** **corrected** — the panel bid had moved again since the canonical `$3,996.10` capture at
  4:10 p.m. ET. The older quote is retained as dated history and is not used in any calculation.

## Verbatim panel

```
Live GoldPrice
Oct 23, 2026 - 19:43 NY Time
Bid
3,994.90  USD
-28.20(-0.70%)
Ask
3,996.90

- ounce        3,994.90    -28.20
- gram           128.44     -0.91
- Kilo       128,440.99   -906.65
- pennyweight    199.75     -1.41
- tola         1,498.09    -10.58
- tael         4,854.91    -34.27

3975.10   4040.20   Day's Range

Prices provided by Kitco Metals Inc. Displayed in U.S. dollars (USD),
as of October 23, 2026 at 7:42 p.m. EDT.
```

## Verbatim body sentence

> "The current price of gold is **$3,994.90** per troy ounce as of October 23, 2026, 7:42 p.m. ET,
> down $28.40 today."

## Verbatim "Gold Value by Purity" table (same page, same capture)

| Fineness | VALUE (USD) |
|---|---|
| 24K Gold — 99.99% Gold — 999 | $3,994.90 |
| 22K Gold — 91.67% Gold — 916 | $3,662.12 |
| 18K Gold — 75.00% Gold — 750 | $2,996.18 |
| 14K Gold — 58.33% Gold — 585 | $2,330.23 |
| 10K Gold — 41.67% Gold — 417 | $1,664.67 |

Page footnote (verbatim): "* Estimated metal value only, retail premiums may apply to physical products."
The page also shows "Updated Oct 23, 2026 • 5:00 PM NY Time" next to that calculator block and an
embedded OANDA XAUUSD widget printing `C 3,995.810` at `19:43:05 UTC-4` — a **third** distinct print on
one page. Only the panel bid ($3,994.90) and its own per-gram figure ($128.44) are used for
calculations; the other prints are disclosed as FL-25 ("multiple spot prints on one page").

## Verbatim unit table ("Gold Price Today — Per Ounce, Gram and Kilo")

| Unit | Gold Price (USD) | Change | Low | High |
|---|---|---|---|---|
| per ounce | $3,994.90 | -$28.40 | $3,975.10 | $4,040.20 |
| per gram | $128.44 | -$0.91 | $127.80 | $129.90 |
| per 10 grams | $1,284.39 | -$9.13 | $1,278.02 | $1,298.95 |
| per kilo | $128,439.02 | -$913.08 | $127,802.43 | $129,895.45 |
| per pennyweight | $199.75 | -$1.42 | $198.76 | $202.01 |
| per tola | $1,498.09 | -$10.65 | $1,490.66 | $1,515.07 |
| per tael | $4,854.91 | -$34.51 | $4,830.85 | $4,909.97 |

Note the page's own internal inconsistency, recorded rather than smoothed over: the ticker block prints
kilo `128,440.99` while the unit table prints `128,439.02`. Neither figure is used in a calculation on
this site; the site computes per-gram values from `$3,994.90 / 31.1034768` (NIST troy ounce) and rounds
to the page's published `$128.44`.

## Arithmetic actually used (recomputed, never typed by hand)

* `$3,994.90 / 31.1034768 = $128.4379…/g` → published as the page's own **$128.44/g**.
* Intraday move from the previous canonical quote: `$3,994.90 − $3,996.10 = −$1.20/oz (−0.03%)`.
* Move from the 5:44 a.m. ET quote: `$3,994.90 − $4,022.50 = −$27.60/oz`.
* Fine gold = exact grams × published fineness (14K = 0.5833, 18K = 0.75, per 15 U.S.C. § 295 minimums).
* Metal value = fine gold × `$128.44/g`. Rows without an exact gram figure stay **blank** — no range is
  converted into a weight and no weight is inferred.
