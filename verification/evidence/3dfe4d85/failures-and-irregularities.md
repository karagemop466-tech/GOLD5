# Fetch failures and irregularities — session `3dfe4d85`, 2026-10-25

Recorded so that nothing that did not happen is presented as if it did, and nothing that failed is
quietly skipped. All fetches in this pass used the platform `fetch_page` proxy between
2026-10-25 **03:14 and 03:40 UTC**.

## F1 — transient proxy signature errors that SUCCEEDED on retry (2 URLs)

* `https://www.etsy.com/listing/576343849/fine-14k-solid-white-gold-ring-7g-solid?show_sold_out_detail=1`
  (L25) and `https://www.bluenile.com/policies/returns` (P01) each returned
  `SignatureDoesNotMatch` from the fetch proxy on their first attempt (~03:26 UTC). Both were retried
  immediately and both succeeded; the successful reads are recorded as L25 / P01. A proxy error is
  not a dead link and was not recorded as one.

## F2 — transient proxy signature error that succeeded on the second retry (1 URL)

* `https://www.bluenile.com/services/warranty` (P02) failed twice (~03:27–03:28 UTC) and succeeded on
  the third attempt. Recorded as P02.

## F3 — Blue Nile contact page — 2 attempts, all failed (P03 **not** re-read today)

* `https://www.bluenile.com/contact-us` returned `SignatureDoesNotMatch` on both attempts
  (~03:27 and ~03:38 UTC). The canonical check stays the 2026-10-23 read and is labelled inherited;
  no contact detail was re-confirmed today.

## F4 — Brilliant Earth returns / warranty / contact — attempts failed (P04, P05, P06 not re-read)

* `https://www.brilliantearth.com/30-Day-Returns/` (P04): `SignatureDoesNotMatch` on 2 attempts
  (~03:27 and ~03:31 UTC).
* `https://www.brilliantearth.com/customer-service/warranty/#manufacturing_warranty` (P05): failed
  with the four-URL parallel batch (~03:27 UTC).
* `https://www.brilliantearth.com/contact/` (P06): not attempted after the proxy began failing
  globally at ~03:30 UTC — recorded as **not attempted**, not as a failed fetch.
* All three keep their 2026-10-23 reads, labelled inherited, with FL-33.

## F5 — Allurez policy pages — returns attempt failed; warranty/contact not attempted (P07–P09)

* `https://www.allurez.com/pages/return-policy` (P07): `SignatureDoesNotMatch` (~03:27 and ~03:36).
* `https://www.allurez.com/pages/warranty` (P08) and `…/pages/contact` (P09): not attempted after the
  proxy outage began. All three keep their 2026-10-23 reads with the inherited label and FL-33.
* Note: Allurez's return-policy *marketing block* was re-read on all three product pages today
  ("Return or exchange within 30 days if unsatisfied"), which corroborates but does not replace the
  dedicated policy page — recorded that way, with the corroboration explicitly labelled marketing.

## F6 — official references R01–R11 — not re-read today

* One attempt against `https://consumer.ftc.gov/articles/buying-platinum-gold-and-silver-jewelry`
  (R01) at ~03:36 UTC failed with the same proxy error; after that the proxy returned
  `SignatureDoesNotMatch` for **every** URL attempted (including a Blue Nile page that had served
  normally 20 minutes earlier), so the remaining ten reference URLs were **not attempted** rather
  than individually failed.
* All eleven references keep their 2026-10-23 captures (R05/§ 297 that of session `6d10ac0a`), with
  their original evidence ids and paths, labelled `readBy: <session> (inherited)`, and flagged FL-33.
  Statutory and regulatory texts do not expire daily, so the inherited label is recorded as a
  freshness caveat, not as a suspected error.

## Consequences drawn (and not drawn)

1. **No value was upgraded from an inherited read.** Every inherited check keeps its 2026-10-23 date
   everywhere it is displayed (listing rows, verification table, flag texts).
2. **No price was inferred from a search result or converted between currencies.** The four Brilliant
   Earth USD cells are the direct consequence: BE-NADIA and BE-SECRET move to `prior` rows behind
   FL-08 + FL-33 because the page served EUR today; BE-1343 and BE-1343HH keep their blank USD cells
   for the same reason.
3. **Three real price drifts were found and corrected from this pass's own captures** (ET-4366425533
   546.09 → 546.18, ET-1566052947 251.30 → 246.35, ET-1433905613 999.70 → 984.32), and the superseded
   figures are kept as dated observations in the ledger `corrections` list, not erased.
4. **Every other listing value matched exactly** — 21 of 25 listings unchanged, the 18K/14K Blue Nile
   conflict (FL-30) unchanged for a third consecutive pass, the sold-out case study still sold out.
5. The gold quote is re-confirmed, not re-based: $3,994.90/oz and $128.44/g at the newer weekend
   timestamp. Spot markets had not reopened since Friday's 5:00 PM NY close, so no derived value moved
   with the timestamp — the build still recomputed everything.
6. **Next-pass recommendation (unchanged and reinforced):** re-attempt P03–P09 and R01–R11 when the
   fetch path is healthy, re-read the four Brilliant Earth pages from a USD origin, and keep hunting
   for hallucinations after every review: `python3 scripts/verify.py` and
   `python3 tools/check_hallucinations.py`.
