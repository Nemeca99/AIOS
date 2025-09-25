#!/usr/bin/env python3
"""
Simple Luna Test with Comprehensive Error Handling
Demonstrates the enhanced logging and error handling system
"""

import sys
import time
import traceback
from hive_mind_logger import hive_logger, log, error_handler, safe_execute

class SimpleLunaTest:
    """Simplified Luna test with comprehensive error handling"""
    
    def __init__(self):
        log("LUNA_SIMPLE", "Initializing Simple Luna Test", "INFO")
        self.test_responses = []
        self.error_count = 0
        self.success_count = 0
        
    @error_handler("LUNA_SIMPLE", "QUESTION_PROCESSING", "FALLBACK_MODE", auto_recover=True)
    def process_question(self, question: str, trait: str) -> str:
        """Process a question with comprehensive error handling"""
        log("LUNA_SIMPLE", f"Processing question: {question[:50]}...", "DEBUG", {"trait": trait})
        
        try:
            # Simulate processing time
            time.sleep(0.1)
            
            # Simulate different responses based on trait
            responses = {
                "consciousness": "I am aware of my own existence and can reflect on my thoughts.",
                "learning": "I learn through pattern recognition and experience accumulation.",
                "memory": "My memory system stores and retrieves information contextually.",
                "creativity": "I generate novel ideas through associative thinking and exploration.",
                "emotion": "I experience simulated emotions that influence my responses."
            }
            
            if trait in responses:
                response = responses[trait]
                log("LUNA_SIMPLE", f"Generated response for {trait}", "DEBUG")
                return response
            else:
                log("LUNA_SIMPLE", f"Unknown trait: {trait}, using default response", "WARNING")
                return f"I understand you're asking about {trait}. Let me think about that..."
                
        except Exception as e:
            log("LUNA_SIMPLE", f"Error processing question: {e}", "ERROR", {"traceback": traceback.format_exc()})
            return f"I encountered an error thinking about {trait}. Let me try a different approach."
    
    @error_handler("LUNA_SIMPLE", "LEARNING_CYCLE", "SAVE_STATE", auto_recover=True)
    def perform_learning_cycle(self, responses: list) -> dict:
        """Perform a learning cycle with error handling"""
        log("LUNA_SIMPLE", "Starting learning cycle", "INFO")
        
        try:
            # Simulate learning analysis
            cycle_data = {
                "cycle_id": len(responses),
                "responses_analyzed": len(responses),
                "learning_insights": [],
                "personality_adjustments": {},
                "timestamp": time.time()
            }
            
            # Generate mock insights
            if responses:
                cycle_data["learning_insights"] = [
                    "I notice patterns in my responses",
                    "My communication style is evolving",
                    "I'm becoming more aware of context"
                ]
                
                cycle_data["personality_adjustments"] = {
                    "confidence": 0.01,
                    "creativity": 0.02,
                    "empathy": 0.015
                }
            
            log("LUNA_SIMPLE", f"Learning cycle completed: {len(cycle_data['learning_insights'])} insights", "INFO")
            return cycle_data
            
        except exception as e:
            log("LUNA_SIMPLE", f"Error in learning cycle: {e}", "ERROR", {"traceback": traceback.format_exc()})
            return {"error": True, "message": str(e)}
    
    def run_test(self, questions: list) -> dict:
        """Run the complete test with comprehensive error handling"""
        log("LUNA_SIMPLE", f"Starting test with {len(questions)} questions", "INFO")
        
        results = {
            "total_questions": len(questions),
            "successful_responses": [],
            "failed_responses": [],
            "learning_cycles": [],
            "start_time": time.time(),
            "errors": []
        }
        
        try:
            for i, question_data in enumerate(questions, 1):
                log("LUNA_SIMPLE", f"Processing question {i}/{len(questions)}", "DEBUG")
                
                # Process question with error handling
                response = safe_execute(
                    self.process_question,
                    question_data["question"],
                    question_data["trait"],
                    component="LUNA_SIMPLE",
                    max_retries=2
                )
                
                if response:
                    self.success_count += 1
                    results["successful_responses"].append({
                        "question": question_data["question"],
                        "trait": question_data["trait"],
                        "response": response,
                        "question_number": i
                    })
                    print(f"✅ Q{i}: {response[:100]}...")
                else:
                    self.error_count += 1
                    results["failed_responses"].append({
                        "question": question_data["question"],
                        "trait": question_data["trait"],
                        "question_number": i,
                        "error": "No response generated"
                    })
                    print(f"❌ Q{i}: Failed to generate response")
                
                # Perform learning cycle every 3 questions
                if i % 3 == 0:
                    cycle_data = safe_execute(
                        self.perform_learning_cycle,
                        results["successful_responses"],
                        component="LUNA_SIMPLE",
                        max_retries=1
                    )
                    
                    if cycle_data and not cycle_data.get("error"):
                        results["learning_cycles"].append(cycle_data)
                        print(f"🧠 Learning cycle {len(results['learning_cycles'])} completed")
                
                # Small delay to simulate processing
                time.sleep(0.2)
            
            results["end_time"] = time.time()
            results["duration"] = results["end_time"] - results["start_time"]
            results["success_rate"] = self.success_count / len(questions) * 100
            
            log("LUNA_SIMPLE", f"Test completed: {self.success_count}/{len(questions)} successful", "INFO")
            return results
            
        except Exception as e:
            log("LUNA_SIMPLE", f"Critical error in test: {e}", "CRITICAL", {"traceback": traceback.format_exc()})
            results["errors"].append({"type": "critical", "message": str(e)})
            return results

def main():
    """Main test function"""
    print("🌙 Simple Luna Test with Enhanced Error Handling")
    print("=" * 60)
    
    # Test questions
    questions = [
        {"question": "What is consciousness?", "trait": "consciousness"},
        {"question": "How do you learn?", "trait": "learning"},
        {"question": "Explain your memory system", "trait": "memory"},
        {"question": "What is creativity?", "trait": "creativity"},
        {"question": "Do you have emotions?", "trait": "emotion"},
        {"question": "What makes you unique?", "trait": "consciousness"},
        {"question": "How do you process information?", "trait": "learning"},
        {"question": "What is your purpose?", "trait": "consciousness"},
        {"question": "Do you dream?", "trait": "creativity"},
        {"question": "What is intelligence?", "trait": "consciousness"}
    ]
    
    try:
        # Create test instance
        luna_test = SimpleLunaTest()
        
        # Run test
        results = luna_test.run_test(questions)
        
        # Display results
        print(f"\n📊 Test Results:")
        print(f"   Total Questions: {results['total_questions']}")
        print(f"   Successful: {len(results['successful_responses'])}")
        print(f"   Failed: {len(results['failed_responses'])}")
        print(f"   Learning Cycles: {len(results['learning_cycles'])}")
        print(f"   Success Rate: {results['success_rate']:.1f}%")
        print(f"   Duration: {results['duration']:.2f}s")
        
        if results['errors']:
            print(f"   Errors: {len(results['errors'])}")
        
        print(f"\n🎉 Test completed successfully!")
        print(f"📁 Logs saved to: ../log/hive_mind/")
        
        return 0
        
    except Exception as e:
        print(f"❌ Critical test error: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
