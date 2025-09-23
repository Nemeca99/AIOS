import os

# Path to scan
base_path = r"E:\Nova AI"

print(f"\n📁 Contents of {base_path}\n")

# Walk top-level only
with os.scandir(base_path) as entries:
    for entry in entries:
        size = os.path.getsize(entry.path) if entry.is_file() else "-"
        type_label = "📄 FILE " if entry.is_file() else "📂 FOLDER"
        size_str = f"{size / (1024 * 1024):.2f} MB" if size != "-" else ""
        print(f"{type_label:10} {entry.name:40} {size_str}")
