#!/usr/bin/env python3
"""
DREAM CORE SYSTEM
Self-contained dream and meditation system for AIOS Clean
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

import argparse
from typing import Dict, List, Optional, Any

class DreamCore:
    """
    Self-contained dream and meditation system for AIOS Clean.
    Handles all dream cycles, meditation phases, and memory consolidation.
    """
    
    def __init__(self):
        """Initialize the dream core system."""
        self.dream_dir = Path("dream_core")
        self.dream_dir.mkdir(exist_ok=True)
        
        print(f"🌙 Dream Core System Initialized")
        print(f"   Dream Directory: {self.dream_dir}")
    
    def run_quick_nap(self, duration_minutes: int = 30, dream_cycles: int = 2, meditation_blocks: int = 1, verbose: bool = False) -> Dict[str, Any]:
        """Run a quick nap dream cycle."""
        print(f"🌙 Starting Quick Nap Dream Cycle")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Dream Cycles: {dream_cycles}")
        print(f"   Meditation Blocks: {meditation_blocks}")
        
        # Import and run the dream middleware
        try:
            from dream_quick_nap_middleware import DreamQuickNapMiddleware
            dream_system = DreamQuickNapMiddleware()
            dream_system.run_quick_nap(
                duration_minutes=duration_minutes,
                dream_cycles=dream_cycles,
                meditation_blocks=meditation_blocks,
                verbose=verbose
            )
            return {"status": "success", "duration": duration_minutes}
        except Exception as e:
            print(f"❌ Dream cycle failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_overnight_dream(self, duration_minutes: int = 480, verbose: bool = False) -> Dict[str, Any]:
        """Run an overnight dream cycle."""
        print(f"🌙 Starting Overnight Dream Cycle")
        print(f"   Duration: {duration_minutes} minutes")
        
        # Placeholder for overnight dream implementation
        print("🌙 Overnight mode not yet implemented")
        return {"status": "not_implemented"}
    
    def run_meditation_session(self, duration_minutes: int = 30, verbose: bool = False) -> Dict[str, Any]:
        """Run a meditation session."""
        print(f"🧘 Starting Meditation Session")
        print(f"   Duration: {duration_minutes} minutes")
        
        try:
            from meditation_controller import MeditationController
            controller = MeditationController()
            controller.run_meditation(
                duration_minutes=duration_minutes,
                verbose=verbose
            )
            return {"status": "success", "duration": duration_minutes}
        except Exception as e:
            print(f"❌ Meditation session failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_test_mode(self, duration_minutes: int = 2, verbose: bool = True) -> Dict[str, Any]:
        """Run test mode for validation."""
        print(f"🧪 Starting Dream System Test")
        print(f"   Duration: {duration_minutes} minutes")
        
        return self.run_quick_nap(
            duration_minutes=duration_minutes,
            dream_cycles=1,
            meditation_blocks=1,
            verbose=verbose
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current dream system status."""
        return {
            "status": "ready",
            "dream_directory": str(self.dream_dir),
            "available_modes": ["quick-nap", "overnight", "meditation", "test"],
            "last_run": None  # Would track last run time
        }

def main():
    parser = argparse.ArgumentParser(description="AIOS Dream Core System")
    
    # Main operation modes
    parser.add_argument('--mode', '-m', 
                       choices=['quick-nap', 'overnight', 'meditation', 'test'],
                       default='quick-nap',
                       help='Dream operation mode (default: quick-nap)')
    
    # Duration options
    parser.add_argument('--duration', '-d',
                       type=int,
                       default=30,
                       help='Duration in minutes (default: 30)')
    
    # Dream cycle options
    parser.add_argument('--cycles', '-c',
                       type=int,
                       default=2,
                       help='Number of dream cycles per REM phase (default: 2)')
    
    parser.add_argument('--meditation-blocks', '-mb',
                       type=int,
                       default=1,
                       help='Number of meditation blocks per cycle (default: 1)')
    
    # Advanced options
    parser.add_argument('--max-fragments', '-mf',
                       type=int,
                       default=100,
                       help='Maximum fragments to process (default: 100)')
    
    parser.add_argument('--consolidation-threshold', '-ct',
                       type=float,
                       default=0.8,
                       help='Memory consolidation threshold (default: 0.8)')
    
    # Debug options
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose logging')
    
    parser.add_argument('--debug',
                       action='store_true',
                       help='Enable debug mode')
    
    # Output options
    parser.add_argument('--output-dir', '-o',
                       type=str,
                       default='log',
                       help='Output directory for logs (default: log)')
    
    parser.add_argument('--no-log',
                       action='store_true',
                       help='Disable logging to files')
    
    args = parser.parse_args()
    
    print("🌙 AIOS Dream Core System")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    print(f"Duration: {args.duration} minutes")
    print(f"Dream Cycles: {args.cycles}")
    print(f"Meditation Blocks: {args.meditation_blocks}")
    print(f"Max Fragments: {args.max_fragments}")
    print(f"Verbose: {args.verbose}")
    print("=" * 50)
    
    # Import and run the appropriate system
    if args.mode == 'quick-nap':
        from dream_quick_nap_middleware import DreamQuickNapMiddleware
        dream_system = DreamQuickNapMiddleware()
        dream_system.run_quick_nap(
            duration_minutes=args.duration,
            dream_cycles=args.cycles,
            meditation_blocks=args.meditation_blocks,
            verbose=args.verbose
        )
    elif args.mode == 'overnight':
        print("🌙 Overnight mode not yet implemented")
        print("Use quick-nap mode for now")
        sys.exit(1)
    elif args.mode == 'meditation':
        from meditation_controller import MeditationController
        controller = MeditationController()
        controller.run_meditation(
            duration_minutes=args.duration,
            verbose=args.verbose
        )
    elif args.mode == 'test':
        print("🧪 Test mode - running quick validation")
        from dream_quick_nap_middleware import DreamQuickNapMiddleware
        dream_system = DreamQuickNapMiddleware()
        dream_system.run_quick_nap(
            duration_minutes=2,  # Short test
            dream_cycles=1,
            meditation_blocks=1,
            verbose=True
        )
    
    print("🌙 Dream Core System Complete")

if __name__ == "__main__":
    main()
