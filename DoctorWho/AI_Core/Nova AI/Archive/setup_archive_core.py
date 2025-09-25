import os

# Define base folder for the Archive core system
core_dir = os.path.join(os.getcwd(), "Archive", "core")
os.makedirs(core_dir, exist_ok=True)

# File definitions
files_to_create = {
    "archive_chat.py": """# archive_chat.py
# Terminal chat interface for Archive AI

import memory_engine

print("📣 ARCHIVE READY. Type your message. Type 'exit' to quit.")

while True:
    user_input = input("Dev: ")
    if user_input.lower() in ['exit', 'quit']:
        print("👋 Archive signing off.")
        break
    response = memory_engine.process(user_input)
    print("Archive:", response)
""",

    "memory_engine.py": """# memory_engine.py
# Handles storing input to Archive memory

def process(user_input):
    log_line = f"[Dev] {user_input}\\n"
    with open("Archive/Echoe/memory_log.txt", "a", encoding="utf-8") as f:
        f.write(log_line)
    return f"I've logged that: '{user_input}'. What would you like to do next?"
""",

    "version_tracker.py": """# version_tracker.py
# Used to log version milestones in the Archive

def write_version(version_note):
    with open("Archive/06_Archives/Version_History/version_notes.txt", "a", encoding="utf-8") as f:
        f.write(version_note + "\\n")
"""
}

# Create each file
for filename, content in files_to_create.items():
    path = os.path.join(core_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ setup_archive_core.py has created the Archive/core system with all files.")
