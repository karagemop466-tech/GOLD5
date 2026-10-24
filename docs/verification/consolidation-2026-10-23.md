# Verification report — consolidated GOLD5 site

- Run: 2026-10-24 00:48 UTC
- Data as of: 2026-10-23
- Result: **PASS** — 23 checks passed, 0 failed

- PASS · **C1** — 25 entries, 13 sellers, 32 flags, 11 references
- PASS · **C2** — 25 listings have an https official-source URL and a dated check (data as of 2026-10-23)
- PASS · **C3** — every blank and source conflict is covered by a flag
- PASS · **C4** — spot, purity and 25 rows of derived values recompute
- PASS · **C5** — 25 listing rows, each with its official source link
- PASS · **C6** — all internal links and anchors resolve across 19 pages
- PASS · **C7** — every external link (67 registered URLs) is recorded in the dataset
- PASS · **C8** — every dollar figure on the site is dataset-sourced or computed (251 allowed values)
- PASS · **C9** — every published price, weight and source URL is rendered in its row
- PASS · **C10** — no placeholders or template leftovers
- PASS · **C11** — site/assets/data.js matches data.json
- PASS · **C12** — spot, prior spot and three raw-gold cells recompute on the gold-price page
- PASS · **C13** — 19 pages parse as well-formed HTML
- PASS · **C14** — the NO HALLUCINATIONS rule is on every page
- PASS · **C15** — no http://, javascript:, frames, third-party scripts, inline handlers or posting forms; every new-tab link is rel=noopener
- PASS · **C16** — provenance: 25 live 2026-10-23 + 0 prior rows, each prior row dated, noted and flagged
- PASS · **C17** — 7 category pages cover all 25 rows, row counts match the rules, each links back
- PASS · **C18** — consistent 12-item nav on all 19 pages and every page reachable from the dashboard
- PASS · **C19** — https sources for every row, seller policy, flag reference and official reference; 11 references dated
- PASS · **C20** — counts and row provenance labels match the dataset on all 25 listing rows
- PASS · **C21** — 46-check evidence ledger covers every row and agrees with canonical observed values
- PASS · **C22** — reader attribution: 8 rows re-read by 6d10ac0a, 17 inherited from bc4e36a1 and labelled, partial reads and failures published
- PASS · **N1-N18** — 18/18 injected errors caught by the rules they target

## What each check means

- C1 dataset integrity · C2 official source + date per listing · C3 every blank flagged
- C4 arithmetic · C5/C9 rendered rows · C6 internal links · C7 external link registry
- C8 every dollar figure sourced or computed · C10 placeholders · C11 data.js/data.json parity
- C12 published gold values · C13 HTML well-formedness · C14 no-hallucinations banner
- C15 security: https-only, rel=noopener on new tabs, no frames, third-party scripts, inline handlers or posting forms
- C16 provenance: live rows dated to this pass, prior rows dated, noted and flagged; all-live datasets are valid
- C21 evidence ledger: 46 current checks, saved excerpts and observed values agree with every canonical row
- C17 category coverage: every row appears on a category page and the row counts match the rules
- C18 navigation: the same 12-item nav everywhere and no orphan page
- C19 source discipline: https for every listing, policy, flag reference and official reference
- C20 dataset ↔ page counts and per-row provenance labels
- C22 reader attribution: every row, ledger check and page names the session that actually read the source;
  inherited same-day reads keep FL-31, partial reads and fetch failures stay published
- N1–N16 negative self-tests: injected errors must be caught, or the harness fails
  (N15 covers the single-quoted-attribute blind spot in the link/security scans;
   N16 covers a citation-scope read detached from the change request it answers;
   N17 covers a landing page claiming reads this pass did not perform;
   N18 covers a category page claiming re-reads this pass inherited)
