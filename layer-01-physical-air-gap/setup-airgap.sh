#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 1: Setup Air-Gap script
# Description: Hardens a Linux machine into a strict air-gapped state.
# WARNING: This script disables networking. Run locally via console.
# ==============================================================================

set -eo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run as root."
  exit 1
fi

echo "🛡️  AVIK Shield: Initiating Layer 1 Air-Gap Hardening 🛡️"
echo "====================================================="

# 1. Disable NetworkManager & Systemd-Networkd
echo "[+] Disabling network management services..."
systemctl disable --now NetworkManager 2>/dev/null || true
systemctl disable --now systemd-networkd 2>/dev/null || true
systemctl disable --now wpa_supplicant 2>/dev/null || true
systemctl disable --now bluetooth.service 2>/dev/null || true

# 2. Block Wireless via rfkill
echo "[+] Asserting rfkill blocks on all wireless transmitters..."
if command -v rfkill &> /dev/null; then
    rfkill block all
else
    echo "[-] rfkill not found, skipping user-space block..."
fi

# 3. Bring down all network interfaces except loopback
echo "[+] Bringing down active interfaces..."
for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
    if [ "$iface" != "lo" ] && [ "$iface" != "diode0" ]; then
        echo "    -> Shutting down $iface"
        ip link set dev "$iface" down 2>/dev/null || true
    fi
done

# 4. Blacklist Network & Wireless Kernel Modules
echo "[+] Blacklisting wireless and common networking kernel modules..."
cat <<EOF > /etc/modprobe.d/avik-airgap-blacklist.conf
# AVIK Shield Layer 1 - Kernel Module Blacklist
# Wireless & Bluetooth
blacklist cfg80211
blacklist mac80211
blacklist iwlwifi
blacklist iwlmvm
blacklist btusb
blacklist bluetooth
blacklist btrtl
blacklist btbcm
blacklist btintel

# Prevent auto-loading of USB network adapters
blacklist cdc_ether
blacklist cdc_eem
blacklist cdc_ncm
blacklist rndis_host
blacklist r8152
EOF

# Update initramfs to ensure blacklists apply on boot
echo "[+] Updating initramfs..."
if command -v update-initramfs &> /dev/null; then
    update-initramfs -u
elif command -v dracut &> /dev/null; then
    dracut -f
fi

# 5. Disable USB Storage (Optional but recommended for strict isolation)
read -p "[?] Do you want to aggressively disable USB mass storage? (y/N): " disable_usb
if [[ "$disable_usb" =~ ^[Yy]$ ]]; then
    echo "    -> Blacklisting usb-storage"
    echo "blacklist usb-storage" >> /etc/modprobe.d/avik-airgap-blacklist.conf
    echo "blacklist uas" >> /etc/modprobe.d/avik-airgap-blacklist.conf
fi

# 6. Flush iptables and set default DROP policies (defense in depth)
echo "[+] Configuring iptables for total DROP..."
if command -v iptables &> /dev/null; then
    iptables -F
    iptables -X
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
    # Allow loopback traffic internally
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT
fi

echo "====================================================="
echo "✅ Layer 1 Hardening Complete."
echo "⚠️  System is now software-isolated. Physical hardware modification"
echo "    (e.g., removing Wi-Fi cards) is still required for true Layer 1 compliance."
echo "    Please reboot for kernel module blacklists to take full effect."
