# Connection Interface Specification: Layer 1 ➡️ Layer 2 ➡️ External

This document details the precise technical boundaries connecting the Physical Air-Gap (Layer 1), the Hardware Data Diode (Layer 2), and the external monitoring environment.

## The Tri-Node Architecture

A proper hardware diode setup requires three distinct physical components:

### 1. The Send Node (Inside Containment - Layer 1)
- **Role:** Generates telemetry, logs, and Guardian alerts.
- **Hardware:** Connects to the TX (Transmit) end of the hardware diode.
- **Network Stack:** Configured for blind UDP broadcast. Dynamic ARP is disabled.
- **Software Interface:** Uses `diode-interface.py` to transmit payloads.

### 2. The Hardware Diode (Layer 2)
- **Role:** The physical guarantor of unidirectionality.
- **Mechanism:** Accepts electronic or optical input from the Send Node. Transmits light across a physical gap to the Receive Node. Lacks any physical pathway to send light backward.
- **Transport:** Layer 2 operates purely at the physical layer (OSI Layer 1). It does not understand IP or TCP; it merely moves bits.

### 3. The Receive Node (Outside Containment)
- **Role:** Reconstructs the UDP packets and forwards them to Layer 7 (Immutable Audit).
- **Hardware:** Connects to the RX (Receive) end of the hardware diode.
- **Network Stack:** Listens promiscuously for incoming UDP frames on the designated port.
- **Software Interface:** Runs a proxy daemon that handles packet deduplication (since the Send Node transmits repeatedly for redundancy) and Forward Error Correction decoding.

---

## Technical Constraints

### Payload Specifications
- **Protocol:** Strictly UDP (User Datagram Protocol).
- **Max Transmission Unit (MTU):** 1400 bytes. Payloads exceeding this must be fragmented by the application layer before calling `transmit()`, as network-layer fragmentation across a diode is highly unreliable.
- **Serialization:** Protocol Buffers or JSON are recommended.

### Error Handling
Because there is no reverse channel, the Send Node cannot know if a packet was dropped.
- **Redundancy:** The `HardwareDiodeInterface` defaults to transmitting every payload 3 times.
- **Sequencing:** Every payload must include a strictly monotonically increasing sequence number so the Receive Node can detect missing packets and deduplicate repeated ones.

### ARP Resolution
The Send Node must be configured with a **Static ARP Table**. The `setup-diode.sh` script enforces this. Because the diode blocks inbound traffic, the Send Node will never receive an ARP Reply from the Receive Node. Attempting to transmit without a static ARP entry will result in the OS dropping the packets before they even reach the network card.
