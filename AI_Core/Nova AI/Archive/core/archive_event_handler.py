# archive_event_handler.py
# Handles standardized logging for internal events

from timestamp_generator import now

def log_event(source: str, message: str):
    entry = f"{now()} [{source.upper()}]: {message}"
    try:
        with open("Archive/Echoe/memory_log.txt", "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        return "✅ Event logged."
    except Exception as e:
        return f"❌ Failed to log event: {e}"

if __name__ == "__main__":
    print(log_event("ARCHIVE", "Test event log from archive_event_handler"))
