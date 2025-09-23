#!/usr/bin/env python3
"""
Continuous Real Luna Runner
Runs the ACTUAL Luna system with real LLM calls in a loop
"""

import subprocess
import time
import random
import signal
import sys
from datetime import datetime

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class ContinuousRealLunaRunner:
    def __init__(self):
        self.running = True
        self.question_count = 0
        self.start_time = datetime.now()
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🌙 Starting REAL Continuous Luna Data Gathering")
        print("============================================================")
        print(f"⏰ Started: {self.start_time.strftime('%H:%M:%S')}")
        print("🔄 Mode: Continuous question processing with REAL LLM")
        print("⏱️ Delay: 3-5 seconds between questions (random)")
        print("🛑 Press Ctrl+C to stop gracefully")
        print("============================================================")
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        if self.running:  # Only print once
            print(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
        self.running = False
        
    def run_continuous(self):
        """Run Luna continuously with random delays"""
        try:
            while self.running:
                # Run Luna with 1 question
                self.run_single_luna_question()
                
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
            
    def run_single_luna_question(self):
        """Run Luna with a single question"""
        self.question_count += 1
        
        print(f"\n🔄 Running Luna Question #{self.question_count}")
        print("=" * 60)
        
        try:
            # Just run it directly and let it output to console
            print("🚀 Starting Luna...")
            result = subprocess.run([
                sys.executable, "-u", "HiveMind/luna_main.py", 
                "--mode", "real_learning", "--questions", "1"
            ], timeout=120)
            
            if result.returncode == 0:
                print("✅ Luna completed successfully")
            else:
                print(f"❌ Luna failed with code {result.returncode}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Luna timed out, continuing...")
        except Exception as e:
            print(f"❌ Error: {e}")
            
        # Log stats every 10 questions
        if self.question_count % 10 == 0:
            self.log_stats()
            
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
    runner = ContinuousRealLunaRunner()
    runner.run_continuous()
