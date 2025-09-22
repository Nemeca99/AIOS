#!/usr/bin/env python3
"""
Ablation Runner for CARMA System
Runs different configurations to test feature contributions
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from typing import Dict, List

def run_config(cfg: Dict, outdir: str = "ablation_results", questions: int = 120):
    """Run a single configuration and collect results"""
    os.makedirs(outdir, exist_ok=True)
    
    # Build command
    cmd = ["python", "luna_main.py", "--mode", "real_learning", "--questions", str(questions)]
    
    # Add configuration flags
    if cfg.get('carma', True):
        cmd += ["--carma", "on"]
    else:
        cmd += ["--carma", "off"]
    
    if cfg.get('crosslinks', True):
        cmd += ["--crosslinks", "on"]
    else:
        cmd += ["--crosslinks", "off"]
    
    if cfg.get('reinforce', True):
        cmd += ["--reinforce", "on"]
    else:
        cmd += ["--reinforce", "off"]
    
    # Add output flags
    cmd += ["--quiet"]  # Reduce output noise
    cmd += ["--output_dir", outdir]
    cmd += ["--prefix", cfg["name"]]
    
    start = time.time()
    print(f"🚀 RUNNING: {cfg['name']}")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
        runtime = time.time() - start
        
        # Parse results from stdout
        results = parse_luna_output(result.stdout, result.stderr, runtime, cfg)
        
        # Save results
        output_file = os.path.join(outdir, f"{cfg['name']}_results.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ {cfg['name']} completed in {runtime:.1f}s")
        print(f"   Results saved to: {output_file}")
        
        return results
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {cfg['name']} timed out after 1 hour")
        return {"config": cfg, "runtime": 3600, "error": "timeout"}
    except Exception as e:
        print(f"❌ {cfg['name']} failed: {e}")
        return {"config": cfg, "error": str(e)}

def parse_luna_output(stdout: str, stderr: str, runtime: float, cfg: Dict) -> Dict:
    """Parse Luna output to extract metrics"""
    results = {
        "config": cfg,
        "runtime": runtime,
        "stdout": stdout,
        "stderr": stderr,
        "metrics": {}
    }
    
    # Extract metrics from stdout
    lines = stdout.split('\n')
    for line in lines:
        if "Success Rate:" in line:
            try:
                rate = float(line.split("Success Rate:")[1].strip().replace("%", ""))
                results["metrics"]["success_rate"] = rate
            except:
                pass
        elif "Avg Response Time:" in line:
            try:
                time_str = line.split("Avg Response Time:")[1].strip().replace("s", "")
                results["metrics"]["avg_response_time"] = float(time_str)
            except:
                pass
        elif "Learning Efficiency:" in line:
            try:
                efficiency = float(line.split("Learning Efficiency:")[1].strip().replace("%", ""))
                results["metrics"]["learning_efficiency"] = efficiency
            except:
                pass
        elif "Mycelium Network:" in line:
            try:
                fragments = int(line.split("related fragments")[0].split(":")[1].strip())
                results["metrics"]["related_fragments"] = fragments
            except:
                pass
        elif "Collective Intelligence:" in line:
            try:
                parts = line.split("Collective Intelligence:")[1].strip()
                fragments = int(parts.split("fragments")[0].strip())
                pathways = int(parts.split(",")[1].split("neural pathways")[0].strip())
                results["metrics"]["total_fragments"] = fragments
                results["metrics"]["neural_pathways"] = pathways
            except:
                pass
    
    return results

def run_all_ablation_tests(questions: int = 120):
    """Run all ablation test configurations"""
    
    # Define test configurations
    CONFIGS = [
        {
            "name": "baseline",
            "description": "No CARMA, standard RAG only",
            "carma": False,
            "crosslinks": False,
            "reinforce": False
        },
        {
            "name": "carma_cache_only",
            "description": "CARMA cache without crosslinks",
            "carma": True,
            "crosslinks": False,
            "reinforce": False
        },
        {
            "name": "carma_full",
            "description": "Full CARMA system with all features",
            "carma": True,
            "crosslinks": True,
            "reinforce": True
        }
    ]
    
    print("🧪 STARTING ABLATION TESTS")
    print("=" * 50)
    print(f"Questions per test: {questions}")
    print(f"Total configurations: {len(CONFIGS)}")
    print()
    
    all_results = []
    
    for i, cfg in enumerate(CONFIGS, 1):
        print(f"📊 Test {i}/{len(CONFIGS)}: {cfg['name']}")
        print(f"   Description: {cfg['description']}")
        
        result = run_config(cfg, questions=questions)
        all_results.append(result)
        
        print()
    
    # Generate summary report
    generate_ablation_report(all_results)
    
    return all_results

def generate_ablation_report(results: List[Dict]):
    """Generate a summary report of ablation test results"""
    
    print("📈 ABLATION TEST SUMMARY")
    print("=" * 50)
    
    # Create summary table
    print(f"{'Config':<20} {'Success Rate':<12} {'Avg Time':<10} {'Fragments':<10} {'Pathways':<10}")
    print("-" * 70)
    
    for result in results:
        if "error" in result:
            print(f"{result['config']['name']:<20} {'ERROR':<12} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
            continue
        
        metrics = result.get("metrics", {})
        success_rate = metrics.get("success_rate", 0)
        avg_time = metrics.get("avg_response_time", 0)
        fragments = metrics.get("total_fragments", 0)
        pathways = metrics.get("neural_pathways", 0)
        
        print(f"{result['config']['name']:<20} {success_rate:<12.1f}% {avg_time:<10.1f}s {fragments:<10} {pathways:<10}")
    
    print()
    
    # Calculate improvements
    if len(results) >= 3:
        baseline = results[0]
        carma_full = results[2]
        
        if "error" not in baseline and "error" not in carma_full:
            baseline_metrics = baseline.get("metrics", {})
            carma_metrics = carma_full.get("metrics", {})
            
            print("🚀 CARMA IMPROVEMENTS OVER BASELINE:")
            print("-" * 40)
            
            # Success rate improvement
            baseline_success = baseline_metrics.get("success_rate", 0)
            carma_success = carma_metrics.get("success_rate", 0)
            success_improvement = carma_success - baseline_success
            print(f"Success Rate: {baseline_success:.1f}% → {carma_success:.1f}% ({success_improvement:+.1f}%)")
            
            # Response time comparison
            baseline_time = baseline_metrics.get("avg_response_time", 0)
            carma_time = carma_metrics.get("avg_response_time", 0)
            if baseline_time > 0:
                time_change = ((carma_time - baseline_time) / baseline_time) * 100
                print(f"Response Time: {baseline_time:.1f}s → {carma_time:.1f}s ({time_change:+.1f}%)")
            
            # Fragment retrieval
            baseline_frags = baseline_metrics.get("related_fragments", 0)
            carma_frags = carma_metrics.get("related_fragments", 0)
            frag_improvement = carma_frags - baseline_frags
            print(f"Related Fragments: {baseline_frags} → {carma_frags} ({frag_improvement:+d})")
            
            # Neural pathways
            carma_pathways = carma_metrics.get("neural_pathways", 0)
            print(f"Neural Pathways: 0 → {carma_pathways} (NEW)")
    
    print()
    print("💾 Detailed results saved in ablation_results/ directory")

def main():
    parser = argparse.ArgumentParser(description="Run ablation tests for CARMA system")
    parser.add_argument("--questions", type=int, default=120,
                       help="Number of questions per test (default: 120)")
    parser.add_argument("--quick", action="store_true",
                       help="Run quick test with 30 questions")
    
    args = parser.parse_args()
    
    questions = 30 if args.quick else args.questions
    
    try:
        results = run_all_ablation_tests(questions)
        
        # Save combined results
        combined_file = "ablation_results/combined_results.json"
        with open(combined_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ All ablation tests completed!")
        print(f"   Combined results saved to: {combined_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Ablation tests failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
