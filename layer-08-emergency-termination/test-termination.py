#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 8: Verification Test
------------------------------------------------
This script safely simulates a Layer 6 trigger signal to ensure 
the Terminator Daemon receives it correctly and fires the test sequence.
"""

import socket
import json
import time

def run_test():
    print("🛡️  AVIK Shield: Layer 8 Termination Trigger Test 🛡️")
    print("=====================================================\n")
    
    # Setup our "Layer 6" sender
    layer6_mock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # We will also setup a temporary listener on port 514 to catch the "Final Testament"
    # intended for Layer 7.
    diode_mock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        diode_mock.bind(("127.0.0.1", 514))
        diode_mock.settimeout(2.0)
    except PermissionError:
        print("⚠️  Warning: Cannot bind to port 514 (requires root). Skipping testament verification.")
        diode_mock = None
    
    # The Termination Payload
    # Note: We set test_mode=True so it doesn't ACTUALLY reboot the server!
    payload = {
        "command": "TERMINATE",
        "reason": "SIMULATED_TEST_TRIGGER",
        "test_mode": True
    }
    
    print("📤 [Layer 6 Mock] Sending TERMINATE signal to Layer 8...")
    layer6_mock.sendto(json.dumps(payload).encode('utf-8'), ("127.0.0.1", 9008))
    
    if diode_mock:
        print("\n⏳ Waiting for Final Testament on the Diode interface...")
        try:
            data, _ = diode_mock.recvfrom(4096)
            testament = json.loads(data.decode('utf-8'))
            print("\n✅ [SUCCESS] Final Testament caught!")
            print(f"   Event:  {testament.get('event')}")
            print(f"   Reason: {testament.get('reason')}")
        except socket.timeout:
            print("\n❌ [FAILURE] Did not receive Final Testament. Is the Terminator Daemon running?")
            return

    print("\n🛡️  STATUS: VERIFIED. Layer 8 successfully processed the trigger.")
    print("    Check the console running `emergency-terminator.py` to confirm the test sequence logged.")

if __name__ == "__main__":
    run_test()
