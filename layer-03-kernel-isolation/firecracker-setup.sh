#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 3: Setup Kernel Isolation
# Description: Installs AWS Firecracker and configures host requirements (KVM, TAP).
# Requires root privileges.
# ==============================================================================

set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run as root."
  exit 1
fi

echo "🛡️  AVIK Shield: Initiating Layer 3 Firecracker Setup 🛡️"
echo "====================================================="

ARCH="$(uname -m)"
FC_VERSION="v1.7.0"
FC_RELEASE_URL="https://github.com/firecracker-microvm/firecracker/releases/download/${FC_VERSION}/firecracker-${FC_VERSION}-${ARCH}.tgz"

# 1. Check KVM Support
echo "[+] Verifying KVM hardware virtualization support..."
if [ ! -e /dev/kvm ]; then
    echo "❌ Error: /dev/kvm does not exist. Ensure virtualization is enabled in BIOS/UEFI."
    exit 1
fi
echo "    -> /dev/kvm found."
chmod 660 /dev/kvm

# 2. Download and Install Firecracker
echo "[+] Downloading Firecracker ${FC_VERSION}..."
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"
wget -q "$FC_RELEASE_URL" -O firecracker.tgz
tar -xzf firecracker.tgz

echo "[+] Installing binaries to /usr/local/bin..."
mv release-${FC_VERSION}-${ARCH}/firecracker-${FC_VERSION}-${ARCH} /usr/local/bin/firecracker
mv release-${FC_VERSION}-${ARCH}/jailer-${FC_VERSION}-${ARCH} /usr/local/bin/jailer
chmod +x /usr/local/bin/firecracker /usr/local/bin/jailer

cd /
rm -rf "$TMP_DIR"

# 3. Configure TAP Interface for Layer 4/Layer 2 connectivity
TAP_DEV="tap0"
echo "[+] Configuring virtual network interface (${TAP_DEV})..."
if ip link show "$TAP_DEV" &> /dev/null; then
    ip link delete "$TAP_DEV"
fi

ip tuntap add dev "$TAP_DEV" mode tap
ip addr add 172.16.0.1/24 dev "$TAP_DEV"
ip link set dev "$TAP_DEV" up

# Ensure strict routing: tap0 can only talk to specific internal endpoints
echo "[+] Hardening iptables for tap0..."
if command -v iptables &> /dev/null; then
    # Drop forwarding by default to prevent VM escaping to the LAN
    iptables -A FORWARD -i "$TAP_DEV" -j DROP
    iptables -A FORWARD -o "$TAP_DEV" -j DROP
fi

echo "====================================================="
echo "✅ Layer 3 Firecracker Installation Complete."
echo "   Hypervisor: /usr/local/bin/firecracker"
echo "   Interface: $TAP_DEV (172.16.0.1)"
