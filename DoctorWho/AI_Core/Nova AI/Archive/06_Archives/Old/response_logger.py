# response_logger.py
# Logs Archive AI responses to the memory log

from datetime import datetime

def log_response(response: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} [ARCHIVE]: {response}"
    try:
        with open("Archive/Echoe/memory_log.txt", "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        return "✅ Response logged."
    except Exception as e:
        return f"❌ Failed to log response: {e}"

if __name__ == "__main__":
    print(log_response("Test archive response."))
