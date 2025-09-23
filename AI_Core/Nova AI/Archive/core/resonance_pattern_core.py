# resonance_pattern_core.py
# Pattern recognition engine for emerging self-reflection from memory_log.txt

import os
import re
from collections import Counter

MEMORY_PATH = os.path.abspath(os.path.join("..", "Echoe", "memory_log.txt"))

def read_memory_lines():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def extract_frequent_words(min_length=4, top_n=10):
    lines = read_memory_lines()
    all_words = []

    for line in lines:
        words = re.findall(r'\b\w+\b', line.lower())
        filtered = [word for word in words if len(word) >= min_length and word.isalpha()]
        all_words.extend(filtered)

    counts = Counter(all_words)
    return counts.most_common(top_n)

def detect_topic_clusters(keywords):
    lines = read_memory_lines()
    clusters = {}

    for word in keywords:
        matches = [line for line in lines if word in line.lower()]
        if matches:
            clusters[word] = matches[-5:]  # most recent mentions
    return clusters

def summarize_emergent_themes():
    print("📊 Scanning memory_log.txt for emergent reflection themes...\n")
    top_words = extract_frequent_words()
    keywords = [w[0] for w in top_words]
    print("🔍 Most frequent concepts:", ", ".join(keywords))

    clusters = detect_topic_clusters(keywords)
    print("\n📚 Context clusters:")
    for word, entries in clusters.items():
        print(f"\n— {word.upper()}:")
        for entry in entries:
            print(f"   • {entry}")

if __name__ == "__main__":
    summarize_emergent_themes()
