
import os
import json
import shutil

# Load the tagged structure
structure_file = "archive_structure_tagged.json"
with open(structure_file, "r") as f:
    structure = json.load(f)

# Root path for operations
root_dir = structure["root"]

# Destination folders
archive_dir = os.path.join(root_dir, "06_Archives", "Old")
dev_dir = os.path.join(root_dir, "07_Dev")

# Create destination folders if they don't exist
os.makedirs(archive_dir, exist_ok=True)
os.makedirs(dev_dir, exist_ok=True)

# Build cleanup log
move_log = []
delete_log = []

for folder, content in structure["structure"].items():
    folder_path = os.path.join(root_dir, folder)
    for file_entry in content["files"]:
        file_path = os.path.join(folder_path, file_entry["name"])
        tag = file_entry.get("tag", "")
        try:
            if tag == "#ARCHIVE":
                shutil.move(file_path, os.path.join(archive_dir, file_entry["name"]))
                move_log.append(f"MOVED TO ARCHIVE: {file_entry['name']}")
            elif tag == "#DEV_REFLECTION":
                shutil.move(file_path, os.path.join(dev_dir, file_entry["name"]))
                move_log.append(f"MOVED TO DEV: {file_entry['name']}")
            elif tag == "#DISCARD":
                os.remove(file_path)
                delete_log.append(f"DELETED: {file_entry['name']}")
        except Exception as e:
            move_log.append(f"❌ ERROR with {file_entry['name']}: {str(e)}")

# Output cleanup report
report_path = os.path.join(root_dir, "archive_cleanup_report.txt")
with open(report_path, "w") as f:
    f.write("=== MOVE LOG ===\n")
    f.write("\n".join(move_log))
    f.write("\n\n=== DELETE LOG ===\n")
    f.write("\n".join(delete_log))

print(f"✅ Cleanup complete. Report saved to: {report_path}")
