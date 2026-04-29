#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 3: Run Isolated LLM
# Description: Starts the Firecracker process and orchestrates the microVM using
# the kernel-isolation.py API.
# ==============================================================================

set -euo pipefail

API_SOCKET="/tmp/firecracker.socket"
LOG_FILE="/var/log/firecracker.log"

echo "🛡️  AVIK Shield: Igniting Layer 3 microVM 🛡️"
echo "====================================================="

# 1. Cleanup stale sockets
if [ -e "$API_SOCKET" ]; then
    echo "[+] Removing stale API socket..."
    rm -f "$API_SOCKET"
fi

# 2. Start the Firecracker daemon in the background
echo "[+] Starting Firecracker daemon..."
# In a true production deployment, jailer is used here instead of raw firecracker
firecracker --api-sock "$API_SOCKET" --show-level --show-log-origin > "$LOG_FILE" 2>&1 &
FC_PID=$!

echo "[+] Firecracker daemon running with PID: $FC_PID"

# 3. Wait for the API socket to become available
sleep 1
if [ ! -e "$API_SOCKET" ]; then
    echo "❌ Error: Firecracker failed to start. Check $LOG_FILE."
    exit 1
fi

# 4. Orchestrate via Python API
# We use a quick inline python script to consume the kernel-isolation module
echo "[+] Orchestrating via Python Layer 3 API..."

python3 - <<EOF
import sys
from kernel_isolation import FirecrackerManager, IsolationViolation

try:
    fc = FirecrackerManager(socket_path="$API_SOCKET")
    
    # 1. Hardware Constraints (4 vCPU, 16GB RAM)
    fc.configure_machine(vcpu_count=4, mem_size_mib=16384, smt=False)
    
    # 2. Boot Source
    # Assuming vmlinux.bin is prepared in the current directory
    fc.configure_boot_source(
        kernel_path="$(pwd)/vmlinux.bin",
        boot_args="console=ttyS0 reboot=k panic=1 pci=off nomodules ipv6.disable=1 quiet"
    )
    
    # 3. Root Filesystem (Strictly Read-Only)
    fc.configure_rootfs(
        drive_path="$(pwd)/rootfs.ext4",
        is_read_only=True
    )
    
    # 4. Network Constraints
    fc.configure_network(
        iface_id="eth0",
        host_dev_name="tap0",
        guest_mac="AA:FC:00:00:00:01"
    )
    
    # 5. Ignite
    fc.start_instance()
    
except IsolationViolation as e:
    print(f"❌ Isolation Constraint Failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)
EOF

echo "====================================================="
echo "✅ Layer 3 Execution Environment is live."
echo "   The Core LLM is now running inside the hardware boundary."
echo "   Logs: $LOG_FILE"
