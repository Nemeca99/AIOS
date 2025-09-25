#!/usr/bin/env python3
"""
Fragment Growth Analysis
Analyzes fractal memory growth patterns and cross-linking in CARMA system.
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any
import argparse

# Add parent directory to path to import CARMA modules
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from fractal_mycelium_cache import FractalMyceliumCache

def analyze_fragment_growth(cache_file: str = "Data/FractalCache/registry.json") -> Dict[str, Any]:
    """Analyze fragment growth patterns in CARMA system."""
    
    print("🌱 Fragment Growth Analysis")
    print("=" * 50)
    
    # Initialize cache
    cache = FractalMyceliumCache()
    
    if not os.path.exists(cache_file):
        print(f"❌ Cache file not found: {cache_file}")
        print("   Run: python HiveMind/seed_carma_cache.py --dir ./seed_corpus --limit 300")
        return {'error': 'Cache file not found'}
    
    try:
        cache.load_registry()
        print(f"✅ Cache loaded: {len(cache.file_registry)} fragments")
    except Exception as e:
        print(f"❌ Cache load failed: {e}")
        return {'error': str(e)}
    
    # Analyze fragment structure
    fragments = cache.file_registry
    total_fragments = len(fragments)
    
    if total_fragments == 0:
        print("❌ No fragments found in cache!")
        return {'error': 'No fragments found'}
    
    # Count fragments by level
    level_counts = {}
    max_level = 0
    
    for frag_id, frag_data in fragments.items():
        level = frag_data.get('level', 0)
        level_counts[level] = level_counts.get(level, 0) + 1
        max_level = max(max_level, level)
    
    # Count fragments with splits
    fragments_with_splits = 0
    total_splits = 0
    
    for frag_id, frag_data in fragments.items():
        children = frag_data.get('children', [])
        if children:
            fragments_with_splits += 1
            total_splits += len(children)
    
    # Count cross-link connections
    cross_links = 0
    for frag_id, frag_data in fragments.items():
        # Count connections to other fragments
        connections = len(frag_data.get('ancestors', [])) + len(frag_data.get('children', []))
        cross_links += connections
    
    # Calculate memory consolidation rate
    consolidation_rate = (fragments_with_splits / total_fragments) * 100 if total_fragments > 0 else 0
    
    # Analyze content distribution
    content_lengths = []
    for frag_id, frag_data in fragments.items():
        content = frag_data.get('content', '')
        content_lengths.append(len(content))
    
    avg_content_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
    min_content_length = min(content_lengths) if content_lengths else 0
    max_content_length = max(content_lengths) if content_lengths else 0
    
    # Analyze hit patterns (if available)
    hit_counts = []
    for frag_id, frag_data in fragments.items():
        hits = frag_data.get('hits', 0)
        hit_counts.append(hits)
    
    avg_hits = sum(hit_counts) / len(hit_counts) if hit_counts else 0
    max_hits = max(hit_counts) if hit_counts else 0
    
    # Print analysis results
    print(f"Total fragments: {total_fragments}")
    print(f"Max split level: {max_level}")
    print(f"Fragments with splits: {fragments_with_splits}")
    print(f"Total splits: {total_splits}")
    print(f"Cross-link connections: {cross_links}")
    print(f"Memory consolidation rate: {consolidation_rate:.1f}%")
    print()
    
    print("📊 Fragment Distribution by Level:")
    for level in sorted(level_counts.keys()):
        count = level_counts[level]
        percentage = (count / total_fragments) * 100
        print(f"   Level {level}: {count} fragments ({percentage:.1f}%)")
    
    print()
    print("📏 Content Analysis:")
    print(f"   Average content length: {avg_content_length:.1f} characters")
    print(f"   Min content length: {min_content_length} characters")
    print(f"   Max content length: {max_content_length} characters")
    
    print()
    print("🎯 Hit Analysis:")
    print(f"   Average hits per fragment: {avg_hits:.1f}")
    print(f"   Max hits: {max_hits}")
    
    # Analyze growth patterns
    print()
    print("🌱 Growth Patterns:")
    
    if max_level > 0:
        print(f"   ✅ Fractal splitting active (max level: {max_level})")
    else:
        print("   ⚠️  No fractal splitting detected")
    
    if fragments_with_splits > 0:
        print(f"   ✅ Memory consolidation active ({fragments_with_splits} fragments split)")
    else:
        print("   ⚠️  No memory consolidation detected")
    
    if cross_links > 0:
        print(f"   ✅ Cross-linking active ({cross_links} connections)")
    else:
        print("   ⚠️  No cross-linking detected")
    
    if consolidation_rate > 10:
        print(f"   ✅ High consolidation rate ({consolidation_rate:.1f}%)")
    elif consolidation_rate > 5:
        print(f"   ⚠️  Moderate consolidation rate ({consolidation_rate:.1f}%)")
    else:
        print(f"   ❌ Low consolidation rate ({consolidation_rate:.1f}%)")
    
    # Generate recommendations
    print()
    print("💡 Recommendations:")
    
    if max_level == 0:
        print("   1. Increase content size or lower split threshold to trigger fractal splitting")
    
    if fragments_with_splits == 0:
        print("   2. Run more queries to generate hits and trigger memory consolidation")
    
    if cross_links == 0:
        print("   3. Enable cross-linking in configuration or run more diverse queries")
    
    if consolidation_rate < 10:
        print("   4. Consider running longer learning sessions to increase consolidation")
    
    if avg_hits < 2:
        print("   5. Run more queries to increase fragment hit counts")
    
    # Save analysis results
    analysis_data = {
        'timestamp': time.time(),
        'cache_file': cache_file,
        'total_fragments': total_fragments,
        'max_level': max_level,
        'fragments_with_splits': fragments_with_splits,
        'total_splits': total_splits,
        'cross_links': cross_links,
        'consolidation_rate': consolidation_rate,
        'level_distribution': level_counts,
        'content_analysis': {
            'avg_length': avg_content_length,
            'min_length': min_content_length,
            'max_length': max_content_length
        },
        'hit_analysis': {
            'avg_hits': avg_hits,
            'max_hits': max_hits
        },
        'growth_patterns': {
            'fractal_splitting': max_level > 0,
            'memory_consolidation': fragments_with_splits > 0,
            'cross_linking': cross_links > 0,
            'high_consolidation': consolidation_rate > 10
        }
    }
    
    # Save to JSON
    os.makedirs('reports', exist_ok=True)
    json_file = f'reports/fragment_growth_analysis_{int(time.time())}.json'
    with open(json_file, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    print(f"📁 Analysis saved to: {json_file}")
    
    return analysis_data

def main():
    parser = argparse.ArgumentParser(description="Analyze fragment growth patterns in CARMA system")
    parser.add_argument("--cache", type=str, default="Data/FractalCache/registry.json",
                       help="Path to cache file")
    
    args = parser.parse_args()
    
    results = analyze_fragment_growth(args.cache)
    
    if 'error' in results:
        print(f"\n❌ Analysis failed: {results['error']}")
        sys.exit(1)
    else:
        print(f"\n✅ Analysis completed successfully!")

if __name__ == "__main__":
    import time
    main()
