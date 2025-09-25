print("🧭 LIVE TEST: This is the real session_log_init.py")

print("🧭 SESSION_LOG_INIT: Loaded from live environment.")

print("🔍 SESSION_LOG_INIT: Running updated version.")

# session_log_init.py
# Logs the start of a new Archive session with hardcoded memory path

from core.timestamp_generator import now

def log_session_start():
    log_path = r"E:\\Nova AI\\Archive\\Echoe\\memory_log.txt"
    entry = f"{now()} [SYSTEM]: Archive session started."
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        return "✅ Session start logged."
    except Exception as e:
        return f"❌ Error logging session: {e}"

if __name__ == "__main__":
    print(log_session_start())
