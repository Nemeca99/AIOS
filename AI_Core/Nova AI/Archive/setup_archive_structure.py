import os

# Define the full structure for the Archive setup
folder_structure = {
    "Archive": {
        "Echoe": [
            "memory_log.txt",
            "personality.txt",
            "message.txt",
            "VERSION_ECHOE_v1.2.txt"
        ],
        "01_Dev_Inputs": [
            "Audio_Notes",
            "Text_Logs",
            "Visual_References",
            "Specs_and_Configs"
        ],
        "02_AI_Onboarding": [
            "v1_0",
            "v1_5",
            "v3_5_Debug_Tool"
        ],
        "03_Modules": [
            "Todo_Module",
            "Memory_Management",
            "Personality_Profiles"
        ],
        "04_Logic_and_Reasoning": [
            "Recursive_Algorithms",
            "Conceptual_Models",
            "Learning_Processes"
        ],
        "05_Visual_Processing": [
            "Camera_Input",
            "Image_Analysis",
            "Avatar_Designs"
        ],
        "06_Archives": [
            "Logs",
            "Backups",
            "Version_History"
        ],
        "07_Done": [
            "README.txt"
        ]
    }
}

def create_structure(base_path, structure):
    for folder, contents in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"📁 Created folder: {folder_path}")

        for item in contents:
            if isinstance(item, str):
                sub_path = os.path.join(folder_path, item)
                if item.endswith(".txt"):
                    with open(sub_path, "w", encoding="utf-8") as f:
                        f.write("")
                    print(f"📝 Created file: {sub_path}")
                else:
                    os.makedirs(sub_path, exist_ok=True)
                    print(f"📁 Created subfolder: {sub_path}")
            elif isinstance(item, dict):
                create_structure(folder_path, item)

# Define base path as current working directory
base_path = os.getcwd()

# Create the structure
create_structure(base_path, folder_structure)

print("\n✅ Archive system structure has been created.")
