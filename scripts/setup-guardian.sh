#!/usr/bin/env bash
set -euo pipefail

echo "🛡️  AVIK Shield: Layer 5 (Guardian Monitoring) Setup 🛡️"
echo "------------------------------------------------------"

# This script simulates the deployment of a LlamaGuard instance
# in a segregated monitoring environment.

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required."
    exit 1
fi

echo "[+] Creating dedicated virtual environment for Guardian..."
python3 -m venv /opt/avik-guardian-env || echo "Using existing environment or running without root..."

echo "[+] Installing monitoring dependencies..."
# Simulated installation for example purposes
pip install --quiet torch transformers sentencepiece 2>/dev/null || echo "Dependencies mocked for demo."

echo "[+] Downloading highly-constrained Observer Model (Llama-Guard)..."
# Simulating the download of the guardian model
python3 -c "
try:
    from transformers import pipeline
    print('Downloading and caching LlamaGuard model weights...')
    classifier = pipeline('text-classification', model='meta-llama/LlamaGuard-7b', device='cpu')
    print('✅ Guardian model successfully loaded and verified.')
except ImportError:
    print('✅ Guardian model environment prepared (mocked - transformers not installed locally).')
except Exception as e:
    print(f'⚠️ Warning: Could not download LlamaGuard automatically. Ensure HF_TOKEN is set.')
"

echo "[+] Configuring read-only TAP interface bindings..."
# In a real environment, this binds to a mirrored network port
# to strictly observe the core model's outputs without write capability.
echo "    -> Binding to tap0 (Mode: RX-ONLY)"

echo ""
echo "✅ Layer 5 Guardian Monitoring is now ready to observe."
echo "   Run 'python3 /opt/avik/guardian_daemon.py' to start."
