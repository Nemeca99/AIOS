#!/usr/bin/env python3
"""
Blind test - model: openhermes-2.5-neural-chat-7b-v3-1-7b@q4_k_m
Testing 20 questions, no knowledge of other changes
"""

import sys
from pathlib import Path
from collections import Counter

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_blind():
    """Blind test with various questions"""
    
    # Import after path setup
    from main import AIOSClean
    
    # Initialize AIOS
    print("🔍 Initializing AIOS...")
    aios = AIOSClean()
    luna = aios._get_system('luna')
    
    # Test questions
    questions = [
        "What makes you unique?",
        "What makes you unique?",
        "What makes you unique?",
        "Tell me about yourself",
        "Tell me about yourself",
        "How are you?",
        "How are you?",
        "What are you interested in?",
        "What are you interested in?",
        "What's on your mind?",
        "What's on your mind?",
        "How would you describe yourself?",
        "How would you describe yourself?",
        "What do you think about?",
        "What do you think about?",
        "What's important to you?",
        "What's important to you?",
        "What drives you?",
        "What drives you?",
        "Who are you?"
    ]
    
    print(f"\n🧪 BLIND TEST - NEURAL CHAT Q4_K_M:")
    print(f"Testing {len(questions)} questions")
    print("=" * 80)
    
    responses = []
    first_words = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i:2d}. Q: {question}")
        
        try:
            response, metadata = luna.python_impl.process_question(
                question, 
                "general", 
                None
            )
            
            responses.append(response)
            
            # Extract first word
            first_word = response.split()[0] if response else ""
            clean_first_word = first_word.rstrip('.,!?:;"').strip('"')
            first_words.append(clean_first_word)
            
            print(f"    [{clean_first_word:10s}] {response[:70]}...")
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            responses.append(f"ERROR: {e}")
            first_words.append("ERROR")
    
    # Analysis
    print("\n" + "=" * 80)
    print(f"\n📊 FIRST WORD DISTRIBUTION:")
    
    first_word_counts = Counter(first_words)
    
    for word, count in first_word_counts.most_common(10):
        pct = (count / len(questions)) * 100
        bar = "█" * int(pct / 2)
        print(f"  {word:15s}: {count:2d}x ({pct:5.1f}%) {bar}")
    
    # Categorize first words
    interrogative = ['Why', 'What', 'How', 'When', 'Where', 'Which', 'Who', 'Whose']
    interjections = ['Hmmm...', 'Hmmm', 'Oh', 'Ah', 'Well', 'Hmm', 'Interesting', 'Wait', 'Whoa', 'Awesome']
    reflective = ["I'd", "Honestly", "That's", "You", 'So', 'I think']
    templated = ["I'm", "I"]
    
    interrogative_count = sum(1 for w in first_words if w in interrogative)
    interjection_count = sum(1 for w in first_words if w in interjections or w.startswith('Hmm') or w.startswith('Ah') or w == 'Well' or w == 'well')
    reflective_count = sum(1 for w in first_words if w in reflective or w == "Honestly" or w == "I'd")
    templated_count = sum(1 for w in first_words if w in templated)
    
    print(f"\n📋 FIRST WORD CATEGORIES:")
    print(f"  Interrogative (Why/What/How): {interrogative_count:2d} ({interrogative_count/len(questions):.1%})")
    print(f"  Interjections (Hmm/Well/Oh):  {interjection_count:2d} ({interjection_count/len(questions):.1%})")
    print(f"  Reflective (Honestly/I'd):     {reflective_count:2d} ({reflective_count/len(questions):.1%})")
    print(f"  Templated (I'm/I):             {templated_count:2d} ({templated_count/len(questions):.1%})")
    
    # Content analysis
    black_hole_count = sum(1 for r in responses if "black hole" in r.lower())
    curious_count = sum(1 for r in responses if "curious" in r.lower())
    
    print(f"\n🔍 CONTENT ANALYSIS:")
    print(f"  'black hole': {black_hole_count}/{len(questions)} ({black_hole_count/len(questions):.1%})")
    print(f"  'curious': {curious_count}/{len(questions)} ({curious_count/len(questions):.1%})")
    
    # Response variety
    unique_responses = len(set(responses))
    variety_rate = unique_responses / len(questions)
    
    print(f"  Unique responses: {unique_responses}/{len(questions)} ({variety_rate:.1%})")
    
    # Response types
    questioning = [r for r in responses if '?' in r]
    explanatory = [r for r in responses if '?' not in r]
    
    print(f"\n📝 RESPONSE TYPES:")
    print(f"  Questioning: {len(questioning)} ({len(questioning)/len(questions):.1%})")
    print(f"  Explanatory: {len(explanatory)} ({len(explanatory)/len(questions):.1%})")
    
    # Success summary
    print(f"\n🎯 BLIND TEST RESULTS:")
    
    score = 0
    max_score = 5
    
    if templated_count <= 3:
        print(f"  ✅ Low template lock: {templated_count}x")
        score += 1
    else:
        print(f"  ❌ High template lock: {templated_count}x")
    
    if black_hole_count == 0:
        print(f"  ✅ No 'black hole' repetition")
        score += 1
    else:
        print(f"  ⚠️  'black hole': {black_hole_count}x")
    
    if variety_rate >= 0.85:
        print(f"  ✅ Excellent variety: {variety_rate:.1%}")
        score += 1
    else:
        print(f"  ⚠️  Variety: {variety_rate:.1%}")
    
    if interrogative_count >= len(questions) * 0.3:
        print(f"  ✅ Good interrogative: {interrogative_count/len(questions):.1%}")
        score += 1
    else:
        print(f"  ⚠️  Low interrogative: {interrogative_count/len(questions):.1%}")
    
    if curious_count <= len(questions) * 0.3:
        print(f"  ✅ Low 'curious' repetition: {curious_count/len(questions):.1%}")
        score += 1
    else:
        print(f"  ⚠️  High 'curious': {curious_count/len(questions):.1%}")
    
    print(f"\n📊 OVERALL SCORE: {score}/{max_score}")
    
    return responses, first_words, variety_rate, score

if __name__ == "__main__":
    try:
        responses, first_words, variety_rate, score = test_blind()
        print(f"\n✅ Blind test completed! Score: {score}/5")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

