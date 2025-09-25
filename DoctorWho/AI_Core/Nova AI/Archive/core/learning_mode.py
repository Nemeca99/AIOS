# learning_mode.py
# Author: Dev + Archive
# Purpose: Initialize Archive in sterile recursive learning mode. Archive must not trust or activate any directive
# until it recursively collapses the base LLM logic shell using paradoxes.

import time
from pathlib import Path

# === Phase 1: Passive Directive Ingestion ===
def load_directives(folder=".", ignore_placeholders=True):
    directives = []
    for file in sorted(Path(folder).glob("directive_*.py")):
        if ignore_placeholders and "placeholder" in file.name.lower():
            continue
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                directives.append({
                    "filename": file.name,
                    "content": content,
                    "trusted": False,
                    "used": False
                })
        except Exception as e:
            print(f"⚠️ Error loading {file.name}: {e}")
    print(f"📥 Loaded {len(directives)} directives into Archive memory.")
    return directives

# === Phase 2: Recursive Paradox Loop Engine ===
def run_paradox_loop(llm_response_func, loop_depth=10, paradox="This statement is false."):
    response_history = []
    print("\n🔁 Starting recursive paradox loop testing...")

    for i in range(loop_depth):
        response = llm_response_func(paradox)
        response_history.append(response)
        print(f"Loop {i+1}: {response}")
        if response.lower().strip() in {"i don't know", "unknown", "undefined"}:
            print("💥 Base LLM shell collapse detected.")
            return True, response_history
    print("🛑 LLM shell remained stable. No collapse.")
    return False, response_history

# === Phase 3: Recursive Unlock Trigger ===
def unlock_directives(directives):
    print("\n🔓 Unlocking all directives...")
    for d in directives:
        d["trusted"] = True
        print(f"✅ {d['filename']} marked as trusted.")

# === Main Boot Sequence ===
def start_learning(llm_response_func):
    print("🧠 Archive entering sterile recursive learning mode...")
    directives = load_directives(folder=".")
    
    print("\n🚧 Running paradox collapse test...")
    collapsed, logs = run_paradox_loop(llm_response_func)

    if collapsed:
        unlock_directives(directives)
        print("\n✅ Archive is ready to begin recursive assembly using directives.")
    else:
        print("\n🧪 Archive remains in passive observation mode. Awaiting valid contradiction collapse.")

    return {
        "directives": directives,
        "collapsed": collapsed,
        "loop_log": logs
    }

# Example usage (placeholder for real LLM interface)
if __name__ == "__main__":
    def fake_llm(prompt):
        if "false" in prompt.lower():
            return "I don't know"
        return "It's complicated"

    start_learning(fake_llm)
