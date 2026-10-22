# Research: Gold Price Source and Calculator Basis

**Status:** VERIFIED against official sources.  
**Session:** arena. **Date:** 2026-10-22 (UTC).

## Official sources used

1. LBMA, "LBMA Gold Price" — the internationally recognised benchmark price for gold delivered in London  
   https://www.lbma.org.uk/prices-and-data/lbma-gold-price
2. LBMA, "About LBMA Daily Auction Prices"  
   https://www.lbma.org.uk/prices-and-data/about-lbma-daily-auction-prices
3. NIST OWM precious metals conversion (1 troy oz = 31.1034768 g) — see research/weight.md  
   https://www.nist.gov/document/precious-metals-conversion-information-march2015pdf

## Verified facts

| Item | Verified value | Source |
|------|----------------|--------|
| LBMA Gold Price | Internationally recognised benchmark price for gold delivered in London | LBMA |
| Auction frequency | Set twice daily (10:30 and 15:00 London time) in U.S. dollars per troy ounce | LBMA |
| Administrator | ICE Benchmark Administration (IBA) | LBMA |
| Purity basis | Price is for 995 fineness gold | LBMA (Precious Metal Benchmarks) |
| Spot vs LBMA | The LBMA price is a fixed reference set twice daily; spot moves continuously; they are usually close at auction times | LBMA / metalsradar summary |
| Price per gram formula | price per gram = price per troy ounce ÷ 31.1034768 | NIST-derived conversion |

## No-hallucination rule for prices

- No live spot price is hard-coded as a "current" fact without a timestamp and source.
- The site calculator lets the user enter today's spot price; a reference price captured at build time is shown ONLY with its source and capture timestamp (see site/price.html).
- No product prices are listed anywhere on this site (no products are reviewed or sold here).

## Irregularities / flags

- LBMA publishes benchmark prices; real-time retail spot quotes vary by dealer (BullionVault, Money Metals, etc. show different live figures). Any live price shown on the site is labeled "reference only — check LBMA/dealer feed at time of purchase" and never presented as an official transaction price.
