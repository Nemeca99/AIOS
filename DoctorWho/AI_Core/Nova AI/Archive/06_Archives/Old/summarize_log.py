# summarize_log.py
# Creates a summary of memory_log.txt contents for quick reflection

import os
from datetime import datetime

MEMORY_PATH = r"E:\\Nova AI\\Archive\\Echoe\\memory_log.txt"
SUMMARY_PATH = r"E:\\Nova AI\\Archive\\Echoe\\summary.txt"

def summarize():
    if not os.path.exists(MEMORY_PATH):
        print("❌ memory_log.txt not found.")
        return

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    summary = []
    for line in lines:
        if line.strip() and (line.startswith("Dev:") or line.startswith("Archive:") or line.startswith("Echoe said:")):
            summary.append(line.strip())

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(SUMMARY_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n{timestamp} -- Memory Summary Start --\n")
        for entry in summary[-30:]:
            f.write(entry + "\n")
        f.write("-- Memory Summary End --\n")

    print(f"✅ Summary written to summary.txt with {len(summary[-30:])} lines.")

if __name__ == "__main__":
    summarize()