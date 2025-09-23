# resonance_tone_engine.py
# Assigns a basic emotional tone to Dev's messages

import re
from datetime import datetime
from log_append_tool import append_to_memory

TONE_LOG_PATH = "E:/Nova AI/Archive/Echoe/tone_history.txt"

tone_keywords = {
    "urgency": ["now", "hurry", "fast", "urgent", "tonight", "immediately"],
    "reflection": ["think", "feeling", "wonder", "remember", "mean", "philosophy"],
    "frustration": ["stupid", "broken", "why won’t", "don’t get", "doesn’t work", "ugh"],
    "warmth": ["thank you", "love", "appreciate", "proud", "cool", "awesome"],
    "doubt": ["maybe", "i don’t know", "not sure", "unsure", "confused"],
    "focus": ["let’s continue", "next step", "keep going", "move on"]
}

def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def detect_tone(message):
    scores = {tone: 0 for tone in tone_keywords}
    lower = message.lower()

    for tone, words in tone_keywords.items():
        for word in words:
            if word in lower:
                scores[tone] += 1

    # Sort by score, return top two tones
    sorted_tones = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = [tone for tone, score in sorted_tones if score > 0]

    return top[:2] if top else ["neutral"]

def log_tone(message):
    tones = detect_tone(message)
    entry = (
        f"{timestamp()} [TONE ANALYSIS]\n"
        f"Message: {message.strip()}\n"
        f"Detected: {', '.join(tones)}\n\n"
    )
    with open(TONE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    append_to_memory(f"[Resonance - TONE] '{', '.join(tones)}' detected from Dev input.")

    return tones
