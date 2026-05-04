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
4. Decide whether a library search is justified.
5. If search is not justified, do not search externally. Recommend `build it in-house`, explain why, describe the smallest safe in-house approach, and state any production checks still needed.
6. If search is justified, search for candidates.
7. Apply hard rejection gates.
8. Evaluate remaining candidates with `references/rubric.md`.
9. Compare against in-house implementation.
10. Recommend one option or `build it in-house`.
11. Explain evidence and risks.
12. Provide install/import commands only if the recommendation passes all gates.
13. Provide manual integration next steps.
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

## Search Scope Definition

Before searching for candidates, define:

- primary language/ecosystem
- expected package registry, if any
- relevant GitHub repositories
- search keywords
- minimum required features
- optional features
- technical constraints
- license constraints
- runtime/deploy constraints
- whether small libraries are acceptable or only mature libraries should be considered

Do not search broadly before the scope is clear enough to avoid irrelevant popular packages.

## Decide Whether Search Is Justified

Skip external library search and recommend `build it in-house` when the problem is simple, the implementation would be short and clear, the project only needs a tiny slice of a library, or a dependency would add more risk than value.

Search is justified when the requirement is non-trivial, security-sensitive, standards-driven, algorithmically complex, interoperability-heavy, or already solved by mature libraries with a meaningful maintenance advantage.

This decision is a branch point. If search is skipped, do not list external candidates as evaluated and do not provide install commands. Keep the answer focused on the in-house approach, why external dependencies are unnecessary, and what must still be verified.

## Hard Rejection Gates

Reject by default if any candidate has:

- missing, unclear, proprietary, paid-only, or incompatible license
- incompatible strong-copyleft license for expected commercial/internal use
- unresolved high or critical security advisories
- malware, typosquatting, package hijacking, or suspicious package provenance signals
- suspicious install scripts without clear justification
- risky maintainer signals
- abandoned package for a critical/runtime dependency
- incompatible stack, runtime, framework, or API
- excessive dependency weight for the problem
- integration requiring architecture rewrite
- unreliable releases
- ignored security issues
- package/repository mismatch
- insufficient documentation for safe use

A hard rejection blocks recommendation even if the candidate is popular or scores well.

## Conservative Decision Rules

- Popularity does not imply safety.
- A library must clearly beat custom implementation to be recommended.
- Prefer `build it in-house` when the problem is simple, short, clear, or low-risk.
- Prefer `build it in-house` when dependency risk, size, configuration, license uncertainty, security uncertainty, or maintenance uncertainty outweighs value.
- Apply stricter scrutiny to runtime dependencies than dev dependencies or reference-only snippets.
- Treat external SDKs, plugins, framework extensions, and runtime dependencies as high-impact unless proven otherwise.

If evidence is missing, say exactly:

`Evidencia insuficiente para recomendar esta librería de forma segura.`

Do not invent license, security, maintenance, compatibility, or provenance data.

## Build-vs-In-House Guidance

Compare each viable candidate against a direct in-house implementation:

- problem complexity
- module criticality
- security and license risk
- dependency size and runtime/bundle impact
- maintenance frequency and maturity
- ease of replacement and lock-in
- stack compatibility
- integration cost
- cost to implement internally
- cost to maintain internally

Recommend a library only when the benefit remains clear after this comparison.

## Required Final Output Format

Use these sections in the final answer:

- Context detected
- Problem to solve
- Search scope
- Candidates evaluated
- Comparison table
- Rejections and reasons
- Final recommendation
- Why not build from scratch, or why build in-house
- Pending risks
- Install/import commands, if applicable
- Checklist before integration
- Sources/evidence reviewed

Include install/import commands only for candidates that pass all gates. If recommending `build it in-house`, omit install commands and describe the smallest safe in-house approach.
