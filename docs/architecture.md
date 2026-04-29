# Architecture Specification: The 8-Layer Defense-in-Depth Model

## Core Philosophy

The AVIK Sandbox Shield is constructed on a fundamental premise: **Any single security boundary, regardless of its sophistication, has a non-zero probability of failure when subjected to the capabilities of a frontier AI system.** 

Standard containment strategies (e.g., containerization, prompt engineering) represent a "flat" security model. A breach of the namespace implies a total system compromise. AVIK Shield implements a deeply stratified architecture where the layers are fundamentally asymmetric. An exploit capable of bypassing Layer 4 (application logic) is useless against Layer 2 (optical physics).

## Layer Stratification & Domain Mechanics

| Layer | Domain | Attack Surface | Mitigation Mechanism |
| :--- | :--- | :--- | :--- |
| **L1: Air-Gap** | Physics / RF | Network Sockets, EM Emissions | Faraday Cages, Physical Disconnection |
| **L2: Data Diode** | Optics / Hardware | Bi-directional TCP/C2 | TX-disabled fiber optic receivers |
| **L3: Kernel Isolation** | OS / Hypervisor | VFS, eBPF, Namespaces | Hardware-accelerated microVMs (Firecracker) |
| **L4: Prompt Enforcement**| Application / NLP | Prompt Injection, Serialization | Strict Schema, Stateless proxy validation |
| **L5: Guardian Monitoring**| AI / Semantics | Deception, Steganography | Ensembles of narrow observer models |
| **L6: Anomaly Detection** | Statistics / Systems| Syscall deviations, Resource | eBPF profiling, HIDS, PMCs |
| **L7: Immutable Audit** | Cryptography | Log tampering, Forensics | Merkle trees, WORM storage, HSMs |
| **L8: Kill Switch** | Electrical Eng. | Total software compromise | Out-of-band electromechanical power relays |

## Strict Data Flow & The Isolation Boundary

The architecture defines a strict **Isolation Boundary** containing Layers 3, 4, and the Core LLM. 

### Ingress (The Path In)
1. The operator submits a prompt.
2. The prompt crosses Layer 1 physically.
3. It hits Layer 4 (Prompt Enforcement), running in a dedicated Layer 3 microVM.
4. If it passes schema validation, it is forwarded over a virtual point-to-point link to the Core LLM microVM.

### Egress (The Path Out)
1. The Core LLM generates an output.
2. The output is intercepted by Layer 4 for redaction and validation.
3. Simultaneously, a read-only mirror of the output is streamed to Layer 5 (Guardians).
4. System metrics are gathered by Layer 6 (eBPF).
5. Output, metrics, and Guardian verdicts are pushed through Layer 2 (Data Diode) to Layer 7 (Immutable Audit).

### Control Plane
- The Control Plane (Layer 6 and Layer 8) operates completely out-of-band. 
- If Layer 6 detects a critical anomaly, it bypasses all software stacks and sends a hardware signal to Layer 8, cutting power.

## Formal Verification Requirements

For a deployment to achieve **AVIK Shield Certified** status, specific formal proofs must be provided:
1. **Network Proof:** Proof of absence of logical routes from the Core LLM namespace to any routable IP space.
2. **Diode Proof:** Hardware schematics proving the absence of a TX laser on the receiving end of Layer 2.
3. **Immutability Proof:** Mathematical proof of the hash chain integrity mechanism in Layer 7.
