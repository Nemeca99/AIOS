import os
import json

# Root directory to scan
root_dir = r"E:\Nova AI\Archive"  # Change this if needed

def scan_structure(base_path):
    structure = {}
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            structure[folder_name] = {
                "description": "",
                "files": []
            }
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    structure[folder_name]["files"].append({
                        "name": file_name,
                        "tag": ""  # You or I can fill this later (e.g., #CORE, #DISCARD, etc.)
                    })
    return structure

# Run scan and save JSON
archive_structure = {
    "root": root_dir,
    "structure": scan_structure(root_dir)
}

output_path = os.path.join(root_dir, "archive_structure.json")
with open(output_path, "w") as f:
    json.dump(archive_structure, f, indent=4)

print(f"✅ archive_structure.json saved to: {output_path}")
