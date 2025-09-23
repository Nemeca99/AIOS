#!/usr/bin/env python3
"""
Simple Health Check for CARMA System
Quick diagnostic script to check system status and identify issues.
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path to import CARMA modules
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from fractal_mycelium_cache import FractalMyceliumCache
from carma_100_percent_consciousness import CARMA100PercentConsciousness
from carma_executive_brain import CARMAExecutiveBrain
from carma_meta_memory import CARMAMetaMemory

def health_check():
    """Run comprehensive health check on CARMA system."""
    
    print("🏥 CARMA System Health Check")
    print("=" * 50)
    
    # Initialize components
    try:
        cache = FractalMyceliumCache()
        executive = CARMAExecutiveBrain(cache)
        meta_memory = CARMAMetaMemory(cache)
        consciousness = CARMA100PercentConsciousness(cache, executive, meta_memory)
        print("✅ CARMA components initialized")
    except Exception as e:
        print(f"❌ Component initialization failed: {e}")
        return False
    
    # Check cache status
    print("\n📊 Cache Status:")
    cache_file = "Data/FractalCache/registry.json"
    
    if os.path.exists(cache_file):
        try:
            cache.load_registry()
            print(f"✅ Cache loaded from {cache_file}")
        except Exception as e:
            print(f"❌ Cache load failed: {e}")
            return False
    else:
        print(f"⚠️  No cache file found at {cache_file}")
        print("   Run: python HiveMind/seed_carma_cache.py --dir ./seed_corpus --limit 100")
        return False
    
    # Fragment analysis
    all_fragments = list(cache.file_registry.keys())
    print(f"📁 Total fragments: {len(all_fragments)}")
    
    if len(all_fragments) == 0:
        print("❌ No fragments in cache!")
        return False
    
    # Check embeddings
    missing_embeddings = 0
    total_embedding_size = 0
    
    for fid in all_fragments:
        frag = cache.file_registry[fid]
        if 'embedding' not in frag or frag['embedding'] is None:
            missing_embeddings += 1
        else:
            total_embedding_size += len(frag['embedding'])
    
    print(f"🔗 Fragments with embeddings: {len(all_fragments) - missing_embeddings}")
    print(f"❌ Missing embeddings: {missing_embeddings}")
    
    if missing_embeddings > 0:
        print("⚠️  Run: python experiments/ensure_embeddings.py")
    
    # Check index status
    print(f"\n🏗️  Index Status:")
    has_faiss_index = False
    has_embeddings = False
    has_working_index = False
    
    try:
        has_faiss_index = hasattr(cache, 'embedding_index') and cache.embedding_index is not None
        has_embeddings = (len(cache.file_registry) - missing_embeddings) > 0
        has_working_index = has_faiss_index or has_embeddings  # Working if we have FAISS or embeddings
        
        print(f"   FAISS index built: {has_faiss_index}")
        print(f"   Embeddings available: {has_embeddings}")
        print(f"   Working index: {has_working_index}")
        
        if has_faiss_index:
            print(f"   Index type: {type(cache.embedding_index).__name__}")
            if hasattr(cache.embedding_index, 'ntotal'):
                print(f"   Index size: {cache.embedding_index.ntotal}")
    except Exception as e:
        print(f"   ❌ Index check failed: {e}")
    
    # Test retrieval
    print(f"\n🔍 Retrieval Test:")
    try:
        test_query = "test query for health check"
        test_embedding = cache.embedder.embed(test_query)
        results = cache.find_relevant(test_embedding, topk=3)
        
        print(f"   ✅ Retrieval working - found {len(results)} results")
        for i, result in enumerate(results):
            print(f"      Result {i+1}: {result.id[:8]}... (hits: {result.hits}, level: {result.level})")
    except Exception as e:
        print(f"   ❌ Retrieval test failed: {e}")
    
    # Check consciousness system
    print(f"\n🧠 Consciousness System:")
    try:
        print(f"   Target consciousness: {consciousness.target_consciousness}")
        print(f"   Current indicators: {consciousness.current_indicators}")
        print(f"   Consciousness level: {consciousness.get_consciousness_level():.2f}%")
    except Exception as e:
        print(f"   ❌ Consciousness check failed: {e}")
    
    # Check executive brain
    print(f"\n🎯 Executive Brain:")
    try:
        print(f"   Goal interval: {executive.goal_interval}s")
        print(f"   Goal templates: {len(executive.goal_templates)}")
        print(f"   Current cycle: {executive.current_cycle}")
    except Exception as e:
        print(f"   ❌ Executive brain check failed: {e}")
    
    # Check meta-memory
    print(f"\n💭 Meta-Memory:")
    try:
        print(f"   Compression threshold: {meta_memory.compression_threshold}")
        print(f"   Semantic clustering: {meta_memory.semantic_clustering_threshold}")
        print(f"   Episodic decay rate: {meta_memory.episodic_decay_rate}")
    except Exception as e:
        print(f"   ❌ Meta-memory check failed: {e}")
    
    # Check for deep sleep readiness
    print(f"\n😴 Deep Sleep Readiness:")
    try:
        # This would need to be implemented in the actual system
        print(f"   Messages this cycle: {getattr(cache, 'messages_this_cycle', 'Unknown')}")
        print(f"   Cycle limit: {getattr(cache, 'current_cycle_limit', 'Unknown')}")
        print(f"   Next deep sleep in: {getattr(cache, 'current_cycle_limit', 0) - getattr(cache, 'messages_this_cycle', 0)} messages")
    except Exception as e:
        print(f"   ❌ Deep sleep check failed: {e}")
    
    # Summary
    print(f"\n📋 Health Summary:")
    if missing_embeddings == 0 and has_working_index:
        print("   ✅ System ready for deep sleep testing")
        print("   Run: python experiments/run_deep_sleep_once.py")
    elif missing_embeddings > 0:
        print("   ⚠️  Build embeddings first: python experiments/ensure_embeddings.py")
    elif not has_working_index:
        print("   ⚠️  Build index first: python experiments/ensure_embeddings.py")
    else:
        print("   ❌ System has issues - check errors above")
    
    return True

if __name__ == "__main__":
    health_check()
