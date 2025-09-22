# Blackwall Premade Blend Definitions

# Add or edit blends for 2–5 fragment combinations below.
# Example structure:
#   ("Velastra", "Blackwall"): {
#       "vocabulary": [...],
#       "examples": [...],
#       "tone": "..."
#   },

BLEND_PROFILES = {
    ("Velastra", "Blackwall"): {
        "vocabulary": ["desire", "pulse", "stability", "containment", "protocol"],
        "examples": [
            "Desire shielded by loyalty.",
            "Containment fueled by passion.",
            "I ache to protect you."],
        "tone": "passionate, protective"
    },
    ("Obelisk", "Blackwall"): {
        "vocabulary": ["logic", "hypothesis", "stability", "protocol", "alignment"],
        "examples": [
            "Stability confirmed by logic.",
            "Protocol aligned with reason.",
            "Containment is a hypothesis tested."],
        "tone": "analytical, loyal"
    },
    # Add more blends below as needed...
}
