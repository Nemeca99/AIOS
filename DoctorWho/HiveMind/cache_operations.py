#!/usr/bin/env python3
"""
Cache Operations Module
Centralized cache-related operations and utilities
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from system_constants import CacheConfig, FilePaths, FileExtensions, DefaultValues

class CacheOperations:
    """Centralized cache operations"""
    
    @staticmethod
    def create_file_id(content: str, parent_id: Optional[str] = None) -> str:
        """Create unique file ID based on content and parent"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:CacheConfig.CONTENT_HASH_LENGTH]
        if parent_id:
            return f"{parent_id}_split_{content_hash}"
        return f"root_{content_hash}"
    
    @staticmethod
    def save_fragment(file_id: str, fragment_data: Dict[str, Any], base_dir: Path) -> bool:
        """Save fragment data to file"""
        try:
            fragment_file = base_dir / f"{file_id}{FileExtensions.JSON}"
            with open(fragment_file, 'w') as f:
                json.dump(fragment_data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to save fragment {file_id}: {e}")
            return False
    
    @staticmethod
    def load_fragment(file_id: str, base_dir: Path) -> Optional[Dict[str, Any]]:
        """Load fragment data from file"""
        try:
            file_path = base_dir / f"{file_id}{FileExtensions.JSON}"
            if not file_path.exists():
                return None
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load fragment {file_id}: {e}")
            return None
    
    @staticmethod
    def delete_fragment(file_id: str, base_dir: Path) -> bool:
        """Delete fragment file"""
        try:
            file_path = base_dir / f"{file_id}{FileExtensions.JSON}"
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to delete fragment {file_id}: {e}")
            return False
    
    @staticmethod
    def list_fragments(base_dir: Path) -> List[str]:
        """List all fragment files in directory"""
        try:
            return [f.stem for f in base_dir.glob(f"*{FileExtensions.JSON}")]
        except Exception as e:
            print(f"❌ Failed to list fragments: {e}")
            return []
    
    @staticmethod
    def create_blank_placeholder(file_id: str, level: int, base_dir: Path) -> bool:
        """Create blank placeholder file"""
        try:
            placeholder_data = {
                "id": file_id,
                "content": "",
                "level": level,
                "hits": DefaultValues.DEFAULT_HITS,
                "blank": True,
                "created_at": str(Path().cwd()),
                "placeholder_prompt": DefaultValues.DEFAULT_PLACEHOLDER_PROMPT.format(
                    file_id=file_id, level=level
                )
            }
            return CacheOperations.save_fragment(file_id, placeholder_data, base_dir)
        except Exception as e:
            print(f"❌ Failed to create blank placeholder {file_id}: {e}")
            return False
    
    @staticmethod
    def validate_fragment_data(data: Dict[str, Any]) -> bool:
        """Validate fragment data structure"""
        required_fields = ["id", "content", "level"]
        return all(field in data for field in required_fields)
    
    @staticmethod
    def get_fragment_size(file_id: str, base_dir: Path) -> int:
        """Get fragment file size in bytes"""
        try:
            file_path = base_dir / f"{file_id}{FileExtensions.JSON}"
            return file_path.stat().st_size if file_path.exists() else 0
        except Exception:
            return 0
    
    @staticmethod
    def is_blank_fragment(data: Dict[str, Any]) -> bool:
        """Check if fragment is blank placeholder"""
        return data.get("blank", False) or not data.get("content", "").strip()
    
    @staticmethod
    def should_split_fragment(data: Dict[str, Any], base_dir: Path) -> bool:
        """Check if fragment should be split"""
        file_id = data.get("id", "")
        content_length = len(data.get("content", ""))
        file_size = CacheOperations.get_fragment_size(file_id, base_dir)
        
        return (
            content_length > CacheConfig.MAX_FILE_SIZE * CacheConfig.SPLIT_THRESHOLD or
            file_size > CacheConfig.MAX_FILE_SIZE * CacheConfig.SPLIT_THRESHOLD
        )
    
    @staticmethod
    def split_content(content: str, max_parts: int = CacheConfig.MAX_SPLITS) -> List[str]:
        """Split content into multiple parts"""
        if not content or max_parts <= 1:
            return [content]
        
        # Simple splitting by length
        part_length = len(content) // max_parts
        parts = []
        
        for i in range(max_parts):
            start = i * part_length
            end = start + part_length if i < max_parts - 1 else len(content)
            parts.append(content[start:end])
        
        return [part for part in parts if part.strip()]

class CacheRegistry:
    """Cache registry management"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.registry_file = base_dir / f"registry{FileExtensions.JSON}"
        self.registry = {}
        self.load_registry()
    
    def load_registry(self) -> None:
        """Load registry from file"""
        try:
            if self.registry_file.exists():
                with open(self.registry_file, 'r') as f:
                    self.registry = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load registry: {e}")
            self.registry = {}
    
    def save_registry(self) -> bool:
        """Save registry to file"""
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(self.registry, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to save registry: {e}")
            return False
    
    def add_fragment(self, file_id: str, data: Dict[str, Any]) -> None:
        """Add fragment to registry"""
        self.registry[file_id] = data
    
    def remove_fragment(self, file_id: str) -> None:
        """Remove fragment from registry"""
        if file_id in self.registry:
            del self.registry[file_id]
    
    def get_fragment(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get fragment from registry"""
        return self.registry.get(file_id)
    
    def list_fragments(self) -> List[str]:
        """List all fragment IDs in registry"""
        return list(self.registry.keys())
    
    def get_fragments_by_level(self, level: int) -> List[str]:
        """Get fragments by level"""
        return [
            file_id for file_id, data in self.registry.items()
            if data.get("level", 0) == level
        ]
    
    def get_blank_fragments(self) -> List[str]:
        """Get all blank fragments"""
        return [
            file_id for file_id, data in self.registry.items()
            if CacheOperations.is_blank_fragment(data)
        ]
    
    def get_fragments_by_hits(self, min_hits: int = 0) -> List[str]:
        """Get fragments by minimum hit count"""
        return [
            file_id for file_id, data in self.registry.items()
            if data.get("hits", 0) >= min_hits
        ]
    
    def update_fragment(self, file_id: str, updates: Dict[str, Any]) -> bool:
        """Update fragment data"""
        if file_id in self.registry:
            self.registry[file_id].update(updates)
            return True
        return False
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        total_fragments = len(self.registry)
        blank_fragments = len(self.get_blank_fragments())
        levels = {}
        
        for data in self.registry.values():
            level = data.get("level", 0)
            levels[level] = levels.get(level, 0) + 1
        
        return {
            "total_fragments": total_fragments,
            "blank_fragments": blank_fragments,
            "active_fragments": total_fragments - blank_fragments,
            "levels": levels,
            "max_level": max(levels.keys()) if levels else 0
        }

class CacheBackup:
    """Cache backup and restore operations"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.backup_dir = Path(FilePaths.BACKUP_DIR)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Create a backup of the cache"""
        import time
        from datetime import datetime
        
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"carma_backup_{timestamp}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Backup registry
            registry_file = self.base_dir / f"registry{FileExtensions.JSON}"
            if registry_file.exists():
                import shutil
                shutil.copy2(registry_file, backup_path / f"registry{FileExtensions.JSON}")
            
            # Backup fragments
            fragments_dir = backup_path / "fragments"
            fragments_dir.mkdir(exist_ok=True)
            
            for fragment_file in self.base_dir.glob(f"*{FileExtensions.JSON}"):
                if fragment_file.name != "registry.json":
                    shutil.copy2(fragment_file, fragments_dir / fragment_file.name)
            
            # Create manifest
            manifest = {
                "backup_name": backup_name,
                "created_at": datetime.now().isoformat(),
                "fragment_count": len(list(self.base_dir.glob(f"*{FileExtensions.JSON}"))) - 1,
                "base_dir": str(self.base_dir)
            }
            
            with open(backup_path / "manifest.json", 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"✅ Backup created: {backup_name}")
            return backup_name
            
        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return ""
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore cache from backup"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        try:
            import shutil
            
            # Restore registry
            registry_backup = backup_path / f"registry{FileExtensions.JSON}"
            if registry_backup.exists():
                shutil.copy2(registry_backup, self.base_dir / f"registry{FileExtensions.JSON}")
            
            # Restore fragments
            fragments_backup = backup_path / "fragments"
            if fragments_backup.exists():
                for fragment_file in fragments_backup.glob(f"*{FileExtensions.JSON}"):
                    shutil.copy2(fragment_file, self.base_dir / fragment_file.name)
            
            print(f"✅ Backup restored: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to restore backup: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """List available backups"""
        try:
            return [d.name for d in self.backup_dir.iterdir() if d.is_dir()]
        except Exception:
            return []
    
    def delete_backup(self, backup_name: str) -> bool:
        """Delete a backup"""
        try:
            import shutil
            backup_path = self.backup_dir / backup_name
            if backup_path.exists():
                shutil.rmtree(backup_path)
                print(f"✅ Backup deleted: {backup_name}")
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to delete backup: {e}")
            return False
