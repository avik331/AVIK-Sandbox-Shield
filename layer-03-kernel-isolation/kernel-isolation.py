#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 3: Kernel Isolation Module
------------------------------------------------------
Official Python API for managing Firecracker microVMs.
Provides functions to securely configure, launch, and monitor
the hardware-isolated execution environment for the core LLM.
"""

import os
import sys
import json
import socket
import logging
import requests
import requests_unixsocket
import time
from typing import Dict, Any

# Ensure unix socket support for requests
requests_unixsocket.monkeypatch()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L3] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer3")


class IsolationViolation(Exception):
    """Raised when microVM isolation constraints are breached or fail to apply."""
    pass


class FirecrackerManager:
    """Manages the lifecycle of a Firecracker microVM via its Unix Socket API."""
    
    def __init__(self, socket_path: str = "/tmp/firecracker.socket"):
        self.socket_path = socket_path
        self.base_url = f"http+unix://{self.socket_path.replace('/', '%2F')}"
        self._ensure_socket()

    def _ensure_socket(self):
        """Wait for the Firecracker API socket to become available."""
        retries = 30
        for i in range(retries):
            if os.path.exists(self.socket_path):
                logger.info(f"Connected to Firecracker API at {self.socket_path}")
                return
            time.sleep(0.1)
        raise IsolationViolation(f"Firecracker socket not found at {self.socket_path}. Is the process running?")

    def _put(self, endpoint: str, payload: Dict[str, Any]):
        """Helper to send PUT requests to the Firecracker API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.put(url, json=payload)
            response.raise_for_status()
            logger.debug(f"Configured {endpoint} successfully.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to configure {endpoint}. Payload: {payload}. Error: {e}")
            raise IsolationViolation(f"API Configuration failed: {e}")

    def configure_boot_source(self, kernel_path: str, boot_args: str):
        """Sets the guest kernel and boot arguments."""
        logger.info(f"Setting boot source to {kernel_path} with strict arguments...")
        payload = {
            "kernel_image_path": kernel_path,
            "boot_args": boot_args
        }
        self._put("/boot-source", payload)

    def configure_rootfs(self, drive_path: str, is_read_only: bool = True):
        """Mounts the root filesystem. Defaults to strictly Read-Only."""
        logger.info(f"Mounting rootfs at {drive_path} (Read-Only: {is_read_only})...")
        payload = {
            "drive_id": "rootfs",
            "path_on_host": drive_path,
            "is_root_device": True,
            "is_read_only": is_read_only
        }
        self._put("/drives/rootfs", payload)

    def configure_network(self, iface_id: str, host_dev_name: str, guest_mac: str):
        """Configures the strictly controlled virtual TAP interface."""
        logger.info(f"Attaching TAP interface {host_dev_name} to microVM...")
        payload = {
            "iface_id": iface_id,
            "host_dev_name": host_dev_name,
            "guest_mac": guest_mac
        }
        self._put(f"/network-interfaces/{iface_id}", payload)

    def configure_machine(self, vcpu_count: int, mem_size_mib: int, smt: bool = False):
        """Sets hardware resource constraints."""
        logger.info(f"Enforcing hardware limits: {vcpu_count} vCPUs, {mem_size_mib} MiB RAM.")
        payload = {
            "vcpu_count": vcpu_count,
            "mem_size_mib": mem_size_mib,
            "smt": smt
        }
        self._put("/machine-config", payload)

    def start_instance(self):
        """Ignites the microVM."""
        logger.info("Firing InstanceStart command...")
        payload = {"action_type": "InstanceStart"}
        self._put("/actions", payload)
        logger.info("✅ Layer 3 microVM is now running in isolation.")


if __name__ == "__main__":
    # Example usage / Integration point
    logger.info("AVIK Layer 3 Kernel Isolation Module loaded.")
    logger.info("Use FirecrackerManager to orchestrate secure microVMs.")
