#!/usr/bin/env bash
# AVIK Sandbox Shield — test runner
# Usage: bash tests/run-tests.sh [pytest options]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v python3 &>/dev/null; then
    echo "error: python3 not found" >&2
    exit 1
fi

if ! python3 -c "import pytest" 2>/dev/null; then
    echo "Installing pytest..."
    pip3 install --quiet pytest pyyaml
fi

echo
echo "AVIK Sandbox Shield v1.1 — Test Suite"
echo "--------------------------------------"
echo

cd "$REPO_ROOT"
python3 -m pytest tests/test_full_stack.py -v "$@"
