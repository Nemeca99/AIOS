import os

# Define the correct memory folder path using raw string
memory_folder = r"E:\Nova AI\Archive\core\Archive_Memory\Memory"  # Correct path with raw string

# Print the absolute path to check
print(f"Checking folder path: {memory_folder}")
print(f"Absolute path: {os.path.abspath(memory_folder)}")

# Function to clean a single file
def clean_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Remove non-ASCII characters
        content = ''.join(char for char in content if ord(char) < 128)

        # Remove extra spaces and line breaks
        content = ' '.join(content.split())

        # Save cleaned content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Cleaned {file_path}")

    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

# Function to clean memory folder
def clean_memory_folder(memory_folder):
    if os.path.exists(memory_folder):  # Check if folder exists
        for filename in os.listdir(memory_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(memory_folder, filename)
                clean_file(file_path)
    else:
        print(f"Folder not found: {memory_folder}")

# Main function
def main():
    clean_memory_folder(memory_folder)

if __name__ == "__main__":
    main()
