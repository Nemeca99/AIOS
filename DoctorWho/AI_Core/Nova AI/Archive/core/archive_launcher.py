# archive_launcher.py
# Entry point for Archive boot sequence (local execution only)

from session_log_init import log_session_start
from archive_chat import main as chat_main
from memory_loader import load_memory_log
from directives_registry import initialize_directives
from presence_layer import ArchivePresence

if __name__ == "__main__":
    presence = ArchivePresence()
    presence.detect_environment()
    presence.apply_personality()

    log_session_start()
    memory = load_memory_log()
    directives = initialize_directives()
    print(f"[🧬 Persona: {presence.persona}] — Mode: {presence.mode}")
    chat_main()
