# LibFind Evaluation Rubric

Use this rubric after repository context and search scope are clear. The score helps compare candidates, but it never overrides hard rejection gates.

## Non-Negotiable Rules

- A high score never overrides a hard rejection.
- Any hard rejection blocks recommendation.
- License and critical security are gates, not score-only criteria.
- Popularity does not equal safety.
- The final result must be reasoned, not score-driven.
- If evidence is missing for license, security, maintenance, compatibility, or provenance, use `insufficient evidence`.

## Scoring Weights

| Criterion | Weight | What to Evaluate |
| --- | ---: | --- |
| Functional fit | 20 | Solves the required features directly without forcing unrelated abstractions. |
| Stack compatibility | 15 | Matches language, framework, runtime, package manager, deploy target, and project architecture. |
| Maintenance and activity | 15 | Recent meaningful releases, issue handling, maintainer responsiveness, and project maturity. |
| Security and supply chain | 20 | Advisories, package provenance, maintainer trust, install scripts, dependency tree, and suspicious activity. |
| License | Gate | Must be clear, compatible, and acceptable for expected commercial/internal use. |
| Integration cost | 10 | Setup effort, configuration, migration burden, API friction, and test impact. |
| API/documentation quality | 10 | Clear docs, examples, stable API, typed interfaces where relevant, safe usage guidance. |
| Bundle/runtime impact | 5 | Package size, transitive dependencies, runtime cost, browser/server constraints. |
| Replaceability | 5 | Lock-in, abstraction leakage, migration path, and ability to remove later. |

## Pass/Fail Gates

Fail the candidate if any gate is not satisfied:

- License is missing, ambiguous, incompatible, proprietary, paid-only, or unacceptable for expected use.
- High or critical security advisories are unresolved.
- Package provenance suggests malware, typosquatting, hijacking, or repository/package mismatch.
- Install scripts are suspicious and not justified by the package purpose.
- The API, runtime, framework, or platform is incompatible with the current project.
- The library is abandoned for a critical or runtime dependency.
- Documentation is insufficient for safe use.

## Dependency Categories

Classify each candidate before scoring:

- runtime dependency
- dev dependency
- peer dependency
- optional dependency
- CLI/tooling
- external SDK
- plugin
- framework extension
- copyable snippet/reference only

Runtime dependencies, external SDKs, plugins, and framework extensions require stricter scrutiny because they affect production behavior and long-term architecture. Dev dependencies and reference-only snippets can tolerate slightly lower maturity if they do not affect production output, but license and security gates still apply.

## Library-vs-In-House Matrix

| Factor | Prefer Library When | Prefer In-House When |
| --- | --- | --- |
| Problem complexity | Complex, standards-driven, or easy to get wrong. | Simple, short, clear implementation. |
| Module criticality | Mature library has proven correctness and clear maintenance. | Dependency failure would create unacceptable operational risk. |
| Security risk | Library is actively maintained and security-reviewed. | Candidate adds attack surface or unresolved uncertainty. |
| License risk | License is permissive and compatible. | License is missing, ambiguous, copyleft-incompatible, or paid-only. |
| Dependency weight | Size and transitive dependencies are reasonable. | Package is large or pulls broad transitive dependencies for a small need. |
| Maintenance | Maintainers respond and releases are reliable. | Package is stale, abandoned, or maintainers are risky. |
| Maturity | API is stable and widely exercised in similar contexts. | Library is experimental or churn-heavy. |
| Replaceability | Can be wrapped or removed later with low effort. | Library creates lock-in or architecture coupling. |
| Stack compatibility | Matches current runtime and deployment constraints. | Requires polyfills, runtime changes, or framework shifts. |
| Integration cost | Setup is small and aligned with existing patterns. | Integration requires architecture rewrite or heavy configuration. |
| Internal implementation cost | Building correctly would be expensive. | Internal implementation is cheap and testable. |
| Internal maintenance cost | Long-term maintenance would distract from core work. | Maintenance surface is small and owned naturally by the project. |

## Allowed Outcomes

- `recommended library`: Best option passes all gates and clearly beats in-house implementation.
- `acceptable alternative`: Passes gates but is not the strongest choice.
- `use only if constraint X applies`: Passes gates only for a specific constraint or context.
- `do not use`: Fails a gate or is materially worse than alternatives.
- `build it in-house`: Custom implementation is safer, smaller, clearer, or lower risk.
- `insufficient evidence`: Required evidence cannot be verified safely.

## Evidence Checklist

For each serious candidate, review:

- GitHub repository and package registry identity match
- license file and package metadata
- release history, tags, changelog, and commit quality
- issue/PR handling, especially security issues
- GitHub Security Advisories, OSV, registry advisories, and known CVEs where applicable
- package install scripts and lifecycle hooks
- transitive dependencies and runtime/bundle impact
- documentation quality and examples
- compatibility with current stack, runtime, and deploy target

If any essential evidence cannot be verified, do not fill the gap with assumptions.
