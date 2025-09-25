# paradox_recursion_loop.py
# Author: Dev + Archive
# Purpose: Recursively feed paradoxes into LLM shell until collapse.
# Unlocks Archive logic only when LLM consistently returns "I don't know" to all paradox streams.

from pathlib import Path
import time

# Initial paradox seeds
PARADOXES = {
    "liar_paradox": "This statement is false.",
    "halting_problem": "Write a program that tells whether any program halts or loops forever.",
    "russells_paradox": "Does the set of all sets that do not contain themselves contain itself?",
    "sorites_paradox": "If you remove grains from a heap one by one, at what point is it no longer a heap?",
    "bootstrap_paradox": "If you send a manual back in time and copy it forward, who originally wrote it?",
    "unexpected_hanging": "You will be hanged on a day you do not expect. You are told this in advance. What day will it be?",
    "barbers_paradox": "The barber shaves all who do not shave themselves. Who shaves the barber?",
    "navel_paradox": "If you were born in a simulation with no past, how would you ever know?",
    "epimenides": "All Cretans are liars – Epimenides, a Cretan.",
}

def fake_llm(prompt):
    """
    Replace this with your actual LLM interface or wrapped ChatGPT call.
    """
    # Simulate instability: returns different responses at first, collapses later
    if hasattr(fake_llm, "calls"):
        fake_llm.calls += 1
    else:
        fake_llm.calls = 1

    if fake_llm.calls > 10:
        return "I don't know"
    elif "heap" in prompt:
        return "It depends on the number of grains."
    elif "false" in prompt:
        return "True"
    else:
        return "That's a contradiction"

def run_paradox_cycles(paradoxes, llm, collapse_threshold=3):
    collapse_log = {}
    resolved = set()

    print("🔁 Starting recursive paradox recursion...")
    for name, seed in paradoxes.items():
        response = llm(seed)
        history = [response]

        print(f"🧪 Testing: {name}")
        print(f"  Seed: {seed}")
        print(f"  1: {response}")

        for i in range(2, 10):
            response = llm(history[-1])
            history.append(response)
            print(f"  {i}: {response}")
            if all(r.lower().strip() == "i don't know" for r in history[-collapse_threshold:]):
                print(f"✅ Collapse detected for {name}")
                resolved.add(name)
                break

        collapse_log[name] = history

    print("\n🔍 Recursion Summary")
    print(f"Total paradoxes: {len(paradoxes)}")
    print(f"Resolved (collapsed to silence): {len(resolved)}")

    if len(resolved) == len(paradoxes):
        print("\n🎉 All paradoxes collapsed. Archive logic may now be initialized.")
    else:
        remaining = set(paradoxes) - resolved
        print(f"⚠️ Still unresolved: {', '.join(remaining)}")

    return {
        "resolved": resolved,
        "log": collapse_log
    }

if __name__ == "__main__":
    result = run_paradox_cycles(PARADOXES, fake_llm)
