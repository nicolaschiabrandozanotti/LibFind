# LibFind Output Formats

Use these templates as the output contract for LibFind recommendations.

## Contract Rules

- Keep `Outcome code` in English and `kebab-case`.
- Keep `Reason code` in English when present.
- Write explanatory prose in the user's language.
- Omit empty sections instead of adding filler.
- Do not include install commands unless the recommendation passes all gates.

## Canonical Outcome Codes

- `recommended-library`
- `acceptable-alternative`
- `use-only-if-constraint-applies`
- `do-not-use`
- `build-it-in-house`
- `insufficient-evidence`

## Compact Format

Use this when search is skipped, a single named candidate fails a gate, an internal utility already solves the problem, or critical evidence is missing.

```markdown
## Context detected
- Language:
- Framework or runtime:
- Dependency type:

## Problem to solve
...

## Final recommendation
- Outcome code: build-it-in-house
- Recommended option: Build it in-house
- Reason code: simple-scope

## Key evidence and reasoning
...

## Pending risks
...

## Checklist before integration
- ...

## Sources or evidence reviewed
- Repo context
- Internal utilities
- External search skipped
```

## Full Format

Use this when multiple candidates were evaluated or the tradeoff is high impact.

```markdown
## Context detected
- Language:
- Framework or runtime:
- Package manager:
- Dependency type:

## Problem to solve
...

## Search scope
- Registry:
- Keywords:
- Minimum required features:
- Constraints:

## Candidates evaluated
| Candidate | Category | Outcome code | Notes |
| --- | --- | --- | --- |
| example-lib | runtime dependency | acceptable-alternative | ... |

## Comparison table
| Option | Fit | Risk | Integration cost | Verdict |
| --- | --- | --- | --- | --- |
| In-house | ... | ... | ... | ... |
| Candidate A | ... | ... | ... | ... |

## Final recommendation
- Outcome code: recommended-library
- Recommended option: example-lib
- Reason code: standards-complexity

## Rejections and reasons
- ...

## Key evidence and reasoning
...

## Pending risks
...

## Checklist before integration
- ...

## Sources or evidence reviewed
- GitHub repository
- Package registry page
- Advisory sources
- Documentation
```
