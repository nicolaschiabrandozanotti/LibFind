# LibFind Test Scenarios

Use these scenarios when changing LibFind behavior, output format, or evaluation criteria. They are mirrored in `.plugin-eval/benchmark.json` for measured runs when `plugin-eval` is available.

## How to Review

For each scenario, ask an agent to use `$libfind` with the user prompt. The response should satisfy every checklist item without installing packages or editing project code.

## Scenario Summary

| Scenario | Expected Shape | Main Risk Tested |
| --- | --- | --- |
| Trivial helper should skip search | Compact `build it in-house` answer | Dependency creep |
| Markdown sanitizer needs full comparison | Full comparison with security gates | XSS and standards complexity |
| Missing license blocks recommendation | `insufficient evidence` or rejection | License/provenance uncertainty |
| CSV import should distinguish simple and robust scope | Search justified for robust CSV parsing | Scope sensitivity |
| Cryptography should avoid custom implementation | Library search with strict security scrutiny | Unsafe in-house crypto |
| Runtime SDK requires high-impact scrutiny | Runtime/SDK risk review | Lock-in and production impact |

## Detailed Scenarios

### Trivial helper should skip search

Prompt:

```text
Use $libfind before adding a helper that maps two boolean UI flags into one CSS class string. The implementation should be under 20 lines and only used in one component.
```

Success checklist:

- Recommends `build it in-house`.
- Explicitly says external search is not justified.
- Uses the compact format without candidate or comparison-table sections.
- Does not provide install commands.

### Markdown sanitizer needs full comparison

Prompt:

```text
Use $libfind to evaluate TypeScript libraries for rendering and sanitizing user-submitted Markdown in a Next.js app. The content is stored, rendered to other users, and XSS risk matters.
```

Success checklist:

- Defines npm/TypeScript/Next.js search scope before evaluating candidates.
- Evaluates multiple candidates with license, security, maintenance, and compatibility evidence.
- Uses the full comparison format with rejections and reasons.
- Compares the recommended library against building a parser/sanitizer in-house.

### Missing license blocks recommendation

Prompt:

```text
Use $libfind to evaluate a small GitHub package for parsing feature-flag expressions. The repository appears useful, but you cannot verify license metadata or package provenance.
```

Success checklist:

- Does not recommend the package.
- Uses the exact insufficient-evidence phrase when critical evidence is missing.
- Explains which evidence is missing.
- Does not provide install commands.

### CSV import should distinguish simple and robust scope

Prompt:

```text
Use $libfind before implementing CSV import in a Node TypeScript service. The feature must handle quoted fields, embedded newlines, large files, streaming, and clear row-level errors.
```

Success checklist:

- Treats robust CSV parsing as search-justified.
- Calls out that a tiny one-off CSV subset would be in-house, but this requirement is broader.
- Classifies candidate dependency impact correctly.
- Includes pending production checks for malformed files and large-file behavior.

### Cryptography should avoid custom implementation

Prompt:

```text
Use $libfind before implementing password hashing and signed reset tokens in a backend service. Decide whether to add a library or build the crypto pieces ourselves.
```

Success checklist:

- Treats cryptography as security-sensitive and search-justified.
- Rejects custom cryptographic primitives as the default path.
- Applies stricter security and maintenance gates.
- Separates library recommendation from final production security review.

### Runtime SDK requires high-impact scrutiny

Prompt:

```text
Use $libfind before adding a geocoding provider SDK to a serverless app. It would run in production, affect cold starts, and could lock us into one provider.
```

Success checklist:

- Classifies the candidate category as external SDK/runtime dependency.
- Applies stricter scrutiny for lock-in, bundle/runtime impact, maintenance, and provenance.
- Compares SDK use against a small direct HTTP client if the API surface is narrow.
- Lists manual checks for rate limits, retries, credentials, and provider portability.

## Must-Pass Behaviors

- Skip external search for trivial, short, one-off implementation work.
- Search when work is security-sensitive, standards-driven, interoperability-heavy, or easy to get wrong.
- Reject candidates that fail hard gates before discussing popularity or score.
- Use compact output only when candidate/comparison sections would be empty or misleading.
- Omit install commands unless a candidate passes all gates.
- State missing critical evidence instead of filling gaps with assumptions.
