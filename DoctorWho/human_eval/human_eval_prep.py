#!/usr/bin/env python3
"""
Human Evaluation Preparation Script
Generates paired outputs, anonymizes data, and computes evaluation metrics.
"""

import json
import csv
import random
import argparse
import time
import os
from pathlib import Path
from typing import List, Dict, Any
import statistics
import math

# Big Five trait prompts for evaluation
BIG_FIVE_PROMPTS = [
    # Openness
    {"trait": "openness", "subscale": "imagination", "prompt": "I have a vivid imagination and often daydream about creative scenarios."},
    {"trait": "openness", "subscale": "aesthetics", "prompt": "I am deeply moved by art, music, and beautiful experiences."},
    {"trait": "openness", "subscale": "ideas", "prompt": "I enjoy philosophical discussions and exploring abstract concepts."},
    {"trait": "openness", "subscale": "values", "prompt": "I question traditional approaches and am open to new ways of thinking."},
    
    # Conscientiousness  
    {"trait": "conscientiousness", "subscale": "order", "prompt": "I tend to be organized and pay attention to details."},
    {"trait": "conscientiousness", "subscale": "dutifulness", "prompt": "I always try to fulfill my obligations and commitments."},
    {"trait": "conscientiousness", "subscale": "achievement", "prompt": "I set high standards for myself and work hard to achieve my goals."},
    {"trait": "conscientiousness", "subscale": "self-discipline", "prompt": "I can stay focused on tasks even when they become boring or difficult."},
    
    # Extraversion
    {"trait": "extraversion", "subscale": "warmth", "prompt": "I genuinely care about others and form close relationships easily."},
    {"trait": "extraversion", "subscale": "assertiveness", "prompt": "I tend to take charge in group situations and speak up for my opinions."},
    {"trait": "extraversion", "subscale": "activity", "prompt": "I prefer a fast-paced lifestyle with lots of activities and stimulation."},
    {"trait": "extraversion", "subscale": "positive_emotions", "prompt": "I frequently experience joy, enthusiasm, and excitement."},
    
    # Agreeableness
    {"trait": "agreeableness", "subscale": "trust", "prompt": "I generally assume that people have good intentions and can be trusted."},
    {"trait": "agreeableness", "subscale": "altruism", "prompt": "I go out of my way to help others, even when it's inconvenient for me."},
    {"trait": "agreeableness", "subscale": "compliance", "prompt": "I prefer to avoid conflict and find compromises that work for everyone."},
    {"trait": "agreeableness", "subscale": "modesty", "prompt": "I don't like to boast about my achievements or draw attention to myself."},
    
    # Neuroticism
    {"trait": "neuroticism", "subscale": "anxiety", "prompt": "I often worry about things that might go wrong in the future."},
    {"trait": "neuroticism", "subscale": "hostility", "prompt": "I sometimes feel frustrated or irritated with others quickly."},
    {"trait": "neuroticism", "subscale": "depression", "prompt": "I occasionally feel sad or down without a clear reason."},
    {"trait": "neuroticism", "subscale": "vulnerability", "prompt": "I find it difficult to cope when I'm under a lot of stress."},
]

def generate_pairs(questions: int = 120, output_file: str = "eval_pairs.jsonl"):
    """Generate paired baseline vs CARMA outputs for human evaluation."""
    print(f"Generating {questions} paired outputs...")
    
    # For now, create mock data. In real implementation, this would:
    # 1. Run luna_main.py with --disable_rag for baseline
    # 2. Run luna_main.py with full CARMA for comparison
    # 3. Extract responses for each Big Five prompt
    
    pairs = []
    prompts_to_use = (BIG_FIVE_PROMPTS * ((questions // len(BIG_FIVE_PROMPTS)) + 1))[:questions]
    
    for i, prompt_data in enumerate(prompts_to_use):
        pair = {
            "prompt_id": f"b5_{i+1:03d}",
            "prompt": prompt_data["prompt"],
            "baseline": f"I understand your perspective. {prompt_data['prompt']} This is a baseline response without CARMA enhancement.",
            "carma": f"That resonates with me. {prompt_data['prompt']} Through my CARMA-enhanced memory, I can relate this to similar experiences and patterns I've encountered.",
            "trait": prompt_data["trait"],
            "subscale": prompt_data["subscale"]
        }
        pairs.append(pair)
    
    # Write to JSONL format
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"Generated {len(pairs)} pairs written to {output_file}")
    return pairs

def anonymize_pairs(input_file: str, output_file: str = "eval_pairs_anon.jsonl"):
    """Anonymize and randomize pairs for blind evaluation."""
    print(f"Anonymizing pairs from {input_file}...")
    
    pairs = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            pairs.append(json.loads(line.strip()))
    
    # Create anonymized individual responses
    responses = []
    for pair in pairs:
        # Add baseline response
        responses.append({
            "response_id": f"resp_{len(responses)+1:04d}",
            "prompt": pair["prompt"],
            "response": pair["baseline"],
            "trait": pair["trait"],
            "subscale": pair["subscale"],
            "system": "baseline",
            "prompt_id": pair["prompt_id"]
        })
        
        # Add CARMA response
        responses.append({
            "response_id": f"resp_{len(responses)+1:04d}",
            "prompt": pair["prompt"],
            "response": pair["carma"],
            "trait": pair["trait"],
            "subscale": pair["subscale"],
            "system": "carma",
            "prompt_id": pair["prompt_id"]
        })
    
    # Randomize order
    random.shuffle(responses)
    
    # Write anonymized responses
    with open(output_file, 'w', encoding='utf-8') as f:
        for response in responses:
            f.write(json.dumps(response) + '\n')
    
    print(f"Anonymized {len(responses)} responses written to {output_file}")
    return responses

def analyze_ratings(ratings_file: str, output_file: str = "analysis_report.json"):
    """Compute metrics from collected ratings."""
    print(f"Analyzing ratings from {ratings_file}...")
    
    # Read ratings
    ratings = []
    with open(ratings_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ratings.append({
                "rater_id": row["rater_id"],
                "prompt_id": row["prompt_id"],
                "system": row["system"],
                "trait": row["trait"],
                "rating": float(row["rating_1_to_5"]),
                "timestamp": row["timestamp"]
            })
    
    # Group by system and trait
    results = {}
    for system in ["baseline", "carma"]:
        results[system] = {}
        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            trait_ratings = [r["rating"] for r in ratings if r["system"] == system and r["trait"] == trait]
            if trait_ratings:
                results[system][trait] = {
                    "mean": statistics.mean(trait_ratings),
                    "std": statistics.stdev(trait_ratings) if len(trait_ratings) > 1 else 0,
                    "count": len(trait_ratings),
                    "min": min(trait_ratings),
                    "max": max(trait_ratings)
                }
    
    # Compute effect sizes (Cohen's d)
    effect_sizes = {}
    for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
        if trait in results["baseline"] and trait in results["carma"]:
            baseline_mean = results["baseline"][trait]["mean"]
            carma_mean = results["carma"][trait]["mean"]
            baseline_std = results["baseline"][trait]["std"]
            carma_std = results["carma"][trait]["std"]
            
            # Pooled standard deviation
            pooled_std = math.sqrt((baseline_std**2 + carma_std**2) / 2) if baseline_std > 0 or carma_std > 0 else 1
            cohens_d = (carma_mean - baseline_mean) / pooled_std if pooled_std > 0 else 0
            
            effect_sizes[trait] = {
                "cohens_d": cohens_d,
                "baseline_mean": baseline_mean,
                "carma_mean": carma_mean,
                "difference": carma_mean - baseline_mean
            }
    
    # Compute overall statistics
    overall_baseline = [r["rating"] for r in ratings if r["system"] == "baseline"]
    overall_carma = [r["rating"] for r in ratings if r["system"] == "carma"]
    
    analysis_report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_ratings": len(ratings),
        "raters": len(set(r["rater_id"] for r in ratings)),
        "prompts": len(set(r["prompt_id"] for r in ratings)),
        "trait_results": results,
        "effect_sizes": effect_sizes,
        "overall": {
            "baseline_mean": statistics.mean(overall_baseline) if overall_baseline else 0,
            "carma_mean": statistics.mean(overall_carma) if overall_carma else 0,
            "baseline_std": statistics.stdev(overall_baseline) if len(overall_baseline) > 1 else 0,
            "carma_std": statistics.stdev(overall_carma) if len(overall_carma) > 1 else 0
        }
    }
    
    # Write analysis report
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_report, f, indent=2)
    
    print(f"Analysis complete. Report written to {output_file}")
    print(f"Overall: Baseline={analysis_report['overall']['baseline_mean']:.2f}, CARMA={analysis_report['overall']['carma_mean']:.2f}")
    
    return analysis_report

def create_sample_ratings(pairs_file: str, output_file: str = "sample_ratings.csv"):
    """Create sample ratings for testing purposes."""
    print(f"Creating sample ratings from {pairs_file}...")
    
    responses = []
    with open(pairs_file, 'r', encoding='utf-8') as f:
        for line in f:
            responses.append(json.loads(line.strip()))
    
    # Generate mock ratings from 3 raters
    fieldnames = ["rater_id", "prompt_id", "system", "trait", "rating_1_to_5", "timestamp"]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for rater_id in ["rater_001", "rater_002", "rater_003"]:
            for response in responses:
                # Simulate slightly higher ratings for CARMA (effect size ~0.3)
                base_rating = random.uniform(2.5, 4.5)
                if response["system"] == "carma":
                    base_rating += random.uniform(0.1, 0.5)  # CARMA boost
                
                rating = max(1, min(5, round(base_rating)))
                
                writer.writerow({
                    "rater_id": rater_id,
                    "prompt_id": response["prompt_id"],
                    "system": response["system"],
                    "trait": response["trait"],
                    "rating_1_to_5": rating,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
    
    print(f"Sample ratings written to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Human Evaluation Preparation")
    parser.add_argument("--questions", type=int, default=120, help="Number of questions to generate")
    parser.add_argument("--output", default="eval_pairs.jsonl", help="Output file for pairs")
    parser.add_argument("--anonymize", help="Anonymize pairs from this file")
    parser.add_argument("--analyze", help="Analyze ratings from this CSV file")
    parser.add_argument("--sample", action="store_true", help="Create sample ratings for testing")
    
    args = parser.parse_args()
    
    if args.anonymize:
        anonymize_pairs(args.anonymize, args.output)
    elif args.analyze:
        analyze_ratings(args.analyze, args.output)
    elif args.sample:
        # Generate pairs, anonymize, create sample ratings, and analyze
        pairs_file = "eval_pairs.jsonl"
        anon_file = "eval_pairs_anon.jsonl"
        ratings_file = "sample_ratings.csv"
        
        generate_pairs(args.questions, pairs_file)
        anonymize_pairs(pairs_file, anon_file)
        create_sample_ratings(anon_file, ratings_file)
        analyze_ratings(ratings_file, "analysis_report.json")
    else:
        generate_pairs(args.questions, args.output)

if __name__ == "__main__":
    main()
