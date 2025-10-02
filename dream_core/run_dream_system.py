#!/usr/bin/env python3
"""
Dream System Launcher - Simple way to run the dream processing system
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import the dream system directly
from carma_core.dream_quick_nap_middleware import DreamQuickNapMiddleware

def main():
    """Run the dream system."""
    print("🌙 Starting Dream Quick Nap System...")
    print("This will run a 30-minute dream cycle with REM phases and meditation.")
    print("Press Ctrl+C to stop early.\n")
    
    try:
        # Create and run the dream controller
        controller = DreamQuickNapMiddleware()
        controller.run_quick_nap()
        
    except KeyboardInterrupt:
        print("\n🌙 Dream system stopped by user")
    except Exception as e:
        print(f"\n❌ Error running dream system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
