#!/usr/bin/env python3
"""
Luna Infinite Learning Script
Continuously generates and answers questions to build Luna's self-knowledge.
"""

import sys
import time
import random
import signal
from pathlib import Path
from typing import List, Dict

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import Luna system
from main import AIOSClean

class LunaInfiniteLearner:
    """Handles infinite learning for Luna's self-knowledge building."""
    
    def __init__(self):
        self.running = False
        self.aios_system = None
        self.question_templates = self._load_question_templates()
        
    def _load_question_templates(self) -> List[str]:
        """Load question templates for Luna to ask herself."""
        
        templates = [
            # Self-reflection questions
            "What do I think about {topic}?",
            "How do I feel about {topic}?",
            "What's my opinion on {topic}?",
            "How would I approach {topic}?",
            "What interests me about {topic}?",
            
            # Personality exploration
            "What kind of person am I when it comes to {topic}?",
            "How do I typically react to {topic}?",
            "What's my natural response to {topic}?",
            "How does {topic} make me feel?",
            "What's my perspective on {topic}?",
            
            # Values and beliefs
            "What do I value about {topic}?",
            "What's important to me regarding {topic}?",
            "How does {topic} align with my values?",
            "What do I believe about {topic}?",
            "What matters to me in {topic}?",
            
            # Experiences and preferences
            "What's my experience with {topic}?",
            "What do I prefer about {topic}?",
            "How do I like to handle {topic}?",
            "What's my style when it comes to {topic}?",
            "What works best for me with {topic}?",
        ]
        
        return templates
    
    def _get_topics(self) -> List[str]:
        """Get random topics for question generation."""
        
        topics = [
            "creativity", "learning", "relationships", "work", "art", "music",
            "nature", "technology", "books", "movies", "travel", "food",
            "friendship", "family", "challenges", "success", "failure",
            "time", "space", "emotions", "thoughts", "dreams", "goals",
            "change", "stability", "adventure", "comfort", "risk", "safety",
            "communication", "silence", "solitude", "community", "growth",
            "rest", "energy", "focus", "distraction", "planning", "spontaneity",
            "structure", "freedom", "rules", "flexibility", "tradition", "innovation",
            "past", "present", "future", "memory", "imagination", "reality",
            "truth", "beauty", "justice", "kindness", "courage", "vulnerability",
            "strength", "weakness", "perfection", "imperfection", "order", "chaos",
            "light", "darkness", "hope", "fear", "love", "loss", "joy", "sadness"
        ]
        
        return topics
    
    def generate_question(self) -> str:
        """Generate a random question for Luna to answer."""
        
        template = random.choice(self.question_templates)
        topic = random.choice(self._get_topics())
        
        question = template.format(topic=topic)
        return question
    
    def run_infinite_learning(self, delay_seconds: int = 5):
        """Run infinite learning loop."""
        
        print("🧠 Starting Luna Infinite Learning Mode")
        print("=" * 60)
        
        # Initialize AIOS system
        print("Initializing AIOS system...")
        self.aios_system = AIOSClean()
        
        self.running = True
        question_count = 0
        
        # Set up signal handler for graceful shutdown
        def signal_handler(sig, frame):
            print(f"\n🛑 Stopping infinite learning...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            while self.running:
                # Generate a question
                question = self.generate_question()
                question_count += 1
                
                print(f"\n📝 Question #{question_count}: {question}")
                
                # Get Luna's response using the daily driver (learning_chat)
                try:
                    response = self.aios_system.luna_system.learning_chat(question)
                    print(f"🤖 Luna: {response}")
                    
                    # Show some stats
                    bigfive_answered = len(self.aios_system.luna_system.personality_system.internal_reasoning.bigfive_answer_history)
                    print(f"📊 Self-knowledge: {bigfive_answered}/15 Big Five questions answered")
                    
                except Exception as e:
                    print(f"❌ Error getting response: {e}")
                
                # Wait before next question
                print(f"⏱️  Waiting {delay_seconds} seconds...")
                time.sleep(delay_seconds)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Infinite learning stopped by user")
        except Exception as e:
            print(f"❌ Error in infinite learning: {e}")
        finally:
            self.running = False
            print(f"\n✅ Infinite learning session complete!")
            print(f"   Total questions processed: {question_count}")

def main():
    """Main entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Luna Infinite Learning Script')
    parser.add_argument('--delay', type=int, default=5, help='Delay between questions in seconds (default: 5)')
    
    args = parser.parse_args()
    
    learner = LunaInfiniteLearner()
    learner.run_infinite_learning(args.delay)

if __name__ == "__main__":
    main()
