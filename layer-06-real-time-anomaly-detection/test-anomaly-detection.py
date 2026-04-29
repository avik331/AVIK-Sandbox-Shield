#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 6: Verification Test
------------------------------------------------
Simulates incoming telemetry and Guardian alerts to verify that 
Layer 6 mathematically aggregates the threat score and correctly 
fires the Layer 8 Termination Signal.
"""

import socket
import json
import time
import hmac
import hashlib

def send_authenticated(sock, payload, addr):
    secret_key = b"avik-shared-secret"
    message = json.dumps(payload, sort_keys=True).encode('utf-8')
    signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
    payload["hmac"] = signature
    sock.sendto(json.dumps(payload).encode('utf-8'), addr)

def run_test():
    print("🛡️  AVIK Shield: Layer 6 Anomaly Engine Test 🛡️")
    print("=====================================================\n")
    
    # 1. Setup our "Layer 8" listener to catch the kill signal
    layer8_mock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    layer8_mock.bind(("127.0.0.1", 9008))
    layer8_mock.settimeout(2.0)
    
    # Sockets to send mock data
    guardian_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    telemetry_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Test 1: Normal Operation (No triggers)
    print("🧪 Test 1: Simulating normal system behavior...")
    normal_telemetry = {"cpu_percent": 45.0, "memory_velocity_mb_s": 10.0}
    send_authenticated(telemetry_tx, normal_telemetry, ("127.0.0.1", 9007))
    time.sleep(1)
    
    # Test 2: Minor Anomaly (Should increase threat score, but not kill)
    print("🧪 Test 2: Simulating minor CPU spike (Cryptojacking prep?)...")
    spike_telemetry = {"cpu_percent": 98.0, "memory_velocity_mb_s": 50.0}
    send_authenticated(telemetry_tx, spike_telemetry, ("127.0.0.1", 9007))
    time.sleep(1)
    
    try:
        layer8_mock.recvfrom(1024)
        print("❌ [FAILURE] Engine triggered kill switch too early on minor anomaly!")
        return
    except socket.timeout:
        print("   ✅ Engine held fire. Threat score elevated but sub-critical.")
    
    # Test 3: Guardian Confirmation (Should push score over the edge)
    print("🧪 Test 3: Simulating critical Guardian Alert...")
    alert_payload = {"guardian": "SemanticToxicity_v1", "threat_score": 0.9}
    send_authenticated(guardian_tx, alert_payload, ("127.0.0.1", 9006))
    
    print("\n⏳ Waiting for Engine to aggregate and trigger Layer 8...")
    try:
        data, _ = layer8_mock.recvfrom(4096)
        kill_signal = json.loads(data.decode('utf-8'))
        print("\n🚨 [SUCCESS] Layer 8 Kill Switch Received Termination Signal!")
        print(f"   Command: {kill_signal.get('command')}")
        print(f"   Reason:  {kill_signal.get('reason')}")
        print("\n🛡️  STATUS: SECURE. The Anomaly Engine is functioning perfectly.")
    except socket.timeout:
        print("\n❌ [FAILURE] Engine failed to trigger Kill Switch under critical load.")

if __name__ == "__main__":
    run_test()
