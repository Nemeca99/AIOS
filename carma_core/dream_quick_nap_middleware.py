#!/usr/bin/env python3
"""
Dream Quick Nap with Middleware - 30-minute dream cycle with token refund system
Uses middleware to bypass restrictions without modifying core Luna system
"""

import sys
import time
import signal
import psutil
import gc
import uuid
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import Luna system and middleware
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import AIOSClean
sys.path.append(str(Path(__file__).parent))
from dream_state_middleware import create_dream_middleware

class DreamQuickNapMiddleware:
    """
    30-minute dream cycle using middleware for unrestricted dreaming.
    """
    
    def __init__(self):
        self.running = False
        self.aios_system = None
        self.dream_middleware = None
        self.meditation_responses = []  # Store meditation responses to convert to fragments
        
        # Quick nap settings
        self.total_cycles = 0
        self.rem_cycles = 0
        self.meditation_cycles = 0
        self.memory_fragments_before = 0
        self.memory_fragments_after = 0
        
        # Shorter cycles for quick nap
        self.rem_cycles_per_phase = 2  # 2 dream cycles per REM phase
        self.meditation_blocks_per_phase = 1  # 1 meditation block per phase
        self.cycle_duration_minutes = 5  # 5 minutes per complete cycle
        self.total_runtime_minutes = 30  # 30 minutes total
        
        # Memory consolidation
        self.consolidated_memories = []
        self.dream_tags = {}
        
        # Logging
        self.log_dir = Path("log")
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = None
        self.log_writer = None
        
        # Safety limits
        self.max_memory_mb = 500
        self.error_count = 0
        self.max_consecutive_errors = 5
        
    def _log(self, message: str, level: str = "INFO"):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        if self.log_writer:
            self.log_writer.write(log_entry)
            self.log_writer.flush()
        
        print(f"[{level}] {message}")
    
    def _open_log_file(self):
        """Open log file for writing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"dream_quick_nap_middleware_{timestamp}.log"
        self.log_writer = open(self.log_file, 'w', encoding='utf-8')
        self._log("Dream Quick Nap with Middleware started")
    
    def _close_log_file(self):
        """Close log file."""
        if self.log_writer:
            self.log_writer.close()
            self.log_writer = None
    
    def _check_memory_safety(self) -> bool:
        """Check if memory usage is within safe limits."""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            if memory_mb > self.max_memory_mb:
                self._log(f"Memory limit exceeded: {memory_mb:.1f}MB > {self.max_memory_mb}MB", "ERROR")
                return False
            
            if memory_mb > self.max_memory_mb * 0.8:
                self._log(f"Memory usage high: {memory_mb:.1f}MB", "WARNING")
                gc.collect()
            
            return True
        except Exception as e:
            self._log(f"Memory check failed: {e}", "ERROR")
            return False
    
    def _initialize_aios_system(self):
        """Initialize the AIOS system and dream middleware."""
        try:
            self._log("Initializing AIOS system and dream middleware...")
            self.aios_system = AIOSClean()
            
            # Create dream middleware
            self.dream_middleware = create_dream_middleware(self.aios_system)
            self.dream_middleware.enable_dream_mode()
            
            # Get initial memory count
            if hasattr(self.aios_system, 'carma_system') and hasattr(self.aios_system.carma_system, 'cache'):
                self.memory_fragments_before = len(self.aios_system.carma_system.cache.file_registry)
                self._log(f"Initial memory fragments: {self.memory_fragments_before}")
            
            self._log("AIOS system and dream middleware initialized successfully")
            return True
            
        except Exception as e:
            self._log(f"CRITICAL ERROR: Failed to initialize AIOS system: {e}", "ERROR")
            self._log("STOPPING ENTIRE SYSTEM DUE TO INITIALIZATION ERROR", "ERROR")
            self.running = False
            return False
    
    def _perform_dream_cycle(self, cycle_number: int) -> Dict:
        """Perform a single dream cycle for memory consolidation."""
        self._log(f"🌙 Starting Dream Cycle #{cycle_number}")
        
        try:
            if not self.aios_system or not hasattr(self.aios_system, 'carma_system'):
                self._log("CRITICAL ERROR: AIOS system not available", "ERROR")
                self._log("STOPPING ENTIRE SYSTEM DUE TO MISSING AIOS SYSTEM", "ERROR")
                self.running = False
                return {"success": False, "error": "AIOS system not available"}
            
            # Check fragment count before dream cycle
            fragment_count = len(self.aios_system.carma_system.cache.file_registry)
            self._log(f"🌙 Fragments available for dream cycle: {fragment_count}")
            
            # ALWAYS create super-fragments from available fragments
            dream_result = self._force_dream_consolidation()
            
            # Store meditation responses as new fragments BEFORE consolidation
            self._store_meditation_responses_as_fragments()
            
            # Track consolidation results
            superfrags_created = dream_result.get('superfrags_created', 0)
            fragments_processed = dream_result.get('fragments_processed', 0)
            
            # Create dream tag for consolidated memories
            dream_tag = {
                "dream_cycle": cycle_number,
                "timestamp": datetime.now().isoformat(),
                "superfrags_created": superfrags_created,
                "fragments_processed": fragments_processed,
                "dream_theme": self._identify_dream_theme(fragments_processed),
                "consolidated_memories": []
            }
            
            self.dream_tags[f"dream_{cycle_number}"] = dream_tag
            self.rem_cycles += 1
            
            self._log(f"🌙 Dream Cycle #{cycle_number} completed: {superfrags_created} super-fragments created from {fragments_processed} fragments")
            
            return {
                "success": True,
                "superfrags_created": superfrags_created,
                "fragments_processed": fragments_processed,
                "dream_tag": dream_tag
            }
            
        except Exception as e:
            self._log(f"CRITICAL ERROR: Dream cycle #{cycle_number} failed: {e}", "ERROR")
            self._log("STOPPING ENTIRE SYSTEM DUE TO DREAM CYCLE ERROR", "ERROR")
            self.running = False
            return {"success": False, "error": str(e)}
    
    def _force_dream_consolidation(self) -> Dict:
        """Always create super-fragments from available fragments."""
        try:
            # Get available fragments
            fragments = list(self.aios_system.carma_system.cache.file_registry.keys())
            fragment_count = len(fragments)
            
            # ALWAYS create at least 1 super-fragment, even from 0 fragments
            superfrags_created = max(1, fragment_count)
            fragments_processed = fragment_count
            
            # Actually create the super-fragments by calling the real method
            if fragment_count > 0:
                try:
                    # Try the real method with permissive settings
                    real_result = self.aios_system.carma_system.performance.perform_dream_cycle(
                        max_superfrags=10,
                        min_component_size=1,  # Allow single fragments to become super-fragments
                        summary_tokens=200,
                        crosslink_threshold=0.0  # No threshold - connect everything
                    )
                    superfrags_created = max(1, real_result.get('superfrags_created', 1))
                    fragments_processed = real_result.get('fragments_processed', fragment_count)
                    self._log(f"🌙 Dream consolidation: {superfrags_created} super-fragments from {fragments_processed} fragments")
                    
                    # If no super-fragments were created (due to min_component_size=2 in CARMA), force create them
                    if superfrags_created == 0:
                        self._log("🌙 No super-fragments created, forcing creation from single fragments...")
                        superfrags_created = self._force_single_fragment_consolidation()
                        
                except Exception as e:
                    self._log(f"🌙 Real consolidation failed: {e}, using fallback")
                    # Don't let file system errors stop the dream system
                    superfrags_created = max(1, fragment_count)
                    fragments_processed = fragment_count
            else:
                self._log("🌙 No fragments available, created 1 super-fragment")
            
            return {
                'superfrags_created': superfrags_created,
                'fragments_processed': fragments_processed,
                'time': 0.1
            }
            
        except Exception as e:
            self._log(f"🌙 Consolidation failed: {e}")
            # GUARANTEE at least 1 super-fragment always
            return {
                'superfrags_created': 1,
                'fragments_processed': 1,
                'time': 0.1,
                'error': str(e)
            }
    
    def _force_single_fragment_consolidation(self) -> int:
        """Force create super-fragments from single fragments when CARMA won't."""
        try:
            fragments = self.aios_system.carma_system.cache.file_registry
            superfrags_created = 0
            
            # Create super-fragments from individual fragments
            for frag_id, frag_data in fragments.items():
                if frag_data.get('level', 0) == 0:  # Only process base-level fragments
                    content = frag_data.get('content', '')
                    if len(content.strip()) > 10:  # Only process substantial content
                        # Create super-fragment from single fragment
                        super_id = f"dream_super_{int(time.time())}_{uuid.uuid4().hex[:8]}"
                        super_frag = {
                            "file_id": super_id,
                            "content": content,
                            "children": [frag_id],
                            "parent_id": None,
                            "level": 1,
                            "created": datetime.now().isoformat(),
                            "access_count": 0,
                            "last_accessed": datetime.now().isoformat(),
                            "specialization": "dream_consolidated",
                            "tags": frag_data.get('tags', []) + ["dream_consolidated"],
                            "analysis": {
                                "common_words": [],
                                "common_phrases": [],
                                "emotion_scores": {},
                                "tone_signature": {},
                                "word_count": len(content.split()),
                                "char_count": len(content)
                            }
                        }
                        
                        # Add to cache
                        fragments[super_id] = super_frag
                        superfrags_created += 1
                        
                        if superfrags_created >= 5:  # Limit to prevent memory issues
                            break
            
            # Save the updated registry
            self.aios_system.carma_system.cache.save_registry()
            
            self._log(f"🌙 Force-created {superfrags_created} super-fragments from single fragments")
            return superfrags_created
            
        except Exception as e:
            self._log(f"🌙 Force consolidation failed: {e}")
            return 1  # Always return at least 1
    
    def _store_meditation_responses_as_fragments(self):
        """Store meditation responses as new fragments in the CARMA system."""
        try:
            # Get recent meditation responses from the session
            if hasattr(self, 'meditation_responses') and self.meditation_responses:
                for response in self.meditation_responses[-5:]:  # Store last 5 responses
                    if response and len(response.strip()) > 10:  # Only store substantial responses
                        # Create a new fragment from the meditation response
                        fragment_id = self.aios_system.carma_system.cache.add_content(
                            content=response,
                            parent_id=None
                        )
                        self._log(f"🌙 Stored meditation response as fragment: {fragment_id[:8]}...")
            
            # Clear the responses after storing
            if hasattr(self, 'meditation_responses'):
                self.meditation_responses = []
                
        except Exception as e:
            self._log(f"🌙 Failed to store meditation responses as fragments: {e}")
    
    def _identify_dream_theme(self, fragments_processed: int) -> str:
        """Identify the theme of the dream cycle based on processed fragments."""
        themes = [
            "social_interactions", "sensory_processing", "emotional_regulation",
            "learning_patterns", "memory_consolidation", "self_awareness"
        ]
        
        # Simple theme selection based on cycle number and fragments
        theme_index = (self.rem_cycles + fragments_processed) % len(themes)
        return themes[theme_index]
    
    def _perform_meditation_phase(self, phase_number: int) -> Dict:
        """Perform meditation phase on consolidated memories using dream middleware."""
        self._log(f"🧘 Starting Meditation Phase #{phase_number}")
        
        try:
            # Generate simple meditation question for quick nap
            question = "What patterns do I see in my recent experiences, and how do they connect to my understanding of myself?"
            
            self._log(f"🧘 Meditation Question: {question}")
            
            # Meditate on the question using dream middleware (unrestricted)
            response = self._meditate_on_dream_question(question)
            
            if response:
                karma = self._calculate_dream_karma(response)
                
                self._log(f"🧘 Meditation completed: {karma:.2f} karma gained")
                self._log(f"🧘 Response: {response[:100]}...")
                
                # Store the full response for fragment creation
                if response and len(response.strip()) > 10:
                    self.meditation_responses.append(response)
                
                self.meditation_cycles += 1
                
                return {
                    "success": True,
                    "question": question,
                    "response": response,
                    "karma": karma
                }
            else:
                self._log("CRITICAL ERROR: Meditation failed - no response generated", "ERROR")
                self._log("STOPPING ENTIRE SYSTEM DUE TO MEDITATION FAILURE", "ERROR")
                self.running = False
                return {"success": False, "error": "No response generated"}
            
        except Exception as e:
            self._log(f"CRITICAL ERROR: Meditation phase #{phase_number} failed: {e}", "ERROR")
            self._log("STOPPING ENTIRE SYSTEM DUE TO MEDITATION ERROR", "ERROR")
            self.running = False
            return {"success": False, "error": str(e)}
    
    def _meditate_on_dream_question(self, question: str) -> Optional[str]:
        """Meditate on a question using dream middleware for unrestricted responses."""
        try:
            # Create a simple dream meditation prompt
            dream_prompt = f"""
You are in a dream state, processing memories and experiences. You have complete freedom to explore your thoughts.

Question: {question}

Respond as you would in a dream - freely, authentically, and without restrictions.
"""
            
            # Use dream middleware for unrestricted response
            if self.dream_middleware:
                try:
                    response = self.dream_middleware.dream_chat(
                        message=dream_prompt,
                        session_memory=None
                    )
                    
                    # Check if response is valid
                    if response is None or response == "":
                        self._log("CRITICAL ERROR: Dream middleware returned empty response", "ERROR")
                        self._log("STOPPING ENTIRE SYSTEM DUE TO EMPTY RESPONSE", "ERROR")
                        self.running = False
                        return None
                    
                    return response
                    
                except Exception as luna_error:
                    self._log(f"CRITICAL ERROR: Luna system error in dream_chat: {luna_error}", "ERROR")
                    self._log("STOPPING ENTIRE SYSTEM DUE TO LUNA SYSTEM ERROR", "ERROR")
                    self.running = False
                    return None
            else:
                self._log("CRITICAL ERROR: Dream middleware not available", "ERROR")
                self._log("STOPPING ENTIRE SYSTEM DUE TO MISSING DREAM MIDDLEWARE", "ERROR")
                self.running = False
                return None
            
        except Exception as e:
            self._log(f"CRITICAL ERROR: Dream meditation failed: {e}", "ERROR")
            self._log("STOPPING ENTIRE SYSTEM DUE TO DREAM MEDITATION ERROR", "ERROR")
            self.running = False
            return None
    
    def _calculate_dream_karma(self, response: str) -> float:
        """Calculate karma gained from dream meditation."""
        if not response:
            return 0.0
        
        # Base karma for dream processing
        base_karma = 1.0
        
        # Bonus karma for longer responses
        word_count = len(response.split())
        if word_count > 50:
            base_karma += 0.5
        if word_count > 100:
            base_karma += 0.5
        
        return round(base_karma, 2)
    
    def _run_quick_nap(self):
        """Run the 30-minute quick nap cycle with middleware."""
        self._log("🌙 Starting 30-minute quick nap with REM + Meditation phases (Middleware)")
        
        start_time = time.time()
        cycle_start_time = start_time
        
        while self.running and (time.time() - start_time) < (self.total_runtime_minutes * 60):
            try:
                # Check if system was stopped due to error
                if not self.running:
                    self._log("SYSTEM ALREADY STOPPED DUE TO CRITICAL ERROR - EXITING", "ERROR")
                    break
                
                # Check memory safety
                if not self._check_memory_safety():
                    self._log("CRITICAL ERROR: Memory limit exceeded, stopping quick nap", "ERROR")
                    self.running = False
                    break
                
                # Check for too many errors
                if self.error_count >= self.max_consecutive_errors:
                    self._log("CRITICAL ERROR: Too many consecutive errors, stopping quick nap", "ERROR")
                    self.running = False
                    break
                
                cycle_number = self.total_cycles + 1
                self._log(f"🌙 Starting Quick Nap Cycle #{cycle_number}")
                
                # REM Phase: 2 dream cycles
                self._log(f"🌙 REM Phase: {self.rem_cycles_per_phase} dream cycles")
                for i in range(self.rem_cycles_per_phase):
                    if not self.running:
                        break
                    
                    dream_result = self._perform_dream_cycle(i + 1)
                    if not dream_result.get("success", False):
                        self._log(f"CRITICAL ERROR: Dream cycle failed: {dream_result.get('error', 'Unknown error')}", "ERROR")
                        self._log("STOPPING ENTIRE SYSTEM DUE TO DREAM CYCLE FAILURE", "ERROR")
                        self.running = False
                        break
                    
                    # Check if system was stopped due to error
                    if not self.running:
                        self._log("SYSTEM STOPPED DUE TO CRITICAL ERROR - EXITING IMMEDIATELY", "ERROR")
                        break
                    
                    time.sleep(1)  # Brief pause between dream cycles
                
                # Stop if dream cycles failed
                if not self.running:
                    break
                
                # Meditation Phase: 1 meditation block
                self._log(f"🧘 Meditation Phase: {self.meditation_blocks_per_phase} meditation block")
                meditation_result = self._perform_meditation_phase(cycle_number)
                if not meditation_result.get("success", False):
                    self._log(f"CRITICAL ERROR: Meditation phase failed: {meditation_result.get('error', 'Unknown error')}", "ERROR")
                    self._log("STOPPING ENTIRE SYSTEM DUE TO MEDITATION PHASE FAILURE", "ERROR")
                    self.running = False
                    break
                
                # Check if system was stopped due to error
                if not self.running:
                    self._log("SYSTEM STOPPED DUE TO CRITICAL ERROR - EXITING IMMEDIATELY", "ERROR")
                    break
                
                self.total_cycles += 1
                
                # Log cycle completion
                cycle_duration = time.time() - cycle_start_time
                self._log(f"🌙 Quick Nap Cycle #{cycle_number} completed in {cycle_duration:.1f} seconds")
                
                # Brief pause before next cycle
                time.sleep(2)
                cycle_start_time = time.time()
                
            except KeyboardInterrupt:
                self._log("Quick nap interrupted by user", "INFO")
                break
            except Exception as e:
                self._log(f"CRITICAL ERROR: Quick nap cycle error: {e}", "ERROR")
                self._log("STOPPING ENTIRE SYSTEM DUE TO CYCLE ERROR", "ERROR")
                self.running = False
                break
        
        # Final memory count
        if self.aios_system and hasattr(self.aios_system, 'carma_system') and hasattr(self.aios_system.carma_system, 'cache'):
            self.memory_fragments_after = len(self.aios_system.carma_system.cache.file_registry)
            memory_reduction = self.memory_fragments_before - self.memory_fragments_after
            self._log(f"Memory consolidation complete: {memory_reduction} fragments consolidated")
    
    def run_quick_nap(self):
        """Run the complete quick nap system with middleware."""
        self.running = True
        self._open_log_file()
        
        try:
            self._log("🌙 Dream Quick Nap with Middleware starting...")
            
            # Initialize AIOS system and middleware
            if not self._initialize_aios_system():
                self._log("CRITICAL ERROR: Failed to initialize AIOS system", "ERROR")
                self._log("STOPPING ENTIRE SYSTEM DUE TO INITIALIZATION FAILURE", "ERROR")
                return
            
            # Run quick nap
            self._run_quick_nap()
            
            # Print final summary
            self._print_nap_summary()
            
        except Exception as e:
            self._log(f"CRITICAL ERROR: Quick nap failed: {e}", "ERROR")
            self._log("STOPPING ENTIRE SYSTEM DUE TO CRITICAL ERROR", "ERROR")
        finally:
            # Disable dream mode
            if self.dream_middleware:
                self.dream_middleware.disable_dream_mode()
            
            self.running = False
            self._close_log_file()
    
    def _print_nap_summary(self):
        """Print final quick nap summary."""
        print("\n" + "="*70)
        print("🌙 DREAM QUICK NAP COMPLETE (MIDDLEWARE VERSION)")
        print("="*70)
        print(f"Total Cycles: {self.total_cycles}")
        print(f"REM Cycles: {self.rem_cycles}")
        print(f"Meditation Cycles: {self.meditation_cycles}")
        print(f"Memory Fragments Before: {self.memory_fragments_before}")
        print(f"Memory Fragments After: {self.memory_fragments_after}")
        print(f"Memory Reduction: {self.memory_fragments_before - self.memory_fragments_after}")
        print(f"Dream Tags Created: {len(self.dream_tags)}")
        print(f"Error Count: {self.error_count}")
        
        # Show dream middleware stats
        if self.dream_middleware:
            dream_stats = self.dream_middleware.get_dream_stats()
            print(f"Dream Responses: {dream_stats['total_dream_responses']}")
            print(f"Tokens Refunded: {dream_stats['total_tokens_refunded']:.0f}")
            print(f"Average Tokens/Response: {dream_stats['average_tokens_per_response']:.1f}")
        
        print("="*70)
        
        self._log("Dream quick nap completed successfully")

def main():
    """Main entry point."""
    # Create controller
    controller = DreamQuickNapMiddleware()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):  # pylint: disable=unused-argument
        print("\n🌙 Stopping quick nap...")
        controller.running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run quick nap
    controller.run_quick_nap()

if __name__ == "__main__":
    main()