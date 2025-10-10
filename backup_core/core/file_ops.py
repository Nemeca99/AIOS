#!/usr/bin/env python3
"""
File Operations - Helper functions for file system operations
"""

import os
import shutil
from pathlib import Path
from typing import List, Set, Optional, Tuple
import fnmatch


class FileOperations:
    """Helper class for file system operations"""
    
    # Default ignore patterns (like .gitignore)
    DEFAULT_IGNORE_PATTERNS = [
        '__pycache__',
        '*.pyc',
        '.pytest_cache',
        'node_modules',
        '.git',
        '.aios_backup',  # Don't backup the backup system itself
        'backup_core',   # Don't backup into itself
        '*.zip',
        '*.tar.gz',
        '.DS_Store',
        'Thumbs.db',
        '*.swp',
        '*.swo',
        '*~',
        '.vscode',
        '.idea',
    ]
    
    def __init__(self, workspace_root: Path, ignore_patterns: Optional[List[str]] = None):
        self.workspace_root = workspace_root
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE_PATTERNS
        self._ignore_file = workspace_root / ".backupignore"
        
        # Load additional ignore patterns from .backupignore
        if self._ignore_file.exists():
            with open(self._ignore_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.ignore_patterns.append(line)
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        path_str = str(path)
        
        # Check each ignore pattern
        for pattern in self.ignore_patterns:
            # Check if any part of the path matches the pattern
            if fnmatch.fnmatch(path.name, pattern):
                return True
            # Check if pattern is in any part of the path
            if pattern in path.parts:
                return True
            # Check full path match
            if fnmatch.fnmatch(path_str, pattern):
                return True
        
        return False
    
    def get_all_files(self, directory: Optional[Path] = None) -> List[Path]:
        """
        Get all files in directory (recursively), respecting ignore patterns
        Args:
            directory: Directory to scan (defaults to workspace_root)
        Returns:
            List of file paths relative to workspace_root
        """
        if directory is None:
            directory = self.workspace_root
        
        files = []
        
        try:
            for entry in directory.rglob("*"):
                # Skip if should ignore
                if self.should_ignore(entry):
                    continue
                
                # Only include files
                if entry.is_file():
                    try:
                        # Get relative path from workspace root
                        rel_path = entry.relative_to(self.workspace_root)
                        files.append(rel_path)
                    except ValueError:
                        # File is outside workspace root
                        continue
                    except (PermissionError, OSError):
                        # Can't access file
                        continue
        except (PermissionError, OSError):
            # Can't access directory
            pass
        
        return sorted(files)
    
    def get_files_in_paths(self, paths: List[Path]) -> List[Path]:
        """
        Get all files from a list of paths (files or directories)
        Args:
            paths: List of file or directory paths
        Returns:
            List of file paths
        """
        result_files = []
        
        for path in paths:
            full_path = self.workspace_root / path
            
            if not full_path.exists():
                continue
            
            if self.should_ignore(path):
                continue
            
            if full_path.is_file():
                result_files.append(path)
            elif full_path.is_dir():
                # Get all files in directory
                dir_files = self.get_all_files(full_path)
                result_files.extend(dir_files)
        
        return sorted(set(result_files))
    
    def get_file_mode(self, file_path: Path) -> str:
        """
        Get file mode for Git storage
        Returns: '100644' for normal files, '100755' for executables
        """
        full_path = self.workspace_root / file_path
        
        if not full_path.exists():
            return "100644"
        
        # Check if executable
        if os.access(full_path, os.X_OK):
            return "100755"
        
        return "100644"
    
    def read_file(self, file_path: Path) -> bytes:
        """Read file content"""
        full_path = self.workspace_root / file_path
        with open(full_path, 'rb') as f:
            return f.read()
    
    def write_file(self, file_path: Path, content: bytes):
        """Write file content"""
        full_path = self.workspace_root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(content)
    
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists"""
        return (self.workspace_root / file_path).exists()
    
    def delete_file(self, file_path: Path):
        """Delete file"""
        full_path = self.workspace_root / file_path
        if full_path.exists():
            full_path.unlink()
    
    def copy_file(self, src: Path, dst: Path):
        """Copy file from src to dst"""
        src_full = self.workspace_root / src
        dst_full = self.workspace_root / dst
        dst_full.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_full, dst_full)
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        full_path = self.workspace_root / file_path
        if full_path.exists():
            return full_path.stat().st_size
        return 0
    
    def get_file_mtime(self, file_path: Path) -> float:
        """Get file modification time"""
        full_path = self.workspace_root / file_path
        if full_path.exists():
            return full_path.stat().st_mtime
        return 0.0
    
    def create_backup_ignore_file(self):
        """Create a sample .backupignore file"""
        if not self._ignore_file.exists():
            sample_content = """# AIOS Backup Ignore Patterns
# Add patterns for files/directories to exclude from backups

# Python
__pycache__
*.pyc
*.pyo
.pytest_cache

# Node
node_modules

# IDEs
.vscode
.idea
*.swp

# System
.DS_Store
Thumbs.db

# Backup system itself
.aios_backup
backup_core

# Large files
*.zip
*.tar.gz
*.log
"""
            with open(self._ignore_file, 'w') as f:
                f.write(sample_content)

