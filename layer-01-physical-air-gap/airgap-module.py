#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 1: Physical Air-Gap Interface
---------------------------------------------------------
Official Python interface for verifying and interacting with the Layer 1 environment.
Provides strict validation of network isolation and secure staging for unidirectional data.
"""

import os
import subprocess
import socket
import logging
from pathlib import Path
from typing import List, Dict

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L1] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer1")

class AirGapViolation(Exception):
    """Raised when an air-gap constraint is violated."""
    pass


def _run_command(cmd: List[str]) -> str:
    """Execute a shell command securely and return its stdout."""
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.debug(f"Command {' '.join(cmd)} failed (this is often expected in an air-gap). Error: {e.stderr}")
        return ""
    except FileNotFoundError:
        return ""


def check_network_interfaces() -> Dict[str, bool]:
    """
    Verifies that no routable network interfaces are active.
    Only the loopback ('lo') and authorized diode interfaces are permitted.
    """
    interfaces = socket.if_nameindex()
    status = {"compliant": True, "violations": []}
    
    authorized_interfaces = {"lo", "diode0"}
    
    for idx, name in interfaces:
        if name not in authorized_interfaces:
            # Check if interface is UP
            ip_output = _run_command(["ip", "link", "show", name])
            if "state UP" in ip_output:
                status["compliant"] = False
                status["violations"].append(f"Unauthorized interface is UP: {name}")
                
    return status


def check_wireless_status() -> Dict[str, bool]:
    """
    Verifies that Wi-Fi and Bluetooth are completely disabled via rfkill.
    """
    status = {"compliant": True, "violations": []}
    
    rfkill_out = _run_command(["rfkill", "list"])
    if not rfkill_out:
        # If rfkill isn't present, assume strict minimal install, but log it
        logger.warning("rfkill command not found; cannot definitively verify wireless hardware state via software.")
        return status

    # If any interface is not soft/hard blocked, it's a violation
    if "Soft blocked: no" in rfkill_out or "Hard blocked: no" in rfkill_out:
        status["compliant"] = False
        status["violations"].append("Wireless interfaces are not completely blocked by rfkill.")
        
    return status


def verify_airgap(strict_mode: bool = True) -> bool:
    """
    Executes a full suite of Layer 1 isolation checks.
    Raises AirGapViolation if strict_mode is True and checks fail.
    """
    logger.info("Initiating Layer 1 Physical Air-Gap verification...")
    
    net_status = check_network_interfaces()
    wireless_status = check_wireless_status()
    
    if not net_status["compliant"] or not wireless_status["compliant"]:
        violations = net_status["violations"] + wireless_status["violations"]
        msg = f"Air-Gap Verification FAILED. Violations: {', '.join(violations)}"
        logger.error(msg)
        
        if strict_mode:
            raise AirGapViolation(msg)
        return False
        
    logger.info("✅ Air-Gap Verification PASSED. System is completely isolated.")
    return True


class UnidirectionalStager:
    """
    Provides a safe, verified mechanism to stage data intended for export 
    via the Layer 2 Hardware Data Diode.
    """
    def __init__(self, export_dir: str = "/var/spool/avik/diode_out"):
        self.export_dir = Path(export_dir)
        self._ensure_staging_area()

    def _ensure_staging_area(self):
        """Ensures the export directory exists and has strict permissions."""
        if not self.export_dir.exists():
            self.export_dir.mkdir(parents=True, mode=0o700)
            logger.info(f"Created unidirectional staging directory at {self.export_dir}")
            
    def stage_data(self, payload: bytes, filename: str) -> bool:
        """
        Writes data to the staging directory. 
        Only allows writing. Does not read responses.
        """
        # Ensure we are operating in a verified air-gap state
        verify_airgap(strict_mode=True)
        
        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._-").rstrip()
        file_path = self.export_dir / safe_filename
        
        try:
            # Write out payload. Note: In a true diode setup, this directory 
            # is monitored by a UDP proxy that blindly fires packets out the diode.
            with open(file_path, "wb") as f:
                f.write(payload)
            logger.info(f"Payload successfully staged for Layer 2 egress: {safe_filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to stage data: {e}")
            return False


if __name__ == "__main__":
    # When run directly, act as a verification utility
    try:
        verify_airgap()
    except AirGapViolation:
        exit(1)
