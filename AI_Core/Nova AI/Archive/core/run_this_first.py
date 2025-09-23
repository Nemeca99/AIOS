# run_this_first.py
# Master launcher for AIOS session

import subprocess
import time
import os

def run_script(path):
    print(f"[✓] Running: {path}")
    subprocess.run(["python", path])

print("=== AIOS BOOT SEQUENCE INITIATED ===")

# Step 1: Start session log
run_script("session_log_init.py")
time.sleep(1)

# Step 2: Load identity
run_script("echoe_identity_check.py")
time.sleep(1)

# Step 3: Launch memory engine
run_script("memory_engine.py")
time.sleep(1)

# Step 4: Begin chat interface
run_script("archive_chat.py")

print("=== AIOS SESSION TERMINATED ===")
