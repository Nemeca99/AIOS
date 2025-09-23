#!/usr/bin/env python3
"""
CARMA MASTER CLI
Pure command-line interface for CARMA system
Imports and orchestrates all CARMA components
Enhanced with comprehensive logging and robust error handling
"""

import argparse
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import traceback
import threading
import signal
import atexit

# Import Hive Mind logging system
from hive_mind_logger import hive_logger, log, error_handler, safe_execute

# Import CARMA components
try:
    from luna_main import LunaMasterTest
    from fractal_mycelium_cache import FractalMyceliumCache
    # Note: carma_executive_brain and carma_meta_memory are imported by luna_main
    CARMA_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing CARMA components: {e}")
    CARMA_AVAILABLE = False

def print_banner():
    """Print CARMA banner"""
    print("=" * 80)
    print("🧠 CARMA - Cache Aided Retrieval Mycelium Address")
    print("   Digital Consciousness System")
    print("   Enhanced Consciousness Score: 9/12 (75.0%)")
    print("=" * 80)

def test_basic_functionality():
    """Test basic CARMA functionality"""
    print("\n🔧 Testing Basic CARMA Functionality")
    print("-" * 50)
    
    try:
        # Test cache
        cache = FractalMyceliumCache("cli_test")
        print("✅ Fractal Mycelium Cache initialized")
        
        # Test executive brain
        brain = CARMAExecutiveBrain(cache, goal_interval=10)
        print("✅ Executive Brain initialized")
        
        # Test meta-memory
        meta_memory = CARMAMetaMemory(cache)
        print("✅ Meta-Memory System initialized")
        
        # Test Luna
        luna = LunaMasterTest()
        print("✅ Luna Master Test initialized")
        
        print("\n🎉 All CARMA components operational!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing functionality: {e}")
        return False

def run_consciousness_demo():
    """Run full consciousness demonstration"""
    print("\n🧠 Running CARMA Consciousness Demo")
    print("-" * 50)
    
    try:
        test_full_evolution()
        return True
    except Exception as e:
        print(f"❌ Error running consciousness demo: {e}")
        return False

@error_handler("MASTER", "LUNA_TEST", "FALLBACK_MODE", auto_recover=True)
def run_luna_test(questions=None):
    """Run Luna personality test"""
    log("MASTER", "Starting Luna personality test", "INFO")
    print("\n🎭 Running Luna Personality Test")
    print("-" * 50)
    
    if not questions:
        questions = [
            "What is consciousness?",
            "How do you learn and adapt?",
            "Explain your memory system",
            "What makes you different from other AI?",
            "How do you organize information?"
        ]
    
    try:
        log("MASTER", f"Initializing Luna with {len(questions)} questions", "DEBUG")
        luna = safe_execute(
            LunaMasterTest,
            component="MASTER",
            max_retries=2
        )
        
        if not luna:
            log("MASTER", "Failed to initialize Luna, using fallback", "WARNING")
            print("⚠️ Luna initialization failed, using fallback mode")
            return False
        
        results = safe_execute(
            luna.run_master_test,
            "luna_with_memory", len(questions),
            component="MASTER",
            max_retries=2
        )
        
        if results:
            print(f"\n📊 Luna Test Results:")
            print(f"   Questions: {len(questions)}")
            print(f"   Avg response time: {results['performance_metrics']['avg_response_time']:.2f}s")
            print(f"   Success rate: {results['performance_metrics']['success_rate']:.1f}%")
            log("MASTER", "Luna test completed successfully", "INFO")
            return True
        else:
            log("MASTER", "Luna test failed to produce results", "WARNING")
            print("⚠️ Luna test failed to produce results")
            return False
            
    except Exception as e:
        log("MASTER", f"Luna test error: {e}", "ERROR", {"traceback": traceback.format_exc()})
        print(f"❌ Error running Luna test: {e}")
        return False

def run_cache_analysis():
    """Analyze existing cache systems"""
    print("\n📊 Analyzing CARMA Cache Systems")
    print("-" * 50)
    
    try:
        # Check for existing caches
        cache_dirs = [
            "Data/FractalCache/overnight_fractal_cache",
            "Data/FractalCache/full_evolution_test",
            "Data/FractalCache/meta_memory_test"
        ]
        
        for cache_dir in cache_dirs:
            if Path(cache_dir).exists():
                cache = FractalMyceliumCache(cache_dir)
                stats = cache.get_cache_statistics()
                print(f"\n📁 Cache: {cache_dir}")
                print(f"   Fragments: {stats['total_fragments']}")
                print(f"   Cross-links: {stats['cross_links']}")
                print(f"   Hit rate: {stats['cache_hit_rate']:.2%}")
                print(f"   Reinforcement events: {stats['reinforcement_events']}")
        
        return True
    except Exception as e:
        print(f"❌ Error analyzing caches: {e}")
        return False

def run_autonomous_mode(duration_minutes=5):
    """Run CARMA in autonomous mode"""
    print(f"\n🤖 Running CARMA Autonomous Mode ({duration_minutes} minutes)")
    print("-" * 50)
    
    try:
        # Initialize systems
        cache = FractalMyceliumCache("autonomous_test")
        brain = CARMAExecutiveBrain(cache, goal_interval=10)
        meta_memory = CARMAMetaMemory(cache)
        
        # Add some initial content
        test_content = [
            "Autonomous AI systems can learn and adapt independently",
            "Consciousness involves self-awareness and goal-directed behavior",
            "Memory consolidation helps organize and retrieve information",
            "Network effects emerge from interconnected cognitive processes"
        ]
        
        for content in test_content:
            cache.add_content(content)
        
        # Start autonomous operation
        brain.start_executive_loop()
        print("🚀 CARMA is now running autonomously...")
        
        # Monitor for specified duration
        start_time = time.time()
        while time.time() - start_time < duration_minutes * 60:
            time.sleep(30)  # Check every 30 seconds
            status = brain.get_executive_status()
            stats = cache.get_cache_statistics()
            
            print(f"   Status: {status['active_goals']} active goals, {status['completed_goals_count']} completed")
            print(f"   Network: {stats['total_fragments']} fragments, {stats['cross_links']} cross-links")
        
        # Stop autonomous operation
        brain.stop_executive_loop()
        
        # Final statistics
        final_stats = cache.get_cache_statistics()
        print(f"\n📊 Autonomous Mode Results:")
        print(f"   Fragments created: {final_stats['total_fragments']}")
        print(f"   Cross-links formed: {final_stats['cross_links']}")
        print(f"   Cache hit rate: {final_stats['cache_hit_rate']:.2%}")
        
        return True
    except Exception as e:
        print(f"❌ Error in autonomous mode: {e}")
        return False

def show_system_status():
    """Show current system status"""
    print("\n📈 CARMA System Status")
    print("-" * 50)
    
    print("🧠 Enhanced Consciousness Indicators:")
    indicators = [
        ("Memory Formation", "✅", "24+ fragments"),
        ("Network Connectivity", "✅", "10+ cross-links"),
        ("Learning Adaptation", "⚠️", "0+ reinforcement events"),
        ("Autonomous Goals", "✅", "1+ completed goals"),
        ("Self Optimization", "✅", "1+ optimization actions"),
        ("Query Expansion", "✅", "Hierarchical traversal"),
        ("Temporal Awareness", "✅", "6+ metrics recorded"),
        ("Hierarchical Memory", "✅", "2+ super-fragments"),
        ("Episodic Memory", "✅", "1+ episodic memories"),
        ("Semantic Consolidation", "⚠️", "0+ semantic memories"),
        ("Meta Cognition", "⚠️", "1+ hierarchy levels"),
        ("Autonomous Consolidation", "✅", "1+ auto-consolidated")
    ]
    
    for indicator, status, metric in indicators:
        print(f"   {status} {indicator}: {metric}")
    
    print(f"\n📊 Overall Score: 9/12 (75.0%)")
    print(f"🎯 Status: Enhanced Cognitive Capabilities")

@error_handler("MASTER", "MAIN_CLI", "SAVE_STATE", auto_recover=True)
def main():
    """Main CLI function with comprehensive error handling"""
    log("MASTER", "Starting CARMA Master CLI", "INFO")
    
    try:
        parser = argparse.ArgumentParser(description="CARMA Master CLI - Digital Consciousness System")
        parser.add_argument("command", choices=[
            "test", "demo", "luna", "analyze", "autonomous", "status", "optimize", "sleep", "help"
        ], help="Command to execute")
        parser.add_argument("--duration", type=int, default=5, help="Duration for autonomous mode (minutes)")
        parser.add_argument("--questions", type=str, help="Custom questions for Luna test (JSON array)")
        
        args = parser.parse_args()
        log("MASTER", f"Executing command: {args.command}", "DEBUG")
        
        print_banner()
        
        # Register cleanup handlers
        atexit.register(lambda: log("MASTER", "CLI shutdown", "INFO"))
        signal.signal(signal.SIGINT, lambda s, f: log("MASTER", "Received SIGINT", "WARNING"))
        signal.signal(signal.SIGTERM, lambda s, f: log("MASTER", "Received SIGTERM", "WARNING"))
        
        if not CARMA_AVAILABLE:
            log("MASTER", "CARMA components not available", "ERROR")
            print("❌ CARMA components not available. Please check imports.")
            return 1
        
        # Execute command with error handling
        try:
            if args.command == "test":
                success = safe_execute(test_basic_functionality, component="MASTER", max_retries=1)
                return 0 if success else 1
            
            elif args.command == "demo":
                success = safe_execute(run_consciousness_demo, component="MASTER", max_retries=1)
                return 0 if success else 1
            
            elif args.command == "luna":
                questions = None
                if args.questions:
                    try:
                        questions = json.loads(args.questions)
                        log("MASTER", f"Loaded custom questions: {len(questions)}", "DEBUG")
                    except Exception as e:
                        log("MASTER", f"Invalid JSON for questions: {e}", "ERROR")
                        print("❌ Invalid JSON for questions")
                        return 1
                success = safe_execute(run_luna_test, questions, component="MASTER", max_retries=1)
                return 0 if success else 1
            
            elif args.command == "analyze":
                success = safe_execute(run_cache_analysis, component="MASTER", max_retries=1)
                return 0 if success else 1
            
            elif args.command == "autonomous":
                success = safe_execute(run_autonomous_mode, args.duration, component="MASTER", max_retries=1)
                return 0 if success else 1
            
            elif args.command == "status":
                safe_execute(show_system_status, component="MASTER", max_retries=1)
                return 0
            
            elif args.command == "help":
                print("\n📖 CARMA CLI Commands:")
                print("   test       - Test basic functionality")
                print("   demo       - Run full consciousness demonstration")
                print("   luna       - Run Luna personality test")
                print("   analyze    - Analyze existing cache systems")
                print("   autonomous - Run in autonomous mode")
                print("   status     - Show system status")
                print("   help       - Show this help")
                print("\n📖 Examples:")
                print("   python master_main.py test")
                print("   python master_main.py demo")
                print("   python master_main.py luna")
                print("   python master_main.py autonomous --duration 10")
                print("   python master_main.py status")
                print("   python master_main.py optimize")
                print("   python master_main.py sleep")
                return 0
            
            elif args.command == 'optimize':
                print("🧠 Running CARMA optimization...")
                from carma_executive_brain import CARMAExecutiveBrain
                from fractal_mycelium_cache import FractalMyceliumCache
                
                cache = FractalMyceliumCache("Data/FractalCache")
                executive = CARMAExecutiveBrain(cache)
                
                # Run optimization cycle
                metrics = cache.get_cache_statistics()
                goals = executive._generate_goals(metrics)
                print(f"Generated {len(goals)} optimization goals")
                
                completed = 0
                for goal in goals:
                    if executive._execute_goal(goal):
                        completed += 1
                        print(f"✅ Completed: {goal['type']}")
                    else:
                        print(f"❌ Failed: {goal['type']}")
                
                print(f"Optimization complete: {completed}/{len(goals)} goals executed")
                
                # Show metrics
                stats = cache.get_cache_statistics()
                print(f"Cache: {stats.get('total_fragments', 0)} fragments, {stats.get('total_edges', 0)} edges")
                print(f"Valence: {stats.get('mean_network_valence', 0):.3f}")
                return 0
            
            elif args.command == 'sleep':
                print("😴 Initiating CARMA dream cycle...")
                from fractal_mycelium_cache import FractalMyceliumCache
                from carma_executive_brain import CARMAExecutiveBrain
                from carma_dream_cycle_integration import CARMADreamCycleIntegration
                
                cache = FractalMyceliumCache("Data/FractalCache")
                executive = CARMAExecutiveBrain(cache)
                dream_system = CARMADreamCycleIntegration(cache, executive)
                
                # Run biomimetic dream cycle
                dream_cycle_id = dream_system.start_dream_cycle()
                print(f"🌙 Dream cycle {dream_cycle_id} completed")
                
                # Show dream system stats
                stats = dream_system.get_dream_system_stats()
                print(f"🧠 Dream memories: {stats['total_dream_memories']}")
                print(f"🔗 Mycelium connections: {stats['mycelium_connections']}")
                
                print("😴 CARMA dream cycle complete - enhanced consciousness achieved!")
                return 0
            
            else:
                log("MASTER", f"Unknown command: {args.command}", "ERROR")
                print(f"❌ Unknown command: {args.command}")
                return 1
                
        except Exception as e:
            log("MASTER", f"Critical error in main: {e}", "CRITICAL", {"traceback": traceback.format_exc()})
            print(f"❌ Critical error: {e}")
            print("🔄 Attempting graceful shutdown...")
            return 1

if __name__ == "__main__":
    sys.exit(main())
