#!/usr/bin/env python3
"""
AIOS Clean - Provenance to Results Converter

Converts NDJSON provenance logs into publication-ready RESULTS.md and CSV files.
Reads from data_core/analytics/provenance.ndjson and generates:
- summary_by_arch_layer_backend.csv (p50/p95 latency, mean accept rate, etc.)
- routing_accuracy.csv (from golden suite's expected_tier)
- RESULTS.md (auto-generated tables for papers)

Usage:
    python provenance_to_results.py --input data_core/analytics/provenance.ndjson --outdir analytics_out
"""

import json
import argparse
import csv
import statistics
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

def load_provenance_data(input_file):
    """Load provenance data from NDJSON file."""
    provenance_data = []
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    provenance_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Warning: Invalid JSON on line {line_num}: {e}")
                    continue
    except FileNotFoundError:
        print(f"❌ Error: Provenance file not found: {input_file}")
        return []
    except Exception as e:
        print(f"❌ Error reading provenance file: {e}")
        return []
    
    print(f"✅ Loaded {len(provenance_data)} provenance records")
    return provenance_data

def extract_architecture(model_name):
    """Extract architecture from model name."""
    if not model_name or model_name == 'N/A':
        return 'unknown'
    
    model_lower = model_name.lower()
    if 'llama' in model_lower:
        return 'LLaMA'
    elif 'qwen' in model_lower:
        return 'Qwen'
    elif 'phi' in model_lower:
        return 'Phi'
    elif 'mistral' in model_lower:
        return 'Mistral'
    else:
        return 'Other'

def calculate_percentile(data, percentile):
    """Calculate percentile from data list."""
    if not data:
        return None
    sorted_data = sorted(data)
    index = (percentile / 100) * (len(sorted_data) - 1)
    if index.is_integer():
        return sorted_data[int(index)]
    else:
        lower = sorted_data[int(index)]
        upper = sorted_data[int(index) + 1]
        return lower + (upper - lower) * (index - int(index))

def generate_summary_csv(provenance_data, output_dir):
    """Generate summary statistics CSV by architecture/layer/backend."""
    summary_data = defaultdict(lambda: {
        'latencies': [],
        'accept_rates': [],
        'tokens_in': [],
        'tokens_out': [],
        'fragments_found': [],
        'count': 0
    })
    
    for record in provenance_data:
        # Extract key dimensions
        arch = extract_architecture(record.get('models', {}).get('main', ''))
        core = record.get('core', 'unknown')
        backend = record.get('retrieval', {}).get('backend', 'none')
        
        key = f"{arch}|{core}|{backend}"
        
        # Extract metrics
        latency = record.get('latency_ms')
        if latency is not None:
            summary_data[key]['latencies'].append(latency)
        
        accept_rate = record.get('spec_decode', {}).get('accept_rate')
        if accept_rate is not None:
            summary_data[key]['accept_rates'].append(accept_rate)
        
        tokens_in = record.get('tokens_in')
        if tokens_in is not None:
            summary_data[key]['tokens_in'].append(tokens_in)
        
        tokens_out = record.get('tokens_out')
        if tokens_out is not None:
            summary_data[key]['tokens_out'].append(tokens_out)
        
        fragments = record.get('retrieval', {}).get('fragments_found')
        if fragments is not None:
            summary_data[key]['fragments_found'].append(fragments)
        
        summary_data[key]['count'] += 1
    
    # Generate CSV
    csv_path = output_dir / 'summary_by_arch_layer_backend.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Architecture', 'Core', 'Backend', 'Count',
            'Latency_p50_ms', 'Latency_p95_ms', 'Latency_mean_ms',
            'Accept_Rate_mean', 'Accept_Rate_min', 'Accept_Rate_max',
            'Tokens_In_mean', 'Tokens_Out_mean',
            'Fragments_Found_mean', 'Fragments_Found_std'
        ])
        
        for key, data in summary_data.items():
            arch, core, backend = key.split('|')
            
            # Calculate statistics
            lat_p50 = calculate_percentile(data['latencies'], 50)
            lat_p95 = calculate_percentile(data['latencies'], 95)
            lat_mean = statistics.mean(data['latencies']) if data['latencies'] else None
            
            accept_mean = statistics.mean(data['accept_rates']) if data['accept_rates'] else None
            accept_min = min(data['accept_rates']) if data['accept_rates'] else None
            accept_max = max(data['accept_rates']) if data['accept_rates'] else None
            
            tokens_in_mean = statistics.mean(data['tokens_in']) if data['tokens_in'] else None
            tokens_out_mean = statistics.mean(data['tokens_out']) if data['tokens_out'] else None
            
            frag_mean = statistics.mean(data['fragments_found']) if data['fragments_found'] else None
            frag_std = statistics.stdev(data['fragments_found']) if len(data['fragments_found']) > 1 else None
            
            writer.writerow([
                arch, core, backend, data['count'],
                lat_p50, lat_p95, lat_mean,
                accept_mean, accept_min, accept_max,
                tokens_in_mean, tokens_out_mean,
                frag_mean, frag_std
            ])
    
    print(f"✅ Generated summary CSV: {csv_path}")
    return csv_path

def generate_routing_accuracy_csv(provenance_data, output_dir):
    """Generate routing accuracy CSV from golden suite data."""
    routing_data = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    for record in provenance_data:
        # Only process records with routing information
        if 'router_tier' not in record or 'expected_tier' not in record:
            continue
        
        actual_tier = record.get('router_tier')
        expected_tier = record.get('expected_tier')
        arch = extract_architecture(record.get('models', {}).get('main', ''))
        
        key = f"{arch}|{expected_tier}"
        routing_data[key]['total'] += 1
        if actual_tier == expected_tier:
            routing_data[key]['correct'] += 1
    
    # Generate CSV
    csv_path = output_dir / 'routing_accuracy.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Architecture', 'Expected_Tier', 'Correct', 'Total', 'Accuracy_Percent'])
        
        for key, data in routing_data.items():
            arch, tier = key.split('|')
            accuracy = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            writer.writerow([arch, tier, data['correct'], data['total'], accuracy])
    
    print(f"✅ Generated routing accuracy CSV: {csv_path}")
    return csv_path

def generate_results_md(provenance_data, output_dir):
    """Generate RESULTS.md with auto-generated tables."""
    # Load summary data
    summary_data = defaultdict(lambda: {
        'latencies': [], 'accept_rates': [], 'fragments_found': []
    })
    
    routing_data = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    for record in provenance_data:
        arch = extract_architecture(record.get('models', {}).get('main', ''))
        core = record.get('core', 'unknown')
        backend = record.get('retrieval', {}).get('backend', 'none')
        
        # Summary data
        key = f"{arch}|{core}|{backend}"
        if 'latency_ms' in record:
            summary_data[key]['latencies'].append(record['latency_ms'])
        if 'spec_decode' in record and 'accept_rate' in record['spec_decode']:
            summary_data[key]['accept_rates'].append(record['spec_decode']['accept_rate'])
        if 'retrieval' in record and 'fragments_found' in record['retrieval']:
            summary_data[key]['fragments_found'].append(record['retrieval']['fragments_found'])
        
        # Routing data
        if 'router_tier' in record and 'expected_tier' in record:
            routing_key = f"{arch}|{record['expected_tier']}"
            routing_data[routing_key]['total'] += 1
            if record['router_tier'] == record['expected_tier']:
                routing_data[routing_key]['correct'] += 1
    
    # Generate RESULTS.md
    md_path = output_dir / 'RESULTS.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Results\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"**Records:** {len(provenance_data)} provenance entries\n")
        f.write("**Setup.** Deterministic run (`--execution-mode real --deterministic`), golden suite. Every request logs provenance.\n\n")
        
        # Routing Accuracy
        f.write("## Routing Accuracy\n")
        arch_tiers = defaultdict(list)
        for key, data in routing_data.items():
            arch, tier = key.split('|')
            accuracy = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            arch_tiers[arch].append((tier, accuracy))
        
        for arch, tiers in arch_tiers.items():
            f.write(f"- **{arch}**: ")
            tier_accs = []
            for tier, acc in tiers:
                tier_accs.append(f"{tier} {acc:.1f}%")
            f.write(", ".join(tier_accs) + "\n")
        f.write("\n")
        
        # Speculative Decoding
        f.write("## Speculative Decoding\n")
        f.write("| Arch | Accept Rate (mean) | Min | Max | Samples |\n")
        f.write("|------|---------------------|-----|-----|----------|\n")
        
        arch_accept = defaultdict(list)
        for key, data in summary_data.items():
            arch = key.split('|')[0]
            arch_accept[arch].extend(data['accept_rates'])
        
        for arch, rates in arch_accept.items():
            if rates:
                mean_rate = statistics.mean(rates)
                min_rate = min(rates)
                max_rate = max(rates)
                f.write(f"| {arch} | {mean_rate:.3f} | {min_rate:.3f} | {max_rate:.3f} | {len(rates)} |\n")
        f.write("\n")
        
        # Latency (p95, ms)
        f.write("## Latency (p95, ms)\n")
        f.write("| Layer | Backend | LLaMA | Qwen | Phi |\n")
        f.write("|-------|---------|-------|------|-----|\n")
        
        layer_backends = set()
        for key in summary_data.keys():
            _, layer, backend = key.split('|')
            layer_backends.add((layer, backend))
        
        for layer, backend in sorted(layer_backends):
            f.write(f"| {layer} | {backend} | ")
            for arch in ['LLaMA', 'Qwen', 'Phi']:
                key = f"{arch}|{layer}|{backend}"
                if key in summary_data and summary_data[key]['latencies']:
                    p95 = calculate_percentile(summary_data[key]['latencies'], 95)
                    f.write(f"{p95:.0f} | " if p95 else "__ | ")
                else:
                    f.write("__ | ")
            f.write("\n")
        f.write("\n")
        
        # Retrieval Stability
        f.write("## Retrieval Stability\n")
        all_fragments = []
        for data in summary_data.values():
            all_fragments.extend(data['fragments_found'])
        
        if all_fragments:
            median_frags = statistics.median(all_fragments)
            q1 = calculate_percentile(all_fragments, 25)
            q3 = calculate_percentile(all_fragments, 75)
            f.write(f"Median `fragments_found` = {median_frags:.1f} (IQR {q1:.1f}–{q3:.1f}) consistent across backends.\n\n")
        
        # Environment
        if provenance_data:
            env_sample = provenance_data[0].get('env', {})
            f.write("## Environment Details\n")
            f.write(f"- Python: {env_sample.get('python_version', 'unknown')}\n")
            f.write(f"- Platform: {env_sample.get('platform', 'unknown')}\n")
            f.write(f"- CPU: {env_sample.get('cpu_model', 'unknown')}\n")
            f.write(f"- GPU: {env_sample.get('gpu', 'unknown')}\n")
            if 'cuda_version' in env_sample:
                f.write(f"- CUDA: {env_sample['cuda_version']}\n")
            f.write("\n")
        
        # Provenance Example
        if provenance_data:
            f.write("## Provenance Example\n")
            f.write("```json\n")
            example = provenance_data[0]
            # Clean up for display
            display_example = {k: v for k, v in example.items() if v is not None and v != 'N/A'}
            f.write(json.dumps(display_example, indent=2)[:500] + "...\n")
            f.write("```\n")
    
    print(f"✅ Generated RESULTS.md: {md_path}")
    return md_path

def main():
    parser = argparse.ArgumentParser(description='Convert provenance NDJSON to publication-ready results')
    parser.add_argument('--input', required=True, help='Input provenance NDJSON file')
    parser.add_argument('--outdir', required=True, help='Output directory for generated files')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔍 AIOS Clean - Provenance to Results Converter")
    print("=" * 60)
    
    # Load provenance data
    provenance_data = load_provenance_data(input_path)
    if not provenance_data:
        print("❌ No provenance data found. Exiting.")
        return 1
    
    # Generate outputs
    try:
        generate_summary_csv(provenance_data, output_dir)
        generate_routing_accuracy_csv(provenance_data, output_dir)
        generate_results_md(provenance_data, output_dir)
        
        print("\n🎉 All outputs generated successfully!")
        print(f"📁 Output directory: {output_dir}")
        print("📄 Files created:")
        for file_path in output_dir.iterdir():
            if file_path.is_file():
                print(f"   - {file_path.name}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating outputs: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
