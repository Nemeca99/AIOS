#!/usr/bin/env python3
"""
Cross-Architecture Benchmark Script for AIOS Clean
Runs the same harness across LLaMA, Qwen, and Phi with provenance tracking
"""

import subprocess
import sys
import json
import time
from pathlib import Path

def run_benchmark(arch_name, model_name, output_file):
    """Run benchmark for a specific architecture."""
    print(f"\n🚀 Running {arch_name.upper()} benchmark...")
    print(f"   Model: {model_name}")
    print(f"   Output: {output_file}")
    
    # First, update the model configuration
    print(f"   🔧 Updating model configuration...")
    update_cmd = [
        sys.executable, "main.py", 
        "--system", "--modchange", "--main", 
        "--model-name", model_name
    ]
    
    try:
        result = subprocess.run(update_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"   ❌ Failed to update model config: {result.stderr}")
            return False
        print(f"   ✅ Model config updated")
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout updating model config")
        return False
    
    # Run the golden prompts test
    print(f"   🧪 Running golden prompts test...")
    test_cmd = [
        sys.executable, "main.py",
        "--execution-mode", "real",
        "--deterministic",
        "--test-suite", "--golden",
        "--report", output_file
    ]
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"   ✅ {arch_name.upper()} benchmark completed")
            return True
        else:
            print(f"   ❌ {arch_name.upper()} benchmark failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ❌ {arch_name.upper()} benchmark timeout")
        return False

def main():
    """Run cross-architecture benchmarks."""
    print("🔥 AIOS Clean Cross-Architecture Benchmark")
    print("=" * 60)
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)
    
    # Define architectures and models
    benchmarks = [
        {
            "arch": "llama",
            "model": "llama-3.2-pkd-deckard-almost-human-abliterated-uncensored-7b-i1",
            "output": "results_llama.json"
        },
        {
            "arch": "qwen", 
            "model": "qwen/qwen3-4b-thinking-2507",
            "output": "results_qwen.json"
        },
        {
            "arch": "phi",
            "model": "microsoft/Phi-3-mini-4k-instruct",  # Example Phi model
            "output": "results_phi.json"
        }
    ]
    
    results = []
    start_time = time.time()
    
    for benchmark in benchmarks:
        success = run_benchmark(
            benchmark["arch"],
            benchmark["model"], 
            benchmark["output"]
        )
        results.append({
            "arch": benchmark["arch"],
            "model": benchmark["model"],
            "success": success,
            "output_file": benchmark["output"]
        })
    
    # Print summary
    total_time = time.time() - start_time
    print(f"\n📊 Cross-Architecture Benchmark Summary")
    print(f"=" * 60)
    print(f"Total time: {total_time:.1f}s")
    print(f"Results:")
    
    successful = 0
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"   {result['arch'].upper():>6}: {status} ({result['model']})")
        if result["success"]:
            successful += 1
    
    print(f"\n🎯 {successful}/{len(results)} architectures benchmarked successfully")
    
    # Create combined results file
    combined_results = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "total_time_seconds": total_time,
        "architectures": results,
        "summary": {
            "total": len(results),
            "successful": successful,
            "failed": len(results) - successful
        }
    }
    
    with open("cross_arch_results.json", 'w') as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"📄 Combined results saved to: cross_arch_results.json")
    
    if successful == len(results):
        print(f"🎉 All cross-architecture benchmarks passed!")
        return 0
    else:
        print(f"⚠️  {len(results) - successful} benchmarks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
