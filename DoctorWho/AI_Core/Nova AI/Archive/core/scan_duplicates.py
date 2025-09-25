import os
import hashlib
from collections import defaultdict

# 🔧 Set this to your target directory
archive_path = r"E:\Nova AI\Archive"

# Store hashes and their associated file paths
hash_dict = defaultdict(list)

def compute_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

print("🔍 Scanning for duplicate files...")

# Walk through directory and hash all files
for root, _, files in os.walk(archive_path):
    for name in files:
        path = os.path.join(root, name)
        file_hash = compute_hash(path)
        if file_hash:
            hash_dict[file_hash].append(path)

# Find and display duplicates
duplicates_found = False
for file_hash, paths in hash_dict.items():
    if len(paths) > 1:
        duplicates_found = True
        print(f"\n🧩 Duplicate Group (SHA-256: {file_hash}):")
        total_size = 0
        for p in paths:
            size = os.path.getsize(p)
            total_size += size
            print(f"   {p} ({size / 1024:.2f} KB)")
        print(f"   🧮 Total Size: {total_size / (1024 * 1024):.2f} MB")

if not duplicates_found:
    print("✅ No exact duplicate files found.")

print("\n✅ Duplicate scan complete.")
