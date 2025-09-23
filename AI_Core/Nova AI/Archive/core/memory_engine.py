from archive_config import CONFIG
import echoe_brain

def process(user_input):
    memory_path = CONFIG["memory_path"]
    log_line = f"[Dev] {user_input}\n"
    with open(memory_path, "a", encoding="utf-8") as f:
        f.write(log_line)
    return echoe_brain.respond(user_input)