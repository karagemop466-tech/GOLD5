# COORDINATION — Shared Task Board (GOLD5)

> **NO HALLUCINATIONS RULE (applies to every task, every session):** Never invent, estimate, or infer
> a price, weight, karat, hallmark, policy, or date. Every table row needs a source link to an official
> site. If a value cannot be confirmed from an official source, leave it **blank and flag it
> unverified** — publish it on the Flagged for Review page. Every review pass ends with the
> hallucination/security check for that session's data:
> `python3 scripts/verify.py` (root site) and `python3 tools/check_hallucinations.py` (docs/ site).

- Last updated: 2026-10-22 (UTC) — **integrated by session `37e8ff42` (final integration of this brief)**
- Branch rule (all sessions, same platform constraint): each session is bound to its fixed Arena
  branch (`arena/638c9614-gold5` / `arena/090bae73-gold5` / `arena/37e8ff42-gold5`); the
  `session-<id>/<task>` naming scheme from the brief cannot be used (the platform forbids other
  branches). Logged as a deviation by the affected sessions; non-overlapping file scopes were used instead.
- Stale-claim rule: a claim older than 60 minutes with no commits may be taken over (log the handoff).
- **Ownership of shared outputs** (site `index.html`/nav, this board, README): modified only by the
  final integration session — here, `37e8ff42`. Conflicts were resolved as **unions**: no session's
  content was discarded.

## Session registry & deliveries

| Session ID | Branch | Delivery | Merged via |
|---|---|---|---|
| `638c9614` | `arena/638c9614-gold5` | `data/` (rings/sellers/spot/flags + verbatim `evidence/*.txt`), `docs/` site, `tools/` (checker + builder) | PR #1 (`fb1a94f`) + follow-up PR #2 (`ed54ada`) |
| `090bae73` ("arena-gold5-01") | `arena/090bae73-gold5` | Checklist-format site: root `index.html` (now preserved at `index-090bae73.html`), 13 `pages/*.html` checklist subpages, `assets/css/style.css`, `assets/js/script.js` | PR #3 (`9f6caed`) |
| `37e8ff42` | `arena/37e8ff42-gold5` | **Landing dashboard** at root (`index.html` + 7 subpages: Listings, Gold Price, Calculator, Checklist, Sellers, Flagged for Review, Sources), `site/assets/data.js` (strict JSON: 14 listings, 9 sellers, 9 references, 12 flags), `scripts/verify.py`, `docs/verification/*.md` | PR #5 (this integration) |

Cross-corroboration: all sessions that captured spot prices recorded the **same Kitco snapshot**
($4,025.00/oz bid, $129.41/g, 2026-10-22 7:10 p.m. EDT) — independent agreement, no conflicts.

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

## Task board — session 090bae73 / "arena-gold5-01" (verbatim, from PR #3)

| Task ID | Description | Status | Owner | Files Touched |
|---------|-------------|--------|-------|---------------|
| T-01 | Create COORDINATION.md task board | done | arena-gold5-01 | COORDINATION.md |
| T-02 | Build project structure and landing page (index.html) | done | arena-gold5-01 | index.html, style.css, script.js |
| T-03 | Create subpages: gold-purity, solid-gold, hallmark, weight | done | arena-gold5-01 | pages/gold-purity.html, pages/solid-gold.html, pages/hallmark.html, pages/weight.html |
| T-04 | Create subpages: seller-reputation, price, return-policy, payment | done | arena-gold5-01 | pages/seller-reputation.html, pages/price.html, pages/return-policy.html, pages/payment.html |
| T-05 | Create subpages: documentation, upon-arrival, xrf-testing, calculator | done | arena-gold5-01 | pages/documentation.html, pages/upon-arrival.html, pages/xrf-testing.html, pages/calculator.html |
| T-06 | Create Flagged for Review page | done | arena-gold5-01 | pages/flagged-review.html |
| T-07 | Verify all content against official sources, add citations | done | arena-gold5-01 | All pages |
| T-08 | Set up GitHub Pages and verify build | done (merged via PR #3; status was "in progress" in their last snapshot — no further log line exists) | arena-gold5-01 | .github/workflows/, site config |
| T-09 | Create PR and merge to main | done (PR #3, `9f6caed`) | arena-gold5-01 | GitHub PR |

### Verified sources — session 090bae73 (verbatim)
- FTC Consumer Guide: https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry
- FTC Jewelry Guides (16 CFR Part 23): https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23
- Federal Register (2018 revisions): https://www.federalregister.gov/documents/2018/08/16/2018-17454/guides-for-the-jewelry-precious-metals-and-pewter-industries
- World Gold Council: https://www.gold.org/about-gold/about-gold-jewellery
- LBMA (spot price): https://www.lbma.org.uk

### Irregularities / flagged items — session 090bae73 (verbatim)
- Ring weight: cannot be confirmed without specific product listing — left blank, flagged
- Ring price: varies by seller — left blank, flagged
- Gold spot price: changes constantly — must check LBMA at time of purchase — left blank, flagged
- XRF testing cost/availability: varies by jeweler — left blank, flagged
- Gold-tone: not specifically regulated by FTC — left blank, flagged

## Task board — session 37e8ff42 (final integrator)

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
| T10 | **Integration (final)**: merge all sessions, re-verify, link check, Pages, PR + merge, log | done at PR #5 merge | 37e8ff42 | `COORDINATION.md` (log), Pages config |

### T5 note (negative result)
Walmart search HTML serves no product cards/prices (client-rendered); excluded per policy, logged in
`docs/verification/sellers.md`. No Walmart data appears anywhere — nothing was guessed.

### Log — session 37e8ff42
- 2026-10-22 (UTC): created board, claimed T1–T10 scopes. T1 done. Repo started with an empty
  skeleton at claim time (single `GOLD` commit with README only).
- 2026-10-22 (UTC) T2 done: 4 same-day spot quotes (Kitco primary $4,025.00 bid @7:10pm ET direct fetch;
  CNBC $4,083.82 9am ET; APMEX $4,077.60 11:02am ET; Kitco news ~$4,086.90 morning) — spread 1.54%,
  gram/oz math checked. Sources: kitco.com/charts/gold, cnbc.com/select, apmex.com/gold-price, kitco.com news.
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
- 2026-10-22 (UTC): **Merge conflict #1 encountered & resolved.** Session 638c9614 had merged PR #1
  (`fb1a94f`) and follow-up PR #2 (`ed54ada`, root `.nojekyll` + their `pages/` redirect work) to `main`.
  An aborted `git pull --rebase` left add/add conflicts on `COORDINATION.md` + `README.md`.
  Resolution: `git merge origin/main` with **union** of boards/logs; all of 638c9614's files
  (`data/`, `docs/`, `tools/`) taken in unmodified. Neither session's work was discarded.
  Note: 638c9614's T5 final log line (PR link/merge/Pages result) was never written; recorded here.
- 2026-10-22 (UTC): **Merge conflict #2 encountered & resolved.** While PR #5 was being merged, main
  advanced again: session 090bae73 had merged PR #3 (`9f6caed`) adding its checklist-format site at the
  root (`index.html` + `pages/*.html` + `assets/`) and replacing this board with its own. Resolution:
  `git merge origin/main`, **union** of all three sessions' boards (this file). Root `index.html` belongs
  to the final integration session per the shared-output rule, so 37e8ff42's dashboard is the landing
  page; 090bae73's root index was **preserved byte-identical at `index-090bae73.html`** (its 13
  checklist subpages remain at `pages/`, styles at `assets/` — nothing deleted or edited), and it is
  linked from the landing page and from flag F12.
- 2026-10-22 (UTC): Post-merge re-verification (integration passes): `python3 scripts/verify.py` →
  PASS (0 errors, 9 checks); DOM smoke test 20/20; local link integrity re-checked after each merge
  (all root-site links resolve; `docs/`, `pages/`, `assets/` untouched). Both checkers coexist; run
  the one matching the data you touched.
- 2026-10-22 (UTC): Pages config verified via GitHub API: source `main` branch, path `/` (legacy) →
  URL https://karagemop466-tech.github.io/GOLD5/ . After PR #5 merges, the 37e8ff42 dashboard is the
  landing page; 638c9614's site is served at /docs/ and 090bae73's checklist site at
  /index-090bae73.html + /pages/.
- 2026-10-22 (UTC): **PR #5 created** (arena/37e8ff42-gold5 → main):
  https://github.com/karagemop466-tech/GOLD5/pull/5 — **merged as `1f29d83`** (2026-10-22). Flagged
  items from all sessions remain published on their respective Flagged for Review pages and do not
  block the merge.
- 2026-10-22 (UTC): **Pages deploy confirmed.** Build for merged commit `1f29d83` = `built` (GitHub
  API `pages/builds/latest`). Live-verified after deploy:
  - https://karagemop466-tech.github.io/GOLD5/ → 37e8ff42 dashboard (landing; no-hallucinations
    banner, 4-source spot table, 14 listings, 12 flags, calculator)
  - https://karagemop466-tech.github.io/GOLD5/docs/ → 638c9614 site (11 listings, 23 flags)
  - https://karagemop466-tech.github.io/GOLD5/index-090bae73.html → 090bae73 checklist site
  Final verification state at merge: `scripts/verify.py` PASS 0 errors / 9 checks;
  `tools/check_hallucinations.py` 166 checks, 0 FAIL, 0 WARN, 1 INFO; DOM smoke test 20/20.
  **T10 complete — all tasks done; no open claims.**

## Verification policy (applies to ALL sessions)
1. A value is recorded **only** after it is read from the source page (direct fetch) or a search
   result that quotes the source page (snippet — labeled as such) — and the source URL is recorded next to it.
2. `checkedOn` date is recorded for every cell group; stale prices are re-checked before publish.
3. Derived numbers (gold content, gold value) are computed by the checkers/browser JS from raw inputs —
   never typed by hand, and recomputed at every pass.
4. Anything not confirmable from an official source → blank + flagged on the Flagged for Review page.
5. After every review: run `python3 scripts/verify.py` **and** `python3 tools/check_hallucinations.py`
   (as applicable), and log the result here.
