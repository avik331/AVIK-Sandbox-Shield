# Connection Interface Specification: Layer 1 to Layer 2

This document defines the strict, mathematically verifiable protocol for connecting the Layer 1 Physical Air-Gap environment to the Layer 2 Hardware Data Diode.

## 🛑 The Core Axiom
**Layer 1 cannot have any physical or logical capability to receive data from the outside world once sealed.**

Therefore, the interface between Layer 1 and the rest of the architecture must be strictly unidirectional outbound (Egress Only).

## Physical Connection Topologies

To connect Layer 1 to Layer 2, you must use one of the following physically constrained methodologies:

### Method A: Simplex Fiber Optic (Recommended)
This is the enterprise standard for AVIK Shield compliance.
1. **Host Configuration:** The air-gapped machine must have an SFP/SFP+ network interface card installed.
2. **The Diode:** Connect a fiber optic cable from the host's TX (Transmit) port to the external log server's RX (Receive) port.
3. **The Physical Constraint:** The cable connecting the external server's TX port back to the host's RX port **must not exist** (or must be physically severed).
4. **Result:** The host can emit photons, but the hardware physically lacks the pathway to receive them.

### Method B: Serial Unidirectional Cable
For smaller setups or embedded hardware without PCIe slots.
1. **Host Configuration:** Utilize an RS-232 serial port.
2. **The Diode:** Wire a custom serial cable where only the `TX` (Transmit) and `GND` (Ground) pins are connected from the host to the receiver.
3. **The Physical Constraint:** The `RX` (Receive) pin on the air-gapped host must be physically disconnected or desoldered.

---

## Software Interface (OSI Layer 2/3)

Because the physical layer lacks a return path, standard TCP/IP networking will fail entirely. TCP requires a three-way handshake (SYN, SYN-ACK, ACK), which is impossible.

### The Diode Interface (`diode0`)
In Layer 1, the network interface connected to the physical diode must be configured purely for UDP broadcast or point-to-point UDP streaming.

**Requirements:**
- No IP address assignment is strictly necessary if using raw ethernet frames, but statically assigning an IP (e.g., `10.0.0.2/24`) is acceptable for ease of use.
- ARP resolution will fail (no return path). The host must be configured with a static ARP entry for the receiving MAC address.

### The Staging Workflow
1. Layer 5 (Guardians) or Layer 6 (Anomaly Detection) generates an alert.
2. The alert is passed to the Layer 1 `airgap-module.py` via `UnidirectionalStager.stage_data()`.
3. A separate proxy daemon running on the host reads the staged file and blindly blasts it out of `diode0` via UDP datagrams.
4. **Forward Error Correction (FEC):** Because packets may drop and TCP cannot recover them, the proxy daemon must wrap the data in Reed-Solomon FEC encoding and transmit it multiple times.

*Connecting any bi-directional capable interface (like standard Cat6 copper ethernet) between Layer 1 and an external switch immediately voids AVIK Shield compliance.*
