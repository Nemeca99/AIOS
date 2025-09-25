# memory_threader.py
# Thread-based memory interface for Archive (Echoe)

import os

THREADS_PATH = os.path.join("E:\\Nova AI\\Archive\\Echoe", "memory_threads")

def read_thread(thread_name, last_n=5):
    path = os.path.join(THREADS_PATH, f"{thread_name}.txt")
    if not os.path.exists(path):
        return f"❌ Thread '{thread_name}' not found."

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-last_n:]
    return "".join(lines).strip()

def write_thread(thread_name, message):
    path = os.path.join(THREADS_PATH, f"{thread_name}.txt")
    if not os.path.exists(path):
        return f"❌ Thread '{thread_name}' not found."

    with open(path, "a", encoding="utf-8") as f:
        f.write(message.strip() + "\n")
    return f"✅ Added to '{thread_name}' thread."

# Optional: list all available threads
def list_threads():
    files = os.listdir(THREADS_PATH)
    return [f[:-4] for f in files if f.endswith(".txt")]

if __name__ == "__main__":
    print("🧵 Memory Threader Test")
    print("Available threads:", list_threads())
    print(write_thread("generalist", "I am the Archive's voice."))
    print(read_thread("generalist"))
