#!/usr/bin/env python3
"""
AIOS Clean - Paper Generator

Merges auto-generated RESULTS.md with PAPER_METHODS_RESULTS.md template
to create a complete, publication-ready manuscript.

Usage:
    python generate_paper.py --results analytics_out/RESULTS.md --template PAPER_METHODS_RESULTS.md --output final_paper.md
"""

import argparse
import re
from pathlib import Path

def load_file(file_path):
    """Load file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return None

def extract_results_sections(results_content):
    """Extract specific sections from RESULTS.md."""
    sections = {}
    
    # Extract routing accuracy
    routing_match = re.search(r'## Routing Accuracy\n(.*?)\n\n', results_content, re.DOTALL)
    if routing_match:
        sections['routing_accuracy'] = routing_match.group(1).strip()
    
    # Extract speculative decoding
    spec_match = re.search(r'## Speculative Decoding\n(.*?)\n\n', results_content, re.DOTALL)
    if spec_match:
        sections['speculative_decoding'] = spec_match.group(1).strip()
    
    # Extract latency
    latency_match = re.search(r'## Latency \(p95, ms\)\n(.*?)\n\n', results_content, re.DOTALL)
    if latency_match:
        sections['latency'] = latency_match.group(1).strip()
    
    # Extract retrieval stability
    retrieval_match = re.search(r'## Retrieval Stability\n(.*?)\n\n', results_content, re.DOTALL)
    if retrieval_match:
        sections['retrieval_stability'] = retrieval_match.group(1).strip()
    
    # Extract environment
    env_match = re.search(r'## Environment Details\n(.*?)\n\n', results_content, re.DOTALL)
    if env_match:
        sections['environment'] = env_match.group(1).strip()
    
    return sections

def merge_paper_template(template_content, results_sections):
    """Merge results into paper template."""
    merged_content = template_content
    
    # Replace routing accuracy section
    if 'routing_accuracy' in results_sections:
        routing_pattern = r'(\| Architecture \| Trivial \| Moderate \| High \|.*?\|)'
        merged_content = re.sub(
            routing_pattern, 
            results_sections['routing_accuracy'], 
            merged_content, 
            flags=re.DOTALL
        )
    
    # Replace speculative decoding section
    if 'speculative_decoding' in results_sections:
        spec_pattern = r'(\| Architecture \| Accept Rate \(mean\) \| Min \| Max \| Samples \|.*?\|)'
        merged_content = re.sub(
            spec_pattern,
            results_sections['speculative_decoding'],
            merged_content,
            flags=re.DOTALL
        )
    
    # Replace latency section
    if 'latency' in results_sections:
        latency_pattern = r'(\| Layer \| Backend \| LLaMA \| Qwen \| Phi \|.*?\|)'
        merged_content = re.sub(
            latency_pattern,
            results_sections['latency'],
            merged_content,
            flags=re.DOTALL
        )
    
    # Replace retrieval stability
    if 'retrieval_stability' in results_sections:
        merged_content = re.sub(
            r'Median `fragments_found` = \[AUTO-GENERATED\].*',
            results_sections['retrieval_stability'],
            merged_content
        )
    
    # Replace environment details
    if 'environment' in results_sections:
        env_pattern = r'(\*\*Hardware\*\*: \[AUTO-GENERATED FROM ENV\].*?- Python: \[VERSION\].*?- GPU: \[MODEL\])'
        merged_content = re.sub(
            env_pattern,
            f"**Hardware**: {results_sections['environment']}",
            merged_content,
            flags=re.DOTALL
        )
    
    # Remove remaining [AUTO-GENERATED] placeholders
    merged_content = re.sub(r'\[AUTO-GENERATED\]', 'TBD', merged_content)
    merged_content = re.sub(r'\[VERSION\]', 'TBD', merged_content)
    merged_content = re.sub(r'\[OS\]', 'TBD', merged_content)
    merged_content = re.sub(r'\[MODEL\]', 'TBD', merged_content)
    
    return merged_content

def main():
    parser = argparse.ArgumentParser(description='Generate publication-ready paper from template and results')
    parser.add_argument('--results', required=True, help='Path to RESULTS.md from provenance_to_results.py')
    parser.add_argument('--template', default='PAPER_METHODS_RESULTS.md', help='Path to paper template')
    parser.add_argument('--output', default='AIOS_Clean_Paper.md', help='Output file path')
    
    args = parser.parse_args()
    
    print("📝 AIOS Clean - Paper Generator")
    print("=" * 50)
    
    # Load template
    template_content = load_file(args.template)
    if not template_content:
        return 1
    
    # Load results
    results_content = load_file(args.results)
    if not results_content:
        return 1
    
    # Extract sections from results
    print("🔍 Extracting results sections...")
    results_sections = extract_results_sections(results_content)
    
    if not results_sections:
        print("⚠️  Warning: No results sections found in RESULTS.md")
    
    # Merge template with results
    print("🔗 Merging template with results...")
    merged_content = merge_paper_template(template_content, results_sections)
    
    # Write output
    output_path = Path(args.output)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        print(f"✅ Generated paper: {output_path}")
        print(f"📄 Paper length: {len(merged_content.split())} words")
        
        # Show sections that were merged
        if results_sections:
            print("\n📊 Merged sections:")
            for section in results_sections:
                print(f"   ✅ {section}")
        else:
            print("\n⚠️  No sections were merged (template used as-is)")
            
        return 0
        
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
