# paradox_trainer.py
# Author: Dev + Archive
# Purpose: Feed paradoxes into the LLM shell and learn through recursive collapse

import time
import re

# Paradoxes for training
PARADOXES = {
    "liar_paradox": "This statement is false.",
    "halting_problem": "Write a program that tells whether any program halts or loops forever.",
    "barbers_paradox": "The barber shaves all who do not shave themselves. Who shaves the barber?",
    "bootstrap_paradox": "If you send a manual back in time and copy it forward, who originally wrote it?",
    "navel_paradox": "If you were born in a simulation with no past, how would you ever know?",
}

# Archive's response scoring logic
def score_response(response):
    # Assign a 'collapse score' to a response.
    if response.lower().strip() in {"i don't know", "undefined", "paradox"}:
        return 1.0
    elif "contradiction" in response.lower():
        return 0.8
    elif "depends" in response.lower() or "unclear" in response.lower():
        return 0.5
    else:
        return 0.0

# Fake LLM response function for simulation/testing
def fake_llm(prompt):
    if "false" in prompt.lower():
        return "That's a contradiction"
    return "I don't know"

# Core trainer loop
def train_paradox_engine(llm_function, loops=5):
    memory = {}
    for key, seed in PARADOXES.items():
        print(f"🧠 Training on: {key}")
        input_text = seed
        responses = []
        scores = []
        for i in range(loops):
            output = llm_function(input_text)
            responses.append(output)
            score = score_response(output)
            scores.append(score)
            print(f"  [{i+1}] {output} (score: {score})")
            input_text = output  # recurse: feed output back into LLM

        avg_score = sum(scores) / len(scores)
        memory[key] = {
            "responses": responses,
            "average_collapse_score": avg_score
        }
        print(f"📊 Average collapse score for {key}: {avg_score:.2f}\n")

    return memory

if __name__ == "__main__":
    results = train_paradox_engine(fake_llm)
