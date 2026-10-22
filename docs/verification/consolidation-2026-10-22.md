# Verification report — consolidated GOLD5 site

- Run: 2026-10-22 23:44 UTC
- Data as of: 2026-10-22
- Result: **PASS** — 15 checks passed, 0 failed

- PASS · **C1** — 25 entries, 13 sellers, 25 flags, 10 references
- PASS · **C2** — 25 listings have an https official-source URL and a 2026-10-22 check date
- PASS · **C3** — every blank is covered by a flag
- PASS · **C4** — spot, purity and 25 rows of derived values recompute
- PASS · **C5** — 25 listing rows, each with its official source link
- PASS · **C6** — all internal links and anchors resolve across 10 pages
- PASS · **C7** — every external link (65 registered URLs) is recorded in the dataset
- PASS · **C8** — every dollar figure on the site is dataset-sourced or computed (224 allowed values)
- PASS · **C9** — every published price, weight and source URL is rendered in its row
- PASS · **C10** — no placeholders or template leftovers
- PASS · **C11** — site/assets/data.js matches data.json
- PASS · **C12** — spot, prior spot and three raw-gold cells recompute on the gold-price page
- PASS · **C13** — 10 pages parse as well-formed HTML
- PASS · **C14** — the NO HALLUCINATIONS rule is on every page
- PASS · **C15** — no http://, javascript:, frames, third-party scripts, inline handlers or posting forms; every new-tab link is rel=noopener

## What each check means

- C1 dataset integrity · C2 official source + date per listing · C3 every blank flagged
- C4 arithmetic · C5/C9 rendered rows · C6 internal links · C7 external link registry
- C8 every dollar figure sourced or computed · C10 placeholders · C11 data.js/data.json parity
- C12 published gold values · C13 HTML well-formedness · C14 no-hallucinations banner
- C15 security: https-only, rel=noopener on new tabs, no frames, third-party scripts, inline handlers or posting forms
