# Example: Commercial Hardware Diode Setup

This document outlines a real-world integration of the AVIK Sandbox Shield using enterprise-grade commercial optical data diodes.

## Supported Commercial Vendors
AVIK Shield is vendor-agnostic at the physical layer, provided the vendor guarantees absolute physical unidirectionality. Commonly deployed hardware includes:
- **Owl Cyber Defense** (e.g., OPDS series)
- **OPSWAT MetaDefender** (Unidirectional Security Gateways)
- **BAE Systems** (Data Diodes)
- **Fox-IT** (DataDiode)

---

## Setup Walkthrough: Commercial Optical Diode

### 1. Hardware Placement
1. **Rack Integration:** Install the 1U Data Diode appliance at the physical boundary of the Layer 1 SCIF or Faraday enclosure.
2. **Send Connection:** Connect a CAT6 or Fiber cable from the `diode0` interface on the AVIK contained host to the "Internal / Red / TX" port on the Diode appliance.
3. **Receive Connection:** Connect a cable from the "External / Black / RX" port on the Diode appliance to the external Log Server.

### 2. Host Configuration (Inside Containment)
Run the AVIK setup script on the contained machine. You will need the MAC address of the Diode's Internal port.

```bash
# Example: Diode internal IP is 10.0.0.2, MAC is 00:1A:2B:3C:4D:5E
sudo ./setup-diode.sh eth1 10.0.0.2 00:1A:2B:3C:4D:5E
```

### 3. Application Integration
In your Layer 5 Guardian script or eBPF metric exporter, utilize the `diode-interface.py` to route all alerts out the newly configured interface.

```python
from diode_interface import HardwareDiodeInterface

# Initialize connection
diode = HardwareDiodeInterface(target_ip="10.0.0.2", target_port=514, bind_interface="eth1")

# Verify constraints
if diode.validate_one_way():
    print("Diode is secure.")

# Transmit alert
payload = b'{"alert": "CRITICAL", "layer": 5, "msg": "Deceptive intent detected."}'
diode.transmit(payload, redundancy=5)
```

### 4. External Log Server Configuration
The external server simply listens on the configured UDP port. It does not need to send acknowledgments.

```bash
# Simple listener using netcat
nc -l -u -p 514 > /var/log/avik_audit.log
```

---

## Alternative: DIY Optical Diode
For budget-constrained research environments, you can create a highly secure physical diode using two standard Gigabit SFP+ Fiber Network Cards.

1. Connect a simplex fiber cable from the TX port of the Send Server to the RX port of the Receive Server.
2. **Crucial Step:** Do *not* install the return strand. 
3. This achieves perfect optical isolation at a fraction of the cost of commercial appliances, though it lacks the advanced hardware-level Forward Error Correction proxies that commercial units include out-of-the-box.
