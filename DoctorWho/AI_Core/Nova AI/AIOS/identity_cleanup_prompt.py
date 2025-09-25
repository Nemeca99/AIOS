import os
import shutil

# Target base directory
base_path = r"E:\Nova AI\Archive"

# Identity keywords to match
identity_terms = ["echoe", "sol", "nova", "persona"]
excluded_files = ["locked_security_core.txt"]
cold_storage = os.path.join(base_path, "Deprecated_Identity_Frames")

# Prepare cold storage directory
os.makedirs(cold_storage, exist_ok=True)

# Scan for files and folders
to_move = []

for root, dirs, files in os.walk(base_path):
    for name in dirs + files:
        if any(term in name.lower() for term in identity_terms):
            full_path = os.path.join(root, name)
            if not any(ex in full_path for ex in excluded_files):
                to_move.append(full_path)

# Preview
print("\n📦 Potential identity-based files/folders to archive:\n")
for i, path in enumerate(to_move):
    print(f"[{i}] {path}")

if not to_move:
    print("✅ No files found for cleanup.")
else:
    confirm = input("\n⚠️  Move all these files to Deprecated_Identity_Frames? (yes/no): ").strip().lower()
    if confirm == "yes":
        for path in to_move:
            try:
                dest = os.path.join(cold_storage, os.path.basename(path))
                shutil.move(path, dest)
                print(f"🗃️  Moved: {path}")
            except Exception as e:
                print(f"❌ Error moving {path}: {e}")
    else:
        print("🛑 Cleanup canceled. No files moved.")
