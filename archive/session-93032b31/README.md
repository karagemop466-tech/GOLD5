# Session `93032b31` — 24-row pass-2 dashboard (preserved verbatim)

This folder is the root dashboard published by session `93032b31` (merged in PR #10 as `b6e6a74`),
preserved when the `7cca80c9` consolidation replaced the root pages on 2026-10-22.

**Open `index.html`** to browse it. It is fully static: 24 listings, 14 sellers, 20 flags, the
12-point checklist, the calculator, and its own verification page.

What is here:

| Path | Contents |
|---|---|
| `index.html` | Landing dashboard (24 rows, spot $4,026.90/oz at 7:26 p.m. ET) |
| `listings.html` | All 24 rows, filterable |
| `sellers.html`, `gold-price.html`, `calculator.html`, `checklist.html` | Category pages |
| `analysis.html`, `verification.html`, `flagged.html`, `sources.html` | Findings and audit trail |
| `archive.html` | Its own archive page |
| `index-37e8ff42.html` | The earlier `37e8ff42` dashboard, as that session left it |
| `site/assets/dashboard.css` | The stylesheet those pages use |
| `site/assets/data.js` | The dataset its calculator loads |

**One mechanical edit only:** 23 relative links that pointed at repo-root paths (e.g.
`href="docs/index.html"`, `href="guide/index.html"`) were rewritten to `../../…` so they resolve from
this folder. No text, price, policy, listing or flag was changed.

Its 24 listings are a subset of the 25 in the consolidated dataset — the only addition in the newer
site is Blue Nile setting `203348` ($1,145). Nothing from this dashboard was dropped.
