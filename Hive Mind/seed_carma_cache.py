#!/usr/bin/env python3
"""
CARMA Cache Seeding Script
Seeds the CARMA system with a larger corpus for testing
"""

import argparse
import json
import time
from pathlib import Path
from typing import List, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from fractal_mycelium_cache import FractalMyceliumCache
from hive_mind_logger import log

def create_sample_corpus(num_docs: int = 300) -> List[str]:
    """Create a sample corpus of personality-related content"""
    
    # Big Five personality traits content
    conscientiousness_content = [
        "I am someone who is organized and methodical in my approach to tasks.",
        "I am someone who always follows through on my commitments.",
        "I am someone who pays attention to details and rarely makes mistakes.",
        "I am someone who plans ahead and prepares for future events.",
        "I am someone who works systematically toward my goals.",
        "I am someone who is disciplined and self-controlled.",
        "I am someone who takes responsibility for my actions.",
        "I am someone who is reliable and dependable.",
        "I am someone who values order and structure in my life.",
        "I am someone who is careful and thorough in my work."
    ]
    
    agreeableness_content = [
        "I am someone who is trusting and believes in the goodness of others.",
        "I am someone who is helpful and willing to assist others.",
        "I am someone who is compassionate and empathetic.",
        "I am someone who values cooperation and harmony.",
        "I am someone who is forgiving and understanding.",
        "I am someone who is respectful and considerate of others.",
        "I am someone who is generous and giving.",
        "I am someone who is patient and tolerant.",
        "I am someone who is kind and caring.",
        "I am someone who is supportive and encouraging."
    ]
    
    extraversion_content = [
        "I am someone who is outgoing and sociable.",
        "I am someone who enjoys being around other people.",
        "I am someone who is talkative and expressive.",
        "I am someone who is energetic and enthusiastic.",
        "I am someone who is assertive and confident.",
        "I am someone who is adventurous and seeks excitement.",
        "I am someone who is optimistic and positive.",
        "I am someone who is spontaneous and flexible.",
        "I am someone who is charismatic and engaging.",
        "I am someone who is active and dynamic."
    ]
    
    neuroticism_content = [
        "I am someone who experiences anxiety and worry frequently.",
        "I am someone who is sensitive to stress and pressure.",
        "I am someone who has mood swings and emotional instability.",
        "I am someone who is self-critical and perfectionistic.",
        "I am someone who is prone to negative thinking.",
        "I am someone who is easily overwhelmed by challenges.",
        "I am someone who is insecure and lacks confidence.",
        "I am someone who is pessimistic and expects the worst.",
        "I am someone who is irritable and easily frustrated.",
        "I am someone who is emotionally reactive and sensitive."
    ]
    
    openness_content = [
        "I am someone who is curious and interested in new ideas.",
        "I am someone who is creative and imaginative.",
        "I am someone who is open to new experiences and adventures.",
        "I am someone who is intellectually curious and questioning.",
        "I am someone who appreciates art, music, and beauty.",
        "I am someone who is flexible and adaptable to change.",
        "I am someone who is original and unconventional.",
        "I am someone who is philosophical and deep-thinking.",
        "I am someone who is innovative and forward-thinking.",
        "I am someone who is culturally aware and diverse."
    ]
    
    # Combine all content
    all_content = (conscientiousness_content + agreeableness_content + 
                  extraversion_content + neuroticism_content + openness_content)
    
    # Repeat content to reach desired number
    corpus = []
    while len(corpus) < num_docs:
        corpus.extend(all_content)
    
    return corpus[:num_docs]

def seed_carma_cache(cache_dir: str = "luna_carma_integration", num_docs: int = 300):
    """Seed the CARMA cache with sample content"""
    
    log("SEED", f"Starting CARMA cache seeding with {num_docs} documents", "INFO")
    
    # Initialize CARMA cache
    cache = FractalMyceliumCache(cache_dir)
    
    # Create sample corpus
    corpus = create_sample_corpus(num_docs)
    
    # Add content to cache
    added_count = 0
    for i, content in enumerate(corpus):
        try:
            cache.add_content(content)
            added_count += 1
            if (i + 1) % 50 == 0:
                log("SEED", f"Added {i + 1}/{num_docs} documents", "INFO")
        except Exception as e:
            log("SEED", f"Error adding document {i}: {e}", "ERROR")
    
    # Get final statistics
    stats = cache.get_cache_statistics()
    
    log("SEED", f"CARMA cache seeding complete: {added_count} documents added", "INFO")
    log("SEED", f"Cache statistics: {stats['total_fragments']} fragments, {stats['total_edges']} edges", "INFO")
    
    return cache, stats

def main():
    parser = argparse.ArgumentParser(description="Seed CARMA cache with sample content")
    parser.add_argument("--dir", type=str, default="luna_carma_integration", 
                       help="Cache directory path")
    parser.add_argument("--limit", type=int, default=300, 
                       help="Number of documents to add")
    parser.add_argument("--output", type=str, default="seed_results.json",
                       help="Output file for seeding results")
    
    args = parser.parse_args()
    
    try:
        # Seed the cache
        cache, stats = seed_carma_cache(args.dir, args.limit)
        
        # Save results
        results = {
            "timestamp": time.time(),
            "cache_dir": args.dir,
            "documents_added": args.limit,
            "cache_statistics": stats,
            "success": True
        }
        
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ CARMA cache seeded successfully!")
        print(f"   Documents added: {args.limit}")
        print(f"   Cache fragments: {stats['total_fragments']}")
        print(f"   Cache edges: {stats['total_edges']}")
        print(f"   Results saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        log("SEED", f"Seeding failed: {e}", "CRITICAL")
        print(f"❌ Seeding failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
