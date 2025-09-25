import os

SOURCE_DIR = r"E:\\Nova AI\\Archive\\Online Memories"
TARGET_LOG = r"E:\\Nova AI\\Archive\\Echoe\\memory_log.txt"

def import_memories():
    imported_files = 0

    if not os.path.exists(SOURCE_DIR):
        print("❌ Source folder does not exist.")
        return

    with open(TARGET_LOG, "a", encoding="utf-8") as target:
        for filename in sorted(os.listdir(SOURCE_DIR)):
            if filename.lower().endswith(".txt"):
                file_path = os.path.join(SOURCE_DIR, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as src:
                        content = src.read().strip()
                    target.write(f"\n\n=== Imported from {filename} ===\n")
                    target.write(content + "\n")
                    imported_files += 1
                except Exception as e:
                    print(f"❌ Failed to import {filename}: {e}")

    print(f"✅ Imported {imported_files} file(s) into memory_log.txt.")

if __name__ == "__main__":
    import_memories()