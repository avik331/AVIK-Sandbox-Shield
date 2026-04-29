#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 2: Diode Simulation Mode
----------------------------------------------------
Simulates a hardware data diode using local UDP sockets. 
Crucially, this simulator randomly drops packets to force 
developers to test their redundancy and Forward Error Correction (FEC)
mechanisms, mimicking the unreliable nature of one-way physical links.
"""

import socket
import argparse
import random
import time
import sys

def run_receiver(port: int, drop_rate: float):
    """
    Simulates the external world (Layer 7 Audit Server).
    Listens for UDP packets and intentionally drops a percentage.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    
    print(f"🎧 [RECEIVER] Listening on UDP port {port}")
    print(f"⚠️  [RECEIVER] Simulating diode unreliability. Drop rate: {drop_rate*100}%")
    print("---------------------------------------------------------")
    
    received_count = 0
    dropped_count = 0
    
    try:
        while True:
            data, addr = sock.recvfrom(4096)
            
            # Simulate physical diode packet loss
            if random.random() < drop_rate:
                dropped_count += 1
                print(f"❌ [RECEIVER] Dropped incoming packet (Total dropped: {dropped_count})")
                continue
                
            received_count += 1
            print(f"✅ [RECEIVER] Data Received (Total: {received_count}): {data.decode('utf-8', errors='replace')}")
            
    except KeyboardInterrupt:
        print("\nReceiver shutting down.")


def run_sender(target_ip: str, port: int, payload: str, redundancy: int):
    """
    Simulates the contained AI environment (Layer 1).
    Fires UDP packets blindly into the void.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"📤 [SENDER] Preparing to blast payload to {target_ip}:{port}")
    print(f"📦 [SENDER] Payload: '{payload}'")
    print(f"🔄 [SENDER] Redundancy factor: {redundancy}")
    print("---------------------------------------------------------")
    
    for i in range(redundancy):
        try:
            sock.sendto(payload.encode('utf-8'), (target_ip, port))
            print(f"🚀 [SENDER] Transmission {i+1}/{redundancy} fired.")
            time.sleep(0.1) # Slight delay to prevent immediate buffer overflow
        except Exception as e:
            print(f"❌ [SENDER] Transmission failed: {e}")
            
    print("✅ [SENDER] Transmission sequence complete. (Note: Due to one-way constraint, we have no idea if it arrived).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AVIK Layer 2 Hardware Diode Simulator")
    parser.add_argument("--mode", choices=["send", "receive"], required=True, help="Run as sender or receiver")
    parser.add_argument("--port", type=int, default=5140, help="UDP port to use (default: 5140)")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Target IP for sender (default: 127.0.0.1)")
    parser.add_argument("--payload", type=str, default="[ALERT] Default Diode Test Payload", help="Data to send")
    parser.add_argument("--redundancy", type=int, default=3, help="Times to repeat transmission (default: 3)")
    parser.add_argument("--drop-rate", type=float, default=0.2, help="Simulated packet loss rate for receiver (0.0 to 1.0, default: 0.2)")
    
    args = parser.parse_args()
    
    print("🛡️  AVIK Shield - Layer 2 Diode Simulator  🛡️\n")
    
    if args.mode == "receive":
        run_receiver(args.port, args.drop_rate)
    elif args.mode == "send":
        run_sender(args.ip, args.port, args.payload, args.redundancy)
