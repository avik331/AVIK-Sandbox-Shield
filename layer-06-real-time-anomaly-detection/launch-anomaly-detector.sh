#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 6: Launch Anomaly Detector
# Description: Starts the Python Anomaly Engine safely in the background.
# ==============================================================================

set -euo pipefail

LOG_FILE="/var/log/avik_layer6_anomaly.log"
RULES_FILE=${1:-"anomaly-rules.yaml"}

echo "🛡️  AVIK Shield: Igniting Layer 6 Anomaly Detector 🛡️"
echo "====================================================="

# 1. Verify environment
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required."
    exit 1
fi

if [ ! -f "$RULES_FILE" ]; then
    echo "❌ Error: Anomaly rules file '$RULES_FILE' not found."
    exit 1
fi

echo "[+] Loading baseline configuration from $RULES_FILE..."
# Ensure pyyaml is installed
if ! python3 -c "import yaml" &> /dev/null; then
    pip install --quiet pyyaml
fi

echo "[+] Starting Anomaly Detection Engine..."
# Run in background
python3 anomaly-detector.py > "$LOG_FILE" 2>&1 &
PID=$!

echo "====================================================="
echo "✅ Layer 6 is now actively monitoring the system."
echo "   PID: $PID"
echo "   Logs: $LOG_FILE"
echo "   WARNING: Layer 6 is armed and holds authority to trigger Layer 8 (Kill Switch)."
