#!/usr/bin/env python3
"""
BACKUP CORE SYSTEM - Refactored to use shared utilities
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

class BackupCore(CoreSystemBase):
    """
    Backup Core System - Refactored to eliminate duplicate code.
    Uses shared utilities for common functionality.
    """
    
    def __init__(self):
        """Initialize backup core system using shared utilities."""
        # Initialize with shared base functionality
        super().__init__("backup", "backup_core")
        
        # Set up system-specific directories
        self._setup_system_directories()
        
        # Initialize system-specific functionality
        self._initialize_system_specific()
        
        print(f"🔒 Backup Core System Ready")
    
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
        base_info.update({
            "custom_field": "custom_value",
            "special_status": "active"
        })
        
        return base_info

if __name__ == "__main__":
    system = BackupCore()
    print("System initialized successfully!")
    print(f"System info: {system.get_system_info()}")
