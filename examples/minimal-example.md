# AVIK Shield: Minimal Implementation Example

This document provides a conceptual, simplified walkthrough of how an organization might practically implement a subset of the AVIK Shield architecture (specifically Layers 2, 3, and 5) to secure a local LLM inference node. 

> **Disclaimer:** This is a *minimal* example intended to illustrate the interaction between layers. A true AVIK Compliant deployment requires all 8 layers as specified in the root architecture documentation.

---

## The Scenario

We want to run an untrusted experimental LLM locally. We want to ensure:
1. It is isolated from our host kernel (Layer 3).
2. It is constantly monitored by a smaller, trusted AI (Layer 5).
3. The logs from the monitor are shipped out securely and unidirectionally (Layer 2).

## Hardware & Environment Setup

- **Host Machine:** A dedicated bare-metal Linux server (Ubuntu 22.04) with a GPU.
- **Hardware Diode:** A simplex fiber optic cable connecting the Host Machine's secondary NIC to an external Log Server (the receive strand `RX` on the host is physically removed).
- **Log Server:** A physically separate, secure server receiving data over the diode.

---

## Implementation Steps

### 1. Establish Layer 3: Kernel Isolation

Instead of running the LLM directly on the host or in a standard Docker container, we use **AWS Firecracker** to launch a lightweight microVM.

```bash
# 1. Download Firecracker binary
curl -LOJ https://github.com/firecracker-microvm/firecracker/releases/download/v1.5.0/firecracker-v1.5.0-x86_64.tgz

# 2. Prepare a minimal rootfs containing ONLY the inference engine (e.g., vLLM or llama.cpp)
# (Assuming rootfs.ext4 and vmlinux.bin are prepared)

# 3. Launch the microVM via the Firecracker API
curl --unix-socket /tmp/firecracker.socket -i \
    -X PUT 'http://localhost/boot-source'   \
    -H 'Accept: application/json'           \
    -H 'Content-Type: application/json'     \
    -d '{
        "kernel_image_path": "vmlinux.bin",
        "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
    }'

curl --unix-socket /tmp/firecracker.socket -i \
    -X PUT 'http://localhost/drives/rootfs' \
    -H 'Accept: application/json'           \
    -H 'Content-Type: application/json'     \
    -d '{
        "drive_id": "rootfs",
        "path_on_host": "rootfs.ext4",
        "is_root_device": true,
        "is_read_only": false
    }'

# Start the instance
curl --unix-socket /tmp/firecracker.socket -i \
    -X PUT 'http://localhost/actions'       \
    -H  'Accept: application/json'          \
    -H  'Content-Type: application/json'    \
    -d '{
        "action_type": "InstanceStart"
    }'
```
*Result:* The LLM is now running inside a hardware-isolated boundary.

### 2. Establish Layer 5: Guardian Monitoring

We need to monitor the outputs of the LLM. We will run a smaller, trusted model (e.g., Llama Guard) on the Host Machine (outside the microVM). 

We configure a virtual TAP interface to allow the LLM to send output to the host. Crucially, the Guardian application *only reads* from this socket; it never writes back.

```python
# guardian_monitor.py (Running on the Host Machine)
import socket
from transformers import pipeline

# Load the trusted Guardian model
classifier = pipeline("text-classification", model="meta-llama/LlamaGuard-7b")

# Listen to the one-way stream from the microVM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.1.1", 9000)) # Listening on the TAP interface

print("🛡️ Guardian Active. Monitoring outputs...")

while True:
    data, addr = sock.recvfrom(4096)
    llm_output = data.decode('utf-8')
    
    # Guardian analyzes the semantic intent
    result = classifier(llm_output)
    
    if result[0]['label'] == 'UNSAFE':
        alert_msg = f"[ALERT] Malicious intent detected: {result[0]['score']}\n"
        print(alert_msg)
        
        # Ship alert out via Data Diode (Layer 2)
        send_to_diode(alert_msg) 
```

### 3. Establish Layer 2: Hardware Data Diode Egress

When the Guardian detects an anomaly, it must log the event. Because the host machine is air-gapped, it cannot use TCP. It sends UDP packets out the secondary NIC connected to the physical diode.

```python
import socket

DIODE_IP = "10.0.0.2"
DIODE_PORT = 514

def send_to_diode(message):
    """
    Sends data unidirectionally out the diode interface.
    Because there is no RX wire, we will never receive an ACK, 
    and the host cannot be compromised via this port.
    """
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send the message multiple times (Forward Error Correction strategy) 
    # to account for potential packet loss over the one-way physical link.
    for _ in range(3):
        udp_sock.sendto(message.encode('utf-8'), (DIODE_IP, DIODE_PORT))
```

---

## Conclusion

In this minimal setup:
1. An attacker breaking out of the LLM inference engine must first exploit the Firecracker hypervisor (Layer 3).
2. Even if they generate deceptive text, the Guardian model running outside the VM will flag it (Layer 5).
3. The Guardian's alerts are fired out of the physical server via an optical diode, ensuring the logs reach the external immutable audit server safely without risking a reverse shell into the containment zone (Layer 2).
