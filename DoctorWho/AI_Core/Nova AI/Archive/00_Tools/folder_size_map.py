import os

# 🔧 Set the root directory
base_path = r"E:\Nova AI\Archive"

def get_folder_size(path):
    total_size = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total_size += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass
    return total_size

folder_sizes = []
for item in os.listdir(base_path):
    full_path = os.path.join(base_path, item)
    if os.path.isdir(full_path):
        size_mb = get_folder_size(full_path) / (1024 * 1024)
        folder_sizes.append((item, round(size_mb, 2)))

# Sort by size descending
folder_sizes.sort(key=lambda x: x[1], reverse=True)

print("📂 Archive Folder Size Breakdown:\n")
for folder, size in folder_sizes:
    print(f"🗂️  {folder:30} {size:.2f} MB")

print("\n✅ Folder scan complete.")
