# GOLD5 — Coordination Board

Shared task board for parallel agent sessions. See repo instructions for the full
coordination protocol.

Session IDs: `arena` (this session, branch `arena/3c8bb7ee-gold5`).

| # | Task | Status | Owner | Files touched | Sources / verification | Irregularities |
|---|------|--------|-------|---------------|------------------------|----------------|
| 1 | Create COORDINATION.md task board | done | arena | COORDINATION.md | — | None |
| 2 | Research gold purity standards (10K/14K/18K) from official sources | done | arena | research/gold-purity.md | FTC consumer.ftc.gov; eCFR 16 CFR 23.3; Jewelers of America | None |
| 3 | Research hallmark / maker's mark requirements (official) | done | arena | research/hallmarking.md | eCFR 16 CFR 23.10; 15 U.S.C. 297 (National Stamping Act); FTC consumer page | None |
| 4 | Research gold weight (grams) measurement guidance (official) | done | arena | research/weight.md | NIST OWM precious metals conversion (31.1034768 g = 1 troy oz) | None |
| 5 | Research seller reputation checks (BBB/FTC official) | done | arena | research/seller-reputation.md | FTC consumer page (Before You Buy); state AG / NAAG | None |
| 6 | Research live gold price source + calculator basis (official) | done | arena | research/gold-price.md | LBMA Gold Price benchmark | None |
| 7 | Research return policy / consumer protection (FTC official) | done | arena | research/return-policy.md | FTC Cooling-Off Rule 16 CFR 429; FTC consumer page | None |
| 8 | Research payment protection / credit card (official) | done | arena | research/payment.md | FTC consumer page (FCBA); 15 U.S.C. 1666 | None |
| 9 | Research documentation requirements | done | arena | research/documentation.md | FTC consumer page (Before You Buy / Report Problems) | None |
| 10 | Research independent jeweler / XRF verification | done | arena | research/verification.md | Jewelers of America find-a-jeweler; Thermo Fisher / Assay Office XRF (industry, not government) | XRF sourcing is industry/lab, not a government regulation |
| 11 | Build site landing page (index.html) | in progress | arena | site/index.html, site/css/style.css | — | None |
| 12 | Build category subpages | in progress | arena | site/*.html | — | None |
| 13 | Build data table with entries + source links | in progress | arena | site/checklist.html, site/data/entries.json | All research/*.md | None |
| 14 | Build "Flagged for Review" page | in progress | arena | site/flagged.html, site/findings.html | research/verification.md flags | Listed in research files |
| 15 | Configure GitHub Pages | unclaimed | — | .github/workflows, site | — | None |
| 16 | Integration: line-by-line verification, broken-link check | unclaimed | — | all | — | None |
| 17 | PR to main + merge + confirm Pages deploy | unclaimed | — | — | — | None |

Rules: claim a task by writing your session ID and file scope, commit and push the
claim immediately. Never start a task another session has claimed. Keep scopes
non-overlapping. If a session crashes or its claim is >60 minutes old with no
commits, another session may take over and note the handoff in the log. When a
task is finished, record its sources, verification performed, and any
irregularities here and mark it done. Shared outputs (table data, index,
navigation) are changed only by the final integration session.
