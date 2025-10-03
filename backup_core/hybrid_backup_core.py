#!/usr/bin/env python3
"""
HYBRID BACKUP CORE - Multi-Language Backup System
Automatically uses Rust implementation when available, falls back to Python
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add utils_core to path for rust_bridge
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.rust_bridge import RustBridge, MultiLanguageCore

# Import original Python implementation
from .backup_core import BackupCore

class HybridBackupCore(MultiLanguageCore):
    """
    Hybrid backup core that uses Rust when available, Python as fallback.
    Provides identical interface to original BackupCore.
    """
    
    def __init__(self):
        """Initialize hybrid backup core."""
        # Initialize Python implementation
        python_backup = BackupCore()
        
        # Initialize Rust bridge
        rust_bridge = None
        try:
            rust_path = Path(__file__).parent / "rust_backup"
            if rust_path.exists():
                rust_bridge = RustBridge("backup", str(rust_path))
                
                # Try to compile and load Rust module
                if rust_bridge.compile_rust_module():
                    rust_bridge.load_rust_module()
        except Exception as e:
            print(f"⚠️ Rust backup initialization failed: {e}")
            print("   Falling back to Python implementation")
        
        # Initialize multi-language core
        super().__init__("backup", python_backup, rust_bridge)
        
        # Expose backup directory paths for compatibility
        self.backup_dir = python_backup.backup_dir
        self.active_backup_dir = python_backup.active_backup_dir
        self.archive_backup_dir = python_backup.archive_backup_dir
        self.backup_tracking_file = python_backup.backup_tracking_file
        self.file_checksums_file = python_backup.file_checksums_file
        self.last_backup_timestamp = python_backup.last_backup_timestamp
        self.file_checksums = python_backup.file_checksums
        
        print(f"🔀 Hybrid Backup Core Initialized")
        print(f"   Current implementation: {self.current_implementation.upper()}")
        print(f"   Active Backup: {self.active_backup_dir}")
        print(f"   Archive Backup: {self.archive_backup_dir}")
    
    def create_backup(self, 
                     backup_name: Optional[str] = None,
                     include_data: bool = True,
                     include_logs: bool = True,
                     include_config: bool = True,
                     incremental: bool = True) -> str:
        """
        Create/update backup using current implementation (Rust or Python).
        
        Args:
            backup_name: Name for the backup (defaults to 'active')
            include_data: Include data directories
            include_logs: Include log files
            include_config: Include configuration files
            incremental: Only backup changed files since last backup
            
        Returns:
            Path to the active backup directory
        """
        print(f"🔄 Creating backup using {self.current_implementation.upper()} implementation...")
        
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            return self._create_rust_backup(include_data, include_logs, include_config)
        else:
            return self._create_python_backup(backup_name, include_data, include_logs, include_config, incremental)
    
    def _create_rust_backup(self, include_data: bool, include_logs: bool, include_config: bool) -> str:
        """Create backup using Rust implementation."""
        try:
            # Get Rust class
            PyRustBackupCore = self.rust_bridge.get_rust_class("PyRustBackupCore")
            if PyRustBackupCore is None:
                raise Exception("Rust backup class not available")
            
            # Create Rust instance
            rust_backup = PyRustBackupCore(str(self.backup_dir))
            
            # Perform backup
            result = rust_backup.create_backup(include_data, include_logs, include_config)
            
            # Access attributes using getattr for compatibility
            success = getattr(result, 'success', False)
            if success:
                files_processed = getattr(result, 'files_processed', 0)
                files_changed = getattr(result, 'files_changed', 0)
                time_taken_ms = getattr(result, 'time_taken_ms', 0)
                backup_path = getattr(result, 'backup_path', '')
                
                print(f"✅ Rust backup completed successfully")
                print(f"   Files processed: {files_processed}")
                print(f"   Files changed: {files_changed}")
                print(f"   Time taken: {time_taken_ms / 1000:.2f}s")
                print(f"   Backup path: {backup_path}")
                return backup_path
            else:
                error_message = getattr(result, 'error_message', "Unknown Rust backup error")
                raise Exception(error_message)
                
        except Exception as e:
            print(f"❌ Rust backup failed: {e}")
            print("   Falling back to Python implementation...")
            self.switch_to_python()
            return self._create_python_backup("active", include_data, include_logs, include_config, True)
    
    def _create_python_backup(self, backup_name: Optional[str], include_data: bool, 
                            include_logs: bool, include_config: bool, incremental: bool) -> str:
        """Create backup using Python implementation."""
        # Get Python implementation
        python_backup = self.python_implementation
        return python_backup.create_backup(backup_name, include_data, include_logs, include_config, incremental)
    
    def benchmark_backup(self, include_data: bool = True, include_logs: bool = True, 
                        include_config: bool = True) -> Dict[str, Any]:
        """
        Benchmark both Python and Rust backup implementations.
        
        Returns:
            Dictionary with performance comparison data
        """
        print(f"⚡ Running backup performance benchmark...")
        
        def python_backup_func():
            return self.python_implementation.create_backup(
                "benchmark", include_data, include_logs, include_config, True
            )
        
        def rust_backup_func():
            if not (self.rust_bridge and self.rust_bridge.is_available()):
                raise Exception("Rust implementation not available")
            
            PyRustBackupCore = self.rust_bridge.get_rust_class("PyRustBackupCore")
            if PyRustBackupCore is None:
                raise Exception("Rust backup class not available")
            
            rust_backup = PyRustBackupCore(str(self.backup_dir))
            result = rust_backup.create_backup(include_data, include_logs, include_config)
            
            if not result.success:
                raise Exception(result.error_message or "Rust backup failed")
            
            return result.backup_path
        
        return self.benchmark(include_data, include_logs, include_config)
    
    def switch_implementation(self, implementation: str) -> bool:
        """
        Switch between Python and Rust implementations.
        
        Args:
            implementation: 'python' or 'rust'
            
        Returns:
            True if switch successful, False otherwise
        """
        if implementation.lower() == "rust":
            return self.switch_to_rust()
        elif implementation.lower() == "python":
            self.switch_to_python()
            return True
        else:
            print(f"❌ Invalid implementation: {implementation}")
            print("   Valid options: 'python', 'rust'")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get status information about the hybrid backup core.
        
        Returns:
            Dictionary with status information
        """
        return {
            "core_name": "hybrid_backup",
            "current_implementation": self.current_implementation,
            "rust_available": self.rust_bridge and self.rust_bridge.is_available(),
            "python_available": True,
            "backup_dir": str(self.backup_dir),
            "active_backup_dir": str(self.active_backup_dir),
            "archive_backup_dir": str(self.archive_backup_dir),
            "last_backup_timestamp": self.last_backup_timestamp,
            "file_checksums_count": len(self.file_checksums)
        }
