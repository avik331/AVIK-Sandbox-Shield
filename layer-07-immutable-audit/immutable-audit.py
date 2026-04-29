#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 7: Immutable Audit Daemon
-----------------------------------------------------
Receives incoming system logs (via UDP from the Diode), chains them 
cryptographically to previous logs, and writes them to an append-only ledger.
Periodically computes the Merkle Root for the entire log chain.
"""

import socket
import json
import time
import hashlib
import os
import logging
from typing import Dict, Any, List
from merkle_tree import MerkleTree

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L7-AUDIT] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer7")

class ImmutableLedger:
    def __init__(self, ledger_dir: str = "/var/log/avik_ledger"):
        self.ledger_dir = ledger_dir
        self.ledger_file = os.path.join(self.ledger_dir, "blockchain.json")
        self.root_hash_file = os.path.join(self.ledger_dir, "merkle_root.sha256")
        self.last_block_hash = "0" * 64 # Genesis hash
        
        self._ensure_setup()
        self._load_state()

    def _ensure_setup(self):
        if not os.path.exists(self.ledger_dir):
            os.makedirs(self.ledger_dir, mode=0o700)
            
        if not os.path.exists(self.ledger_file):
            with open(self.ledger_file, 'w') as f:
                pass

    def _load_state(self):
        try:
            with open(self.ledger_file, 'r') as f:
                last_line = None
                for line in f:
                    if line.strip():
                        last_line = line
                if last_line:
                    last_block = json.loads(last_line)
                    self.last_block_hash = last_block["block_hash"]
        except Exception:
            pass # Start fresh if empty

    def _calculate_block_hash(self, timestamp: float, previous_hash: str, payload: str) -> str:
        block_string = f"{timestamp}{previous_hash}{payload}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def append_log(self, payload: Dict[str, Any]):
        """Appends a new log to the cryptographic chain."""
        timestamp = time.time()
        payload_str = json.dumps(payload, sort_keys=True)
        
        # Calculate new block hash chaining the previous block
        block_hash = self._calculate_block_hash(timestamp, self.last_block_hash, payload_str)
        
        entry = {
            "timestamp": timestamp,
            "previous_hash": self.last_block_hash,
            "block_hash": block_hash,
            "payload": payload
        }
        
        # Write to ledger
        with open(self.ledger_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
            
        self.last_block_hash = block_hash
        logger.info(f"Block Mined & Appended | Hash: {block_hash[:16]}...")
        
        # Periodically update Merkle Root (for high efficiency, done every N blocks)
        self.update_merkle_root()

    def update_merkle_root(self):
        """Calculates the Merkle Root of all block hashes to prove global integrity."""
        block_hashes = []
        try:
            with open(self.ledger_file, 'r') as f:
                for line in f:
                    if line.strip():
                        block_hashes.append(json.loads(line)["block_hash"])
        except Exception:
            pass
            
        if not block_hashes:
            return
            
        tree = MerkleTree(block_hashes)
        root_hash = tree.get_root_hash()
        
        with open(self.root_hash_file, 'w') as f:
            f.write(root_hash)
            
        logger.debug(f"Merkle Root Updated: {root_hash[:16]}...")


class AuditListener:
    def __init__(self, listen_ip: str = "0.0.0.0", listen_port: int = 514):
        self.ledger = ImmutableLedger()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((listen_ip, listen_port))
        logger.info(f"Audit Daemon listening on UDP {listen_ip}:{listen_port}")

    def start(self):
        logger.info("Ready to receive secure telemetry from Layer 2 Diode...")
        try:
            while True:
                data, addr = self.sock.recvfrom(65535)
                try:
                    payload = json.loads(data.decode('utf-8'))
                    self.ledger.append_log(payload)
                except json.JSONDecodeError:
                    # Log raw string if not JSON
                    self.ledger.append_log({"raw_data": data.decode('utf-8', errors='replace')})
        except KeyboardInterrupt:
            logger.info("Audit Daemon shutting down.")


if __name__ == "__main__":
    listener = AuditListener()
    listener.start()
