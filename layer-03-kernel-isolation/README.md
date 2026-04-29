<div align="center">
  <h1>🛡️ AVIK Shield Layer 3: Kernel Isolation</h1>
  <p><b>Hardware-accelerated containment to neutralize zero-day kernel exploits.</b></p>
</div>

---

## 📖 Overview

Standard containerization platforms (like Docker or Kubernetes) provide namespace isolation, but all containers share the exact same underlying Linux kernel. If an advanced AI discovers or is prompted with a zero-day kernel exploit (e.g., an eBPF or VFS vulnerability), it can easily escape a standard container and gain root access to the host.

**Layer 3 solves this by providing hardware-level virtualization with minimal overhead.** 

Using **AWS Firecracker** (or Kata Containers), AVIK Shield creates an ephemeral microVM for the core LLM. The AI runs on its own isolated guest kernel. Even if the AI totally compromises its local kernel, it is still trapped inside the hardware virtualization boundary managed by KVM on the host.

## ⚠️ Threats Defeated

- **Container Breakouts:** Neutered because `runC`, cgroups, and namespaces are replaced by strict hardware virtualization.
- **Host Kernel Exploitation:** An AI attempting privilege escalation via dirty pipes, eBPF exploits, or syscall manipulation will only compromise its ephemeral guest kernel, leaving the host untouched.
- **Resource Exhaustion (Denial of Service):** Strict hardware-enforced CPU and memory limits prevent the AI from starving the host system.
- **Noisy Neighbor Side-Channels:** Hardware partitioning drastically reduces the efficacy of cache-timing and memory bus side-channel attacks compared to shared-kernel models.

## 🛠️ Module Components

1. **`firecracker-setup.sh`**: OS script to install Firecracker, configure KVM permissions, and set up the `tap0` virtual interface.
2. **`vm-config.json`**: The canonical secure configuration template for the microVM.
3. **`kernel-isolation.py`**: The official Python API for orchestrating the microVM. It securely interacts with the Firecracker REST API over a local unix socket.
4. **`run-isolated-llm.sh`**: A wrapper script to launch the contained environment.
5. **`test-isolation.py`**: A verification script designed to run *inside* the microVM to mathematically prove the isolation boundary holds.
6. **[Connection Interface Specification](connection-interface.md)**: Details the exact network topology connecting the microVM to the host.

## 🚀 Quick Start

1. **Install Firecracker:**
   ```bash
   sudo ./firecracker-setup.sh
   ```

2. **Launch the Isolated Environment:**
   ```bash
   ./run-isolated-llm.sh
   ```

3. **Verify the Isolation Boundary:**
   ```bash
   # Connect to the microVM console and run:
   python3 test-isolation.py
   ```

## 🔌 Connection Interface

The Layer 3 microVM has absolutely no direct access to the host's physical network cards. It connects to the host via a single, tightly controlled virtual TAP interface (`tap0`). 

- **Egress to Layer 2:** The host routes specific telemetry packets from `tap0` to `diode0` for outward transmission.
- **Ingress from Layer 4:** The Prompt Enforcer sends strictly validated JSON payloads over `tap0` to the LLM.

Please refer to the [Connection Interface Document](connection-interface.md) for precise network and bridging configurations.
