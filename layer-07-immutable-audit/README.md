<div align="center">
  <h1>🛡️ AVIK Shield Layer 7: Immutable Audit</h1>
  <p><b>Cryptographically verifiable, append-only ledgers to guarantee absolute forensic integrity.</b></p>
</div>

---

## 📖 Overview

Standard log files are vulnerable. If an advanced AI escapes containment or a malicious insider attempts to sabotage the sandbox, their first action will be to erase or alter the logs to cover their tracks. 

The **Immutable Audit Layer** ensures that once an event occurs, it is cryptographically locked into the historical record forever. By utilizing a continuous Merkle Tree and blockchain-style cryptographic chaining, Layer 7 guarantees that any attempt to alter, delete, or insert a past log entry will mathematically invalidate the entire ledger, instantly alerting administrators to the tampering.

Crucially, Layer 7 sits **outside** the physical air-gap. It receives data exclusively via the Layer 2 Hardware Data Diode, meaning the core LLM has absolutely zero physical path to reach the ledger to tamper with it.

## ⚠️ Threats Defeated

- **Log Tampering:** Cryptographic chaining makes it computationally infeasible to alter a past log entry without recalculating all subsequent hashes.
- **Evidence Destruction:** Because logs are streamed through a one-way diode instantly, the core model cannot "delete" logs before they are written to the immutable ledger.
- **Audit Forgery:** Ensures that forensic investigators can prove mathematically that the log record exactly matches what the system originally produced.
- **Insider Threat / Cover-up:** A rogue administrator cannot easily alter the logs post-incident without invalidating the Merkle Root.

## 🛠️ Module Components

1. **`merkle-tree.py`**: A robust, standalone Python implementation of a Merkle Tree used to generate the cryptographic proofs.
2. **`immutable-audit.py`**: The core daemon that receives events, structures them into blocks, appends them to the ledger, and updates the Merkle Root.
3. **`setup-audit-ledger.sh`**: Initializes the secure, append-only directory structure for the ledger on the external host.
4. **`test-audit-integrity.py`**: A verification suite that deliberately tampers with the ledger and proves that the cryptographic validation catches the forgery.
5. **[Connection Interface Specification](connection-interface.md)**: Details the flow from Layer 2 to Layer 7.
6. **[Example Audit Log](example-audit-log.md)**: Shows the JSON structure of the cryptographic ledger.

## 🚀 Quick Start

1. **Initialize the Ledger:**
   ```bash
   sudo ./setup-audit-ledger.sh
   ```
2. **Start the Audit Daemon:**
   ```bash
   python3 immutable-audit.py
   ```
3. **Verify Cryptographic Integrity:**
   ```bash
   python3 test-audit-integrity.py
   ```

## 🔌 Connection Interface

Layer 7 is completely decoupled from the execution environment. 

- **Ingress:** It listens promiscuously on the external side of the Layer 2 Hardware Data Diode. It ingests all telemetry, LLM inputs/outputs, Layer 5 Guardian alerts, and Layer 6 Anomaly triggers.
- **Egress:** It does not communicate outward. It writes locally to highly secure, append-only storage.

Please refer to the [Connection Interface Document](connection-interface.md) for architectural specifics.
