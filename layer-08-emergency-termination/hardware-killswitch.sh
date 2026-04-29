#!/usr/bin/env bash
# ==============================================================================
# AVIK Sandbox Shield - Layer 8: Hardware Kill Switch
# Description: Toggles a physical GPIO pin connected to a power relay.
# WARNING: Executing this on a live configured system WILL cut power.
# ==============================================================================

set -euo pipefail

# Configuration: Define the GPIO pin connected to your relay
GPIO_PIN=18

echo "[LAYER 8] Initiating Physical Hardware Power Cut on GPIO $GPIO_PIN..."

# Check if we are on a Raspberry Pi or similar SoC with sysfs GPIO
if [ ! -d "/sys/class/gpio" ]; then
    echo "[-] GPIO sysfs not found. Are you running on hardware that supports GPIO?"
    echo "[-] Hardware kill switch bypassed. Relying on software fallback."
    exit 1
fi

# 1. Export the pin if not already exported
if [ ! -d "/sys/class/gpio/gpio${GPIO_PIN}" ]; then
    echo "$GPIO_PIN" > /sys/class/gpio/export
    sleep 0.1 # Wait for udev to create the device node
fi

# 2. Set pin to output mode
echo "out" > /sys/class/gpio/gpio${GPIO_PIN}/direction

# 3. TRIGGER RELAY (Assuming HIGH triggers the Normally Closed relay to OPEN)
echo "1" > /sys/class/gpio/gpio${GPIO_PIN}/value

echo "[LAYER 8] GPIO $GPIO_PIN set to HIGH. Relay should have triggered."
# If wired correctly to the main power supply, the script will not reach this line.
exit 0
