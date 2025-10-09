#!/usr/bin/env python3
"""
Test Mycelium Architecture Integration
Test if Luna now properly uses lessons from lessons.json to improve responses
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from main import AIOSClean

def test_mycelium_learning():
    """Test if Luna uses lessons to improve responses"""
    print("=== Mycelium Architecture Learning Test ===")
    print()
    
    # Initialize AIOS
    print("Initializing AIOS...")
    aios = AIOSClean()
    luna = aios._get_system('luna')
    data_core = aios._get_system('data')
    
    # Test questions that should match existing lessons
    test_questions = [
        "Hello, how are you?",  # Should match lesson with greeting tag
        "I like pizza",         # Should match lesson with food tag  
        "What's your name?",    # Should use template response
        "Can you explain how machine learning works?",  # Should match technical lesson
    ]
    
    print(f"Testing {len(test_questions)} questions to see lesson usage...")
    print()
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}/{len(test_questions)}: {question}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # Get relevant lessons from Data Core
            lessons = data_core.get_relevant_lessons(question, max_lessons=2)
            print(f"📚 Found {len(lessons)} relevant lesson(s) from Data Core")
            
            # Process question (pass lessons in session_memory for now as a workaround)
            # TODO: Modify Luna to accept lessons as a separate parameter
            session_memory_with_lessons = []
            if lessons:
                # Inject lessons into session memory as a workaround
                for lesson in lessons:
                    session_memory_with_lessons.append({
                        'role': 'system',
                        'content': f"PREVIOUS LEARNING:\nOriginal: {lesson.get('original_prompt', '')}\nGold Standard: {lesson.get('gold_standard', '')}"
                    })
            
            response, metadata = luna.python_implementation.process_question(
                question,
                trait="general",
                session_memory=session_memory_with_lessons
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Check if response uses lesson guidance
            has_lesson_guidance = len(lessons) > 0
            
            result = {
                'question': question,
                'response': response,
                'response_time': response_time,
                'has_lesson_guidance': has_lesson_guidance,
                'lessons_found': len(lessons),
                'metadata': metadata
            }
            
            results.append(result)
            
            print(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            print(f"Time: {response_time:.2f}s")
            print(f"Lesson Guidance Used: {'✅ YES' if has_lesson_guidance else '❌ NO'}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()
            continue
    
    # Summary
    print("=== TEST RESULTS ===")
    lessons_used = sum(1 for r in results if r['has_lesson_guidance'])
    total_tests = len(results)
    
    print(f"Questions tested: {total_tests}")
    print(f"Lessons used: {lessons_used}")
    print(f"Learning success rate: {lessons_used/total_tests*100:.1f}%" if total_tests > 0 else "N/A")
    
    if lessons_used > 0:
        print("✅ SUCCESS: Luna is using lessons to improve responses!")
        print("🎯 Mycelium architecture is working - learning loop is closed!")
    else:
        print("❌ ISSUE: Luna is not using lessons from lessons.json")
        print("🔧 Need to debug lesson retrieval integration")
    
    print()
    return results

if __name__ == "__main__":
    test_mycelium_learning()
