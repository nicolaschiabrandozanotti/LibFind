#!/usr/bin/env python3
"""Validate LibFind skill metadata without third-party dependencies."""

from __future__ import annotations

import re
import sys
import json
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


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


def validate_skill(skill_path: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return ["SKILL.md not found"]

    try:
        frontmatter = _parse_simple_frontmatter(skill_md.read_text(encoding="utf-8"))
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

    agent_metadata = skill_path / "agents" / "openai.yaml"
    if agent_metadata.exists():
        agent_text = agent_metadata.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "default_prompt:"):
            if required not in agent_text:
                errors.append(f"agents/openai.yaml missing {required}")

    benchmark = skill_path / ".plugin-eval" / "benchmark.json"
    if benchmark.exists():
        try:
            benchmark_data = json.loads(benchmark.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f".plugin-eval/benchmark.json is invalid JSON: {exc}")
        else:
            scenarios = benchmark_data.get("scenarios")
            if not isinstance(scenarios, list) or len(scenarios) < 3:
                errors.append(".plugin-eval/benchmark.json must define at least three scenarios")
            else:
                for index, scenario in enumerate(scenarios, start=1):
                    if not isinstance(scenario, dict):
                        errors.append(f"Benchmark scenario {index} must be an object")
                        continue
                    for required in ("id", "title", "purpose", "userInput", "successChecklist"):
                        if required not in scenario:
                            errors.append(f"Benchmark scenario {index} missing {required}")
                    checklist = scenario.get("successChecklist")
                    if not isinstance(checklist, list) or not checklist:
                        errors.append(f"Benchmark scenario {index} must include a non-empty successChecklist")

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
