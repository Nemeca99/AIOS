import os

SOURCE_DIR = r"E:\\Nova AI\\Archive\\Online Memories"

def clean_text(content):
    return content.replace("\r", "").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2014", "--")

def auto_clean_memory_logs():
    if not os.path.exists(SOURCE_DIR):
        print("❌ Online Memories folder not found.")
        return

    cleaned_count = 0
    for filename in os.listdir(SOURCE_DIR):
        if filename.lower().endswith(".txt"):
            full_path = os.path.join(SOURCE_DIR, filename)
            try:
                with open(full_path, "rb") as f:
                    raw = f.read()
                decoded = raw.decode("utf-8", errors="replace")
                cleaned = clean_text(decoded)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                cleaned_count += 1
            except Exception as e:
                print(f"❌ Failed to clean {filename}: {e}")
    print(f"✅ Cleaned {cleaned_count} memory file(s).")

if __name__ == "__main__":
    auto_clean_memory_logs()