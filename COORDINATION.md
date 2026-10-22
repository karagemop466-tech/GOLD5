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
| T1 | Repo review & coordination setup | in progress | 638c9614 | `COORDINATION.md`, `README.md` |
| T2 | Data collection: gold spot (Kitco) + ring listings + seller policies | in progress | 638c9614 | `data/spot.json`, `data/rings.json`, `data/sellers.json`, `data/evidence/*` |
| T3 | Tools: calculator + build script + hallucination checker | in progress | 638c9614 | `tools/*` |
| T4 | Site generation (GitHub Pages, `docs/`) | in progress | 638c9614 | `docs/*` (generated), `tools/build_site.py` |
| T5 | Final integration: re-verify, link check, PR, merge, Pages deploy | unclaimed (runs after T1–T4) | — | PR only, `COORDINATION.md` |

Status values: unclaimed · in progress · done · needs review (= published on Flagged for Review page; does not block).

## Log
- 2026-10-22: Repo reviewed. Only `README.md` (`# GOLD5`) existed; no data, no site. GitHub Pages was already enabled (legacy, branch `main`, path `/`) with no content.
