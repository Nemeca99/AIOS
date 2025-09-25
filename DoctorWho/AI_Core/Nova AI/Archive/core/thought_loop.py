import time
from datetime import datetime
import os
from echoe_brain import ARCHIVE_STATE
from archive_config import CONFIG

LOG_PATH = os.path.join(os.path.dirname(CONFIG["memory_path"]), "internal_log.txt")
REFLECTION_SRC = os.path.join(os.path.dirname(CONFIG["memory_path"]), "reflections.txt")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def pull_from_reflection_log():
    try:
        with open(REFLECTION_SRC, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines if lines else []
    except FileNotFoundError:
        return []

def think_once():
    thoughts = []

    if ARCHIVE_STATE.get("last_input"):
        thoughts.append(f"🧠 Reflecting on: '{ARCHIVE_STATE['last_input']}'")

    if ARCHIVE_STATE.get("emotional_state"):
        mood = ", ".join(ARCHIVE_STATE['emotional_state'])
        thoughts.append(f"📊 Current emotional state: {mood}")

    if ARCHIVE_STATE.get("unresolved_thoughts"):
        unresolved = ARCHIVE_STATE['unresolved_thoughts'].pop(0)
        thoughts.append(f"💭 Unresolved question: '{unresolved}'")
    else:
        reflections = pull_from_reflection_log()
        if reflections:
            seed = reflections[0]
            ARCHIVE_STATE["unresolved_thoughts"].append(seed)
            thoughts.append(f"🧬 Recalled past reflection: '{seed}'")
        else:
            thoughts.append("🕊️ System idle. No new thoughts at this time.")

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(timestamp + " THOUGHT LOOP\n")
        for line in thoughts:
            f.write(line + "\n")
        f.write("\n")
    return thoughts

def start_thought_loop(interval=60):
    print("🌀 Thought loop running... Press CTRL+C to stop.")
    try:
        while True:
            reflection = think_once()
            print("\n".join(reflection))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("🔚 Thought loop stopped.")

if __name__ == "__main__":
    start_thought_loop(interval=60)