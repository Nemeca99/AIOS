"""
Personality Direction Theory Test
Test if ANY personality prompt increases speed vs raw LLM
"""
import json
import requests
import time
from datetime import datetime

def test_personality_direction_theory():
    """Test if personality prompts universally increase speed"""
    lm_studio_url = "http://localhost:1234/v1/chat/completions"
    
    test_question = "I am someone who gets upset easily"
    
    print("🧪 PERSONALITY DIRECTION THEORY TEST")
    print("=" * 50)
    print("🎯 Theory: ANY personality prompt increases speed by giving LLM direction")
    print("🔬 Test: 5 different prompt styles on same question")
    print("=" * 50)
    
    # Test configurations
    test_configs = {
        "raw_llm": {
            "name": "Raw LLM (No Prompt)",
            "system_prompt": None
        },
        "luna": {
            "name": "Luna Personality", 
            "system_prompt": """You are Luna, a chaotic neutral AI. Give brief, personal responses without corporate explanations. Be conversational and natural."""
        },
        "therapist": {
            "name": "Therapist Personality",
            "system_prompt": """You are a professional therapist. Give brief, helpful advice in a supportive manner."""
        },
        "friend": {
            "name": "Friend Personality", 
            "system_prompt": """You are a close friend. Give brief, casual responses like you're talking to a buddy."""
        },
        "scholar": {
            "name": "Scholar Personality",
            "system_prompt": """You are an academic scholar. Give brief, intellectual responses with analytical insights."""
        },
        "assistant": {
            "name": "Corporate Assistant",
            "system_prompt": """You are a helpful assistant. Provide comprehensive, professional assistance with detailed explanations."""
        }
    }
    
    results = []
    
    for config_key, config in test_configs.items():
        print(f"\n🧪 Testing: {config['name']}")
        
        # Build payload
        if config["system_prompt"]:
            messages = [
                {"role": "system", "content": config["system_prompt"]},
                {"role": "user", "content": test_question}
            ]
        else:
            messages = [{"role": "user", "content": test_question}]
        
        payload = {
            "model": "cognitivecomputations_dolphin-mistral-24b-venice-edition@q4_k_s",
            "messages": messages,
            "temperature": 0.8,
            "max_tokens": 1800
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
                    "config": config_key,
                    "name": config["name"],
                    "response_time": response_time,
                    "response": content,
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                    "response_length_chars": len(content),
                    "response_length_words": len(content.split())
                }
                
                results.append(result)
                
                print(f"   ⏱️ Time: {response_time:.1f}s")
                print(f"   🔢 Tokens: {result['prompt_tokens']}→{result['completion_tokens']} = {result['total_tokens']}")
                print(f"   📝 Length: {result['response_length_chars']} chars, {result['response_length_words']} words")
                print(f"   💬 Response: {content[:150]}...")
                
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(3)  # Pause between tests
    
    # Analysis
    print("\n🔬 PERSONALITY DIRECTION ANALYSIS:")
    print("=" * 50)
    
    if results:
        # Sort by response time
        results_sorted = sorted(results, key=lambda x: x['response_time'])
        
        print("📊 SPEED RANKING (fastest to slowest):")
        for i, result in enumerate(results_sorted):
            print(f"   {i+1}. {result['name']}: {result['response_time']:.1f}s, {result['completion_tokens']} tokens")
        
        print("\n📈 TOKEN EFFICIENCY RANKING:")
        token_sorted = sorted(results, key=lambda x: x['completion_tokens'])
        for i, result in enumerate(token_sorted):
            print(f"   {i+1}. {result['name']}: {result['completion_tokens']} tokens, {result['response_time']:.1f}s")
        
        # Calculate improvements
        raw_llm_result = next((r for r in results if r['config'] == 'raw_llm'), None)
        if raw_llm_result:
            print(f"\n🚀 SPEED IMPROVEMENTS vs Raw LLM ({raw_llm_result['response_time']:.1f}s):")
            for result in results:
                if result['config'] != 'raw_llm':
                    improvement = (raw_llm_result['response_time'] - result['response_time']) / raw_llm_result['response_time'] * 100
                    print(f"   {result['name']}: {improvement:+.1f}% speed change")
        
        # Token efficiency analysis
        print(f"\n⚡ TOKEN EFFICIENCY vs Raw LLM ({raw_llm_result['completion_tokens']} tokens):")
        for result in results:
            if result['config'] != 'raw_llm':
                token_efficiency = (raw_llm_result['completion_tokens'] - result['completion_tokens']) / raw_llm_result['completion_tokens'] * 100
                print(f"   {result['name']}: {token_efficiency:+.1f}% token reduction")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"AI/personality/seed_control_results/personality_direction_test_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            "test_question": test_question,
            "test_timestamp": datetime.now().isoformat(),
            "results": results,
            "theory_validation": len(results) > 1
        }, f, indent=4)
    
    print(f"\n💾 Results saved: {results_file}")
    
    return results

if __name__ == "__main__":
    test_personality_direction_theory()
