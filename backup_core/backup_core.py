#!/usr/bin/env python3
"""
BACKUP CORE SYSTEM - Git-like Incremental Backup
Self-contained backup and recovery system for AIOS Clean
Works like Git: one active backup that gets updated incrementally
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

import os
import shutil
import json
import zipfile
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

class BackupCore:
    """
    Git-like backup system for AIOS Clean.
    Maintains one active backup that gets updated incrementally.
    Archives old versions of changed files before updating.
    """
    
    def __init__(self):
        """Initialize the backup core system."""
        self.backup_dir = Path("backup_core")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Git-like backup structure
        self.active_backup_dir = self.backup_dir / "active_backup"
        self.archive_backup_dir = self.backup_dir / "archive_backup"
        self.active_backup_dir.mkdir(exist_ok=True)
        self.archive_backup_dir.mkdir(exist_ok=True)
        
        # Initialize backup tracking
        self.backup_tracking_file = self.backup_dir / "backup_tracking.json"
        self.file_checksums_file = self.backup_dir / "file_checksums.json"
        self.last_backup_timestamp = self._load_last_backup_timestamp()
        self.file_checksums = self._load_file_checksums()
        
        print(f"🔒 Backup Core System Initialized (Git-like)")
        print(f"   Active Backup: {self.active_backup_dir}")
        print(f"   Archive Backup: {self.archive_backup_dir}")
        print(f"   Last Backup: {datetime.fromtimestamp(self.last_backup_timestamp) if self.last_backup_timestamp > 0 else 'Never'}")
    
    def create_backup(self, 
                     backup_name: Optional[str] = None,
                     include_data: bool = True,
                     include_logs: bool = True,
                     include_config: bool = True,
                     incremental: bool = True) -> str:
        """
        Create/update a Git-like backup: one active backup that gets updated incrementally.
        Old versions of changed files are archived before updating.
        
        Args:
            backup_name: Name for the backup (defaults to 'active')
            include_data: Include data directories
            include_logs: Include log files
            include_config: Include configuration files
            incremental: Only backup changed files since last backup
            
        Returns:
            Path to the active backup directory
        """
        if backup_name is None:
            backup_name = "active"
        
        print(f"🔄 Updating active backup (Git-like)")
        start_time = time.time()
        
        try:
            # Get list of files to backup
            files_to_backup = self._get_files_to_backup(include_data, include_logs, include_config)
            
            # Check for changed files and archive old versions
            changed_files = self._get_changed_files(files_to_backup)
            
            if changed_files:
                print(f"📦 Archiving {len(changed_files)} changed files...")
                self._archive_changed_files(changed_files)
            
            # Update active backup with new/changed files
            print(f"🔄 Updating active backup with {len(files_to_backup)} files...")
            self._update_active_backup(files_to_backup)
            
            # Update file checksums
            self._update_file_checksums(files_to_backup)
            
            # Update backup tracking
            self._update_last_backup_timestamp()
            
            elapsed_time = time.time() - start_time
            
            print(f"✅ Active backup updated")
            print(f"   Files processed: {len(files_to_backup)}")
            print(f"   Files changed: {len(changed_files)}")
            print(f"   Time taken: {elapsed_time:.1f}s")
            
            return str(self.active_backup_dir)
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            raise
    
    def _get_files_to_backup(self, include_data: bool, include_logs: bool, include_config: bool) -> List[Path]:
        """Get list of files to include in backup."""
        files_to_backup = []
        
        # Core directories to backup
        core_dirs = [
            "backup_core",
            "carma_core", 
            "data_core",
            "dream_core",
            "enterprise_core",
            "luna_core",
            "streamlit_core",
            "support_core",
            "utils_core"
        ]
        
        # Add core files
        for core_dir in core_dirs:
            if Path(core_dir).exists():
                for file_path in Path(core_dir).rglob("*"):
                    if file_path.is_file():
                        files_to_backup.append(file_path)
        
        # Add main files
        main_files = ["main.py", "requirements.txt", "README.md"]
        for main_file in main_files:
            if Path(main_file).exists():
                files_to_backup.append(Path(main_file))
        
        # Conditionally add other directories
        if include_config:
            config_dir = Path("config")
            if config_dir.exists():
                for file_path in config_dir.rglob("*"):
                    if file_path.is_file():
                        files_to_backup.append(file_path)
        
        if include_logs:
            log_dir = Path("log")
            if log_dir.exists():
                for file_path in log_dir.rglob("*"):
                    if file_path.is_file():
                        files_to_backup.append(file_path)
        
        return files_to_backup
    
    def _get_changed_files(self, files_to_backup: List[Path]) -> List[Path]:
        """Get list of files that have changed since last backup."""
        changed_files = []
        
        for file_path in files_to_backup:
            # Get current file checksum
            try:
                current_checksum = self._calculate_file_checksum(file_path)
                stored_checksum = self.file_checksums.get(str(file_path))
                
                # If file is new or checksum changed, it needs to be backed up
                if stored_checksum != current_checksum:
                    changed_files.append(file_path)
                    
            except Exception as e:
                print(f"⚠️ Warning: Could not check {file_path}: {e}")
                # If we can't check, assume it changed
                changed_files.append(file_path)
        
        return changed_files
    
    def _archive_changed_files(self, changed_files: List[Path]):
        """Archive old versions of changed files before updating."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = self.archive_backup_dir / f"archive_{timestamp}"
        archive_dir.mkdir(exist_ok=True)
        
        for file_path in changed_files:
            try:
                # Get relative path from project root, handle absolute paths
                if file_path.is_absolute():
                    # Try to get relative path from current working directory
                    try:
                        relative_path = file_path.relative_to(Path.cwd())
                    except ValueError:
                        # If file is outside project directory, skip it
                        continue
                else:
                    relative_path = file_path
                
                # Create archive path maintaining directory structure
                archive_file_path = archive_dir / relative_path
                archive_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy old version from active backup to archive
                active_backup_file = self.active_backup_dir / relative_path
                if active_backup_file.exists():
                    shutil.copy2(active_backup_file, archive_file_path)
                    print(f"📦 Archived: {relative_path}")
                    
            except Exception as e:
                print(f"⚠️ Warning: Could not archive {file_path}: {e}")
    
    def _update_active_backup(self, files_to_backup: List[Path]):
        """Update the active backup with current files."""
        for file_path in files_to_backup:
            try:
                # Get relative path from project root, handle absolute paths
                if file_path.is_absolute():
                    # Try to get relative path from current working directory
                    try:
                        relative_path = file_path.relative_to(Path.cwd())
                    except ValueError:
                        # If file is outside project directory, skip it
                        continue
                else:
                    relative_path = file_path
                
                # Create backup path maintaining directory structure
                backup_file_path = self.active_backup_dir / relative_path
                backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy current file to active backup
                shutil.copy2(file_path, backup_file_path)
                
            except Exception as e:
                print(f"⚠️ Warning: Could not backup {file_path}: {e}")
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""
    
    def _update_file_checksums(self, files_to_backup: List[Path]):
        """Update stored checksums for all files."""
        for file_path in files_to_backup:
            try:
                checksum = self._calculate_file_checksum(file_path)
                self.file_checksums[str(file_path)] = checksum
            except Exception as e:
                print(f"⚠️ Warning: Could not update checksum for {file_path}: {e}")
        
        # Save checksums to file
        self._save_file_checksums()
    
    def _load_file_checksums(self) -> Dict[str, str]:
        """Load file checksums from disk."""
        if self.file_checksums_file.exists():
            try:
                with open(self.file_checksums_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_file_checksums(self):
        """Save file checksums to disk."""
        try:
            with open(self.file_checksums_file, 'w') as f:
                json.dump(self.file_checksums, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save checksums: {e}")
    
    def _load_last_backup_timestamp(self) -> float:
        """Load the last backup timestamp."""
        if self.backup_tracking_file.exists():
            try:
                with open(self.backup_tracking_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_backup_timestamp', 0)
            except Exception:
                pass
        return 0
    
    def _update_last_backup_timestamp(self):
        """Update the last backup timestamp."""
        try:
            data = {
                'last_backup_timestamp': time.time(),
                'backup_date': datetime.now().isoformat()
            }
            with open(self.backup_tracking_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not update backup timestamp: {e}")
    
    def auto_backup_on_access(self) -> str:
        """Trigger auto-backup when main.py is accessed."""
        print("🔄 Auto-backup triggered by main.py access...")
        return self.create_backup("auto_access", incremental=True)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get backup system information."""
        try:
            active_files = len(list(self.active_backup_dir.rglob("*"))) if self.active_backup_dir.exists() else 0
            archive_dirs = len(list(self.archive_backup_dir.iterdir())) if self.archive_backup_dir.exists() else 0
            
            return {
                "system_type": "Git-like Incremental Backup",
                "active_backup_dir": str(self.active_backup_dir),
                "archive_backup_dir": str(self.archive_backup_dir),
                "active_files": active_files,
                "archive_directories": archive_dirs,
                "total_backups": 1,  # Only one active backup
                "last_backup": datetime.fromtimestamp(self.last_backup_timestamp).isoformat() if self.last_backup_timestamp > 0 else "Never",
                "tracked_files": len(self.file_checksums)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def cleanup_old_archives(self, keep_days: int = 7):
        """Clean up old archive directories (like Git garbage collection)."""
        if not self.archive_backup_dir.exists():
            return
        
        cutoff_time = time.time() - (keep_days * 24 * 60 * 60)
        cleaned_count = 0
        
        for archive_dir in self.archive_backup_dir.iterdir():
            if archive_dir.is_dir() and archive_dir.stat().st_mtime < cutoff_time:
                try:
                    shutil.rmtree(archive_dir)
                    cleaned_count += 1
                    print(f"🗑️ Cleaned old archive: {archive_dir.name}")
                except Exception as e:
                    print(f"⚠️ Warning: Could not clean {archive_dir}: {e}")
        
        if cleaned_count > 0:
            print(f"✅ Cleaned {cleaned_count} old archive directories")

if __name__ == "__main__":
    # Test the backup system
    backup_system = BackupCore()
    backup_system.create_backup()
    print("\n" + "="*50)
    info = backup_system.get_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")