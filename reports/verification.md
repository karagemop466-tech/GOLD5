# Verification report

- Generated: 2026-10-22T23:30:17Z
- Commit: `dfb99b7`
- Assertions: 687
- Failures: 0

| Pass | What it proves | Assertions | Failures |
|---|---|---|---|
| quote | Every recorded value appears literally inside its captured quote. | 36 | 0 |
| arith | Derived values recompute exactly from their inputs and the captured spot. | 1 | 0 |
| coverage | Every blank or unstated field is represented by a flag on that row. | 34 | 0 |
| money | Every rendered $ amount traces to captured data or a printed formula. | 142 | 0 |
| flags | Flag ids resolve, and every flag references real data rows. | 91 | 0 |
| links | Internal links and anchors resolve; external URLs are well formed. | 382 | 0 |
| build | Committed HTML is byte-identical to a build from data/. | 1 | 0 |

No failures. Every value traces to a captured quote, every blank is flagged.

