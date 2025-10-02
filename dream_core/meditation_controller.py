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
    
    def _get_meditation_question(self) -> str:
        """Get a meditation question for Luna"""
        questions = [
            "What memories feel most important to me right now, and how do they connect to form a deeper understanding of my experiences?",
            "What aspects of myself am I becoming more aware of, and how is this awareness changing my perspective on who I am?",
            "How do I approach problems, and what strategies have proven most effective in helping me find solutions?",
            "What patterns do I see in my recent experiences, and how do they connect to my understanding of myself?",
            "What am I learning about my own thought processes, and how can I use this knowledge to grow?",
            "How do I handle uncertainty, and what does this reveal about my core values and beliefs?",
            "What relationships and connections feel most meaningful to me, and why?",
            "How do I balance my need for growth with my need for stability and comfort?",
            "What am I most curious about right now, and how can I explore this curiosity?",
            "How do I want to evolve, and what steps can I take to move in that direction?"
        ]
        
        import random
        return random.choice(questions)
    
    def _perform_meditation(self) -> float:
        """Perform a single meditation session"""
        try:
            question = self._get_meditation_question()
            self._log(f"Meditation Question: {question}")
            
            # Get Luna's response
            if self.luna_system:
                response = self.luna_system.generate_response(question)
                if response:
                    self._log(f"Response: {response[:100]}...")
                    
                    # Calculate karma based on response quality
                    karma = self._calculate_karma(response)
                    self._log(f"Meditation completed: {karma:.2f} karma gained")
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
