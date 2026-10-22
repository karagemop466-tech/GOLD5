# GOLD5 — Coordination Board

Shared task board for parallel agent sessions. See repo instructions for the full
coordination protocol.

## Sessions

| Session ID | Branch | Role | Scope |
|------------|--------|------|-------|
| `3c8bb7ee` | `arena/3c8bb7ee-gold5` | Research (checklist topics) | `research/*.md` |
| `3e3fae49` | `arena/3e3fae49-gold5` | Product data + site build + **final integration** | `index.html`, `assets/**`, `data/**`, `pages/**`, `README.md`, `COORDINATION.md` |

Note on branch naming: the brief asks for `session-<id>/<task>` branches. Arena pins each
session to a fixed branch and forbids switching branches, so each session uses its
Arena-assigned branch instead (`arena/<session-id>-gold5`). Logged here for transparency.

## Task board

| # | Task | Status | Owner | Files touched | Sources / verification | Irregularities |
|---|------|--------|-------|---------------|------------------------|----------------|
| 1 | Create COORDINATION.md task board | done | 3c8bb7ee | COORDINATION.md | — | None |
| 2 | Research gold purity standards (10K/14K/18K) from official sources | done | 3c8bb7ee | research/gold-purity.md | FTC consumer page; 16 CFR §23.3 (eCFR); Jewelers of America | Board originally left this "unclaimed" although the file was committed — corrected by integration session |
| 3 | Research hallmark / maker's mark requirements (official) | done | 3c8bb7ee | research/hallmarking.md | FTC; 16 CFR §23.10; 15 U.S.C. 297 | US has no mandatory pre-sale assay (flagged in doc) |
| 4 | Research gold weight (grams) measurement guidance (official) | done | 3c8bb7ee | research/weight.md | NIST OWM conversion factors; LBMA troy ounce | None |
| 5 | Research seller reputation checks (BBB/FTC official) | done | 3c8bb7ee | research/seller-reputation.md | FTC; ReportFraud.ftc.gov; NAAG | No government seller-rating DB exists (flagged in doc) |
| 6 | Research live gold price source + calculator basis (official) | done | 3c8bb7ee | research/gold-price.md | LBMA; ICE/IBA; NIST | LBMA historical tables now licence-gated (MyLBMA portal) — see flag F-01 |
| 7 | Research return policy / consumer protection (FTC official) | done | 3c8bb7ee | research/return-policy.md | FTC; 16 CFR Part 429 | Cooling-Off Rule does not cover most online sales (flagged in doc) |
| 8 | Research payment protection / credit card (official) | done | 3c8bb7ee | research/payment.md | FTC (FCBA, 15 U.S.C. 1666) | Quality disputes are not FCBA billing errors (flagged in doc) |
| 9 | Research documentation requirements | done | 3c8bb7ee | research/documentation.md | FTC; 16 CFR §23.10 | None |
| 10 | Research independent jeweler / XRF verification | needs review | 3c8bb7ee | research/verification.md | Jewelers of America; FTC; Thermo Fisher (vendor); industry blog | Doc self-reports PARTIALLY VERIFIED: XRF claims rest on vendor/industry sources, not government. Published on Flagged for Review (F-02) |
| 11 | Build site landing page | in progress | 3e3fae49 | index.html | — | Scope moved from `site/index.html` to repo root — see decision D-01 |
| 12 | Build category subpages | in progress | 3e3fae49 | pages/*.html, assets/* | — | Scope moved from `site/*.html` to `pages/` — see D-01 |
| 13 | Build data table with entries + source links | in progress | 3e3fae49 | data/*.json, data/*.csv, pages/*.html | Every row carries official source URL + capture timestamp + literal price excerpt | See D-02 (scope conflict with research/gold-price.md) |
| 13a | Verify live gold spot/benchmark price with source + timestamp | in progress | 3e3fae49 | data/gold-price.json | Kitco, CNBC, Fortune, Yahoo Finance, JMBullion cross-check; LBMA/IBA methodology | Multiple feeds disagree intraday — all values timestamped, none presented as "the" price |
| 13b | Collect + verify solid-gold engagement ring listings (brand retailers) | in progress | 3e3fae49 | data/rings.json | Official retailer product pages fetched live | Prices change constantly; each row timestamped |
| 13c | Collect + verify marketplace listings (Amazon/eBay/Etsy) | in progress | 3e3fae49 | data/rings.json | Marketplace product pages fetched live | Higher fraud risk category — flagged |
| 13d | Collect + verify NOT-solid-gold look-alikes (plated/vermeil/filled) | in progress | 3e3fae49 | data/rings.json | Official brand product pages fetched live | Included as red-flag training examples, clearly labelled |
| 14 | Build "Flagged for Review" page | in progress | 3e3fae49 | pages/flagged.html | — | — |
| 15 | Configure GitHub Pages | done | 3e3fae49 | (no file change needed) | `gh api repos/karagemop466-tech/GOLD5/pages` on 2026-10-22 | Pages was ALREADY enabled: legacy build, branch `main`, path `/`. No workflow needed — see D-01 |
| 16 | Integration: line-by-line verification, broken-link check | in progress | 3e3fae49 | all | scripts/verify.py | — |
| 17 | PR to main + merge + confirm Pages deploy | unclaimed | — | — | — | — |

## Decision log

- **D-01 (2026-10-22, session 3e3fae49):** GitHub Pages on this repo is already configured as
  `build_type: legacy`, `source: {branch: main, path: "/"}` and reports `status: built`
  (verified with `gh api repos/karagemop466-tech/GOLD5/pages`). With path `/`, the site root is
  the **repository root**, so `site/index.html` would never be served as the landing page.
  The site is therefore published from the repo root: `index.html`, `assets/`, `pages/`, `data/`.
  No `.github/workflows` file is added and the Pages config is not changed, so the two sessions
  cannot conflict on Pages settings.
- **D-02 (2026-10-22, session 3e3fae49):** `research/gold-price.md` states "No product prices are
  listed anywhere on this site (no products are reviewed or sold here)". The project brief
  explicitly requires product entries with links, current prices, and a gold-weight calculator.
  Resolution: the integration session adds a product dataset in which **every price row carries
  (a) the official retailer URL, (b) an ISO-8601 capture timestamp, and (c) the literal text
  excerpt from the fetched page that contains the price**. Any value that could not be confirmed
  from a live fetch of an official page is left blank and flagged `unverified`. No price is ever
  inferred, estimated, or carried over from a cached search snippet. `research/*.md` is owned by
  session 3c8bb7ee and was **not** edited; the change request is logged below instead.
- **D-03 (2026-10-22, session 3e3fae49):** Session 3e3fae49 merged `arena/3c8bb7ee-gold5` into its
  own branch before starting, so the research docs are preserved and included in the integration PR.
  No files owned by 3c8bb7ee were modified.

## Cross-session change requests

| # | Requested change | File (owner) | Requested by | Status |
|---|------------------|--------------|--------------|--------|
| R-01 | Update the bullet "No product prices are listed anywhere on this site" — the site now carries verified product listings with timestamps and excerpts (see D-02) | research/gold-price.md (3c8bb7ee) | 3e3fae49 | open — not edited by this session |
| R-02 | `research/weight.md` says "no products are listed on this site"; same correction applies | research/weight.md (3c8bb7ee) | 3e3fae49 | open — not edited by this session |
| R-03 | Tasks 2–10 were committed but left "unclaimed" on the board; statuses corrected by integration session after re-verifying each cited source resolves | COORDINATION.md | 3e3fae49 | done |

## Handoff / takeover log

- 2026-10-22 23:14 UTC — session 3e3fae49 started. Found `arena/3c8bb7ee-gold5` with 2 commits
  (last 23:13 UTC, i.e. active, < 60 min old). No takeover performed. Tasks 11–14 and 16 were
  unclaimed on the board and are claimed here by 3e3fae49. Task 15 found already satisfied.

Rules: claim a task by writing your session ID and file scope, commit and push the
claim immediately. Never start a task another session has claimed. Keep scopes
non-overlapping. If a session crashes or its claim is >60 minutes old with no
commits, another session may take over and note the handoff in the log. When a
task is finished, record its sources, the verification performed, and any
irregularities here and mark it done. Shared outputs (table data, index,
navigation) are changed only by the final integration session.
