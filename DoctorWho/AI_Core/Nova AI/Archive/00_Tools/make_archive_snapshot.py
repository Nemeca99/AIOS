
import os
import shutil
import zipfile
from datetime import datetime

# === CONFIG ===
archive_root = r"E:\Nova AI\Archive"

files_to_include = [
    "archive_structure.json",
    "personality.txt",
    "locked_security_core.txt",
    "memory_log.txt",
    "dev_commands.txt",
    "reflection_log.txt",
    "core_config.py",
    "run_this_first.py",
    "reflection_engine.py",
    "task_handler.py",
    "archive_voice.py",
    "bootstrap.py",
    "build_index.py",
    "archive_cleanup_local.py",
    "session_tracker.json",
    "vault_map.json",
    "directive_registry.json",
    "module_flags.json"
]

temp_dir = os.path.join(archive_root, "temp_snapshot")
os.makedirs(temp_dir, exist_ok=True)

copied_files = []
for file in files_to_include:
    src = os.path.join(archive_root, file)
    if os.path.exists(src):
        dst = os.path.join(temp_dir, file)
        shutil.copy2(src, dst)
        copied_files.append(file)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_name = f"archive_snapshot_{timestamp}.zip"
zip_path = os.path.join(archive_root, zip_name)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in copied_files:
        zipf.write(os.path.join(temp_dir, file), arcname=file)

shutil.rmtree(temp_dir)
print(f"✅ Snapshot complete: {zip_path}")
