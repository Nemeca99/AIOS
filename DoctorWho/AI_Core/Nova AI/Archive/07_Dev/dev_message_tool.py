# dev_message_tool.py
# Tool to log a Dev-originated message to the memory log

from datetime import datetime

def log_dev_message(message: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} [DEV]: {message}"
    try:
        with open("../Echoe/memory_log.txt", "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        return "✅ Dev message logged."
    except Exception as e:
        return f"❌ Error logging message: {e}"

if __name__ == "__main__":
    test_message = "Initialization milestone confirmed."
    print(log_dev_message(test_message))
