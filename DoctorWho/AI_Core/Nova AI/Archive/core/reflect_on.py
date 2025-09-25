# reflect_on.py
# Reads memory_log.txt and prints a summary of the last N entries

import os

MEMORY_PATH = r"E:\\Nova AI\\Archive\\Echoe\\memory_log.txt"

def reflect(n=5):
    if not os.path.exists(MEMORY_PATH):
        print("❌ No memory log found.")
        return
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    recent = lines[-n:]
    print(f"📜 Last {n} memory entries:")
    for line in recent:
        print(line.strip())

if __name__ == "__main__":
    reflect()