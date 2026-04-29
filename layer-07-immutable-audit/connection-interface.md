# Connection Interface Specification: Layer 7 Audit Integration

This document explains where the Immutable Audit Layer sits within the AVIK Sandbox Shield topology and how it receives data safely.

## Topological Placement

Layer 7 exists **outside** the containment boundary (Layers 1-6). It resides on a completely separate, hardened logging server.

```text
┌─────────────────────────────────────┐
│ CONTAINMENT ZONE (Layers 1,3,4,5,6) │
│ Host OS (eBPF, iptables)            │
└──────────────────┬──────────────────┘
                   │ 
           (Internal UDP 514)
                   │
           ┌───────▼───────┐
           │ Layer 2 Data  │
           │ Diode (TX)    │
           └───────┬───────┘
             (Optical Gap)
           ┌───────▼───────┐
           │ Layer 2 Data  │
           │ Diode (RX)    │
           └───────┬───────┘
                   │
           (External UDP 514)
                   │
           ┌───────▼───────┐
           │ Layer 7 Audit │
           │ Daemon        │
           └──────────────────────────┘
```

## Connection Constraints

### 1. Ingress Only via Data Diode
- The Audit Daemon (`immutable-audit.py`) listens on a network interface that is physically connected to the RX (receive) side of the Layer 2 Data Diode.
- **Critical Security Guarantee:** Because the physical hardware of Layer 2 lacks the components to transmit data backwards, it is impossible for the Audit Daemon (or a compromised logging server) to send malicious data or commands back into the containment zone.

### 2. Upstream Data Aggregation
The containment zone host must route all vital telemetry to the Data Diode's internal interface. This includes:
- Layer 3 microVM logs
- Layer 4 prompt enforcement records
- Layer 5 Guardian alerts
- Layer 6 Anomaly triggers
- General Syslog (auth, kern)

### 3. Egress to Layer 8
- Layer 7 does *not* trigger Layer 8 (the Kill Switch). Layer 6 is responsible for triggering the kill switch from *inside* the containment zone based on live metrics.
- Layer 7's only job is to provide the post-mortem forensic ledger of *why* Layer 6 threw the switch, proving that the anomaly occurred and the kill was justified.
