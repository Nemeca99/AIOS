# log_append_tool.py
# Appends a single entry to the memory log

def append_to_memory(entry: str):
    try:
        with open("../Echoe/memory_log.txt", "a", encoding="utf-8") as f:
            f.write(entry.strip() + "\\n")
        return "✅ Memory updated successfully."
    except Exception as e:
        return f"❌ Failed to write to memory: {e}"

if __name__ == "__main__":
    test_entry = "[SYSTEM] Test entry from log_append_tool."
    print(append_to_memory(test_entry))
