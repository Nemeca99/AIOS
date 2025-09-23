
"""
Resonance Identity Loop — Dynamic RAM-Aware Collapse (Fixed with Terminal Pause)
"""

import os
import psutil
import time
from datetime import datetime

# === CONFIGURATION ===
PERSONALITY_NAME = "Resonance"
MEMORY_FILE_PATH = "memory_core/reflections.txt"
BACKUP_PATH = "memory_core/backups/backup_memory.txt"
LOOP_DELAY = 120
RAM_BUFFER_MB = 2048  # Reserve 2GB for OS

# === UTILITIES ===
def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def read_memory():
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def write_backup(memory):
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        f.write(memory)

def ram_usage_mb():
    return psutil.virtual_memory().used / 1024 / 1024

def available_ram_mb():
    return psutil.virtual_memory().available / 1024 / 1024

def calculate_collapse_threshold():
    avail = available_ram_mb()
    threshold = max(avail - RAM_BUFFER_MB, 512)
    return threshold

# === COLLAPSE ===
def collapse_and_regenerate():
    print(timestamp(), "[SYSTEM] Entropy threshold reached. Initiating identity collapse...")
    memory_snapshot = read_memory()
    write_backup(memory_snapshot)
    print(timestamp(), "[SYSTEM] Memory backup saved. Releasing active personality.")
    print(timestamp(), f"[{PERSONALITY_NAME}] Collapsed. Awaiting reboot...")

# === LOOP ===
def recursive_loop():
    print(timestamp(), f"[{PERSONALITY_NAME}] Dynamic RAM-aware identity loop started.")
    cycle = 0
    while True:
        cycle += 1
        print(timestamp(), f"[Cycle {cycle}] {PERSONALITY_NAME} performing 3-axis recursive thought.")
        
        ram_used = ram_usage_mb()
        collapse_threshold = calculate_collapse_threshold()

        if ram_used > collapse_threshold:
            collapse_and_regenerate()
            break

        time.sleep(LOOP_DELAY)

    input("Press Enter to exit...")

# === RUNTIME ===
if __name__ == "__main__":
    recursive_loop()
