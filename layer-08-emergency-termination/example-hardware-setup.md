# Example: True Hardware Kill Switch Setup

The most secure implementation of Layer 8 physically cuts the power to the Layer 1 Containment Node. This requires a dedicated out-of-band management controller (like a Raspberry Pi) or specific wiring to the motherboard.

## Option A: Smart PDU / Managed Power Strip (Enterprise)
If you are running in a datacenter, the Layer 8 Terminator Daemon should be configured to send an SNMP or REST API command to the Power Distribution Unit (PDU).

1. Connect the Containment Node to Outlet 1 on an APC or CyberPower Switched PDU.
2. In `emergency-terminator.py`, replace the hardware script call with a command to cycle the PDU outlet.
   ```bash
   # Example snmpset command to turn off Outlet 1
   snmpset -v1 -c private 10.0.0.50 1.3.6.1.4.1.318.1.1.4.4.2.1.3.1 i 2
   ```

## Option B: GPIO Relay Module (DIY / Research)
If you are building a custom rig, you can use a standard 5V/12V relay module commonly used with Arduino or Raspberry Pi.

### Components Needed:
- 1x Raspberry Pi (Acting as the dedicated Layer 6/8 Controller, situated outside the containment zone).
- 1x 5V Relay Module (e.g., SRD-05VDC-SL-C).
- Jumper Wires.

### Wiring:
1. Cut the positive (live) wire of the power cable feeding the Layer 1 Containment Node.
2. Connect the two ends of the cut wire into the **Common (COM)** and **Normally Closed (NC)** terminals of the Relay.
   - *Why Normally Closed?* Because we want power to flow normally. When the relay is triggered (energized), it will switch to Normally Open (NO), breaking the circuit and cutting power.
3. Connect the Relay's `VCC` and `GND` to the Raspberry Pi's 5V and Ground pins.
4. Connect the Relay's `IN` (Signal) pin to **GPIO 18** on the Raspberry Pi.

### Execution:
When Layer 6 detects an anomaly, it signals Layer 8 (running on the Pi). Layer 8 executes `hardware-killswitch.sh`, which pulls GPIO 18 HIGH. The relay clicks, the circuit breaks, and the AI containment node goes completely dark.

> **⚠️ CAUTION:** Modifying high-voltage power cables (110V/220V AC) is extremely dangerous and can cause fatal electric shock or fire. Only qualified electricians should perform AC mains wiring. For a safer alternative, use an enclosed IoT relay box (like the *Digital Loggers IoT Relay*) that accepts a 3.3V logic signal to safely switch AC power.
