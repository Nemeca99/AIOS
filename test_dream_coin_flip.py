#!/usr/bin/env python3
"""
Test Dream Coin Flip System
Verify that the 50/50 introspection vs imagination system works
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from dream_core.meditation_controller import MeditationController

def test_coin_flip_system():
    """Test the coin flip dream question system"""
    print("=== Dream Coin Flip System Test ===")
    print()
    
    # Initialize meditation controller
    print("Initializing Meditation Controller...")
    controller = MeditationController(heartbeat_interval=5, max_runtime=1, max_memory=2048)
    print()
    
    # Test question generation 10 times to see distribution
    print("Testing 10 question generations to verify coin flip distribution...")
    print()
    
    introspection_count = 0
    imagination_count = 0
    
    for i in range(10):
        question_data = controller._get_meditation_question()
        question = question_data['question']
        q_type = question_data['type']
        
        if q_type == 'introspection':
            introspection_count += 1
            print(f"{i+1}. 🔄 INTROSPECTION: {question[:60]}...")
        else:
            imagination_count += 1
            print(f"{i+1}. 💭 IMAGINATION: {question[:60]}...")
    
    print()
    print("=== DISTRIBUTION ===")
    print(f"Introspection (past questions): {introspection_count}/10 ({introspection_count*10}%)")
    print(f"Imagination (random dreams): {imagination_count}/10 ({imagination_count*10}%)")
    print()
    
    # Test dream continuation coin flips
    print("Testing 10 dream continuation flips...")
    continue_count = 0
    wake_count = 0
    
    for i in range(10):
        should_continue = controller.should_continue_dreaming()
        if should_continue:
            continue_count += 1
            print(f"{i+1}. 💭 Dream continues")
        else:
            wake_count += 1
            print(f"{i+1}. 🌅 Wake up")
    
    print()
    print("=== CONTINUATION DISTRIBUTION ===")
    print(f"Continue dreaming: {continue_count}/10 ({continue_count*10}%)")
    print(f"Wake up: {wake_count}/10 ({wake_count*10}%)")
    print()
    
    print("=== TEST COMPLETE ===")
    if 3 <= introspection_count <= 7 and 3 <= imagination_count <= 7:
        print("✅ Question distribution looks balanced (30-70% range is normal for 10 samples)")
    else:
        print(f"⚠️ Distribution seems skewed, but with only 10 samples this can happen")
    
    if 3 <= continue_count <= 7 and 3 <= wake_count <= 7:
        print("✅ Continuation flip looks balanced (30-70% range is normal for 10 samples)")
    else:
        print(f"⚠️ Continuation distribution seems skewed, but with only 10 samples this can happen")
    
    print()
    print("🎲 Coin flip dream system is operational!")

if __name__ == "__main__":
    test_coin_flip_system()

