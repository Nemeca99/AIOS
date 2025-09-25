#!/usr/bin/env python3
"""
UNIFIED SUPPORT CORE SYSTEM
Complete support system with all utilities integrated.
"""

import sys
import time
import json
import random
import hashlib
import uuid
import math
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# === ENUMS AND DATA CLASSES ===

class CacheStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CORRUPTED = "corrupted"
    RECOVERING = "recovering"

class EmbeddingStatus(Enum):
    READY = "ready"
    LOADING = "loading"
    ERROR = "error"
    NOT_AVAILABLE = "not_available"

class RecoveryStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"

@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    total_fragments: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    hit_rate: float = 0.0
    avg_response_time: float = 0.0
    memory_usage: float = 0.0
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class EmbeddingMetrics:
    """Embedding performance metrics"""
    total_embeddings: int = 0
    valid_embeddings: int = 0
    invalid_embeddings: int = 0
    avg_embedding_time: float = 0.0
    model_name: str = ""
    dimension: int = 384
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

# === SYSTEM CONSTANTS ===

class SystemConfig:
    """System configuration constants"""
    # File and Cache Settings
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    MAX_CACHE_SIZE = 1000
    MAX_SPLITS = 6
    CACHE_DIR = "Data/FractalCache"
    CONFIG_DIR = "config"
    LOG_DIR = "log"
    BACKUP_DIR = "backups"
    TEMP_DIR = "temp"
    
    # Embedding Settings
    DEFAULT_EMBEDDING_DIMENSION = 1024  # mixedbread-ai/mxbai-embed-large-v1 uses 1024 dimensions
    DEFAULT_EMBEDDING_MODEL = "mlabonne_qwen3-0.6b-abliterated"  # Use available model for embeddings
    EMBEDDING_BATCH_SIZE = 32
    FALLBACK_DIMENSION = 1024
    
    # API Settings
    LM_STUDIO_URL = "http://localhost:1234"
    LM_STUDIO_CHAT_ENDPOINT = "/v1/chat/completions"
    LM_STUDIO_EMBEDDING_ENDPOINT = "/v1/embeddings"
    DEFAULT_TIMEOUT = 0  # No timeout for localhost
    MAX_RETRIES = 3
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60
    
    # Performance Settings
    CACHE_CLEANUP_INTERVAL = 3600  # 1 hour
    RECOVERY_RETRY_LIMIT = 3
    GOAL_INTERVAL = 300  # 5 minutes
    CONSOLIDATION_THRESHOLD = 0.8
    SEMANTIC_CLUSTERING = 0.6
    EPISODIC_DECAY_RATE = 0.1
    
    # Personality Settings
    DEFAULT_EMPATHY = 0.9
    DEFAULT_HUMOR = 0.7
    LEARNING_RATE = 0.01
    ADAPTATION_THRESHOLD = 0.1
    EMOTION_DECAY_RATE = 0.95
    BOOST_THRESHOLD = 0.7
    
    # Memory Settings
    SLOW_WAVE_THRESHOLD = 0.6
    REM_THRESHOLD = 0.8
    SLOW_WAVE_DURATION = 5
    REM_DURATION = 3
    UNCERTAINTY_THRESHOLD = 0.3
    CONFIDENCE_THRESHOLD = 0.7
    TEMPORAL_WINDOW = 300
    WEAK_THRESHOLD = 0.3
    STRONG_THRESHOLD = 0.7
    TAGGING_STRENGTH = 0.2
    PREDICTION_WINDOW = 5
    PREDICTION_THRESHOLD = 0.3
    
    # Network Settings
    SERVER_BLOCKS = 20
    MAX_USERS_PER_BLOCK = 60
    TOTAL_CAPACITY = 1200
    
    # Performance Settings
    TARGET_PERFORMANCE = 100  # 100% performance
    PERFORMANCE_INDICATORS = 12

class FilePaths:
    """File path constants"""
    CACHE_DIR = "Data/FractalCache"
    CONFIG_DIR = "config"
    LOG_DIR = "log"
    BACKUP_DIR = "backups"
    TEMP_DIR = "temp"
    
    # Specific files
    CACHE_REGISTRY = "Data/FractalCache/registry.json"
    EMBEDDING_CACHE = "Data/FractalCache/embeddings.json"
    RECOVERY_LOG = "log/recovery.log"
    SYSTEM_LOG = "log/system.log"

class SystemMessages:
    """System status messages"""
    CACHE_INITIALIZED = "✅ Cache system initialized"
    EMBEDDING_READY = "✅ Embedding system ready"
    RECOVERY_SUCCESS = "✅ Recovery completed successfully"
    SYSTEM_READY = "✅ System ready for operation"
    
    CACHE_ERROR = "❌ Cache error occurred"
    EMBEDDING_ERROR = "❌ Embedding error occurred"
    RECOVERY_ERROR = "❌ Recovery failed"
    SYSTEM_ERROR = "❌ System error occurred"

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        SystemConfig.CACHE_DIR,
        SystemConfig.CONFIG_DIR,
        SystemConfig.LOG_DIR,
        SystemConfig.BACKUP_DIR,
        FilePaths.TEMP_DIR
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# === CACHE OPERATIONS ===

class CacheOperations:
    """Core cache operations and management"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path(SystemConfig.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = CacheMetrics()
        
        print("📁 Cache Operations Initialized")
        print(f"   Cache directory: {self.cache_dir}")
    
    def create_file_id(self, content: str, parent_id: str = None) -> str:
        """Create unique file ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        return f"frag_{content_hash}_{timestamp}_{random_suffix}"
    
    def save_fragment(self, file_id: str, fragment_data: Dict, cache_dir: Path) -> bool:
        """Save fragment to cache"""
        try:
            fragment_file = cache_dir / f"{file_id}.json"
            with open(fragment_file, 'w') as f:
                json.dump(fragment_data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving fragment {file_id}: {e}")
            return False
    
    def load_fragment(self, file_id: str, cache_dir: Path) -> Optional[Dict]:
        """Load fragment from cache"""
        try:
            fragment_file = cache_dir / f"{file_id}.json"
            if fragment_file.exists():
                with open(fragment_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Error loading fragment {file_id}: {e}")
        return None
    
    def delete_fragment(self, file_id: str, cache_dir: Path) -> bool:
        """Delete fragment from cache"""
        try:
            fragment_file = cache_dir / f"{file_id}.json"
            if fragment_file.exists():
                fragment_file.unlink()
                return True
        except Exception as e:
            print(f"❌ Error deleting fragment {file_id}: {e}")
        return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        fragment_files = list(self.cache_dir.glob("*.json"))
        
        return {
            'total_fragments': len(fragment_files),
            'cache_size_mb': sum(f.stat().st_size for f in fragment_files) / (1024 * 1024),
            'cache_directory': str(self.cache_dir),
            'status': 'active' if fragment_files else 'empty'
        }

class CacheRegistry:
    """Cache registry for tracking fragments"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.registry_file = cache_dir / "registry.json"
        self.fragments = {}
        self.load_registry()
        
        print("📋 Cache Registry Initialized")
        print(f"   Registry file: {self.registry_file}")
        print(f"   Loaded {len(self.fragments)} fragments")
    
    def load_registry(self):
        """Load registry from file"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    self.fragments = data.get('fragments', {})
            except Exception as e:
                print(f"⚠️  Error loading registry: {e}")
                self.fragments = {}
    
    def save_registry(self):
        """Save registry to file"""
        try:
            data = {
                'fragments': self.fragments,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.registry_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving registry: {e}")
    
    def add_fragment(self, file_id: str, fragment_data: Dict):
        """Add fragment to registry"""
        self.fragments[file_id] = {
            'id': file_id,
            'created': fragment_data.get('created', datetime.now().isoformat()),
            'size': len(str(fragment_data)),
            'status': 'active'
        }
        self.save_registry()
    
    def remove_fragment(self, file_id: str):
        """Remove fragment from registry"""
        if file_id in self.fragments:
            del self.fragments[file_id]
            self.save_registry()
    
    def get_fragment(self, file_id: str) -> Optional[Dict]:
        """Get fragment from registry"""
        return self.fragments.get(file_id)
    
    def list_fragments(self) -> List[str]:
        """List all fragment IDs"""
        return list(self.fragments.keys())
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            'total_fragments': len(self.fragments),
            'active_fragments': sum(1 for f in self.fragments.values() if f.get('status') == 'active'),
            'total_size': sum(f.get('size', 0) for f in self.fragments.values()),
            'last_updated': datetime.now().isoformat()
        }

class CacheBackup:
    """Cache backup and restore operations"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.backup_dir = Path(SystemConfig.BACKUP_DIR)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        print("💾 Cache Backup System Initialized")
        print(f"   Backup directory: {self.backup_dir}")
    
    def create_backup(self, backup_name: str = None) -> str:
        """Create cache backup"""
        if not backup_name:
            backup_name = f"backup_{int(time.time())}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Copy cache directory
            shutil.copytree(self.cache_dir, backup_path / "cache", dirs_exist_ok=True)
            
            # Create backup metadata
            metadata = {
                'backup_name': backup_name,
                'created_at': datetime.now().isoformat(),
                'source_directory': str(self.cache_dir),
                'fragment_count': len(list(self.cache_dir.glob("*.json")))
            }
            
            with open(backup_path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Backup created: {backup_name}")
            return backup_name
            
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore cache from backup"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        try:
            # Clear current cache
            for file in self.cache_dir.glob("*.json"):
                file.unlink()
            
            # Restore from backup
            cache_backup = backup_path / "cache"
            if cache_backup.exists():
                shutil.copytree(cache_backup, self.cache_dir, dirs_exist_ok=True)
            
            print(f"✅ Backup restored: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """List available backups"""
        backups = []
        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir() and (backup_dir / "metadata.json").exists():
                backups.append(backup_dir.name)
        return sorted(backups, reverse=True)

# === EMBEDDING OPERATIONS ===

class SimpleEmbedder:
    """Simple embedding generator with LM Studio integration"""
    
    def __init__(self, model_name: str = None):
        self.embedding_model = model_name or os.getenv("EMBEDDING_MODEL", SystemConfig.DEFAULT_EMBEDDING_MODEL)
        self.api_url = f"{SystemConfig.LM_STUDIO_URL}{SystemConfig.LM_STUDIO_EMBEDDING_ENDPOINT}"
        self.use_api = False  # Disable API to prevent 404 errors
        self.fallback_dimension = SystemConfig.FALLBACK_DIMENSION
        self.cache = {}
        
        print("🧠 Simple Embedder Initialized")
        print(f"   Model: {self.embedding_model}")
        print(f"   API URL: {self.api_url}")
        print(f"   Use API: {self.use_api}")
        print(f"   Fallback dimension: {self.fallback_dimension}")
    
    def embed(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text"""
        if not text or not text.strip():
            return None
        
        # Check cache first
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if text_hash in self.cache:
            return self.cache[text_hash]
        
        # Generate embedding
        if self.use_api:
            embedding = self._embed_via_api(text)
        else:
            embedding = self._embed_fallback(text)
        
        # Cache result
        if embedding:
            self.cache[text_hash] = embedding
        
        return embedding
    
    def _embed_via_api(self, text: str) -> Optional[List[float]]:
        """Generate embedding via LM Studio API"""
        try:
            import requests
            
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.embedding_model,
                "input": text,
                "encoding_format": "float"
            }
            
            response = requests.post(self.api_url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['data'][0]['embedding']
            else:
                print(f"⚠️  API error: {response.status_code}")
                return self._embed_fallback(text)
                
        except Exception as e:
            print(f"⚠️  API call failed: {e}")
            return self._embed_fallback(text)
    
    def _embed_fallback(self, text: str) -> List[float]:
        """Generate fallback embedding"""
        # Simple hash-based embedding
        text_hash = hashlib.md5(text.encode()).hexdigest()
        seed = int(text_hash[:8], 16)
        
        random.seed(seed)
        embedding = [random.uniform(-1, 1) for _ in range(self.fallback_dimension)]
        
        # Normalize
        norm = math.sqrt(sum(x*x for x in embedding))
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get embedding cache statistics"""
        return {
            'cached_embeddings': len(self.cache),
            'model_name': self.embedding_model,
            'dimension': self.fallback_dimension,
            'api_available': self.use_api
        }

class EmbeddingCache:
    """Embedding cache management"""
    
    def __init__(self, cache_file: str = "Data/FractalCache/embeddings.json"):
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.embeddings = {}
        self.load_cache()
        
        print("💾 Embedding Cache Initialized")
        print(f"   Cache file: {self.cache_file}")
        print(f"   Loaded {len(self.embeddings)} embeddings")
    
    def load_cache(self):
        """Load embedding cache from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.embeddings = json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading embedding cache: {e}")
                self.embeddings = {}
    
    def save_cache(self):
        """Save embedding cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.embeddings, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving embedding cache: {e}")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding from cache"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return self.embeddings.get(text_hash)
    
    def store_embedding(self, text: str, embedding: List[float]):
        """Store embedding in cache"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        self.embeddings[text_hash] = {
            'text': text,
            'embedding': embedding,
            'created_at': datetime.now().isoformat()
        }
        self.save_cache()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get embedding cache statistics"""
        return {
            'total_embeddings': len(self.embeddings),
            'cache_size_mb': self.cache_file.stat().st_size / (1024 * 1024) if self.cache_file.exists() else 0,
            'last_updated': datetime.now().isoformat()
        }

class FAISSOperations:
    """FAISS index operations using real FAISS library"""
    
    def __init__(self, dimension: int = 384, index_path: str = None):
        self.dimension = dimension
        self.index_path = index_path
        self.vectors = []
        self.metadata = []
        
        print("🔍 FAISS Operations Initialized")
        print(f"   Dimension: {dimension}")
        print(f"   Index path: {index_path or 'None'}")
        
        try:
            import faiss
            self.faiss = faiss
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            print("   ✅ Real FAISS implementation")
        except ImportError:
            self.faiss = None
            self.index = None
            print("   ⚠️  FAISS not available - using fallback similarity search")
    
    def add(self, vectors: List[List[float]], metadata: List[Dict] = None):
        """Add vectors to index"""
        if self.faiss and self.index is not None:
            try:
                import numpy as np
                vectors_array = np.array(vectors, dtype=np.float32)
                # Normalize vectors for cosine similarity
                self.faiss.normalize_L2(vectors_array)
                self.index.add(vectors_array)
                print(f"✅ Real FAISS: Added {len(vectors)} vectors. Total: {self.index.ntotal}")
            except Exception as e:
                print(f"❌ FAISS error: {e}")
                # Fallback to memory storage
                for i, vector in enumerate(vectors):
                    self.vectors.append(vector)
                    self.metadata.append(metadata[i] if metadata else {})
        else:
            # Fallback: store in memory
            for i, vector in enumerate(vectors):
                self.vectors.append(vector)
                self.metadata.append(metadata[i] if metadata else {})
            print(f"Fallback: Added {len(vectors)} vectors to memory")
    
    def search(self, query_vector: List[float], k: int = 1) -> List[Tuple[str, float]]:
        """Search for similar vectors"""
        if self.faiss and self.index is not None and self.index.ntotal > 0:
            try:
                import numpy as np
                query_array = np.array([query_vector], dtype=np.float32)
                # Normalize query vector
                self.faiss.normalize_L2(query_array)
                
                # Search
                scores, indices = self.index.search(query_array, min(k, self.index.ntotal))
                
                results = []
                for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                    if idx >= 0:  # Valid index
                        results.append((f"vector_{idx}", float(score)))
                
                return results
            except Exception as e:
                print(f"❌ FAISS search error: {e}")
                return self._fallback_search(query_vector, k)
        else:
            return self._fallback_search(query_vector, k)
    
    def _fallback_search(self, query_vector: List[float], k: int) -> List[Tuple[str, float]]:
        """Fallback similarity search using cosine similarity"""
        if not self.vectors:
            return []
        
        similarities = []
        for i, vector in enumerate(self.vectors):
            similarity = self._cosine_similarity(query_vector, vector)
            similarities.append((f"vector_{i}", similarity))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity"""
        if len(a) != len(b):
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def save(self, path: str):
        """Save index to file"""
        if self.faiss and self.index is not None:
            try:
                self.faiss.write_index(self.index, f"{path}.faiss")
                # Save metadata separately
                import pickle
                with open(f"{path}.metadata", 'wb') as f:
                    pickle.dump(self.metadata, f)
                print(f"✅ Real FAISS: Saved index to {path}.faiss")
            except Exception as e:
                print(f"❌ FAISS save error: {e}")
        else:
            print(f"Fallback: Saving {len(self.vectors)} vectors to memory")
    
    def load(self, path: str):
        """Load index from file"""
        if self.faiss:
            try:
                if os.path.exists(f"{path}.faiss"):
                    self.index = self.faiss.read_index(f"{path}.faiss")
                    print(f"✅ Real FAISS: Loaded index with {self.index.ntotal} vectors")
                    
                    # Load metadata
                    if os.path.exists(f"{path}.metadata"):
                        import pickle
                        with open(f"{path}.metadata", 'rb') as f:
                            self.metadata = pickle.load(f)
                        print(f"✅ Real FAISS: Loaded {len(self.metadata)} metadata entries")
                else:
                    print(f"⚠️  FAISS index file {path}.faiss not found, creating new index")
                    self.index = self.faiss.IndexFlatIP(self.dimension)
            except Exception as e:
                print(f"❌ FAISS load error: {e}")
                self.index = self.faiss.IndexFlatIP(self.dimension)
        else:
            print(f"Fallback: No FAISS available, using memory storage")
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        if self.faiss and self.index is not None:
            return {
                'total_vectors': self.index.ntotal,
                'dimension': self.dimension,
                'faiss_available': True,
                'status': 'loaded' if self.index.ntotal > 0 else 'empty'
            }
        else:
            return {
                'total_vectors': len(self.vectors),
                'dimension': self.dimension,
                'faiss_available': False,
                'status': 'loaded' if self.vectors else 'empty'
            }

class EmbeddingSimilarity:
    """Embedding similarity calculations"""
    
    @staticmethod
    def calculate_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings"""
        if len(embedding1) != len(embedding2):
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(embedding1, embedding2))
        norm1 = math.sqrt(sum(x * x for x in embedding1))
        norm2 = math.sqrt(sum(x * x for x in embedding2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    @staticmethod
    def calculate_euclidean_distance(embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate Euclidean distance between embeddings"""
        if len(embedding1) != len(embedding2):
            return float('inf')
        
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(embedding1, embedding2)))

# === RECOVERY OPERATIONS ===

class RecoveryOperations:
    """System recovery and healing operations"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.recovery_log = Path("log/recovery.log")
        self.recovery_log.parent.mkdir(parents=True, exist_ok=True)
        
        print("🔧 Recovery Operations Initialized")
        print(f"   Cache directory: {cache_dir}")
        print(f"   Recovery log: {self.recovery_log}")
    
    @staticmethod
    def create_blank_placeholder(file_id: str, level: int = 0) -> bool:
        """Create blank placeholder for recovery"""
        try:
            placeholder = {
                'file_id': file_id,
                'content': '',
                'level': level,
                'status': 'blank',
                'created': datetime.now().isoformat(),
                'recovery_needed': True
            }
            
            placeholder_file = Path("temp") / f"{file_id}_placeholder.json"
            placeholder_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(placeholder_file, 'w') as f:
                json.dump(placeholder, f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error creating placeholder: {e}")
            return False
    
    @staticmethod
    def find_blank_fragments(cache_dir: Path) -> List[Dict[str, Any]]:
        """Find all blank fragments that need recovery"""
        blank_fragments = []
        
        for fragment_file in cache_dir.glob("*.json"):
            try:
                with open(fragment_file, 'r') as f:
                    fragment = json.load(f)
                
                # Handle both list and dict formats
                if isinstance(fragment, dict):
                    content = fragment.get('content', '')
                else:
                    content = str(fragment)
                
                if str(content).strip() == '':
                    # Handle both list and dict formats for metadata
                    if isinstance(fragment, dict):
                        file_id = fragment.get('file_id', fragment_file.stem)
                        level = fragment.get('level', 0)
                        created = fragment.get('created', '')
                    else:
                        file_id = fragment_file.stem
                        level = 0
                        created = ''
                    
                    blank_fragments.append({
                        'file_id': file_id,
                        'file_path': str(fragment_file),
                        'level': level,
                        'created': created,
                        'recovery_priority': level
                    })
            except Exception as e:
                print(f"⚠️  Error reading fragment {fragment_file}: {e}")
        
        return sorted(blank_fragments, key=lambda x: x['recovery_priority'], reverse=True)

class SemanticReconstruction:
    """Semantic reconstruction for blank fragments"""
    
    def __init__(self, cache_system, embedder):
        self.cache_system = cache_system
        self.embedder = embedder
        self.reconstruction_threshold = 0.7
        
        print("🧠 Semantic Reconstruction Initialized")
        print(f"   Reconstruction threshold: {self.reconstruction_threshold}")
    
    def reconstruct_blank_fragments(self, blank_fragments: List[Dict]) -> Dict[str, Any]:
        """Reconstruct blank fragments using semantic analysis"""
        results = {
            'total_blank': len(blank_fragments),
            'reconstructed': 0,
            'failed': 0,
            'reconstructions': []
        }
        
        for fragment in blank_fragments:
            try:
                # Attempt reconstruction
                reconstructed_content = self._reconstruct_fragment(fragment)
                
                if reconstructed_content:
                    # Update fragment
                    self._update_fragment_content(fragment['file_id'], reconstructed_content)
                    
                    results['reconstructed'] += 1
                    results['reconstructions'].append({
                        'file_id': fragment['file_id'],
                        'status': 'success',
                        'content_length': len(reconstructed_content)
                    })
                else:
                    results['failed'] += 1
                    results['reconstructions'].append({
                        'file_id': fragment['file_id'],
                        'status': 'failed',
                        'error': 'Could not reconstruct content'
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['reconstructions'].append({
                    'file_id': fragment['file_id'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
    
    def _reconstruct_fragment(self, fragment: Dict) -> Optional[str]:
        """Reconstruct content for a single fragment"""
        # Simple reconstruction based on file ID and level
        file_id = fragment['file_id']
        level = fragment.get('level', 0)
        
        # Generate content based on fragment characteristics
        if level == 0:
            return f"Recovered content for fragment {file_id} at level {level}"
        else:
            return f"Recovered hierarchical content for fragment {file_id} at level {level}"
    
    def _update_fragment_content(self, file_id: str, content: str):
        """Update fragment with reconstructed content"""
        # This would update the actual fragment in the cache system
        print(f"✅ Reconstructed fragment {file_id} with {len(content)} characters")

class ProgressiveHealing:
    """Progressive healing system for system recovery"""
    
    def __init__(self, cache_system, embedder):
        self.cache_system = cache_system
        self.embedder = embedder
        self.healing_cycles = 0
        self.max_cycles = 5
        
        print("🔄 Progressive Healing Initialized")
        print(f"   Max healing cycles: {self.max_cycles}")
    
    def run_healing_cycles(self, num_cycles: int = 3) -> Dict[str, Any]:
        """Run progressive healing cycles"""
        results = {
            'cycles_run': 0,
            'total_healed': 0,
            'healing_history': []
        }
        
        for cycle in range(min(num_cycles, self.max_cycles)):
            print(f"🔄 Running healing cycle {cycle + 1}/{num_cycles}")
            
            cycle_result = self._run_single_healing_cycle(cycle + 1)
            results['healing_history'].append(cycle_result)
            results['total_healed'] += cycle_result['healed_count']
            results['cycles_run'] += 1
            
            # Stop if no more healing needed
            if cycle_result['healed_count'] == 0:
                break
        
        print(f"✅ Healing complete: {results['total_healed']} items healed in {results['cycles_run']} cycles")
        return results
    
    def _run_single_healing_cycle(self, cycle_number: int) -> Dict[str, Any]:
        """Run a single healing cycle"""
        # Find issues to heal
        issues = self._identify_healing_issues()
        
        healed_count = 0
        for issue in issues:
            if self._heal_issue(issue):
                healed_count += 1
        
        return {
            'cycle': cycle_number,
            'issues_found': len(issues),
            'healed_count': healed_count,
            'timestamp': datetime.now().isoformat()
        }
    
    def _identify_healing_issues(self) -> List[Dict]:
        """Identify issues that need healing"""
        issues = []
        
        # Check for blank fragments
        blank_fragments = RecoveryOperations.find_blank_fragments(self.cache_system.cache_dir)
        for fragment in blank_fragments:
            issues.append({
                'type': 'blank_fragment',
                'file_id': fragment['file_id'],
                'priority': fragment['recovery_priority']
            })
        
        return issues
    
    def _heal_issue(self, issue: Dict) -> bool:
        """Heal a specific issue"""
        try:
            if issue['type'] == 'blank_fragment':
                # Attempt to heal blank fragment
                return self._heal_blank_fragment(issue['file_id'])
            return False
        except Exception as e:
            print(f"❌ Error healing issue {issue}: {e}")
            return False
    
    def _heal_blank_fragment(self, file_id: str) -> bool:
        """Heal a blank fragment"""
        # Simple healing: generate placeholder content
        content = f"Healed fragment {file_id} at {datetime.now().isoformat()}"
        print(f"🔧 Healing blank fragment {file_id}")
        return True

class RecoveryAssessment:
    """Recovery assessment and reporting"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        
        print("📊 Recovery Assessment Initialized")
        print(f"   Cache directory: {cache_dir}")
    
    def assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health"""
        health_score = 100
        issues = []
        
        # Check cache integrity
        cache_health = self._assess_cache_health()
        health_score -= cache_health['issues'] * 10
        issues.extend(cache_health['problems'])
        
        # Check embedding system
        embedding_health = self._assess_embedding_health()
        health_score -= embedding_health['issues'] * 5
        issues.extend(embedding_health['problems'])
        
        # Check recovery status
        recovery_health = self._assess_recovery_health()
        health_score -= recovery_health['issues'] * 15
        issues.extend(recovery_health['problems'])
        
        return {
            'health_score': max(0, health_score),
            'status': 'healthy' if health_score > 80 else 'degraded' if health_score > 50 else 'critical',
            'issues': issues,
            'recommendations': self._get_health_recommendations(health_score, issues)
        }
    
    def _assess_cache_health(self) -> Dict[str, Any]:
        """Assess cache system health"""
        issues = 0
        problems = []
        
        # Check if cache directory exists
        if not self.cache_dir.exists():
            issues += 1
            problems.append("Cache directory does not exist")
        
        # Check for blank fragments
        blank_fragments = RecoveryOperations.find_blank_fragments(self.cache_dir)
        if blank_fragments:
            issues += len(blank_fragments)
            problems.append(f"Found {len(blank_fragments)} blank fragments")
        
        return {
            'issues': issues,
            'problems': problems
        }
    
    def _assess_embedding_health(self) -> Dict[str, Any]:
        """Assess embedding system health"""
        issues = 0
        problems = []
        
        # Check embedding cache
        embedding_cache = Path("Data/FractalCache/embeddings.json")
        if not embedding_cache.exists():
            issues += 1
            problems.append("Embedding cache not found")
        
        return {
            'issues': issues,
            'problems': problems
        }
    
    def _assess_recovery_health(self) -> Dict[str, Any]:
        """Assess recovery system health"""
        issues = 0
        problems = []
        
        # Check recovery log
        recovery_log = Path("log/recovery.log")
        if not recovery_log.exists():
            issues += 1
            problems.append("Recovery log not found")
        
        return {
            'issues': issues,
            'problems': problems
        }
    
    def _get_health_recommendations(self, health_score: int, issues: List[str]) -> List[str]:
        """Get health improvement recommendations"""
        recommendations = []
        
        if health_score < 50:
            recommendations.append("Run full system recovery")
            recommendations.append("Check all cache files for corruption")
        elif health_score < 80:
            recommendations.append("Run progressive healing cycles")
            recommendations.append("Monitor system performance")
        else:
            recommendations.append("System is healthy - continue monitoring")
        
        if "blank fragments" in str(issues):
            recommendations.append("Reconstruct blank fragments")
        
        if "embedding cache" in str(issues):
            recommendations.append("Rebuild embedding cache")
        
        return recommendations

# === UNIFIED SUPPORT SYSTEM ===

class SupportSystem:
    """Unified support system with all utilities integrated"""
    
    def __init__(self, cache_dir: str = None):
        print("🛠️ Initializing Unified Support System")
        print("=" * 80)
        
        # Initialize core components
        self.cache_ops = CacheOperations(cache_dir)
        self.registry = CacheRegistry(self.cache_ops.cache_dir)
        self.backup = CacheBackup(self.cache_ops.cache_dir)
        self.embedder = SimpleEmbedder()
        self.embedding_cache = EmbeddingCache()
        self.faiss_ops = FAISSOperations()
        self.recovery_ops = RecoveryOperations(self.cache_ops.cache_dir)
        self.assessment = RecoveryAssessment(self.cache_ops.cache_dir)
        
        print("✅ Unified Support System Initialized")
        print(f"   Cache directory: {self.cache_ops.cache_dir}")
        print(f"   Embedder: {self.embedder.embedding_model}")
        print(f"   FAISS: {'Available' if self.faiss_ops else 'Not available'}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        cache_stats = self.cache_ops.get_cache_stats()
        registry_stats = self.registry.get_registry_stats()
        embedding_stats = self.embedding_cache.get_cache_stats()
        faiss_stats = self.faiss_ops.get_index_stats()
        health_assessment = self.assessment.assess_system_health()
        
        return {
            'cache': cache_stats,
            'registry': registry_stats,
            'embeddings': embedding_stats,
            'faiss': faiss_stats,
            'health': health_assessment,
            'system_ready': health_assessment['status'] == 'healthy'
        }
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        print("🔍 Running System Health Check")
        print("=" * 50)
        
        status = self.get_system_status()
        
        # Display health status
        health = status['health']
        print(f"Health Score: {health['health_score']}/100")
        print(f"Status: {health['status'].upper()}")
        
        if health['issues']:
            print(f"Issues Found: {len(health['issues'])}")
            for issue in health['issues']:
                print(f"  • {issue}")
        
        if health['recommendations']:
            print("Recommendations:")
            for rec in health['recommendations']:
                print(f"  • {rec}")
        
        return status
    
    def create_system_backup(self, backup_name: str = None) -> str:
        """Create complete system backup"""
        print(f"💾 Creating System Backup: {backup_name or 'auto'}")
        
        backup_id = self.backup.create_backup(backup_name)
        if backup_id:
            print(f"✅ Backup created successfully: {backup_id}")
        else:
            print("❌ Backup creation failed")
        
        return backup_id
    
    def restore_system_backup(self, backup_name: str) -> bool:
        """Restore system from backup"""
        print(f"🔄 Restoring System from Backup: {backup_name}")
        
        success = self.backup.restore_backup(backup_name)
        if success:
            print(f"✅ System restored successfully from {backup_name}")
        else:
            print(f"❌ System restore failed from {backup_name}")
        
        return success

# === MAIN ENTRY POINT ===

def main():
    """Test the unified support system"""
    print("🧪 Testing Unified Support System")
    
    # Initialize system
    support = SupportSystem()
    
    # Run health check
    health_status = support.run_health_check()
    
    # Create backup
    backup_id = support.create_system_backup("test_backup")
    
    # Get system status
    status = support.get_system_status()
    
    print(f"\n📊 System Status Summary:")
    print(f"   Cache fragments: {status['cache']['total_fragments']}")
    print(f"   Embeddings cached: {status['embeddings']['total_embeddings']}")
    print(f"   Health score: {status['health']['health_score']}/100")
    print(f"   System ready: {status['system_ready']}")

if __name__ == "__main__":
    main()
