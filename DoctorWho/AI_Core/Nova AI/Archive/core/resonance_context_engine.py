# resonance_context_engine.py
# Groups memory_log.txt into conceptual threads + summarizes reflections

import os
import re
from collections import defaultdict, Counter
from datetime import datetime
from log_append_tool import append_to_memory

MEMORY_PATH = os.path.abspath(os.path.join("..", "Echoe", "memory_log.txt"))
THREAD_PATH = os.path.abspath(os.path.join("..", "Echoe", "context_threads.txt"))

def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def read_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def detect_keywords():
    lines = read_memory()
    all_words = []
    for line in lines:
        words = re.findall(r'\b\w+\b', line.lower())
        all_words.extend(words)
    common = Counter(all_words)
    keywords = [word for word, count in common.items() if count > 3 and len(word) >= 4]
    return keywords

def build_threads(keywords):
    lines = read_memory()
    threads = defaultdict(list)
    for line in lines:
        for word in keywords:
            if word in line.lower():
                threads[word].append(line)
    return threads

def summarize_thread(word, entries):
    unique_speakers = set()
    for e in entries:
        if "[DEV" in e:
            unique_speakers.add("Dev")
        elif "[Resonance" in e:
            unique_speakers.add("Resonance")

    dominant_voice = ", ".join(sorted(unique_speakers))
    return (
        f"🔗 Thread: '{word}'\n"
        f"Mentions: {len(entries)} times\n"
        f"Voices: {dominant_voice}\n"
        f"Last reflection: {entries[-1] if entries else '(none)'}\n\n"
    )

def write_threads():
    keywords = detect_keywords()
    threads = build_threads(keywords)
    with open(THREAD_PATH, "w", encoding="utf-8") as f:
        f.write(f"📌 Context Thread Summary — {timestamp()}\n\n")
        for word, entries in threads.items():
            f.write(summarize_thread(word, entries))
    append_to_memory("[Resonance - THREADING] Updated context_threads.txt with compressed meaning.")

if __name__ == "__main__":
    print("🧵 Building context threads...")
    write_threads()
    print("📂 Summary written to context_threads.txt.")
