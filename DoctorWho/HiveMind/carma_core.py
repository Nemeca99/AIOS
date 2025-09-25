#!/usr/bin/env python3
"""
CARMA Core - Single Entry Point
Main entry point for the CARMA system
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Import all operations
try:
    from .cache_operations import CacheOperations, CacheRegistry, CacheBackup
    from .embedding_operations import EmbeddingOperations, EmbeddingCache, FAISSOperations, EmbeddingSimilarity
    from .recovery_operations import RecoveryOperations, SemanticReconstruction, ProgressiveHealing, RecoveryAssessment
    from .system_constants import SystemConfig, FilePaths, SystemMessages, ensure_directories
except ImportError:
    # Fallback for direct execution
    from cache_operations import CacheOperations, CacheRegistry, CacheBackup
    from embedding_operations import EmbeddingOperations, EmbeddingCache, FAISSOperations, EmbeddingSimilarity
    from recovery_operations import RecoveryOperations, SemanticReconstruction, ProgressiveHealing, RecoveryAssessment
    from system_constants import SystemConfig, FilePaths, SystemMessages, ensure_directories

class CARMACore:
    """Main CARMA system entry point"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize CARMA system"""
        # Ensure directories exist
        ensure_directories()
        
        # Set up paths
        self.cache_dir = Path(cache_dir) if cache_dir else Path(FilePaths.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.cache_ops = CacheOperations()
        self.registry = CacheRegistry(self.cache_dir)
        self.backup = CacheBackup(self.cache_dir)
        self.embedding_cache = EmbeddingCache()
        self.faiss_ops = FAISSOperations()
        
        print(SystemMessages.CACHE_INITIALIZED)
    
    # === CACHE OPERATIONS ===
    
    def add_fragment(self, content: str, parent_id: Optional[str] = None, 
                    level: int = 0, metadata: Optional[Dict] = None) -> str:
        """Add a new fragment to the cache"""
        file_id = self.cache_ops.create_file_id(content, parent_id)
        
        fragment_data = {
            "id": file_id,
            "content": content,
            "level": level,
            "hits": 0,
            "parent_id": parent_id,
            "children_ids": [],
            "created_at": str(Path().cwd()),
            "metadata": metadata or {}
        }
        
        if self.cache_ops.save_fragment(file_id, fragment_data, self.cache_dir):
            self.registry.add_fragment(file_id, fragment_data)
            return file_id
        return ""
    
    def get_fragment(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get fragment by ID"""
        return self.registry.get_fragment(file_id)
    
    def delete_fragment(self, file_id: str) -> bool:
        """Delete fragment by ID"""
        if self.cache_ops.delete_fragment(file_id, self.cache_dir):
            self.registry.remove_fragment(file_id)
            return True
        return False
    
    def list_fragments(self) -> List[str]:
        """List all fragment IDs"""
        return self.registry.list_fragments()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.registry.get_registry_stats()
    
    def search_fragments(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for fragments using semantic similarity"""
        try:
            # Get query embedding
            query_embedding = self.embed_text(query)
            if not query_embedding:
                return []
            
            # Find similar fragments
            similar_fragments = self.find_similar_fragments(query_embedding, top_k=limit)
            
            # Format results
            results = []
            for fragment_id, similarity in similar_fragments:
                fragment = self.get_fragment(fragment_id)
                if fragment:
                    fragment['similarity'] = similarity
                    results.append(fragment)
            
            return results
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    # === ALIAS METHODS FOR COMPATIBILITY ===
    
    def store_fragment(self, fragment_id: str, fragment_data: Dict) -> bool:
        """Store a fragment (alias for add_fragment)"""
        try:
            # Extract content and metadata
            content = fragment_data.get("content", "")
            parent_id = fragment_data.get("parent_id")
            level = fragment_data.get("level", 0)
            metadata = fragment_data.get("metadata", {})
            
            # Add the fragment
            file_id = self.add_fragment(content, parent_id, level, metadata)
            return file_id == fragment_id
        except Exception as e:
            print(f"❌ Failed to store fragment {fragment_id}: {e}")
            return False
    
    def query_fragments(self, query: str, limit: int = 10) -> List[Dict]:
        """Query fragments (alias for search_fragments)"""
        return self.search_fragments(query, limit)
    
    # === EMBEDDING OPERATIONS ===
    
    def embed_text(self, text: str, model_name: Optional[str] = None) -> Optional[List[float]]:
        """Embed text using the configured model"""
        # This would integrate with your actual embedder
        # For now, return a placeholder
        return [0.0] * 384  # Placeholder embedding
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate similarity between two embeddings"""
        import numpy as np
        return EmbeddingOperations.calculate_cosine_similarity(
            np.array(embedding1), np.array(embedding2)
        )
    
    def find_similar_fragments(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        """Find similar fragments using FAISS"""
        import numpy as np
        return self.faiss_ops.search(np.array(query_embedding), top_k)
    
    # === RECOVERY OPERATIONS ===
    
    def create_blank_placeholder(self, file_id: str, level: int = 0) -> bool:
        """Create blank placeholder for recovery"""
        return RecoveryOperations.create_blank_placeholder(file_id, level, self.cache_dir)
    
    def find_blank_fragments(self) -> List[Dict[str, Any]]:
        """Find all blank fragments"""
        return RecoveryOperations.find_blank_fragments(self.cache_dir)
    
    def reconstruct_fragments(self, blank_fragments: List[Dict[str, Any]], 
                            embedder) -> Dict[str, Any]:
        """Reconstruct blank fragments"""
        reconstruction = SemanticReconstruction(self, embedder)
        return reconstruction.reconstruct_blank_fragments(blank_fragments)
    
    def run_progressive_healing(self, num_cycles: int = 3, embedder=None) -> Dict[str, Any]:
        """Run progressive healing cycles"""
        if embedder is None:
            print("❌ Embedder required for progressive healing")
            return {}
        
        healing = ProgressiveHealing(self, embedder)
        return healing.run_healing_cycles(num_cycles)
    
    # === BACKUP OPERATIONS ===
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Create system backup"""
        return self.backup.create_backup(backup_name)
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from backup"""
        return self.backup.restore_backup(backup_name)
    
    def list_backups(self) -> List[str]:
        """List available backups"""
        return self.backup.list_backups()
    
    # === SYSTEM OPERATIONS ===
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        cache_stats = self.get_cache_stats()
        faiss_stats = self.faiss_ops.get_index_stats()
        embedding_stats = self.embedding_cache.get_cache_stats()
        
        return {
            "cache": cache_stats,
            "faiss": faiss_stats,
            "embeddings": embedding_stats,
            "system_ready": faiss_stats.get("status") == "loaded"
        }
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run system health check"""
        status = self.get_system_status()
        
        # Check if system is healthy
        healthy = (
            status["cache"]["total_fragments"] > 0 and
            status["faiss"]["status"] == "loaded" and
            status["embeddings"]["valid_embeddings"] > 0
        )
        
        return {
            "healthy": healthy,
            "status": status,
            "recommendations": self._get_health_recommendations(status)
        }
    
    def _get_health_recommendations(self, status: Dict[str, Any]) -> List[str]:
        """Get health recommendations"""
        recommendations = []
        
        if status["cache"]["total_fragments"] == 0:
            recommendations.append("Add some fragments to the cache")
        
        if status["faiss"]["status"] != "loaded":
            recommendations.append("Rebuild FAISS index")
        
        if status["embeddings"]["valid_embeddings"] == 0:
            recommendations.append("Generate embeddings for fragments")
        
        return recommendations

# === CONVENIENCE FUNCTIONS ===

def create_carma_system(cache_dir: Optional[str] = None) -> CARMACore:
    """Create a new CARMA system instance"""
    return CARMACore(cache_dir)

def quick_test() -> Dict[str, Any]:
    """Run a quick system test"""
    carma = create_carma_system()
    
    # Add test fragments
    test_contents = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks with multiple layers",
        "Natural language processing deals with human language",
        "Computer vision enables machines to interpret visual information"
    ]
    
    fragment_ids = []
    for content in test_contents:
        frag_id = carma.add_fragment(content)
        if frag_id:
            fragment_ids.append(frag_id)
    
    # Run health check
    health = carma.run_health_check()
    
    return {
        "fragments_added": len(fragment_ids),
        "fragment_ids": fragment_ids,
        "health_check": health
    }

if __name__ == "__main__":
    # Run quick test
    print("🧪 Running CARMA quick test...")
    results = quick_test()
    
    print(f"✅ Test completed:")
    print(f"   Fragments added: {results['fragments_added']}")
    print(f"   System healthy: {results['health_check']['healthy']}")
    
    if results['health_check']['recommendations']:
        print("   Recommendations:")
        for rec in results['health_check']['recommendations']:
            print(f"     • {rec}")
