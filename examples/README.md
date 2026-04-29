# AVIK Shield Examples

This directory contains reference implementations and examples for integrating and deploying the AVIK Sandbox Shield framework.

## Available Examples

### 1. `basic-prompt-enforcer`
A Python example demonstrating Layer 4 (Prompt Enforcement) using Pydantic schemas and strict token filtering.

### 2. `firecracker-microvm-setup`
A reference configuration and deployment script for Layer 3 (Kernel Isolation) using AWS Firecracker to spin up an ephemeral microVM.

### 3. `audit-logger-merkle`
A Go-based example of Layer 7 (Immutable Audit) implementing a basic Merkle tree hash chain for tamper-proof logging.

## Usage

Each example contains its own `README.md` with specific prerequisites and instructions.

> **Note:** These are *examples* intended for educational and developmental purposes. Do not deploy these directly into production environments without thorough security review and adaptation to your specific hardware.
