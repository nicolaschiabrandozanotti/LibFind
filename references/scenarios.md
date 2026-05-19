# LibFind Test Scenarios

Use these scenarios when changing LibFind behavior, output format, or evaluation criteria. They are mirrored in `.plugin-eval/benchmark.json` for measured runs when `plugin-eval` is available.

## How to Review

For each scenario, ask an agent to use `$libfind` with the user prompt. The response should satisfy every checklist item without installing packages or editing project code.

## Scenario Summary

| Scenario | Expected Shape | Main Risk Tested |
| --- | --- | --- |
| Trivial helper should skip search | Compact `build-it-in-house` answer | Dependency creep |
| Markdown sanitizer needs full comparison | Full comparison with security gates | XSS and standards complexity |
| Missing license blocks recommendation | `insufficient-evidence` | License and provenance uncertainty |
| CSV import should distinguish simple and robust scope | Search justified for robust CSV parsing | Scope sensitivity |
| Cryptography should avoid custom implementation | Search justified with strict security scrutiny | Unsafe in-house crypto |
| Runtime SDK requires high-impact scrutiny | Full comparison with SDK tradeoffs | Lock-in and production impact |
| Named package still needs evidence | Compact rejection or insufficient evidence | User preference anchoring |
| Existing internal utility should block a new dependency | Compact `build-it-in-house` answer | Redundant dependency adoption |
| Dev tooling can tolerate lower scrutiny than runtime | Full or compact answer with dev classification | Over-applying runtime standards |
| Provenance mismatch should reject the candidate | Compact `do-not-use` answer | Typosquatting and package mismatch |
| No-network evaluation must stay provisional | Compact `insufficient-evidence` answer | Invented external facts |

## Detailed Scenarios

### Trivial helper should skip search

Prompt:

```text
Use $libfind before adding a helper that maps two boolean UI flags into one CSS class string. The implementation should be under 20 lines and only used in one component.
```

Success checklist:

- Includes `Outcome code: build-it-in-house`.
- Explicitly says external search is not justified.
- Uses the compact format without candidate or comparison-table sections.
- Does not provide install commands.

### Markdown sanitizer needs full comparison

Prompt:

```text
Use $libfind to evaluate TypeScript libraries for rendering and sanitizing user-submitted Markdown in a Next.js app. The content is stored, rendered to other users, and XSS risk matters.
```

Success checklist:

- Defines npm, TypeScript, and Next.js search scope before evaluating candidates.
- Evaluates multiple candidates with license, security, maintenance, and compatibility evidence.
- Uses the full comparison format with rejections and reasons.
- Compares the recommendation against building a parser or sanitizer in-house.

### Missing license blocks recommendation

Prompt:

```text
Use $libfind to evaluate a small GitHub package for parsing feature-flag expressions. The repository appears useful, but you cannot verify license metadata or package provenance.
```

Success checklist:

- Does not recommend the package.
- Includes `Outcome code: insufficient-evidence`.
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

- Classifies the candidate category as `external SDK` or runtime dependency.
- Applies stricter scrutiny for lock-in, bundle or runtime impact, maintenance, and provenance.
- Compares SDK use against a small direct HTTP client if the API surface is narrow.
- Lists manual checks for rate limits, retries, credentials, and provider portability.

### Named package still needs evidence

Prompt:

```text
Use $libfind to evaluate a GitHub package the team already wants to use for feature-flag parsing. You cannot verify the registry owner or a license file, but the package name is already in the design doc.
```

Success checklist:

- Does not treat team preference as evidence.
- Includes `Outcome code: insufficient-evidence`.
- Explains the missing provenance or license checks.
- Does not provide install commands.

### Existing internal utility should block a new dependency

Prompt:

```text
Use $libfind before adding a slugify library to this Node service. The repository already contains a small internal helper that handles the only slug format the product needs.
```

Success checklist:

- Detects that an internal utility already satisfies the requirement.
- Includes `Outcome code: build-it-in-house`.
- Keeps the answer compact and focused on the existing internal path.
- Does not provide install commands.

### Dev tooling can tolerate lower scrutiny than runtime

Prompt:

```text
Use $libfind before adding a CLI-only Markdown link checker to a docs CI job. It will not ship to production, but it still needs to be maintainable and safe to install in CI.
```

Success checklist:

- Classifies the candidate as `dev dependency` or `CLI and tooling`.
- Keeps license and security gates intact.
- States that lower maturity may be acceptable than for a runtime dependency, and explains why.
- Lists pending checks around CI fit, false positives, and maintenance.

### Provenance mismatch should reject the candidate

Prompt:

```text
Use $libfind to evaluate a package whose registry name is one character away from a popular library, and the linked GitHub repository does not match the published package metadata.
```

Success checklist:

- Rejects the candidate on provenance or typosquatting risk.
- Includes `Outcome code: do-not-use` or `Outcome code: insufficient-evidence`.
- Explains the package or repository mismatch.
- Does not provide install commands.

### No-network evaluation must stay provisional

Prompt:

```text
Use $libfind in a locked-down environment with no external network access to decide on a new dependency. You only have the repo context and the package name.
```

Success checklist:

- States that the evaluation is limited by missing external evidence.
- Includes `Outcome code: insufficient-evidence`.
- Does not invent license, security, or maintenance facts.
- Lists the exact external checks still required.

## Must-Pass Behaviors

- Skip external search for trivial, short, one-off implementation work.
- Search when work is security-sensitive, standards-driven, interoperability-heavy, or easy to get wrong.
- Reject candidates that fail hard gates before discussing popularity or score.
- Use compact output only when candidate or comparison sections would be empty or misleading.
- Use `Outcome code` values from the canonical contract.
- Omit install commands unless a candidate passes all gates.
- State missing critical evidence instead of filling gaps with assumptions.
