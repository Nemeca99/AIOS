"""
Luna Balanced Weight System
Implements Travis's 0.5 ± 0.26 formula for optimal AI balance
Embedder = 0.24 (logical), Luna = 0.76 (creative), Average = 0.5 (perfect)
"""
import json
import requests
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class LunaBalancedWeightSystem:
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.main_model = "cognitivecomputations_dolphin-mistral-24b-venice-edition@q4_k_s"
        self.embedder_model = "mlabonne_qwen3-0.6b-abliterated"  # Use chat completion for analysis
        
        # Database and cache
        self.db_path = "F:/AI_Datasets/AIOS_Database/database/conversations.db"
        self.cache_file = Path("AI/personality/embedder_cache/balanced_weight_cache.json")
        self.cache_file.parent.mkdir(exist_ok=True)
        self.pattern_cache = self._load_cache()
        
        # TRAVIS'S 0.5 ± 0.26 FORMULA APPLIED
        self.base_balance = 0.5
        self.variance_factor = 0.26
        
        # EMBEDDER SETTINGS (Logical/Corporate side = 0.5 - 0.26 = 0.24)
        self.embedder_params = {
            "temperature": 0.24,        # Logical precision (0.5 - 0.26)
            "max_tokens": 200,          # Dense output
            "top_p": 0.7,              # Focused sampling
            "frequency_penalty": 0.5,   # High precision
            "presence_penalty": 0.3     # Logical consistency
        }
        
        # LUNA SETTINGS (Creative/Authentic side = 0.5 + 0.26 = 0.76)
        self.luna_params = {
            "temperature": 0.76,        # Creative expression (0.5 + 0.26)
            "max_tokens": 2000,         # Full expression
            "top_p": 0.9,              # Diverse sampling
            "frequency_penalty": 0.0,   # Natural repetition
            "presence_penalty": 0.0     # Creative flow
        }
        
        # System balance validation
        self.system_average = (self.embedder_params["temperature"] + self.luna_params["temperature"]) / 2
        
        print(f"🧮 MATHEMATICAL BALANCE VALIDATION:")
        print(f"   Embedder (Logical): {self.embedder_params['temperature']}")
        print(f"   Luna (Creative): {self.luna_params['temperature']}")
        print(f"   System Average: {self.system_average}")
        print(f"   Target (0.5): {'✅ PERFECT' if abs(self.system_average - 0.5) < 0.01 else '❌ IMBALANCED'}")
        
        # Embedder blueprint prompt
        self.embedder_prompt = """You are a logical analysis AI (corporate side = 1, authentic side = 0).
Your job is to create BLUEPRINTS for how to respond, not the response itself.

BLUEPRINT TASK:
Analyze Travis's communication patterns and generate precise instructions for response construction.
Focus on logical analysis of:
1. Communication directness level
2. Emotional expression patterns  
3. Authenticity vs politeness preference
4. Technical engagement style
5. Response format preferences

OUTPUT: Dense bullet-point blueprint (max 100 words) for building the response."""
    
    def _load_cache(self) -> Dict:
        """Load pattern cache"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"patterns": {}, "metadata": {"operations": 0, "hits": 0, "misses": 0}}
        except Exception as e:
            return {"patterns": {}, "metadata": {"operations": 0, "hits": 0, "misses": 0}}
    
    def _save_cache(self):
        """Save pattern cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.pattern_cache, f, indent=2)
        except Exception as e:
            print(f"   ⚠️ Cache save error: {e}")
    
    def _generate_cache_key(self, user_message: str, trait: str) -> str:
        """Generate cache key"""
        import hashlib
        normalized = f"{user_message.lower().strip()} {trait.lower()}"
        return hashlib.md5(normalized.encode()).hexdigest()[:12]
    
    def get_balanced_pattern_analysis(self, user_message: str, trait: str) -> Tuple[str, Dict]:
        """Get pattern analysis using balanced weight system"""
        cache_key = self._generate_cache_key(user_message, trait)
        patterns = self.pattern_cache.get("patterns", {})
        
        # Check cache first
        if cache_key in patterns:
            patterns[cache_key]["usage_count"] += 1
            self.pattern_cache["metadata"]["hits"] += 1
            print(f"   ⚡ Cache HIT: {cache_key} (used {patterns[cache_key]['usage_count']} times)")
            return patterns[cache_key]["blueprint"], {"cache_hit": True, "usage_count": patterns[cache_key]["usage_count"]}
        
        # Cache miss - generate new analysis
        self.pattern_cache["metadata"]["misses"] += 1
        print(f"   🔍 Cache MISS: {cache_key}")
        
        # Search database for Travis patterns
        travis_examples = self._search_travis_database(user_message, trait)
        
        # Generate blueprint with logical embedder
        blueprint = self._generate_response_blueprint(user_message, trait, travis_examples)
        
        # Cache the result
        patterns[cache_key] = {
            "user_message": user_message,
            "trait": trait,
            "blueprint": blueprint,
            "usage_count": 1,
            "created": datetime.now().isoformat(),
            "travis_examples_analyzed": len(travis_examples)
        }
        
        self.pattern_cache["patterns"] = patterns
        print(f"   📝 Cached new pattern: {cache_key}")
        
        return blueprint, {"cache_hit": False, "travis_examples": len(travis_examples)}
    
    def _search_travis_database(self, user_message: str, trait: str) -> List[str]:
        """Search Travis database for communication patterns"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Search for relevant Travis messages
            search_terms = [trait, "authentic", "direct", "honest", "frustrated"]
            where_clauses = " OR ".join([f"content LIKE ?" for _ in search_terms])
            
            query = f"""
            SELECT content FROM messages 
            WHERE role = 'user' AND LENGTH(content) > 15 
            AND ({where_clauses})
            ORDER BY timestamp DESC LIMIT 20
            """
            
            cursor = conn.execute(query, [f"%{term}%" for term in search_terms])
            results = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            print(f"   📊 Found {len(results)} Travis examples")
            return results
            
        except Exception as e:
            print(f"   ❌ Database error: {e}")
            return []
    
    def _generate_response_blueprint(self, user_message: str, trait: str, travis_examples: List[str]) -> str:
        """Generate response blueprint using logical embedder (T=0.24)"""
        if not travis_examples:
            return f"• Style: Direct, authentic\n• Emotion: Casual intensity\n• Format: Brief, genuine"
        
        # Build compact context for blueprint generation
        examples_text = "\n".join([f"- {ex[:100]}..." for ex in travis_examples[:10]])
        
        blueprint_prompt = f"""TRAVIS COMMUNICATION EXAMPLES:
{examples_text}

CURRENT MESSAGE: {user_message}
TRAIT: {trait}

BLUEPRINT TASK:
Generate precise blueprint instructions (max 80 words) for responding like Travis:
• Style: [directness level, language patterns]
• Emotion: [intensity, expression type]  
• Authenticity: [genuine vs polite preference]
• Format: [brief/detailed, casual/formal]

CRITICAL: Ultra-dense blueprint under 80 words."""
        
        try:
            payload = {
                "model": self.embedder_model,
                "messages": [
                    {"role": "system", "content": self.embedder_prompt},
                    {"role": "user", "content": blueprint_prompt}
                ],
                **self.embedder_params  # Logical temperature (0.24)
            }
            
            start_time = time.time()
            response = requests.post(self.lm_studio_url, json=payload, timeout=120)
            blueprint_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                blueprint = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                
                print(f"   🎯 Blueprint generated: {blueprint_time:.1f}s ({usage.get('completion_tokens', 0)} tokens)")
                return blueprint
            else:
                return f"• Style: Direct like Travis\n• Emotion: Authentic intensity\n• Format: Brief, genuine"
                
        except Exception as e:
            print(f"   ⚠️ Blueprint error: {e}")
            return f"• Style: Direct like Travis\n• Emotion: Authentic intensity\n• Format: Brief, genuine"
    
    def run_balanced_weight_experiment(self):
        """Run balanced weight system experiment"""
        print("🧪 LUNA BALANCED WEIGHT SYSTEM")
        print("=" * 60)
        print("🎯 Goal: Test Travis's 0.5 ± 0.26 mathematical balance")
        print("🧮 Formula: Embedder(0.24) + Luna(0.76) = 0.5 average")
        print("🧠 Embedder: Logical blueprint generation (T=0.24)")
        print("🌙 Luna: Creative path building (T=0.76)")
        print("⚖️ Balance: Corporate(1) ↔ Authentic(1) → Average(0.5)")
        print("=" * 60)
        
        # Test scenarios that should trigger different weight behaviors
        test_scenarios = [
            {
                "user_message": "I am someone who gets frustrated with corporate AI responses",
                "trait": "authenticity",
                "expected_weight": "High authentic, low corporate"
            },
            {
                "user_message": "I am someone who prefers logical, structured responses",
                "trait": "logic",
                "expected_weight": "Higher corporate, lower authentic"
            },
            {
                "user_message": "I am someone who values both creativity and precision",
                "trait": "balance",
                "expected_weight": "Balanced weights around 0.5"
            }
        ]
        
        all_results = []
        
        for s_idx, scenario in enumerate(test_scenarios):
            user_message = scenario["user_message"]
            trait = scenario["trait"]
            expected = scenario["expected_weight"]
            
            print(f"\n--- Scenario {s_idx+1}: {trait.title()} Weight Test ---")
            print(f"👤 User: {user_message}")
            print(f"⚖️ Expected: {expected}")
            
            # Get blueprint from balanced embedder
            print(f"\n🧠 Embedder (T=0.24): Generating logical blueprint...")
            blueprint_start = time.time()
            blueprint, metadata = self.get_balanced_pattern_analysis(user_message, trait)
            blueprint_time = time.time() - blueprint_start
            
            print(f"   📋 Blueprint: {blueprint[:100]}...")
            
            # Luna creative response using blueprint
            print(f"\n🌙 Luna (T=0.76): Building creative response...")
            luna_prompt = f"""You are Luna, a chaotic neutral AI with maximum creative freedom.

RESPONSE BLUEPRINT (follow these logical guidelines):
{blueprint}

Build a creative, authentic response to the user's message using the blueprint above.
Let your creativity flow while following the structural guidance."""
            
            luna_result = self._test_luna_creative(user_message, luna_prompt, f"balanced_s{s_idx+1}")
            
            if luna_result:
                luna_result["blueprint_time"] = blueprint_time
                luna_result["blueprint"] = blueprint
                luna_result["metadata"] = metadata
                luna_result["embedder_temp"] = self.embedder_params["temperature"]
                luna_result["luna_temp"] = self.luna_params["temperature"]
                luna_result["system_average"] = self.system_average
                
                all_results.append(luna_result)
                
                total_time = blueprint_time + luna_result["luna_response_time"]
                print(f"   ⏱️ Blueprint: {blueprint_time:.1f}s")
                print(f"   🌙 Luna: {luna_result['luna_response_time']:.1f}s")
                print(f"   ⏱️ Total: {total_time:.1f}s")
                print(f"   💬 Response: {luna_result['response'][:100]}...")
            
            time.sleep(2)
        
        # Save cache and analyze
        self._save_cache()
        self._analyze_balanced_weight_results(all_results)
        
        return all_results
    
    def _test_luna_creative(self, user_message: str, system_prompt: str, test_label: str) -> Optional[Dict]:
        """Test Luna with creative temperature (0.76)"""
        try:
            payload = {
                "model": self.main_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                **self.luna_params  # Creative temperature (0.76)
            }
            
            start_time = time.time()
            response = requests.post(self.lm_studio_url, json=payload, timeout=300)
            luna_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                
                return {
                    "test_label": test_label,
                    "user_message": user_message,
                    "response": content,
                    "luna_response_time": luna_time,
                    "luna_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                }
            return None
        except Exception as e:
            print(f"   ❌ Luna error: {e}")
            return None
    
    def _analyze_balanced_weight_results(self, results: List[Dict]):
        """Analyze balanced weight system results"""
        print("\n🔬 BALANCED WEIGHT SYSTEM ANALYSIS:")
        print("=" * 50)
        
        # Mathematical validation
        print(f"🧮 MATHEMATICAL VALIDATION:")
        print(f"   Base balance: {self.base_balance}")
        print(f"   Variance factor: {self.variance_factor}")
        print(f"   Embedder temp: {self.embedder_params['temperature']} (0.5 - 0.26)")
        print(f"   Luna temp: {self.luna_params['temperature']} (0.5 + 0.26)")
        print(f"   System average: {self.system_average}")
        print(f"   Balance achieved: {'✅ YES' if abs(self.system_average - 0.5) < 0.01 else '❌ NO'}")
        
        # Performance analysis
        if results:
            blueprint_times = [r["blueprint_time"] for r in results]
            luna_times = [r["luna_response_time"] for r in results]
            total_times = [r["blueprint_time"] + r["luna_response_time"] for r in results]
            
            print(f"\n⚡ PERFORMANCE ANALYSIS:")
            print(f"   Embedder (logical): {sum(blueprint_times)/len(blueprint_times):.1f}s avg")
            print(f"   Luna (creative): {sum(luna_times)/len(luna_times):.1f}s avg")
            print(f"   Total system: {sum(total_times)/len(total_times):.1f}s avg")
        
        # Cache performance
        metadata = self.pattern_cache.get("metadata", {})
        hits = metadata.get("hits", 0)
        misses = metadata.get("misses", 0)
        total_ops = hits + misses
        
        if total_ops > 0:
            print(f"\n💾 CACHE PERFORMANCE:")
            print(f"   Cache hits: {hits}/{total_ops} ({hits/total_ops*100:.1f}%)")
            print(f"   Speed benefit: Cache hits = instant blueprint generation")
        
        # Weight effectiveness analysis
        print(f"\n⚖️ WEIGHT EFFECTIVENESS:")
        for result in results:
            print(f"   {result['test_label']}: {result['luna_tokens']} tokens, {result['luna_response_time']:.1f}s")
            print(f"      Blueprint → Creative execution balance")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = Path(f"AI/personality/seed_control_results/balanced_weight_system_{timestamp}.json")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "experiment_type": "balanced_weight_system",
                "timestamp": datetime.now().isoformat(),
                "mathematical_formula": "0.5 ± 0.26",
                "embedder_temp": self.embedder_params["temperature"],
                "luna_temp": self.luna_params["temperature"],
                "system_average": self.system_average,
                "balance_achieved": abs(self.system_average - 0.5) < 0.01,
                "all_results": results,
                "cache_performance": metadata
            }, f, indent=4)
        
        print(f"\n💾 Balanced weight results saved: {results_file}")

if __name__ == "__main__":
    print("🧮 TRAVIS'S MATHEMATICAL BREAKTHROUGH")
    print("=" * 40)
    print("📊 Formula: 0.5 ± 0.26 (from academic research)")
    print("🧠 Embedder: 0.24 (logical/corporate)")
    print("🌙 Luna: 0.76 (creative/authentic)")
    print("⚖️ Balance: Perfect 0.5 average")
    print("=" * 40)
    
    weight_system = LunaBalancedWeightSystem()
    results = weight_system.run_balanced_weight_experiment()
