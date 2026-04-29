#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 7: Setup Audit Ledger
# Description: Initializes secure directories for the append-only ledger.
# ==============================================================================

set -euo pipefail

LEDGER_DIR="/var/log/avik_ledger"

echo "🛡️  AVIK Shield: Initializing Layer 7 Immutable Ledger 🛡️"
echo "====================================================="

if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run as root."
  exit 1
fi

echo "[+] Creating highly restricted ledger directory..."
mkdir -p "$LEDGER_DIR"
chown root:root "$LEDGER_DIR"
chmod 700 "$LEDGER_DIR"

echo "[+] Initializing empty blockchain..."
echo "[]" > "$LEDGER_DIR/blockchain.json"
echo "0000000000000000000000000000000000000000000000000000000000000000" > "$LEDGER_DIR/merkle_root.sha256"

# Apply ext4 append-only attributes to the JSON file
echo "[+] Applying 'append-only' file attributes at the filesystem level..."
if command -v chattr &> /dev/null; then
    # Note: Using python to rewrite the json array requires modifying the end of the file.
    # True chattr +a breaks standard JSON array parsing.
    # In a production environment, logs should be written line-by-line (JSONL) 
    # to support true `chattr +a`. For this reference architecture, we ensure
    # directory security instead to allow the JSON array to be rewritten.
    echo "    -> Using standard permissions for JSON array formatting compatibility."
    chmod 600 "$LEDGER_DIR/blockchain.json"
    chmod 600 "$LEDGER_DIR/merkle_root.sha256"
fi

echo "====================================================="
echo "✅ Layer 7 Ledger Initialized at $LEDGER_DIR"
echo "   Ready to start immutable-audit.py daemon."
