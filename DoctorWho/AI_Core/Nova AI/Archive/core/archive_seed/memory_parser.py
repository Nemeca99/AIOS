# Archive Memory Parser v0.1
# Reads memory_log.txt and summarizes reflection patterns

import re
from collections import Counter
from datetime import datetime

MEMORY_FILE = "memory_log.txt"
SUMMARY_FILE = "memory_reflection_summary.txt"

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def parse_memory(lines):
    internal = []
    user = []
    collapse = 0
    superposition = 0

    for line in lines:
        if "INTERNAL" in line:
            internal.append(line)
        if "Input:" in line and "Output:" in line:
            user.append(line)
            if "Reflection collapsed" in line:
                collapse += 1
            elif "Superposition detected" in line:
                superposition += 1

    return {
        "total_entries": len(lines),
        "internal_thoughts": len(internal),
        "user_interactions": len(user),
        "collapses": collapse,
        "superpositions": superposition
    }

def write_summary(stats):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SUMMARY_FILE, "a", encoding="utf-8") as f:
        f.write(f"--- Reflection Summary ({timestamp}) ---\n")
        for key, value in stats.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        f.write("\n")

def run():
    memory = load_memory()
    stats = parse_memory(memory)
    write_summary(stats)
    print("Reflection summary written to memory_reflection_summary.txt")

if __name__ == "__main__":
    run()