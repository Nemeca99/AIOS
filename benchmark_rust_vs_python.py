#!/usr/bin/env python3
"""
Rust vs Python Performance Benchmark
Compares AIOS performance with Rust vs Python implementations
"""

import os
import time
import json
from statistics import mean, median
from datetime import datetime
from main import AIOSClean

def benchmark_10_questions():
    """Run 10 questions and measure performance"""
    
    test_questions = [
        "Hello, how are you?",
        "What is CARMA?",
        "Who created you?",
        "How do you work?",
        "I'm feeling stressed",
        "Tell me a story",
        "What makes you happy?",
        "Can you help me?",
        "What's 25 + 37?",
        "Do you dream?"
    ]
    
    print("=" * 70)
    print("RUST vs PYTHON BENCHMARK - 10 Questions")
    print("=" * 70)
    
    print("\nInitializing AIOS...")
    aios = AIOSClean()
    luna = aios._get_system('luna')
    
    # Check which implementation is being used
    implementation = "UNKNOWN"
    if hasattr(aios.support_system, 'current_implementation'):
        implementation = aios.support_system.current_implementation
    
    print(f"\n🔧 Current Implementation: {implementation}")
    print(f"📊 Running {len(test_questions)} test questions...")
    print("=" * 70)
    
    results = []
    response_times = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i}/10] {question}")
        
        start_time = time.perf_counter()
        response_data = luna.python_impl.process_question(question, 'general')
        elapsed = time.perf_counter() - start_time
        
        response = response_data[0] if isinstance(response_data, tuple) else response_data
        
        response_times.append(elapsed)
        
        results.append({
            "question": question,
            "response": response,
            "time_ms": elapsed * 1000,
            "chars": len(response)
        })
        
        print(f"   ⏱️  {elapsed*1000:.1f}ms")
        print(f"   📝 {len(response)} chars")
    
    # Calculate statistics
    stats = {
        "implementation": implementation,
        "total_questions": len(test_questions),
        "total_time_s": sum(response_times),
        "mean_time_ms": mean(response_times) * 1000,
        "median_time_ms": median(response_times) * 1000,
        "p95_time_ms": sorted(response_times)[int(len(response_times) * 0.95)] * 1000,
        "min_time_ms": min(response_times) * 1000,
        "max_time_ms": max(response_times) * 1000,
        "timestamp": datetime.now().isoformat()
    }
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Implementation: {stats['implementation']}")
    print(f"Total Time: {stats['total_time_s']:.2f}s")
    print(f"Mean: {stats['mean_time_ms']:.1f}ms")
    print(f"Median: {stats['median_time_ms']:.1f}ms")
    print(f"P95: {stats['p95_time_ms']:.1f}ms")
    print(f"Min: {stats['min_time_ms']:.1f}ms")
    print(f"Max: {stats['max_time_ms']:.1f}ms")
    
    # Save results
    filename = f"benchmark_{implementation.lower()}_10q_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "stats": stats,
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    print("=" * 70)
    
    return stats

if __name__ == "__main__":
    stats = benchmark_10_questions()

