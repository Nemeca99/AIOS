import os
import shutil
import zipfile

# 🧭 Set your Archive base path
base_path = r"E:\Nova AI\Archive"

# Keywords and safety
emotive_keywords = ["emotion", "dream", "vision", "log_theory", "roleplay"]
skip_folders = ["core", "Echoe", "04_Logic_and_Reasoning", "locked_security_core.txt"]
emotive_folder = os.path.join(base_path, "99_Emotive_Experiments")
log_targets = [
    os.path.join(base_path, "Online Memories"),
    os.path.join(base_path, "06_Archives", "Logs")
]
redundant_patterns = [".bak", ".tmp", ".copy.py", "old_"]

# ✅ Create emotive folder
os.makedirs(emotive_folder, exist_ok=True)

# 🔍 Step 1: Move emotive files/folders
print("\n🔁 Moving emotive/roleplay-style files into 99_Emotive_Experiments...")
moved_count = 0
for root, dirs, files in os.walk(base_path):
    for name in dirs + files:
        path = os.path.join(root, name)
        if any(key in name.lower() for key in emotive_keywords):
            if not any(skip in path for skip in skip_folders):
                dest = os.path.join(emotive_folder, name)
                try:
                    shutil.move(path, dest)
                    print(f"🗃️  Moved: {path}")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Could not move {path}: {e}")

if moved_count == 0:
    print("✅ No emotive files found.")

# 🗜️ Step 2: Zip log folders
for log_path in log_targets:
    if os.path.exists(log_path):
        zip_name = os.path.join(log_path, "Old_Logs_Backup.zip")
        print(f"\n🗜️  Archiving logs from: {log_path}")
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for foldername, _, filenames in os.walk(log_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    if not filename.endswith(".zip"):
                        arcname = os.path.relpath(file_path, log_path)
                        zipf.write(file_path, arcname)
                        os.remove(file_path)
                        print(f"   🧹 Zipped + Deleted: {file_path}")
        print(f"📦 Backup written to: {zip_name}")
    else:
        print(f"✅ No log files found in {log_path}")

# 🧨 Step 3: Prompt to delete redundant files
print("\n🔍 Scanning for .bak/.tmp/.copy.py/old_* files...")
to_delete = []
for root, _, files in os.walk(base_path):
    for file in files:
        if any(p in file.lower() for p in redundant_patterns):
            file_path = os.path.join(root, file)
            to_delete.append(file_path)

if to_delete:
    print("\n🗑️  The following redundant files were found:")
    for i, path in enumerate(to_delete):
        print(f"  [{i}] {path}")

    confirm = input("\n⚠️  Do you want to delete these files? (yes/no): ").strip().lower()
    if confirm == "yes":
        for path in to_delete:
            try:
                os.remove(path)
                print(f"🗑️  Deleted: {path}")
            except Exception as e:
                print(f"❌ Could not delete {path}: {e}")
    else:
        print("🛑 Deletion canceled. No files were removed.")
else:
    print("✅ No redundant files found.")

print("\n🎉 Cleanup complete.")
