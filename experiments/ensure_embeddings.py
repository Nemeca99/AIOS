#!/usr/bin/env python3
"""
Ensure Embeddings and Index Builder
Builds embeddings for all fragments and creates the FAISS index before deep sleep runs.
This fixes the "No embeddings present - index not built" issue.
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path to import CARMA modules
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from fractal_mycelium_cache import FractalMyceliumCache
from carma_100_percent_consciousness import CARMA100PercentConsciousness
from carma_executive_brain import CARMAExecutiveBrain
from carma_meta_memory import CARMAMetaMemory
import json

def ensure_embeddings():
    """Build embeddings and index for all fragments in the CARMA system."""
    
    print("🔧 Building embeddings and index for CARMA system...")
    print("=" * 60)
    
    # Initialize CARMA system components
    print("📁 Initializing CARMA system...")
    cache = FractalMyceliumCache()
    executive = CARMAExecutiveBrain(cache)
    meta_memory = CARMAMetaMemory(cache)
    consciousness = CARMA100PercentConsciousness(cache, executive, meta_memory)
    
    # Load existing cache if available
    cache_file = "luna_carma_integration/registry.json"
    if os.path.exists(cache_file):
        print(f"📂 Loading existing cache from {cache_file}")
        cache.load_registry()
    else:
        print("⚠️  No existing cache found, starting fresh")
    
    # Get all fragment IDs
    all_ids = list(cache.file_registry.keys())
    print(f"📊 Found {len(all_ids)} fragments in cache")
    
    if len(all_ids) == 0:
        print("❌ No fragments found! Please seed the cache first:")
        print("   python HiveMind/seed_carma_cache.py --dir ./seed_corpus --limit 100")
        return False
    
    # Check which fragments need embeddings
    missing_embeddings = []
    for fid in all_ids:
        frag = cache.file_registry[fid]
        if not hasattr(frag, 'embedding') or frag.embedding is None:
            missing_embeddings.append(fid)
    
    print(f"🔍 Fragments missing embeddings: {len(missing_embeddings)}")
    
    if len(missing_embeddings) == 0:
        print("✅ All fragments already have embeddings")
    else:
        print("🔄 Building embeddings for missing fragments...")
        
        # Build embeddings for missing fragments
        for i, fid in enumerate(missing_embeddings):
            frag = cache.file_registry[fid]
            print(f"   Processing {i+1}/{len(missing_embeddings)}: {fid[:8]}...")
            
            try:
                # Generate embedding for fragment content
                embedding = cache.embedder.embed(frag['content'])
                frag['embedding'] = embedding
                print(f"   ✅ Generated embedding (dim: {len(embedding)})")
            except Exception as e:
                print(f"   ❌ Error generating embedding: {e}")
                continue
    
    # Build the FAISS index
    print("\n🏗️  Building FAISS index...")
    try:
        cache.ensure_embedding_index()
        print("✅ FAISS index built successfully")
    except Exception as e:
        print(f"❌ Error building index: {e}")
        return False
    
    # Save the updated cache
    print("\n💾 Saving updated cache...")
    try:
        cache.save_registry()
        print(f"✅ Cache saved to {cache_file}")
    except Exception as e:
        print(f"❌ Error saving cache: {e}")
        return False
    
    # Verify the index
    print("\n🔍 Verifying index...")
    try:
        # Test retrieval
        test_query = "test query for verification"
        test_embedding = cache.embedder.embed(test_query)
        results = cache.find_relevant(test_embedding, topk=3)
        
        print(f"✅ Index verification successful - found {len(results)} results")
        for i, result in enumerate(results):
            if hasattr(result, 'id'):
                print(f"   Result {i+1}: {result.id[:8]}... (hits: {result.hits}, level: {result.level})")
            else:
                # Handle dict results from fallback search
                frag_id = result.get('file_id', 'unknown')[:8]
                hits = result.get('hits', 0)
                level = result.get('level', 0)
                print(f"   Result {i+1}: {frag_id}... (hits: {hits}, level: {level})")
            
    except Exception as e:
        print(f"❌ Index verification failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Embeddings and index build complete!")
    print(f"📊 Total fragments: {len(all_ids)}")
    print(f"🔗 Index ready for deep sleep superfragment creation")
    
    return True

if __name__ == "__main__":
    success = ensure_embeddings()
    if success:
        print("\n✅ Ready for deep sleep testing!")
        print("Run: python experiments/run_deep_sleep_once.py")
    else:
        print("\n❌ Build failed - check errors above")
        sys.exit(1)
