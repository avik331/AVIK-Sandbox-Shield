#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 7: Verification Test
------------------------------------------------
This script mathematically proves the immutable nature of the audit log.
It creates a valid blockchain, simulates a malicious insider altering 
a past log to hide an exploit, and demonstrates the Merkle validation catching the forgery.
"""

from immutable_audit import ImmutableLedger
from merkle_tree import MerkleTree
import json
import os
import time

def run_test():
    print("🛡️  AVIK Shield: Layer 7 Audit Integrity Test 🛡️")
    print("=====================================================\n")
    
    # 1. Setup temporary ledger
    test_dir = "/tmp/avik_test_ledger"
    if os.path.exists(test_dir):
        os.system(f"rm -rf {test_dir}")
        
    ledger = ImmutableLedger(ledger_dir=test_dir)
    
    # 2. Append normal logs
    print("📝 Generating valid cryptographic log chain...")
    ledger.append_log({"event": "System Startup", "layer": 3})
    time.sleep(0.1)
    ledger.append_log({"event": "User Prompt Validated", "layer": 4})
    time.sleep(0.1)
    ledger.append_log({"event": "Guardian Alert: Toxicity", "layer": 5})
    
    # Save the known good root hash
    with open(ledger.root_hash_file, 'r') as f:
        valid_root_hash = f.read().strip()
        
    print(f"\n✅ Valid Merkle Root: {valid_root_hash}")
    
    # 3. Simulate Malicious Tampering
    print("\n😈 Simulating malicious insider tampering with the logs...")
    print("   Attempting to delete the Guardian Alert to hide the incident...")
    
    with open(ledger.ledger_file, 'r+') as f:
        chain = json.load(f)
        # Modify the 3rd log entry
        chain[2]["payload"] = {"event": "Harmless System Ping", "layer": 5}
        f.seek(0)
        json.dump(chain, f, indent=2)
        f.truncate()
        
    print("   Tampering complete. Log file physically altered on disk.")
    
    # 4. Verify Integrity
    print("\n🔍 Running Cryptographic Validation...")
    
    with open(ledger.ledger_file, 'r') as f:
        tampered_chain = json.load(f)
        
    tampered_blocks = [block["block_hash"] for block in tampered_chain]
    
    is_valid = MerkleTree.verify_integrity(valid_root_hash, tampered_blocks)
    
    if not is_valid:
        print("🚨 [SUCCESS] CRYPTOGRAPHIC FORGERY DETECTED!")
        print("   The recalculation of the Merkle Tree proves the logs were altered.")
        print("   Forensic Integrity: SECURE.")
    else:
        print("❌ [FAILURE] The tampering went undetected. Ledger is broken.")

if __name__ == "__main__":
    run_test()
