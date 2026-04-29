# AVIK Shield Scripts

This directory contains utility scripts for validating, deploying, and testing the AVIK Sandbox Shield framework.

## Available Scripts

### `check-prerequisites.sh`
Validates that the host system meets all necessary requirements for deploying the software layers of the shield (e.g., checks for KVM support, required Python/Go versions, and Docker).

### `deploy-layer3.sh`
A helper script to automatically build a minimal Linux kernel and rootfs, and launch a test Firecracker microVM.

### `compliance-check.sh`
The core validation script. It checks the presence and configuration of all 8 layers. For physical layers (1, 2, and 8), it relies on cryptographic attestations provided by the hardware during setup.

### `run-tests.sh`
Executes the test suite across all implemented software layers.

## Usage

All scripts should be executed from the root of the repository:

```bash
./scripts/check-prerequisites.sh
```

Ensure scripts have execute permissions (`chmod +x scripts/*.sh`).
