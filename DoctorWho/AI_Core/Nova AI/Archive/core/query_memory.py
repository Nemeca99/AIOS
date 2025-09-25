# query_memory.py
# Offline command tool to query memory_log.txt for specific terms or sessions

import os

MEMORY_PATH = r"E:\\Nova AI\\Archive\\Echoe\\memory_log.txt"

def search_memory(term):
    if not os.path.exists(MEMORY_PATH):
        print("❌ memory_log.txt not found.")
        return
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"🔍 Searching for: '{term}'\n")
    found = False
    for line in lines:
        if term.lower() in line.lower():
            print(line.strip())
            found = True
    if not found:
        print("⚠️ No matches found.")

if __name__ == "__main__":
    term = input("Enter keyword or session to search: ")
    search_memory(term)