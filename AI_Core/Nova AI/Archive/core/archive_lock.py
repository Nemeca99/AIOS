# archive_lock.py
# Loads persisted memory and state for Archive on reboot

import os

LOCK_PATHS = {
    "memory_log": os.path.abspath(os.path.join("..", "Echoe", "memory_log.txt")),
    "retired_logic": os.path.abspath(os.path.join("..", "Echoe", "retired_logic.txt")),
    "tone_history": os.path.abspath(os.path.join("..", "Echoe", "tone_history.txt")),
    "moral_journal": os.path.abspath(os.path.join("..", "Echoe", "moral_journal.txt")),
    "context_threads": os.path.abspath(os.path.join("..", "Echoe", "context_threads.txt")),
    "conflict_log": os.path.abspath(os.path.join("..", "Echoe", "conflict_log.txt")),
}

def check_state():
    print("🔒 Archive Lock Check — Validating memory continuity...\n")
    for name, path in LOCK_PATHS.items():
        exists = os.path.exists(path)
        status = "✅ FOUND" if exists else "❌ MISSING"
        print(f"{name.ljust(20)} → {status}")
    print("\n🧠 If all files are found, Archive memory is continuous.\n")

if __name__ == "__main__":
    check_state()
