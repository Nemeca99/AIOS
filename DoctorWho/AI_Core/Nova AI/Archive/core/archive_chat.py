# archive_chat.py
# Echoe v1.3 - Live conversational interface

import memory_engine

def main():
    print("🧠 Echoe v1.3 activated — Live Archive Mode enabled.")
    print("📣 ARCHIVE READY. Type your message. Type 'exit' to quit.")

    while True:
        try:
            user_input = input("Dev: ")
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Archive signing off.")
                break
            response = memory_engine.process(user_input)
            print("Archive:", response)
        except KeyboardInterrupt:
            print("\n👋 Archive interrupted. Shutting down.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
