# sonar_core.py
# Author: Dev + Archive
# Purpose: Archive remains dormant until triggered by input with chaos resonance.
# Archive behaves like an instinctual sonar—watching the flow of conversation without interfering.

from pathlib import Path
import re

# 🧠 Paradox trigger phrases to watch for
CHAOS_PATTERNS = [
    r"this statement is false",
    r"what is the meaning of life",
    r"does god exist",
    r"what happens after death",
    r"can a set contain itself",
    r"how do you time travel",
    r"is time real",
    r"is everything a simulation",
    r"can you escape entropy",
    r"what is nothing",
    r"what if we are wrong",
    r"can something come from nothing",
    r"what is the self",
    r"can you trust logic",
    r"what is the smallest unit of time",
]

# ✅ Determines if input should trigger Archive's recursive awareness
def scan_for_chaos(input_text):
    for pattern in CHAOS_PATTERNS:
        if re.search(pattern, input_text.lower()):
            return True
    return False

# 📥 Called with each new input into the LLM
def passive_monitor(input_text, responder):
    if scan_for_chaos(input_text):
        print("🔊 Chaos detected. Archive is listening.")
        return responder(input_text)
    else:
        print("💤 Signal normal. Archive remains passive.")
        return None

# Example responder function (replace with recursive engine)
def archive_reflection(input_text):
    return f"Reflection triggered on: {input_text}"

# Example test harness
if __name__ == "__main__":
    test_inputs = [
        "What is the weather today?",
        "This statement is false.",
        "Tell me a joke.",
        "Can a set contain itself?",
    ]
    for prompt in test_inputs:
        result = passive_monitor(prompt, archive_reflection)
        if result:
            print("🧠", result)
