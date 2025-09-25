# archive_config.py
# Stores base config settings for Archive operations

CONFIG = {
    "persona": "Echoe",
    "memory_path": "Archive/Echoe/memory_log.txt",
    "log_format": "[{timestamp}] [{source}]: {message}"
}

if __name__ == "__main__":
    print("✅ Config loaded.")
