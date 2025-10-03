#!/usr/bin/env python3
"""
Hybrid Utils Core - Python-Rust bridge for Utils system
"""

from pathlib import Path
from utils_core.rust_bridge import RustBridge, MultiLanguageCore
from .utils_core import UtilsCore

class HybridUtilsCore(MultiLanguageCore):
    """
    Hybrid Utils Core that combines Python and Rust implementations.
    """
    
    def __init__(self):
        """
        Initialize the Hybrid Utils Core.
        """
        print("🔧 Initializing Hybrid Utils Core...")
        
        # Initialize Python implementation
        python_utils = UtilsCore()
        
        # Initialize Rust bridge
        rust_bridge = None
        try:
            rust_path = Path(__file__).parent / "rust_utils"
            if rust_path.exists():
                rust_bridge = RustBridge("utils", str(rust_path))
                
                # Try to compile and load Rust module
                if rust_bridge.compile_rust_module():
                    rust_bridge.load_rust_module()
        except Exception as e:
            print(f"⚠️ Rust Utils initialization failed: {e}")
            print("   Falling back to Python implementation")
        
        # Initialize multi-language core
        super().__init__("utils", python_utils, rust_bridge)
        
        # Expose key attributes for compatibility
        self.python_impl = python_utils
        
        print(f"🚀 Hybrid Utils Core Initialized")
        print(f"   Current implementation: {self.current_implementation.upper()}")
    
    def validate_data(self, data, data_type: str = "general"):
        """
        Validate data using hybrid implementation.
        
        Args:
            data: Data to validate
            data_type: Type of data to validate
            
        Returns:
            Validation result
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    result = rust_instance.validate_data(str(data), data_type)
                    
                    # Convert to Python dict format
                    return {
                        'is_valid': result.is_valid,
                        'data_type': result.data_type,
                        'sanitized_data': result.sanitized_data,
                        'warnings': result.warnings,
                        'timestamp': result.timestamp
                    }
            except Exception as e:
                print(f"⚠️ Rust Utils data validation failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.validate_data(data, data_type)
    
    def sanitize_input(self, input_data: str, max_length: int = 10000):
        """
        Sanitize input data using hybrid implementation.
        
        Args:
            input_data: Input data to sanitize
            max_length: Maximum length for output
            
        Returns:
            Sanitized input data
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    return rust_instance.sanitize_input(input_data, max_length)
            except Exception as e:
                print(f"⚠️ Rust Utils input sanitization failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.sanitize_input(input_data, max_length)
    
    def safe_file_read(self, file_path, encoding: str = 'utf-8'):
        """
        Safe file read operation using hybrid implementation.
        
        Args:
            file_path: Path to file to read
            encoding: File encoding
            
        Returns:
            File read result
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    result = rust_instance.safe_file_read(str(file_path), encoding)
                    
                    # Convert to Python dict format
                    return {
                        'success': result.success,
                        'file_path': result.file_path,
                        'operation': result.operation,
                        'bytes_processed': result.bytes_processed,
                        'hash': result.hash,
                        'timestamp': result.timestamp
                    }
            except Exception as e:
                print(f"⚠️ Rust Utils file read failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.safe_file_read(file_path, encoding)
    
    def safe_file_write(self, file_path, content: str, encoding: str = 'utf-8'):
        """
        Safe file write operation using hybrid implementation.
        
        Args:
            file_path: Path to file to write
            content: Content to write
            encoding: File encoding
            
        Returns:
            File write result
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    result = rust_instance.safe_file_write(str(file_path), content, encoding)
                    
                    # Convert to Python dict format
                    return {
                        'success': result.success,
                        'file_path': result.file_path,
                        'operation': result.operation,
                        'bytes_processed': result.bytes_processed,
                        'hash': result.hash,
                        'timestamp': result.timestamp
                    }
            except Exception as e:
                print(f"⚠️ Rust Utils file write failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.safe_file_write(file_path, content, encoding)
    
    def generate_file_hash(self, file_path, algorithm: str = "sha256"):
        """
        Generate file hash using hybrid implementation.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm to use
            
        Returns:
            File hash
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    return rust_instance.generate_file_hash(str(file_path), algorithm)
            except Exception as e:
                print(f"⚠️ Rust Utils file hash generation failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.generate_file_hash(file_path, algorithm)
    
    def generate_content_id(self, content: str, prefix: str = "GEN"):
        """
        Generate content ID using hybrid implementation.
        
        Args:
            content: Content to generate ID for
            prefix: Prefix for the ID
            
        Returns:
            Generated content ID
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    return rust_instance.generate_content_id(content, prefix)
            except Exception as e:
                print(f"⚠️ Rust Utils content ID generation failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.generate_content_id(content, prefix)
    
    def create_core_message(self, source_core: str, target_core: str, message_type: str, payload: str):
        """
        Create core message using hybrid implementation.
        
        Args:
            source_core: Source core name
            target_core: Target core name
            message_type: Type of message
            payload: Message payload
            
        Returns:
            Core message
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    return rust_instance.create_core_message(source_core, target_core, message_type, payload)
            except Exception as e:
                print(f"⚠️ Rust Utils core message creation failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.create_core_message(source_core, target_core, message_type, payload)
    
    def validate_core_message(self, message):
        """
        Validate core message using hybrid implementation.
        
        Args:
            message: Message to validate
            
        Returns:
            Validation result
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    return rust_instance.validate_core_message(message)
            except Exception as e:
                print(f"⚠️ Rust Utils core message validation failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.validate_core_message(message)
    
    def get_system_metrics(self):
        """
        Get system metrics using hybrid implementation.
        
        Returns:
            System metrics
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    metrics = rust_instance.get_system_metrics()
                    
                    # Convert to Python dict format
                    return {
                        'uptime_seconds': metrics.uptime_seconds,
                        'memory_usage_mb': metrics.memory_usage_mb,
                        'disk_usage_percent': metrics.disk_usage_percent,
                        'cpu_usage_percent': metrics.cpu_usage_percent,
                        'active_utilities': metrics.active_utilities,
                        'timestamp': metrics.timestamp
                    }
            except Exception as e:
                print(f"⚠️ Rust Utils system metrics failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.get_system_metrics()
    
    def cleanup_old_data(self, days_old: int = 30):
        """
        Cleanup old data using hybrid implementation.
        
        Args:
            days_old: Number of days old data to clean up
            
        Returns:
            Cleanup result
        """
        if self.current_implementation == "rust" and self.rust_bridge and self.rust_bridge.is_available():
            try:
                # Use Rust implementation
                rust_class = self.rust_bridge.get_rust_class("RustUtilsCore")
                if rust_class:
                    rust_instance = rust_class()
                    return rust_instance.cleanup_old_data(days_old)
            except Exception as e:
                print(f"⚠️ Rust Utils data cleanup failed: {e}")
                print("   Falling back to Python implementation")
        
        # Fall back to Python implementation
        return self.python_impl.cleanup_old_data(days_old)
    
    def get_hybrid_status(self):
        """
        Get hybrid system status.
        
        Returns:
            Status information
        """
        return {
            'core_name': self.core_name,
            'current_implementation': self.current_implementation,
            'rust_available': self.rust_bridge.is_available() if self.rust_bridge else False,
            'python_available': True,
            'usage_stats': getattr(self.python_impl, 'usage_stats', {}),
            'utility_registry': getattr(self.python_impl, 'utility_registry', {})
        }
