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
- **Cryptographic Signatures:** The Layer 8 Daemon generates a 32-byte hexadecimal secret key at startup (`/etc/avik/killswitch.key`). Layer 6 must read this key and use it to sign the JSON payload with an HMAC-SHA256 signature.
- **Fail-Closed:** If the `hmac` field is missing, malformed, or mathematically invalid, Layer 8 instantly drops the packet and logs an unauthorized breach attempt. This prevents local privilege escalation or UDP spoofing.

### 3. The Final Testament
- In the milliseconds between receiving the trigger and cutting the power, Layer 8 sends a final UDP datagram to Layer 2 (the Data Diode) to be recorded in the Layer 7 Immutable Audit log.
- This ensures that investigators know exactly *why* the server went offline.

### 4. Privilege Requirements
- Layer 8 **must** run as `root`. Without root privileges, it cannot interact with `/sys/class/gpio` or `/proc/sysrq-trigger`.
