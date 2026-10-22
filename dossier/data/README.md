# Data dictionary — GOLD5 product dataset

All files in `data/` are generated/maintained by session `3e3fae49`.

## Verification tiers (`evidence.tier`)

| Tier | Meaning | Displayed as |
|------|---------|--------------|
| `live` | Value was read directly from a live HTTP fetch of the official product page during this session (2026-10-22 UTC). Excerpt stored in `evidence.excerpt`. | VERIFIED — LIVE |
| `snippet` | Value was read from a search-engine index snippet **of the official retailer page**, with the snippet's reported page date stored. Not re-confirmed by a live fetch (the fetch proxy was failing at capture time). | SNIPPET — CONFIRM ON PAGE |
| `unverified` | Could not be confirmed from any official source. Field left **blank**. Never inferred. | UNVERIFIED |

## Anti-hallucination rules applied to every row

1. A price is recorded ONLY if the literal price string was observed on the official
   retailer page (tier `live`) or in an index snippet of that official page (tier `snippet`).
2. The literal observed string is stored in `evidence.excerpt` so any reviewer can diff it.
3. `captured_at` is an ISO-8601 UTC timestamp of when the value was observed.
4. Missing values are `null` and rendered as blank + flagged, never estimated.
5. Weight in grams is recorded only when the seller states it on the page.
6. Currency is recorded explicitly. Rows observed in a non-USD currency are excluded
   unless a USD figure is present on the same page.
