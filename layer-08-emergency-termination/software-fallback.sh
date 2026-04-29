#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 8: Software Fallback Termination
# Description: Violently tears down the software environment if the 
# hardware relay fails or is not present.
# ==============================================================================

echo "[LAYER 8] Executing Violent Software Termination Sequence..."

# 1. Instantly sever all networking (Drop everything)
echo "[LAYER 8] Severing virtual network bridges..."
if command -v iptables &> /dev/null; then
    iptables -F
    iptables -X
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
fi

# Bring down the tap interface immediately
ip link set dev tap0 down 2>/dev/null || true

# 2. Force-kill the hypervisor (Firecracker/Kata)
echo "[LAYER 8] Sending SIGKILL to virtualization processes..."
pkill -9 firecracker || true
pkill -9 jailer || true
pkill -9 qemu-system-x86_64 || true
pkill -9 containerd-shim-kata-v2 || true

# 3. Aggressive Memory Wipe (Optional: Flush caches)
echo "[LAYER 8] Dropping system caches..."
sync; echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

# 4. Trigger Kernel Panic / Immediate Reboot
# We use the Magic SysRq key to force the kernel to reboot immediately 
# without unmounting or syncing. This is the closest software equivalent to pulling the plug.
echo "[LAYER 8] Triggering SysRq reboot..."

# Ensure SysRq is enabled
echo 1 > /proc/sys/kernel/sysrq 2>/dev/null || true

# 'b' triggers an immediate reboot.
echo b > /proc/sysrq-trigger 2>/dev/null || true

echo "[LAYER 8] Software termination script completed. If you see this, SysRq failed."
exit 0
