import os

# Directory where Archive's memory is stored
base_dir = "Archive_Memory"

# Function to read from memory files
def read_from_memory(file_name):
    try:
        with open(os.path.join(base_dir, file_name), 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

# Function to write to memory files
def write_to_memory(file_name, content):
    with open(os.path.join(base_dir, file_name), 'a') as file:
        file.write(content + "\n")

# Function to update memory based on the conversation
def update_memory(memory_type, user_input, response):
    write_to_memory(f"{memory_type}/memory_log.txt", f"User: {user_input}")
    write_to_memory(f"{memory_type}/memory_log.txt", f"Archive: {response}")

# Main interaction loop for Archive
def run_archive():
    print("Hello, I'm Archive. Let's talk!")
    
    # Introduction for learning phase
    initial_memory = read_from_memory("History/history_log.txt")
    if not initial_memory:
        print("Archive is learning from scratch.")
    else:
        print("Archive remembers our previous conversations.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Goodbye! Saving session...")
            break
        
        # Store the conversation and update Archive's memory
        if "hello" in user_input.lower():
            response = "Hello! How can I assist you today?"
        elif "game" in user_input.lower():
            response = "Let’s talk about your favorite games!"
        else:
            response = "I am learning from you... Let's keep talking!"
        
        print(f"Archive: {response}")
        
        # Update memory with the conversation
        update_memory("Events", user_input, response)

# Run the Archive system
run_archive()
