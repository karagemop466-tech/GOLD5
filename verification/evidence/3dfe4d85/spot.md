# S01 — Kitco live gold price re-read (session `3dfe4d85`, 2026-10-25)

* **Official URL:** <https://www.kitco.com/charts/gold>
* **Retrieved:** 2026-10-25 03:14 UTC (Sat night / Sun early ET — world spot markets closed after the
  Friday 5:00 p.m. NY close) with `fetch_page`; page rendered in USD.
* **Result:** **unchanged in value, newer in timestamp** — the panel still prints the Friday close
  (bid $3,994.90, −28.20, −0.70%; gram $128.44). The panel timestamp moved from
  `Oct 23, 2026 - 19:43 NY Time` to `Oct 24, 2026 - 23:14 NY Time`, and the body sentence now says
  "as of October 24, 2026, 11:12 p.m. ET". The canonical primary quote ($3,994.90 / $128.44) is
  re-confirmed by this session's own read; the prior 2026-10-23 7:42 p.m. ET capture moves to the
  dated history chain.

## Verbatim panel

```
Live GoldPrice
Oct 24, 2026 - 23:14 NY Time
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
as of October 24, 2026 at 11:12 p.m. EDT.
```

## Verbatim body sentence

> "The current price of gold is **$3,994.90** per troy ounce as of October 24, 2026, 11:12 p.m. ET,
> down $28.40 today."

## Verbatim "Gold Value by Purity" table (same page, same capture)

| Fineness | VALUE (USD) |
|---|---|
| 24K Gold 99.99% (999 24K · 24KT · 999.9 · 1000) | $3,994.90 |
| 22K Gold 91.67% (916 22K · 22KT · 917) | $3,662.12 |
| 18K Gold 75.00% (750 18K · 18KT) | $2,996.18 |
| 14K Gold 58.33% (585 14K · 14KT · 583) | $2,330.23 |
| 10K Gold 41.67% (417 10K · 10KT · 416) | $1,664.67 |

Followed by: "Gold Value by Purity at spot bid — Based on a Kitco Gold Spot Bid, one (1) troy ounce of
24K Gold is worth approximately $3,994.90. … of 22K … $3,662.12. … of 18K … $2,996.18. … of 14K …
$2,330.23. … of 10K … $1,664.67." and the table's own update stamp "Updated Oct 23, 2026 • 5:00 PM NY
Time" — i.e., the purity table itself carries the Friday 5:00 PM NY update stamp, consistent with a
weekend close.

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

Same two kilo prints as the 2026-10-23 capture: ticker **128,440.99** vs unit-table **128,439.02**
(FL-25 disclosure continues; neither is used in any calculation — the gram and ounce figures are).

## Extra prints in this capture (disclosed, unused — FL-25)

* Embedded TradingView XAUUSD widget: header row rendered **O ∅ H ∅ L ∅ C ∅** with clock
  `23:14:15 UTC-4` — this time the widget printed **no numeric close at all** (on 2026-10-23 the same
  widget printed a close of 3,995.810). No widget number is used anywhere.
* "A troy ounce is 31.1034768 grams" (page's own prose, matches the constant used by every
  calculation on the site).

## Derived-value basis (recomputed by script, never typed)

* Primary quote used for all arithmetic: **bid $3,994.90/oz = $128.44/g** (same numbers as the
  2026-10-23 7:42 p.m. ET capture because the market has not reopened; timestamp is newer and was
  read by this session).
* Purity per-oz values 24K 3,994.90 / 22K 3,662.12 / 18K 2,996.18 / 14K 2,330.23 / 10K 1,664.67 are
  taken verbatim from this capture.
