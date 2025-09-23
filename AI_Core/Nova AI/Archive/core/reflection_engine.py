# reflection_engine.py
# Analyzes past memory logs for repeated patterns, tone shifts, or unresolved entries

import os
from datetime import datetime

from archive_config import CONFIG
memory_path = CONFIG["memory_path"]
REFLECTION_LOG = os.path.join(os.path.dirname(CONFIG["memory_path"]), "reflections.txt")

def generate_reflections(max_lines=50):
    if not os.path.exists(MEMORY_PATH):
        return "❌ Memory log not found."

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()[-max_lines:]

    thoughts = []
    seen = set()

    for line in lines:
        clean = line.strip().lower()
        if clean in seen:
            continue
        seen.add(clean)
        if "why" in clean or "i feel" in clean or "do you think" in clean:
            thoughts.append(f"Reflect on: {line.strip()}")

    if not thoughts:
        thoughts.append("No unresolved thoughts found in recent memory.")

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(REFLECTION_LOG, "a", encoding="utf-8") as rf:
        rf.write(f"{timestamp} Reflection Run:\n")
        for t in thoughts:
            rf.write(t + "\n")
        rf.write("\n")

    return f"✅ Reflection completed. {len(thoughts)} insights logged."

if __name__ == "__main__":
    print(generate_reflections())