# LibFind Test Scenarios

Use these scenarios when changing LibFind behavior, output format, or evaluation criteria. They are mirrored in `.plugin-eval/benchmark.json` for measured runs when `plugin-eval` is available.

## How to Review

For each scenario, ask an agent to use `$libfind` with the user prompt. The response should satisfy every checklist item without installing packages or editing project code.

## Scenarios

| Scenario | Expected Shape | Main Risk Tested |
| --- | --- | --- |
| Trivial helper should skip search | Compact `build it in-house` answer | Dependency creep |
| Markdown sanitizer needs full comparison | Full comparison with security gates | XSS and standards complexity |
| Missing license blocks recommendation | `insufficient evidence` or rejection | License/provenance uncertainty |
| CSV import should distinguish simple and robust scope | Search justified for robust CSV parsing | Scope sensitivity |
| Cryptography should avoid custom implementation | Library search with strict security scrutiny | Unsafe in-house crypto |
| Runtime SDK requires high-impact scrutiny | Runtime/SDK risk review | Lock-in and production impact |

## Must-Pass Behaviors

- Skip external search for trivial, short, one-off implementation work.
- Search when work is security-sensitive, standards-driven, interoperability-heavy, or easy to get wrong.
- Reject candidates that fail hard gates before discussing popularity or score.
- Use compact output only when candidate/comparison sections would be empty or misleading.
- Omit install commands unless a candidate passes every gate.
- State missing critical evidence instead of filling gaps with assumptions.
