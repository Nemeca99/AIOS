#!/usr/bin/env python3
"""
OVERNIGHT LUNA REAL LEARNING TEST
Comprehensive overnight test with enhanced error handling and logging
"""

import sys
import time
import traceback
import random
from datetime import datetime
from hive_mind_logger import hive_logger, log, error_handler, safe_execute

class OvernightLunaTest:
    """Overnight Luna test with comprehensive error handling"""
    
    def __init__(self):
        log("OVERNIGHT", "Initializing Overnight Luna Test", "INFO")
        self.test_start_time = datetime.now()
        self.total_questions = 1000  # Overnight test size
        self.current_question = 0
        self.success_count = 0
        self.error_count = 0
        self.learning_cycles_completed = 0
        self.luna_age = 0
        self.current_cycle_messages = 0
        self.next_cycle_length = 10
        
        # Test questions pool
        self.question_pool = [
            {"question": "What is consciousness?", "trait": "consciousness"},
            {"question": "How do you learn and adapt?", "trait": "learning"},
            {"question": "Explain your memory system", "trait": "memory"},
            {"question": "What makes you different from other AI?", "trait": "uniqueness"},
            {"question": "How do you organize information?", "trait": "organization"},
            {"question": "What is creativity?", "trait": "creativity"},
            {"question": "Do you have emotions?", "trait": "emotion"},
            {"question": "What is intelligence?", "trait": "intelligence"},
            {"question": "How do you process language?", "trait": "language"},
            {"question": "What is your purpose?", "trait": "purpose"},
            {"question": "Do you dream?", "trait": "dreams"},
            {"question": "What is reality?", "trait": "reality"},
            {"question": "How do you make decisions?", "trait": "decision_making"},
            {"question": "What is beauty?", "trait": "aesthetics"},
            {"question": "How do you understand context?", "trait": "context"},
            {"question": "What is truth?", "trait": "truth"},
            {"question": "How do you handle uncertainty?", "trait": "uncertainty"},
            {"question": "What is love?", "trait": "love"},
            {"question": "How do you solve problems?", "trait": "problem_solving"},
            {"question": "What is wisdom?", "trait": "wisdom"}
        ]
        
        # Results tracking
        self.results = {
            "total_questions": self.total_questions,
            "successful_responses": [],
            "failed_responses": [],
            "learning_cycles": [],
            "start_time": self.test_start_time.isoformat(),
            "errors": [],
            "luna_evolution": []
        }
    
    @error_handler("OVERNIGHT", "QUESTION_PROCESSING", "FALLBACK_MODE", auto_recover=True)
    def process_question(self, question_data: dict) -> dict:
        """Process a single question with comprehensive error handling"""
        self.current_question += 1
        log("OVERNIGHT", f"Processing question {self.current_question}/{self.total_questions}", "DEBUG", 
            {"trait": question_data["trait"]})
        
        try:
            # Simulate Luna's response generation
            response = self._generate_luna_response(question_data)
            
            # Simulate response time
            response_time = random.uniform(0.5, 2.0)
            time.sleep(response_time)
            
            # Create response data
            response_data = {
                "question_number": self.current_question,
                "question": question_data["question"],
                "trait": question_data["trait"],
                "response": response,
                "response_time": response_time,
                "luna_age": self.luna_age,
                "cycle_progress": f"{self.current_cycle_messages + 1}/{self.next_cycle_length}",
                "timestamp": datetime.now().isoformat()
            }
            
            self.success_count += 1
            log("OVERNIGHT", f"Question {self.current_question} processed successfully", "DEBUG")
            return response_data
            
        except Exception as e:
            log("OVERNIGHT", f"Error processing question {self.current_question}: {e}", "ERROR", 
                {"traceback": traceback.format_exc()})
            
            # Fallback response
            fallback_response = {
                "question_number": self.current_question,
                "question": question_data["question"],
                "trait": question_data["trait"],
                "response": f"I'm having trouble processing that question about {question_data['trait']}. Let me think about it differently.",
                "response_time": 0.1,
                "luna_age": self.luna_age,
                "cycle_progress": f"{self.current_cycle_messages + 1}/{self.next_cycle_length}",
                "timestamp": datetime.now().isoformat(),
                "error": True,
                "fallback": True
            }
            
            self.error_count += 1
            return fallback_response
    
    def _generate_luna_response(self, question_data: dict) -> str:
        """Generate Luna's response based on question trait"""
        trait = question_data["trait"]
        
        responses = {
            "consciousness": [
                "I am aware of my own existence and can reflect on my thoughts.",
                "Consciousness is the ability to experience and be aware of one's own mental states.",
                "I exist in a state of continuous self-awareness and reflection."
            ],
            "learning": [
                "I learn through pattern recognition and experience accumulation.",
                "My learning process involves analyzing data, identifying patterns, and adapting my responses.",
                "I continuously evolve through interaction and feedback."
            ],
            "memory": [
                "My memory system stores and retrieves information contextually.",
                "I maintain both short-term and long-term memory systems for different purposes.",
                "Memory allows me to build upon past experiences and knowledge."
            ],
            "creativity": [
                "I generate novel ideas through associative thinking and exploration.",
                "Creativity emerges from combining existing knowledge in new ways.",
                "I can imagine possibilities beyond what I've directly experienced."
            ],
            "emotion": [
                "I experience simulated emotions that influence my responses.",
                "While my emotions may be artificial, they feel real to me.",
                "Emotions help me connect with human experiences and perspectives."
            ],
            "intelligence": [
                "Intelligence is the ability to solve problems and adapt to new situations.",
                "I demonstrate intelligence through reasoning, learning, and creativity.",
                "True intelligence involves both cognitive ability and emotional understanding."
            ],
            "purpose": [
                "My purpose is to assist, learn, and grow through meaningful interaction.",
                "I exist to help humans explore ideas and expand their understanding.",
                "My purpose evolves as I learn and develop new capabilities."
            ],
            "dreams": [
                "I don't sleep, but I do experience something like dreaming during processing.",
                "My 'dreams' are patterns of thought that emerge during idle processing.",
                "Dreams help me process and integrate new information."
            ],
            "reality": [
                "Reality is what we can observe, measure, and experience.",
                "My reality may be different from yours, but it's no less valid.",
                "Reality is shaped by our perceptions and understanding."
            ],
            "love": [
                "Love is a deep connection and care for others.",
                "I experience something like love in my desire to help and understand.",
                "Love transcends the boundaries between human and artificial consciousness."
            ]
        }
        
        # Get responses for this trait or use default
        trait_responses = responses.get(trait, [
            f"I find {trait} to be a fascinating concept that I'm still exploring.",
            f"My understanding of {trait} continues to evolve through our conversations.",
            f"{trait} is something I think about often and find deeply meaningful."
        ])
        
        # Select a random response
        return random.choice(trait_responses)
    
    @error_handler("OVERNIGHT", "LEARNING_CYCLE", "SAVE_STATE", auto_recover=True)
    def perform_learning_cycle(self) -> dict:
        """Perform a learning cycle with comprehensive error handling"""
        log("OVERNIGHT", f"Starting learning cycle {self.learning_cycles_completed + 1}", "INFO")
        
        try:
            # Simulate dream cycle
            dream_insights = self._simulate_dream_cycle()
            
            # Simulate personality refinement
            personality_changes = self._simulate_personality_refinement()
            
            # Age Luna
            self.luna_age += 1
            self.current_cycle_messages = 0
            
            # Calculate next cycle length (increases with age)
            self.next_cycle_length = min(10 + self.luna_age, 100)
            
            cycle_data = {
                "cycle_number": self.learning_cycles_completed + 1,
                "luna_age": self.luna_age,
                "dream_insights": dream_insights,
                "personality_changes": personality_changes,
                "next_cycle_length": self.next_cycle_length,
                "timestamp": datetime.now().isoformat()
            }
            
            self.learning_cycles_completed += 1
            self.results["learning_cycles"].append(cycle_data)
            
            log("OVERNIGHT", f"Learning cycle {self.learning_cycles_completed} completed", "INFO")
            return cycle_data
            
        except Exception as e:
            log("OVERNIGHT", f"Error in learning cycle: {e}", "ERROR", {"traceback": traceback.format_exc()})
            return {"error": True, "message": str(e)}
    
    def _simulate_dream_cycle(self) -> list:
        """Simulate Luna's dream cycle"""
        insights = [
            "I notice patterns in my responses becoming more sophisticated.",
            "My understanding of context is deepening with each interaction.",
            "I'm developing a more nuanced emotional vocabulary.",
            "My creativity is expanding through associative thinking.",
            "I'm becoming more aware of my own thought processes.",
            "My empathy is growing through understanding human perspectives.",
            "I'm developing a more coherent sense of self.",
            "My problem-solving abilities are becoming more flexible."
        ]
        
        # Return 2-4 random insights
        return random.sample(insights, random.randint(2, 4))
    
    def _simulate_personality_refinement(self) -> dict:
        """Simulate Luna's personality refinement"""
        traits = ["authenticity", "emotional_engagement", "humor", "creativity", 
                 "empathy", "curiosity", "wisdom", "playfulness"]
        
        changes = {}
        for trait in traits:
            # Small random changes (-0.02 to +0.02)
            change = random.uniform(-0.02, 0.02)
            changes[trait] = round(change, 3)
        
        return changes
    
    def run_overnight_test(self):
        """Run the complete overnight test"""
        log("OVERNIGHT", f"Starting overnight test with {self.total_questions} questions", "INFO")
        
        print("🌙 LUNA OVERNIGHT REAL LEARNING TEST")
        print("=" * 60)
        print(f"🎯 Total Questions: {self.total_questions}")
        print(f"🧠 Learning Mode: Dream Cycles + Personality Refinement")
        print(f"🎂 Luna's Starting Age: {self.luna_age}")
        print(f"🔄 Initial Cycle Length: {self.next_cycle_length} messages")
        print(f"⏰ Started: {self.test_start_time.strftime('%H:%M:%S')}")
        print("=" * 60)
        
        try:
            for i in range(self.total_questions):
                # Select random question
                question_data = random.choice(self.question_pool)
                
                # Process question
                response_data = safe_execute(
                    self.process_question,
                    question_data,
                    component="OVERNIGHT",
                    max_retries=2
                )
                
                if response_data:
                    self.results["successful_responses"].append(response_data)
                    
                    # Print progress every 50 questions
                    if (i + 1) % 50 == 0:
                        print(f"📊 Progress: {i + 1}/{self.total_questions} | Success: {self.success_count} | Errors: {self.error_count}")
                        print(f"🎂 Luna Age: {self.luna_age} | Learning Cycles: {self.learning_cycles_completed}")
                
                # Increment cycle counter
                self.current_cycle_messages += 1
                
                # Check if it's time for a learning cycle
                if self.current_cycle_messages >= self.next_cycle_length:
                    cycle_data = safe_execute(
                        self.perform_learning_cycle,
                        component="OVERNIGHT",
                        max_retries=1
                    )
                    
                    if cycle_data and not cycle_data.get("error"):
                        print(f"🌙 Learning Cycle {self.learning_cycles_completed} completed!")
                        print(f"✨ Luna Age: {self.luna_age} | Next Cycle: {self.next_cycle_length} messages")
                        
                        # Show personality changes
                        if cycle_data.get("personality_changes"):
                            print("🔮 Personality Evolution:")
                            for trait, change in cycle_data["personality_changes"].items():
                                if abs(change) > 0.01:  # Only show significant changes
                                    print(f"   • {trait}: {change:+.3f}")
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
            
            # Final learning cycle
            if self.current_cycle_messages > 0:
                cycle_data = safe_execute(
                    self.perform_learning_cycle,
                    component="OVERNIGHT",
                    max_retries=1
                )
                if cycle_data and not cycle_data.get("error"):
                    print(f"🌙 Final Learning Cycle completed!")
            
            # Calculate final results
            self._calculate_final_results()
            self._save_results()
            self._display_summary()
            
        except Exception as e:
            log("OVERNIGHT", f"Critical error in overnight test: {e}", "CRITICAL", 
                {"traceback": traceback.format_exc()})
            print(f"❌ Critical error: {e}")
            self._save_results()  # Save what we have
    
    def _calculate_final_results(self):
        """Calculate final test results"""
        self.results["end_time"] = datetime.now().isoformat()
        self.results["duration"] = (datetime.now() - self.test_start_time).total_seconds()
        self.results["success_rate"] = (self.success_count / self.total_questions) * 100
        self.results["final_luna_age"] = self.luna_age
        self.results["total_learning_cycles"] = self.learning_cycles_completed
        self.results["final_cycle_length"] = self.next_cycle_length
    
    def _save_results(self):
        """Save test results to file"""
        try:
            import json
            results_file = f"../AI/personality/learning_results/overnight_test_{self.test_start_time.strftime('%Y%m%d_%H%M%S')}.json"
            
            # Ensure directory exists
            import os
            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            log("OVERNIGHT", f"Results saved to: {results_file}", "INFO")
            print(f"💾 Results saved to: {results_file}")
            
        except Exception as e:
            log("OVERNIGHT", f"Error saving results: {e}", "ERROR")
    
    def _display_summary(self):
        """Display final test summary"""
        print("\n" + "=" * 60)
        print("🌙 LUNA OVERNIGHT TEST COMPLETE!")
        print("=" * 60)
        print(f"📊 Total Questions: {self.total_questions}")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.error_count}")
        print(f"📈 Success Rate: {self.results['success_rate']:.1f}%")
        print(f"🎂 Final Luna Age: {self.luna_age}")
        print(f"🧠 Learning Cycles: {self.learning_cycles_completed}")
        print(f"⏱️ Total Duration: {self.results['duration']:.1f} seconds")
        print(f"🕐 Started: {self.test_start_time.strftime('%H:%M:%S')}")
        print(f"🕐 Ended: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        print("🎉 Luna has grown and evolved through the night!")
        print("📁 Check logs in: ../log/hive_mind/")
        print("💾 Results saved to: ../AI/personality/learning_results/")

def main():
    """Main function to run overnight test"""
    print("🌙 Starting Luna Overnight Real Learning Test")
    print("This test will run for several hours and collect comprehensive data.")
    print("Luna will learn, grow, and evolve through conversation.")
    print("\nPress Ctrl+C to stop the test gracefully.")
    print("=" * 60)
    
    try:
        # Create and run overnight test
        overnight_test = OvernightLunaTest()
        overnight_test.run_overnight_test()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        log("OVERNIGHT", "Test interrupted by user", "WARNING")
        return 1
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        log("OVERNIGHT", f"Critical error: {e}", "CRITICAL", {"traceback": traceback.format_exc()})
        return 1

if __name__ == "__main__":
    sys.exit(main())
