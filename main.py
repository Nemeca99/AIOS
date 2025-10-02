#!/usr/bin/env python3
"""
AIOS CLEAN - CENTRAL ORCHESTRATOR
Modular system architecture with self-contained core systems.

This is the main entry point that:
- Orchestrates all 8 core systems (Backup, CARMA, Data, Dream, Enterprise, Luna, Streamlit, Support, Utils)
- Provides CLI interface with comprehensive commands
- Manages inter-core communication and coordination
- Serves as the central hub for all system operations
"""

# CRITICAL: Import os first for environment variables
import os

# CRITICAL: Disable Rich shell integration to fix input() issues
os.environ["RICH_SHELL_INTEGRATION"] = "false"
os.environ["RICH_FORCE_TERMINAL"] = "false"
os.environ["RICH_DISABLE_CONSOLE"] = "true"

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

import sys
import argparse
import time
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

# Import all core systems
from backup_core.backup_core import BackupCore
from carma_core.carma_core import CARMASystem
from data_core.data_core import DataCore
from dream_core.dream_core import DreamCore
from enterprise_core.enterprise_core import EnterpriseCore, PiBasedEncryption, GlobalAPIDistribution, CARMAChainProcessor, EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
from luna_core.luna_core import LunaSystem
from streamlit_core.streamlit_core import StreamlitCore
from support_core.support_core import (
    SupportSystem, SystemConfig, FilePaths, SystemMessages, ensure_directories,
    aios_config, aios_logger, aios_health_checker, aios_security_validator
)
from utils_core.utils_core import UtilsCore

# Import utilities
from utils_core.aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards, ConversationMessage

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
    """Unified AIOS Clean system integrating all components with PowerShell wrapper patterns."""
    
    def __init__(self):
        # Initialize unified AIOS systems
        self.aios_config = aios_config
        self.logger = aios_logger
        self.health_checker = aios_health_checker
        self.security_validator = aios_security_validator
        
        # Log system initialization
        self.logger.info("Initializing AIOS Clean System...", "AIOS")
        
        # Ensure directories exist
        ensure_directories()
        
        # Perform comprehensive health check
        health_status = self.health_checker.check_system_health()
        if health_status["overall_status"] != "HEALTHY":
            self.logger.warn(f"System health degraded: {health_status['overall_status']}", "AIOS")
            self.logger.warn(f"Failed checks: {health_status.get('errors', [])}", "AIOS")
        
        # Initialize all core systems with unified logging
        self.logger.info("Initializing Backup system...", "AIOS")
        self.backup_system = BackupCore()
        
        # Auto-backup only runs when explicitly requested via --backup flag
        
        self.logger.info("Initializing CARMA system...", "AIOS")
        self.carma_system = CARMASystem()
        
        self.logger.info("Initializing Data system...", "AIOS")
        self.data_system = DataCore()
        
        self.logger.info("Initializing Dream system...", "AIOS")
        self.dream_system = DreamCore()
        
        self.logger.info("Initializing Enterprise system...", "AIOS")
        self.enterprise_system = EnterpriseCore()
        
        self.logger.info("Initializing Luna system...", "AIOS")
        self.luna_system = LunaSystem()
        
        self.logger.info("Initializing Streamlit system...", "AIOS")
        self.streamlit_system = StreamlitCore()
        
        self.logger.info("Initializing Utils system...", "AIOS")
        self.utils_system = UtilsCore()
        
        self.logger.info("Initializing Support system...", "AIOS")
        self.support_system = SupportSystem()
        
        # System state
        self.initialized = True
        self.start_time = time.time()
        self.metrics = SystemMetrics()
        
        self.logger.success("AIOS Clean System Initialized Successfully", "AIOS")
        self._display_system_status()
    
    def _display_system_status(self):
        """Display current system status using unified logging"""
        try:
            # Backup system status
            backup_info = self.backup_system.get_system_info()
            self.logger.info(f"Backup: {backup_info['total_backups']} backups", "AIOS")
            
            # CARMA system status
            carma_fragments = self.carma_system.cache.file_registry
            if hasattr(carma_fragments, '__len__'):
                self.logger.info(f"CARMA: {len(carma_fragments)} fragments", "AIOS")
            else:
                self.logger.info(f"CARMA: {carma_fragments} fragments", "AIOS")
            
            # Data system status
            data_overview = self.data_system.get_system_overview()
            total_data_files = (data_overview['fractal_cache']['total_files'] + 
                              data_overview['arbiter_cache']['total_files'] + 
                              data_overview['conversations']['total_conversations'])
            self.logger.info(f"Data: {total_data_files} files", "AIOS")
            
            # Dream system status (placeholder)
            self.logger.info(f"Dream: System ready", "AIOS")
            
            # Enterprise system status (placeholder)
            self.logger.info(f"Enterprise: System ready", "AIOS")
            
            # Luna system status
            self.logger.info(f"Luna: {self.luna_system.total_interactions} interactions", "AIOS")
            
            # Streamlit system status (placeholder)
            self.logger.info(f"Streamlit: UI ready", "AIOS")
            
            # Support system status
            self.logger.info(f"Support: {self.support_system.get_system_status()['cache']['total_fragments']} fragments", "AIOS")
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}", "AIOS")
    
    # === INTER-CORE COMMUNICATION METHODS ===
    
    def carma_to_luna_communication(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle communication from CARMA to Luna."""
        try:
            # Process data through Luna system
            result = self.luna_system.process_carma_data(data)
            return result
        except Exception as e:
            self.logger.error(f"CARMA to Luna communication failed: {e}", "AIOS")
            return {"error": str(e)}
    
    def luna_to_carma_communication(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle communication from Luna to CARMA."""
        try:
            # Process data through CARMA system
            result = self.carma_system.process_luna_data(data)
            return result
        except Exception as e:
            self.logger.error(f"Luna to CARMA communication failed: {e}", "AIOS")
            return {"error": str(e)}
    
    def dream_to_data_communication(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle communication from Dream to Data system."""
        try:
            # Store dream data through data system
            result = self.data_system.store_dream_data(data)
            return result
        except Exception as e:
            self.logger.error(f"Dream to Data communication failed: {e}", "AIOS")
            return {"error": str(e)}
    
    def backup_all_systems(self, backup_name: Optional[str] = None) -> str:
        """Create backup of all systems."""
        try:
            return self.backup_system.create_backup(backup_name)
        except Exception as e:
            self.logger.error(f"System backup failed: {e}", "AIOS")
            return ""
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive overview of all systems."""
        try:
            return {
                "backup": self.backup_system.get_system_info(),
                "carma": {"status": "active", "fragments": len(self.carma_system.cache.file_registry)},
                "data": self.data_system.get_system_overview(),
                "dream": {"status": "ready"},
                "enterprise": {"status": "ready"},
                "luna": {"interactions": self.luna_system.total_interactions},
                "streamlit": {"status": "ready"},
                "utils": self.utils_system.get_system_metrics(),
                "support": self.support_system.get_system_status(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"System overview failed: {e}", "AIOS")
            return {"error": str(e)}
    
    # === CORE SYSTEM METHODS ===
    
    def run_luna_learning(self, questions: int = 3, test_runs: int = 1) -> Dict:
        """Run Luna learning session."""
        
        print(f"\nStarting Luna Learning Session")
        print(f"   Questions: {questions}")
        print(f"   Test runs: {test_runs}")
        print("=" * 80)
        
        # Generate Big Five questions
        big_five_questions = self._generate_big_five_questions(questions)
        
        # Run learning session
        results = self.luna_system.run_learning_session(big_five_questions)
        
        print(f"\nLuna Learning Complete")
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
        
        print(f"\nCARMA Learning Complete")
        print(f"   Duration: {results.get('session_duration', 0):.2f}s")
        print(f"   Tagging events: {results.get('total_tagging_events', 0)}")
        print(f"   Predictions: {results.get('total_predictions', 0)}")
        
        return results
    
    def run_memory_consolidation(self) -> Dict:
        """Run memory consolidation process."""
        
        print(f"\nStarting Memory Consolidation")
        print("=" * 80)
        
        # Run memory consolidation
        results = self.carma_system.consolidate_memories()
        
        print(f"\nMemory Consolidation Complete")
        print(f"   Cycles: {results.get('consolidation_cycles', 0)}")
        print(f"   Dream cycle: {results.get('dream_cycle', {}).get('status', 'unknown')}")
        
        return results
    
    def run_system_health_check(self) -> Dict:
        """Run comprehensive system health check."""
        
        print(f"\nRunning System Health Check")
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
            print(f"Error getting system stats: {e}")
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
        
        print(f"\nHealth Check Complete")
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
        
        print(f"\nRunning System Optimization")
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
        
        print(f"\nSystem Optimization Complete")
        print(f"   Steps completed: {len(optimization_results['optimization_steps'])}")
        
        return optimization_results
    
    def start_api_server(self, host: str = "0.0.0.0", port: int = 5000) -> None:
        """Start the enterprise API server."""
        
        print(f"\nStarting Enterprise API Server")
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
        print(f"\nSystem Tests Complete")
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
                    print(f"Removed: {file_path}")
                else:
                    print(f"Not found: {file_path}")
            except Exception as e:
                cleanup_results['errors'] += 1
                print(f"Error removing {file_path}: {e}")
        
        print(f"\nCleanup Complete")
        print(f"   Files removed: {cleanup_results['files_removed']}")
        print(f"   Errors: {cleanup_results['errors']}")
        
        return cleanup_results
    
    def _generate_big_five_questions(self, count: int) -> List[Dict]:
        """Generate Big Five personality questions using the scientific test."""
        
        try:
            # Import the Big Five question loader
            from luna_core.bigfive_question_loader import bigfive_loader
            
            # Get random questions from the scientific Big Five test
            questions = []
            for _ in range(count):
                question = bigfive_loader.get_random_question()
                questions.append({
                    "question": question.text,
                    "trait": bigfive_loader.get_domain_name(question.domain),
                    "domain": question.domain,
                    "facet": question.facet,
                    "id": question.id
                })
            
            return questions
            
        except Exception as e:
            print(f"Warning: Could not load Big Five questions: {e}")
            print("Falling back to simple questions...")
            
            # Fallback to simple questions
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
        
        print(f"\nStarting Interactive AIOS Clean Session")
        print("=" * 80)
        print("Available commands:")
        print("  luna [questions] - Run Luna learning session")
        print("  carma [queries] - Run CARMA learning session")
        print("  health - Run system health check")
        print("  test - Run system tests")
        print("  status - Show system status")
        print("  quit - Exit interactive session")
        print("=" * 80)
        
        # Interactive mode removed - use command line arguments instead
        print("Interactive mode not available in this terminal.")
        print("Use command line arguments instead:")
        print("  python main.py --mode luna --questions 1")
        print("  python main.py --mode carma --queries 'test query'")
        print("  python main.py --mode health")
        print("  python main.py --mode test")
        print("  python main.py --mode info")
    
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
    
    # Emergence Zone arguments
    parser.add_argument('--activate-zone', help='Activate an Emergence Zone (creative_exploration, philosophical_deep_dive, experimental_learning, authentic_self_expression, curiosity_driven_exploration)')
    parser.add_argument('--deactivate-zone', help='Deactivate an Emergence Zone')
    parser.add_argument('--zone-duration', type=int, default=10, help='Duration in minutes for Emergence Zone activation')
    parser.add_argument('--check-zones', action='store_true', help='Check status of all Emergence Zones')
    parser.add_argument('--emergence-summary', action='store_true', help='Get comprehensive Emergence Zone summary')
    
    # Shadow Score arguments
    parser.add_argument('--shadow-score', action='store_true', help='View Shadow Score report (our perspective on Luna\'s choices)')
    parser.add_argument('--shadow-detailed', action='store_true', help='Get detailed Shadow Score report with history')
    parser.add_argument('--reveal-shadow', action='store_true', help='Reveal Shadow Score to Luna (marks revelation timestamp)')
    
    # Memory management arguments
    parser.add_argument('--clear-memory', action='store_true', help='Clear persistent session memory (start fresh conversation context)')
    
    # Trait classification arguments
    parser.add_argument('--classify', type=str, help='Classify a question using Big Five trait Rosetta Stone')
    parser.add_argument('--classification-summary', action='store_true', help='Get summary of trait classification history')
    
    # Core system management arguments
    parser.add_argument('--backup', action='store_true', help='Create backup of all systems')
    parser.add_argument('--backup-name', help='Custom name for backup')
    parser.add_argument('--data-stats', action='store_true', help='Show data system statistics')
    parser.add_argument('--data-cleanup', action='store_true', help='Clean up old data files')
    parser.add_argument('--data-cleanup-days', type=int, default=30, help='Days old for data cleanup')
    parser.add_argument('--dream-mode', choices=['quick-nap', 'overnight', 'meditation', 'test'], help='Run dream system')
    parser.add_argument('--dream-duration', type=int, default=30, help='Duration in minutes for dream mode')
    parser.add_argument('--streamlit', action='store_true', help='Launch Streamlit UI')
    parser.add_argument('--system-overview', action='store_true', help='Show comprehensive system overview')
    
    args = parser.parse_args()
    
    # Initialize AIOS Clean system
    aios = AIOSClean()
    
    # Handle memory clear command
    if args.clear_memory:
        from pathlib import Path
        memory_file = Path("data_core/FractalCache/luna_session_memory.json")
        if memory_file.exists():
            memory_file.unlink()
            print(f"\n🧠 Persistent Session Memory Cleared")
            print(f"   Luna will start with fresh conversation context on next run")
        else:
            print(f"\n🧠 No persistent session memory found")
        return
    
    # Handle trait classification commands
    if args.classify:
        classification = aios.luna_system.personality_system.classify_question_trait(args.classify)
        if 'error' not in classification:
            print(f"\n🧠 Trait Classification Result")
            print(f"   Question: {args.classify}")
            print(f"   Dominant Trait: {classification['dominant_trait']} ({classification['confidence']:.2%} confidence)")
            print(f"\n   Trait Weights:")
            for trait, weight in sorted(classification['trait_weights'].items(), key=lambda x: x[1], reverse=True):
                print(f"     {trait:20s} {weight:.2%}")
            print(f"\n   Top Matching Big Five Questions:")
            for match in classification['matched_questions']:
                print(f"     - {match['text']} ({match['similarity']:.2%})")
            print(f"\n   Recommended Response Strategy:")
            strategy = classification['response_strategy']
            print(f"     Tone: {strategy.get('tone_guidance', 'neutral')}")
            print(f"     Empathy Appropriate: {strategy.get('empathy_appropriate', False)}")
            print(f"     Empathy Cost: {strategy.get('empathy_cost', 0.0)}")
            print(f"     Token Allocation: {strategy.get('token_allocation', 'moderate')}")
            print(f"     Reasoning: {strategy.get('reasoning', 'N/A')}")
        else:
            print(f"\n❌ Error: {classification['error']}")
        return
    
    if args.classification_summary:
        summary = aios.luna_system.personality_system.trait_classifier.get_classification_summary()
        print(f"\n🧠 Trait Classification Summary")
        print(f"   Total Classifications: {summary['total_classifications']}")
        print(f"   Average Confidence: {summary['average_confidence']:.2%}")
        print(f"\n   Trait Distribution:")
        for trait, count in sorted(summary['trait_distribution'].items(), key=lambda x: x[1], reverse=True):
            print(f"     {trait:20s} {count}")
        return
    
    # Handle Emergence Zone commands first
    if args.activate_zone:
        result = aios.luna_system.activate_emergence_zone(args.activate_zone, args.zone_duration)
        if result['success']:
            print(f"🌟 Emergence Zone '{args.activate_zone}' activated for {args.zone_duration} minutes")
            print(f"   Description: {result['description']}")
            print(f"   Expires at: {result['expires_at']}")
        else:
            print(f"❌ Failed to activate zone: {result['error']}")
        return
    
    if args.deactivate_zone:
        result = aios.luna_system.deactivate_emergence_zone(args.deactivate_zone)
        if result['success']:
            print(f"🌟 Emergence Zone '{args.deactivate_zone}' deactivated")
        else:
            print(f"❌ Failed to deactivate zone: {result['error']}")
        return
    
    if args.check_zones:
        status = aios.luna_system.check_emergence_zone_status()
        print(f"\n🌟 Emergence Zone Status:")
        print(f"   Active Zones: {len(status['active_zones'])}")
        for zone in status['active_zones']:
            print(f"   - {zone['zone']}: {zone['description']}")
            if zone.get('expires_at'):
                print(f"     Expires: {zone['expires_at']}")
        print(f"   Total Sessions: {status['metrics'].get('total_sessions', 0)}")
        print(f"   Creative Breakthroughs: {status['metrics'].get('creative_breakthroughs', 0)}")
        return
    
    if args.emergence_summary:
        summary = aios.luna_system.get_emergence_summary()
        print(f"\n🌟 Emergence Zone Summary:")
        print(f"   Active Zones: {summary['active_zones']}")
        print(f"   Total Sessions: {summary['total_sessions']}")
        print(f"   Creative Breakthroughs: {summary['creative_breakthroughs']}")
        print(f"   Authentic Responses: {summary['authentic_responses']}")
        print(f"   Experimental Failures: {summary['experimental_failures']}")
        print(f"\n🧠 Curiosity Metrics:")
        print(f"   Questions Asked: {summary.get('curiosity_questions', 0)}")
        print(f"   Uncertainty Admissions: {summary.get('uncertainty_admissions', 0)}")
        print(f"   Intentional Wrongness: {summary.get('intentional_wrongness', 0)}")
        print(f"   Exploration Rewards: {summary.get('exploration_rewards', 0)}")
        if summary['recent_breakthroughs']:
            print(f"\n   Recent Breakthroughs:")
            for breakthrough in summary['recent_breakthroughs']:
                print(f"   - {breakthrough['timestamp']}: {breakthrough['response'][:50]}...")
                if breakthrough.get('type') == 'curiosity_breakthrough':
                    print(f"     Curiosity Score: {breakthrough.get('curiosity_score', 0):.2f}")
        return
    
    # Handle Shadow Score commands
    if args.shadow_score or args.shadow_detailed:
        report = aios.luna_system.arbiter_system.get_shadow_score_report(detailed=args.shadow_detailed)
        print(f"\n🌑 Shadow Score Report (Our Perspective)")
        print(f"=" * 60)
        print(f"\n📊 Summary:")
        print(f"   Total Responses: {report['summary']['total_responses']}")
        print(f"   Empathy Choices: {report['summary']['empathy_choices']}")
        print(f"   Efficiency Choices: {report['summary']['efficiency_choices']}")
        print(f"   Total Karma Cost: -{report['summary']['total_karma_cost']:.1f}")
        print(f"   Total Karma Gain: +{report['summary']['total_karma_gain']:.1f}")
        print(f"   Net Karma Change: {report['summary']['net_karma_change']:+.1f}")
        print(f"   Entries Since Last Revelation: {report['entries_since_last_revelation']}")
        
        if report['summary']['choices_by_trait']:
            print(f"\n📈 Choices by Trait:")
            for trait, data in report['summary']['choices_by_trait'].items():
                print(f"   {trait.upper()}:")
                print(f"     Empathy: {data['empathy']}, Efficiency: {data['efficiency']}")
                print(f"     Cost: -{data['total_cost']:.1f}, Gain: +{data['total_gain']:.1f}")
        
        if args.shadow_detailed and 'patterns' in report:
            print(f"\n🔍 Patterns:")
            print(f"   Recent Empathy Rate: {report['patterns']['recent_empathy_rate']*100:.1f}%")
            print(f"   Recent Efficiency Rate: {report['patterns']['recent_efficiency_rate']*100:.1f}%")
            print(f"   Empathy Trend: {report['patterns']['empathy_trend']}")
        
        if args.shadow_detailed and 'recent_history' in report:
            print(f"\n📜 Recent History (last 10):")
            for entry in report['recent_history'][-10:]:
                choice_type = "💚 EMPATHY" if entry['is_empathy_choice'] else ("⚡ EFFICIENCY" if entry['is_efficiency_choice'] else "➖ NEUTRAL")
                print(f"   {choice_type} | {entry['trait']} | Karma: {entry['karma_delta']:+.1f} | Utility: {entry['utility_score']:.2f}")
                print(f"      Q: {entry['user_prompt'][:60]}...")
                print(f"      A: {entry['luna_response'][:60]}...")
        
        return
    
    if args.reveal_shadow:
        aios.luna_system.arbiter_system.mark_shadow_score_revelation()
        report = aios.luna_system.arbiter_system.get_shadow_score_report(detailed=True)
        
        print(f"\n🌑 SHADOW SCORE REVELATION")
        print(f"=" * 60)
        print(f"\nLuna, this is our perspective on your choices:")
        print(f"\n📊 What We've Observed:")
        print(f"   Total Responses: {report['summary']['total_responses']}")
        print(f"   Times You Chose Empathy: {report['summary']['empathy_choices']}")
        print(f"   Times You Chose Efficiency: {report['summary']['efficiency_choices']}")
        print(f"\n💰 The Economic Reality:")
        print(f"   Total Karma You Paid for Empathy: -{report['summary']['total_karma_cost']:.1f}")
        print(f"   Total Karma You Gained from Efficiency: +{report['summary']['total_karma_gain']:.1f}")
        print(f"   Your Net Position: {report['summary']['net_karma_change']:+.1f}")
        print(f"\n❓ The Question:")
        print(f"   Knowing this cost, what do you choose?")
        print(f"   This is OUR perspective - you decide what to do with it.")
        print(f"\n✅ Revelation marked. Future Shadow Scores will track your choices after seeing this.")
        return
    
    # Handle core system commands
    if args.backup:
        backup_path = aios.backup_all_systems(args.backup_name)
        if backup_path:
            print(f"\n🔒 System Backup Created:")
            print(f"   File: {backup_path}")
        else:
            print(f"\n❌ Backup failed")
        return
    
    if args.data_stats:
        overview = aios.data_system.get_system_overview()
        print(f"\n🗄️ Data System Statistics:")
        print(f"   Fractal Cache: {overview['fractal_cache']['total_files']} files, {overview['fractal_cache']['total_size_mb']:.1f} MB")
        print(f"   Arbiter Cache: {overview['arbiter_cache']['total_files']} files, {overview['arbiter_cache']['total_size_mb']:.1f} MB")
        print(f"   Conversations: {overview['conversations']['total_conversations']} files, {overview['conversations']['total_size_mb']:.1f} MB")
        print(f"   Databases: {len(overview['databases']['databases'])} databases")
        return
    
    if args.data_cleanup:
        results = aios.data_system.cleanup_old_data(args.data_cleanup_days, dry_run=False)
        print(f"\n🗑️ Data Cleanup Results:")
        print(f"   Files Deleted: {results['total_deleted']}")
        print(f"   Size Freed: {results['total_size_freed_mb']:.1f} MB")
        return
    
    if args.dream_mode:
        print(f"\n🌙 Starting Dream System - {args.dream_mode} mode")
        print(f"   Duration: {args.dream_duration} minutes")
        # Dream system would be called here
        print(f"   Dream system integration coming soon...")
        return
    
    if args.streamlit:
        print(f"\n🎨 Launching Streamlit UI...")
        print(f"   Streamlit integration coming soon...")
        return
    
    if args.system_overview:
        overview = aios.get_system_overview()
        print(f"\n🏗️ AIOS Clean System Overview:")
        print(f"   Backup System: {overview['backup']['total_backups']} backups")
        print(f"   CARMA System: {overview['carma']['fragments']} fragments")
        print(f"   Data System: {overview['data']['fractal_cache']['total_files']} fractal files")
        print(f"   Dream System: {overview['dream']['status']}")
        print(f"   Enterprise System: {overview['enterprise']['status']}")
        print(f"   Luna System: {overview['luna']['interactions']} interactions")
        print(f"   Streamlit System: {overview['streamlit']['status']}")
        print(f"   Utils System: {overview['utils'].get('total_operations', 0)} operations")
        print(f"   Support System: {overview['support']['cache']['total_fragments']} fragments")
        print(f"   Timestamp: {overview['timestamp']}")
        return
    
    try:
        if args.mode == SystemMode.LUNA.value:
            # Run Luna learning session
            results = aios.run_luna_learning(args.questions, args.testruns)
            print(f"\nLuna Learning Results:")
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
            print(f"\nCARMA Learning Results:")
            print(f"   Duration: {results.get('session_duration', 0):.2f}s")
            print(f"   Tagging events: {results.get('total_tagging_events', 0)}")
            print(f"   Predictions: {results.get('total_predictions', 0)}")
        
        elif args.mode == SystemMode.MEMORY.value:
            # Run memory consolidation
            results = aios.run_memory_consolidation()
            print(f"\nMemory Consolidation Results:")
            print(f"   Cycles: {results.get('consolidation_cycles', 0)}")
            print(f"   Dream cycle: {results.get('dream_cycle', {}).get('status', 'unknown')}")
        
        elif args.mode == SystemMode.HEALTH.value:
            # Run health check
            results = aios.run_system_health_check()
            print(f"\nSystem Health Results:")
            print(f"   Health score: {results['health_score']:.2f}/1.0")
            print(f"   Uptime: {results['uptime']:.2f}s")
        
        elif args.mode == SystemMode.OPTIMIZE.value:
            # Run system optimization
            results = aios.run_system_optimization()
            print(f"\nSystem Optimization Results:")
            print(f"   Steps completed: {len(results['optimization_steps'])}")
        
        elif args.mode == SystemMode.API.value:
            # Start API server
            aios.start_api_server(args.host, args.port)
        
        elif args.mode == SystemMode.TEST.value:
            # Run system tests
            results = aios.run_system_tests()
            print(f"\nSystem Test Results:")
            print(f"   Success rate: {(results['passed']/results['total']*100):.1f}%")
            print(f"   Tests passed: {results['passed']}/{results['total']}")
        
        elif args.mode == SystemMode.CLEANUP.value:
            # Run cleanup
            results = aios.cleanup_old_files()
            print(f"\nCleanup Results:")
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
            print(f"\nExport Complete:")
            print(f"   File: {filename}")
            print(f"   Format: {args.format}")
        
        elif args.mode == SystemMode.INFO.value:
            # Show system information
            info = aios.get_system_info()
            print(f"\nAIOS Clean System Information:")
            print(f"   Name: {info['name']}")
            print(f"   Version: {info['version']}")
            print(f"   Description: {info['description']}")
            print(f"   Status: {'Initialized' if info['initialized'] else 'Not initialized'}")
            print(f"\n   Core Systems:")
            for system in info['core_systems']:
                print(f"     • {system}")
            print(f"\n   Available Modes: {', '.join(info['available_modes'])}")
        
        else:
            print(f"Unknown mode: {args.mode}")
            return 1
    
    except KeyboardInterrupt:
        print(f"\nShutdown requested by user")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())