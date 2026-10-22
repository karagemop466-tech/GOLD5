# COORDINATION — shared task board

> **NO HALLUCINATIONS RULE (applies to every task):** Never invent, estimate, or infer a price, weight, karat, hallmark, policy, or date.
> Every table row needs an official source link. If a value cannot be confirmed from an official source, leave it blank and flag it **unverified**.
> Every review pass ends with `python3 tools/check_hallucinations.py` — see the Flagged for Review page.

- Last updated: 2026-10-22 (UTC)
- Branch rule: this session is bound to the fixed branch `arena/638c9614-gold5` by the platform. The `session-<id>/<task>` naming scheme from the brief cannot be used here (the platform forbids creating other branches), so all tasks use this one branch. Logged here as a deviation.
- Stale-claim rule: a claim older than 60 minutes with no commits may be taken over by another session (log the handoff).

## Task board

| ID | Task | Status | Owner session | Files touched |
|----|------|--------|---------------|---------------|
| T1 | Repo review & coordination setup | done | 638c9614 | `COORDINATION.md`, `README.md` |
| T2 | Data collection: gold spot (Kitco) + ring listings + seller policies | done (items on Flagged page = needs review) | 638c9614 | `data/spot.json`, `data/rings.json`, `data/sellers.json`, `data/evidence/*` |
| T3 | Tools: calculator + build script + hallucination checker | done | 638c9614 | `tools/*` |
| T4 | Site generation (GitHub Pages, `docs/`) | done | 638c9614 | `docs/*` (generated), `tools/build_site.py` |
| T5 | Final integration: re-verify, link check, PR, merge, Pages deploy | in progress | 638c9614 | PR only, `COORDINATION.md` |

Status values: unclaimed · in progress · done · needs review (= published on Flagged for Review page; does not block).

## Log
- 2026-10-22: Repo reviewed. Only `README.md` (`# GOLD5`) existed; no data, no site. GitHub Pages was already enabled (legacy, branch `main`, path `/`) with no content.
- 2026-10-22: **T2 done.** Sources (all fetched live 2026-10-22, verbatim excerpts in `data/evidence/`): Kitco live gold price (spot bid $4,025.00/oz, 7:10 p.m. EDT); Brilliant Earth (yellow-gold listing + Freesia 2mm product page); Blue Nile (product page + returns policy); Allurez (3 product pages + return policy); Avianne & Co (product page); The Jewelry Master (product page); Solid Gold Jewelers (product page). 11 listings, 10 with a price.
  Irregularities: Kitco page shows two spot numbers ($4,025.00 bid vs $4,024.60 in body text); Brilliant Earth category text says 18K while item URLs say 14K; Pompeii3 and marquise-jewelers listings found by search were dead (excluded); Solid Gold Jewelers page shows no price although a search snippet did (price left blank); Jewelry Master "Retail Price" ≈ 2× "Special Price" (retail not used); Allurez "Everyone Else" prices not used. Full list: Flagged for Review page / `data/flags.json`.
  Not done (blank + flagged): independent reviews/complaints for every seller; payment methods; hallmark/maker's mark (no listing states one); weights for 5 listings; full Brilliant Earth / Avianne / Jewelry Master return terms.
- 2026-10-22: **T3 done.** `tools/check_hallucinations.py` negative-tested: an injected fake price, a fake weight, a fake "solid" claim, and a hand-typed `$999.99` in HTML were all caught (FAIL) and then reverted.
- 2026-10-22: **T4 done.** Site generated into `docs/`; calculator JS cross-checked against the Python calculation ($377.44 for 5 g of 14K at $4,025.00/oz).
- 2026-10-22: Hallucination pass 1 (after T2–T4): 165 checks passed, 0 FAIL, 0 WARN, 1 INFO (R09 and R10 both list 2.3 g / 14K from different sellers — flagged for independent confirmation). Recorded in `data/pass_history.json`.
- 2026-10-22: **T5 integration pass.** Re-read every row against the saved evidence and original page captures; hallucination pass 2: 0 FAIL. Internal links/anchors on all 9 pages resolve (check C8); every external link is a known source URL. Note: R02–R04 product-page URLs come from the official Brilliant Earth listing and were not individually opened (only R01's product page was) — price/karat for those come from the listing only, hence blank karat + flags.
  Limitation logged: the build sandbox can only reach GitHub/npm/PyPI hosts, so seller pages were verified at capture time via live page fetches, not re-fetched during the build.
- 2026-10-22: **PR #1 merged** (merge commit fb1a94f): https://github.com/karagemop466-tech/GOLD5/pull/1 . Attempt to switch Pages source to `main` `/docs` returned HTTP 403 (token lacks Pages-admin permission), so Pages stays on `main` `/`. Fix: root `index.html` redirect + `.nojekyll`; site is live at `/GOLD5/docs/`. Owner may optionally switch Settings → Pages → `/docs`.
