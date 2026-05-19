#!/usr/bin/env sh
set -eu

TARGET="${1:-.}"

if command -v python3 >/dev/null 2>&1; then
  exec python3 scripts/validate_skill.py "$TARGET"
fi

if command -v python >/dev/null 2>&1; then
  exec python scripts/validate_skill.py "$TARGET"
fi

echo "Python 3 was not found in PATH." >&2
exit 1
