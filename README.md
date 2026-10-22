# GOLD5 — Solid Gold Engagement Ring Research

Research project to **find gold engagement rings** that meet a strict online-buying checklist
(solid gold, karat, hallmark + maker's mark, weight in grams, seller reputation, price vs. gold
value, return/resize policy, payment protection, documentation, independent XRF test).

Two parallel agent sessions each delivered a complete, verified site + dataset. **Both are
preserved** (see the merge note in [COORDINATION.md](./COORDINATION.md)):

| Session | Site (live) | Data | Checker |
|---|---|---|---|
| `37e8ff42` (this integration) | **repo root** — https://karagemop466-tech.github.io/GOLD5/ (landing dashboard: Listings, Gold Price, Calculator, Checklist, Sellers, Flagged for Review, Sources) | [site/assets/data.js](./site/assets/data.js) (strict JSON) | `python3 scripts/verify.py` |
| `638c9614` (PR #1) | `docs/` — https://karagemop466-tech.github.io/GOLD5/docs/ (Dashboard, Rings, Calculator, Analysis, Sellers, Checklist, Flagged for Review, Verification, Sources) | [data/rings.json](./data/rings.json), `sellers.json`, `spot.json`, `flags.json` + verbatim `data/evidence/*.txt` | `python3 tools/check_hallucinations.py` |

Both datasets were captured from official pages on 2026-10-22 and **independently corroborate the
same Kitco spot snapshot** ($4,025.00/oz bid, $129.41/g, 7:10 p.m. EDT).

## ◆ NO HALLUCINATIONS RULE (applies to everything)
No price, weight, karat, hallmark, policy, or claim is recorded without a link to the **official
source page** and a check date. Anything not confirmable from an official source is **left blank
and flagged** on the respective "Flagged for Review" page — never guessed, estimated or inferred.
"Calculated" values are arithmetic on verified inputs (`weight × spot/gram × karat/24`).
**After every review pass run the checker** and record it in COORDINATION.md:
- `python3 scripts/verify.py` (root site + data)
- `python3 tools/check_hallucinations.py --log "what I reviewed"` (docs/ site + data)

## Layout (session 638c9614 files, preserved as-is)
| Path | What |
|---|---|
| `data/rings.json`, `sellers.json`, `spot.json`, `flags.json` | Table data for the `docs/` site (shared output — edited only by the integration session) |
| `data/evidence/*.txt` | Verbatim excerpts + source URL + capture date for every value |
| `tools/check_hallucinations.py` | Security check: every value must appear verbatim in evidence; blanks must be flagged; every `$` on the site must be sourced or registered as calculated; links must resolve |
| `tools/build_site.py` | Generates the static site into `docs/` (standard library only) and runs the check |
| `docs/` | GitHub Pages site of session 638c9614 |
| `index.html`, `site/**` | GitHub Pages site (landing) of session 37e8ff42 |
| `scripts/verify.py` | Hallucination + link + arithmetic pass for the root site/data |
| `docs/verification/*.md` | Per-source verification notes with exact quotes & URLs (session 37e8ff42) |
| `COORDINATION.md` | Shared task board for parallel sessions |

## Refreshing data
1. Re-open each listing, copy the new verbatim text into the session's evidence store
   (`data/evidence/<id>.txt` for the docs/ site; quote+URL entries in `site/assets/data.js` +
   `docs/verification/*.md` for the root site).
2. Run the matching checker → fix any FAIL.
3. For the docs/ site: `python3 tools/build_site.py` → commit `data/` and `docs/`.
4. Update the log in [COORDINATION.md](./COORDINATION.md).
