#!/usr/bin/env python3
"""
CARMA Latency Benchmark
Measures response times for CARMA system queries.
"""

import sys
import time
import argparse
import statistics
from pathlib import Path
from typing import List, Dict, Any
import json
import csv

# Add parent directory to path to import CARMA modules
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from fractal_mycelium_cache import FractalMyceliumCache
from carma_100_percent_consciousness import CARMA100PercentConsciousness
from carma_executive_brain import CARMAExecutiveBrain
from carma_meta_memory import CARMAMetaMemory

def run_carma_query(cache, query: str) -> Dict[str, Any]:
    """Run a single query through the CARMA system."""
    start_time = time.time()
    
    try:
        # Generate embedding for query
        if hasattr(cache, 'embedder'):
            query_embedding = cache.embedder.embed(query)
        else:
            # Fallback: simple hash-based embedding simulation
            import hashlib
            query_hash = hashlib.md5(query.encode()).hexdigest()
            query_embedding = [float(int(query_hash[i:i+2], 16)) / 255.0 for i in range(0, 32, 2)]
        
        # Find relevant fragments
        results = cache.find_relevant_fragments(query, max_results=3)
        
        # Simulate response generation (in real system, this would call LLM)
        response = f"Based on {len(results)} relevant fragments, here's my response to: {query}"
        
        end_time = time.time()
        
        return {
            'query': query,
            'response': response,
            'latency': end_time - start_time,
            'fragments_found': len(results),
            'success': True
        }
        
    except Exception as e:
        end_time = time.time()
        return {
            'query': query,
            'response': f"Error: {e}",
            'latency': end_time - start_time,
            'fragments_found': 0,
            'success': False,
            'error': str(e)
        }

def benchmark_carma_latency(questions: int = 50, iterations: int = 3) -> Dict[str, Any]:
    """Run CARMA latency benchmark."""
    
    print("🔥 CARMA Latency Benchmark")
    print("=" * 50)
    print(f"Questions: {questions}, Iterations: {iterations}")
    print()
    
    # Initialize CARMA system
    try:
        cache = FractalMyceliumCache()
        executive = CARMAExecutiveBrain(cache)
        meta_memory = CARMAMetaMemory(cache)
        consciousness = CARMA100PercentConsciousness(cache, executive, meta_memory)
        
        # Load cache if available
        cache_file = "Data/FractalCache/registry.json"
        if Path(cache_file).exists():
            cache.load_registry()
            print(f"✅ Cache loaded: {len(cache.file_registry)} fragments")
        else:
            print("⚠️  No cache found, using empty system")
            
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return {'error': str(e)}
    
    # Test queries
    test_queries = [
        "What is the capital of France?",
        "Explain quantum entanglement simply.",
        "Tell me a short story about a robot.",
        "How does machine learning work?",
        "What are the benefits of renewable energy?",
        "Describe the process of photosynthesis.",
        "What is artificial intelligence?",
        "How do computers process information?",
        "What is the meaning of life?",
        "Explain the theory of relativity.",
        "What are the principles of democracy?",
        "How does the human brain work?",
        "What is climate change?",
        "Describe the water cycle.",
        "What is the history of the internet?",
        "How do vaccines work?",
        "What is sustainable development?",
        "Explain the concept of evolution.",
        "What are the benefits of exercise?",
        "How does music affect the brain?"
    ]
    
    # Extend queries if needed
    while len(test_queries) < questions:
        test_queries.extend(test_queries[:min(20, questions - len(test_queries))])
    
    test_queries = test_queries[:questions]
    
    # Run benchmark iterations
    all_results = []
    
    for iteration in range(iterations):
        print(f"Iteration {iteration + 1}: Running {questions} queries...")
        
        iteration_results = []
        iteration_times = []
        
        for i, query in enumerate(test_queries):
            result = run_carma_query(cache, query)
            iteration_results.append(result)
            iteration_times.append(result['latency'])
            
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{questions} queries...")
        
        avg_time = statistics.mean(iteration_times)
        min_time = min(iteration_times)
        max_time = max(iteration_times)
        std_time = statistics.stdev(iteration_times) if len(iteration_times) > 1 else 0
        
        print(f"Iteration {iteration + 1}: {avg_time:.1f}s average")
        
        all_results.extend(iteration_results)
    
    # Calculate overall statistics
    all_times = [r['latency'] for r in all_results if r['success']]
    successful_queries = len([r for r in all_results if r['success']])
    failed_queries = len(all_results) - successful_queries
    
    if all_times:
        avg_latency = statistics.mean(all_times)
        min_latency = min(all_times)
        max_latency = max(all_times)
        std_latency = statistics.stdev(all_times) if len(all_times) > 1 else 0
        median_latency = statistics.median(all_times)
    else:
        avg_latency = min_latency = max_latency = std_latency = median_latency = 0
    
    # Print results
    print()
    print("📊 Results:")
    print(f"   Average latency: {avg_latency:.2f}s")
    print(f"   Min latency: {min_latency:.2f}s")
    print(f"   Max latency: {max_latency:.2f}s")
    print(f"   Median latency: {median_latency:.2f}s")
    print(f"   Standard deviation: {std_latency:.2f}s")
    print(f"   Successful queries: {successful_queries}/{len(all_results)}")
    print(f"   Failed queries: {failed_queries}")
    
    # Save results
    results_data = {
        'timestamp': time.time(),
        'system': 'CARMA',
        'questions': questions,
        'iterations': iterations,
        'total_queries': len(all_results),
        'successful_queries': successful_queries,
        'failed_queries': failed_queries,
        'avg_latency': avg_latency,
        'min_latency': min_latency,
        'max_latency': max_latency,
        'median_latency': median_latency,
        'std_latency': std_latency,
        'results': all_results
    }
    
    # Save to JSON
    os.makedirs('reports', exist_ok=True)
    json_file = f'reports/carma_latency_benchmark_{int(time.time())}.json'
    with open(json_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    # Save to CSV
    csv_file = f'reports/carma_latency_benchmark_{int(time.time())}.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['query', 'latency', 'success', 'fragments_found', 'error'])
        for result in all_results:
            writer.writerow([
                result['query'],
                result['latency'],
                result['success'],
                result['fragments_found'],
                result.get('error', '')
            ])
    
    print(f"📁 Results saved to: {json_file}")
    print(f"📁 CSV saved to: {csv_file}")
    
    return results_data

def main():
    parser = argparse.ArgumentParser(description="Benchmark CARMA system latency")
    parser.add_argument("--questions", type=int, default=50, help="Number of questions to test")
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations to run")
    
    args = parser.parse_args()
    
    results = benchmark_carma_latency(args.questions, args.iterations)
    
    if 'error' in results:
        print(f"\n❌ Benchmark failed: {results['error']}")
        sys.exit(1)
    else:
        print(f"\n✅ Benchmark completed successfully!")
        print(f"🚀 CARMA average latency: {results['avg_latency']:.2f}s")

if __name__ == "__main__":
    import os
    main()
