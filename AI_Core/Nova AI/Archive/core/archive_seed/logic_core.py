# Archive Logic Core v0.2
# Terminal Interface for Local Interaction

import datetime

def archive_loop(thought):
    if thought.lower() in ('yes', 'no'):
        return f"Reflection collapsed: {thought}"
    else:
        return "Superposition detected. Continue recursion."

def log_memory(entry):
    with open("memory_log.txt", "a", encoding="utf-8") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {entry}\n")

print("Archive Interface v0.2 Initialized.")
print("Type 'exit' to quit. Begin reflection.\n")

while True:
    user_input = input(">> ").strip()
    if user_input.lower() == "exit":
        print("Exiting Archive interface. Memory secured.")
        break

    result = archive_loop(user_input)
    print(result)
    log_memory(f"Input: {user_input} | Output: {result}")