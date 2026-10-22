# GOLD — Gold engagement ring research

GOLD is a source-linked research dashboard for screening online gold engagement-ring listings against the project's buyer-protection checklist. It separates seller statements from independently verified facts, dates and scopes each displayed product price, leaves unknown values blank, and publishes open issues on the **Flagged for Review** page.

## Site sections

- **Overview:** top-level no-hallucinations rule and current research status.
- **Listings:** source-linked candidate table; seller-stated claims are not proof of purity.
- **Gold calculator:** fine-gold equivalent and a simple metal-value proxy from explicit, user-supplied and source-linked inputs. No spot price is prefilled.
- **Sources:** seller, government, benchmark, and independent-review source register with scope and access dates.
- **Flagged for Review:** missing evidence and other open diligence items.

The research snapshot is dated **October 22, 2026** and currently contains two reviewed listings: a Blue Nile 14K yellow-gold *setting* with a seller-displayed $1,145 setting price, and a Quince 1 ct engagement-ring listing at $900 with a 14K gold band and platinum head. Neither currently qualifies as purchase-ready; missing values are intentionally left blank. This is not an exhaustive scan of every retailer or ring, and seller prices/options can change. See the site and source register for exact evidence, seller-return terms, independent BBB snapshots, and limitations.

## Verify and build locally

Requires Python 3 (standard library only; no package install required):

```sh
python scripts/audit.py
python scripts/build_site.py
```

The audit checks that recorded prices map to dated, scoped seller evidence; unknown product fields remain blank; sources use HTTPS on approved seller, government, benchmark, and independent-review hosts; local page references resolve; and selected static-code safety checks pass. It is a project-specific evidence/security check, not a professional penetration test or independent gold assay. The build output is written to `_site/` (ignored by Git).

## GitHub Pages

`.github/workflows/pages.yml` validates pull requests targeting `main`, and builds/deploys the static site after a push to `main`. In repository Settings → Pages, choose **GitHub Actions** as the Pages source. The workflow deploys the artifact at the repository's configured Pages URL.

## Evidence limits

Seller product and policy pages are primary evidence for what that seller states, not independent certification. The U.S. eCFR Jewelry Guides are cited as government guidance, not as proof of a particular ring's composition. A purity stamp alone is not treated as proof: have an independent jeweler professionally test the received ring and confirm its weight before wearing or resizing it. Do not enter an undated or unsourced gold quote in the calculator.
