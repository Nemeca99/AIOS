#!/usr/bin/env python3
"""
UTILS CORE SYSTEM
Central utility hub for all AIOS core files
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
from utils_core.core_utilities import CoreSystemBase, CoreSystemManager
from utils_core.system_initializer import SystemInitializer, initialize_core_system
setup_unicode_safe_output()

import os
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

class UtilsCore(CoreSystemBase):
    """
    Central utility hub for all AIOS core files.
    Provides common functionality, data validation, and inter-core communication utilities.
    """
    
    def __init__(self):
        """Initialize the utils core system."""
        # Initialize with shared base functionality
        super().__init__("utils", "utils_core")
        
        # Initialize utility tracking
        self.usage_stats = self._load_usage_stats()
        self.utility_registry = self._load_utility_registry()
        
        print(f"   Registered Utilities: {len(self.utility_registry)}")
    
    # === DATA VALIDATION & SANITIZATION ===
    
    def validate_data(self, data: Any, data_type: str = "general") -> Dict[str, Any]:
        """
        Validate data based on type and return validation results.
        
        Args:
            data: Data to validate
            data_type: Type of data (json, text, file_path, etc.)
            
        Returns:
            Dict with validation results
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "data_type": data_type,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if data_type == "json":
                if isinstance(data, str):
                    json.loads(data)
                elif not isinstance(data, (dict, list)):
                    result["valid"] = False
                    result["errors"].append("Invalid JSON data type")
                    
            elif data_type == "file_path":
                path = Path(data)
                if not path.exists():
                    result["warnings"].append(f"File path does not exist: {data}")
                    
            elif data_type == "text":
                if not isinstance(data, str):
                    result["valid"] = False
                    result["errors"].append("Text data must be string")
                elif len(data.strip()) == 0:
                    result["warnings"].append("Text data is empty")
                    
        except json.JSONDecodeError as e:
            result["valid"] = False
            result["errors"].append(f"JSON decode error: {e}")
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Validation error: {e}")
        
        # Track usage
        self._track_utility_usage("validate_data", result["valid"])
        
        return result
    
    def sanitize_input(self, input_data: str, max_length: int = 10000) -> str:
        """
        Sanitize user input to prevent injection attacks and ensure safety.
        
        Args:
            input_data: Raw input data
            max_length: Maximum allowed length
            
        Returns:
            Sanitized input data
        """
        if not isinstance(input_data, str):
            input_data = str(input_data)
        
        # Basic sanitization
        sanitized = input_data.strip()
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            self._track_utility_usage("sanitize_input", False, "truncated")
        
        self._track_utility_usage("sanitize_input", True)
        return sanitized
    
    # === FILE OPERATIONS ===
    
    def safe_file_read(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        Safely read a file with error handling and encoding safety.
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            Dict with file contents and metadata
        """
        result = {
            "success": False,
            "content": None,
            "error": None,
            "file_size": 0,
            "encoding": encoding,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            path = Path(file_path)
            if not path.exists():
                result["error"] = f"File not found: {file_path}"
                return result
            
            # Check file size (prevent reading huge files)
            file_size = path.stat().st_size
            result["file_size"] = file_size
            
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                result["error"] = f"File too large: {file_size / (1024*1024):.1f}MB"
                return result
            
            # Read file with encoding safety
            with open(path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
                result["content"] = content
                result["success"] = True
                
        except Exception as e:
            result["error"] = str(e)
        
        self._track_utility_usage("safe_file_read", result["success"])
        return result
    
    def safe_file_write(self, file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        Safely write to a file with backup and atomic operations.
        
        Args:
            file_path: Path to file
            content: Content to write
            encoding: File encoding
            
        Returns:
            Dict with write results
        """
        result = {
            "success": False,
            "bytes_written": 0,
            "error": None,
            "backup_created": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            path = Path(file_path)
            
            # Create backup if file exists
            if path.exists():
                backup_path = path.with_suffix(f"{path.suffix}.backup")
                path.rename(backup_path)
                result["backup_created"] = True
            
            # Write to temporary file first (atomic operation)
            temp_path = path.with_suffix(f"{path.suffix}.tmp")
            with open(temp_path, 'w', encoding=encoding, errors='replace') as f:
                bytes_written = f.write(content)
                result["bytes_written"] = bytes_written
            
            # Atomic rename
            temp_path.rename(path)
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            # Restore backup if write failed
            if result["backup_created"]:
                backup_path = path.with_suffix(f"{path.suffix}.backup")
                if backup_path.exists():
                    backup_path.rename(path)
        
        self._track_utility_usage("safe_file_write", result["success"])
        return result
    
    # === HASHING & IDENTIFICATION ===
    
    def generate_file_hash(self, file_path: Union[str, Path], algorithm: str = "sha256") -> str:
        """
        Generate hash for a file.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256)
            
        Returns:
            Hash string
        """
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            self._track_utility_usage("generate_file_hash", True)
            return hash_obj.hexdigest()
            
        except Exception as e:
            self._track_utility_usage("generate_file_hash", False, str(e))
            return ""
    
    def generate_content_id(self, content: str, prefix: str = "GEN") -> str:
        """
        Generate unique ID for content based on hash and timestamp.
        
        Args:
            content: Content to generate ID for
            prefix: ID prefix
            
        Returns:
            Unique ID string
        """
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:8]
        timestamp = int(time.time())
        random_part = os.urandom(4).hex()[:4]
        
        content_id = f"{prefix}{timestamp}_{content_hash}_{random_part}"
        self._track_utility_usage("generate_content_id", True)
        return content_id
    
    # === INTER-CORE COMMUNICATION ===
    
    def create_core_message(self, source_core: str, target_core: str, 
                          message_type: str, data: Any, priority: int = 1) -> Dict[str, Any]:
        """
        Create standardized message for inter-core communication.
        
        Args:
            source_core: Source core system
            target_core: Target core system
            message_type: Type of message
            data: Message data
            priority: Message priority (1-10)
            
        Returns:
            Standardized message dict
        """
        message = {
            "message_id": self.generate_content_id(f"{source_core}_{target_core}_{message_type}"),
            "source_core": source_core,
            "target_core": target_core,
            "message_type": message_type,
            "data": data,
            "priority": min(max(priority, 1), 10),
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self._track_utility_usage("create_core_message", True)
        return message
    
    def validate_core_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate inter-core message format and content.
        
        Args:
            message: Message to validate
            
        Returns:
            Validation results
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        required_fields = ["message_id", "source_core", "target_core", "message_type", "data", "timestamp"]
        
        for field in required_fields:
            if field not in message:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")
        
        if "priority" in message:
            if not isinstance(message["priority"], int) or not (1 <= message["priority"] <= 10):
                result["warnings"].append("Invalid priority value (should be 1-10)")
        
        self._track_utility_usage("validate_core_message", result["valid"])
        return result
    
    # === SYSTEM MONITORING ===
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "utility_usage": self.usage_stats,
            "registered_utilities": len(self.utility_registry),
            "system_uptime": self._get_system_uptime(),
            "memory_usage": self._get_memory_usage(),
            "disk_usage": self._get_disk_usage()
        }
    
    def cleanup_old_data(self, days_old: int = 30) -> Dict[str, Any]:
        """
        Clean up old utility data and logs.
        
        Args:
            days_old: Age threshold for cleanup
            
        Returns:
            Cleanup results
        """
        cleanup_result = {
            "files_deleted": 0,
            "bytes_freed": 0,
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            threshold_time = time.time() - (days_old * 24 * 60 * 60)
            
            # Clean up old log files
            for log_file in self.system_dir.glob("*.log"):
                if log_file.stat().st_mtime < threshold_time:
                    file_size = log_file.stat().st_size
                    log_file.unlink()
                    cleanup_result["files_deleted"] += 1
                    cleanup_result["bytes_freed"] += file_size
            
            # Clean up old temporary files
            for temp_file in self.system_dir.glob("*.tmp"):
                if temp_file.stat().st_mtime < threshold_time:
                    file_size = temp_file.stat().st_size
                    temp_file.unlink()
                    cleanup_result["files_deleted"] += 1
                    cleanup_result["bytes_freed"] += file_size
            
        except Exception as e:
            cleanup_result["errors"].append(str(e))
        
        self._track_utility_usage("cleanup_old_data", True)
        return cleanup_result
    
    # === PRIVATE METHODS ===
    
    def _load_usage_stats(self) -> Dict[str, Any]:
        """Load utility usage statistics."""
        stats_file = self.system_dir / "usage_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"total_operations": 0, "successful_operations": 0, "utility_usage": {}}
    
    def _save_usage_stats(self):
        """Save utility usage statistics."""
        stats_file = self.system_dir / "usage_stats.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.usage_stats, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save usage stats: {e}")
    
    def _load_utility_registry(self) -> Dict[str, Any]:
        """Load registered utilities."""
        registry_file = self.system_dir / "utility_registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _track_utility_usage(self, utility_name: str, success: bool, note: str = None):
        """Track utility usage for monitoring."""
        self.usage_stats["total_operations"] += 1
        if success:
            self.usage_stats["successful_operations"] += 1
        
        if utility_name not in self.usage_stats["utility_usage"]:
            self.usage_stats["utility_usage"][utility_name] = {
                "total_calls": 0,
                "successful_calls": 0,
                "last_used": None,
                "notes": []
            }
        
        usage = self.usage_stats["utility_usage"][utility_name]
        usage["total_calls"] += 1
        if success:
            usage["successful_calls"] += 1
        usage["last_used"] = datetime.now().isoformat()
        
        if note:
            usage["notes"].append(f"{datetime.now().isoformat()}: {note}")
            if len(usage["notes"]) > 100:  # Keep only last 100 notes
                usage["notes"] = usage["notes"][-100:]
        
        # Save stats periodically
        if self.usage_stats["total_operations"] % 10 == 0:
            self._save_usage_stats()
    
    def _get_system_uptime(self) -> float:
        """Get system uptime in seconds."""
        try:
            return time.time() - self.usage_stats.get("system_start_time", time.time())
        except:
            return 0.0
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                "rss_mb": memory_info.rss / (1024 * 1024),
                "vms_mb": memory_info.vms / (1024 * 1024),
                "percent": process.memory_percent()
            }
        except ImportError:
            return {"error": "psutil not available"}
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage information."""
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            return {
                "total_gb": total / (1024**3),
                "used_gb": used / (1024**3),
                "free_gb": free / (1024**3),
                "percent_used": (used / total) * 100
            }
        except Exception as e:
            return {"error": str(e)}

# Main entry point for standalone usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AIOS Utils Core System")
    parser.add_argument('--action', choices=['validate', 'cleanup', 'metrics', 'info'], 
                       default='info', help='Action to perform')
    parser.add_argument('--data', help='Data to validate')
    parser.add_argument('--type', help='Data type for validation')
    parser.add_argument('--days', type=int, default=30, help='Days for cleanup')
    
    args = parser.parse_args()
    
    utils_system = UtilsCore()
    
    if args.action == 'validate':
        if not args.data:
            print("❌ --data required for validate action")
            sys.exit(1)
        result = utils_system.validate_data(args.data, args.type or "general")
        print(f"Validation Result: {json.dumps(result, indent=2)}")
    elif args.action == 'cleanup':
        result = utils_system.cleanup_old_data(args.days)
        print(f"Cleanup Result: {json.dumps(result, indent=2)}")
    elif args.action == 'metrics':
        metrics = utils_system.get_system_metrics()
        print(f"System Metrics: {json.dumps(metrics, indent=2)}")
    elif args.action == 'info':
        print("🔧 Utils Core System Info:")
        print(f"  Registered Utilities: {len(utils_system.utility_registry)}")
        print(f"  Total Operations: {utils_system.usage_stats['total_operations']}")
        print(f"  Successful Operations: {utils_system.usage_stats['successful_operations']}")
        print(f"  Success Rate: {(utils_system.usage_stats['successful_operations'] / max(utils_system.usage_stats['total_operations'], 1)) * 100:.1f}%")
