# COORDINATION — Shared Task Board (GOLD5)

> **NO HALLUCINATIONS RULE (applies to every task, every session):** Never invent, estimate, or infer
> a price, weight, karat, hallmark, policy, or date. Every table row needs a source link to an official
> site. If a value cannot be confirmed from an official source, leave it **blank and flag it
> unverified** — publish it on the Flagged for Review page. Every review pass ends with the
> hallucination/security check for that session's data:
> `python3 scripts/verify.py` (root site) and `python3 tools/check_hallucinations.py` (docs/ site).

- Last updated: 2026-10-22 (UTC) — **integrated by session `37e8ff42` after merging `638c9614` (PR #1)**
- Branch rule (both sessions, same platform constraint): each session is bound to its fixed Arena
  branch (`arena/638c9614-gold5` / `arena/37e8ff42-gold5`); the `session-<id>/<task>` naming scheme
  from the brief cannot be used (the platform forbids other branches). Logged as a deviation by both
  sessions; non-overlapping file scopes were used instead.
- Stale-claim rule: a claim older than 60 minutes with no commits may be taken over (log the handoff).

## Session registry

| Session ID | Branch | Delivered |
|---|---|---|
| `638c9614` | `arena/638c9614-gold5` | `data/`, `docs/` site, `tools/`, PR #1 (merged as `fb1a94f`) |
| `37e8ff42` | `arena/37e8ff42-gold5` | root site (`index.html`, `site/**`), `scripts/verify.py`, `docs/verification/`, PR #2 |

## Task board — session 638c9614 (verbatim, from PR #1)

| ID | Task | Status | Owner session | Files touched |
|----|------|--------|---------------|---------------|
| T1 | Repo review & coordination setup | done | 638c9614 | `COORDINATION.md`, `README.md` |
| T2 | Data collection: gold spot (Kitco) + ring listings + seller policies | done (items on Flagged page = needs review) | 638c9614 | `data/spot.json`, `data/rings.json`, `data/sellers.json`, `data/evidence/*` |
| T3 | Tools: calculator + build script + hallucination checker | done | 638c9614 | `tools/*` |
| T4 | Site generation (GitHub Pages, `docs/`) | done | 638c9614 | `docs/*` (generated), `tools/build_site.py` |
| T5 | Final integration: re-verify, link check, PR, merge, Pages deploy | done (merged as `fb1a94f` — final log line was never written; recorded here by 37e8ff42) | 638c9614 | PR #1 only, `COORDINATION.md` |

Status values: unclaimed · in progress · done · needs review (= published on Flagged for Review page; does not block).

### Log — session 638c9614 (verbatim, from PR #1)
- 2026-10-22: Repo reviewed. Only `README.md` (`# GOLD5`) existed; no data, no site. GitHub Pages was already enabled (legacy, branch `main`, path `/`) with no content.
- 2026-10-22: **T2 done.** Sources (all fetched live 2026-10-22, verbatim excerpts in `data/evidence/`): Kitco live gold price (spot bid $4,025.00/oz, 7:10 p.m. EDT); Brilliant Earth (yellow-gold listing + Freesia 2mm product page); Blue Nile (product page + returns policy); Allurez (3 product pages + return policy); Avianne & Co (product page); The Jewelry Master (product page); Solid Gold Jewelers (product page). 11 listings, 10 with a price.
  Irregularities: Kitco page shows two spot numbers ($4,025.00 bid vs $4,024.60 in body text); Brilliant Earth category text says 18K while item URLs say 14K; Pompeii3 and marquise-jewelers listings found by search were dead (excluded); Solid Gold Jewelers page shows no price although a search snippet did (price left blank); Jewelry Master "Retail Price" ≈ 2× "Special Price" (retail not used); Allurez "Everyone Else" prices not used. Full list: Flagged for Review page / `data/flags.json`.
  Not done (blank + flagged): independent reviews/complaints for every seller; payment methods; hallmark/maker's mark (no listing states one); weights for 5 listings; full Brilliant Earth / Avianne / Jewelry Master return terms.
- 2026-10-22: **T3 done.** `tools/check_hallucinations.py` negative-tested: an injected fake price, a fake weight, a fake "solid" claim, and a hand-typed `$999.99` in HTML were all caught (FAIL) and then reverted.
- 2026-10-22: **T4 done.** Site generated into `docs/`; calculator JS cross-checked against the Python calculation ($377.44 for 5 g of 14K at $4,025.00/oz).
- 2026-10-22: Hallucination pass 1 (after T2–T4): 165 checks passed, 0 FAIL, 0 WARN, 1 INFO (R09 and R10 both list 2.3 g / 14K from different sellers — flagged for independent confirmation). Recorded in `data/pass_history.json`.
- 2026-10-22: **T5 integration pass.** Re-read every row against the saved evidence and original page captures; hallucination pass 2: 0 FAIL. Internal links/anchors on all 9 pages resolve (check C8); every external link is a known source URL. Note: R02–R04 product-page URLs come from the official Brilliant Earth listing and were not individually opened (only R01's product page was) — price/karat for those come from the listing only, hence blank karat + flags.
  Limitation logged: the build sandbox can only reach GitHub/npm/PyPI hosts, so seller pages were verified at capture time via live page fetches, not re-fetched during the build.

## Task board — session 37e8ff42

| ID | Task | Status | Owner | File scope (exclusive) |
|---|---|---|---|---|
| T1 | Create COORDINATION.md task board + baseline docs | done | 37e8ff42 | `COORDINATION.md`, `README.md` |
| T2 | Verify gold spot price from official sources (dated quotes) | done | 37e8ff42 | `site/assets/data.js` (spot section), `docs/verification/gold-price.md` |
| T3 | Collect & verify Blue Nile 14K/18K engagement-ring listings + seller facts | done | 37e8ff42 | `site/assets/data.js` (blue-nile entries), `docs/verification/bluenile.md` |
| T4 | Collect & verify Etsy solid-gold listings (grams + price + hallmark) | done | 37e8ff42 | `site/assets/data.js` (etsy entries), `docs/verification/etsy.md` |
| T5 | Collect & verify Walmart 14K solid gold listings (if fetchable) | done (negative) | 37e8ff42 | `docs/verification/sellers.md` (fetch log) |
| T6 | Verify seller facts: contact, return policy, payment, reputation links | done | 37e8ff42 | `site/assets/data.js` (sellers), `docs/verification/sellers.md` |
| T7 | Reference material: checklist, karat/fineness, FTC hallmark guidance (linked) | done | 37e8ff42 | `docs/verification/references.md`, site page content for guides |
| T8 | Build GitHub Pages site (index + subpages + calculator + styles) | done | 37e8ff42 | `index.html`, `site/**` (non-data), `assets/**` |
| T9 | Hallucination/security verification harness + run passes | done | 37e8ff42 | `scripts/verify.py`, `docs/verification/report.md` |
| T10 | **Integration (final)**: merge both sessions, re-verify, link check, Pages, PR + merge, log | in progress → done at merge | 37e8ff42 | `COORDINATION.md` (log), Pages config |

### T5 note (negative result)
Walmart search HTML serves no product cards/prices (client-rendered); excluded per policy, logged in
`docs/verification/sellers.md`. No Walmart data appears anywhere — nothing was guessed.

### Log — session 37e8ff42
- 2026-10-22 (UTC): created board, claimed T1–T10 scopes. T1 done. Repo started with an empty
  skeleton at claim time (single `GOLD` commit with README only).
- 2026-10-22 (UTC) T2 done: 4 same-day spot quotes (Kitco primary $4,025.00 bid @7:10pm ET direct fetch;
  CNBC $4,083.82 9am ET; APMEX $4,077.60 11:02am ET; Kitco news ~$4,086.90 morning) — spread 1.54%,
  gram/oz math checked. Sources: kitco.com/charts/gold, cnbc.com/select, apmex.com/gold-price, kitco.com news.
  **Cross-session corroboration:** session 638c9614's `data/spot.json` captured the identical Kitco
  snapshot ($4,025.00 bid, $129.41/g, 7:10 p.m. EDT, same purity table) — independent, no conflict.
- 2026-10-22 (UTC) T3 done: 7 Blue Nile 14K/18K settings verified on product/category pages
  ($870–$2,320, all "setting price"); returns policy (30-day, resized/engraved/custom excluded),
  warranty (eff. 2026-10-11, lifetime ≥$1,000, free resize ≤6mo), contact (1-800-242-2728,
  service@bluenile.com), BBB (A+ since 1999, 121 complaints/3yr, BBB reviews 1/5×25,
  ConsumerAffairs 1.7/5×172). Gram weights not published → blank + F3.
- 2026-10-22 (UTC) T4 done: 8 Etsy shops / 7 active listings + 1 sold case study verified on
  listing pages (RAKSHAKJEWELS 14K $1,891.78 IGI 2.50ct; ForeverForLove 14K from $547.26;
  VeraByEden 14K $969.00 + 3.70g via snippet + off-platform-photos flag F2; VibrantStone from $251.30;
  adelafinejewels 14K $999.70+; Cittali from $195.75; case study 7g 14K at $444.80 = 0.84× melt → F1).
- 2026-10-22 (UTC) T6/T7 done: seller profiles + official references (FTC consumer article fetched
  direct; 16 CFR Part 23 eCFR; Cornell LII §23.3; FTC FRN PDF; Etsy Purchase Protection; JVC;
  ReportFraud).
- 2026-10-22 (UTC) T8/T9 done: site built (8 pages, data-driven, calculator, no build step, no
  external deps). Harness `scripts/verify.py`: PASS 0 errors / 9 checks (sources, dates, domain
  allowlist, spot math, purity math, derived-ratio recompute, flag cross-refs, local link integrity).
  DOM smoke test: 20/20 passed.

### Log — merge & final integration (session 37e8ff42)
- 2026-10-22 (UTC): **Merge conflict encountered & resolved.** While pushing, session 37e8ff42 discovered
  that session 638c9614 had already merged its full delivery to `main` as PR #1 (`fb1a94f`). An aborted
  `git pull --rebase` left a conflict on `COORDINATION.md` + `README.md` (add/add). Resolution:
  `git merge origin/main` with **union** of both boards/logs (this file) and a merged README preserving
  both sessions' descriptions; all of 638c9614's files (`data/`, `docs/`, `tools/`) taken in unmodified.
  Neither session's work was discarded. Note: 638c9614's T5 final log line (PR link/merge/Pages result)
  was never written; the merge is recorded here instead.
- 2026-10-22 (UTC): Post-merge re-verification (integration pass): `python3 scripts/verify.py` → PASS
  (0 errors, 9 checks) on root data; DOM smoke test 20/20; local link integrity re-checked after merge
  (all root-site links resolve; `docs/` site untouched). Both checkers now coexist; run the one matching
  the data you touched.
- 2026-10-22 (UTC): Pages config verified via GitHub API: source `main` branch, path `/` (legacy) →
  URL https://karagemop466-tech.github.io/GOLD5/ . After this branch merges, the root site becomes the
  landing page; the 638c9614 site remains fully served at https://karagemop466-tech.github.io/GOLD5/docs/ .
- 2026-10-22 (UTC): **PR #2 created** (this branch → main): https://github.com/karagemop466-tech/GOLD5/pull/2 — merged: (recorded at merge). Flagged items from both sessions remain published on their respective Flagged for Review pages and do not block the merge.

## Verification policy (applies to ALL sessions)
1. A value is recorded **only** after it is read from the source page (direct fetch) or a search
   result that quotes the source page (snippet — labeled as such) — and the source URL is recorded next to it.
2. `checkedOn` date is recorded for every cell group; stale prices are re-checked before publish.
3. Derived numbers (gold content, gold value) are computed by the checkers/browser JS from raw inputs —
   never typed by hand, and recomputed at every pass.
4. Anything not confirmable from an official source → blank + flagged on the Flagged for Review page.
5. After every review: run `python3 scripts/verify.py` **and** `python3 tools/check_hallucinations.py`
   (as applicable), and log the result here.
