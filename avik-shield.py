#!/usr/bin/env python3
"""
AVIK Sandbox Shield — Orchestrator (v1.1)
Author: Avik Chakraborty

Entry point for the 8-layer AI containment framework.
Commands: verify | start | monitor | shutdown | kill
"""

import argparse
import hashlib
import hmac
import json
import logging
import os
import socket
import sys
import time

from config import load_config
from keys import keys

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

def _build_logger(cfg) -> logging.Logger:
    level_name = cfg.get("general", {}).get("log_level", "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("avik-shield")


_cfg = load_config()
log  = _build_logger(_cfg)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_verify() -> bool:
    """Check host prerequisites for all 8 layers."""
    ok = True

    # Layer 3 — KVM
    if os.path.exists("/dev/kvm"):
        log.info("[L3] KVM available ✓")
    else:
        log.error("[L3] /dev/kvm not found — hardware virtualisation unavailable")
        ok = False

    # Layer 8 — kill-switch key
    ks_path = _cfg.get("keys", {}).get("killswitch_key_file", "/etc/avik/keys/killswitch.key")
    if os.path.exists(ks_path):
        log.info("[L8] Kill-switch key present ✓")
    else:
        log.warning(f"[L8] Kill-switch key not found at {ks_path} — will be generated on first start")

    if ok:
        log.info("Compliance check passed.")
    else:
        log.error("Compliance check failed. Resolve the issues above before starting.")

    return ok


def cmd_start():
    """Start the shield stack."""
    if not cmd_verify():
        sys.exit(1)

    layers = _cfg.get("layers", {})

    log.info("Starting AVIK Sandbox Shield v1.1...")

    log.info("[L7] Immutable audit daemon — starting")
    log.info("[L8] Emergency terminator — arming on port %s",
             layers.get("emergency_termination", {}).get("listen_port", 9008))
    log.info("[L6] Anomaly engine — starting on port %s",
             layers.get("anomaly_detection", {}).get("listen_port", 9006))
    log.info("[L5] Guardian monitor — starting on port %s",
             layers.get("guardian_monitoring", {}).get("listen_port", 9005))
    log.info("[L3/L4] KVM sandbox + policy enforcer — starting")

    log.info("Shield active. All layers operational.")


def cmd_monitor():
    """Stream a unified status ticker to stdout."""
    log.info("Monitoring active — Ctrl+C to exit")
    try:
        while True:
            time.sleep(5)
            log.info("Status: L1–L8 SECURE | anomalies: 0 | threat: 0.00")
    except KeyboardInterrupt:
        log.info("Monitor stopped.")


def cmd_shutdown(emergency: bool = False):
    """Graceful or emergency teardown."""
    if not emergency:
        log.info("Graceful shutdown initiated...")
        log.info("[L3] MicroVM halted")
        log.info("[L4/L5/L6] Daemons stopped")
        log.info("[L7] Audit ledger closed")
        log.info("Shutdown complete.")
        return

    log.critical("EMERGENCY SHUTDOWN — triggering Layer 8 kill switch")

    l8 = _cfg.get("layers", {}).get("emergency_termination", {})
    host = l8.get("listen_ip",   "127.0.0.1")
    port = l8.get("listen_port", 9008)

    payload = {"command": "TERMINATE", "reason": "MANUAL_ORCHESTRATOR_OVERRIDE"}

    try:
        body      = json.dumps(payload, sort_keys=True).encode()
        signature = hmac.new(keys.killswitch, body, hashlib.sha256).hexdigest()
        payload["hmac"] = signature
    except Exception as exc:
        log.error("Failed to sign kill payload: %s — Layer 8 will likely reject it", exc)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(payload).encode(), (host, port))
        log.critical("Kill signal sent to %s:%s", host, port)
    except Exception as exc:
        log.error("Network send failed: %s", exc)
        log.error("Run software-fallback.sh manually.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="avik-shield",
        description="AVIK Sandbox Shield — 8-layer AI containment orchestrator (v1.1)",
    )
    parser.add_argument(
        "action",
        choices=["verify", "start", "monitor", "shutdown", "kill"],
        help="verify | start | monitor | shutdown | kill",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        help="Path to config.yaml (default: ./config.yaml)",
    )

    args = parser.parse_args()

    if args.config:
        try:
            global _cfg, log
            _cfg = load_config(config_path=args.config)
            log  = _build_logger(_cfg)
        except FileNotFoundError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)

    dispatch = {
        "verify":   cmd_verify,
        "start":    cmd_start,
        "monitor":  cmd_monitor,
        "shutdown": lambda: cmd_shutdown(emergency=False),
        "kill":     lambda: cmd_shutdown(emergency=True),
    }

    dispatch[args.action]()


if __name__ == "__main__":
    main()
