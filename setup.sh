#!/usr/bin/env bash
# AVIK Sandbox Shield — first-run setup
# Usage: bash setup.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()  { echo "  $*"; }
ok()    { echo "  [ok] $*"; }
fail()  { echo "  [error] $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 1. Python dependencies
# ---------------------------------------------------------------------------

echo
echo "AVIK Sandbox Shield v1.1 — Setup"
echo "---------------------------------"
echo

echo "[1/4] Installing Python dependencies..."
if command -v pip3 &>/dev/null; then
    pip3 install --quiet pyyaml
    ok "pyyaml installed"
else
    fail "pip3 not found. Install Python 3.9+ and try again."
fi

# ---------------------------------------------------------------------------
# 2. Runtime directories
# ---------------------------------------------------------------------------

echo "[2/4] Creating runtime directories..."

DATA_DIR="/var/lib/avik-shield"
KEY_DIR="/etc/avik/keys"
FALLBACK_KEY_DIR="$HOME/.avik/keys"
LOG_DIR="/var/log/avik-shield"

for dir in "$DATA_DIR" "$KEY_DIR" "$LOG_DIR"; do
    if mkdir -p "$dir" 2>/dev/null; then
        ok "$dir"
    else
        info "$dir not writable — using fallback locations"
        mkdir -p "$FALLBACK_KEY_DIR"
        ok "$FALLBACK_KEY_DIR (fallback)"
        break
    fi
done

# ---------------------------------------------------------------------------
# 3. Cryptographic keys
# ---------------------------------------------------------------------------

echo "[3/4] Generating cryptographic keys..."
bash "$SCRIPTS_DIR/generate-keys.sh"

# ---------------------------------------------------------------------------
# 4. Script permissions
# ---------------------------------------------------------------------------

echo "[4/4] Setting executable permissions..."

find "$REPO_ROOT" -name "*.sh" -exec chmod +x {} \;
chmod +x "$REPO_ROOT/avik-shield.py"
ok "Done"

# ---------------------------------------------------------------------------
# Next steps
# ---------------------------------------------------------------------------

echo
echo "---------------------------------"
echo "Setup complete."
echo
echo "Next steps:"
echo "  1. Review config:   $REPO_ROOT/config.yaml"
echo "  2. Verify system:   python3 avik-shield.py verify"
echo "  3. Start shield:    python3 avik-shield.py start"
echo "  4. Monitor:         python3 avik-shield.py monitor"
echo
echo "For emergency shutdown: python3 avik-shield.py kill"
echo
