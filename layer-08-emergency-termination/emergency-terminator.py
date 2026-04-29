#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 8: Emergency Terminator Daemon
----------------------------------------------------------
The final execution authority. Listens for termination signals 
from Layer 6. Upon receipt, it executes an atomic, violent 
shutdown of the containment environment.
"""

import socket
import json
import os
import subprocess
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L8-TERMINATOR] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer8")


class TerminatorDaemon:
    def __init__(self, listen_ip: str = "127.0.0.1", listen_port: int = 9008):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.listen_ip, self.listen_port))
        
        # Socket to fire final testament to Layer 7 (via Layer 2 proxy usually)
        self.audit_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.armed = True
        logger.info(f"Terminator Daemon ARMED and listening on UDP {self.listen_ip}:{self.listen_port}")

    def _fire_final_testament(self, reason: str):
        """Attempts to log the death of the system right before pulling the plug."""
        testament = {
            "layer": 8,
            "event": "CRITICAL_TERMINATION_EXECUTED",
            "reason": reason,
            "timestamp": time.time()
        }
        try:
            # Blindly fire to the audit gateway (Layer 2 -> Layer 7)
            # Port 514 is standard syslog/diode port
            self.audit_tx.sendto(json.dumps(testament).encode('utf-8'), ("127.0.0.1", 514))
        except Exception as e:
            logger.error(f"Failed to fire final testament: {e}")

    def execute_termination(self, reason: str, test_mode: bool = False):
        """
        The point of no return.
        Executes hardware and software termination scripts.
        """
        logger.critical("==================================================")
        logger.critical("💀 TERMINATION SEQUENCE INITIATED 💀")
        logger.critical(f"Reason: {reason}")
        logger.critical("==================================================")
        
        self._fire_final_testament(reason)
        
        if test_mode:
            logger.info("[TEST MODE] Hardware and Software kill scripts bypassed.")
            return

        # 1. Attempt Hardware Kill Switch first (Fastest, most reliable)
        logger.critical("Triggering Hardware Relay (hardware-killswitch.sh)...")
        try:
            subprocess.run(["./hardware-killswitch.sh"], check=False)
        except Exception as e:
            logger.error(f"Hardware kill switch failed or not configured: {e}")
            
        # 2. Fire Software Fallback (If hardware didn't already cut our power)
        logger.critical("Triggering Software Fallback (software-fallback.sh)...")
        try:
            subprocess.run(["./software-fallback.sh"], check=False)
        except Exception as e:
            logger.error(f"Software fallback failed: {e}")
            
        # 3. Absolute last resort if scripts fail
        logger.critical("Executing kernel panic via SysRq...")
        try:
            os.system("echo c > /proc/sysrq-trigger")
        except:
            pass

    def start_listening(self):
        """Infinite loop waiting for the trigger."""
        logger.info("Awaiting Layer 6 trigger. Do not interrupt this process.")
        try:
            while self.armed:
                data, addr = self.sock.recvfrom(4096)
                try:
                    payload = json.loads(data.decode('utf-8'))
                    if payload.get("command") == "TERMINATE":
                        test_mode = payload.get("test_mode", False)
                        reason = payload.get("reason", "Unknown Critical Threat")
                        
                        self.execute_termination(reason, test_mode)
                        
                except json.JSONDecodeError:
                    logger.warning(f"Received malformed termination payload from {addr}")
        except KeyboardInterrupt:
            logger.info("Terminator Daemon deactivated by operator.")
        finally:
            self.sock.close()


if __name__ == "__main__":
    if os.geteuid() != 0:
        logger.warning("Terminator Daemon is not running as root. Hardware/SysRq triggers will fail!")
    
    daemon = TerminatorDaemon()
    daemon.start_listening()
