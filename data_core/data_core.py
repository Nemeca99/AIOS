#!/usr/bin/env python3
"""
DATA CORE SYSTEM
Self-contained data management system for AIOS Clean
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

import os
import json
import sqlite3
import shutil
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

class DataCore:
    """
    Self-contained data management system for AIOS Clean.
    Handles all data storage, retrieval, and management operations.
    """
    
    def __init__(self):
        """Initialize the data core system."""
        self.data_dir = Path("data_core")
        self.data_dir.mkdir(exist_ok=True)
        
        # Core data directories - Main data pipeline for ALL AIOS data
        self.fractal_cache_dir = self.data_dir / "FractalCache"
        self.arbiter_cache_dir = self.data_dir / "ArbiterCache"
        self.conversations_dir = self.data_dir / "conversations"
        self.config_dir = self.data_dir / "config"
        self.database_dir = self.data_dir / "AIOS_Database" / "database"
        
        # Additional data pipeline directories
        self.logs_dir = self.data_dir / "logs"
        self.temp_dir = self.data_dir / "temp"
        self.cache_dir = self.data_dir / "cache"
        # Note: backups_dir removed - backup_core manages its own backups
        self.exports_dir = self.data_dir / "exports"
        self.imports_dir = self.data_dir / "imports"
        self.analytics_dir = self.data_dir / "analytics"
        
        # Initialize data pipeline tracking
        self.pipeline_stats = self._load_pipeline_stats()
        self.data_registry = self._load_data_registry()
        
        # Ensure directories exist
        self._ensure_directories()
        
        print(f"🗄️ Data Core System Initialized - Main Data Pipeline for ALL AIOS Data")
        print(f"   Data Directory: {self.data_dir}")
        print(f"   Fractal Cache: {self.fractal_cache_dir}")
        print(f"   Arbiter Cache: {self.arbiter_cache_dir}")
        print(f"   Conversations: {self.conversations_dir}")
        print(f"   Logs: {self.logs_dir}")
        print(f"   Temp: {self.temp_dir}")
        print(f"   Cache: {self.cache_dir}")
        print(f"   Exports: {self.exports_dir}")
        print(f"   Analytics: {self.analytics_dir}")
    
    def _ensure_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.fractal_cache_dir,
            self.arbiter_cache_dir,
            self.conversations_dir,
            self.config_dir,
            self.database_dir,
            self.logs_dir,
            self.temp_dir,
            self.cache_dir,
            # Note: backups_dir removed - backup_core manages its own backups
            self.exports_dir,
            self.imports_dir,
            self.analytics_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_fractal_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the FractalCache."""
        if not self.fractal_cache_dir.exists():
            return {'total_files': 0, 'total_size_mb': 0, 'files': []}
        
        files = []
        total_size = 0
        
        for file_path in self.fractal_cache_dir.glob("*.json"):
            try:
                stat = file_path.stat()
                file_size = stat.st_size
                total_size += file_size
                
                # Try to read file metadata
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    files.append({
                        'name': file_path.name,
                        'size_bytes': file_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'content_type': data.get('specialization', 'unknown'),
                        'tags': data.get('tags', []),
                        'word_count': len(data.get('content', '').split()) if data.get('content') else 0
                    })
                except:
                    files.append({
                        'name': file_path.name,
                        'size_bytes': file_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'content_type': 'corrupted',
                        'tags': [],
                        'word_count': 0
                    })
                    
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")
        
        return {
            'total_files': len(files),
            'total_size_mb': total_size / (1024 * 1024),
            'files': sorted(files, key=lambda x: x['modified'], reverse=True)
        }
    
    def get_arbiter_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the ArbiterCache."""
        if not self.arbiter_cache_dir.exists():
            return {'total_files': 0, 'total_size_mb': 0, 'files': []}
        
        files = []
        total_size = 0
        
        for file_path in self.arbiter_cache_dir.glob("*.json"):
            try:
                stat = file_path.stat()
                file_size = stat.st_size
                total_size += file_size
                
                files.append({
                    'name': file_path.name,
                    'size_bytes': file_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
                    
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")
        
        return {
            'total_files': len(files),
            'total_size_mb': total_size / (1024 * 1024),
            'files': sorted(files, key=lambda x: x['modified'], reverse=True)
        }
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about conversations."""
        if not self.conversations_dir.exists():
            return {'total_conversations': 0, 'total_size_mb': 0}
        
        conversations = list(self.conversations_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in conversations)
        
        return {
            'total_conversations': len(conversations),
            'total_size_mb': total_size / (1024 * 1024),
            'latest_conversation': max(conversations, key=lambda x: x.stat().st_mtime).name if conversations else None
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about databases."""
        if not self.database_dir.exists():
            return {'databases': []}
        
        databases = []
        for db_file in self.database_dir.glob("*.db"):
            try:
                stat = db_file.stat()
                db_size = stat.st_size
                
                # Get table info
                tables = []
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [row[0] for row in cursor.fetchall()]
                    conn.close()
                except:
                    pass
                
                databases.append({
                    'name': db_file.name,
                    'size_mb': db_size / (1024 * 1024),
                    'tables': tables,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
                
            except Exception as e:
                print(f"⚠️ Error processing {db_file}: {e}")
        
        return {'databases': databases}
    
    def cleanup_old_data(self, days_old: int = 30, dry_run: bool = True) -> Dict[str, Any]:
        """
        Clean up old data files.
        
        Args:
            days_old: Delete files older than this many days
            dry_run: If True, only report what would be deleted
            
        Returns:
            Dictionary with cleanup results
        """
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        cleanup_results = {
            'fractal_cache': {'deleted': 0, 'size_freed_mb': 0},
            'arbiter_cache': {'deleted': 0, 'size_freed_mb': 0},
            'conversations': {'deleted': 0, 'size_freed_mb': 0},
            'total_deleted': 0,
            'total_size_freed_mb': 0
        }
        
        # Clean FractalCache
        if self.fractal_cache_dir.exists():
            for file_path in self.fractal_cache_dir.glob("*.json"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_size = file_path.stat().st_size
                    if not dry_run:
                        file_path.unlink()
                    cleanup_results['fractal_cache']['deleted'] += 1
                    cleanup_results['fractal_cache']['size_freed_mb'] += file_size / (1024 * 1024)
        
        # Clean ArbiterCache
        if self.arbiter_cache_dir.exists():
            for file_path in self.arbiter_cache_dir.glob("*.json"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_size = file_path.stat().st_size
                    if not dry_run:
                        file_path.unlink()
                    cleanup_results['arbiter_cache']['deleted'] += 1
                    cleanup_results['arbiter_cache']['size_freed_mb'] += file_size / (1024 * 1024)
        
        # Clean old conversations
        if self.conversations_dir.exists():
            for file_path in self.conversations_dir.glob("*.json"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_size = file_path.stat().st_size
                    if not dry_run:
                        file_path.unlink()
                    cleanup_results['conversations']['deleted'] += 1
                    cleanup_results['conversations']['size_freed_mb'] += file_size / (1024 * 1024)
        
        cleanup_results['total_deleted'] = (
            cleanup_results['fractal_cache']['deleted'] +
            cleanup_results['arbiter_cache']['deleted'] +
            cleanup_results['conversations']['deleted']
        )
        
        cleanup_results['total_size_freed_mb'] = (
            cleanup_results['fractal_cache']['size_freed_mb'] +
            cleanup_results['arbiter_cache']['size_freed_mb'] +
            cleanup_results['conversations']['size_freed_mb']
        )
        
        action = "Would delete" if dry_run else "Deleted"
        print(f"🗑️ {action} {cleanup_results['total_deleted']} files ({cleanup_results['total_size_freed_mb']:.1f} MB)")
        
        return cleanup_results
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview."""
        return {
            'fractal_cache': self.get_fractal_cache_stats(),
            'arbiter_cache': self.get_arbiter_cache_stats(),
            'conversations': self.get_conversation_stats(),
            'databases': self.get_database_stats(),
            'timestamp': datetime.now().isoformat()
        }
    
    def backup_data(self, backup_name: Optional[str] = None) -> str:
        """Create a backup of all data."""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"data_backup_{timestamp}"
        
        backup_dir = self.data_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        backup_path = backup_dir / f"{backup_name}"
        
        print(f"🗄️ Creating data backup: {backup_name}")
        
        # Copy fractal cache
        if self.fractal_cache_dir.exists():
            shutil.copytree(self.fractal_cache_dir, backup_path / "FractalCache")
        
        # Copy arbiter cache
        if self.arbiter_cache_dir.exists():
            shutil.copytree(self.arbiter_cache_dir, backup_path / "ArbiterCache")
        
        # Copy conversations
        if self.conversations_dir.exists():
            shutil.copytree(self.conversations_dir, backup_path / "conversations")
        
        print(f"✅ Data backup created: {backup_path}")
        
        return str(backup_path)

    def _load_pipeline_stats(self) -> Dict[str, Any]:
        """Load data pipeline statistics."""
        stats_file = self.data_dir / "pipeline_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "total_operations": 0,
            "data_ingested": 0,
            "data_processed": 0,
            "data_exported": 0,
            "pipeline_uptime": datetime.now().isoformat(),
            "last_operation": None
        }

    def _save_pipeline_stats(self):
        """Save data pipeline statistics."""
        stats_file = self.data_dir / "pipeline_stats.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.pipeline_stats, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save pipeline stats: {e}")

    def _load_data_registry(self) -> Dict[str, Any]:
        """Load data registry for tracking all data operations."""
        registry_file = self.data_dir / "data_registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"data_sources": {}, "data_sinks": {}, "data_transforms": {}}

    def _save_data_registry(self):
        """Save data registry."""
        registry_file = self.data_dir / "data_registry.json"
        try:
            with open(registry_file, 'w') as f:
                json.dump(self.data_registry, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save data registry: {e}")

    def ingest_data(self, data: Any, source: str, data_type: str = "unknown") -> Dict[str, Any]:
        """
        Ingest data into the AIOS data pipeline.
        
        Args:
            data: Data to ingest
            source: Source system/core
            data_type: Type of data
            
        Returns:
            Ingestion results
        """
        ingestion_id = f"ING_{int(time.time())}_{hash(str(data)) % 10000:04d}"
        
        result = {
            "ingestion_id": ingestion_id,
            "source": source,
            "data_type": data_type,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "storage_path": None,
            "error": None
        }
        
        try:
            # Store data in appropriate location
            if data_type == "fragment":
                storage_path = self.fractal_cache_dir / f"{ingestion_id}.json"
            elif data_type == "arbiter":
                storage_path = self.arbiter_cache_dir / f"{ingestion_id}.json"
            elif data_type == "conversation":
                storage_path = self.conversations_dir / f"{ingestion_id}.json"
            elif data_type == "log":
                storage_path = self.logs_dir / f"{ingestion_id}.log"
            else:
                storage_path = self.temp_dir / f"{ingestion_id}.json"
            
            # Write data
            with open(storage_path, 'w', encoding='utf-8') as f:
                if isinstance(data, (dict, list)):
                    json.dump(data, f, indent=2, default=str)
                else:
                    f.write(str(data))
            
            result["success"] = True
            result["storage_path"] = str(storage_path)
            
            # Update pipeline stats
            self.pipeline_stats["total_operations"] += 1
            self.pipeline_stats["data_ingested"] += 1
            self.pipeline_stats["last_operation"] = datetime.now().isoformat()
            self._save_pipeline_stats()
            
            # Update data registry
            if source not in self.data_registry["data_sources"]:
                self.data_registry["data_sources"][source] = {"count": 0, "last_ingestion": None}
            self.data_registry["data_sources"][source]["count"] += 1
            self.data_registry["data_sources"][source]["last_ingestion"] = datetime.now().isoformat()
            self._save_data_registry()
            
        except Exception as e:
            result["error"] = str(e)
        
        return result

    def export_data(self, data_type: str, target_format: str = "json", 
                   filter_criteria: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Export data from the AIOS data pipeline.
        
        Args:
            data_type: Type of data to export
            target_format: Export format (json, csv, txt)
            filter_criteria: Criteria to filter data
            
        Returns:
            Export results
        """
        export_id = f"EXP_{int(time.time())}_{os.urandom(4).hex()[:4]}"
        
        result = {
            "export_id": export_id,
            "data_type": data_type,
            "format": target_format,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "export_path": None,
            "records_exported": 0,
            "error": None
        }
        
        try:
            # Determine source directory
            if data_type == "fragment":
                source_dir = self.fractal_cache_dir
            elif data_type == "arbiter":
                source_dir = self.arbiter_cache_dir
            elif data_type == "conversation":
                source_dir = self.conversations_dir
            elif data_type == "log":
                source_dir = self.logs_dir
            else:
                source_dir = self.temp_dir
            
            # Create export file
            export_path = self.exports_dir / f"{export_id}.{target_format}"
            
            # Export data based on format
            if target_format == "json":
                self._export_to_json(source_dir, export_path, filter_criteria)
            elif target_format == "csv":
                self._export_to_csv(source_dir, export_path, filter_criteria)
            else:
                self._export_to_text(source_dir, export_path, filter_criteria)
            
            result["success"] = True
            result["export_path"] = str(export_path)
            
            # Update pipeline stats
            self.pipeline_stats["total_operations"] += 1
            self.pipeline_stats["data_exported"] += 1
            self.pipeline_stats["last_operation"] = datetime.now().isoformat()
            self._save_pipeline_stats()
            
        except Exception as e:
            result["error"] = str(e)
        
        return result

    def _export_to_json(self, source_dir: Path, export_path: Path, filter_criteria: Dict[str, Any] = None):
        """Export data to JSON format."""
        data_list = []
        
        for file_path in source_dir.glob("*"):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if self._matches_filter(data, filter_criteria):
                            data_list.append(data)
                except:
                    pass
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2, default=str)

    def _export_to_csv(self, source_dir: Path, export_path: Path, filter_criteria: Dict[str, Any] = None):
        """Export data to CSV format."""
        import csv
        
        all_data = []
        for file_path in source_dir.glob("*"):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if self._matches_filter(data, filter_criteria):
                            all_data.append(data)
                except:
                    pass
        
        if all_data:
            fieldnames = set()
            for item in all_data:
                if isinstance(item, dict):
                    fieldnames.update(item.keys())
            
            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(fieldnames))
                writer.writeheader()
                for item in all_data:
                    if isinstance(item, dict):
                        writer.writerow(item)

    def _export_to_text(self, source_dir: Path, export_path: Path, filter_criteria: Dict[str, Any] = None):
        """Export data to text format."""
        with open(export_path, 'w', encoding='utf-8') as f:
            for file_path in source_dir.glob("*"):
                if file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as source_f:
                            content = source_f.read()
                            f.write(f"=== {file_path.name} ===\n")
                            f.write(content)
                            f.write("\n\n")
                    except:
                        pass

    def _matches_filter(self, data: Any, filter_criteria: Dict[str, Any] = None) -> bool:
        """Check if data matches filter criteria."""
        if not filter_criteria:
            return True
        
        if not isinstance(data, dict):
            return False
        
        for key, value in filter_criteria.items():
            if key not in data or data[key] != value:
                return False
        
        return True

    def get_pipeline_metrics(self) -> Dict[str, Any]:
        """Get comprehensive data pipeline metrics."""
        return {
            "pipeline_stats": self.pipeline_stats,
            "data_registry": self.data_registry,
            "directory_stats": {
                "fractal_cache": self._get_dir_stats(self.fractal_cache_dir),
                "arbiter_cache": self._get_dir_stats(self.arbiter_cache_dir),
                "conversations": self._get_dir_stats(self.conversations_dir),
                "logs": self._get_dir_stats(self.logs_dir),
                "temp": self._get_dir_stats(self.temp_dir),
                "exports": self._get_dir_stats(self.exports_dir)
            },
            "timestamp": datetime.now().isoformat()
        }

    def _get_dir_stats(self, directory: Path) -> Dict[str, Any]:
        """Get statistics for a directory."""
        if not directory.exists():
            return {"total_files": 0, "total_size_mb": 0}
        
        files = list(directory.iterdir())
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        
        return {
            "total_files": len([f for f in files if f.is_file()]),
            "total_size_mb": total_size / (1024 * 1024)
        }

# Main entry point for standalone usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AIOS Data Core System")
    parser.add_argument('--action', choices=['stats', 'overview', 'cleanup', 'backup'], 
                       default='overview', help='Action to perform')
    parser.add_argument('--days', type=int, default=30, help='Days old for cleanup')
    parser.add_argument('--dry-run', action='store_true', help='Dry run for cleanup')
    parser.add_argument('--backup-name', help='Name for backup')
    
    args = parser.parse_args()
    
    data_system = DataCore()
    
    if args.action == 'stats':
        print("📊 Fractal Cache Stats:")
        fractal_stats = data_system.get_fractal_cache_stats()
        print(f"  Files: {fractal_stats['total_files']}")
        print(f"  Size: {fractal_stats['total_size_mb']:.1f} MB")
        
        print("\n📊 Arbiter Cache Stats:")
        arbiter_stats = data_system.get_arbiter_cache_stats()
        print(f"  Files: {arbiter_stats['total_files']}")
        print(f"  Size: {arbiter_stats['total_size_mb']:.1f} MB")
        
        print("\n📊 Conversation Stats:")
        conv_stats = data_system.get_conversation_stats()
        print(f"  Conversations: {conv_stats['total_conversations']}")
        print(f"  Size: {conv_stats['total_size_mb']:.1f} MB")
        
    elif args.action == 'overview':
        overview = data_system.get_system_overview()
        print("🗄️ Data System Overview:")
        print(f"  Fractal Cache: {overview['fractal_cache']['total_files']} files, {overview['fractal_cache']['total_size_mb']:.1f} MB")
        print(f"  Arbiter Cache: {overview['arbiter_cache']['total_files']} files, {overview['arbiter_cache']['total_size_mb']:.1f} MB")
        print(f"  Conversations: {overview['conversations']['total_conversations']} files, {overview['conversations']['total_size_mb']:.1f} MB")
        print(f"  Databases: {len(overview['databases']['databases'])} databases")
        
    elif args.action == 'cleanup':
        results = data_system.cleanup_old_data(args.days, args.dry_run)
        print(f"🗑️ Cleanup Results:")
        print(f"  Total Files: {results['total_deleted']}")
        print(f"  Size Freed: {results['total_size_freed_mb']:.1f} MB")
        
    elif args.action == 'backup':
        data_system.backup_data(args.backup_name)
