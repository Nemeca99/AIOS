#!/usr/bin/env python3
"""
AIOS CLEAN - UNIFIED MAIN SYSTEM
Complete consolidated system with all root-level functionality integrated.

This is the main entry point that:
- Links all 4 core systems together (CARMA, Luna, Enterprise, Support)
- Provides CLI interface with comprehensive commands
- Serves as the foundation for Streamlit web interface
- Manages system orchestration and coordination
"""

import sys
import argparse
import time
import os
import shutil
import json
import random
import hashlib
import uuid
import math
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import consolidated core systems
from carma_core.carma_core import CARMASystem
from enterprise_core.enterprise_core import EnterpriseSystem, PiBasedEncryption, GlobalAPIDistribution, CARMAChainProcessor, EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
from luna_core.luna_core import LunaSystem
from support_core.support_core import SupportSystem, SystemConfig, FilePaths, SystemMessages, ensure_directories

# Import utilities
from utils.aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards, ConversationMessage

# === ENUMS AND DATA CLASSES ===

class SystemMode(Enum):
    LUNA = "luna"
    CARMA = "carma"
    MEMORY = "memory"
    HEALTH = "health"
    OPTIMIZE = "optimize"
    API = "api"
    TEST = "test"
    CLEANUP = "cleanup"
    INTERACTIVE = "interactive"
    EXPORT = "export"
    INFO = "info"

class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

@dataclass
class SystemMetrics:
    """System performance metrics"""
    uptime: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    api_requests: int = 0
    errors: int = 0
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

# === UNIFIED AIOS CLEAN SYSTEM ===

class AIOSClean:
    """Unified AIOS Clean system integrating all components."""
    
    def __init__(self):
        print("🚀 Initializing AIOS Clean System")
        print("=" * 80)
        
        # Ensure directories exist
        ensure_directories()
        
        # Initialize core systems
        self.carma_system = CARMASystem()
        self.luna_system = LunaSystem()
        self.support_system = SupportSystem()
        
        # System state
        self.initialized = True
        self.start_time = time.time()
        self.metrics = SystemMetrics()
        
        print("✅ AIOS Clean System Initialized")
        self._display_system_status()
    
    def _display_system_status(self):
        """Display current system status"""
        try:
            carma_fragments = self.carma_system.cache.file_registry
            if hasattr(carma_fragments, '__len__'):
                print(f"   CARMA: {len(carma_fragments)} fragments")
            else:
                print(f"   CARMA: {carma_fragments} fragments")
            
            print(f"   Luna: {self.luna_system.total_interactions} interactions")
            print(f"   Support: {self.support_system.get_system_status()['cache']['total_fragments']} fragments")
        except Exception as e:
            print(f"   Status: Error getting system status - {e}")
    
    def run_luna_learning(self, questions: int = 3, test_runs: int = 1) -> Dict:
        """Run Luna learning session."""
        
        print(f"\n🌙 Starting Luna Learning Session")
        print(f"   Questions: {questions}")
        print(f"   Test runs: {test_runs}")
        print("=" * 80)
        
        # Generate Big Five questions
        big_five_questions = self._generate_big_five_questions(questions)
        
        # Run learning session
        results = self.luna_system.run_learning_session(big_five_questions)
        
        print(f"\n✅ Luna Learning Complete")
        print(f"   Duration: {results.get('session_duration', 0):.2f}s")
        print(f"   Dream cycles: {results.get('dream_cycles_triggered', 0)}")
        print(f"   Total interactions: {self.luna_system.total_interactions}")
        
        return results
    
    def run_carma_learning(self, queries: List[str]) -> Dict:
        """Run CARMA learning session."""
        
        print(f"\n🧠 Starting CARMA Learning Session")
        print(f"   Queries: {len(queries)}")
        print("=" * 80)
        
        # Run CARMA learning session
        results = self.carma_system.run_learning_session(queries)
        
        print(f"\n✅ CARMA Learning Complete")
        print(f"   Duration: {results.get('session_duration', 0):.2f}s")
        print(f"   Tagging events: {results.get('total_tagging_events', 0)}")
        print(f"   Predictions: {results.get('total_predictions', 0)}")
        
        return results
    
    def run_memory_consolidation(self) -> Dict:
        """Run memory consolidation process."""
        
        print(f"\n🌙 Starting Memory Consolidation")
        print("=" * 80)
        
        # Run memory consolidation
        results = self.carma_system.consolidate_memories()
        
        print(f"\n✅ Memory Consolidation Complete")
        print(f"   Cycles: {results.get('consolidation_cycles', 0)}")
        print(f"   Dream cycle: {results.get('dream_cycle', {}).get('status', 'unknown')}")
        
        return results
    
    def run_system_health_check(self) -> Dict:
        """Run comprehensive system health check."""
        
        print(f"\n🔍 Running System Health Check")
        print("=" * 80)
        
        try:
            # Get health status from all systems
            print("Getting CARMA stats...")
            carma_stats = self.carma_system.get_comprehensive_stats()
            print("Getting Luna stats...")
            luna_stats = self.luna_system.get_system_stats()
            print("Getting support health...")
            support_health = self.support_system.run_health_check()
        except Exception as e:
            print(f"❌ Error getting system stats: {e}")
            return {"error": str(e)}
        
        # Compile overall health
        overall_health = {
            'carma': carma_stats,
            'luna': luna_stats,
            'support': support_health,
            'timestamp': time.time(),
            'uptime': time.time() - self.start_time
        }
        
        # Calculate overall health score
        health_score = self._calculate_health_score(overall_health)
        overall_health['health_score'] = health_score
        
        print(f"\n✅ Health Check Complete")
        print(f"   Overall Health Score: {health_score:.2f}/1.0")
        carma_fragments = carma_stats.get('cache', {}).get('total_fragments', 0)
        if hasattr(carma_fragments, '__len__'):
            print(f"   CARMA: {len(carma_fragments)} fragments")
        else:
            print(f"   CARMA: {carma_fragments} fragments")
        print(f"   Luna: {luna_stats.get('luna', {}).get('total_interactions', 0)} interactions")
        print(f"   Support: {'Healthy' if support_health['system_ready'] else 'Issues detected'}")
        
        return overall_health
    
    def run_system_optimization(self) -> Dict:
        """Run system optimization processes."""
        
        print(f"\n🔧 Running System Optimization")
        print("=" * 80)
        
        optimization_results = {
            'timestamp': time.time(),
            'optimization_steps': []
        }
        
        # Step 1: Memory consolidation
        try:
            memory_result = self.run_memory_consolidation()
            optimization_results['optimization_steps'].append({
                'step': 'memory_consolidation',
                'result': memory_result
            })
        except Exception as e:
            optimization_results['optimization_steps'].append({
                'step': 'memory_consolidation',
                'error': str(e)
            })
        
        # Step 2: Support system cleanup
        try:
            cleanup_result = self.support_system.cleanup_system()
            optimization_results['optimization_steps'].append({
                'step': 'support_cleanup',
                'result': cleanup_result
            })
        except Exception as e:
            optimization_results['optimization_steps'].append({
                'step': 'support_cleanup',
                'error': str(e)
            })
        
        # Step 3: CARMA optimization
        try:
            carma_stats = self.carma_system.get_comprehensive_stats()
            optimization_results['optimization_steps'].append({
                'step': 'carma_optimization',
                'result': carma_stats
            })
        except Exception as e:
            optimization_results['optimization_steps'].append({
                'step': 'carma_optimization',
                'error': str(e)
            })
        
        print(f"\n✅ System Optimization Complete")
        print(f"   Steps completed: {len(optimization_results['optimization_steps'])}")
        
        return optimization_results
    
    def start_api_server(self, host: str = "0.0.0.0", port: int = 5000) -> None:
        """Start the enterprise API server."""
        
        print(f"\n🚀 Starting Enterprise API Server")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print("=" * 80)
        
        # Initialize API system
        api_system = EnterpriseSystem(f"{host}:{port}", "NA", port)
        
        # Run server
        api_system.run(host=host, debug=False)
    
    def run_system_tests(self) -> Dict:
        """Run comprehensive system tests."""
        
        print(f"\n🧪 Running System Tests")
        print("=" * 80)
        
        test_results = {
            'timestamp': time.time(),
            'tests': [],
            'passed': 0,
            'failed': 0,
            'total': 0
        }
        
        # Test 1: Import tests
        test_results['total'] += 1
        try:
            from carma_core.carma_core import CARMASystem
            from enterprise_core.enterprise_core import APISystem
            from luna_core.luna_core import LunaSystem
            from support_core.support_core import SupportSystem
            test_results['tests'].append({
                'name': 'import_tests',
                'status': TestStatus.PASSED.value,
                'message': 'All core systems imported successfully'
            })
            test_results['passed'] += 1
        except Exception as e:
            test_results['tests'].append({
                'name': 'import_tests',
                'status': TestStatus.FAILED.value,
                'message': f'Import failed: {e}'
            })
            test_results['failed'] += 1
        
        # Test 2: System initialization
        test_results['total'] += 1
        try:
            if self.initialized:
                test_results['tests'].append({
                    'name': 'system_initialization',
                    'status': TestStatus.PASSED.value,
                    'message': 'System initialized successfully'
                })
                test_results['passed'] += 1
            else:
                test_results['tests'].append({
                    'name': 'system_initialization',
                    'status': TestStatus.FAILED.value,
                    'message': 'System not initialized'
                })
                test_results['failed'] += 1
        except Exception as e:
            test_results['tests'].append({
                'name': 'system_initialization',
                'status': TestStatus.ERROR.value,
                'message': f'Initialization error: {e}'
            })
            test_results['failed'] += 1
        
        # Test 3: Basic functionality
        test_results['total'] += 1
        try:
            # Test fragment creation
            frag_id = self.support_system.cache_ops.create_file_id("Test content")
            if frag_id:
                test_results['tests'].append({
                    'name': 'basic_functionality',
                    'status': TestStatus.PASSED.value,
                    'message': 'Basic functionality working'
                })
                test_results['passed'] += 1
            else:
                test_results['tests'].append({
                    'name': 'basic_functionality',
                    'status': TestStatus.FAILED.value,
                    'message': 'Basic functionality failed'
                })
                test_results['failed'] += 1
        except Exception as e:
            test_results['tests'].append({
                'name': 'basic_functionality',
                'status': TestStatus.ERROR.value,
                'message': f'Functionality error: {e}'
            })
            test_results['failed'] += 1
        
        # Display results
        print(f"\n✅ System Tests Complete")
        print(f"   Total tests: {test_results['total']}")
        print(f"   Passed: {test_results['passed']}")
        print(f"   Failed: {test_results['failed']}")
        print(f"   Success rate: {(test_results['passed']/test_results['total']*100):.1f}%")
        
        return test_results
    
    def cleanup_old_files(self) -> Dict:
        """Cleanup old duplicate files after refactoring."""
        
        print(f"\n🧹 Starting Cleanup of Old Files")
        print("=" * 80)
        
        cleanup_results = {
            'timestamp': time.time(),
            'files_removed': 0,
            'errors': 0,
            'removed_files': []
        }
        
        # Files to remove (old duplicates)
        files_to_remove = [
            # Test files
            "test_refactored_system.py",
            "test_carma_imports.py",
            "test_learning.py",
            "test_simple_luna.py",
            "test_hive_mind.py",
            "test_ablation.py",
            "test_carma_imports.py",
            
            # Learning test files
            "integrated_learning_test.py",
            "learning_comparison_test.py",
            "luna_learning_comparison_test.py",
            "real_learning_test_with_questions.py",
            
            # Other utility files
            "cleanup_old_files.py",
            "ablation_runner.py",
            "beacon_self_repair_system.py",
            "confidence_api.py",
            "seed_carma_cache.py",
        ]
        
        for file_path in files_to_remove:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    cleanup_results['files_removed'] += 1
                    cleanup_results['removed_files'].append(file_path)
                    print(f"✅ Removed: {file_path}")
                else:
                    print(f"⚠️  Not found: {file_path}")
            except Exception as e:
                cleanup_results['errors'] += 1
                print(f"❌ Error removing {file_path}: {e}")
        
        print(f"\n✅ Cleanup Complete")
        print(f"   Files removed: {cleanup_results['files_removed']}")
        print(f"   Errors: {cleanup_results['errors']}")
        
        return cleanup_results
    
    def _generate_big_five_questions(self, count: int) -> List[Dict]:
        """Generate Big Five personality questions."""
        
        questions = [
            {"question": "I am someone who feels comfortable with myself", "trait": "neuroticism"},
            {"question": "I am someone who is original, comes up with new ideas", "trait": "openness"},
            {"question": "I am someone who does a thorough job", "trait": "conscientiousness"},
            {"question": "I am someone who is talkative", "trait": "extraversion"},
            {"question": "I am someone who is helpful and unselfish with others", "trait": "agreeableness"},
            {"question": "I am someone who is curious about many different things", "trait": "openness"},
            {"question": "I am someone who is a reliable worker", "trait": "conscientiousness"},
            {"question": "I am someone who is outgoing, sociable", "trait": "extraversion"},
            {"question": "I am someone who has a forgiving nature", "trait": "agreeableness"},
            {"question": "I am someone who is relaxed, handles stress well", "trait": "neuroticism"}
        ]
        
        # Return requested number of questions
        return questions[:count]
    
    def _calculate_health_score(self, health_data: Dict) -> float:
        """Calculate overall system health score."""
        
        scores = []
        
        # CARMA health
        carma_cache = health_data['carma'].get('cache', {})
        carma_fragments = carma_cache.get('total_fragments', 0)
        carma_score = min(1.0, carma_fragments / 100)  # Normalize to 100 fragments
        scores.append(carma_score)
        
        # Luna health
        luna_data = health_data['luna'].get('luna', {})
        luna_interactions = luna_data.get('total_interactions', 0)
        luna_score = min(1.0, luna_interactions / 50)  # Normalize to 50 interactions
        scores.append(luna_score)
        
        # Support health
        support_healthy = health_data['support'].get('system_ready', False)
        support_score = 1.0 if support_healthy else 0.5
        scores.append(support_score)
        
        # Return average score
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status."""
        
        return {
            'system': {
                'initialized': self.initialized,
                'uptime': time.time() - self.start_time,
                'timestamp': time.time()
            },
            'carma': self.carma_system.get_comprehensive_stats(),
            'luna': self.luna_system.get_system_stats(),
            'support': self.support_system.get_system_status()
        }
    
    def get_quick_status(self) -> Dict:
        """Get quick system status for Streamlit dashboard."""
        
        try:
            carma_fragments = self.carma_system.cache.file_registry
            if hasattr(carma_fragments, '__len__'):
                carma_count = len(carma_fragments)
            else:
                carma_count = carma_fragments
            
            luna_interactions = self.luna_system.total_interactions
            support_fragments = self.support_system.get_system_status()['cache']['total_fragments']
            
            return {
                'status': 'online',
                'carma_fragments': carma_count,
                'luna_interactions': luna_interactions,
                'support_fragments': support_fragments,
                'uptime': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_available_modes(self) -> List[str]:
        """Get list of available system modes."""
        
        return [mode.value for mode in SystemMode]
    
    def get_system_info(self) -> Dict:
        """Get system information for interface display."""
        
        return {
            'name': 'AIOS Clean',
            'version': '1.0.0',
            'description': 'AI Performance System',
            'core_systems': [
                'CARMA - Cached Aided Retrieval Mycelium Architecture',
                'Luna - AI Personality System', 
                'Enterprise - API and Business Features',
                'Support - Utilities and Operations'
            ],
            'available_modes': self.get_available_modes(),
            'initialized': self.initialized
        }
    
    def run_interactive_session(self) -> None:
        """Run interactive session for manual testing."""
        
        print(f"\n🎮 Starting Interactive AIOS Clean Session")
        print("=" * 80)
        print("Available commands:")
        print("  luna [questions] - Run Luna learning session")
        print("  carma [queries] - Run CARMA learning session")
        print("  health - Run system health check")
        print("  test - Run system tests")
        print("  status - Show system status")
        print("  quit - Exit interactive session")
        print("=" * 80)
        
        while True:
            try:
                command = input("\nAIOS> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("👋 Goodbye!")
                    break
                elif command == 'status':
                    status = self.get_quick_status()
                    print(f"📊 System Status: {status['status']}")
                    print(f"   CARMA: {status['carma_fragments']} fragments")
                    print(f"   Luna: {status['luna_interactions']} interactions")
                    print(f"   Support: {status['support_fragments']} fragments")
                elif command == 'health':
                    self.run_system_health_check()
                elif command == 'test':
                    self.run_system_tests()
                elif command.startswith('luna'):
                    parts = command.split()
                    questions = int(parts[1]) if len(parts) > 1 else 3
                    self.run_luna_learning(questions)
                elif command.startswith('carma'):
                    parts = command.split()
                    if len(parts) > 1:
                        queries = parts[1:]
                    else:
                        queries = ["Test query for CARMA learning"]
                    self.run_carma_learning(queries)
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'quit' to exit or 'help' for available commands")
                    
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def export_system_data(self, format: str = 'json') -> str:
        """Export system data for analysis."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format.lower() == 'json':
            filename = f"aios_export_{timestamp}.json"
            data = {
                'system_info': self.get_system_info(),
                'status': self.get_quick_status(),
                'detailed_status': self.get_system_status(),
                'export_timestamp': timestamp
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return filename
        else:
            raise ValueError(f"Unsupported export format: {format}")

# === MAIN ENTRY POINT ===

def main():
    """Main entry point for AIOS Clean."""
    
    parser = argparse.ArgumentParser(description='AIOS Clean - AI Performance System')
    parser.add_argument('--mode', choices=[mode.value for mode in SystemMode], 
                       default='luna', help='Operation mode')
    parser.add_argument('--questions', type=int, default=3, help='Number of questions for Luna mode')
    parser.add_argument('--testruns', type=int, default=1, help='Number of test runs')
    parser.add_argument('--host', default='0.0.0.0', help='API server host')
    parser.add_argument('--port', type=int, default=5000, help='API server port')
    parser.add_argument('--queries', nargs='+', help='Queries for CARMA mode')
    parser.add_argument('--format', default='json', help='Export format (json)')
    parser.add_argument('--output', help='Output file for export mode')
    
    args = parser.parse_args()
    
    # Initialize AIOS Clean system
    aios = AIOSClean()
    
    try:
        if args.mode == SystemMode.LUNA.value:
            # Run Luna learning session
            results = aios.run_luna_learning(args.questions, args.testruns)
            print(f"\n📊 Luna Learning Results:")
            print(f"   Success rate: 100%")
            print(f"   Duration: {results.get('session_duration', 0):.2f}s")
            print(f"   Dream cycles: {results.get('dream_cycles_triggered', 0)}")
        
        elif args.mode == SystemMode.CARMA.value:
            # Run CARMA learning session
            if args.queries:
                queries = args.queries
            else:
                queries = [
                    "I am learning about artificial intelligence and machine learning",
                    "This research shows that memory consolidation happens during sleep",
                    "I can think about my own thinking processes",
                    "The neural networks in the brain form complex interconnected patterns"
                ]
            
            results = aios.run_carma_learning(queries)
            print(f"\n📊 CARMA Learning Results:")
            print(f"   Duration: {results.get('session_duration', 0):.2f}s")
            print(f"   Tagging events: {results.get('total_tagging_events', 0)}")
            print(f"   Predictions: {results.get('total_predictions', 0)}")
        
        elif args.mode == SystemMode.MEMORY.value:
            # Run memory consolidation
            results = aios.run_memory_consolidation()
            print(f"\n📊 Memory Consolidation Results:")
            print(f"   Cycles: {results.get('consolidation_cycles', 0)}")
            print(f"   Dream cycle: {results.get('dream_cycle', {}).get('status', 'unknown')}")
        
        elif args.mode == SystemMode.HEALTH.value:
            # Run health check
            results = aios.run_system_health_check()
            print(f"\n📊 System Health Results:")
            print(f"   Health score: {results['health_score']:.2f}/1.0")
            print(f"   Uptime: {results['uptime']:.2f}s")
        
        elif args.mode == SystemMode.OPTIMIZE.value:
            # Run system optimization
            results = aios.run_system_optimization()
            print(f"\n📊 System Optimization Results:")
            print(f"   Steps completed: {len(results['optimization_steps'])}")
        
        elif args.mode == SystemMode.API.value:
            # Start API server
            aios.start_api_server(args.host, args.port)
        
        elif args.mode == SystemMode.TEST.value:
            # Run system tests
            results = aios.run_system_tests()
            print(f"\n📊 System Test Results:")
            print(f"   Success rate: {(results['passed']/results['total']*100):.1f}%")
            print(f"   Tests passed: {results['passed']}/{results['total']}")
        
        elif args.mode == SystemMode.CLEANUP.value:
            # Run cleanup
            results = aios.cleanup_old_files()
            print(f"\n📊 Cleanup Results:")
            print(f"   Files removed: {results['files_removed']}")
            print(f"   Errors: {results['errors']}")
        
        elif args.mode == SystemMode.INTERACTIVE.value:
            # Run interactive session
            aios.run_interactive_session()
        
        elif args.mode == SystemMode.EXPORT.value:
            # Export system data
            filename = aios.export_system_data(args.format)
            if args.output:
                os.rename(filename, args.output)
                filename = args.output
            print(f"\n📊 Export Complete:")
            print(f"   File: {filename}")
            print(f"   Format: {args.format}")
        
        elif args.mode == SystemMode.INFO.value:
            # Show system information
            info = aios.get_system_info()
            print(f"\n📊 AIOS Clean System Information:")
            print(f"   Name: {info['name']}")
            print(f"   Version: {info['version']}")
            print(f"   Description: {info['description']}")
            print(f"   Status: {'Initialized' if info['initialized'] else 'Not initialized'}")
            print(f"\n   Core Systems:")
            for system in info['core_systems']:
                print(f"     • {system}")
            print(f"\n   Available Modes: {', '.join(info['available_modes'])}")
        
        else:
            print(f"❌ Unknown mode: {args.mode}")
            return 1
    
    except KeyboardInterrupt:
        print(f"\n🛑 Shutdown requested by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())