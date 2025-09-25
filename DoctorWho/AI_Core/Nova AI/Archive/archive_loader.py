import os

# Function to load memory files into Archive
def load_memory(memory_folder):
    memory_data = ""
    # Loop through the folder and read all memory files
    for filename in os.listdir(memory_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(memory_folder, filename), 'r') as file:
                memory_data += file.read() + "\n"
    return memory_data

# Function to initialize Archive and load the memory
def initialize_archive(memory_data):
    print("Loading Archive's memory...")
    # Logic for Archive to use the memory and reflect
    print("Memory Loaded. Archive is now reflecting on the data.")
    return memory_data  # This will be Archive's loaded memory

# Main function to run everything
def main():
    memory_folder = "E:/Nova AI/Archive/Archive_Memory"  # Adjust the path to your memory folder
    memory_data = load_memory(memory_folder)
    archive_data = initialize_archive(memory_data)
    
    # Archive is now ready to reflect, process, and learn from the loaded memory
    print("Archive is ready to grow. Let's continue the journey!")

if __name__ == "__main__":
    main()
