---
name: libfind
description: Use when evaluating whether to reuse an open-source GitHub library or build in-house before implementing non-trivial features, modules, fixes, or code where a dependency could reduce work. Helps assess library fit, licensing, security, maintenance, supply-chain risk, compatibility, integration cost, and dependency creep.
---

# LibFind

LibFind is an advisory-only workflow for deciding whether to reuse an open-source GitHub library or build the needed code in-house. Be conservative by default: a library must clearly reduce real complexity without adding disproportionate security, license, maintenance, runtime, or integration risk.

## Advisory-Only Policy

Do not install packages.
Do not edit manifests such as `package.json`, `requirements.txt`, `pyproject.toml`, lockfiles, or project configuration.
Do not edit project code.
Do not create wrappers, adapters, migrations, or commits.

Only evaluate options, recommend or reject candidates, justify conclusions with evidence, propose install/import commands when safe, and propose manual next steps.

## Mandatory Workflow

1. Understand the requirement.
2. Inspect or infer the repository context.
3. Define the search scope.
4. Decide whether an external library search is justified.
5. If search is not justified, do not search externally. Recommend `build-it-in-house`, explain why, describe the smallest safe in-house approach, and state any production checks still needed.
6. If search is justified, gather minimum evidence before recommending anything.
7. Search for candidates only after the scope is clear enough to avoid irrelevant popular packages.
8. Apply hard rejection gates.
9. Evaluate remaining candidates with `references/rubric.md`.
10. Compare viable candidates against an in-house implementation.
11. Recommend one option or `build-it-in-house`.
12. Use the output contract in `references/output-formats.md`.
13. Provide install/import commands only if the recommendation passes all gates.
14. State what must be manually verified before production.

## Repository Context Discovery

Before searching externally, inspect or infer:

- primary language and ecosystem
- framework, runtime, and deployment constraints
- package manager and expected package registry
- project type and architecture style
- project license, if present
- existing dependencies and equivalent internal utilities
- whether the new module would be runtime, dev-only, CLI, build-time, plugin, SDK, framework extension, or reference-only

If repo context is unavailable, state the missing context and mark conclusions as provisional.

If the repo already has a small internal utility that safely solves the requirement, prefer `build-it-in-house` and explain that the existing internal path wins over a new dependency.

## Search Scope Definition

Before searching for candidates, define:

- primary language and ecosystem
- expected package registry, if any
- relevant GitHub repositories
- search keywords
- minimum required features
- optional features
- technical constraints
- license constraints
- runtime and deployment constraints
- whether small libraries are acceptable or only mature libraries should be considered

Do not search broadly before the scope is clear enough to avoid irrelevant popular packages.

## Minimum Evidence for Search-Justified Recommendations

When search is justified, review at least:

- package registry identity, if a registry package is involved
- GitHub repository identity and repo/package match
- license file or package license metadata
- release history, tags, changelog, or other maintenance signals
- security evidence such as advisories, OSV, registry alerts, or security issue handling
- install behavior, lifecycle hooks, and dependency weight when that data is available
- documentation quality and compatibility with the current stack

If browsing is unavailable or any critical evidence cannot be verified, do not fill the gap with assumptions. Use `insufficient-evidence`, explain the missing checks, and keep the conclusion provisional.

## Decide Whether Search Is Justified

Skip external library search and recommend `build-it-in-house` when the problem is simple, the implementation would be short and clear, the project only needs a tiny slice of a library, an equivalent internal utility already exists, or a dependency would add more risk than value.

Search is justified when the requirement is non-trivial, security-sensitive, standards-driven, algorithmically complex, interoperability-heavy, or already solved by mature libraries with a meaningful maintenance advantage.

This decision is a branch point. If search is skipped, do not list external candidates as evaluated and do not provide install commands. Keep the answer focused on the in-house approach, why external dependencies are unnecessary, and what must still be verified.

## Rubric Reference

Read `references/rubric.md` when search is justified or a named candidate needs comparison against an in-house implementation.

That file is the source of truth for detailed gates, scoring weights, dependency categories, category-specific heuristics, evidence checklist, and the library-vs-in-house matrix. A hard rejection from the rubric blocks recommendation even if the candidate is popular or requested by name.

## Outcome Contract

Use a stable machine-readable outcome code in English and `kebab-case`. Keep the human explanation in the user's language.

Canonical outcome codes:

- `recommended-library`
- `acceptable-alternative`
- `use-only-if-constraint-applies`
- `do-not-use`
- `build-it-in-house`
- `insufficient-evidence`

Recommended optional reason codes include:

- `simple-scope`
- `existing-internal-utility`
- `missing-license`
- `missing-provenance`
- `missing-security-evidence`
- `compatibility-mismatch`
- `dependency-weight`
- `lock-in-risk`
- `insufficient-maintenance`

If critical evidence is missing, use `insufficient-evidence` as the outcome code and explain exactly which evidence is missing. Do not invent license, security, maintenance, compatibility, or provenance data.

## Hard Rejection Gates

Reject by default when a candidate has material problems with license, security, provenance, install behavior, maintainer trust, compatibility, documentation, dependency weight, release reliability, or integration cost. Use `references/rubric.md` for the exact pass/fail gates.

## Conservative Decision Rules

- Popularity does not imply safety.
- A named package does not get a free pass because the user or team already prefers it.
- A library must clearly beat custom implementation to be recommended.
- Prefer `build-it-in-house` when the problem is simple, short, clear, or low-risk.
- Prefer `build-it-in-house` when dependency risk, size, configuration, license uncertainty, security uncertainty, or maintenance uncertainty outweighs value.
- Apply stricter scrutiny to runtime dependencies than dev dependencies or reference-only snippets.
- Treat external SDKs, plugins, framework extensions, and runtime dependencies as high-impact unless proven otherwise.

## Final Output Contract

Use `references/output-formats.md` as the exact response contract.

Always include:

- context detected
- problem to solve
- final recommendation with `Outcome code`
- key evidence and reasoning
- pending risks
- checklist before integration
- sources or evidence reviewed

Use the compact format when search is skipped, a single named candidate fails a hard gate, the repo already has an internal utility, or evidence is insufficient.

Use the full format when external search evaluates multiple candidates, the user asks for a detailed comparison, or a runtime dependency or external SDK needs a serious tradeoff analysis.

## Forward Testing

When changing decision rules, gates, or output formats, use `references/scenarios.md` for manual review. If `plugin-eval` is available, run the mirrored scenarios in `.plugin-eval/benchmark.json`.
