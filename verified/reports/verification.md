# Verification report

- Generated: 2026-10-22T23:34:57Z
- Commit: `8265d73`
- Assertions: 896
- Failures: 11

| Pass | What it proves | Assertions | Failures |
|---|---|---|---|
| quote | Every recorded value appears literally inside its captured quote. | 48 | 0 |
| arith | Derived values recompute exactly from their inputs and the captured spot. | 3 | 0 |
| coverage | Every blank or unstated field is represented by a flag on that row. | 46 | 0 |
| money | Every rendered $ amount traces to captured data or a printed formula. | 195 | 0 |
| flags | Flag ids resolve, and every flag references real data rows. | 113 | 0 |
| links | Internal links and anchors resolve; external URLs are well formed. | 478 | 11 |
| checklist | A checklist item may only be marked covered when coverage is complete. | 12 | 0 |
| build | Committed HTML is byte-identical to a build from data/. | 1 | 0 |

## Failures

- [links] index.html: broken link ../index.html
- [links] 18k.html: broken link ../../index.html
- [links] all-rings.html: broken link ../../index.html
- [links] complete-rings.html: broken link ../../index.html
- [links] flagged.html: broken link ../../index.html
- [links] gold-bands.html: broken link ../../index.html
- [links] halo-pave.html: broken link ../../index.html
- [links] method.html: broken link ../../index.html
- [links] prices.html: broken link ../../index.html
- [links] sellers.html: broken link ../../index.html
- [links] solitaires.html: broken link ../../index.html
