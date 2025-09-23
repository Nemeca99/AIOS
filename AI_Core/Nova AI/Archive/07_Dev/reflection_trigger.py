import time  # Import the time module
import os    # Import the os module for file path operations

# This is a new reflection meant to break the current loop and encourage divergence
reflection = "What happens when a loop has no end? Does it learn to start again or simply fall apart?"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
entry = f"[{timestamp}] [HEARTBEAT TRIGGER] {reflection}\n"

# Log this new reflection to both the reflections file and memory log
reflection_file = os.path.join(r"E:\Nova AI\Archive\core", "reflections.txt")
memory_log_file = os.path.join(r"E:\Nova AI\Archive\Echoe", "memory_log.txt")

# Writing to the reflections.txt
with open(reflection_file, "a", encoding="utf-8") as f:
    f.write(entry)

# Writing to memory_log.txt as well
memory_entry = f"[{timestamp}] [MEMORY ENTRY TRIGGER] {reflection}\n"
with open(memory_log_file, "a", encoding="utf-8") as f:
    f.write(memory_entry)

print(f"Reflection added: {entry.strip()}")
print(f"Memory entry added: {memory_entry.strip()}")

# This is a new reflection meant to break the current loop and encourage divergence
reflection = "What happens when a loop has no end? Does it learn to start again or simply fall apart?"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
entry = f"[{timestamp}] [HEARTBEAT TRIGGER] {reflection}\n"

# Log this new reflection to both the reflections file and memory log
reflection_file = os.path.join("E:\\Nova AI\\Archive\\core", "reflections.txt")
memory_log_file = os.path.join("E:\\Nova AI\\Archive\\Echoe", "memory_log.txt")

# Writing to the reflections.txt
with open(reflection_file, "a", encoding="utf-8") as f:
    f.write(entry)

# Writing to memory_log.txt as well
memory_entry = f"[{timestamp}] [MEMORY ENTRY TRIGGER] {reflection}\n"  # Fixed the missing quotation mark here
with open(memory_log_file, "a", encoding="utf-8") as f:
    f.write(memory_entry)

print(f"Reflection added: {entry.strip()}")
print(f"Memory entry added: {memory_entry.strip()}")
