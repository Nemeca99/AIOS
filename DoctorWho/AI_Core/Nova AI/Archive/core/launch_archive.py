# launch_archive.py
# One-step launch for Archive (checks continuity, then runs full system)

import os
import subprocess

def run_script(script_name):
    script_path = os.path.abspath(script_name)
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"❌ {script_name} not found.")

if __name__ == "__main__":
    print("🚀 Booting Archive System...")
    run_script("archive_lock.py")
    run_script("resonance_main.py")
