# Changelog

## [0.2.0] - 2026-05-04

### Changed

- Clarified that the library search decision is a real branch in the workflow.
- Added an explicit no-search path that recommends `build it in-house` without evaluating external candidates.
- Reduced duplicated gate and build-vs-in-house detail in `SKILL.md` by making `references/rubric.md` the detailed source of truth.
- Replaced the single mandatory final-answer format with bounded full and compact formats.
- Replaced the personal validation path in `README.md` with a portable local validator.
- Added LibFind benchmark scenarios and manual scenario guidance for future behavior checks.

### Fixed

- Updated remaining `README.md` validation references to use the local validator.
- Expanded manual scenario docs with full prompts and success checklists.
- Added the local skill validator as a `plugin-eval` benchmark verifier command.

## [0.1.0] - 2026-05-03

### Added

- Initial advisory-only LibFind skill.
- Conservative library evaluation workflow.
- Build-vs-in-house decision rules.
- License, security, maintenance, and compatibility gates.
- Rubric for reusable open-source library evaluation.
- OpenAI agent metadata.
