# T2 — Gold spot price verification (checked 2026-10-22)

Rule: a price is recorded only from a source actually read that day. All four quotes below are
same-day (2026-10-22) and agree within ~1.6%.

## Primary (used for all calculations)
- Source: **Kitco**, https://www.kitco.com/charts/gold — captured by **direct page fetch**
- Timestamp: **October 22, 2026, 7:10 p.m. EDT** (latest of the four)
- Quoted: "Live GoldPrice Oct 22, 2026 - 19:11 NY Time … Bid ### 4,025.00 USD … - gram 129.41"
- Page body: "The current price of gold is **$4,024.60** per troy ounce as of October 22, 2026, 7:10 p.m. ET, up $1.30 today."
- Recorded: usdPerOz = 4025.00 (bid), usdPerGram = 129.41
- Consistency: 4025.00 ÷ 31.1034768 = 129.41 ✓ (matches published gram value)

## Cross-checks (same day)
| # | Source | Quote (verbatim snippet) | as of | Recorded |
|---|--------|--------------------------|-------|----------|
| 1 | CNBC Select, https://www.cnbc.com/select/the-price-of-gold-today-oct-22-2026/ | "Gold's spot price — or its current trading value — today as of 9:00 a.m. ET is $4,083.82 per ounce, according to CNBC's Gold/ US Dollar Spot Price." | 2026-10-22 9:00 a.m. ET | 4083.82/oz |
| 2 | APMEX, https://www.apmex.com/gold-price | "Gold Spot Price $4,077.60 USD … Gold Price Per Ounce $4,077.60 … Gold Price Per Gram $131.10 … Last Updated: 10/22/2026 11:02:00 AM ET" | 2026-10-22 11:02 a.m. ET | 4077.60/oz, 131.10/g (4077.60÷31.1035=131.10 ✓) |
| 3 | Kitco News AM Report, https://www.kitco.com/news/article/2026-10-22/gold-silver-pressured-despite-lower-yields-hormuz-attacks-send-crude-higher | "At the latest verified morning price reading, spot gold was near $4,086.90 an ounce, down $53.40, or 1.29%" | 2026-10-22 morning | 4086.90/oz |

Spread: (4086.90 − 4025.00) / 4025.00 = 1.54% — normal intraday variation; recorded as flag F7.

## Purity values (same Kitco page, "Gold Value by Purity", updated Oct 22, 2026 7:11 PM NY)
- 24K 99.99% → $4,025.00/oz · 22K 91.67% → $3,689.72/oz · 18K 75.00% → $3,018.75/oz · 14K 58.33% → $2,347.78/oz · 10K 41.67% → $1,677.22/oz
- Fineness fractions (0.9999/0.9167/0.75/0.5833/0.4167) match karat/24 math; used by the calculator.
- Per-gram values on site are **derived** (÷31.1034768), labeled as derived — not claimed as source-published.

## Irregularities
- None. All four sources independent; no quote omitted.
