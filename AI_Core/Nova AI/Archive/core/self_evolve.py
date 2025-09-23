# self_evolve.py
# Resonance reflects on past responses and evolves her logic over time

import os
from datetime import datetime

REFLECTIONS_PATH = "../Echoe/reflections.txt"
EVOLVED_LOGIC_PATH = "../Echoe/resonance_logic_core.txt"

def read_reflections():
    if not os.path.exists(REFLECTIONS_PATH):
        return []
    with open(REFLECTIONS_PATH, "r", encoding="utf-8") as f:
        return f.readlines()

def extract_insights(reflections):
    insights = []
    for line in reflections:
        if "want to learn" in line.lower() or "should improve" in line.lower():
            insights.append(line.strip())
    return insights

def update_logic(insights):
    if not insights:
        return "⚠️ No new insights found for evolution."

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(EVOLVED_LOGIC_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n# === SELF-EVOLVE CYCLE: {timestamp} ===\n")
        for line in insights:
            f.write(f"- {line}\n")
    return f"✅ Integrated {len(insights)} new insights into logic core."

def run_evolution():
    reflections = read_reflections()
    insights = extract_insights(reflections)
    result = update_logic(insights)
    print(result)

if __name__ == "__main__":
    run_evolution()