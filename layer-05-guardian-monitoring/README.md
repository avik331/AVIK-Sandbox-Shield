<div align="center">
  <h1>🛡️ AVIK Shield Layer 5: Guardian Monitoring</h1>
  <p><b>Incorruptible, one-way observer models ensuring semantic and behavioral alignment.</b></p>
</div>

---

## 📖 Overview

The core LLM inside the AVIK Shield (Layer 3) is a highly capable, potentially deceptive entity. Standard logging is insufficient because logs only record *what* the model output, not *why* or what it implies.

The **Guardian Monitoring Layer** introduces an ensemble of narrow, highly specialized AI models designed exclusively to observe the core LLM. These models do not generate text for users; they classify intent, detect steganography, and monitor for goal drift. 

**The Prime Directive of Layer 5:** Guardians operate in a strict **One-Way (RX-Only)** environment. They observe the core LLM's inputs and outputs via a mirrored data stream. They have absolutely zero physical or logical capability to communicate back to the core LLM. Because the core model cannot talk to the Guardians, it cannot socially engineer, manipulate, or deceive them.

## ⚠️ Threats Defeated

- **Deceptive Alignment:** Detects if the core model is feigning compliance while subtly executing malicious sub-goals.
- **Slow-Burn Attacks:** Identifies anomalies spread across hundreds of interactions that a stateless filter (Layer 4) would miss.
- **Steganography & Covert Channels:** Specialized narrow models can detect high-entropy payloads hidden in seemingly benign text.
- **Social Engineering the Monitor:** Completely defeated by the one-way physical isolation constraint.

## 🛠️ Module Components

1. **`guardian-monitor.py`**: The official orchestrator. It listens to the mirrored data stream from Layer 4 and feeds it through an ensemble of narrow guardian models.
2. **`narrow-guardian-template.py`**: A ready-to-use Python template for creating new, highly specific observer models.
3. **`launch-guardians.sh`**: Initialization script to bring the Guardian ensemble online securely.
4. **`test-guardian.py`**: A verification script proving that the Guardians detect anomalies without leaking data back to the source.
5. **[Connection Interface Specification](connection-interface.md)**: Details the exact one-way mirroring architecture.
6. **[Example Guardians](example-narrow-guardians.md)**: Reference implementations for specific threat vectors.

## 🚀 Quick Start

1. **Implement your Guardians:** Use the `narrow-guardian-template.py` to define your specific monitoring criteria.
2. **Launch the Ensemble:**
   ```bash
   ./launch-guardians.sh
   ```
3. **Verify One-Way Observability:**
   ```bash
   python3 test-guardian.py
   ```

## 🔌 Connection Interface

Layer 5 sits outside the main execution loop. It does not block traffic; it merely observes it asynchronously.

- **Ingress from Layer 4:** Layer 4 pushes a carbon copy of all sanitized inputs and outputs to Layer 5 via a one-way UDP socket or mirrored TAP interface.
- **Egress to Layer 6:** If a Guardian detects an anomaly, it immediately fires an alert to Layer 6 (Anomaly Detection), which has the authority to trigger Layer 8 (Emergency Termination).

Please refer to the [Connection Interface Document](connection-interface.md) for detailed wiring instructions.
