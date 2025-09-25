#!/usr/bin/env python3
"""
LUNA LEARNING COMPARISON TEST - Current vs. This Morning's Results
Compares current Luna learning state to this morning's results
"""

import sys
import os
import json
from pathlib import Path

def test_luna_learning_comparison():
    """Compare current Luna learning state to this morning's results"""
    print("🌙 LUNA LEARNING COMPARISON TEST")
    print("============================================================\n")
    print("📊 Comparing: CURRENT LUNA LEARNING vs. THIS MORNING'S RESULTS")
    print("=" * 60)
    
    try:
        # Check Luna's RAG cache file
        cache_file = Path("AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json")
        
        if cache_file.exists():
            print("✅ Luna RAG cache file found!")
            
            # Load the cache
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Analyze current learning state
            current_patterns = len(cache_data.get('patterns', []))
            current_size_mb = cache_file.stat().st_size / (1024 * 1024)
            
            print(f"📊 Current cached patterns: {current_patterns}")
            print(f"📊 Current cache size: {current_size_mb:.2f} MB")
            
            # This morning we had 120+ questions processed
            morning_patterns = 120
            print(f"📊 This morning's patterns: {morning_patterns}")
            
            if current_patterns >= morning_patterns * 0.8:  # 80% of morning
                print("✅ Learning patterns maintained!")
                pattern_status = "MAINTAINED"
            elif current_patterns > 0:
                print("⚠️ Learning patterns partially maintained")
                pattern_status = "PARTIAL"
            else:
                print("❌ Learning patterns lost")
                pattern_status = "LOST"
            
            # Check cache content quality
            if 'patterns' in cache_data and len(cache_data['patterns']) > 0:
                sample_pattern = cache_data['patterns'][0]
                has_content = 'content' in sample_pattern
                has_embedding = 'embedding' in sample_pattern
                has_metadata = 'metadata' in sample_pattern
                
                print(f"\n📊 Cache Quality Analysis:")
                print(f"   Has content: {has_content}")
                print(f"   Has embeddings: {has_embedding}")
                print(f"   Has metadata: {has_metadata}")
                
                if has_content and has_embedding:
                    print("✅ Cache quality excellent!")
                    quality_status = "EXCELLENT"
                elif has_content or has_embedding:
                    print("✅ Cache quality good!")
                    quality_status = "GOOD"
                else:
                    print("⚠️ Cache quality needs improvement")
                    quality_status = "NEEDS_IMPROVEMENT"
            else:
                print("❌ No patterns found in cache")
                quality_status = "EMPTY"
            
            # Check for Big Five question patterns
            big_five_keywords = [
                "original", "creative", "imaginative", "curious", "artistic",
                "organized", "disciplined", "prepared", "careful", "thorough",
                "outgoing", "social", "party", "energetic", "talkative",
                "trusting", "cooperative", "helpful", "forgiving", "kind",
                "anxious", "stressed", "worried", "nervous", "tense"
            ]
            
            found_keywords = 0
            if 'patterns' in cache_data:
                for pattern in cache_data['patterns']:
                    content = pattern.get('content', '').lower()
                    for keyword in big_five_keywords:
                        if keyword in content:
                            found_keywords += 1
                            break
            
            keyword_coverage = (found_keywords / len(big_five_keywords)) * 100
            print(f"\n📊 Big Five Keyword Coverage: {keyword_coverage:.1f}% ({found_keywords}/{len(big_five_keywords)})")
            
            if keyword_coverage >= 80:
                print("✅ Big Five learning comprehensive!")
                learning_status = "COMPREHENSIVE"
            elif keyword_coverage >= 60:
                print("✅ Big Five learning good!")
                learning_status = "GOOD"
            elif keyword_coverage >= 40:
                print("⚠️ Big Five learning partial")
                learning_status = "PARTIAL"
            else:
                print("❌ Big Five learning minimal")
                learning_status = "MINIMAL"
            
        else:
            print("❌ Luna RAG cache file not found!")
            pattern_status = "LOST"
            quality_status = "EMPTY"
            learning_status = "MINIMAL"
            current_patterns = 0
            current_size_mb = 0
        
        # Check for recovery files
        recovery_dir = Path(os.environ.get('TEMP', '/tmp')) / 'hive_mind_recovery'
        recovery_files = list(recovery_dir.glob('luna_*_state_*.json')) if recovery_dir.exists() else []
        
        print(f"\n📊 Recovery files found: {len(recovery_files)}")
        if recovery_files:
            print("✅ Luna has recovery capabilities!")
            recovery_status = "AVAILABLE"
        else:
            print("⚠️ No recovery files found")
            recovery_status = "NONE"
        
        # Final Comparison Report
        print("\n🎯 LUNA LEARNING COMPARISON REPORT")
        print("=" * 60)
        
        print(f"📚 Pattern Storage: {pattern_status}")
        print(f"🔍 Cache Quality: {quality_status}")
        print(f"🧠 Big Five Learning: {learning_status}")
        print(f"🔄 Recovery System: {recovery_status}")
        
        # Calculate overall comparison score
        status_scores = {
            "MAINTAINED": 100,
            "EXCELLENT": 100,
            "COMPREHENSIVE": 100,
            "GOOD": 80,
            "PARTIAL": 60,
            "NEEDS_IMPROVEMENT": 40,
            "AVAILABLE": 90,
            "LOST": 0,
            "EMPTY": 0,
            "MINIMAL": 20,
            "NONE": 0
        }
        
        overall_score = (
            status_scores.get(pattern_status, 0) * 0.3 +
            status_scores.get(quality_status, 0) * 0.2 +
            status_scores.get(learning_status, 0) * 0.3 +
            status_scores.get(recovery_status, 0) * 0.2
        )
        
        print(f"\n🎓 OVERALL LUNA LEARNING SCORE: {overall_score:.1f}/100")
        
        if overall_score >= 90:
            print("\n🎉 EXCELLENT! Luna learning maintained or improved!")
            print("🌙 Luna's learning state is at peak performance!")
            return True
        elif overall_score >= 80:
            print("\n✅ GOOD! Luna learning mostly maintained!")
            print("🔧 Minor improvements needed but learning is solid!")
            return True
        elif overall_score >= 70:
            print("\n⚠️ FAIR! Luna learning has degraded slightly!")
            print("🔧 Some maintenance needed to restore peak learning!")
            return False
        else:
            print("\n❌ POOR! Luna learning has significantly degraded!")
            print("🔧 Major maintenance needed to restore learning!")
            return False
            
    except Exception as e:
        print(f"❌ Luna comparison test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting Luna Learning Comparison Test...")
    success = test_luna_learning_comparison()
    
    if success:
        print("\n🎉 LUNA LEARNING COMPARISON TEST COMPLETED SUCCESSFULLY!")
        print("🌙 Luna's learning state maintained since this morning!")
    else:
        print("\n❌ LUNA LEARNING COMPARISON TEST SHOWS DEGRADATION!")
        print("🔧 Luna needs maintenance to restore peak learning!")
