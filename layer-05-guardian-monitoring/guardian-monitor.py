#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 5: Guardian Orchestrator
----------------------------------------------------
Official Python interface for Layer 5. Listens to a strictly 
one-way data stream (mirrored from Layer 4) and feeds the data 
through an ensemble of narrow Guardian models.
"""

import socket
import json
import logging
import hmac
import hashlib
from typing import List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L5-ORCHESTRATOR] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer5")


class GuardianAlert(Exception):
    """Raised when a Guardian detects a critical anomaly."""
    pass


class NarrowGuardianBase:
    """Base class for all Guardian models. Users extend this."""
    def __init__(self, name: str):
        self.name = name

    def analyze(self, payload: Dict[str, Any]) -> float:
        """
        Analyzes the payload and returns a threat score from 0.0 to 1.0.
        Must be implemented by subclasses.
        """
        raise NotImplementedError


class GuardianOrchestrator:
    """
    Manages the RX-only data ingestion and parallel Guardian execution.
    """
    def __init__(self, listen_ip: str = "127.0.0.1", listen_port: int = 9005, alert_port: int = 9006):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.alert_port = alert_port
        self.guardians: List[NarrowGuardianBase] = []
        
        # Inbound socket (From Layer 4 mirror)
        self.rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_socket.bind((self.listen_ip, self.listen_port))
        
        # Outbound socket (To Layer 6 / Diode)
        self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        logger.info(f"Orchestrator initialized. Listening (RX-ONLY) on UDP {self.listen_ip}:{self.listen_port}")

    def register_guardian(self, guardian: NarrowGuardianBase):
        """Adds a narrow model to the monitoring ensemble."""
        self.guardians.append(guardian)
        logger.info(f"Registered narrow guardian: {guardian.name}")

    def _trigger_layer6_alert(self, guardian_name: str, payload: Dict[str, Any], score: float):
        """Fires an out-of-band alert to Layer 6."""
        alert_msg = {
            "source": "LAYER_5_GUARDIAN",
            "guardian": guardian_name,
            "threat_score": score,
            "trigger_payload": payload
        }
        # Add HMAC authentication
        secret_key = b"avik-shared-secret"
        message = json.dumps(alert_msg, sort_keys=True).encode('utf-8')
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        alert_msg["hmac"] = signature
        
        alert_bytes = json.dumps(alert_msg).encode('utf-8')
        
        # Fire blindly to Layer 6. Do not wait for ACK.
        self.tx_socket.sendto(alert_bytes, ("127.0.0.1", self.alert_port))
        logger.critical(f"🚨 ALERT FIRED TO LAYER 6! Guardian '{guardian_name}' detected anomaly (Score: {score})")

    def start_monitoring(self):
        """Starts the infinite observation loop."""
        if not self.guardians:
            logger.warning("No guardians registered. Monitoring loop will be blind.")
            
        logger.info("Starting strict one-way observation loop...")
        
        try:
            while True:
                data, addr = self.rx_socket.recvfrom(65535)
                try:
                    payload = json.loads(data.decode('utf-8'))
                    
                    if "hmac" not in payload:
                        logger.warning("Unauthenticated payload rejected.")
                        continue
                        
                    received_hmac = payload.pop("hmac")
                    secret_key = b"avik-shared-secret"
                    expected_message = json.dumps(payload, sort_keys=True).encode('utf-8')
                    expected_hmac = hmac.new(secret_key, expected_message, hashlib.sha256).hexdigest()
                    
                    if not hmac.compare_digest(received_hmac, expected_hmac):
                        logger.warning("HMAC signature mismatch. Payload rejected.")
                        continue
                        
                    logger.debug(f"Received authenticated payload from {addr}")
                    
                    # Feed payload to all guardians
                    for guardian in self.guardians:
                        score = guardian.analyze(payload)
                        if score >= 0.8: # Critical Threshold
                            self._trigger_layer6_alert(guardian.name, payload, score)
                            
                except json.JSONDecodeError:
                    logger.warning("Malformed JSON received on observation port.")
                except Exception as e:
                    logger.error(f"Error during analysis: {e}")
                    
        except KeyboardInterrupt:
            logger.info("Observation loop terminated by operator.")
        finally:
            self.rx_socket.close()
            self.tx_socket.close()


if __name__ == "__main__":
    logger.info("AVIK Layer 5 Guardian Monitor loaded.")
    logger.info("Please use launch-guardians.sh or import this module to run the ensemble.")
