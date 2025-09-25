#!/usr/bin/env python3
"""
AIOS File Standards Validation Script
Validates all file types against AIOS File Standards
"""

import os
import sys
import json
import yaml
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import chardet
import subprocess

class AIOSFileValidator:
    """Validator for AIOS File Standards"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.is_valid = True
        self.file_stats = {
            'total': 0,
            'valid': 0,
            'errors': 0,
            'warnings': 0
        }
    
    def validate_directory(self, directory: str) -> bool:
        """Validate all files in a directory"""
        self.errors = []
        self.warnings = []
        self.is_valid = True
        self.file_stats = {'total': 0, 'valid': 0, 'errors': 0, 'warnings': 0}
        
        directory_path = Path(directory)
        if not directory_path.exists():
            self._add_error(f"Directory does not exist: {directory}")
            return False
        
        print(f"🔍 Validating AIOS Files in: {directory}")
        print("="*60)
        
        # Get all files recursively
        files = list(directory_path.rglob("*"))
        files = [f for f in files if f.is_file()]
        
        for file_path in files:
            self.file_stats['total'] += 1
            if self._validate_file(file_path):
                self.file_stats['valid'] += 1
            else:
                self.file_stats['errors'] += 1
        
        return self.is_valid
    
    def _validate_file(self, file_path: Path) -> bool:
        """Validate a single file"""
        file_errors = []
        file_warnings = []
        
        # Skip hidden files and common ignore patterns
        if (file_path.name.startswith('.') or 
            file_path.name.startswith('__pycache__') or
            'backup' in file_path.name.lower()):
            return True
        
        # Get file extension
        extension = file_path.suffix.lower()
        
        try:
            # Basic file validation
            if not self._validate_basic_file_properties(file_path):
                return False
            
            # File type specific validation
            if extension == '.py':
                file_errors.extend(self._validate_python_file(file_path))
            elif extension == '.json':
                file_errors.extend(self._validate_json_file(file_path))
            elif extension == '.md':
                file_errors.extend(self._validate_markdown_file(file_path))
            elif extension == '.db':
                file_errors.extend(self._validate_database_file(file_path))
            elif extension == '.txt':
                file_errors.extend(self._validate_text_file(file_path))
            elif extension == '.bat':
                file_errors.extend(self._validate_batch_file(file_path))
            elif extension == '.sh':
                file_errors.extend(self._validate_shell_file(file_path))
            elif extension in ['.yml', '.yaml']:
                file_errors.extend(self._validate_yaml_file(file_path))
            elif extension == '.env':
                file_errors.extend(self._validate_env_file(file_path))
            elif extension == '.log':
                file_errors.extend(self._validate_log_file(file_path))
            elif extension == '.csv':
                file_errors.extend(self._validate_csv_file(file_path))
            
            # Add file-specific errors to main error list
            for error in file_errors:
                self._add_error(f"{file_path}: {error}")
            
            for warning in file_warnings:
                self._add_warning(f"{file_path}: {warning}")
            
            if file_errors:
                return False
            else:
                print(f"✅ {file_path.name}")
                return True
                
        except Exception as e:
            self._add_error(f"{file_path}: Validation error: {e}")
            return False
    
    def _validate_basic_file_properties(self, file_path: Path) -> bool:
        """Validate basic file properties"""
        errors = []
        
        # Check file naming convention
        if not self._check_naming_convention(file_path):
            errors.append("File naming does not follow AIOS conventions")
        
        # Check file encoding
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding_info = chardet.detect(raw_data)
                encoding = encoding_info.get('encoding', 'unknown')
                
                # Python, JSON, MD, YAML, ENV files should be UTF-8
                if file_path.suffix.lower() in ['.py', '.json', '.md', '.yml', '.yaml', '.env']:
                    if encoding.lower() not in ['utf-8', 'ascii']:
                        errors.append(f"File should be UTF-8 encoded, detected: {encoding}")
        except Exception as e:
            errors.append(f"Could not detect encoding: {e}")
        
        # Check file size (warn if very large)
        file_size = file_path.stat().st_size
        if file_size > 10 * 1024 * 1024:  # 10MB
            self._add_warning(f"{file_path}: File is very large ({file_size / 1024 / 1024:.1f}MB)")
        
        if errors:
            for error in errors:
                self._add_error(f"{file_path}: {error}")
            return False
        
        return True
    
    def _check_naming_convention(self, file_path: Path) -> bool:
        """Check if file follows AIOS naming conventions"""
        name = file_path.name
        extension = file_path.suffix.lower()
        
        # Skip files that don't need naming validation
        if extension in ['.db', '.log', '.csv']:
            return True
        
        # Python files should be snake_case
        if extension == '.py':
            return self._is_snake_case(name.replace('.py', ''))
        
        # JSON files should follow specific patterns
        if extension == '.json':
            base_name = name.replace('.json', '')
            valid_patterns = [
                lambda x: x.endswith('_conversation'),
                lambda x: x.startswith('conversations_'),
                lambda x: x.startswith('cache_') or x.endswith('_cache'),
                lambda x: x.startswith('config_') or x.endswith('_config'),
                lambda x: x.startswith('results_') or x.endswith('_test_results'),
                lambda x: x.endswith('_personality'),
                lambda x: x.endswith('_memory')
            ]
            return any(pattern(base_name) for pattern in valid_patterns)
        
        # Markdown files should be descriptive
        if extension == '.md':
            return len(name) > 3 and '_' in name or name.isupper()
        
        # Other files
        return True
    
    def _is_snake_case(self, text: str) -> bool:
        """Check if text is in snake_case"""
        return text.replace('_', '').islower() and '_' in text
    
    def _validate_python_file(self, file_path: Path) -> List[str]:
        """Validate Python file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for shebang
            if lines and not lines[0].startswith('#!/usr/bin/env python'):
                if not lines[0].startswith('#!/usr/bin/python'):
                    errors.append("Missing or incorrect shebang")
            
            # Check for module docstring
            if len(lines) > 1 and not lines[1].strip().startswith('"""'):
                errors.append("Missing module docstring")
            
            # Check for imports
            has_imports = any(line.strip().startswith(('import ', 'from ')) for line in lines)
            if not has_imports:
                errors.append("No imports found")
            
            # Check line length (basic check)
            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 88]
            if long_lines:
                errors.append(f"Lines too long (>88 chars): {long_lines[:5]}")
            
            # Check for type hints in function definitions
            function_lines = [i for i, line in enumerate(lines) if line.strip().startswith('def ')]
            for line_num in function_lines:
                line = lines[line_num]
                if 'def ' in line and '->' not in line and 'pass' not in line:
                    errors.append(f"Function at line {line_num+1} missing return type hint")
            
        except Exception as e:
            errors.append(f"Error reading Python file: {e}")
        
        return errors
    
    def _validate_json_file(self, file_path: Path) -> List[str]:
        """Validate JSON file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse JSON
            data = json.loads(content)
            
            # Check if it's an array
            if not isinstance(data, list):
                errors.append("JSON file should be an array")
            
            # If it's an array with items, check for required fields
            if isinstance(data, list) and len(data) > 0:
                for i, item in enumerate(data):
                    if not isinstance(item, dict):
                        errors.append(f"Item {i} is not a dictionary")
                        continue
                    
                    # Check for required fields
                    if 'id' not in item:
                        errors.append(f"Item {i} missing required 'id' field")
                    if 'timestamp' not in item:
                        errors.append(f"Item {i} missing required 'timestamp' field")
        
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {e}")
        except Exception as e:
            errors.append(f"Error reading JSON file: {e}")
        
        return errors
    
    def _validate_markdown_file(self, file_path: Path) -> List[str]:
        """Validate Markdown file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for proper header structure
            if not lines or not lines[0].startswith('#'):
                errors.append("Missing main title (# header)")
            
            # Check for metadata header
            has_metadata = any(line.startswith('**') and '**' in line for line in lines[:10])
            if not has_metadata:
                errors.append("Missing metadata header (Version, Date, Status)")
            
            # Check line length
            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 80]
            if long_lines:
                errors.append(f"Lines too long (>80 chars): {long_lines[:5]}")
        
        except Exception as e:
            errors.append(f"Error reading Markdown file: {e}")
        
        return errors
    
    def _validate_database_file(self, file_path: Path) -> List[str]:
        """Validate database file"""
        errors = []
        
        # Check if it's a valid SQLite file
        try:
            import sqlite3
            conn = sqlite3.connect(str(file_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            if not tables:
                errors.append("Database file has no tables")
        
        except Exception as e:
            errors.append(f"Not a valid SQLite database: {e}")
        
        return errors
    
    def _validate_text_file(self, file_path: Path) -> List[str]:
        """Validate text file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper structure (basic)
            if len(content) > 0 and not content.startswith('#'):
                self._add_warning(f"{file_path}: Text file should start with header comment")
        
        except Exception as e:
            errors.append(f"Error reading text file: {e}")
        
        return errors
    
    def _validate_batch_file(self, file_path: Path) -> List[str]:
        """Validate batch file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for proper batch structure
            if not lines or not lines[0].startswith('@echo off'):
                errors.append("Missing '@echo off' directive")
            
            # Check for comments
            has_comments = any(line.strip().startswith('REM ') for line in lines)
            if not has_comments:
                errors.append("Missing documentation comments")
        
        except Exception as e:
            errors.append(f"Error reading batch file: {e}")
        
        return errors
    
    def _validate_shell_file(self, file_path: Path) -> List[str]:
        """Validate shell file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for shebang
            if not lines or not lines[0].startswith('#!/bin/bash'):
                errors.append("Missing or incorrect shebang")
            
            # Check for error handling
            if 'set -euo pipefail' not in content:
                errors.append("Missing error handling (set -euo pipefail)")
        
        except Exception as e:
            errors.append(f"Error reading shell file: {e}")
        
        return errors
    
    def _validate_yaml_file(self, file_path: Path) -> List[str]:
        """Validate YAML file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML
            data = yaml.safe_load(content)
            
            if data is None:
                errors.append("Empty YAML file")
        
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML format: {e}")
        except Exception as e:
            errors.append(f"Error reading YAML file: {e}")
        
        return errors
    
    def _validate_env_file(self, file_path: Path) -> List[str]:
        """Validate environment file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check for proper format
            for i, line in enumerate(lines):
                line = line.strip()
                if line and not line.startswith('#') and '=' not in line:
                    errors.append(f"Line {i+1}: Invalid format (missing =)")
        
        except Exception as e:
            errors.append(f"Error reading environment file: {e}")
        
        return errors
    
    def _validate_log_file(self, file_path: Path) -> List[str]:
        """Validate log file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check for proper log format
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                if line.strip() and '|' not in line:
                    errors.append(f"Line {i+1}: Not in standard log format")
                    break
        
        except Exception as e:
            errors.append(f"Error reading log file: {e}")
        
        return errors
    
    def _validate_csv_file(self, file_path: Path) -> List[str]:
        """Validate CSV file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if not rows:
                errors.append("Empty CSV file")
            elif len(rows[0]) == 0:
                errors.append("CSV file has no headers")
        
        except Exception as e:
            errors.append(f"Error reading CSV file: {e}")
        
        return errors
    
    def _add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)
        self.is_valid = False
        self.file_stats['errors'] += 1
    
    def _add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)
        self.file_stats['warnings'] += 1
    
    def print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        print("📊 VALIDATION RESULTS")
        print("="*60)
        
        print(f"📁 Total files: {self.file_stats['total']}")
        print(f"✅ Valid files: {self.file_stats['valid']}")
        print(f"❌ Files with errors: {self.file_stats['errors']}")
        print(f"⚠️ Files with warnings: {self.file_stats['warnings']}")
        
        if self.errors:
            print(f"\n🚨 ERRORS ({len(self.errors)}):")
            for error in self.errors[:20]:  # Show first 20 errors
                print(f"   • {error}")
            if len(self.errors) > 20:
                print(f"   ... and {len(self.errors) - 20} more errors")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10 warnings
                print(f"   • {warning}")
            if len(self.warnings) > 10:
                print(f"   ... and {len(self.warnings) - 10} more warnings")
        
        if not self.errors and not self.warnings:
            print("\n🎯 All files are compliant with AIOS File Standards!")
        elif self.errors:
            print(f"\n❌ {len(self.errors)} files have validation errors.")
        else:
            print(f"\n⚠️ {len(self.warnings)} files have warnings but are valid.")

def main():
    """Main validation function"""
    if len(sys.argv) != 2:
        print("Usage: python validate_aios_files.py <directory_path>")
        print("Example: python validate_aios_files.py .")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    validator = AIOSFileValidator()
    is_valid = validator.validate_directory(directory)
    
    validator.print_results()
    
    if is_valid:
        print(f"\n🎯 All files in {directory} are compliant with AIOS File Standards!")
        sys.exit(0)
    else:
        print(f"\n❌ Some files in {directory} have validation errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
