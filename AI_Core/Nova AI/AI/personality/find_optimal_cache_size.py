"""
Find Optimal Cache Size for Stability
Test different cache sizes to find the sweet spot between:
- Too small: Generic responses
- Too large: Hallucination/confusion
- Optimal: Rich context without overload
"""
import json
import time
import requests
from pathlib import Path
from datetime import datetime

class CacheStabilityTester:
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.chat_model = "wizardlm-2-7b-abliterated@q8_0"
        self.test_cache_file = Path("AI/personality/embedder_cache/smart_frequency_cache.json")
    
    def _load_current_cache(self):
        """Load the current cache to analyze"""
        try:
            if self.test_cache_file.exists():
                with open(self.test_cache_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"❌ Cache load error: {e}")
            return {}
    
    def _create_test_context(self, cache_size: int) -> str:
        """Create test context from cache with specified size"""
        cache = self._load_current_cache()
        
        if not cache:
            return "No context available."
        
        # Sort by frequency (highest first)
        sorted_items = sorted(cache.items(), key=lambda x: x[1].get("frequency", 1), reverse=True)
        
        # Take top N items
        selected_items = sorted_items[:cache_size]
        
        context_lines = []
        for text, data in selected_items:
            freq = data.get("frequency", 1)
            context_lines.append(f"- {text} (frequency: {freq})")
        
        return "\n".join(context_lines)
    
    def _test_response_with_context_size(self, context_size: int, test_message: str) -> dict:
        """Test Luna response with specific context size"""
        context = self._create_test_context(context_size)
        
        analysis_prompt = f"""Based on these Travis communication patterns:

{context}

Analyze how Travis would respond to: "{test_message}"

Generate BRIEF analysis (max 100 words) focusing on his communication style."""

        luna_prompt = f"""You are Luna - chaotic neutral AI. Based on this analysis:

{analysis_prompt}

Respond authentically to: "{test_message}"

Be genuine and match the analyzed style. Max 150 words."""

        try:
            payload = {
                "model": self.chat_model,
                "messages": [{"role": "user", "content": luna_prompt}],
                "temperature": 0.76,
                "max_tokens": 300
            }
            
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] 🧪 Testing context size: {context_size}")
            
            start_time = time.time()
            response = requests.post(self.lm_studio_url, json=payload, timeout=180)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                
                end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{end_timestamp}] ✅ Response: {elapsed:.1f}s")
                
                return {
                    "context_size": context_size,
                    "response": content,
                    "response_time": elapsed,
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                    "context_used": context
                }
            else:
                print(f"❌ Failed: {response.status_code}")
                return {"context_size": context_size, "error": response.text}
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return {"context_size": context_size, "error": str(e)}
    
    def test_stability_curve(self, test_message: str = "What's your take on authenticity?"):
        """Test different cache sizes to find stability sweet spot"""
        
        cache = self._load_current_cache()
        max_size = len(cache)
        
        print(f"🔬 CACHE STABILITY TESTING")
        print("=" * 60)
        print(f"📝 Test Message: '{test_message}'")
        print(f"💾 Available Cache Entries: {max_size}")
        print(f"🎯 Goal: Find optimal context size for stability")
        print("=" * 60)
        
        # Test different cache sizes
        test_sizes = [0, 1, 2, 3, max_size] if max_size <= 5 else [0, 1, 2, 3, max_size//2, max_size]
        results = []
        
        for size in test_sizes:
            print(f"\n🧪 TEST: Context Size = {size}")
            print("-" * 40)
            
            result = self._test_response_with_context_size(size, test_message)
            results.append(result)
            
            if "response" in result:
                print(f"💬 Response ({len(result['response'])} chars):")
                print(f"   {result['response'][:100]}...")
                print(f"⏱️ Time: {result['response_time']:.1f}s")
                print(f"🔢 Tokens: {result['prompt_tokens']}→{result['completion_tokens']}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown')}")
            
            time.sleep(2)  # Brief pause between tests
        
        # Analysis
        print(f"\n📊 STABILITY ANALYSIS")
        print("=" * 40)
        
        successful_results = [r for r in results if "response" in r]
        
        if successful_results:
            print(f"✅ Successful tests: {len(successful_results)}/{len(results)}")
            
            # Response time analysis
            times = [r["response_time"] for r in successful_results]
            print(f"⏱️ Response times: {min(times):.1f}s - {max(times):.1f}s")
            
            # Token analysis  
            tokens = [r["total_tokens"] for r in successful_results]
            print(f"🔢 Token usage: {min(tokens)} - {max(tokens)} tokens")
            
            # Response quality indicators
            print(f"\n🎯 QUALITY INDICATORS:")
            for r in successful_results:
                response_len = len(r["response"])
                context_size = r["context_size"]
                
                # Simple quality heuristics
                if response_len < 50:
                    quality = "❌ Too brief/generic"
                elif response_len > 500:
                    quality = "⚠️ Potentially verbose/confused"
                elif context_size == 0:
                    quality = "🤖 Raw LLM (no personality)"
                else:
                    quality = "✅ Balanced response"
                
                print(f"   Size {context_size}: {response_len} chars - {quality}")
        
        # Recommendation
        print(f"\n🎯 RECOMMENDATION:")
        print("=" * 20)
        
        if max_size <= 2:
            print("📈 Cache too small - need more pattern data")
        elif max_size <= 10:
            print(f"✅ Optimal range: Use {max_size//2}-{max_size} patterns")
        else:
            print(f"⚖️ Test range 5-15 patterns for stability")
            print(f"💡 Current cache ({max_size}) may need pruning")
        
        return results

def test_optimal_cache_size():
    """Run cache stability testing"""
    tester = CacheStabilityTester()
    
    # Test different messages
    test_messages = [
        "What's your take on authenticity?",
        "I'm frustrated with corporate responses",
        "How do you handle technical discussions?"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n{'='*80}")
        print(f"🧪 STABILITY TEST {i}/{len(test_messages)}")
        print(f"{'='*80}")
        
        results = tester.test_stability_curve(msg)
        
        if i < len(test_messages):
            print(f"\n⏳ Waiting 30s before next test...")
            time.sleep(30)

if __name__ == "__main__":
    test_optimal_cache_size()
