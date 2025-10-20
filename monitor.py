#!/usr/bin/env python3
"""
Server Health Monitoring Script
Author: Atif Khan
Description: Checks CPU, memory, disk usage, and network connectivity.
"""

import psutil
import socket
import datetime

# Thresholds
CPU_THRESHOLD = 80  # percent
MEM_THRESHOLD = 80  # percent
DISK_THRESHOLD = 80  # percent
HOST_TO_PING = "8.8.8.8"  # Google DNS

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    return usage, usage > CPU_THRESHOLD

def check_memory():
    mem = psutil.virtual_memory()
    return mem.percent, mem.percent > MEM_THRESHOLD

def check_disk():
    disk = psutil.disk_usage('/')
    return disk.percent, disk.percent > DISK_THRESHOLD

def check_network(host=HOST_TO_PING, port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def log_results(results):
    with open("server_health.log", "a") as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        for key, value in results.items():
            f.write(f"{key}: {value}\n")

def main():
    results = {}

    cpu, cpu_alert = check_cpu()
    mem, mem_alert = check_memory()
    disk, disk_alert = check_disk()
    net = check_network()

    results["CPU Usage"] = f"{cpu}% {'⚠️ ALERT' if cpu_alert else 'OK'}"
    results["Memory Usage"] = f"{mem}% {'⚠️ ALERT' if mem_alert else 'OK'}"
    results["Disk Usage"] = f"{disk}% {'⚠️ ALERT' if disk_alert else 'OK'}"
    results["Network Connectivity"] = "Online ✅" if net else "Offline ❌"

    log_results(results)

    # Print to console as well
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()