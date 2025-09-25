#!/usr/bin/env python3
"""
Semantic Reconstruction Module
Robust reconstruction with FAISS fallback to TF-IDF
"""

import json
import numpy as np
import pathlib
import logging
from typing import List, Tuple, Optional, Dict
from sklearn.feature_extraction.text import TfidfVectorizer

# Import our utilities
import sys
sys.path.append("utils")
from faiss_index import load_faiss_index, search_similar

log = logging.getLogger("semrec")

def embed_text(embedder, text: str) -> np.ndarray:
    """Embed text using the provided embedder"""
    try:
        embedding = embedder.embed(text)
        if isinstance(embedding, list):
            embedding = np.array(embedding, dtype=np.float32)
        return embedding
    except Exception as e:
        log.error("Failed to embed text: %s", e)
        return np.zeros(384, dtype=np.float32)  # Fallback dimension

def topk_candidates_faiss(embed_cache_path: str, query_vec: np.ndarray, k: int = 5, 
                         index_path: str = "luna_carma_integration/faiss.index") -> List[Tuple[str, float]]:
    """Find top-k candidates using FAISS index"""
    try:
        index, ids = load_faiss_index(index_path)
        candidates = search_similar(index, ids, query_vec, k)
        log.info("FAISS search found %d candidates", len(candidates))
        return candidates
    except Exception as e:
        log.warning("FAISS search failed: %s", e)
        return []

def topk_candidates_tfidf(cache_dir: str, query_text: str, k: int = 5) -> List[Tuple[str, float, str]]:
    """Find top-k candidates using TF-IDF fallback"""
    try:
        texts = []
        ids = []
        
        # Load all fragment texts
        cache_path = pathlib.Path(cache_dir)
        for fp in cache_path.glob("*.json"):
            try:
                with open(fp, 'r') as f:
                    data = json.load(f)
                frag_id = data.get("id", fp.stem)
                content = data.get("content", "")
                if content.strip():
                    ids.append(frag_id)
                    texts.append(content)
            except:
                continue
        
        if not texts:
            return []
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts + [query_text])
        
        # Calculate similarities
        query_vec = tfidf_matrix[-1].toarray()[0]
        doc_matrix = tfidf_matrix[:-1].toarray()
        
        similarities = doc_matrix @ query_vec
        top_indices = np.argsort(-similarities)[:k]
        
        candidates = []
        for idx in top_indices:
            if idx < len(ids):
                candidates.append((ids[idx], float(similarities[idx]), texts[idx]))
        
        log.info("TF-IDF search found %d candidates", len(candidates))
        return candidates
        
    except Exception as e:
        log.error("TF-IDF search failed: %s", e)
        return []

def reconstruct_from_candidates(candidates: List[Tuple[str, float, str]], max_length: int = 2000) -> str:
    """Reconstruct content from candidate fragments"""
    if not candidates:
        return ""
    
    # Sort by similarity score
    candidates.sort(key=lambda x: -x[1])
    
    # Combine top candidates
    reconstructed_parts = []
    total_length = 0
    
    for frag_id, score, content in candidates:
        if total_length + len(content) > max_length:
            break
        reconstructed_parts.append(content)
        total_length += len(content)
    
    reconstructed = "\n\n".join(reconstructed_parts)
    return reconstructed

def calculate_similarity(embedder, text1: str, text2: str) -> float:
    """Calculate cosine similarity between two texts"""
    try:
        vec1 = embed_text(embedder, text1)
        vec2 = embed_text(embedder, text2)
        
        # Cosine similarity
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = float(np.dot(vec1, vec2) / (norm1 * norm2))
        return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]
        
    except Exception as e:
        log.error("Similarity calculation failed: %s", e)
        return 0.0

def attempt_reconstruct(embedder, original_metadata: Dict, embed_cache_path: str, 
                       cache_dir: str = "Data/FractalCache") -> Tuple[Optional[str], float]:
    """Attempt to reconstruct a fragment using semantic similarity"""
    
    # Get reconstruction prompt
    prompt = original_metadata.get("placeholder_prompt", "")
    if not prompt:
        prompt = f"Reconstruct content for {original_metadata.get('id', 'unknown')}"
    
    log.info("Attempting reconstruction for: %s", original_metadata.get('id', 'unknown'))
    
    # Try FAISS first
    try:
        query_vec = embed_text(embedder, prompt)
        faiss_candidates = topk_candidates_faiss(embed_cache_path, query_vec, k=10)
        
        if faiss_candidates:
            # Convert FAISS candidates to text format
            text_candidates = []
            with open(embed_cache_path, 'r') as f:
                embed_data = json.load(f)
            
            for frag_id, score in faiss_candidates:
                if frag_id in embed_data:
                    content = embed_data[frag_id].get("text", "")
                    if content:
                        text_candidates.append((frag_id, score, content))
            
            if text_candidates:
                reconstructed = reconstruct_from_candidates(text_candidates)
                similarity = calculate_similarity(embedder, prompt, reconstructed)
                log.info("FAISS reconstruction: similarity %.3f", similarity)
                return reconstructed, similarity
    except Exception as e:
        log.warning("FAISS reconstruction failed: %s", e)
    
    # Fallback to TF-IDF
    try:
        tfidf_candidates = topk_candidates_tfidf(cache_dir, prompt, k=10)
        if tfidf_candidates:
            reconstructed = reconstruct_from_candidates(tfidf_candidates)
            similarity = calculate_similarity(embedder, prompt, reconstructed)
            log.info("TF-IDF reconstruction: similarity %.3f", similarity)
            return reconstructed, similarity
    except Exception as e:
        log.warning("TF-IDF reconstruction failed: %s", e)
    
    # Final fallback - generic content
    generic_content = f"Reconstructed content for {original_metadata.get('id', 'unknown')} - {prompt}"
    similarity = 0.1  # Low confidence
    log.info("Generic reconstruction: similarity %.3f", similarity)
    return generic_content, similarity

if __name__ == "__main__":
    # Test the reconstruction system
    import sys
    sys.path.append("HiveMind")
    from fractal_mycelium_cache import FractalMyceliumCache
    
    # Create test cache
    cache = FractalMyceliumCache()
    
    # Test reconstruction
    test_metadata = {
        "id": "test_fragment",
        "placeholder_prompt": "machine learning artificial intelligence neural networks"
    }
    
    embed_cache_path = "AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json"
    
    try:
        reconstructed, similarity = attempt_reconstruct(
            cache.embedder, 
            test_metadata, 
            embed_cache_path
        )
        print(f"✅ Reconstruction test: similarity {similarity:.3f}")
        print(f"Content preview: {reconstructed[:200]}...")
    except Exception as e:
        print(f"❌ Reconstruction test failed: {e}")
