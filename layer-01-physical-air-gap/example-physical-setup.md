# Example: Real-World Physical Setup

This document walks through a practical, real-world example of preparing a standard workstation for AVIK Shield Layer 1 compliance.

## The Objective
Transform a commercial-off-the-shelf (COTS) workstation (e.g., a Lenovo ThinkStation or a custom-built GPU rig) into a mathematically verifiable air-gapped node.

---

## Step 1: Procurement & Chain of Custody
1. **New Hardware:** Never use a machine that has previously been connected to an untrusted network. Purchase new hardware in cash if absolute operational security is required.
2. **Verification:** Inspect the motherboard and components for tampering or unexpected hardware implants upon unboxing.

## Step 2: The Physical "Lobotomy"
Software hardening (like `setup-airgap.sh`) is insufficient. If a zero-day kernel exploit compromises the host, it can re-enable disabled network drivers. True compliance requires hardware modification.

1. **Remove Wireless Modules:** 
   - Open the chassis.
   - Locate the M.2 Wi-Fi/Bluetooth card.
   - Unscrew and physically remove the card. Destroy it or store it outside the facility.
2. **Disable Audio (Side-Channel Prevention):**
   - Disconnect internal speakers from the motherboard.
   - If the motherboard has integrated microphones, physically remove or destroy them.
3. **Port Blocking (Epoxy):**
   - Identify which USB ports are strictly necessary for initial configuration (keyboard/mouse).
   - Fill all unused USB, Thunderbolt, HDMI, and RJ45 Ethernet ports with industrial epoxy or specialized tamper-evident physical port blockers.

## Step 3: Installing the Data Diode Interface
1. Install an SFP+ Fiber Network Card into a PCIe slot.
2. Connect a simplex fiber cable to the TX (transmit) port of the card.
3. Leave the RX (receive) port completely unpopulated.

## Step 4: The Faraday Enclosure
To protect against advanced EM side-channel attacks (where an AI pulses the GPU to emit radio frequencies):
1. Place the entire workstation inside a specialized RF-shielded Faraday tent or cabinet.
2. Route the fiber optic cable out of the enclosure. (Fiber optic cables are immune to EM interference and do not break the Faraday cage's integrity).
3. Ensure the power cable passing into the cage utilizes a high-grade power line filter.

## Step 5: Software Hardening
1. Boot the machine using a verified Linux ISO flashed to a read-only USB drive (using a hardware write-blocker).
2. Install the base OS.
3. Execute `sudo ./setup-airgap.sh` to apply the software-level module blacklists.
4. Execute the Python verification script to confirm zero logical paths exist.

## The Result
You now possess a compute node that is physically incapable of receiving external commands or wirelessly transmitting its data, representing a perfect Layer 1 foundation for the AVIK Sandbox Shield.
