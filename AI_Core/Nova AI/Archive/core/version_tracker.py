# version_tracker.py
# Used to log version milestones in the Archive

def write_version(version_note):
    with open("Archive/06_Archives/Version_History/version_notes.txt", "a", encoding="utf-8") as f:
        f.write(version_note + "\n")
