#!/usr/bin/env python3
"""
HYBRID DATA CORE SYSTEM
Python-Rust hybrid implementation for high-performance data operations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils_core.rust_bridge import RustBridge, MultiLanguageCore
from data_core.data_core import DataCore
from typing import Dict, List, Optional, Any

class HybridDataCore(MultiLanguageCore):
    """
    Hybrid data core that uses Rust when available, Python as fallback.
    Provides identical interface to original DataCore.
    """
    
    def __init__(self, data_dir: str = "data_core"):
        self.data_dir = Path(data_dir)
        
        # Initialize Python implementation
        python_data = DataCore()
        
        # Initialize Rust bridge
        rust_bridge = RustBridge("data", str(self.data_dir / "rust_data"))
        
        # Try to compile and load Rust module
        if rust_bridge.compile_rust_module():
            rust_bridge.load_rust_module()
        
        # Initialize multi-language core
        super().__init__("data", python_data, rust_bridge)
        
        # Set python_impl for compatibility
        self.python_impl = python_data
        
        # Expose key attributes for compatibility
        self.data_dir = Path(data_dir)
        self.fractal_cache_dir = self.data_dir / "FractalCache"
        self.arbiter_cache_dir = self.data_dir / "ArbiterCache"
        self.conversations_dir = self.data_dir / "conversations"
        self.config_dir = self.data_dir / "config"
        self.database_dir = self.data_dir / "AIOS_Database" / "database"
        self.logs_dir = self.data_dir / "logs"
        self.temp_dir = self.data_dir / "temp"
        self.cache_dir = self.data_dir / "cache"
        self.exports_dir = self.data_dir / "exports"
        self.imports_dir = self.data_dir / "imports"
        self.analytics_dir = self.data_dir / "analytics"
        
        # Initialize Rust core instance if available
        self.rust_core_instance = None
        if self.current_implementation == "rust":
            try:
                RustDataCore = self.rust_bridge.get_rust_class("PyRustDataCore")
                if RustDataCore:
                    self.rust_core_instance = RustDataCore(str(self.data_dir))
                else:
                    print("⚠️ PyRustDataCore class not found in module. Falling back to Python.")
                    self.switch_to_python()
            except Exception as e:
                print(f"❌ Failed to initialize Rust data core instance: {e}. Falling back to Python.")
                self.switch_to_python()
        
        print(f"🔀 Hybrid Data Core Initialized")
        print(f"   Current implementation: {self.current_implementation.upper()}")
        print(f"   Data directory: {self.data_dir}")
    
    def get_fractal_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the FractalCache."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"🔍 Getting fractal cache stats using RUST implementation...")
                result = self.rust_core_instance.get_fractal_cache_stats()
                
                # Convert Rust struct to Python dict
                stats_dict = {
                    "total_files": getattr(result, 'total_files', 0),
                    "total_dirs": getattr(result, 'total_dirs', 0),
                    "total_size_bytes": getattr(result, 'total_size_bytes', 0),
                    "total_size_mb": getattr(result, 'total_size_mb', 0.0),
                    "last_modified": getattr(result, 'last_modified', None),
                    "file_types": dict(getattr(result, 'file_types', {})),
                    "implementation": "rust"
                }
                
                print(f"✅ Rust fractal cache stats retrieved")
                return stats_dict
                
            except Exception as e:
                print(f"❌ Rust fractal cache stats failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"🔍 Getting fractal cache stats using PYTHON implementation...")
        return self.python_impl.get_fractal_cache_stats()
    
    def get_arbiter_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the ArbiterCache."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"🔍 Getting arbiter cache stats using RUST implementation...")
                result = self.rust_core_instance.get_arbiter_cache_stats()
                
                # Convert Rust struct to Python dict
                stats_dict = {
                    "total_files": getattr(result, 'total_files', 0),
                    "total_dirs": getattr(result, 'total_dirs', 0),
                    "total_size_bytes": getattr(result, 'total_size_bytes', 0),
                    "total_size_mb": getattr(result, 'total_size_mb', 0.0),
                    "last_modified": getattr(result, 'last_modified', None),
                    "file_types": dict(getattr(result, 'file_types', {})),
                    "implementation": "rust"
                }
                
                print(f"✅ Rust arbiter cache stats retrieved")
                return stats_dict
                
            except Exception as e:
                print(f"❌ Rust arbiter cache stats failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"🔍 Getting arbiter cache stats using PYTHON implementation...")
        return self.python_impl.get_arbiter_cache_stats()
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about conversations."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"🔍 Getting conversation stats using RUST implementation...")
                result = self.rust_core_instance.get_conversation_stats()
                
                # Convert Rust struct to Python dict
                stats_dict = {
                    "total_files": getattr(result, 'total_files', 0),
                    "total_dirs": getattr(result, 'total_dirs', 0),
                    "total_size_bytes": getattr(result, 'total_size_bytes', 0),
                    "total_size_mb": getattr(result, 'total_size_mb', 0.0),
                    "last_modified": getattr(result, 'last_modified', None),
                    "file_types": dict(getattr(result, 'file_types', {})),
                    "implementation": "rust"
                }
                
                print(f"✅ Rust conversation stats retrieved")
                return stats_dict
                
            except Exception as e:
                print(f"❌ Rust conversation stats failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"🔍 Getting conversation stats using PYTHON implementation...")
        return self.python_impl.get_conversation_stats()
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about databases."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"🔍 Getting database stats using RUST implementation...")
                result = self.rust_core_instance.get_database_stats()
                
                # Convert Rust struct to Python dict
                stats_dict = {
                    "total_files": getattr(result, 'total_files', 0),
                    "total_dirs": getattr(result, 'total_dirs', 0),
                    "total_size_bytes": getattr(result, 'total_size_bytes', 0),
                    "total_size_mb": getattr(result, 'total_size_mb', 0.0),
                    "last_modified": getattr(result, 'last_modified', None),
                    "file_types": dict(getattr(result, 'file_types', {})),
                    "implementation": "rust"
                }
                
                print(f"✅ Rust database stats retrieved")
                return stats_dict
                
            except Exception as e:
                print(f"❌ Rust database stats failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"🔍 Getting database stats using PYTHON implementation...")
        return self.python_impl.get_database_stats()
    
    def export_data(self, data_type: str, target_format: str = "json", 
                   filter_criteria: Dict[str, Any] = None) -> Dict[str, Any]:
        """Export data with Rust acceleration when available."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"📤 Exporting data using RUST implementation...")
                
                # Determine source directory based on data_type
                source_dir_map = {
                    "fractal_cache": str(self.fractal_cache_dir),
                    "arbiter_cache": str(self.arbiter_cache_dir),
                    "conversations": str(self.conversations_dir),
                    "database": str(self.database_dir),
                }
                
                source_dir = source_dir_map.get(data_type, str(self.data_dir))
                export_path = str(self.exports_dir / f"{data_type}_export_{int(time.time())}.json")
                
                # Convert filter criteria to string for Rust
                filter_str = None
                if filter_criteria:
                    import json
                    filter_str = json.dumps(filter_criteria)
                
                result = self.rust_core_instance.export_to_json(source_dir, export_path, filter_str)
                
                # Convert Rust result to Python dict
                export_result = {
                    "success": getattr(result, 'success', False),
                    "files_processed": getattr(result, 'files_processed', 0),
                    "bytes_processed": getattr(result, 'bytes_processed', 0),
                    "export_path": getattr(result, 'export_path', ''),
                    "time_taken_ms": getattr(result, 'time_taken_ms', 0),
                    "implementation": "rust"
                }
                
                if export_result["success"]:
                    print(f"✅ Rust export completed successfully")
                    print(f"   Files processed: {export_result['files_processed']}")
                    print(f"   Bytes processed: {export_result['bytes_processed']}")
                    print(f"   Time taken: {export_result['time_taken_ms'] / 1000:.2f}s")
                    print(f"   Export path: {export_result['export_path']}")
                else:
                    error_message = getattr(result, 'error_message', "Unknown Rust export error")
                    print(f"❌ Rust export failed: {error_message}")
                
                return export_result
                
            except Exception as e:
                print(f"❌ Rust export failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"📤 Exporting data using PYTHON implementation...")
        return self.python_impl.export_data(data_type, target_format, filter_criteria)
    
    def cleanup_old_data(self, days_old: int = 30, dry_run: bool = True) -> Dict[str, Any]:
        """Clean up old data files with Rust acceleration."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"🧹 Cleaning up old data using RUST implementation...")
                cleaned_files = self.rust_core_instance.cleanup_old_data(days_old, dry_run)
                
                cleanup_result = {
                    "files_removed": len(cleaned_files),
                    "files_list": cleaned_files,
                    "days_old": days_old,
                    "dry_run": dry_run,
                    "implementation": "rust"
                }
                
                print(f"✅ Rust cleanup completed")
                print(f"   Files {'would be' if dry_run else ''} removed: {len(cleaned_files)}")
                
                return cleanup_result
                
            except Exception as e:
                print(f"❌ Rust cleanup failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"🧹 Cleaning up old data using PYTHON implementation...")
        return self.python_impl.cleanup_old_data(days_old, dry_run)
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"📊 Getting system overview using RUST implementation...")
                overview = self.rust_core_instance.get_system_overview()
                
                # Convert Rust JSON string to Python dict
                import json
                overview_dict = json.loads(overview)
                overview_dict["implementation"] = "rust"
                
                print(f"✅ Rust system overview retrieved")
                return overview_dict
                
            except Exception as e:
                print(f"❌ Rust system overview failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"📊 Getting system overview using PYTHON implementation...")
        return self.python_impl.get_system_overview()
    
    def get_pipeline_metrics(self) -> Dict[str, Any]:
        """Get comprehensive data pipeline metrics."""
        if self.current_implementation == "rust" and self.rust_core_instance:
            try:
                print(f"📈 Getting pipeline metrics using RUST implementation...")
                metrics = self.rust_core_instance.get_pipeline_metrics()
                
                # Convert Rust struct to Python dict
                metrics_dict = {
                    "total_ingestions": getattr(metrics, 'total_ingestions', 0),
                    "total_exports": getattr(metrics, 'total_exports', 0),
                    "last_ingestion": getattr(metrics, 'last_ingestion', None),
                    "last_export": getattr(metrics, 'last_export', None),
                    "cache_hit_rate": getattr(metrics, 'cache_hit_rate', 0.0),
                    "implementation": "rust"
                }
                
                print(f"✅ Rust pipeline metrics retrieved")
                return metrics_dict
                
            except Exception as e:
                print(f"❌ Rust pipeline metrics failed: {e}")
                print("   Falling back to Python implementation...")
                self.switch_to_python()
        
        print(f"📈 Getting pipeline metrics using PYTHON implementation...")
        return self.python_impl.get_pipeline_metrics()
    
    def get_all_files(self):
        """Get all files in the data directory (compatibility method)."""
        import os
        from pathlib import Path
        
        all_files = []
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                all_files.append(Path(root) / file)
        return all_files
    
    # Essential methods for compatibility
    def get_current_implementation(self) -> str:
        """Get the current implementation (Python or Rust)."""
        return self.current_implementation
    
    def switch_to_rust(self) -> bool:
        """Switch to Rust implementation if available."""
        if self.rust_bridge.is_available():
            self.current_implementation = "rust"
            try:
                RustDataCore = self.rust_bridge.get_rust_class("PyRustDataCore")
                if RustDataCore:
                    self.rust_core_instance = RustDataCore(str(self.data_dir))
                else:
                    print("⚠️ PyRustDataCore class not found in module. Staying on Python.")
                    return False
            except Exception as e:
                print(f"❌ Failed to initialize Rust data core instance: {e}. Staying on Python.")
                return False
            print(f"   Switched to Rust implementation for {self.core_name}")
            return True
        print(f"   Rust implementation not available for {self.core_name}. Staying on Python.")
        return False

    def switch_to_python(self) -> bool:
        """Switch to Python implementation."""
        self.current_implementation = "python"
        print(f"   Switched to Python implementation for {self.core_name}")
        return True
    
    # Delegate other methods to Python implementation for now
    def __getattr__(self, name):
        """Delegate any missing attributes to the Python implementation."""
        # Prevent recursion by checking if we're accessing protected attributes
        if name.startswith('_') or name in ['python_impl', 'rust_bridge', 'current_implementation', 'core_name', 'data_dir']:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        # Only delegate to python_impl if it's not one of our core attributes
        if hasattr(self.python_impl, name):
            return getattr(self.python_impl, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# Import time for export_data
import time
