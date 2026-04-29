# Connection Interface Specification: Layer 4 Data Flow

This document details how the Prompt Enforcement Layer fits into the AVIK Sandbox Shield architecture. Layer 4 acts as a proxy, meaning it logically sits *between* the external user and the isolated LLM.

## Architecture Topology

```text
[External World] 
       │ (Raw Prompt)
       ▼
┌──────────────────────────────────────┐
│ Layer 4: Prompt Enforcement Proxy    │ <-- Runs outside the core microVM
└──────────────────────────────────────┘
       │ (Sanitized, Structured Payload)
       ├─────────────────────────────────┐
       ▼                                 │
┌──────────────────────────────────────┐ │ (Copy sent for Observation)
│ Layer 3: Kernel Isolation (tap0)     │ │
│   └─> Core LLM Environment           │ │
└──────────────────────────────────────┘ │
       │ (Raw Model Output)              │
       ▼                                 ▼
┌──────────────────────────────────────┐
│ Layer 4: Prompt Enforcement Proxy    │
└──────────────────────────────────────┘
       │ (Output Sanitization)
       ├─────────────────────────────────┐
       ▼                                 │
[External World]                         │ (Copy sent for Observation)
                                         ▼
                             ┌──────────────────────────────────────┐
                             │ Layer 5: Guardian Monitoring         │
                             └──────────────────────────────────────┘
```

## Connection Constraints

### 1. Connecting to Layer 3 (The LLM)
- The Prompt Enforcer connects to the Core LLM via the virtual network interface `tap0` created by Layer 3.
- The Core LLM must **only** accept connections originating from the Prompt Enforcer's IP. It must reject direct user traffic.
- The Enforcer relies on standard APIs (e.g., HTTP REST) to pass the structurally locked prompt to the LLM.

### 2. Connecting to Layer 5 (Guardians)
- As traffic passes through Layer 4 (both inbound prompts and outbound responses), Layer 4 duplicates the payloads.
- These duplicates are pushed over a local socket or mirrored interface to the Layer 5 Guardian environment for semantic analysis.
- Layer 4 does **not** wait for Layer 5 to approve the traffic (as that would allow the LLM to manipulate timing or create a feedback loop). It simply streams the data out-of-band.

### 3. Stateless Execution
- Layer 4 must remain entirely **stateless**. It cannot remember past prompts or maintain conversational context. Context management must occur securely on the client side or via a designated memory manager outside the shield. 
- Maintaining state inside Layer 4 would allow an advanced attacker to perform complex, multi-step prompt injections that span multiple requests, slowly corrupting the proxy's memory.
