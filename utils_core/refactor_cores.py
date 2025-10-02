#!/usr/bin/env python3
"""
REFACTOR CORES - Script to help refactor existing cores to use shared utilities
This script demonstrates how to eliminate duplicate code across core files.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# CRITICAL: Import Unicode safety layer FIRST
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

from utils_core.core_utilities import CoreSystemBase, CoreSystemManager
from utils_core.system_initializer import SystemInitializer

class RefactorAnalyzer:
    """Analyzes existing cores and suggests refactoring opportunities."""
    
    def __init__(self):
        self.core_files = [
            "backup_core/backup_core.py",
            "data_core/data_core.py", 
            "dream_core/dream_core.py",
            "enterprise_core/enterprise_core.py",
            "streamlit_core/streamlit_core.py",
            "utils_core/utils_core.py"
        ]
        
        self.duplicate_patterns = {
            "initialization_messages": [
                "print.*System.*Initialized",
                "print.*Core.*System.*Initialized"
            ],
            "directory_creation": [
                "mkdir.*exist_ok",
                "mkdir.*parents.*True"
            ],
            "argument_parsers": [
                "argparse.ArgumentParser",
                "add_argument"
            ],
            "system_info_methods": [
                "get_system_info",
                "get_system_status", 
                "get_system_metrics"
            ]
        }
    
    def analyze_duplicates(self) -> Dict[str, List[str]]:
        """Analyze duplicate patterns across core files."""
        duplicates = {}
        
        for pattern_type, patterns in self.duplicate_patterns.items():
            duplicates[pattern_type] = []
            
            for core_file in self.core_files:
                if Path(core_file).exists():
                    with open(core_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in patterns:
                        if pattern in content:
                            duplicates[pattern_type].append(f"{core_file}: {pattern}")
        
        return duplicates
    
    def generate_refactor_suggestions(self) -> List[str]:
        """Generate suggestions for refactoring."""
        suggestions = [
            "1. Replace individual initialization messages with CoreSystemBase",
            "2. Use SystemInitializer for standardized directory creation",
            "3. Create shared argument parser utilities",
            "4. Standardize system info methods across all cores",
            "5. Move common JSON handling to shared utilities",
            "6. Create shared logging utilities",
            "7. Standardize error handling patterns",
            "8. Create shared configuration management"
        ]
        
        return suggestions
    
    def create_refactored_example(self, core_name: str) -> str:
        """Create an example of refactored core code."""
        emoji = CoreSystemManager.get_system_emoji(core_name)
        
        refactored_code = f'''#!/usr/bin/env python3
"""
{core_name.upper()} CORE SYSTEM - Refactored to use shared utilities
Eliminates duplicate code by using CoreSystemBase and shared utilities.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# CRITICAL: Import Unicode safety layer FIRST
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
from utils_core.core_utilities import CoreSystemBase, CoreSystemManager
from utils_core.system_initializer import SystemInitializer
setup_unicode_safe_output()

class {core_name.title()}Core(CoreSystemBase):
    """
    {core_name.title()} Core System - Refactored to eliminate duplicate code.
    Uses shared utilities for common functionality.
    """
    
    def __init__(self):
        """Initialize {core_name} core system using shared utilities."""
        # Initialize with shared base functionality
        super().__init__("{core_name}", "{core_name}_core")
        
        # Set up system-specific directories
        self._setup_system_directories()
        
        # Initialize system-specific functionality
        self._initialize_system_specific()
        
        print(f"{emoji} {core_name.title()} Core System Ready")
    
    def _setup_system_directories(self):
        """Set up system-specific directories."""
        # Add system-specific directory creation here
        # Example: self.create_subdirectory("special_dir")
        pass
    
    def _initialize_system_specific(self):
        """Initialize system-specific functionality."""
        # Add system-specific initialization here
        pass
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information using shared utilities."""
        base_info = super().get_system_info()
        
        # Add system-specific information
        base_info.update({{
            "custom_field": "custom_value",
            "special_status": "active"
        }})
        
        return base_info

if __name__ == "__main__":
    system = {core_name.title()}Core()
    print("System initialized successfully!")
    print(f"System info: {{system.get_system_info()}}")
'''
        
        return refactored_code

def main():
    """Main function to demonstrate refactoring analysis."""
    print("🔧 AIOS Core Refactoring Analysis")
    print("=" * 50)
    
    analyzer = RefactorAnalyzer()
    
    # Analyze duplicates
    print("\n📊 Duplicate Pattern Analysis:")
    duplicates = analyzer.analyze_duplicates()
    
    for pattern_type, matches in duplicates.items():
        print(f"\n{pattern_type.upper()}:")
        for match in matches:
            print(f"  - {match}")
    
    # Generate suggestions
    print("\n💡 Refactoring Suggestions:")
    suggestions = analyzer.generate_refactor_suggestions()
    for suggestion in suggestions:
        print(f"  {suggestion}")
    
    # Create refactored example
    print("\n📝 Refactored Example (backup_core):")
    refactored_example = analyzer.create_refactored_example("backup")
    
    # Save example to file
    example_file = Path("utils_core/refactored_example_backup_core.py")
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write(refactored_example)
    
    print(f"  Example saved to: {example_file}")
    
    print("\n✅ Refactoring analysis complete!")
    print("\nNext steps:")
    print("1. Review the duplicate patterns found")
    print("2. Apply refactoring suggestions to each core")
    print("3. Test each refactored core")
    print("4. Update main.py to use refactored cores")

if __name__ == "__main__":
    main()
