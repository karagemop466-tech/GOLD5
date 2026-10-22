# GOLD5 — Gold Engagement Ring Finder

Collects, organizes and analyzes **solid-gold engagement ring listings** against a buying checklist
(karat · explicit "solid gold" · hallmark + maker's mark · weight in grams · seller reputation · price vs. gold value ·
return/resize policy · payment · documentation · independent XRF test).

**Live site:** https://karagemop466-tech.github.io/GOLD5/  (served from `docs/`)

## ◆ NO HALLUCINATIONS RULE
Every price, weight, karat and policy was copied from the linked **official seller page** on the capture date.
Anything not confirmable there is **left blank and flagged unverified** — never guessed, estimated or inferred.
"Calculated" values are arithmetic on verified inputs (`weight × spot/gram × karat/24`).
**After every review pass run:** `python3 tools/check_hallucinations.py --log "what I reviewed"` and then `python3 tools/build_site.py`.

## Layout
| Path | What |
|---|---|
| `data/rings.json`, `sellers.json`, `spot.json`, `flags.json` | The table data (shared output — edited only by the integration session) |
| `data/evidence/*.txt` | Verbatim excerpts + source URL + capture date for every value |
| `tools/check_hallucinations.py` | Security check: every value must appear verbatim in evidence; blanks must be flagged; every `$` on the site must be sourced or registered as calculated; links must resolve |
| `tools/build_site.py` | Generates the static site into `docs/` (standard library only) and runs the check |
| `docs/` | GitHub Pages site (Dashboard, Rings, Calculator, Analysis, Sellers, Checklist, Flagged for Review, Verification, Sources) |
| `COORDINATION.md` | Shared task board for parallel sessions |

## Refreshing data
1. Re-open each listing, copy the new verbatim text into `data/evidence/<id>.txt`, update `data/rings.json` / `spot.json`.
2. `python3 tools/check_hallucinations.py --log "refresh YYYY-MM-DD"` → fix any FAIL.
3. `python3 tools/build_site.py` → commit `data/` and `docs/`.
