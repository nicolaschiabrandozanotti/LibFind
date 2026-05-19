#!/usr/bin/env python3
"""Validate LibFind skill metadata without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED_FILES = [
    "README.md",
    "SKILL.md",
    "CHANGELOG.md",
    "VERSION",
    "agents/openai.yaml",
    "references/rubric.md",
    "references/output-formats.md",
    "references/scenarios.md",
    "scripts/run_validate.ps1",
    "scripts/run_validate.sh",
    "scripts/validate_skill.py",
    ".plugin-eval/benchmark.json",
]


def _parse_simple_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(?P<body>.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("Invalid or missing YAML frontmatter delimiters")

    data: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith((" ", "\t")):
            continue

        key_match = re.match(r"^(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)$", raw_line)
        if not key_match:
            raise ValueError(f"Unsupported frontmatter line: {raw_line}")

        key = key_match.group("key")
        value = key_match.group("value").strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        data[key] = value

    return data


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _validate_required_files(skill_path: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (skill_path / relative_path).exists():
            errors.append(f"Required file not found: {relative_path}")
    return errors


def _validate_version_and_changelog(skill_path: Path) -> list[str]:
    errors: list[str] = []
    version_text = _read_text(skill_path / "VERSION").strip()
    if not SEMVER_RE.match(version_text):
        errors.append(f"VERSION must be semantic versioning (got: {version_text!r})")

    changelog_text = _read_text(skill_path / "CHANGELOG.md")
    if version_text and f"## [{version_text}]" not in changelog_text:
        errors.append(f"CHANGELOG.md missing entry for VERSION {version_text}")

    return errors


def _validate_skill_references(skill_text: str) -> list[str]:
    errors: list[str] = []
    required_mentions = [
        "references/rubric.md",
        "references/output-formats.md",
        "references/scenarios.md",
        ".plugin-eval/benchmark.json",
    ]
    for mention in required_mentions:
        if mention not in skill_text:
            errors.append(f"SKILL.md missing required reference: {mention}")
    return errors


def _validate_output_formats(skill_path: Path) -> list[str]:
    errors: list[str] = []
    output_formats = _read_text(skill_path / "references" / "output-formats.md")
    for required in ("Outcome code", "## Compact Format", "## Full Format"):
        if required not in output_formats:
            errors.append(f"references/output-formats.md missing {required!r}")
    return errors


def _validate_readme(skill_path: Path) -> list[str]:
    errors: list[str] = []
    readme_text = _read_text(skill_path / "README.md")
    for required in ("run_validate.ps1", "run_validate.sh", "py -3", "python3", "Outcome code"):
        if required not in readme_text:
            errors.append(f"README.md missing {required!r}")
    return errors


def _validate_benchmark(skill_path: Path, scenarios_text: str) -> list[str]:
    errors: list[str] = []
    benchmark_path = skill_path / ".plugin-eval" / "benchmark.json"

    try:
        benchmark_data = json.loads(_read_text(benchmark_path))
    except json.JSONDecodeError as exc:
        return [f".plugin-eval/benchmark.json is invalid JSON: {exc}"]

    commands = benchmark_data.get("verifiers", {}).get("commands")
    if commands != ["sh ./scripts/run_validate.sh ."]:
        errors.append(".plugin-eval/benchmark.json verifiers.commands must be ['sh ./scripts/run_validate.sh .']")

    scenarios = benchmark_data.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) < 3:
        errors.append(".plugin-eval/benchmark.json must define at least three scenarios")
        return errors

    ids_seen: set[str] = set()
    titles_seen: set[str] = set()
    for index, scenario in enumerate(scenarios, start=1):
        if not isinstance(scenario, dict):
            errors.append(f"Benchmark scenario {index} must be an object")
            continue

        for required in ("id", "title", "purpose", "userInput", "successChecklist"):
            if required not in scenario:
                errors.append(f"Benchmark scenario {index} missing {required}")

        scenario_id = scenario.get("id")
        if isinstance(scenario_id, str):
            if scenario_id in ids_seen:
                errors.append(f"Duplicate benchmark scenario id: {scenario_id}")
            ids_seen.add(scenario_id)

        title = scenario.get("title")
        if isinstance(title, str):
            if title in titles_seen:
                errors.append(f"Duplicate benchmark scenario title: {title}")
            titles_seen.add(title)
            if f"### {title}" not in scenarios_text:
                errors.append(f"references/scenarios.md missing detailed heading for benchmark title: {title}")

        checklist = scenario.get("successChecklist")
        if not isinstance(checklist, list) or not checklist:
            errors.append(f"Benchmark scenario {index} must include a non-empty successChecklist")

    return errors


def validate_skill(skill_path: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return ["SKILL.md not found"]

    errors.extend(_validate_required_files(skill_path))
    if errors:
        return errors

    skill_text = _read_text(skill_md)
    scenarios_text = _read_text(skill_path / "references" / "scenarios.md")

    try:
        frontmatter = _parse_simple_frontmatter(skill_text)
    except ValueError as exc:
        return [str(exc)]

    unexpected_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_FRONTMATTER_KEYS))
        unexpected = ", ".join(sorted(unexpected_keys))
        errors.append(f"Unexpected frontmatter keys: {unexpected}. Allowed: {allowed}")

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        errors.append("Missing required frontmatter key: name")
    elif not re.match(r"^[a-z0-9-]+$", name):
        errors.append("Skill name must use lowercase letters, digits, and hyphens only")
    elif name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append("Skill name cannot start/end with hyphen or contain consecutive hyphens")
    elif len(name) > MAX_NAME_LENGTH:
        errors.append(f"Skill name is too long: {len(name)} > {MAX_NAME_LENGTH}")

    if not description:
        errors.append("Missing required frontmatter key: description")
    elif "<" in description or ">" in description:
        errors.append("Description cannot contain angle brackets")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f"Description is too long: {len(description)} > {MAX_DESCRIPTION_LENGTH}")

    agent_text = _read_text(skill_path / "agents" / "openai.yaml")
    for required in ("display_name:", "short_description:", "default_prompt:"):
        if required not in agent_text:
            errors.append(f"agents/openai.yaml missing {required}")

    errors.extend(_validate_version_and_changelog(skill_path))
    errors.extend(_validate_skill_references(skill_text))
    errors.extend(_validate_output_formats(skill_path))
    errors.extend(_validate_readme(skill_path))
    errors.extend(_validate_benchmark(skill_path, scenarios_text))

    return errors


def main() -> int:
    skill_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate_skill(skill_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Skill is valid: {skill_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
