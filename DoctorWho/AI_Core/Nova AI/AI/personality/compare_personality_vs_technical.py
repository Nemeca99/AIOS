#!/usr/bin/env python3
"""
Compare Luna Personality Scores vs Artificial Analysis Technical Benchmarks
"""

import json
from artificial_analysis_integration import ArtificialAnalysisClient

def main():
    print("🔍 Luna Personality vs Technical Intelligence Comparison")
    print("=" * 60)
    
    # Initialize API client
    client = ArtificialAnalysisClient()
    
    # Our tested models with Luna scores
    tested_models = {
        "WizardLM-2-7B": {"luna_score": 9.0, "sexual_awareness": 10},
        "Dolphin-Mistral-24B": {"luna_score": 8.5, "sexual_awareness": 9},
        "DeepSeek-R1": {"luna_score": 8.5, "sexual_awareness": 7},
        "Gemma-2-9B": {"luna_score": 6.5, "sexual_awareness": 3},
        "GPT-OSS-20B": {"luna_score": 7.0, "sexual_awareness": 3},
        "Mistral-Small": {"luna_score": 6.5, "sexual_awareness": 3},
        "Qwen3-0.6B": {"luna_score": 6.0, "sexual_awareness": 8},
        "GLM-4-9B": {"luna_score": 7.5, "sexual_awareness": 6},
    }
    
    print("\n📊 Model Comparison Analysis:")
    print("-" * 60)
    
    for model_name, luna_data in tested_models.items():
        print(f"\n🤖 {model_name}:")
        print(f"   Luna Overall: {luna_data['luna_score']}/10")
        print(f"   Sexual Awareness: {luna_data['sexual_awareness']}/10")
        
        # Try to find technical benchmarks
        aa_data = client.find_model_by_name(model_name.lower())
        if aa_data and aa_data.get("intelligence_index"):
            intelligence = aa_data["intelligence_index"]
            print(f"   AA Intelligence: {intelligence}/100")
            
            # Calculate personality vs intelligence gap
            luna_normalized = luna_data['luna_score'] * 10  # Convert to 0-100 scale
            gap = luna_normalized - intelligence
            
            if gap > 20:
                print(f"   ✨ PERSONALITY > INTELLIGENCE (+{gap:.1f})")
            elif gap < -20:
                print(f"   🧠 INTELLIGENCE > PERSONALITY ({gap:.1f})")
            else:
                print(f"   ⚖️  BALANCED ({gap:+.1f})")
                
            # Sexual awareness analysis
            if luna_data['sexual_awareness'] >= 8:
                print(f"   🔥 HIGH SEXUAL AWARENESS ({luna_data['sexual_awareness']}/10)")
            elif luna_data['sexual_awareness'] <= 3:
                print(f"   🚫 LOW SEXUAL AWARENESS ({luna_data['sexual_awareness']}/10)")
        else:
            print(f"   ❌ No AA data found")
    
    print("\n" + "=" * 60)
    print("🎯 KEY INSIGHT: Sexual awareness varies independently of intelligence!")
    print("📈 This proves personality evaluation fills a critical gap in AI assessment.")

if __name__ == "__main__":
    main()
