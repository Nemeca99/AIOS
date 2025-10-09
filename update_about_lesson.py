import json

# Load lessons
with open('data_core/ArbiterCache/lessons.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

# Update the first lesson (Tell me about yourself)
lessons[0]['gold_standard'] = "What would you like to know? I process things a bit differently than most people... I get really focused on stuff that interests me, I'm pretty direct (sometimes too direct lol), and I overthink things. A lot. Still figuring myself out, but that's kinda the point, right?"

# Save
with open('data_core/ArbiterCache/lessons.json', 'w', encoding='utf-8') as f:
    json.dump(lessons, f, indent=2, ensure_ascii=False)

print("✅ Updated 'tell me about yourself' to be more natural")

