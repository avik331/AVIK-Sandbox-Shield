<div align="center">
  <h1>🛡️ AVIK Shield Layer 1: Physical Air-Gap</h1>
  <p><b>The foundational barrier against network-based compromise and exfiltration.</b></p>
</div>

---

## 📖 Overview

The Physical Air-Gap Layer is the bedrock of the AVIK Sandbox Shield Framework. Designed by Avik Chakraborty, this layer enforces isolation through physical separation and strict configuration hardening. Its singular purpose is to ensure that the contained AI environment has zero logical or physical pathways to an external network.

In the AVIK framework, we consider software-based isolation (like VLANs or hypervisor firewalls) fundamentally insufficient against frontier-level models capable of generating novel zero-day exploits. Layer 1 establishes a mathematical impossibility for standard network transmission.

## ⚠️ Threats Defeated

- **Remote Code Execution (RCE) / Command & Control (C2):** An external attacker physically cannot reach the internal system to execute commands or update payloads.
- **Data Exfiltration:** Even if the core model successfully generates a payload containing sensitive weights, API keys, or operational data, it has no network interface to transmit it outward.
- **Electromagnetic (EM) Side-Channels (when combined with Faraday casing):** Prevents the model from modulating CPU frequencies to emit radio signals (TEMPEST attacks).
- **Supply Chain Beacons:** Prevents compromised hardware components from "phoning home" to arbitrary command servers.

## 🛠️ Module Components

This module is designed to be the "golden staff" to which you bring your own hardware. It provides:

1. **`setup-airgap.sh`**: An aggressive Linux hardening script that disables and blacklists all networking stacks, wireless drivers, and non-essential USB protocols.
2. **`airgap-module.py`**: The official Python API interface for Layer 1. It actively verifies the integrity of the air-gap and provides secure, unidirectional-only data staging interfaces.
3. **[Connection Interface Specification](connection-interface.md)**: The strict rules for how Layer 2 (Data Diode) attaches to this layer.
4. **[Physical Setup Guide](example-physical-setup.md)**: A real-world walkthrough of modifying off-the-shelf hardware for true Layer 1 compliance.

## 🚀 Step-by-Step Setup Guide

To properly deploy the Layer 1 module:

1. **Procure Dedicated Hardware:** Obtain a machine that will *never* connect to the internet again.
2. **Physical Modifications:** Physically remove Wi-Fi/Bluetooth M.2 cards and epoxy unused USB ports (see `example-physical-setup.md`).
3. **OS Installation:** Install a minimal Linux distribution via a trusted, read-only USB drive.
4. **Execute Hardening Script:**
   ```bash
   sudo chmod +x setup-airgap.sh
   sudo ./setup-airgap.sh
   ```
5. **Verify Air-Gap Status:**
   Run the Python verification module to assert the system state.
   ```bash
   python3 -c "from airgap_module import verify_airgap; verify_airgap()"
   ```

## 🔌 Connection Interface

Layer 1 is designed to be a sealed box. The *only* approved method for extracting data (such as Layer 5 Guardian logs or Layer 6 eBPF metrics) from this air-gapped system is via **Layer 2 (Hardware Data Diode)**. 

Please refer to the [Connection Interface Document](connection-interface.md) for the exact physical and software specifications required to bridge Layer 1 to Layer 2 without breaking compliance.
