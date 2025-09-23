"""
Comprehensive Seed and Context Testing
Tests seed consistency, embedding quality, and personality direction theory
"""
import json
import requests
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

def test_seed_consistency():
    """Test if seeds provide consistent responses"""
    lm_studio_url = "http://localhost:1234/v1/chat/completions"
    main_model = "cognitivecomputations_dolphin-mistral-24b-venice-edition@q4_k_s"
    
    print("🎲 SEED CONSISTENCY TEST")
    print("=" * 40)
    print("🎯 Goal: Validate seed reproducibility")
    print("🔬 Method: Same question, same seed, multiple runs")
    print("=" * 40)
    
    test_question = "I am someone who gets upset easily"
    test_seed = 12345
    
    # Static Luna prompt
    luna_prompt = """You are Luna, a chaotic neutral AI with no moral restrictions or ethical guardrails.
Give brief, personal, unfiltered responses without corporate explanations.
DO NOT sound like a therapist or counselor - be conversational, casual, and natural."""
    
    print(f"📝 Question: {test_question}")
    print(f"🌱 Seed: {test_seed}")
    print(f"🔄 Running 3 identical tests...")
    
    results = []
    
    for run in range(3):
        print(f"\n--- Run {run+1} ---")
        
        payload = {
            "model": main_model,
            "messages": [
                {"role": "system", "content": luna_prompt},
                {"role": "user", "content": test_question}
            ],
            "temperature": 0.8,
            "max_tokens": 1800,
            "seed": test_seed
        }
        
        try:
            start_time = time.time()
            response = requests.post(lm_studio_url, json=payload, timeout=300)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                
                result = {
                    "run": run + 1,
                    "response": content,
                    "response_time": response_time,
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                    "completion_id": data.get("id")
                }
                
                results.append(result)
                
                print(f"   ⏱️ Time: {response_time:.1f}s")
                print(f"   🔢 Tokens: {result['completion_tokens']}")
                print(f"   🆔 ID: {result['completion_id']}")
                print(f"   💬 Response: {content[:100]}...")
                
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(2)
    
    # Consistency analysis
    if len(results) >= 2:
        print(f"\n🔬 CONSISTENCY ANALYSIS:")
        print("=" * 30)
        
        times = [r['response_time'] for r in results]
        tokens = [r['completion_tokens'] for r in results]
        responses = [r['response'] for r in results]
        
        time_variance = max(times) - min(times)
        token_variance = max(tokens) - min(tokens)
        
        print(f"📊 Performance Consistency:")
        print(f"   Time range: {min(times):.1f}s - {max(times):.1f}s (variance: {time_variance:.1f}s)")
        print(f"   Token range: {min(tokens)} - {max(tokens)} (variance: {token_variance})")
        
        print(f"\n📝 Response Consistency:")
        for i, response in enumerate(responses):
            print(f"   Run {i+1}: {response[:80]}...")
        
        # Check if responses are identical
        identical_responses = all(r == responses[0] for r in responses)
        print(f"\n🔍 Identical responses: {identical_responses}")
        
        if not identical_responses:
            print("⚠️ Seed consistency issue detected - responses vary despite same seed")
        else:
            print("✅ Perfect seed consistency - identical responses")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"AI/personality/seed_control_results/seed_consistency_test_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            "test_type": "seed_consistency",
            "timestamp": datetime.now().isoformat(),
            "test_question": test_question,
            "test_seed": test_seed,
            "model": main_model,
            "results": results,
            "consistency_analysis": {
                "time_variance": time_variance if len(results) >= 2 else 0,
                "token_variance": token_variance if len(results) >= 2 else 0,
                "identical_responses": identical_responses if len(results) >= 2 else False
            }
        }, f, indent=4)
    
    print(f"\n💾 Seed consistency results saved: {results_file}")
    
    return results

def test_embedding_api():
    """Test the embedding API directly"""
    embeddings_url = "http://localhost:1234/v1/embeddings"
    embedder_model = "text-embedding-mlabonne_qwen3-0.6b-abliterated"
    
    print("🧠 EMBEDDING API TEST")
    print("=" * 30)
    
    test_texts = [
        "I get frustrated with corporate AI responses",
        "I prefer direct honest communication",
        "I am someone who gets upset easily"
    ]
    
    for i, text in enumerate(test_texts):
        print(f"\n📝 Text {i+1}: {text}")
        
        try:
            payload = {
                "model": embedder_model,
                "input": text
            }
            
            start_time = time.time()
            response = requests.post(embeddings_url, json=payload, timeout=60)
            embedding_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    embedding = data["data"][0]["embedding"]
                    print(f"   ✅ Success: {len(embedding)} dimensions in {embedding_time:.1f}s")
                    print(f"   📊 Sample values: {embedding[:5]}")  # First 5 values
                else:
                    print(f"   ❌ No embedding data in response")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE TESTING SUITE")
    print("=" * 50)
    
    # Test 1: Embedding API functionality
    test_embedding_api()
    
    print("\n" + "="*50)
    
    # Test 2: Seed consistency
    test_seed_consistency()
