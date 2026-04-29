# Connection Interface Specification: Layer 6 Topology

This document details the critical topological position of Layer 6 within the AVIK Sandbox Shield. Layer 6 is the System Controller, possessing the ultimate authority over the execution environment.

## Architecture Topology

```text
┌─────────────────────────┐           ┌─────────────────────────┐
│ Layer 5: Guardians      │ ──(1)──>  │ Layer 6: Anomaly Det.   │
│ (Observer Ensembles)    │           │ (System Controller)     │
└─────────────────────────┘           └──────────┬──────────────┘
                                                 │
┌─────────────────────────┐           ┌──────────▼──────────────┐
│ Host OS eBPF Probes     │ ──(2)──>  │ Layer 8: Kill Switch    │
│ (System Telemetry)      │           │ (Emergency Termination) │
└─────────────────────────┘           └─────────────────────────┘
                                                 │
┌─────────────────────────┐           ┌──────────▼──────────────┐
│ Layer 7: Immutable      │ <──(3)──  │ Layer 2: Data Diode     │
│ Audit Ledger (External) │           │ (Egress Hardware)       │
└─────────────────────────┘           └─────────────────────────┘
```

## Connection Constraints

### 1. Ingress from Layer 5 (Semantic Alerts)
- Layer 6 receives asynchronous, one-way alerts from Layer 5 via a dedicated internal UDP port (default `9006`).
- Layer 6 processes these alerts mathematically, applying weights to different guardians. A single alert may not trigger termination, but repeated alerts will quickly overwhelm the decay threshold.

### 2. Ingress from Host OS (Telemetry)
- Layer 6 integrates with host-level monitoring tools (such as `bcc` or `cilium/ebpf`).
- It receives real-time streams of CPU utilization, memory allocation velocity, and syscall frequency on port `9007`.
- **Constraint:** Layer 6 must run as a privileged process (root) on the host OS to access this data, but it is entirely logically separated from the Layer 3 microVM.

### 3. Egress to Layer 8 (Kill Switch)
- Layer 6 has a direct, unimpeded channel to Layer 8 via UDP port `9008` (or direct physical GPIO pins if configured).
- **Constraint:** This is a "Fire-and-Forget" connection. When the critical threshold is reached, Layer 6 sends the `TERMINATE` payload. It does not negotiate or ask the LLM to shut down.

### 4. Egress to Layer 7 (Audit)
- Before and during termination, Layer 6 attempts to flush its current state (the mathematical progression of the threat score and the inciting telemetry) to the `diode0` interface.
- **Constraint:** This telemetry is pushed *through* the physical Layer 2 Data Diode to the Layer 7 Immutable Audit log, ensuring an incorruptible record of *why* the Kill Switch was thrown.
