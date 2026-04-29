# Layer 6: Real-Time Anomaly Detection

## 🛡️ Purpose of the Layer
While Layer 5 observes the *mind* of the AI (semantics and logic), Layer 6 observes the *body* (the physical computing environment). The Real-Time Anomaly Detection layer establishes a cryptographically tight baseline of what normal execution looks like. Any deviation—a strange syscall, a spike in PCIe bus traffic, an unexpected memory allocation—triggers immediate alerts.

## ⚠️ Specific Threats Defeated
- **Zero-Day Exploit Execution:** Detects the specific syscall patterns (like unusual `mprotect` or `execve` calls) associated with kernel or hypervisor exploitation attempts.
- **Cryptojacking & Resource Abuse:** Identifies computational loops or unauthorized compute workloads that do not match the expected inference profile.
- **Network Scanning & Breakout Attempts:** Flags any attempt by the contained system to map local interfaces or construct raw IP packets.
- **Side-Channel Preparation:** Detects the high-frequency CPU/Memory polling patterns often required to execute local side-channel attacks like Spectre or Rowhammer.

## ⚙️ Recommended Real-World Technologies
- **eBPF (Extended Berkeley Packet Filter):** High-performance, in-kernel virtual machine used to trace syscalls, network packets, and VFS operations with near-zero overhead.
- **Prometheus & Grafana:** For aggregating metrics and visualizing deviations (hosted strictly outside the isolation boundary).
- **Statistical ML Profilers:** Models trained on the specific AI workload's baseline to detect subtle anomalies in hardware performance counters (PMCs).
- **Host Intrusion Detection Systems (HIDS):** Agents like Falco or OSSEC, tuned for zero-tolerance environments.

## ☑️ Implementation Checklist
- [ ] Run the AI workload in a known-safe, disconnected state to generate an exhaustive cryptographic baseline of acceptable behavior.
- [ ] Deploy eBPF probes at the host kernel level, completely invisible to the guest microVMs.
- [ ] Host the anomaly detection engine on a dedicated management plane, physically separate from the compute nodes running the AI.
- [ ] Configure thresholds for **Fail-Closed**: in an AI containment scenario, false positives (unnecessary shutdowns) are infinitely preferable to false negatives (allowing an escape).
- [ ] Hardwire critical anomaly triggers directly to Layer 8 (Emergency Termination) for sub-second reaction times.

## 🔒 Security Guarantees Provided
This layer provides **Execution Environment Integrity**. It guarantees that the physical and logical realities of the compute host cannot be altered without immediate, out-of-band detection.
