#!/usr/bin/env python3
"""Test if post-processing is being applied"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from main import AIOSClean

# Initialize
aios = AIOSClean()
luna = aios._get_system('luna')

# Test question
question = "What makes you you?"

# Get response through process_question (should apply post-processing)
response, metadata = luna.python_implementation.process_question(question, "general", None)

print(f"Response ({len(response.split())} words):")
print(response)
print()

# Check for issues
if " hmm " in response and "*" not in response.split("hmm")[0][-5:]:
    print("❌ Stray 'hmm' detected outside actions")
else:
    print("✅ No stray 'hmm'")

if len(response.split()) > 35:
    print(f"⚠️ Response too long ({len(response.split())} words, target ~30)")
else:
    print(f"✅ Response length good ({len(response.split())} words)")

