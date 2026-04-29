# Contributing to AVIK Sandbox Shield

Thank you for your interest in contributing to AVIK Sandbox Shield! This project aims to create the definitive reference architecture for AI containment, and we welcome contributions from security researchers, AI safety engineers, systems programmers, and anyone passionate about safe AI deployment.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Submission Guidelines](#submission-guidelines)
- [Security Vulnerability Reporting](#security-vulnerability-reporting)
- [Style Guides](#style-guides)
- [Community](#community)

---

## 📜 Code of Conduct

This project adheres to the [AVIK Sandbox Shield Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@avik-shield.dev].

---

## 🤝 How Can I Contribute?

### Priority Areas

We are especially looking for contributions in these areas:

| Area | Description | Difficulty |
|------|-------------|------------|
| **Layer Implementations** | Reference implementations for each of the 8 layers | Advanced |
| **Formal Verification** | Mathematical proofs of containment properties | Expert |
| **Hardware Integration** | Guides for specific data diode and kill switch hardware | Advanced |
| **Compliance Tooling** | Scripts and tools for compliance validation | Intermediate |
| **Threat Model Extensions** | New threat vectors and mitigation strategies | Intermediate |
| **Documentation** | Improving guides, tutorials, and API docs | Beginner-Friendly |
| **Examples** | Real-world deployment examples and case studies | Intermediate |

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

**When filing a bug report, include:**
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, kernel version, hypervisor version, etc.)
- Any relevant logs or configuration files

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:
- A clear description of the proposed enhancement
- The motivation and use case
- How it fits into the 8-layer architecture
- Any potential security implications

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-contribution`)
3. Make your changes following our [style guides](#style-guides)
4. Add or update tests as appropriate
5. Update documentation to reflect your changes
6. Commit with clear, descriptive messages
7. Push to your fork and submit a Pull Request

---

## 🛠️ Development Setup

### Prerequisites

- Linux host (kernel ≥ 5.10) with KVM support
- Python ≥ 3.11
- Go ≥ 1.21 (for certain layer implementations)
- Docker (for testing)
- ShellCheck (for script validation)

### Getting Started

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/avik-sandbox-shield.git
cd avik-sandbox-shield

# Verify prerequisites
./scripts/check-prerequisites.sh

# Run tests
./scripts/run-tests.sh
```

---

## 📝 Submission Guidelines

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `security`

**Scopes:** `layer-1` through `layer-8`, `docs`, `scripts`, `compliance`, `core`

**Examples:**
```
feat(layer-3): add Firecracker microVM provisioning script
fix(layer-7): correct Merkle tree hash chain verification
docs(layer-5): add guardian model deployment guide
security(layer-4): patch prompt injection bypass in schema validator
```

### Branch Naming

```
feature/layer-X-description    # New features
fix/layer-X-description        # Bug fixes
docs/description               # Documentation updates
security/description           # Security patches
```

---

## 🔒 Security Vulnerability Reporting

> **⚠️ Do NOT file security vulnerabilities as public GitHub issues.**

If you discover a security vulnerability in any layer of AVIK Shield, please report it responsibly:

1. **Email:** security@avik-shield.dev
2. **Subject:** `[AVIK-VULN] Brief Description`
3. **Include:** Affected layer(s), reproduction steps, potential impact, and suggested fix
4. **Response Time:** We aim to acknowledge within 48 hours and provide a fix timeline within 7 days

We follow [Coordinated Vulnerability Disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure) practices.

---

## 🎨 Style Guides

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use `black` for formatting and `ruff` for linting

### Shell Scripts

- Use `#!/usr/bin/env bash`
- Follow [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- All scripts must pass `shellcheck`
- Use `set -euo pipefail` at the top of every script

### Go

- Follow standard `gofmt` formatting
- Use `golangci-lint` for linting
- Write table-driven tests

### Documentation

- Use Markdown with proper heading hierarchy
- Include Mermaid diagrams for architectural concepts
- Provide code examples for all configuration options
- Keep language clear, precise, and unambiguous

---

## 🌐 Community

- **Discussions:** GitHub Discussions for questions and general conversation
- **Issues:** GitHub Issues for bugs and feature requests
- **Security:** security@avik-shield.dev for vulnerability reports

---

## 📄 License

By contributing to AVIK Sandbox Shield, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

---

<p align="center">
  <strong>Thank you for helping make AI containment safer for everyone. 🛡️</strong>
</p>
