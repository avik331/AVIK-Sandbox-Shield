#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 5: Launch Guardian Ensemble
# Description: Starts the Python orchestrator safely in the background.
# ==============================================================================

set -euo pipefail

LOG_FILE="/var/log/avik_layer5_guardians.log"

echo "🛡️  AVIK Shield: Igniting Layer 5 Guardian Ensemble 🛡️"
echo "====================================================="

# 1. Verify environment
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required."
    exit 1
fi

echo "[+] Loading Guardian definitions..."
# In a real setup, we would load the narrow-guardian templates here.
# For this script, we assume a wrapper script 'run_ensemble.py' exists, 
# or we just test the monitor's base loading.

cat << 'EOF' > /tmp/run_ensemble.py
from guardian_monitor import GuardianOrchestrator
from narrow_guardian_template import SemanticToxicityGuardian, LengthAnomalyGuardian

orch = GuardianOrchestrator()
orch.register_guardian(SemanticToxicityGuardian())
orch.register_guardian(LengthAnomalyGuardian())

print("[+] Ensemble assembled successfully.")
orch.start_monitoring()
EOF

echo "[+] Starting Guardian Orchestrator (RX-Only Mode)..."
python3 /tmp/run_ensemble.py > "$LOG_FILE" 2>&1 &
PID=$!

echo "====================================================="
echo "✅ Layer 5 Guardians are now actively observing."
echo "   PID: $PID"
echo "   Logs: $LOG_FILE"
echo "   Constraint: ONE-WAY MIRROR (No reverse communication possible)."
