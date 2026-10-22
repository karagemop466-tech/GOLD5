# Coordination Board — GOLD5

Shared task board for parallel agent sessions. Last updated: **2026-10-22 (UTC)**.

## Session registry

| Session ID | Branch (platform-fixed) | Status | Notes |
|---|---|---|---|
| `arena-84be683f` | `arena/84be683f-gold5` | active | Only session detected on 2026-10-22: `git branch -a` shows no `session-*` branches, 0 open/closed PRs, 0 issues. This session is therefore also the final integration session (documented below). |

> **Branch-name note:** the platform fixes this session's working branch as `arena/84be683f-gold5`. The
> generic `session-<id>/<task>` convention cannot be used because the session branch is immutable.
> Ownership is therefore recorded by session ID below, and this session only ever commits to
> `arena/84be683f-gold5`.

## Task board

| # | Task | Status | Owner | File scope | Notes / sources |
|---|---|---|---|---|---|
| T1 | Repo review + task board bootstrap | **done** (2026-10-22) | arena-84be683f | `COORDINATION.md`, `README.md` | Repo had only a 1-line README at `dfb99b7`. No other sessions, no PRs, no issues. |
| T2 | Gold price reference log (spot, date, source URL) | **in progress** | arena-84be683f | `data/gold-prices.json`, `pages/prices.html` | Sources: Gold-API `XAU` quote, APMEX spot page, World Gold Council spot page. |
| T3 | Seller due-diligence dataset (contact + return policy + independent complaints) | **in progress** | arena-84be683f | `data/sellers.json`, `pages/sellers.html` | Sources: seller policy/contact pages, BBB profiles, FTC guidance. |
| T4 | Ring entry dataset (karat, solid-gold wording, hallmark, grams, price, URL, evidence) | **in progress** | arena-84be683f | `data/entries.json` | Every field needs a verbatim quote + official URL. Blank + flag when absent. |
| T5 | Site build (landing + category subpages + flagged page + methodology) | **unclaimed** | — | `index.html`, `pages/*.html`, `assets/*`, `scripts/build_site.py` | Will be claimed by arena-84be683f after T2–T4 pass 1. Shared nav/index only changed by the integration session. |
| T6 | Verification harness + hallucination security passes | **unclaimed** | — | `scripts/verify.py`, `reports/*`, `.github/workflows/ci.yml` | Anti-hallucination rule: every recorded value must be a substring of its captured evidence quote. |
| T7 | Final integration: merge, link check, publish to GitHub Pages, record PR | **unclaimed** | — | all | Only session present ⇒ this session performs it at the end. |

## Change log

- **2026-10-22** — `arena-84be683f` created this board, claimed T1–T4 and (later) T5–T7. No conflicts:
  no other branch, PR, issue or coordination file existed. T1 marked done.
- **2026-10-22** — Verified `jamesallen.com` now redirects to `bluenile.com` ("James Allen is Now Part of
  Blue Nile", https://www.bluenile.com/james-allen). Any James Allen setting is therefore recorded with
  its canonical `bluenile.com` URL. Flagged in `data/flags.json` (F-001).
