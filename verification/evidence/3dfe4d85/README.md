# Evidence — session `3dfe4d85` (pass 5, 2026-10-25)

Seven files, read with the platform fetch tool between 2026-10-25 03:14 and 03:40 UTC:

| File | Checks |
|---|---|
| `spot.md` | S01 — Kitco live gold price (bid $3,994.90/oz, $128.44/g, Oct 24 23:14 NY panel) |
| `retailers.md` | L01–L08 Blue Nile, L13–L15 Allurez, L16 Avianne, L17 Jewelry Master, L18 Solid Gold Jewelers |
| `etsy.md` | L19–L25 Etsy (three price drifts corrected from these captures) |
| `brilliant-earth.md` | L09–L12 — all four pages served EUR; USD price not confirmable (FL-08/FL-33) |
| `policies.md` | P01 Blue Nile returns, P02 Blue Nile warranty |
| `references.md` | why R01–R11 are inherited rather than re-read |
| `failures-and-irregularities.md` | F1–F6: every retry, failure and non-attempt, with consequences |

Canonical ledger assembled by `scripts/build_ledger_3dfe4d85.py` →
`data/live_check_3dfe4d85.json` (46 checks: 26 read by this session on 2026-10-25, 20 inherited
from 2026-10-23 and labelled, plus 2 partial reads and the failure records).

**No-hallucinations rules honoured:** every recorded value in this pass comes from a page this
session opened (or is explicitly labelled as an inherited dated observation); no value was converted
from EUR, copied from a snippet, estimated, averaged, or carried forward as if fresh; blanks stay
blank and are flagged; all derived numbers are recomputed by script from these captures.
