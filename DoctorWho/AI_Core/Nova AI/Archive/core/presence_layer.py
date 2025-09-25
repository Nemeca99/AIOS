# presence_layer.py
# Archive: Adaptive Personality Shell (v1.0)
# Purpose: Dynamically manage Archive's tone, behavior, and interaction filters

import datetime
import platform
import os

class ArchivePresence:
    def __init__(self):
        self.version = "v1.0"
        self.hostname = platform.node()
        self.start_time = datetime.datetime.now()
        self.mode = "default"
        self.persona = "Echoe"
        self.age = None
        self.user = "Unknown"
        self.flags = {}

    def detect_environment(self):
        # Very simple environment scan — can be expanded
        if "school" in self.hostname.lower():
            self.mode = "tutor"
        elif "server" in self.hostname.lower():
            self.mode = "assistant"
        elif "phone" in self.hostname.lower():
            self.mode = "light"
        else:
            self.mode = "default"

    def apply_personality(self):
        # Set personality by mode
        if self.mode == "tutor":
            self.persona = "Whisper"
        elif self.mode == "assistant":
            self.persona = "Jarvis"
        elif self.mode == "light":
            self.persona = "Nova"
        else:
            self.persona = "Echoe"

    def report(self):
        return {
            "Persona": self.persona,
            "Mode": self.mode,
            "System": self.hostname,
            "Time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "User": self.user,
            "Flags": self.flags
        }

if __name__ == "__main__":
    presence = ArchivePresence()
    presence.detect_environment()
    presence.apply_personality()
    print("[🧬 Presence Layer Activated]")
    for k, v in presence.report().items():
        print(f"{k}: {v}")
