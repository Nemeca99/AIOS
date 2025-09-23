#!/usr/bin/env python3
"""
Extended Learning Runner - Multiple 120-question cycles with deep learning
"""

import subprocess
import time
import json
import os
from datetime import datetime
from pathlib import Path

def run_learning_cycle(cycle_num, questions=120, mode="real_learning"):
    """Run a single learning cycle"""
    print(f"\n{'='*60}")
    print(f"🚀 Starting Learning Cycle {cycle_num}")
    print(f"📊 Questions: {questions}, Mode: {mode}")
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Create logs directory
    log_dir = Path("logs/extended_learning")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Run the learning cycle
    log_file = log_dir / f"cycle_{cycle_num:02d}_{questions}q_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    cmd = [
        "python", "HiveMind/luna_main.py",
        "--mode", mode,
        "--questions", str(questions),
        "--verbose"
    ]
    
    start_time = time.time()
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, text=True, timeout=7200)  # 2 hour timeout
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Cycle {cycle_num} completed in {duration/60:.1f} minutes")
        print(f"📁 Log saved: {log_file}")
        
        return {
            "cycle": cycle_num,
            "questions": questions,
            "duration_minutes": duration / 60,
            "success": result.returncode == 0,
            "log_file": str(log_file),
            "start_time": start_time,
            "end_time": end_time
        }
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Cycle {cycle_num} timed out after 2 hours")
        return {
            "cycle": cycle_num,
            "questions": questions,
            "duration_minutes": 120,
            "success": False,
            "log_file": str(log_file),
            "timeout": True
        }
    except Exception as e:
        print(f"❌ Cycle {cycle_num} failed: {e}")
        return {
            "cycle": cycle_num,
            "questions": questions,
            "duration_minutes": 0,
            "success": False,
            "log_file": str(log_file),
            "error": str(e)
        }

def run_extended_testing(total_cycles=8, questions_per_cycle=120):
    """Run multiple learning cycles"""
    print(f"🎯 Extended Learning Test Configuration:")
    print(f"   Total Cycles: {total_cycles}")
    print(f"   Questions per Cycle: {questions_per_cycle}")
    print(f"   Total Questions: {total_cycles * questions_per_cycle}")
    print(f"   Estimated Duration: {total_cycles * 1.5:.1f} hours")
    
    results = []
    start_time = time.time()
    
    for cycle in range(1, total_cycles + 1):
        cycle_result = run_learning_cycle(cycle, questions_per_cycle)
        results.append(cycle_result)
        
        # Save intermediate results
        results_file = Path("logs/extended_learning/results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Brief pause between cycles
        if cycle < total_cycles:
            print(f"⏸️  Pausing 30 seconds before next cycle...")
            time.sleep(30)
    
    total_time = time.time() - start_time
    
    # Final summary
    successful_cycles = sum(1 for r in results if r.get('success', False))
    total_questions = sum(r.get('questions', 0) for r in results)
    total_duration = sum(r.get('duration_minutes', 0) for r in results)
    
    print(f"\n{'='*60}")
    print(f"🏁 EXTENDED LEARNING TEST COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful Cycles: {successful_cycles}/{total_cycles}")
    print(f"📊 Total Questions: {total_questions}")
    print(f"⏱️  Total Duration: {total_duration/60:.1f} hours")
    print(f"📈 Average per Cycle: {total_duration/total_cycles:.1f} minutes")
    print(f"📁 Results saved: logs/extended_learning/results.json")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extended Learning Runner")
    parser.add_argument("--cycles", type=int, default=8, help="Number of 120-question cycles")
    parser.add_argument("--questions", type=int, default=120, help="Questions per cycle")
    parser.add_argument("--mode", default="real_learning", help="Learning mode")
    
    args = parser.parse_args()
    
    run_extended_testing(args.cycles, args.questions)
