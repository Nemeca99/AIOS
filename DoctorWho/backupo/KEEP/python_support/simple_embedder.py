#!/usr/bin/env python3
"""
Simple Embedder for CARMA System
Provides embedding functionality for the fractal mycelium cache.
"""

import os
import hashlib
import numpy as np
from typing import Dict, List, Optional
import requests
from datetime import datetime

# =============================
# Constants and Configuration
# =============================
DEFAULT_EMBED_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-mlabonne_qwen3-0.6b-abliterated")
DEFAULT_EMBED_URL: str = os.getenv("EMBEDDINGS_URL", "http://localhost:1234/v1/embeddings")
DEFAULT_EMBED_TIMEOUT: int = int(os.getenv("EMBEDDINGS_TIMEOUT", "30"))
DEFAULT_FALLBACK_DIM: int = int(os.getenv("EMBEDDING_DIM", "384"))

class SimpleEmbedder:
    """Simple embedder that can use local API or fallback to hash-based embeddings."""
    
    def __init__(self,
                 embedding_model: str = DEFAULT_EMBED_MODEL,
                 embeddings_url: str = DEFAULT_EMBED_URL,
                 use_api: bool = True,
                 fallback_dimension: int = DEFAULT_FALLBACK_DIM):
        self.embedding_model: str = embedding_model
        self.embeddings_url: str = embeddings_url
        self.use_api: bool = use_api
        self.fallback_dimension: int = fallback_dimension
        self.cache: Dict[str, List[float]] = {}
        
        print(f"🧠 Simple Embedder Initialized")
        print(f"   Model: {embedding_model}")
        print(f"   API URL: {embeddings_url}")
        print(f"   Use API: {use_api}")
        print(f"   Fallback dimension: {fallback_dimension}")
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        
        # Check cache first
        if text in self.cache:
            return self.cache[text]
        
        # Try API first if enabled
        if self.use_api:
            try:
                embedding = self._get_api_embedding(text)
                if embedding:
                    self.cache[text] = embedding
                    return embedding
            except Exception as e:
                print(f"⚠️  API embedding failed: {e}, using fallback")
        
        # Fallback to hash-based embedding
        embedding = self._get_hash_embedding(text)
        self.cache[text] = embedding
        return embedding
    
    def _get_api_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding from local API."""
        try:
            payload = {
                "model": self.embedding_model,
                "input": text
            }
            
            response = requests.post(self.embeddings_url, json=payload, timeout=DEFAULT_EMBED_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]['embedding']
            
        except Exception as e:
            print(f"❌ API embedding error: {e}")
            
        return None
    
    def _get_hash_embedding(self, text: str) -> List[float]:
        """Generate hash-based embedding as fallback."""
        # Create multiple hash variations for better distribution
        text_bytes = text.encode('utf-8')
        
        # Generate multiple hashes
        md5_hash = hashlib.md5(text_bytes).hexdigest()
        sha1_hash = hashlib.sha1(text_bytes).hexdigest()
        sha256_hash = hashlib.sha256(text_bytes).hexdigest()
        
        # Combine hashes and create embedding
        combined = md5_hash + sha1_hash + sha256_hash
        
        # Convert to float values
        embedding = []
        for i in range(0, len(combined), 2):
            if len(embedding) >= self.fallback_dimension:
                break
            hex_pair = combined[i:i+2]
            value = int(hex_pair, 16) / 255.0  # Normalize to 0-1
            embedding.append(value)
        
        # Pad or truncate to target dimension
        while len(embedding) < self.fallback_dimension:
            embedding.append(0.0)
        
        embedding = embedding[:self.fallback_dimension]
        
        # Normalize the embedding
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding
    
    def get_cache_stats(self) -> dict:
        """Get embedding cache statistics."""
        return {
            'cache_size': len(self.cache),
            'model': self.embedding_model,
            'use_api': self.use_api,
            'fallback_dimension': self.fallback_dimension
        }
    
    def clear_cache(self):
        """Clear the embedding cache."""
        self.cache.clear()
        print("🧹 Embedding cache cleared")

if __name__ == "__main__":
    # Test the embedder
    embedder = SimpleEmbedder(use_api=False)  # Test with fallback
    
    test_text = "This is a test sentence for embedding generation."
    embedding = embedder.embed(test_text)
    
    print(f"✅ Generated embedding: {len(embedding)} dimensions")
    print(f"   First 5 values: {embedding[:5]}")
    print(f"   Cache stats: {embedder.get_cache_stats()}")
