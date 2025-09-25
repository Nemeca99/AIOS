#!/usr/bin/env python3
"""
Build Index Now
Quick script to build the FAISS index for the existing cache.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from fractal_mycelium_cache import FractalMyceliumCache

def build_index_now():
    """Build the FAISS index for the existing cache."""
    
    print("🔧 Building FAISS Index for Existing Cache")
    print("=" * 50)
    
    # Initialize cache
    cache = FractalMyceliumCache()
    
    # Load existing cache
    cache_file = "Data/FractalCache/registry.json"
    if os.path.exists(cache_file):
        print(f"📂 Loading cache from {cache_file}")
        cache.load_registry()
        print(f"✅ Cache loaded: {len(cache.file_registry)} fragments")
    else:
        print(f"❌ Cache file not found: {cache_file}")
        return False
    
    # Check if fragments have embeddings
    fragments_with_embeddings = 0
    for frag_id, frag_data in cache.file_registry.items():
        if 'embedding' in frag_data and frag_data['embedding'] is not None:
            fragments_with_embeddings += 1
    
    print(f"🔗 Fragments with embeddings: {fragments_with_embeddings}/{len(cache.file_registry)}")
    
    if fragments_with_embeddings == 0:
        print("❌ No embeddings found! Run: python experiments/ensure_embeddings.py")
        return False
    
    # Build the FAISS index
    print("\n🏗️  Building FAISS index...")
    try:
        cache.ensure_embedding_index()
        print("✅ FAISS index built successfully!")
    except Exception as e:
        print(f"❌ Error building FAISS index: {e}")
        return False
    
    # Test the index
    print("\n🔍 Testing index...")
    try:
        test_query = "test query for index verification"
        results = cache.find_relevant_fragments(test_query, max_results=3)
        print(f"✅ Index test successful - found {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"   {i+1}. {result['file_id'][:8]}... (score: {result['score']:.2f})")
            
    except Exception as e:
        print(f"❌ Index test failed: {e}")
        return False
    
    print("\n✅ Index building completed successfully!")
    print("The system should now use embeddings instead of simple search.")
    
    return True

if __name__ == "__main__":
    build_index_now()
