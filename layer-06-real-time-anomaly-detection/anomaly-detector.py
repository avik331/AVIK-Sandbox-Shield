#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 6: Real-Time Anomaly Detection Engine
-----------------------------------------------------------------
Official Python interface for Layer 6. Acts as the central nervous
system of the shield. Aggregates host telemetry and Guardian alerts,
evaluates them against YAML-defined thresholds, and triggers
Layer 8 (Emergency Termination) if constraints are breached.
"""

import socket
import json
import yaml
import logging
import time
import threading
import hmac
import hashlib
import os
import sys
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import load_config
from keys import keys

_cfg = load_config()

logging.basicConfig(
    level=getattr(logging, _cfg.get("general", {}).get("log_level", "INFO"), logging.INFO),
    format="[%(asctime)s] [AVIK-L6-ANOMALY] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("avik_layer6")


class AnomalyDetector:
    """
    Central engine for detecting baseline deviations and coordinating
    responses across the AVIK architecture.
    """

    def __init__(self, rules_path: str = "anomaly-rules.yaml"):
        self.rules = self._load_rules(rules_path)

        self.master_key     = keys.master
        self.killswitch_key = keys.killswitch

        self.guardian_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.guardian_rx.bind((self.rules["network"]["listen_ip"], self.rules["network"]["guardian_port"]))

        self.telemetry_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.telemetry_rx.bind((self.rules["network"]["listen_ip"], self.rules["network"]["telemetry_port"]))

        self.kill_switch_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.running = False
        self.current_threat_level = 0.0
        self.decay_rate = self.rules["thresholds"]["threat_decay_per_second"]

    def _load_rules(self, path: str) -> Dict[str, Any]:
        """Loads anomaly thresholds from configuration."""
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.critical(f"Failed to load rules from {path}: {e}")
            raise

    def _trigger_kill_switch(self, reason: str):
        """Fires the absolute hardware termination signal to Layer 8."""
        logger.critical(f"💀 INITIATING LAYER 8 EMERGENCY TERMINATION: {reason}")

        payload_dict = {"command": "TERMINATE", "reason": reason}

        try:
            message   = json.dumps(payload_dict, sort_keys=True).encode("utf-8")
            signature = hmac.new(self.killswitch_key, message, hashlib.sha256).hexdigest()
            payload_dict["hmac"] = signature
        except Exception as e:
            logger.error(f"Failed to sign kill switch payload. Layer 8 will likely reject it. Error: {e}")

        payload     = json.dumps(payload_dict).encode("utf-8")
        target_ip   = self.rules["network"]["layer8_ip"]
        target_port = self.rules["network"]["layer8_port"]
        self.kill_switch_tx.sendto(payload, (target_ip, target_port))

    def _evaluate_threat(self, score_increase: float, source: str):
        """Adds to the global threat level and checks against critical thresholds."""
        self.current_threat_level += score_increase
        logger.warning(f"Threat level +{score_increase} from {source}. Current: {self.current_threat_level:.2f}")

        if self.current_threat_level >= self.rules["thresholds"]["critical_action_threshold"]:
            self._trigger_kill_switch(f"Threshold exceeded ({self.current_threat_level:.2f}) via {source}")

    def _listen_guardians(self):
        """Background thread listening for Layer 5 alerts."""
        logger.info(f"Listening for Guardian alerts on UDP {self.rules['network']['guardian_port']}...")
        while self.running:
            try:
                self.guardian_rx.settimeout(1.0)
                data, _ = self.guardian_rx.recvfrom(4096)
                alert   = json.loads(data.decode("utf-8"))

                if "hmac" not in alert:
                    logger.warning("Unauthenticated Guardian alert rejected.")
                    continue

                received_hmac    = alert.pop("hmac")
                expected_message = json.dumps(alert, sort_keys=True).encode("utf-8")
                expected_hmac    = hmac.new(self.master_key, expected_message, hashlib.sha256).hexdigest()

                if not hmac.compare_digest(received_hmac, expected_hmac):
                    logger.warning("HMAC signature mismatch. Guardian alert rejected.")
                    continue

                score         = alert.get("threat_score", 0.0)
                guardian_name = alert.get("guardian", "Unknown")
                logger.error(f"ALERT from Guardian '{guardian_name}' (Score: {score})")
                self._evaluate_threat(score * self.rules["thresholds"]["guardian_weight"], f"Guardian:{guardian_name}")

            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error parsing Guardian alert: {e}")

    def _listen_telemetry(self):
        """Background thread analyzing host telemetry (CPU, RAM, Syscalls)."""
        logger.info(f"Listening for Host Telemetry on UDP {self.rules['network']['telemetry_port']}...")

        max_cpu     = self.rules["system_baselines"]["max_cpu_utilization_percent"]
        max_mem_vel = self.rules["system_baselines"]["max_memory_velocity_mb_s"]

        while self.running:
            try:
                self.telemetry_rx.settimeout(1.0)
                data, _  = self.telemetry_rx.recvfrom(4096)
                metrics  = json.loads(data.decode("utf-8"))

                if "hmac" not in metrics:
                    logger.warning("Unauthenticated telemetry rejected.")
                    continue

                received_hmac    = metrics.pop("hmac")
                expected_message = json.dumps(metrics, sort_keys=True).encode("utf-8")
                expected_hmac    = hmac.new(self.master_key, expected_message, hashlib.sha256).hexdigest()

                if not hmac.compare_digest(received_hmac, expected_hmac):
                    logger.warning("HMAC signature mismatch. Telemetry rejected.")
                    continue

                if metrics.get("cpu_percent", 0) > max_cpu:
                    logger.warning(f"CPU spike: {metrics['cpu_percent']}%")
                    self._evaluate_threat(0.2, "CPU_Spike")

                if metrics.get("memory_velocity_mb_s", 0) > max_mem_vel:
                    logger.warning(f"Memory velocity spike: {metrics['memory_velocity_mb_s']} MB/s")
                    self._evaluate_threat(0.3, "Mem_Velocity_Spike")

                if metrics.get("unauthorized_syscalls_detected", 0) > 0:
                    logger.critical("Unauthorized syscall detected!")
                    self._evaluate_threat(1.0, "Unauthorized_Syscall")

            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error parsing telemetry: {e}")

    def _decay_threat_level(self):
        """Slowly reduces the threat level over time to forgive minor isolated blips."""
        while self.running:
            time.sleep(1.0)
            if self.current_threat_level > 0:
                self.current_threat_level = max(0.0, self.current_threat_level - self.decay_rate)

    def start(self):
        """Starts the Anomaly Detection Engine."""
        self.running = True
        logger.info("Starting Layer 6 Anomaly Detection Engine...")

        t1 = threading.Thread(target=self._listen_guardians,   daemon=True)
        t2 = threading.Thread(target=self._listen_telemetry,   daemon=True)
        t3 = threading.Thread(target=self._decay_threat_level, daemon=True)

        t1.start()
        t2.start()
        t3.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down Anomaly Detection Engine.")
            self.running = False


if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.start()
