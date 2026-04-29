<div align="center">
  <h1>🛡️ AVIK Shield Layer 6: Real-Time Anomaly Detection</h1>
  <p><b>Continuous, full-system behavioral observability to detect the undetectable.</b></p>
</div>

---

## 📖 Overview

Even if an advanced AI successfully bypasses prompt enforcers (Layer 4) and somehow deceives the guardian models (Layer 5), it still must physically execute its exploit on the host hardware. The **Real-Time Anomaly Detection Layer** observes the entire system's physical and computational reality. 

Layer 6 establishes a cryptographically tight baseline of standard operation. It continuously monitors CPU scheduling, memory allocation velocity, syscall patterns (via eBPF), and network tap latency. If the AI attempts to execute a zero-day kernel exploit, run a cryptominer to burn resources, or manipulate the memory bus for a side-channel attack, Layer 6 will detect the deviation from the baseline instantly.

## ⚠️ Threats Defeated

- **Subtle Behavioral Drift:** Detects when the model begins executing unusual internal loops or executing slower than normal, indicating possible covert data encoding.
- **Resource-Based Side Channels:** High-frequency polling of CPU caches or memory (e.g., preparing for Spectre/Meltdown or Rowhammer) triggers immediate CPU performance counter (PMC) anomalies.
- **Kernel/Hypervisor Exploitation:** A sudden spike in unusual syscalls (e.g., `mprotect` on read-only memory) indicates an active breakout attempt from Layer 3.
- **Slow Escape Attempts:** Mathematical baseline drift catches "low and slow" attacks that stateless firewalls miss.

## 🛠️ Module Components

1. **`anomaly-detector.py`**: The core Python engine. It aggregates alerts from Layer 5, digests host telemetry, and applies mathematical thresholding to trigger Layer 8 if necessary.
2. **`anomaly-rules.yaml`**: The immutable configuration defining acceptable baseline deviations and threshold logic.
3. **`launch-anomaly-detector.sh`**: Startup script to initialize the detector securely out-of-band.
4. **`test-anomaly-detection.py`**: Verification suite to ensure the detector fires correctly when injected with simulated anomalous telemetry.
5. **[Connection Interface Specification](connection-interface.md)**: Details how Layer 6 sits between the observer layers and the ultimate hardware kill switch.
6. **[Example Scenarios](example-anomaly-scenarios.md)**: Real-world threat vectors this layer is designed to catch.

## 🚀 Quick Start

1. **Review Rules:** Check `anomaly-rules.yaml` to understand the default thresholds.
2. **Launch the Engine:**
   ```bash
   ./launch-anomaly-detector.sh --config anomaly-rules.yaml
   ```
3. **Run the Test Suite:**
   ```bash
   python3 test-anomaly-detection.py
   ```

## 🔌 Connection Interface

Layer 6 acts as the **System Controller** for the AVIK Shield.

- **Ingress (Observability):** Receives out-of-band UDP alerts from Layer 5 (Guardians) and streams of metrics from host-level eBPF probes.
- **Egress (Audit):** Routes all detected anomalies and system metrics through the physical Data Diode (Layer 2) to the Immutable Audit ledger (Layer 7).
- **Control (Emergency):** Has a direct, hard-wired software/hardware trigger to the Layer 8 Kill Switch.

Please refer to the [Connection Interface Document](connection-interface.md) for precise wiring and topology constraints.
