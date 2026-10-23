# Verification report — consolidated GOLD5 site

- Run: 2026-10-23 20:25 UTC
- Data as of: 2026-10-23
- Result: **PASS** — 21 checks passed, 0 failed

- PASS · **C1** — 25 entries, 13 sellers, 29 flags, 11 references
- PASS · **C2** — 25 listings have an https official-source URL and a dated check (2026-10-22 or 2026-10-23)
- PASS · **C3** — every blank is covered by a flag
- PASS · **C4** — spot, purity and 25 rows of derived values recompute
- PASS · **C5** — 25 listing rows, each with its official source link
- PASS · **C6** — all internal links and anchors resolve across 19 pages
- PASS · **C7** — every external link (66 registered URLs) is recorded in the dataset
- PASS · **C8** — every dollar figure on the site is dataset-sourced or computed (233 allowed values)
- PASS · **C9** — every published price, weight and source URL is rendered in its row
- PASS · **C10** — no placeholders or template leftovers
- PASS · **C11** — site/assets/data.js matches data.json
- PASS · **C12** — spot, prior spot and three raw-gold cells recompute on the gold-price page
- PASS · **C13** — 19 pages parse as well-formed HTML
- PASS · **C14** — the NO HALLUCINATIONS rule is on every page
- PASS · **C15** — no http://, javascript:, frames, third-party scripts, inline handlers or posting forms; every new-tab link is rel=noopener
- PASS · **C16** — provenance: all 25 rows carry checkedOn=2026-10-23 and provenance=live
- PASS · **C17** — 7 category pages cover all 25 rows, row counts match the rules, each links back
- PASS · **C18** — consistent 12-item nav on all 19 pages and every page reachable from the dashboard
- PASS · **C19** — https sources for every row, seller policy, flag reference and official reference; 11 references dated
- PASS · **C20** — counts and row provenance labels match the dataset on all 25 listing rows
- PASS · **N1-N8** — 8/8 injected errors caught by the rules they target

## What each check means

- C1 dataset integrity · C2 official source + date per listing · C3 every blank flagged
- C4 arithmetic · C5/C9 rendered rows · C6 internal links · C7 external link registry
- C8 every dollar figure sourced or computed · C10 placeholders · C11 data.js/data.json parity
- C12 published gold values · C13 HTML well-formedness · C14 no-hallucinations banner
- C15 security: https-only, rel=noopener on new tabs, no frames, third-party scripts, inline handlers or posting forms
- C16 provenance: live rows dated to this pass, prior rows dated, noted and flagged (FL-26/27/28)
- C17 category coverage: every row appears on a category page and the row counts match the rules
- C18 navigation: the same 12-item nav everywhere and no orphan page
- C19 source discipline: https for every listing, policy, flag reference and official reference
- C20 dataset ↔ page counts and per-row provenance labels
- N1–N8 negative self-tests: injected errors must be caught, or the harness fails
