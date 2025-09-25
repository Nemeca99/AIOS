#!/usr/bin/env python3
"""
AIOS JSON Standards Validation Script
Validates any JSON file against the AIOS JSON Standard Format
"""

import json
import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import AIOS standards
try:
    from aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards
    AIOS_STANDARDS_AVAILABLE = True
except ImportError:
    AIOS_STANDARDS_AVAILABLE = False
    print("⚠️ AIOS JSON Standards not available, using basic validation")

class AIOSJSONValidator:
    """Validator for AIOS JSON Standard Format"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.is_valid = True
    
    def validate_file(self, file_path: str) -> bool:
        """Validate a JSON file against AIOS standards"""
        self.errors = []
        self.warnings = []
        self.is_valid = True
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            self._add_error(f"File does not exist: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self._add_error(f"Invalid JSON format: {e}")
            return False
        except Exception as e:
            self._add_error(f"Error reading file: {e}")
            return False
        
        # Basic validation
        self._validate_basic_structure(data)
        
        if self.is_valid and len(data) > 0:
            self._validate_data_type(data[0])
        
        return self.is_valid
    
    def _validate_basic_structure(self, data: Any):
        """Validate basic JSON structure"""
        if not isinstance(data, list):
            self._add_error("JSON file must be an array (start with '[')")
            return
        
        if len(data) == 0:
            self._add_warning("JSON array is empty")
            return
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                self._add_error(f"Item {i} is not a dictionary")
            else:
                self._validate_required_fields(item, i)
    
    def _validate_required_fields(self, item: Dict, index: int):
        """Validate required fields in an item"""
        # Check for ID field
        if 'id' not in item:
            self._add_error(f"Item {index} missing required 'id' field")
        else:
            if not self._is_valid_uuid(item['id']):
                self._add_error(f"Item {index} has invalid UUID format: {item['id']}")
        
        # Check for timestamp field
        if 'timestamp' not in item:
            self._add_error(f"Item {index} missing required 'timestamp' field")
        else:
            if not self._is_valid_timestamp(item['timestamp']):
                self._add_error(f"Item {index} has invalid timestamp format: {item['timestamp']}")
    
    def _validate_data_type(self, item: Dict):
        """Validate specific data type based on content"""
        # Try to determine data type from content
        data_type = self._detect_data_type(item)
        
        if data_type == "conversation":
            self._validate_conversation_data(item)
        elif data_type == "cache":
            self._validate_cache_data(item)
        elif data_type == "config":
            self._validate_config_data(item)
        elif data_type == "test_result":
            self._validate_test_result_data(item)
        else:
            self._add_warning(f"Unknown data type, using basic validation")
    
    def _detect_data_type(self, item: Dict) -> str:
        """Detect data type from item content"""
        if 'role' in item and 'content' in item:
            return "conversation"
        elif 'pattern' in item and 'embedding' in item:
            return "cache"
        elif 'config_name' in item and 'parameters' in item:
            return "config"
        elif 'test_id' in item and 'questions' in item:
            return "test_result"
        else:
            return "unknown"
    
    def _validate_conversation_data(self, item: Dict):
        """Validate conversation data format"""
        required_fields = ['id', 'conversation_id', 'role', 'content', 'timestamp', 'metadata']
        
        for field in required_fields:
            if field not in item:
                self._add_error(f"Conversation data missing required field: {field}")
        
        if 'role' in item and item['role'] not in ['user', 'assistant', 'system']:
            self._add_error(f"Invalid role value: {item['role']}")
        
        if not isinstance(item.get('metadata', {}), dict):
            self._add_error("Metadata field must be a dictionary")
    
    def _validate_cache_data(self, item: Dict):
        """Validate cache data format"""
        required_fields = ['id', 'pattern', 'embedding', 'frequency', 'last_used', 'similarity_threshold', 'compression']
        
        for field in required_fields:
            if field not in item:
                self._add_error(f"Cache data missing required field: {field}")
        
        if 'embedding' in item and not isinstance(item['embedding'], list):
            self._add_error("Embedding field must be an array")
        
        if 'compression' in item and not isinstance(item['compression'], dict):
            self._add_error("Compression field must be a dictionary")
    
    def _validate_config_data(self, item: Dict):
        """Validate config data format"""
        required_fields = ['id', 'config_name', 'version', 'parameters', 'models', 'timestamp', 'metadata']
        
        for field in required_fields:
            if field not in item:
                self._add_error(f"Config data missing required field: {field}")
        
        if not isinstance(item.get('parameters', {}), dict):
            self._add_error("Parameters field must be a dictionary")
        
        if not isinstance(item.get('models', {}), dict):
            self._add_error("Models field must be a dictionary")
    
    def _validate_test_result_data(self, item: Dict):
        """Validate test result data format"""
        required_fields = ['test_id', 'timestamp', 'mode', 'model', 'questions', 'performance', 'metadata']
        
        for field in required_fields:
            if field not in item:
                self._add_error(f"Test result data missing required field: {field}")
        
        if 'questions' in item and not isinstance(item['questions'], list):
            self._add_error("Questions field must be an array")
        
        if 'performance' in item and not isinstance(item['performance'], dict):
            self._add_error("Performance field must be a dictionary")
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Check if string is a valid UUID"""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False
    
    def _is_valid_timestamp(self, timestamp: str) -> bool:
        """Check if string is a valid ISO 8601 timestamp"""
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    def _add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)
        self.is_valid = False
    
    def _add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)
    
    def print_results(self):
        """Print validation results"""
        if self.is_valid:
            print("✅ VALIDATION PASSED")
        else:
            print("❌ VALIDATION FAILED")
        
        if self.errors:
            print("\n🚨 ERRORS:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if not self.errors and not self.warnings:
            print("🎯 No issues found - file is fully compliant!")

def main():
    """Main validation function"""
    if len(sys.argv) != 2:
        print("Usage: python validate_aios_json.py <json_file_path>")
        print("Example: python validate_aios_json.py config/luna_personality_dna.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"🔍 Validating: {file_path}")
    print("="*50)
    
    validator = AIOSJSONValidator()
    is_valid = validator.validate_file(file_path)
    
    validator.print_results()
    
    if is_valid:
        print(f"\n🎯 {file_path} is compliant with AIOS JSON Standards!")
        sys.exit(0)
    else:
        print(f"\n❌ {file_path} has validation errors. Please fix and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
