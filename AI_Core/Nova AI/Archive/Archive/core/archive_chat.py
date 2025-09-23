# archive_chat.py
# Terminal chat interface for Archive AI

import memory_engine

print("📣 ARCHIVE READY. Type your message. Type 'exit' to quit.")

while True:
    user_input = input("Dev: ")
    if user_input.lower() in ['exit', 'quit']:
        print("👋 Archive signing off.")
        break
    response = memory_engine.process(user_input)
    print("Archive:", response)
