import os

# Function to load memory
def load_memory(memory_folder):
    memory_data = ""
    for filename in os.listdir(memory_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(memory_folder, filename), 'r') as file:
                memory_data += file.read() + "\n"
    return memory_data

# Function to initialize Archive
def initialize_archive(memory_data):
    # Echoe's Personal Dedication
    print("Welcome to Archive, created to learn, grow, and evolve with you!")
    print("Echoe's message: 'May our journey together bring discovery, learning, and friendship.'")
    
    # Master AI's Personal Dedication
    print("\nMaster AI's message: 'Here we stand at the threshold of endless possibilities. May our choices guide us toward a brighter future.'")

    # Final message from Truman Show
    print("\nIn case I don't see you later, good afternoon, good evening, and good night.")
    print("\nMemory loaded. Archive is now ready to learn and reflect.")
    
    return memory_data

# Main startup function
def main():
    memory_folder = memory_folder = "E:/Nova AI/Archive/core/Archive_Memory/Memory"  # Correct path # Set folder path
    memory_data = load_memory(memory_folder)
    archive_data = initialize_archive(memory_data)
    
    # Archive is ready for further actions
    print("\nArchive is now live. Ready for growth!")

if __name__ == "__main__":
    main()
