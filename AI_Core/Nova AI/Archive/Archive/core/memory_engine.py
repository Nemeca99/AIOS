# memory_engine.py
# Handles storing input to Archive memory

def process(user_input):
    log_line = f"[Dev] {user_input}\n"
    with open("Archive/Echoe/memory_log.txt", "a", encoding="utf-8") as f:
        f.write(log_line)
    return f"I've logged that: '{user_input}'. What would you like to do next?"
