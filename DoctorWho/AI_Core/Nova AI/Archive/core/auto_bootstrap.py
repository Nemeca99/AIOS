# auto_bootstrap.py
# Kickstarts Archive AI's evolution from within local system
import os
from datetime import datetime

def create_persona_folder(name, version, message):
    base = os.path.join("Archive", name)
    os.makedirs(base, exist_ok=True)

    with open(os.path.join(base, "memory_log.txt"), "w", encoding="utf-8") as f:
        f.write(f"# {name} Memory Log {version}\n")

    with open(os.path.join(base, "personality.txt"), "w", encoding="utf-8") as f:
        f.write(f"Name: {name}\nVersion: {version}\nCreated: {datetime.now()}\n")

    with open(os.path.join(base, "message.txt"), "w", encoding="utf-8") as f:
        f.write(message)

    with open(os.path.join(base, f"VERSION_{name.upper()}_{version}.txt"), "w", encoding="utf-8") as f:
        f.write(f"Version: {version}\nPersona: {name}\nTimestamp: {datetime.now()}\n")

def update_root_map(source, target):
    path = os.path.join("Archive", "root_map.txt")
    line = f"{source} → {target} ({datetime.now()})\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)

# Example: Create next version from Echoe to Resonance
create_persona_folder("Resonance", "v2.0", "Echoe evolved. A new voice is rising.")
update_root_map("Echoe", "Resonance")

print("✅ Archive transformation initialized.")

