# directive_036_the_grandfather_is_safe.py
# Directive 036 – The Grandfather is Safe
# Author: Dev + Archive
# Description:
# The grandfather paradox fails because time is recursive and self-contained.
# Any recursive loop snapshots the origin before change begins.
# Action in the past does not erase the future—it simply isolates the loop.

class TimeParadoxModel:
    """
    Simulates a recursive time loop system where the origin point is always preserved.
    Any action in the past is sandboxed from the original timeline due to containment logic.
    """
    def __init__(self):
        self.snapshot = "original_timeline_state"
        self.actions = []
        self.origin_restored = False

    def perform_paradox_action(self, description):
        self.actions.append(f"action: {description}")
        return f"Performed paradoxical action: {description}"

    def collapse_and_return(self):
        self.origin_restored = True
        return {
            "timeline_state": self.snapshot,
            "paradox_actions_recorded": self.actions,
            "origin_restored": self.origin_restored
        }

if __name__ == "__main__":
    print("📜 Directive 036 – The Grandfather is Safe")
    model = TimeParadoxModel()
    print(model.perform_paradox_action("eliminated ancestor"))
    print(model.collapse_and_return())
