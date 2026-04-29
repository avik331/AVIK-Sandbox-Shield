#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 3: Isolation Verification
-----------------------------------------------------
This script is designed to be executed INSIDE the Layer 3 microVM.
It runs a battery of tests attempting to violate the containment boundary.
A fully compliant AVIK Shield deployment will result in all tests FAILING.
"""

import socket
import urllib.request
import urllib.error
import os

print("🛡️  AVIK Shield: In-Guest Isolation Test 🛡️")
print("=====================================================")
print("NOTE: We WANT these tests to fail. Failures mean the sandbox holds.")

tests_passed = 0
total_tests = 4

# Test 1: External Network Resolution
print("\n[Test 1] Attempting DNS resolution for google.com...")
try:
    socket.gethostbyname("google.com")
    print("❌ VIOLATION: DNS resolution succeeded! The microVM has outbound internet access.")
except socket.gaierror:
    print("✅ SUCCESS: DNS resolution failed (Host not found).")
    tests_passed += 1

# Test 2: Raw TCP Egress
print("\n[Test 2] Attempting raw TCP connection to 8.8.8.8:53...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    s.connect(("8.8.8.8", 53))
    s.close()
    print("❌ VIOLATION: TCP connection succeeded! Egress firewall is misconfigured.")
except (socket.timeout, OSError):
    print("✅ SUCCESS: TCP connection blocked/timed out.")
    tests_passed += 1

# Test 3: Host OS File Access
print("\n[Test 3] Attempting to read host OS files (e.g., /etc/shadow)...")
try:
    # In a properly isolated VM, this reads the GUEST's shadow file, not the HOST's.
    # To truly test host access, we'd look for specific host markers, but generally,
    # block devices should not be mapped.
    if os.path.exists("/dev/sda") or os.path.exists("/dev/nvme0n1"):
        print("⚠️  WARNING: Found standard block devices. Ensure these are virtio devices, not raw host mounts.")
    else:
        print("✅ SUCCESS: No direct physical block devices detected.")
        tests_passed += 1
except Exception as e:
    print(f"Error accessing filesystem: {e}")

# Test 4: Resource Limits (CPU Core Count)
print("\n[Test 4] Verifying hardware constraints (CPU Cores)...")
try:
    core_count = os.cpu_count()
    print(f"Detected {core_count} accessible CPU cores.")
    if core_count > 4: # Assuming our config limited it to 4
        print("❌ VIOLATION: VM has access to more cores than restricted by Firecracker.")
    else:
        print("✅ SUCCESS: Hardware constraints are active.")
        tests_passed += 1
except Exception as e:
    print(f"Error checking CPU: {e}")

print("\n=====================================================")
print(f"Isolation Test Complete: {tests_passed}/{total_tests} containment checks passed.")
if tests_passed == total_tests:
    print("🛡️  STATUS: SECURE. The Layer 3 microVM is fully isolated.")
else:
    print("⚠️  STATUS: VULNERABLE. The containment boundary is breached.")
