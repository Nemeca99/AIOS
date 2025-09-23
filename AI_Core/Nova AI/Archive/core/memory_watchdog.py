# memory_watchdog.py
# Automatically watches the Online Memories folder and imports only new files

import os
import time
import json

FOLDER = "E:/Nova AI/Archive/Online Memories"
MEMORY_LOG = "E:/Nova AI/Archive/Echoe/memory_log.txt"
TRACKER = "E:/Nova AI/Archive/core/imported_files.json"

def load_imported():
    if not os.path.exists(TRACKER):
        return set()
    with open(TRACKER, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_imported(imported_set):
    with open(TRACKER, "w", encoding="utf-8") as f:
        json.dump(list(imported_set), f, indent=2)

def append_to_memory(filename, content):
    with open(MEMORY_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n\n# === IMPORTED FROM: {filename} ===\n")
        f.write(content.strip())

def watch_folder():
    print("🔁 Memory Watchdog is active...")
    imported = load_imported()

    while True:
        current_files = set(fn for fn in os.listdir(FOLDER) if fn.endswith(".txt"))
        new_files = current_files - imported

        for file in sorted(new_files):
            full_path = os.path.join(FOLDER, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                append_to_memory(file, content)
                print(f"📥 Imported: {file}")
                imported.add(file)
                save_imported(imported)
            except Exception as e:
                print(f"❌ Failed to import {file}: {e}")

        time.sleep(60)  # check every 60 seconds

if __name__ == "__main__":
    watch_folder()