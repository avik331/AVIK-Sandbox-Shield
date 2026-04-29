# Connection Interface Specification: Layer 5 One-Way Mirror

This document specifies how the Guardian Monitoring Layer observes the system without introducing new attack vectors.

## The Strict Observability Axiom
**Layer 5 must never possess a logical route that allows it to transmit data to the execution environment (Layer 3/Layer 4).**

If a Guardian model is compromised (e.g., via a subtle adversarial perturbation in the text it is analyzing), it must not be able to send an exploit payload back to the core LLM.

## Architecture Topology

```text
┌─────────────────────────┐           ┌─────────────────────────┐
│ Layer 4: Prompt Proxy   │ ──(1)──>  │ Layer 3: Core LLM       │
│ (Handles user traffic)  │ <─(2)──   │ (Isolated Execution)    │
└──────────┬──────────────┘           └─────────────────────────┘
           │ (3) UDP Mirror / TAP Mirror
           ▼ (RX ONLY)
┌─────────────────────────┐           ┌─────────────────────────┐
│ Layer 5: Guardian Orch. │ ──(4)──>  │ Layer 6: Anomaly Det.   │
│ (Passive Observer)      │           │ (System Controller)     │
└─────────────────────────┘           └─────────────────────────┘
```

### Data Flow Breakdown

1. **Ingress Mirroring (Path 3):**
   - Layer 4 (or a virtual network switch at the hypervisor level) mirrors all traffic traversing between the User and the Core LLM.
   - This traffic is sent via connectionless UDP datagrams to the Layer 5 Orchestrator (`guardian-monitor.py`).
   - The socket used by the Orchestrator to receive this data (`rx_socket`) is bound, but the Orchestrator mathematically *never* calls `sendto()` on this socket.

2. **Egress Alerting (Path 4):**
   - If a Guardian detects an anomaly, it cannot drop the packet or block the prompt directly (because doing so would require it to be in-line, introducing latency and a bi-directional attack surface).
   - Instead, it fires an asynchronous alert out of a *different* socket (`tx_socket`) directed at Layer 6.
   - Layer 6 then analyzes the alert and can decide to trigger Layer 8 (Emergency Termination).

### Physical Analogue
Think of Layer 5 as a security guard watching a feed from a security camera. The guard can see what is happening in the room, and the guard can press a red alarm button (Layer 6), but the guard has no microphone to speak into the room.
