# Connection Interface Specification: Layer 8 Triggers

This document details the exact mechanism by which the ultimate kill switch is triggered. Layer 8 must be configured to be extremely simple, minimizing the attack surface.

## Architecture Topology

```text
┌─────────────────────────┐
│ Layer 6: Anomaly Det.   │ (System Controller)
└──────────┬──────────────┘
           │ (UDP 9008 / Direct Physical Wiring)
           ▼
┌─────────────────────────┐
│ Layer 8: Terminator     │ (The Executioner)
└──────────┬──────────────┘
           │ (Hardware GPIO / SysRq)
           ▼
[ Layer 1 Host Hardware ] -> ⚡ POWER CUT
```

## Connection Constraints

### 1. The Trigger Input
- **Network Interface:** The `emergency-terminator.py` daemon listens on an internal UDP port (default `9008`). It accepts a simple JSON payload.
- **Physical Interface (Optional but Recommended):** In the highest-security deployments, Layer 6 and Layer 8 are physically wired together using a GPIO pin. If Layer 6 raises the pin HIGH, the hardware relay trips instantly, bypassing the Python daemon entirely.

### 2. Authorization
- **No Handshakes:** There is no TCP handshake, no OAuth, and no complex cryptographic authentication required to *trigger* the shutdown. This is by design. If Layer 6 decides to kill the system, the signal must be unimpeded. The risk of a false positive (accidentally shutting down the system) is vastly preferred over the risk of a false negative (failing to shut down during a breakout).

### 3. The Final Testament
- In the milliseconds between receiving the trigger and cutting the power, Layer 8 sends a final UDP datagram to Layer 2 (the Data Diode) to be recorded in the Layer 7 Immutable Audit log.
- This ensures that investigators know exactly *why* the server went offline.

### 4. Privilege Requirements
- Layer 8 **must** run as `root`. Without root privileges, it cannot interact with `/sys/class/gpio` or `/proc/sysrq-trigger`.
