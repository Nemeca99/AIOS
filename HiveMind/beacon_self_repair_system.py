#!/usr/bin/env python3
"""
CARMA Beacon Self-Repair System
Implements the beacon ping system and deep dream recovery
"""

import json
import time
import random
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict

class BeaconSelfRepairSystem:
    def __init__(self, cache_dir: str = "Data/FractalCache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Network topology
        self.network_map = {}  # file_id -> status info
        self.file_relationships = {}  # file_id -> {parents: [], children: []}
        self.blank_files = {}  # file_id -> blank file info
        
        # Recovery settings
        self.max_blank_files = 100  # Maximum blank files before system fails
        self.recovery_priority_weights = {
            'root': 10.0,
            'level_1': 8.0,
            'level_2': 6.0,
            'level_3': 4.0,
            'level_4': 2.0,
            'level_5': 1.0,
            'level_6': 0.5
        }
        
        print("🌐 Beacon Self-Repair System Initialized")
        print(f"   Cache directory: {self.cache_dir}")
        print(f"   Max blank files: {self.max_blank_files}")
    
    def ping_network(self, start_file_id: str = None) -> Dict:
        """Ping the network like sonar to discover topology"""
        print(f"🌐 Beacon Ping: Starting network discovery")
        
        # Find a starting file if none provided
        if not start_file_id:
            start_file_id = self._find_starting_file()
            if not start_file_id:
                print("   ❌ No files found to start ping")
                return {}
        
        # Reset network map
        self.network_map = {}
        ping_queue = [start_file_id]
        visited = set()
        
        while ping_queue:
            current_id = ping_queue.pop(0)
            if current_id in visited:
                continue
                
            visited.add(current_id)
            
            # Ping current file
            status = self._ping_file(current_id)
            self.network_map[current_id] = status
            
            # Get children and parents
            children = self._get_children(current_id)
            parents = self._get_parents(current_id)
            
            # Add to ping queue
            for child in children:
                if child not in visited:
                    ping_queue.append(child)
            for parent in parents:
                if parent not in visited:
                    ping_queue.append(parent)
        
        print(f"   ✅ Network discovery complete: {len(self.network_map)} files found")
        return self.network_map
    
    def _ping_file(self, file_id: str) -> Dict:
        """Ping a single file for status"""
        file_path = self.cache_dir / f"{file_id}.json"
        
        status = {
            'id': file_id,
            'exists': file_path.exists(),
            'accessible': False,
            'corrupted': False,
            'size': 0,
            'last_modified': None,
            'level': self._get_file_level(file_id)
        }
        
        if status['exists']:
            try:
                # Check if file is accessible and not corrupted
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                status['accessible'] = True
                status['size'] = file_path.stat().st_size
                status['last_modified'] = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                
                # Check for corruption indicators
                if not self._validate_file_structure(data):
                    status['corrupted'] = True
                    status['accessible'] = False
                    
            except Exception as e:
                status['corrupted'] = True
                status['error'] = str(e)
        
        return status
    
    def _validate_file_structure(self, data: Dict) -> bool:
        """Validate file structure for corruption"""
        required_fields = ['id', 'content', 'created', 'last_accessed']
        return all(field in data for field in required_fields)
    
    def _get_file_level(self, file_id: str) -> int:
        """Determine file level from ID pattern"""
        if file_id.startswith('root_'):
            return 0
        elif '_split_' in file_id:
            # Count splits to determine level
            return file_id.count('_split_')
        else:
            return 0
    
    def _get_children(self, file_id: str) -> List[str]:
        """Get children of a file"""
        children = []
        file_path = self.cache_dir / f"{file_id}.json"
        
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                children = data.get('children', [])
            except:
                pass
        
        return children
    
    def _get_parents(self, file_id: str) -> List[str]:
        """Get parents of a file"""
        parents = []
        file_path = self.cache_dir / f"{file_id}.json"
        
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                parents = data.get('parents', [])
            except:
                pass
        
        return parents
    
    def _find_starting_file(self) -> Optional[str]:
        """Find a file to start the ping from"""
        # Look for root files first
        for file_path in self.cache_dir.glob("root_*.json"):
            return file_path.stem
        
        # If no root files, pick any file
        files = list(self.cache_dir.glob("*.json"))
        if files:
            return files[0].stem
        
        return None
    
    def validate_path(self, path: List[str]) -> Tuple[bool, List[str]]:
        """Check if all files in path exist and are accessible"""
        missing_files = []
        
        for file_id in path:
            if file_id not in self.network_map:
                missing_files.append(file_id)
            elif not self.network_map[file_id]['accessible']:
                missing_files.append(file_id)
        
        return len(missing_files) == 0, missing_files
    
    def create_blank_placeholder(self, missing_file_id: str) -> str:
        """Create temporary file with blank flag"""
        blank_file = {
            'id': missing_file_id,
            'content': '',
            'status': 'blank',
            'created': datetime.now().isoformat(),
            'recovery_priority': self._calculate_priority(missing_file_id),
            'parent_id': self._get_parent_id(missing_file_id),
            'children_ids': self._get_children_ids(missing_file_id),
            'blank_created': datetime.now().isoformat()
        }
        
        # Save blank file
        file_path = self.cache_dir / f"{missing_file_id}.json"
        with open(file_path, 'w') as f:
            json.dump(blank_file, f, indent=2)
        
        self.blank_files[missing_file_id] = blank_file
        
        print(f"   📝 Created blank placeholder: {missing_file_id}")
        return missing_file_id
    
    def _calculate_priority(self, file_id: str) -> float:
        """Calculate recovery priority for a file"""
        level = self._get_file_level(file_id)
        level_key = f'level_{level}' if level > 0 else 'root'
        base_priority = self.recovery_priority_weights.get(level_key, 1.0)
        
        # Add random factor to break ties
        random_factor = random.uniform(0.8, 1.2)
        
        return base_priority * random_factor
    
    def _get_parent_id(self, file_id: str) -> Optional[str]:
        """Get parent ID for a file"""
        # Try to infer from file ID pattern
        if '_split_' in file_id:
            parts = file_id.split('_split_')
            if len(parts) > 1:
                return parts[0]
        return None
    
    def _get_children_ids(self, file_id: str) -> List[str]:
        """Get children IDs for a file"""
        # Try to find children by looking for files that start with this ID
        children = []
        for other_file in self.cache_dir.glob("*.json"):
            if other_file.stem.startswith(file_id + "_split_"):
                children.append(other_file.stem)
        return children
    
    def deep_dream_recovery(self) -> Dict:
        """Rebuild system during deep dream cycle"""
        blank_files = self._find_blank_files()
        
        if not blank_files:
            print("   🌙 No blank files to recover")
            return {'recovered': 0, 'failed': 0, 'duration': 0}
        
        print(f"   🌙 Deep Dream Recovery: Rebuilding {len(blank_files)} blank files")
        
        start_time = time.time()
        recovered = 0
        failed = 0
        
        # Sort by priority (most important first)
        blank_files.sort(key=lambda x: x['recovery_priority'], reverse=True)
        
        for blank_file in blank_files:
            try:
                # Rebuild from context
                reconstructed_content = self._reconstruct_from_context(blank_file)
                
                # Update file
                blank_file['content'] = reconstructed_content
                blank_file['status'] = 'reconstructed'
                blank_file['reconstructed'] = datetime.now().isoformat()
                
                # Save updated file
                file_path = self.cache_dir / f"{blank_file['id']}.json"
                with open(file_path, 'w') as f:
                    json.dump(blank_file, f, indent=2)
                
                # Remove from blank files
                if blank_file['id'] in self.blank_files:
                    del self.blank_files[blank_file['id']]
                
                recovered += 1
                print(f"      ✅ Reconstructed: {blank_file['id']}")
                
            except Exception as e:
                failed += 1
                print(f"      ❌ Failed to reconstruct {blank_file['id']}: {e}")
                # Keep as blank for next cycle
        
        duration = time.time() - start_time
        
        result = {
            'recovered': recovered,
            'failed': failed,
            'duration': duration,
            'remaining_blank': len(self._find_blank_files())
        }
        
        print(f"   🌙 Deep Dream Recovery Complete: {recovered} recovered, {failed} failed in {duration:.2f}s")
        return result
    
    def _find_blank_files(self) -> List[Dict]:
        """Find all blank files in the system"""
        blank_files = []
        
        for file_path in self.cache_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if data.get('status') == 'blank':
                    blank_files.append(data)
                    
            except:
                # Skip corrupted files
                continue
        
        return blank_files
    
    def _reconstruct_from_context(self, blank_file: Dict) -> str:
        """Reconstruct content from context and related files"""
        file_id = blank_file['id']
        level = self._get_file_level(file_id)
        
        # Try to reconstruct from parent
        parent_id = blank_file.get('parent_id')
        if parent_id and parent_id in self.network_map:
            parent_content = self._get_file_content(parent_id)
            if parent_content:
                # Create a simplified version based on parent
                return f"Reconstructed from parent {parent_id}: {parent_content[:100]}..."
        
        # Try to reconstruct from children
        children_ids = blank_file.get('children_ids', [])
        if children_ids:
            child_content = self._get_file_content(children_ids[0])
            if child_content:
                return f"Reconstructed from child {children_ids[0]}: {child_content[:100]}..."
        
        # Fallback: create generic content
        return f"Reconstructed content for {file_id} at level {level} - {datetime.now().isoformat()}"
    
    def _get_file_content(self, file_id: str) -> Optional[str]:
        """Get content from a file"""
        file_path = self.cache_dir / f"{file_id}.json"
        
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return data.get('content', '')
            except:
                pass
        
        return None
    
    def calculate_dream_cycle_duration(self) -> float:
        """Calculate how long deep dream cycle should take"""
        base_duration = 5.0  # Base 5 seconds
        total_files = len(self.network_map)
        blank_files = len(self._find_blank_files())
        
        complexity_factor = total_files * 0.1  # 0.1s per file
        blank_files_factor = blank_files * 2.0  # 2s per blank file
        
        total_duration = base_duration + complexity_factor + blank_files_factor
        
        print(f"   🌙 Deep Dream Duration: {total_duration:.1f}s")
        print(f"      Base: {base_duration}s")
        print(f"      Complexity: {complexity_factor:.1f}s ({total_files} files)")
        print(f"      Recovery: {blank_files_factor:.1f}s ({blank_files} blank files)")
        
        return total_duration
    
    def check_system_health(self) -> Dict:
        """Check overall system health"""
        total_files = len(self.network_map)
        accessible_files = sum(1 for f in self.network_map.values() if f['accessible'])
        corrupted_files = sum(1 for f in self.network_map.values() if f['corrupted'])
        blank_files = len(self._find_blank_files())
        
        health_score = (accessible_files / total_files) * 100 if total_files > 0 else 0
        
        # Check if system is too corrupted
        corruption_threshold = 0.7  # 70% corruption threshold
        corruption_ratio = (corrupted_files + blank_files) / total_files if total_files > 0 else 0
        
        is_operational = corruption_ratio < corruption_threshold and blank_files < self.max_blank_files
        
        health = {
            'total_files': total_files,
            'accessible_files': accessible_files,
            'corrupted_files': corrupted_files,
            'blank_files': blank_files,
            'health_score': health_score,
            'corruption_ratio': corruption_ratio,
            'is_operational': is_operational,
            'max_blank_files': self.max_blank_files,
            'corruption_threshold': corruption_threshold
        }
        
        print(f"   🏥 System Health Check:")
        print(f"      Total files: {total_files}")
        print(f"      Accessible: {accessible_files}")
        print(f"      Corrupted: {corrupted_files}")
        print(f"      Blank: {blank_files}")
        print(f"      Health score: {health_score:.1f}%")
        print(f"      Corruption ratio: {corruption_ratio:.1%}")
        print(f"      Operational: {'✅' if is_operational else '❌'}")
        
        return health
    
    def execute_with_fallback(self, query: str, paths: List[List[str]]) -> Tuple[bool, str, List[str]]:
        """Execute query with fallback strategies"""
        print(f"   🔍 Executing query with fallback: {query[:50]}...")
        
        # Try each path in order
        for i, path in enumerate(paths):
            is_valid, missing_files = self.validate_path(path)
            
            if is_valid:
                print(f"      ✅ Using path {i+1}: {len(path)} files")
                return True, f"Executed using path {i+1}", []
            
            print(f"      ❌ Path {i+1} blocked: {len(missing_files)} missing files")
            
            # Create blank placeholders for missing files
            for missing_file in missing_files:
                self.create_blank_placeholder(missing_file)
        
        # All paths failed
        print(f"      ❌ All paths failed, system may be too corrupted")
        return False, "All paths failed", []
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        health = self.check_system_health()
        dream_duration = self.calculate_dream_cycle_duration()
        
        return {
            'health': health,
            'dream_duration': dream_duration,
            'network_map_size': len(self.network_map),
            'blank_files_count': len(self._find_blank_files()),
            'timestamp': datetime.now().isoformat()
        }
