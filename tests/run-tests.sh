#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Golden Staff Test Runner
# Description: Executes the end-to-end full stack verification test.
# ==============================================================================

set -euo pipefail

echo "🛡️  AVIK Shield: Commencing Full Stack Golden Staff Verification 🛡️"
echo "================================================================="

# Ensure we are in the correct directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required to run the test suite."
    exit 1
fi

# Run the test suite
python3 test_full_stack.py

echo "================================================================="
echo "✅ Golden Staff Verification Complete."
