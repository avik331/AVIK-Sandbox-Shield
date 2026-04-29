<div align="center">
  <h1>🛡️ AVIK Shield Layer 2: Hardware Data Diode</h1>
  <p><b>The physical guarantor of one-way telemetry and audit logging.</b></p>
</div>

---

## 📖 Overview

The Hardware Data Diode Layer is the crucial link that solves the primary dilemma of air-gapped systems: *How do we monitor a perfectly isolated system without breaking its isolation?*

Layer 2 enforces **physical unidirectionality**. Unlike software firewalls which can be bypassed via misconfigurations or zero-day exploits, a physical data diode relies on the laws of physics—specifically optics—to ensure data can only travel in one direction. In the AVIK framework, this allows continuous egress of critical logs and metrics from the containment zone (Layer 1) to the external world, without opening any pathway for attackers to send data back in.

## ⚠️ Threats Defeated

- **Bi-directional Communication (C2):** An attacker cannot establish a two-way handshake (e.g., TCP), rendering reverse shells and interactive command channels physically impossible.
- **Reverse Data Flow:** Prevents the external monitoring network from accidentally or maliciously injecting data, commands, or malware into the containment zone.
- **Protocol Exploitation:** Hardware diodes do not run complex network stacks on the transmission line. They strip away TCP/IP complexity, mitigating packet-crafting attacks.
- **Network Exfiltration (Ingress):** Completely blocks any inbound traffic that an escaped model might attempt to pull from external servers.

## 🛠️ Module Components

1. **`setup-diode.sh`**: OS-level hardening script that configures the host network stack for diode compatibility (static ARP, UDP optimization, and strict outbound-only routing).
2. **`diode-interface.py`**: The official Python API for Layer 2. Enforces unidirectional transmission constraints and handles Forward Error Correction (FEC) required for reliable diode transfers.
3. **`simulation-mode.py`**: A local simulator that mimics hardware diode constraints (including random packet loss) for development and testing without physical hardware.
4. **[Connection Interface Specification](connection-interface.md)**: Defines the boundaries between Layer 1, Layer 2, and the external audit servers.
5. **[Real Hardware Setup](example-real-hardware.md)**: Walkthroughs for implementing commercial diodes like OPSWAT or Owl Cyber Defense.

## 🚀 Quick Start (Simulation Mode)

If you do not yet have physical hardware, you can test the software mechanics using the simulator:

1. **Start the Receiver (External World):**
   ```bash
   python3 simulation-mode.py --mode receive
   ```
2. **Send Data (From Containment Zone):**
   ```bash
   python3 simulation-mode.py --mode send --payload "Critical Anomaly Detected"
   ```

## 🔌 Connection Interface

Layer 2 is uniquely positioned at the boundary of the air-gap. 

- **Input:** Receives UDP datagrams from the `diode0` interface of the Layer 1 environment.
- **Output:** Emits physical signals (typically photons over fiber) to the external receiver, which then forwards the data to Layer 7 (Immutable Audit).

For precise technical specifications, see the [Connection Interface Document](connection-interface.md).
