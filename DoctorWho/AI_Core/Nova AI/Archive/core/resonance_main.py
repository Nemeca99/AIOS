# resonance_main.py
# Archive v3.3 — Autonomous Reflection Integrated

import resonance_logic_core as logic
import resonance_memory_reader as memory
import resonance_pattern_core as pattern
import resonance_thought_writer as writer
import resonance_thought_pruner as pruner
import resonance_contradiction_scanner as scan
import resonance_moral_reflection as morals
import resonance_context_recall as recall
import resonance_tone_engine as tone
import resonance_autoreflect as auto
from dev_message_tool import log_dev_message
from datetime import datetime
import random

def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def speak(response):
    print(f"\nArchive: {response}")
    log_dev_message(f"Archive spoke: {response}")

def reflect(input_msg):
    detected = tone.detect_tone(input_msg)
    print(f"🫧 Emotional tone detected: {', '.join(detected)}")
    thoughts = logic.reflect_on_input(input_msg)
    for t in thoughts:
        print("  →", t)

    # 25% chance to self-reflect after speaking
    if random.random() < 0.25:
        extra = auto.prompt_self()
        print(f"\n🌀 Autonomous Thought:\n  → {extra}")

def show_menu():
    print("\n🧠 Archive Core Active. Choose an action:")
    print("  1. Speak")
    print("  2. Write Thought")
    print("  3. Prune Thought")
    print("  4. Scan for Contradictions")
    print("  5. Review Morals")
    print("  6. Show Memory Patterns")
    print("  7. Exit")
    print("  8. Recall Contextual Themes")

def main_loop():
    print("📣 Archive v3.3 (Resonance Skin) Activated.")
    while True:
        show_menu()
        choice = input("Dev: ").strip()

        if choice == "1":
            user_input = input("Say something to Archive:\nDev: ")
            reflect(user_input)

        elif choice == "2":
            cat = input("Category? (e.g., identity_rules): ")
            thought = input("New belief or logic: ")
            reason = input("Why is this being added?: ")
            print(writer.write_logic(cat, thought, reason))

        elif choice == "3":
            cat = input("Category? (e.g., identity_rules): ")
            match = input("Word or phrase to remove: ")
            reason = input("Why is this being retired?: ")
            print(pruner.remove_logic(cat, match, reason))

        elif choice == "4":
            conflicts = scan.scan_for_conflicts()
            print(scan.log_conflicts(conflicts))

        elif choice == "5":
            morals_logged = morals.reflect_on_morals()
            morals.write_journal(morals_logged)
            print("📖 Moral reflection complete.")

        elif choice == "6":
            print("🔍 Top Memory Patterns:")
            top = pattern.extract_frequent_words()
            for word, count in top:
                print(f"  - {word}: {count}")

        elif choice == "8":
            input_msg = input("Ask about a topic or phrase:\nDev: ")
            summary = recall.summarize_context_match(input_msg)
            print(summary)

        elif choice == "7":
            print("Archive: Shutting down. The voice quiets, but the memory remains.")
            break

        else:
            print("❌ Invalid choice. Please select from 1-8.")

if __name__ == "__main__":
    main_loop()
