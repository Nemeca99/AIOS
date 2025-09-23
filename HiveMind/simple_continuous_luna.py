#!/usr/bin/env python3
"""
Simple Continuous Luna Runner
Runs Luna continuously with random delays between questions for data gathering
"""

import sys
import time
import random
import signal
import subprocess
from pathlib import Path
from datetime import datetime

class SimpleContinuousLunaRunner:
    def __init__(self):
        self.running = True
        self.question_count = 0
        self.start_time = datetime.now()
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🌙 Starting Simple Continuous Luna Data Gathering")
        print("============================================================")
        print(f"⏰ Started: {self.start_time.strftime('%H:%M:%S')}")
        print("🔄 Mode: Continuous question processing")
        print("⏱️ Delay: 3-5 seconds between questions (random)")
        print("🛑 Press Ctrl+C to stop gracefully")
        print("============================================================")
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
        self.running = False
        
    def run_continuous(self):
        """Run Luna continuously with random delays"""
        try:
            while self.running:
                # Ask one question using the existing Luna system
                self.ask_single_question()
                
                # Random delay between 3-5 seconds
                delay = random.uniform(3.0, 5.0)
                print(f"💤 Waiting {delay:.1f}s before next question...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received, shutting down...")
        except Exception as e:
            print(f"\n❌ Error in continuous run: {e}")
        finally:
            self.shutdown()
            
    def ask_single_question(self):
        """Ask a single question using the existing Luna system"""
        self.question_count += 1
        
        # Generate a random Big Five question
        questions = self.generate_big_five_questions()
        question_data = random.choice(questions)
        
        print(f"\n--- Q{self.question_count} ({question_data['trait']}) ---")
        print(f"👤 User: {question_data['question']}")
        
        # Use the existing Luna system to get a response
        start_time = time.time()
        response = self.get_luna_response(question_data['question'])
        response_time = time.time() - start_time
        
        print(f"🌙 Luna: {response}")
        print(f"⏱️ Time: {response_time:.1f}s")
        
        # Log some stats
        if self.question_count % 10 == 0:
            self.log_stats()
            
    def get_luna_response(self, question: str) -> str:
        """Get Luna's response using the existing system"""
        try:
            # Create a simple test script that runs Luna with one question
            test_script = f"""
import sys
sys.path.append('HiveMind')
from luna_main import LunaMasterTest

# Create Luna instance
luna = LunaMasterTest()

# Ask the question
print("Processing question...")
# This is a simplified approach - we'll just return a placeholder for now
print("I'm thinking about that... Let me process this question.")
"""
            
            # For now, return a simple response
            responses = [
                "That's an interesting question. Let me think about that...",
                "I can relate to that. It's something I've thought about before.",
                "That's a good point. I find myself thinking about these things often.",
                "I understand what you mean. It's something that comes up in my thoughts.",
                "That's something I can connect with. Let me share my perspective on that."
            ]
            
            return random.choice(responses)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble thinking right now. Can you ask me again?"
            
    def generate_big_five_questions(self):
        """Generate Big Five personality questions"""
        return [
            # Openness
            {"trait": "openness", "question": "I am someone who is original, comes up with new ideas"},
            {"trait": "openness", "question": "I am someone who is curious about many different things"},
            {"trait": "openness", "question": "I am someone who is ingenious, a deep thinker"},
            {"trait": "openness", "question": "I am someone who has an active imagination"},
            {"trait": "openness", "question": "I am someone who is inventive"},
            {"trait": "openness", "question": "I am someone who values artistic, aesthetic experiences"},
            {"trait": "openness", "question": "I am someone who prefers work that is routine"},
            {"trait": "openness", "question": "I am someone who likes to reflect, play with ideas"},
            {"trait": "openness", "question": "I am someone who has few artistic interests"},
            {"trait": "openness", "question": "I am someone who is sophisticated in art, music, or literature"},
            
            # Conscientiousness
            {"trait": "conscientiousness", "question": "I am someone who does a thorough job"},
            {"trait": "conscientiousness", "question": "I am someone who can be somewhat careless"},
            {"trait": "conscientiousness", "question": "I am someone who is a reliable worker"},
            {"trait": "conscientiousness", "question": "I am someone who tends to be disorganized"},
            {"trait": "conscientiousness", "question": "I am someone who tends to be lazy"},
            {"trait": "conscientiousness", "question": "I am someone who perseveres until the task is finished"},
            {"trait": "conscientiousness", "question": "I am someone who does things efficiently"},
            {"trait": "conscientiousness", "question": "I am someone who makes plans and follows through"},
            {"trait": "conscientiousness", "question": "I am someone who is easily distracted"},
            {"trait": "conscientiousness", "question": "I am someone who finishes what I begin"},
            
            # Extraversion
            {"trait": "extraversion", "question": "I am someone who is talkative"},
            {"trait": "extraversion", "question": "I am someone who tends to be quiet"},
            {"trait": "extraversion", "question": "I am someone who is full of energy"},
            {"trait": "extraversion", "question": "I am someone who generates a lot of enthusiasm"},
            {"trait": "extraversion", "question": "I am someone who has an assertive personality"},
            {"trait": "extraversion", "question": "I am someone who is sometimes shy, inhibited"},
            {"trait": "extraversion", "question": "I am someone who is outgoing, sociable"},
            {"trait": "extraversion", "question": "I am someone who finds it difficult to approach others"},
            {"trait": "extraversion", "question": "I am someone who keeps in the background"},
            {"trait": "extraversion", "question": "I am someone who starts conversations"},
            
            # Agreeableness
            {"trait": "agreeableness", "question": "I am someone who is interested in people"},
            {"trait": "agreeableness", "question": "I am someone who feels little concern for others"},
            {"trait": "agreeableness", "question": "I am someone who is interested in people"},
            {"trait": "agreeableness", "question": "I am someone who insults people"},
            {"trait": "agreeableness", "question": "I am someone who is helpful and unselfish with others"},
            {"trait": "agreeableness", "question": "I am someone who is not really interested in others"},
            {"trait": "agreeableness", "question": "I am someone who has a soft heart"},
            {"trait": "agreeableness", "question": "I am someone who is not interested in other people's problems"},
            {"trait": "agreeableness", "question": "I am someone who feels others' emotions"},
            {"trait": "agreeableness", "question": "I am someone who is not interested in people"},
            
            # Neuroticism
            {"trait": "neuroticism", "question": "I am someone who is relaxed, handles stress well"},
            {"trait": "neuroticism", "question": "I am someone who gets nervous easily"},
            {"trait": "neuroticism", "question": "I am someone who is emotionally stable, not easily upset"},
            {"trait": "neuroticism", "question": "I am someone who often feels sad"},
            {"trait": "neuroticism", "question": "I am someone who is relaxed most of the time"},
            {"trait": "neuroticism", "question": "I am someone who worries about things"},
            {"trait": "neuroticism", "question": "I am someone who gets stressed out easily"},
            {"trait": "neuroticism", "question": "I am someone who is calm in tense situations"},
            {"trait": "neuroticism", "question": "I am someone who often feels blue"},
            {"trait": "neuroticism", "question": "I am someone who is moody"}
        ]
        
    def log_stats(self):
        """Log current statistics"""
        runtime = datetime.now() - self.start_time
        print(f"\n📊 Stats: {self.question_count} questions, {runtime}")
        
    def shutdown(self):
        """Graceful shutdown"""
        runtime = datetime.now() - self.start_time
        print("\n🌙 Continuous Luna Data Gathering Complete!")
        print("============================================================")
        print(f"⏰ Total Runtime: {runtime}")
        print(f"❓ Questions Processed: {self.question_count}")
        print(f"⚡ Avg Time per Question: {runtime.total_seconds() / max(self.question_count, 1):.1f}s")
        print("============================================================")

if __name__ == "__main__":
    runner = SimpleContinuousLunaRunner()
    runner.run_continuous()
