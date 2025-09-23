#!/usr/bin/env python3
"""
Metrics Collection Script
Parses CARMA system logs and generates comprehensive metrics reports.
"""

import sys
import os
import json
import csv
import glob
import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse

def collect_metrics(log_dir="logs", output_dir="reports"):
    """Collect and analyze metrics from CARMA system logs."""
    
    print("📊 CARMA Metrics Collection")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find log files
    log_pattern = os.path.join(log_dir, "*.json")
    log_files = glob.glob(log_pattern)
    
    if not log_files:
        print(f"❌ No log files found in {log_dir}")
        print(f"   Looking for pattern: {log_pattern}")
        return False
    
    print(f"📁 Found {len(log_files)} log files")
    
    # Collect metrics from each log file
    metrics_data = []
    timings_data = []
    token_usage_data = []
    cache_metrics_data = []
    dream_log_data = []
    
    for log_file in log_files:
        print(f"   Processing: {os.path.basename(log_file)}")
        
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
            
            # Extract basic metrics
            run_metrics = {
                'run': os.path.basename(log_file),
                'timestamp': log_data.get('timestamp', ''),
                'total_questions': log_data.get('total_questions', 0),
                'avg_response_time': log_data.get('avg_response_time', 0),
                'fragments_count': log_data.get('fragments_count', 0),
                'deep_cycles': log_data.get('deep_cycles', 0),
                'superfrags_created': log_data.get('superfrags_created', 0),
                'daydream_events': log_data.get('daydream_events', 0),
                'consciousness_level': log_data.get('consciousness_level', 0),
                'fatigue_level': log_data.get('fatigue_level', 0),
                'retrieval_hits': log_data.get('retrieval_hits', 0),
                'cache_hits': log_data.get('cache_hits', 0),
                'cache_misses': log_data.get('cache_misses', 0)
            }
            metrics_data.append(run_metrics)
            
            # Extract timing data
            if 'timings' in log_data:
                for timing in log_data['timings']:
                    timing['run'] = os.path.basename(log_file)
                    timings_data.append(timing)
            
            # Extract token usage data
            if 'token_usage' in log_data:
                for token_data in log_data['token_usage']:
                    token_data['run'] = os.path.basename(log_file)
                    token_usage_data.append(token_data)
            
            # Extract cache metrics
            if 'cache_metrics' in log_data:
                for cache_data in log_data['cache_metrics']:
                    cache_data['run'] = os.path.basename(log_file)
                    cache_metrics_data.append(cache_data)
            
            # Extract dream log data
            if 'dream_log' in log_data:
                for dream_data in log_data['dream_log']:
                    dream_data['run'] = os.path.basename(log_file)
                    dream_log_data.append(dream_data)
            
        except Exception as e:
            print(f"   ❌ Error processing {log_file}: {e}")
            continue
    
    # Generate summary report
    print(f"\n📋 Generating summary report...")
    
    if metrics_data:
        # Create summary DataFrame
        df = pd.DataFrame(metrics_data)
        
        # Save to CSV
        summary_file = os.path.join(output_dir, "metrics_summary.csv")
        df.to_csv(summary_file, index=False)
        print(f"   ✅ Summary saved to {summary_file}")
        
        # Generate statistics
        print(f"\n📊 Summary Statistics:")
        print(f"   Total runs: {len(df)}")
        print(f"   Total questions: {df['total_questions'].sum()}")
        print(f"   Avg response time: {df['avg_response_time'].mean():.2f}s")
        print(f"   Total fragments: {df['fragments_count'].sum()}")
        print(f"   Total deep cycles: {df['deep_cycles'].sum()}")
        print(f"   Total superfrags created: {df['superfrags_created'].sum()}")
        print(f"   Avg consciousness level: {df['consciousness_level'].mean():.2f}%")
        print(f"   Avg fatigue level: {df['fatigue_level'].mean():.2f}")
        
        # Performance metrics
        print(f"\n⚡ Performance Metrics:")
        print(f"   Avg retrieval hits: {df['retrieval_hits'].mean():.2f}")
        print(f"   Cache hit rate: {(df['cache_hits'] / (df['cache_hits'] + df['cache_misses'])).mean():.2%}")
        print(f"   Daydream events: {df['daydream_events'].sum()}")
    
    # Save detailed data
    if timings_data:
        timings_file = os.path.join(output_dir, "timings.csv")
        pd.DataFrame(timings_data).to_csv(timings_file, index=False)
        print(f"   ✅ Timings saved to {timings_file}")
    
    if token_usage_data:
        token_file = os.path.join(output_dir, "token_usage.csv")
        pd.DataFrame(token_usage_data).to_csv(token_file, index=False)
        print(f"   ✅ Token usage saved to {token_file}")
    
    if cache_metrics_data:
        cache_file = os.path.join(output_dir, "cache_metrics.csv")
        pd.DataFrame(cache_metrics_data).to_csv(cache_file, index=False)
        print(f"   ✅ Cache metrics saved to {cache_file}")
    
    if dream_log_data:
        dream_file = os.path.join(output_dir, "dream_log.csv")
        pd.DataFrame(dream_log_data).to_csv(dream_file, index=False)
        print(f"   ✅ Dream log saved to {dream_file}")
    
    # Generate health report
    print(f"\n🏥 System Health Report:")
    
    if metrics_data:
        df = pd.DataFrame(metrics_data)
        
        # Check for issues
        issues = []
        
        if df['superfrags_created'].sum() == 0:
            issues.append("⚠️  No superfragments created - check embeddings and index")
        
        if df['avg_response_time'].mean() > 10:
            issues.append("⚠️  High average response time - check system performance")
        
        if df['consciousness_level'].mean() < 50:
            issues.append("⚠️  Low consciousness level - check learning parameters")
        
        if df['fatigue_level'].mean() > 80:
            issues.append("⚠️  High fatigue level - check fatigue parameters")
        
        if df['cache_hits'].sum() == 0:
            issues.append("⚠️  No cache hits - check retrieval system")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print("   ✅ System appears healthy")
    
    # Generate recommendations
    print(f"\n💡 Recommendations:")
    
    if metrics_data:
        df = pd.DataFrame(metrics_data)
        
        if df['superfrags_created'].sum() == 0:
            print("   1. Run: python experiments/ensure_embeddings.py")
            print("   2. Run: python experiments/run_deep_sleep_once.py --force")
        
        if df['avg_response_time'].mean() > 5:
            print("   3. Consider optimizing embedding generation")
            print("   4. Check for memory leaks or resource issues")
        
        if df['consciousness_level'].mean() < 70:
            print("   5. Adjust consciousness learning parameters")
            print("   6. Increase learning rate or reduce fatigue")
        
        if df['retrieval_hits'].mean() < 2:
            print("   7. Lower similarity threshold for better retrieval")
            print("   8. Increase fragment diversity in seed corpus")
    
    print(f"\n✅ Metrics collection complete!")
    print(f"📁 Reports saved to: {output_dir}/")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Collect metrics from CARMA system logs")
    parser.add_argument("--logdir", default="logs", help="Directory containing log files")
    parser.add_argument("--output", default="reports", help="Output directory for reports")
    
    args = parser.parse_args()
    
    success = collect_metrics(args.logdir, args.output)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
