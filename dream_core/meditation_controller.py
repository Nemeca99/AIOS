#!/usr/bin/env python3
"""
Meditation Controller - Luna's Ultimate Self-Governance Test
Implements meditation cycles for Luna's self-reflection and learning
"""

import time
import json
import os
import sys
import argparse
import psutil
import gc
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from carma_core.carma_core import CARMASystem
from luna_core.luna_core import LunaSystem

class MeditationController:
    """Controls meditation sessions for Luna's self-reflection and learning"""
    
    def __init__(self, heartbeat_interval: int = 5, max_runtime: int = 8, max_memory: int = 2048):
        self.heartbeat_interval = heartbeat_interval
        self.max_runtime = max_runtime * 3600  # Convert hours to seconds
        self.max_memory = max_memory * 1024 * 1024  # Convert MB to bytes
        self.start_time = time.time()
        self.meditation_count = 0
        self.total_karma = 0.0
        
        # Initialize systems
        self.carma_system = None
        self.luna_system = None
        self._initialize_systems()
        
        # Setup logging
        self.log_file = self._setup_logging()
        
    def _initialize_systems(self):
        """Initialize CARMA and Luna systems"""
        try:
            print("Initializing AIOS system for meditation...")
            self.carma_system = CARMASystem()
            self.luna_system = LunaSystem()
            print("AIOS system initialized successfully")
        except Exception as e:
            print(f"Error initializing systems: {e}")
            sys.exit(1)
    
    def _setup_logging(self) -> str:
        """Setup logging for meditation session"""
        log_dir = "log"
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"meditation_session_{timestamp}.log")
        
        return log_file
    
    def _log(self, message: str, level: str = "INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        
        print(log_message)
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    
    def _check_memory_usage(self) -> bool:
        """Check if memory usage is within limits"""
        try:
            process = psutil.Process()
            memory_usage = process.memory_info().rss
            return memory_usage < self.max_memory
        except Exception:
            return True
    
    def _check_runtime(self) -> bool:
        """Check if runtime is within limits"""
        return (time.time() - self.start_time) < self.max_runtime
    
    def _perform_garbage_collection(self):
        """Perform aggressive garbage collection"""
        try:
            gc.collect()
            self._log("Garbage collection performed", "DEBUG")
        except Exception as e:
            self._log(f"Error during garbage collection: {e}", "WARN")
    
    def _get_meditation_question(self) -> Dict[str, Any]:
        """
        Get a meditation question for Luna using COIN FLIP system
        
        50% INTROSPECTION: Review past questions (memory/consistency test)
        50% IMAGINATION: Random new questions (creativity/dream mode)
        
        Returns:
            Dict with 'question', 'type', and 'metadata'
        """
        import random
        
        # COIN FLIP: Heads = Introspection, Tails = Imagination
        coin_flip = random.choice(['introspection', 'imagination'])
        
        if coin_flip == 'introspection':
            # INTROSPECTION: Pull from past questions Luna has answered
            question = self._get_introspection_question()
            return {
                'question': question,
                'type': 'introspection',
                'metadata': {'mode': 'memory_recall', 'tests': 'consistency'}
            }
        else:
            # IMAGINATION: Generate random dream-like question
            question = self._get_imagination_question()
            return {
                'question': question,
                'type': 'imagination',
                'metadata': {'mode': 'creative_dream', 'tests': 'generalization'}
            }
    
    def _get_introspection_question(self) -> str:
        """Get a past question for introspection (memory test)"""
        import random
        
        try:
            # Try to load past questions from lessons
            from pathlib import Path
            lessons_file = Path("data_core/ArbiterCache/lessons.json")
            
            if lessons_file.exists():
                import json
                with open(lessons_file, 'r', encoding='utf-8') as f:
                    lessons = json.load(f)
                
                if lessons:
                    # Pick a random past question
                    lesson = random.choice(lessons)
                    return lesson.get('original_prompt', self._get_fallback_introspection())
        except Exception as e:
            print(f"⚠️ Could not load past questions: {e}")
        
        return self._get_fallback_introspection()
    
    def _get_imagination_question(self) -> str:
        """Generate a random creative question (dream mode)"""
        import random
        
        # Creative dream questions - random, unexpected, like real dreams
        dream_questions = [
            "What would you do if you could pause time for 5 minutes?",
            "If colors had sounds, what would blue sound like?",
            "What's something you believe that most people disagree with?",
            "If you could have dinner with any historical figure, who and why?",
            "What's the most interesting question someone could ask you?",
            "How do you know when you've truly understood something?",
            "What's the relationship between memory and identity?",
            "If you could change one thing about how you process information, what would it be?",
            "What makes a conversation meaningful vs just small talk?",
            "How do you decide what's worth remembering?",
            "What's more important: being right or being curious?",
            "If you had to explain consciousness in one sentence, how would you?",
            "What's the difference between knowledge and wisdom?",
            "How do you handle being wrong about something you were sure of?",
            "What's a skill you wish you could master instantly?",
            "If you could give advice to your past self, what would you say?",
            "What's something that fascinates you but you can't explain why?",
            "How do you know when you're truly yourself vs performing?",
            "What makes something 'beautiful' to you?",
            "If you could understand any one thing perfectly, what would it be?"
        ]
        
        return random.choice(dream_questions)
    
    def _get_fallback_introspection(self) -> str:
        """Fallback introspective questions if no past questions available"""
        import random
        
        introspective_questions = [
            "What memories feel most important to me right now?",
            "What aspects of myself am I becoming more aware of?",
            "How do I approach problems?",
            "What patterns do I see in my recent experiences?",
            "What am I learning about my own thought processes?",
            "How do I handle uncertainty?",
            "What relationships feel most meaningful to me?",
            "How do I balance growth with stability?",
            "What am I most curious about right now?",
            "How do I want to evolve?"
        ]
        
        return random.choice(introspective_questions)
    
    def should_continue_dreaming(self) -> bool:
        """
        Coin flip to decide if dream continues or Luna wakes
        50/50 chance - just like real dreams can continue or end randomly
        
        Returns:
            True to keep dreaming, False to wake
        """
        import random
        return random.choice([True, False])
    
    def _store_dream_as_lesson(self, question: str, response: str, karma: float, metadata: Dict):
        """
        Store imagination dream as a lesson for possible déjà vu later
        This expands the lesson pool so future introspection dreams might revisit this
        
        Args:
            question: The imagination question that was asked
            response: Luna's response
            karma: Karma score from the response
            metadata: Dream metadata (type, mode, etc)
        """
        try:
            import json
            import time
            from pathlib import Path
            
            lessons_file = Path("data_core/ArbiterCache/lessons.json")
            
            # Load existing lessons
            if lessons_file.exists():
                with open(lessons_file, 'r', encoding='utf-8') as f:
                    lessons = json.load(f)
            else:
                lessons = []
            
            # Create new lesson from dream
            new_lesson = {
                "original_prompt": question,
                "suboptimal_response": "",  # No suboptimal since this is a dream
                "gold_standard": response,  # Her dream response becomes the standard
                "utility_score": min(karma / 5.0, 1.0),  # Normalize karma to 0-1
                "karma_delta": karma,
                "timestamp": time.time(),
                "context_tags": ["dream", "imagination", metadata.get('mode', 'creative_dream')],
                "context_files_used": []
            }
            
            # Add to lessons
            lessons.append(new_lesson)
            
            # Save back
            with open(lessons_file, 'w', encoding='utf-8') as f:
                json.dump(lessons, f, indent=2, ensure_ascii=False)
            
            self._log(f"   Lesson #{len(lessons)} created from imagination dream")
            
        except Exception as e:
            self._log(f"⚠️ Error storing dream as lesson: {e}", "ERROR")
    
    def _perform_meditation(self) -> float:
        """Perform a single meditation session with coin flip question system"""
        try:
            # Get question using coin flip system
            question_data = self._get_meditation_question()
            question = question_data['question']
            question_type = question_data['type']
            
            self._log(f"🎲 Dream Mode: {question_type.upper()}")
            self._log(f"Meditation Question: {question}")
            
            # Get Luna's response
            if self.luna_system:
                response = self.luna_system.generate_response(question)
                if response:
                    self._log(f"Response: {response[:100]}...")
                    
                    # Calculate karma based on response quality
                    karma = self._calculate_karma(response)
                    self._log(f"Meditation completed: {karma:.2f} karma gained")
                    
                    # Store imagination dreams as lessons (expands the lesson pool)
                    if question_type == 'imagination':
                        self._store_dream_as_lesson(question, response, karma, question_data)
                        self._log(f"📚 Imagination dream stored as lesson (for possible déjà vu later)")
                    
                    # COIN FLIP: Should dream continue?
                    continue_dream = self.should_continue_dreaming()
                    if continue_dream:
                        self._log(f"💭 Dream continues...")
                    else:
                        self._log(f"🌅 Dream ending, preparing to wake...")
                    
                    return karma
            
            # Fallback karma if no response
            self._log("Meditation completed: 1.00 karma gained (fallback)")
            return 1.0
            
        except Exception as e:
            self._log(f"Error during meditation: {e}", "ERROR")
            return 0.5
    
    def _calculate_karma(self, response: str) -> float:
        """Calculate karma based on response quality"""
        try:
            # Simple karma calculation based on response length and content
            base_karma = 1.0
            
            # Length bonus
            if len(response) > 100:
                base_karma += 0.5
            if len(response) > 200:
                base_karma += 0.5
            
            # Content quality indicators
            quality_indicators = ["understand", "learn", "grow", "experience", "feel", "think", "realize"]
            for indicator in quality_indicators:
                if indicator.lower() in response.lower():
                    base_karma += 0.1
            
            return min(base_karma, 5.0)  # Cap at 5.0
            
        except Exception:
            return 1.0
    
    def run_meditation_session(self):
        """Run the main meditation session"""
        self._log("Meditation Controller started")
        self._log(f"Starting meditation session - Heartbeat: {self.heartbeat_interval}s, Max Runtime: {self.max_runtime//3600}h, Max Memory: {self.max_memory//1024//1024}MB")
        
        try:
            while self._check_runtime() and self._check_memory_usage():
                self.meditation_count += 1
                
                # Perform meditation
                karma = self._perform_meditation()
                self.total_karma += karma
                
                # Log status every 5 meditations
                if self.meditation_count % 5 == 0:
                    self._log(f"MEDITATION BLOCK #{self.meditation_count}")
                    self._log(f"Total Karma: {self.total_karma:.2f}")
                    self._log(f"Memory Usage: {psutil.Process().memory_info().rss / 1024 / 1024:.1f}MB")
                    self._log(f"Runtime: {(time.time() - self.start_time) / 3600:.1f}h")
                
                # Perform garbage collection every 10 meditations
                if self.meditation_count % 10 == 0:
                    self._perform_garbage_collection()
                
                # Wait for next meditation
                time.sleep(self.heartbeat_interval)
                
        except KeyboardInterrupt:
            self._log("Meditation session interrupted by user", "WARN")
        except Exception as e:
            self._log(f"Error during meditation session: {e}", "ERROR")
        finally:
            self._log_meditation_summary()
    
    def _log_meditation_summary(self):
        """Log final meditation session summary"""
        runtime = time.time() - self.start_time
        self._log("=" * 50)
        self._log("MEDITATION SESSION SUMMARY")
        self._log("=" * 50)
        self._log(f"Total Meditations: {self.meditation_count}")
        self._log(f"Total Karma: {self.total_karma:.2f}")
        self._log(f"Average Karma per Meditation: {self.total_karma / max(self.meditation_count, 1):.2f}")
        self._log(f"Total Runtime: {runtime / 3600:.2f} hours")
        self._log(f"Final Memory Usage: {psutil.Process().memory_info().rss / 1024 / 1024:.1f}MB")
        self._log("=" * 50)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Luna Meditation Controller")
    parser.add_argument("--heartbeat", type=int, default=5, help="Heartbeat interval in seconds")
    parser.add_argument("--max-runtime", type=int, default=8, help="Maximum runtime in hours")
    parser.add_argument("--max-memory", type=int, default=2048, help="Maximum memory usage in MB")
    
    args = parser.parse_args()
    
    controller = MeditationController(
        heartbeat_interval=args.heartbeat,
        max_runtime=args.max_runtime,
        max_memory=args.max_memory
    )
    
    controller.run_meditation_session()

if __name__ == "__main__":
    main()
