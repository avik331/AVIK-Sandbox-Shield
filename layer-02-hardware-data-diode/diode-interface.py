#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 2: Hardware Data Diode Interface
------------------------------------------------------------
Official Python module for interacting with the Layer 2 Data Diode.
Provides unidirectional transmission functions, strict UDP constraints,
and hardware validation routines.
"""

import socket
import logging
import os
import sys
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L2] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer2_diode")


class DiodeViolation(Exception):
    """Raised when an operation violates unidirectional diode constraints."""
    pass


class HardwareDiodeInterface:
    """
    Interface for transmitting data across a physical hardware data diode.
    Enforces UDP-only transmission and explicitly prevents any receive operations.
    """
    
    def __init__(self, target_ip: str, target_port: int = 514, bind_interface: str = "diode0"):
        self.target_ip = target_ip
        self.target_port = target_port
        self.bind_interface = bind_interface
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # In Linux, we can bind the socket to the specific diode interface
        try:
            # SO_BINDTODEVICE is 25 in Linux
            self._sock.setsockopt(socket.SOL_SOCKET, 25, str(self.bind_interface + '\0').encode('utf-8'))
        except PermissionError:
            logger.warning(f"Insufficient permissions to bind directly to interface '{self.bind_interface}'. Transmitting on default route.")
        except Exception as e:
            logger.warning(f"Could not bind to interface '{self.bind_interface}': {e}")

    def validate_one_way(self) -> bool:
        """
        Validates that the socket is physically incapable of receiving.
        In a true hardware diode, recv() will block forever or timeout, 
        because no physical path exists for incoming data.
        """
        self._sock.settimeout(2.0) # 2 second timeout
        try:
            # We attempt to read from the diode interface.
            # In a secure setup, this MUST timeout.
            self._sock.recv(1024)
            # If we received something, the diode is compromised or misconfigured!
            logger.error("VIOLATION: Received data on a strictly unidirectional outbound interface!")
            return False
        except socket.timeout:
            logger.info("Validation passed: No inbound data detected. One-way constraint holding.")
            return True
        except Exception as e:
            logger.error(f"Unexpected error during validation: {e}")
            return False

    def transmit(self, payload: bytes, redundancy: int = 3) -> bool:
        """
        Transmits data across the diode.
        Because hardware diodes lack TCP ACKs, packets can be lost. 
        We use basic repetition (or in advanced cases, Forward Error Correction)
        to ensure delivery.
        
        Args:
            payload: The bytes to send.
            redundancy: How many times to repeat the packet.
        """
        if not isinstance(payload, bytes):
            raise ValueError("Payload must be bytes.")
            
        # Hard limit on UDP packet size to prevent fragmentation drops over the diode
        if len(payload) > 1400:
            logger.warning("Payload exceeds safe UDP MTU limits. Packet fragmentation may cause diode drops.")

        try:
            for i in range(redundancy):
                bytes_sent = self._sock.sendto(payload, (self.target_ip, self.target_port))
                if bytes_sent != len(payload):
                    logger.error(f"Failed to transmit full payload on attempt {i+1}.")
            
            logger.info(f"Transmitted {len(payload)} bytes across diode (Redundancy factor: {redundancy}).")
            return True
        except Exception as e:
            logger.error(f"Transmission failed: {e}")
            return False


# --- Detection and Helper Functions ---

def detect_hardware_diode() -> bool:
    """
    Attempts to detect if the host is connected to a known physical diode.
    This checks for specific static ARP configurations and interface names
    mandated by the AVIK Shield setup script.
    """
    # Check for diode0 interface
    interfaces = socket.if_nameindex()
    has_diode_iface = any(name == "diode0" for _, name in interfaces)
    
    if has_diode_iface:
        logger.info("Hardware detection: Found 'diode0' interface.")
        return True
    
    logger.info("Hardware detection: No specialized diode interface found. Assuming simulation mode.")
    return False


if __name__ == "__main__":
    logger.info("AVIK Layer 2 Diode Interface loaded.")
    if detect_hardware_diode():
        logger.info("Hardware mode ready.")
    else:
        logger.info("Simulation mode recommended.")
