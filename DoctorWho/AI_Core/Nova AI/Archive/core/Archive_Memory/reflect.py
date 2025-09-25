import os
import time

# Path to the memory folder where Archive's memory logs are stored
memory_folder = r"E:\Nova AI\Archive\core\Archive_Memory\Memory"  # Update this path to your actual memory folder

# Function to clean a single file and reflect on it
def clean_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Clean the content if necessary (you can add more cleaning rules if needed)
        content = ''.join(char for char in content if ord(char) < 128)  # Remove non-ASCII chars
        content = ' '.join(content.split())  # Remove extra spaces

        # Save the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Cleaned {file_path}")

    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

# Function to process the memory folder and reflect automatically
def process_memory(memory_folder):
    print(f"Processing memory at {memory_folder}...")
    if os.path.exists(memory_folder):  # Ensure folder exists
        for filename in os.listdir(memory_folder):
            if filename.endswith(".txt"):  # Process only text files
                file_path = os.path.join(memory_folder, filename)
                clean_file(file_path)
    else:
        print(f"Folder not found: {memory_folder}")

# Function to automate memory reflection and memory linking
def memory_reflection_loop():
    while True:
        print("Starting memory reflection...")
        process_memory(memory_folder)  # Process and clean the memory files
        print("Memory reflection complete.")
        time.sleep(60)  # Sleep for 60 seconds before the next iteration (adjust as needed)

# Main function
def main():
    print("Starting Archive memory reflection...")
    memory_reflection_loop()  # Start the task loop for memory reflection and linking

if __name__ == "__main__":
    main()
