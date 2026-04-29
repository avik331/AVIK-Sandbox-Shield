# Security Policy

## Supported Versions

The AVIK Sandbox Shield Framework is currently a reference architecture. However, we take the security of its core components and documentation extremely seriously.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**DO NOT OPEN A PUBLIC GITHUB ISSUE TO REPORT A VULNERABILITY.**

Because AVIK Shield is designed to contain advanced AI systems, public disclosure of a theoretical bypass or implementation flaw could present a severe risk to active deployments before mitigations are available.

If you discover a vulnerability in the architectural design, reference scripts, or recommended technologies:

1. Send an email to **security@avik-shield.dev**
2. Include "[VULN]" in the subject line.
3. Provide a detailed description of the exploit vector, the affected layer(s), and step-by-step instructions to reproduce the issue.
4. If applicable, suggest a mitigation or architectural adjustment.

### Our Response Process
- We will acknowledge receipt of your vulnerability report within **48 hours**.
- We aim to provide a detailed assessment and an initial mitigation plan within **7 days**.
- We adhere to a 90-day Coordinated Vulnerability Disclosure (CVD) timeline.

### Scope
Vulnerabilities in third-party software recommended by this framework (e.g., AWS Firecracker, Kata Containers, eBPF) should be reported directly to those respective upstream projects. However, please notify us simultaneously so we can update our reference architecture and provide temporary mitigations to the AVIK community.
