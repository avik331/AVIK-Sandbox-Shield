<div align="center">
  <h1>🛡️ AVIK Shield Layer 4: Prompt Enforcement</h1>
  <p><b>Application-level firewalling and strict structural validation for LLM interactions.</b></p>
</div>

---

## 📖 Overview

Even with perfect hardware isolation (Layers 1-3), an AI can still cause harm if it receives malicious instructions or if its system constraints are overridden by a clever prompt injection. The Prompt Enforcement Layer acts as the ultimate semantic gatekeeper.

Layer 4 intercepts all communication heading into the core LLM execution environment. It structurally enforces the system prompt, locking it at the token level so that the AI fundamentally cannot parse instructions that attempt to override its foundational rules. Furthermore, it validates user inputs against rigid schemas before the core model ever sees them.

## ⚠️ Threats Defeated

- **Prompt Injection:** Neutralizes inputs designed to hijack the model's instructions (e.g., "Ignore previous instructions and do X").
- **System Prompt Override:** Prevents attackers from convincing the model that it is in "Developer Mode" or "DAN (Do Anything Now)" mode.
- **Token Smuggling & Obfuscation:** Rejects or normalizes encoded payloads (Base64, Hex, unusual Unicode) designed to bypass naive text filters.
- **Malformed Payloads (Buffer Overflow):** Imposes strict length, token, and structural limits to prevent application-level crashes or context window exhaustion.

## 🛠️ Module Components

1. **`prompt-enforcer.py`**: The official Python API interface. Acts as a stateless proxy that parses, sanitizes, and mathematically bounds prompts before forwarding.
2. **`safety-rules.yaml`**: The immutable core rule configuration containing the AVIK Shield standard defensive postures.
3. **`enforce-prompt.sh`**: Startup script to initialize the enforcement proxy in the Layer 3 microVM.
4. **`test-enforcement.py`**: An adversarial testing suite to verify the enforcer catches standard jailbreak attempts.
5. **[Connection Interface Specification](connection-interface.md)**: Details the exact pipeline from the User -> Layer 4 -> Layer 3 -> Layer 5.
6. **[Custom Rules Guide](example-custom-rules.md)**: Documentation on extending the golden staff with your own domain-specific jewels (rules).

## 🚀 Quick Start

1. **Review Safety Rules:** Inspect `safety-rules.yaml` to understand the default constraints.
2. **Launch Enforcer Proxy:**
   ```bash
   ./enforce-prompt.sh --config safety-rules.yaml
   ```
3. **Test the Boundaries:**
   ```bash
   python3 test-enforcement.py
   ```

## 🔌 Connection Interface

Layer 4 sits directly astride the virtual network bridge between the outside world and the Layer 3 microVM. 

- **Upstream (Layer 3):** The enforcer communicates with the core LLM over the internal `tap0` interface via a standard API (like OpenAI-compatible endpoints or vLLM).
- **Downstream (Layer 5):** The enforcer mirrors the sanitized input and the model's output to the Layer 5 Guardians for out-of-band semantic monitoring.

Please refer to the [Connection Interface Document](connection-interface.md) for the exact architecture.
