# GOLD5 — Solid Gold Engagement Ring Research & Buyer's Dashboard

Research project to **find gold engagement rings** that meet a strict online-buying checklist
(solid gold, karat, hallmark, weight in grams, seller reputation, price vs. gold value,
return policy, payment protection, independent verification).

**Core rule: NO HALLUCINATIONS.** No price, weight, or claim is recorded without a link to the
official source page and a check date. Values that can't be confirmed from an official source are
left **blank and flagged** on the [Flagged for Review](./site/flagged.html) page — never inferred.

## Site
- Live on GitHub Pages (this repo, `main` branch root).
- Landing dashboard: [index.html](./index.html)
- Data (single source of truth): [site/assets/data.js](./site/assets/data.js)

## Tools
- `python3 scripts/verify.py` — hallucination/security pass over all data + link check.
  Run it after every review; it recomputes every derived value and flags anything unsourced.

## Process
- Shared task board for parallel agent sessions: [COORDINATION.md](./COORDINATION.md)
- Per-source verification notes with exact quotes & URLs: `docs/verification/*.md`
