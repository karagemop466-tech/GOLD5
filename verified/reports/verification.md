# Verification report

- Generated: 2026-10-22T23:53:53Z
- Commit: `1c7213f`
- Assertions: 896
- Failures: 0

| Pass | What it proves | Assertions | Failures |
|---|---|---|---|
| quote | Every recorded value appears literally inside its captured quote. | 48 | 0 |
| arith | Derived values recompute exactly from their inputs and the captured spot. | 3 | 0 |
| coverage | Every blank or unstated field is represented by a flag on that row. | 46 | 0 |
| money | Every rendered $ amount traces to captured data or a printed formula. | 195 | 0 |
| flags | Flag ids resolve, and every flag references real data rows. | 113 | 0 |
| links | Internal links and anchors resolve; external URLs are well formed. | 478 | 0 |
| checklist | A checklist item may only be marked covered when coverage is complete. | 12 | 0 |
| build | Committed HTML is byte-identical to a build from data/. | 1 | 0 |

No failures. Every value traces to a captured quote, every blank is flagged.

