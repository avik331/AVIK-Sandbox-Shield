#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 2: Setup Diode Interface
# Description: Configures the Linux network stack for physical data diodes.
# Requires root privileges.
# ==============================================================================

set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run as root."
  exit 1
fi

echo "🛡️  AVIK Shield: Initiating Layer 2 Diode Configuration 🛡️"
echo "====================================================="

DIODE_IFACE=${1:-"diode0"}
TARGET_IP=${2:-"10.0.0.2"}
TARGET_MAC=${3:-"00:11:22:33:44:55"}

# 1. Interface Validation
if ! ip link show "$DIODE_IFACE" &> /dev/null; then
    echo "[-] Interface $DIODE_IFACE not found. Please specify the correct interface."
    echo "    Usage: $0 <interface_name> <target_ip> <target_mac>"
    exit 1
fi

echo "[+] Configuring interface $DIODE_IFACE for unidirectional egress..."

# 2. Disable ARP Resolution on the interface
# Hardware diodes cannot receive ARP replies. We must disable ARP and set it statically.
echo "[+] Disabling dynamic ARP..."
ip link set dev "$DIODE_IFACE" arp off

# 3. Static ARP Configuration
echo "[+] Setting static ARP entry for Target Receiver ($TARGET_IP -> $TARGET_MAC)..."
arp -s "$TARGET_IP" "$TARGET_MAC" -i "$DIODE_IFACE" || ip neigh add "$TARGET_IP" lladdr "$TARGET_MAC" dev "$DIODE_IFACE" nud permanent

# 4. Routing Configuration
# Ensure that ONLY UDP traffic destined for the target IP goes out this interface
echo "[+] Configuring strict routing..."
ip route flush dev "$DIODE_IFACE" 2>/dev/null || true
ip route add "$TARGET_IP" dev "$DIODE_IFACE"

# 5. OS-Level Ingress Blocking
# Even though the hardware diode blocks incoming signals, we implement defense-in-depth 
# at the OS level to drop anything that somehow arrives on the interface.
echo "[+] Applying iptables DROP rules for all ingress on $DIODE_IFACE..."
if command -v iptables &> /dev/null; then
    # Drop all incoming packets on the diode interface
    iptables -A INPUT -i "$DIODE_IFACE" -j DROP
    # Allow outgoing UDP ONLY
    iptables -A OUTPUT -o "$DIODE_IFACE" -p udp -j ACCEPT
    # Drop everything else outbound
    iptables -A OUTPUT -o "$DIODE_IFACE" -j DROP
fi

# 6. Disable IPv6 to reduce attack surface
echo "[+] Disabling IPv6 on diode interface..."
sysctl -w net.ipv6.conf."$DIODE_IFACE".disable_ipv6=1 > /dev/null

echo "====================================================="
echo "✅ Layer 2 Diode Interface configured successfully."
echo "   Interface: $DIODE_IFACE"
echo "   Target: $TARGET_IP ($TARGET_MAC)"
echo "   Status: STRICT EGRESS ONLY"
