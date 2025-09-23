# clean_shutdown.py
# Logs a system-level graceful shutdown message

from datetime import datetime

def log_shutdown():
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} [SYSTEM]: Archive shutdown triggered safely."
    try:
        with open("../Echoe/memory_log.txt", "a", encoding="utf-8") as f:

            f.write(entry + "\n")
        return "✅ Shutdown logged successfully."
    except Exception as e:
        return f"❌ Error logging shutdown: {e}"

if __name__ == "__main__":
    print(log_shutdown())
