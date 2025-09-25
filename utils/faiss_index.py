#!/usr/bin/env python3
"""
FAISS Index Utilities for CARMA System
Provides FAISS index functionality for vector similarity search.
"""

import numpy as np
import os
from typing import List, Optional, Tuple
from pathlib import Path

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS not available - using fallback similarity search")

class FAISSOperations:
    """FAISS operations for vector similarity search."""
    
    def __init__(self, dimension: int = 384, index_path: Optional[str] = None):
        self.dimension = dimension
        self.index_path = index_path or "cache/faiss_index.bin"
        self.index = None
        self.vectors = []
        
        if FAISS_AVAILABLE:
            self._initialize_index()
        else:
            print("⚠️  Using fallback similarity search (no FAISS)")
    
    def _initialize_index(self):
        """Initialize FAISS index."""
        try:
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
                print(f"✅ FAISS index loaded: {self.index.ntotal} vectors")
            else:
                # Create new index
                self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
                print(f"✅ FAISS index created: dimension {self.dimension}")
        except Exception as e:
            print(f"⚠️  Could not load FAISS index: {e}")
            self.index = faiss.IndexFlatIP(self.dimension)
    
    def add_vectors(self, vectors: List[List[float]], ids: Optional[List[int]] = None):
        """Add vectors to the index."""
        if not FAISS_AVAILABLE or self.index is None:
            # Fallback: store vectors in memory
            self.vectors.extend(vectors)
            return
        
        try:
            vectors_array = np.array(vectors, dtype=np.float32)
            self.index.add(vectors_array)
            print(f"✅ Added {len(vectors)} vectors to FAISS index")
        except Exception as e:
            print(f"⚠️  Error adding vectors to FAISS: {e}")
            # Fallback: store in memory
            self.vectors.extend(vectors)
    
    def search(self, query_vector: List[float], k: int = 5) -> Tuple[List[float], List[int]]:
        """Search for similar vectors."""
        if not FAISS_AVAILABLE or self.index is None:
            # Fallback: brute force search
            return self._fallback_search(query_vector, k)
        
        try:
            query_array = np.array([query_vector], dtype=np.float32)
            scores, indices = self.index.search(query_array, k)
            return scores[0].tolist(), indices[0].tolist()
        except Exception as e:
            print(f"⚠️  Error searching FAISS index: {e}")
            return self._fallback_search(query_vector, k)
    
    def _fallback_search(self, query_vector: List[float], k: int) -> Tuple[List[float], List[int]]:
        """Fallback similarity search using cosine similarity."""
        if not self.vectors:
            return [], []
        
        query_np = np.array(query_vector)
        similarities = []
        
        for i, vector in enumerate(self.vectors):
            vector_np = np.array(vector)
            # Cosine similarity
            similarity = np.dot(query_np, vector_np) / (np.linalg.norm(query_np) * np.linalg.norm(vector_np))
            similarities.append((similarity, i))
        
        # Sort by similarity and return top k
        similarities.sort(reverse=True)
        scores = [sim[0] for sim in similarities[:k]]
        indices = [sim[1] for sim in similarities[:k]]
        
        return scores, indices
    
    def save_index(self):
        """Save the FAISS index to disk."""
        if not FAISS_AVAILABLE or self.index is None:
            return
        
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            faiss.write_index(self.index, self.index_path)
            print(f"✅ FAISS index saved to {self.index_path}")
        except Exception as e:
            print(f"⚠️  Error saving FAISS index: {e}")
    
    def get_stats(self) -> dict:
        """Get index statistics."""
        if FAISS_AVAILABLE and self.index is not None:
            return {
                "total_vectors": self.index.ntotal,
                "dimension": self.dimension,
                "faiss_available": True
            }
        else:
            return {
                "total_vectors": len(self.vectors),
                "dimension": self.dimension,
                "faiss_available": False
            }

def load_faiss_index(index_path: str, dimension: int = 384) -> FAISSOperations:
    """Load or create a FAISS index."""
    return FAISSOperations(dimension=dimension, index_path=index_path)
