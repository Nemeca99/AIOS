# memory_loader.py
# Loads preserved memory from disk on Archive startup

def load_memory_log(filepath="Archive/Echoe/memory_log.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            memory = f.readlines()
        print(f"📚 Loaded {len(memory)} memory entries.")
        return memory
    except FileNotFoundError:
        print("⚠️ Memory log file not found. Starting with empty memory.")
        return []
