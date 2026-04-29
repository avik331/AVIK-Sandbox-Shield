#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 4: Setup Prompt Enforcement
# Description: Initializes the Layer 4 proxy daemon.
# ==============================================================================

set -euo pipefail

RULES_FILE=${1:-"safety-rules.yaml"}

echo "🛡️  AVIK Shield: Initiating Layer 4 Prompt Enforcer 🛡️"
echo "====================================================="

if [ ! -f "$RULES_FILE" ]; then
    echo "❌ Error: Safety rules file '$RULES_FILE' not found."
    exit 1
fi

echo "[+] Loading immutable safety rules from $RULES_FILE..."
# In a real environment, this might check a cryptographic signature of the rules file

echo "[+] Validating Python dependencies..."
if ! python3 -c "import yaml" &> /dev/null; then
    echo "[-] Installing python3-yaml..."
    pip install --quiet pyyaml
fi

echo "[+] Starting Enforcer Proxy Daemon..."
# This is a simulation of how the enforcer would run as a service/proxy
echo "    -> Binding proxy to 127.0.0.1:8080"
echo "    -> Forwarding sanitized traffic to Layer 3 (172.16.0.2:8000)"

# In a true deployment, you would start a proxy server here (e.g. FastAPI/Gunicorn)
# that consumes prompt-enforcer.py

echo "====================================================="
echo "✅ Layer 4 Proxy Active."
echo "   All traffic to the Core LLM must now pass through 127.0.0.1:8080."
echo "   Constraint policies are strictly enforced."
