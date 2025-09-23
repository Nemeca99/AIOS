# system_status_report.py
# Outputs a brief status of Archive system files

import os

def check_file(path):
    return "✅ FOUND" if os.path.exists(path) else "❌ MISSING"

def system_status():
    base = "Archive"
    core = os.path.join(base, "core")
    echoe = os.path.join(base, "Echoe")

    files = {
        "memory_log.txt": os.path.join(echoe, "memory_log.txt"),
        "personality.py": os.path.join(core, "personality.py"),
        "brain_loop.py": os.path.join(core, "brain_loop.py"),
        "archive_chat.py": os.path.join(core, "archive_chat.py"),
        "log_append_tool.py": os.path.join(core, "log_append_tool.py"),
        "dev_message_tool.py": os.path.join(core, "dev_message_tool.py"),
        "clean_shutdown.py": os.path.join(core, "clean_shutdown.py"),
        "echoe_identity_check.py": os.path.join(core, "echoe_identity_check.py"),
    }

    print("📋 ARCHIVE STATUS CHECK")
    for name, path in files.items():
        print(f"{name:25} {check_file(path)}")

if __name__ == "__main__":
    system_status()
