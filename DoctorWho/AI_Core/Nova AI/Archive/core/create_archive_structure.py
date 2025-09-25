import os

# Define the base directory for Archive's memory storage
base_dir = "Archive_Memory"

# Define the structure of the directories and files
structure = {
    'Master_AI': ['master_ai_log.txt'],
    'Echoe': ['echoe_log.txt'],
    'Characters': ['characters.txt'],
    'Worlds': ['worlds.txt'],
    'Events': ['events_log.txt'],
    'History': ['history_log.txt'],
    'Backup': []  # Empty folder for backups
}

# Function to create the files inside the directories
def create_files(base_dir, structure):
    # Ensure the base directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created directory: {base_dir}")
    
    # Create the subdirectories and files
    for dir_name, files in structure.items():
        dir_path = os.path.join(base_dir, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write("")  # Initialize the file with an empty string
                print(f"Created file: {file_path}")

# Run the script to create the structure and files
create_files(base_dir, structure)
