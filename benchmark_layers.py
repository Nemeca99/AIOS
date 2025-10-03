#!/usr/bin/env python3
"""
AIOS Clean Layer Benchmark Script
Generates CSV data for performance analysis across all layers
"""

import os
import sys
import time
import csv
import json
from typing import Dict, List, Tuple
from unittest.mock import Mock

# Ensure the current directory is in the Python path for imports
sys.path.insert(0, os.path.abspath('.'))

def benchmark_layer(layer_name: str, backend: str, queries: List[str], warm_up: bool = False) -> List[Dict]:
    """Benchmark a specific layer/backend combination"""
    results = []
    
    print(f"\n=== BENCHMARKING {layer_name} + {backend} ===")
    
    # Initialize the system (this is the cold start)
    if layer_name == "Raw":
        # Mock raw LLM
        llm_mock = Mock(return_value="I'm a raw LLM response.")
        
    elif layer_name == "Basic":
        # Mock basic personality
        basic_personality = Mock()
        basic_personality.generate_response = Mock(return_value="I'm a basic AI assistant.")
        
    elif layer_name == "Luna":
        # Import Luna system
        try:
            from luna_core.hybrid_luna_core import HybridLunaCore
            luna_system = HybridLunaCore()
        except Exception as e:
            print(f"Error importing Luna: {e}")
            return results
    
    # Initialize backend
    if backend == "CARMA":
        try:
            from carma_core.hybrid_carma_core import HybridCarmaCore
            carma_system = HybridCarmaCore()
        except Exception as e:
            print(f"Error importing CARMA: {e}")
            return results
    elif backend == "Simple_RAG":
        try:
            from rag_core.simple_rag import SimpleRAGSystem
            rag_system = SimpleRAGSystem()
        except Exception as e:
            print(f"Error importing Simple RAG: {e}")
            return results
    
    # Warm up if requested
    if warm_up:
        print("   Warming up system...")
        warm_up_query = "Hello, this is a warm-up query."
        if layer_name == "Luna" and backend == "CARMA":
            try:
                luna_system.generate_response(warm_up_query)
                carma_system.process_query(warm_up_query)
            except:
                pass
        elif layer_name == "Luna" and backend == "Simple_RAG":
            try:
                luna_system.generate_response(warm_up_query)
                rag_system.process_query(warm_up_query)
            except:
                pass
    
    # Run benchmarks
    for i, query in enumerate(queries):
        print(f"   Query {i+1}/{len(queries)}: {query[:50]}...")
        
        start_time = time.time()
        
        try:
            if layer_name == "Raw":
                response = llm_mock()
                fragments_found = 0
                tokens_in = len(query.split())
                tokens_out = len(response.split())
                tier = "raw"
                
            elif layer_name == "Basic":
                response = basic_personality.generate_response()
                fragments_found = 0
                tokens_in = len(query.split())
                tokens_out = len(response.split())
                tier = "basic"
                
            elif layer_name == "Luna":
                if backend == "CARMA":
                    # Get CARMA memories first
                    carma_result = carma_system.process_query(query)
                    fragments_found = len(carma_result.get('fragments_found', []))
                    
                    # Get Luna response
                    response = luna_system.generate_response(query)
                    tokens_in = len(query.split())
                    tokens_out = len(response.split()) if isinstance(response, str) else 0
                    tier = "luna_carma"
                    
                elif backend == "Simple_RAG":
                    # Get RAG memories first
                    rag_result = rag_system.process_query(query)
                    fragments_found = len(rag_result.get('fragments_found', []))
                    
                    # Get Luna response
                    response = luna_system.generate_response(query)
                    tokens_in = len(query.split())
                    tokens_out = len(response.split()) if isinstance(response, str) else 0
                    tier = "luna_rag"
                    
        except Exception as e:
            print(f"   Error: {e}")
            response = "Error occurred"
            fragments_found = 0
            tokens_in = len(query.split())
            tokens_out = 0
            tier = "error"
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        results.append({
            'layer': layer_name,
            'backend': backend,
            'tier': tier,
            'prompt_id': i + 1,
            'cold_warm': 'warm' if warm_up else 'cold',
            'latency_ms': round(latency_ms, 2),
            'fragments_found': fragments_found,
            'tokens_in': tokens_in,
            'tokens_out': tokens_out,
            'query': query[:100]  # Truncate for CSV
        })
        
        print(f"   → {latency_ms:.2f}ms, {fragments_found} fragments, {tokens_out} tokens")
    
    return results

def main():
    """Run comprehensive layer benchmarks"""
    print("AIOS Clean Layer Benchmark Suite")
    print("=" * 50)
    
    # Define test queries
    trivial_queries = [
        "hi", "hello", "hey", "yo", "sup", "whats up", "howdy", "greetings",
        "good morning", "good afternoon", "good evening", "hiya", "heya",
        "how are ya", "what's good", "thanks", "thank you", "thx", "ty",
        "ok", "okay", "alright", "sure", "yes", "no", "yep", "nope",
        "yeah", "nah", "yup", "nup", "bye", "goodbye", "see you", "later",
        "peace", "catch ya later", "good", "bad", "fine", "cool"
    ]
    
    moderate_queries = [
        "Hello, how are you today? I hope you're doing well.",
        "Can you tell me about your memory system and how it works?",
        "What is the difference between CARMA and traditional RAG systems?",
        "How does the tier system determine which model to use for responses?",
        "Can you explain how Luna's personality system integrates with the memory?",
        "What are the benefits of the modular architecture in AIOS Clean?",
        "How does speculative decoding improve performance in your system?",
        "Can you describe the dream consolidation process for memory optimization?",
        "What makes the hybrid Python/Rust implementation more efficient?",
        "How does the karma economy system work for response evaluation?",
        "Can you explain the fractal mycelium cache architecture?",
        "What are the key differences between your system and monolithic LLMs?",
        "How does the Big Five personality model influence Luna's responses?",
        "Can you describe the conversation fragment consolidation process?",
        "What role does the embedder play in the tier-based response system?",
        "How does the system handle error recovery and self-healing?",
        "Can you explain the generational learning cycles in AIOS Clean?",
        "What are the performance benefits of the modular core architecture?",
        "How does the system maintain personality consistency across sessions?",
        "Can you describe the memory optimization strategies used in DreamCore?"
    ]
    
    # Combine queries for testing
    all_queries = trivial_queries[:10] + moderate_queries[:10]  # 20 total queries
    
    # Define layer/backend combinations
    test_combinations = [
        ("Raw", "None"),
        ("Basic", "None"),
        ("Basic", "CARMA"),
        ("Basic", "Simple_RAG"),
        ("Luna", "CARMA"),
        ("Luna", "Simple_RAG")
    ]
    
    all_results = []
    
    # Run benchmarks for each combination
    for layer, backend in test_combinations:
        print(f"\n{'='*60}")
        print(f"Testing {layer} + {backend}")
        print(f"{'='*60}")
        
        # Cold run
        print(f"\n--- COLD RUN ---")
        cold_results = benchmark_layer(layer, backend, all_queries, warm_up=False)
        all_results.extend(cold_results)
        
        # Warm run
        print(f"\n--- WARM RUN ---")
        warm_results = benchmark_layer(layer, backend, all_queries, warm_up=True)
        all_results.extend(warm_results)
    
    # Save results to CSV
    csv_filename = "layer_benchmark_results.csv"
    print(f"\n{'='*60}")
    print(f"Saving results to {csv_filename}")
    print(f"{'='*60}")
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['layer', 'backend', 'tier', 'prompt_id', 'cold_warm', 'latency_ms', 'fragments_found', 'tokens_in', 'tokens_out', 'query']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in all_results:
            writer.writerow(result)
    
    print(f"✅ Benchmark complete! Results saved to {csv_filename}")
    
    # Print summary statistics
    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")
    
    for layer, backend in test_combinations:
        layer_results = [r for r in all_results if r['layer'] == layer and r['backend'] == backend]
        if layer_results:
            cold_results = [r for r in layer_results if r['cold_warm'] == 'cold']
            warm_results = [r for r in layer_results if r['cold_warm'] == 'warm']
            
            if cold_results:
                cold_latency = [r['latency_ms'] for r in cold_results]
                cold_avg = sum(cold_latency) / len(cold_latency)
                print(f"{layer} + {backend} (COLD): {cold_avg:.2f}ms avg latency")
            
            if warm_results:
                warm_latency = [r['latency_ms'] for r in warm_results]
                warm_avg = sum(warm_latency) / len(warm_latency)
                print(f"{layer} + {backend} (WARM): {warm_avg:.2f}ms avg latency")
    
    print(f"\n🎯 Benchmark complete! Check {csv_filename} for detailed results.")

if __name__ == "__main__":
    main()
