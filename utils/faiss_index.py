#!/usr/bin/env python3
"""
FAISS Index Builder and Loader
Robust FAISS index creation with sanity checks and fallback logging
"""

import faiss
import numpy as np
import json
import pathlib
import logging
from typing import Tuple, List, Dict

log = logging.getLogger("faiss_index")

def build_faiss_index(embed_cache_path: str, index_path: str = "luna_carma_integration/faiss.index") -> str:
    """Build FAISS index from embedding cache with robust error handling"""
    repo = pathlib.Path(embed_cache_path)
    if not repo.exists():
        raise FileNotFoundError(f"Embedding cache not found: {embed_cache_path}")
    
    # Load embedding data
    with repo.open() as f:
        data = json.load(f)
    
    ids = []
    vecs = []
    
    for k, meta in data.items():
        emb = meta.get("embedding") or meta.get("vector")
        if not emb:
            log.warning("no embedding for %s", k)
            continue
        
        arr = np.array(emb, dtype=np.float32)
        
        # Sanity checks
        if np.isnan(arr).any():
            log.error("nan embedding for %s", k)
            continue
        
        if np.linalg.norm(arr) == 0:
            log.error("zero norm embedding for %s", k)
            continue
        
        ids.append(k)
        vecs.append(arr)
    
    if len(vecs) == 0:
        raise RuntimeError("no valid embeddings to index")
    
    vecs = np.stack(vecs)
    d = vecs.shape[1]
    
    log.info("building faiss index: %d vectors, dim=%d", vecs.shape[0], d)
    
    # Create index (using inner product for cosine similarity)
    index = faiss.IndexFlatIP(d)
    
    # Normalize for cosine similarity
    faiss.normalize_L2(vecs)
    index.add(vecs)
    
    # Save index
    faiss.write_index(index, index_path)
    
    # Save id->pos mapping
    mapping = {"ids": ids}
    mapping_path = pathlib.Path(index_path).with_suffix(".ids.json")
    mapping_path.write_text(json.dumps(mapping))
    
    log.info("faiss index written: %s", index_path)
    return index_path

def load_faiss_index(index_path: str = "luna_carma_integration/faiss.index") -> Tuple[faiss.Index, List[str]]:
    """Load FAISS index with error handling"""
    if not pathlib.Path(index_path).exists():
        raise FileNotFoundError(f"FAISS index not found: {index_path}")
    
    index = faiss.read_index(index_path)
    
    # Load id mapping
    mapping_path = pathlib.Path(index_path).with_suffix(".ids.json")
    if mapping_path.exists():
        mapping = json.loads(mapping_path.read_text())
        ids = mapping["ids"]
    else:
        log.warning("No ID mapping found, using empty list")
        ids = []
    
    log.info("FAISS index loaded: %d vectors", index.ntotal)
    return index, ids

def search_similar(index: faiss.Index, ids: List[str], query_vec: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
    """Search for similar vectors using FAISS index"""
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)
    
    # Normalize query vector
    faiss.normalize_L2(query_vec)
    
    # Search
    D, I = index.search(query_vec, top_k)
    
    # Convert indices to IDs
    results = []
    for i, (dist, idx) in enumerate(zip(D[0], I[0])):
        if idx < len(ids):
            results.append((ids[idx], float(dist)))
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        # Build index
        embed_path = "AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json"
        index_path = "luna_carma_integration/faiss.index"
        
        try:
            result_path = build_faiss_index(embed_path, index_path)
            print(f"✅ Index built successfully: {result_path}")
        except Exception as e:
            print(f"❌ Failed to build index: {e}")
    else:
        # Load and test index
        try:
            index, ids = load_faiss_index()
            print(f"✅ Index loaded: {index.ntotal} vectors")
            print(f"Sample IDs: {ids[:5]}")
        except Exception as e:
            print(f"❌ Failed to load index: {e}")
