#!/usr/bin/env python3
"""
Embedding Operations Module
Centralized embedding-related operations and utilities
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from system_constants import EmbeddingConfig, FilePaths, ModelConfig, PerformanceConfig

class EmbeddingOperations:
    """Centralized embedding operations"""
    
    @staticmethod
    def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
        """Normalize embedding vector for cosine similarity"""
        try:
            import faiss
            # Use FAISS normalization for consistency
            normalized = embedding.reshape(1, -1).astype('float32')
            faiss.normalize_L2(normalized)
            return normalized.flatten()
        except ImportError:
            # Fallback to numpy normalization
            norm = np.linalg.norm(embedding)
            return embedding / norm if norm > 0 else embedding
    
    @staticmethod
    def calculate_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            # Normalize both embeddings
            norm1 = EmbeddingOperations.normalize_embedding(embedding1)
            norm2 = EmbeddingOperations.normalize_embedding(embedding2)
            
            # Calculate cosine similarity
            similarity = np.dot(norm1, norm2)
            return float(similarity)
        except Exception as e:
            print(f"❌ Failed to calculate cosine similarity: {e}")
            return 0.0
    
    @staticmethod
    def calculate_similarity_matrix(embeddings: List[np.ndarray]) -> np.ndarray:
        """Calculate similarity matrix for a list of embeddings"""
        try:
            n = len(embeddings)
            similarity_matrix = np.zeros((n, n))
            
            for i in range(n):
                for j in range(n):
                    if i == j:
                        similarity_matrix[i][j] = 1.0
                    else:
                        similarity_matrix[i][j] = EmbeddingOperations.calculate_cosine_similarity(
                            embeddings[i], embeddings[j]
                        )
            
            return similarity_matrix
        except Exception as e:
            print(f"❌ Failed to calculate similarity matrix: {e}")
            return np.zeros((len(embeddings), len(embeddings)))
    
    @staticmethod
    def find_most_similar(embedding: np.ndarray, candidate_embeddings: List[np.ndarray], 
                         top_k: int = EmbeddingConfig.DEFAULT_TOP_K) -> List[Tuple[int, float]]:
        """Find most similar embeddings"""
        try:
            similarities = []
            for i, candidate in enumerate(candidate_embeddings):
                similarity = EmbeddingOperations.calculate_cosine_similarity(embedding, candidate)
                similarities.append((i, similarity))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        except Exception as e:
            print(f"❌ Failed to find most similar embeddings: {e}")
            return []
    
    @staticmethod
    def validate_embedding(embedding: np.ndarray) -> bool:
        """Validate embedding vector"""
        try:
            # Check if it's a numpy array
            if not isinstance(embedding, np.ndarray):
                return False
            
            # Check dimension
            if len(embedding.shape) != 1:
                return False
            
            # Check for NaN values
            if np.isnan(embedding).any():
                return False
            
            # Check for infinite values
            if np.isinf(embedding).any():
                return False
            
            # Check for zero norm
            if np.linalg.norm(embedding) == 0:
                return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def create_zero_embedding(dimension: int = EmbeddingConfig.EMBEDDING_DIMENSION) -> np.ndarray:
        """Create a zero embedding of specified dimension"""
        return np.zeros(dimension, dtype=np.float32)
    
    @staticmethod
    def create_random_embedding(dimension: int = EmbeddingConfig.EMBEDDING_DIMENSION) -> np.ndarray:
        """Create a random embedding of specified dimension"""
        return np.random.randn(dimension).astype(np.float32)

class EmbeddingCache:
    """Embedding cache management"""
    
    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or Path(FilePaths.EMBEDDER_CACHE)
        self.cache_data = {}
        self.load_cache()
    
    def load_cache(self) -> None:
        """Load embedding cache from file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    self.cache_data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load embedding cache: {e}")
            self.cache_data = {}
    
    def save_cache(self) -> bool:
        """Save embedding cache to file"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache_data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to save embedding cache: {e}")
            return False
    
    def get_embedding(self, key: str) -> Optional[np.ndarray]:
        """Get embedding from cache"""
        try:
            if key in self.cache_data:
                embedding_data = self.cache_data[key].get("embedding") or self.cache_data[key].get("vector")
                if embedding_data:
                    return np.array(embedding_data, dtype=np.float32)
        except Exception as e:
            print(f"❌ Failed to get embedding for {key}: {e}")
        return None
    
    def set_embedding(self, key: str, embedding: np.ndarray, metadata: Optional[Dict] = None) -> None:
        """Set embedding in cache"""
        try:
            self.cache_data[key] = {
                "embedding": embedding.tolist(),
                "dimension": len(embedding),
                "metadata": metadata or {}
            }
        except Exception as e:
            print(f"❌ Failed to set embedding for {key}: {e}")
    
    def has_embedding(self, key: str) -> bool:
        """Check if embedding exists in cache"""
        return key in self.cache_data and "embedding" in self.cache_data[key]
    
    def list_keys(self) -> List[str]:
        """List all keys in cache"""
        return list(self.cache_data.keys())
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_embeddings = len(self.cache_data)
        valid_embeddings = sum(1 for data in self.cache_data.values() if "embedding" in data)
        
        dimensions = []
        for data in self.cache_data.values():
            if "embedding" in data:
                dimensions.append(len(data["embedding"]))
        
        return {
            "total_embeddings": total_embeddings,
            "valid_embeddings": valid_embeddings,
            "invalid_embeddings": total_embeddings - valid_embeddings,
            "dimensions": dimensions,
            "unique_dimensions": list(set(dimensions)) if dimensions else []
        }

class FAISSOperations:
    """FAISS index operations"""
    
    def __init__(self, index_path: Optional[Path] = None, ids_path: Optional[Path] = None):
        self.index_path = index_path or Path(FilePaths.FAISS_INDEX)
        self.ids_path = ids_path or Path(FilePaths.FAISS_IDS)
        self.index = None
        self.ids = []
        self.load_index()
    
    def load_index(self) -> bool:
        """Load FAISS index and IDs"""
        try:
            import faiss
            
            if not self.index_path.exists():
                return False
            
            self.index = faiss.read_index(str(self.index_path))
            
            if self.ids_path.exists():
                with open(self.ids_path, 'r') as f:
                    ids_data = json.load(f)
                    self.ids = ids_data.get("ids", [])
            
            return True
        except Exception as e:
            print(f"❌ Failed to load FAISS index: {e}")
            return False
    
    def save_index(self, embeddings: List[np.ndarray], ids: List[str]) -> bool:
        """Save FAISS index and IDs"""
        try:
            import faiss
            
            if not embeddings:
                return False
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings).astype('float32')
            dimension = embeddings_array.shape[1]
            
            # Create index
            self.index = faiss.IndexFlatIP(dimension)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings_array)
            self.index.add(embeddings_array)
            
            # Save index
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.index_path))
            
            # Save IDs
            self.ids = ids
            with open(self.ids_path, 'w') as f:
                json.dump({"ids": ids}, f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Failed to save FAISS index: {e}")
            return False
    
    def search(self, query_embedding: np.ndarray, top_k: int = EmbeddingConfig.DEFAULT_TOP_K) -> List[Tuple[str, float]]:
        """Search FAISS index"""
        try:
            if self.index is None:
                return []
            
            import faiss
            
            # Normalize query embedding
            query_array = np.array([query_embedding]).astype('float32')
            faiss.normalize_L2(query_array)
            
            # Search
            scores, indices = self.index.search(query_array, top_k)
            
            # Convert to results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.ids):
                    results.append((self.ids[idx], float(score)))
            
            return results
        except Exception as e:
            print(f"❌ FAISS search failed: {e}")
            return []
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get FAISS index statistics"""
        if self.index is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "total_vectors": self.index.ntotal,
            "dimension": self.index.d,
            "ids_count": len(self.ids)
        }

class EmbeddingSimilarity:
    """Embedding similarity calculations"""
    
    @staticmethod
    def calculate_word_overlap(text1: str, text2: str) -> float:
        """Calculate word overlap between two texts"""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    @staticmethod
    def calculate_content_similarity(content1: str, content2: str) -> float:
        """Calculate basic content similarity"""
        if not content1 or not content2:
            return 0.0
        
        # Word overlap
        word_overlap = EmbeddingSimilarity.calculate_word_overlap(content1, content2)
        
        # Length similarity
        len1, len2 = len(content1), len(content2)
        length_similarity = 1.0 - abs(len1 - len2) / max(len1, len2) if max(len1, len2) > 0 else 0.0
        
        # Combined similarity
        return (word_overlap * 0.7 + length_similarity * 0.3)
    
    @staticmethod
    def calculate_quality_score(original: str, reconstructed: str, similarity_score: float) -> float:
        """Calculate overall quality score for reconstruction"""
        word_overlap = EmbeddingSimilarity.calculate_word_overlap(original, reconstructed)
        length_ratio = len(reconstructed) / len(original) if original else 0.0
        
        # Weighted combination
        quality = (
            similarity_score * EmbeddingConfig.SEMANTIC_SIMILARITY_WEIGHT +
            word_overlap * EmbeddingConfig.WORD_OVERLAP_WEIGHT +
            min(1.0, length_ratio) * EmbeddingConfig.LENGTH_APPROPRIATENESS_WEIGHT
        )
        
        return min(1.0, max(0.0, quality))
