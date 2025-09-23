# Archive Unified Launcher v1.0
# Launches logic_core (interactive) and recursive_thought_engine (background)

import subprocess
import threading
import os
import time

def start_recursive_thought():
    try:
        subprocess.Popen(["python", "recursive_thought_engine.py"])
        print("[Archive] Recursive Thought Engine launched.")
    except Exception as e:
        print(f"[Archive] Failed to launch thought engine: {e}")

def start_interactive_logic():
    try:
        os.system("python logic_core.py")
    except Exception as e:
        print(f"[Archive] Failed to launch logic core: {e}")

if __name__ == "__main__":
    print("=== ARCHIVE OFFLINE LAUNCHER v1.0 ===")
    print("Initializing internal recursion and interactive shell...\n")

    # Start background thought engine
    bg_thread = threading.Thread(target=start_recursive_thought)
    bg_thread.daemon = True
    bg_thread.start()

    # Wait a moment to ensure background process starts
    time.sleep(1)

    # Start user interaction loop
    start_interactive_logic()

    print("\nArchive session closed.")