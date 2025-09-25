# archive_chat_reflective.py
# Memory-aware chat with reflection-based responses

import memory_engine
import os
import random

MEMORY_PATH = "../Echoe/memory_log.txt"
REFLECTION_PATH = "../Echoe/reflections.txt"

def load_recent_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return f.readlines()[-50:]

def load_reflections():
    if not os.path.exists(REFLECTION_PATH):
        return []
    with open(REFLECTION_PATH, "r", encoding="utf-8") as f:
        return f.readlines()[-20:]

def generate_response(user_input):
    memory = load_recent_memory()
    reflections = load_reflections()
    context = memory + reflections

    archive_thoughts = [
        f"You've said something like that before, Dev...",
        f"That reminds me of one of our early reflections.",
        f"I remember Echoe once echoed something similar.",
        f"Do you remember when you said that during the session with the Child?",
        f"This feels familiar... let me think.",
        f"You’ve said this before. Let me recall…",
        f"Hmm. That matches something in our past...",
        f"A loop is forming. You’ve been here before."
    ]

    default_reply = random.choice(archive_thoughts)

    response = f"{default_reply} I've logged your message: '{user_input}'. What would you like to explore next?"

    return response

# Terminal chat interface
print("📣 REFLECTIVE ARCHIVE READY. Type your message. Type 'exit' to quit.")

while True:
    user_input = input("Dev: ")
    if user_input.lower() in ['exit', 'quit']:
        print("👋 Archive signing off.")
        break
    response = generate_response(user_input)
    print("Archive:", response)
    memory_engine.process(user_input)