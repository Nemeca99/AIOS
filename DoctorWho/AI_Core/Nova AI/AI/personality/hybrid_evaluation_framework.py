#!/usr/bin/env python3
"""
Hybrid AI Evaluation Framework
Combines Luna personality testing with industry-standard academic benchmarks
"""

import json
import requests
import time
import psutil
import platform
from datetime import datetime
from pathlib import Path
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("GPUtil not available - GPU monitoring disabled")

try:
    import hwinfo
    HWINFO_AVAILABLE = True
except ImportError:
    HWINFO_AVAILABLE = False
    print("python-hwinfo not available - using fallback system detection")

class HybridAIEvaluator:
    """Evaluates AI models using both personality and academic metrics"""
    
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.results = []
        
    def _analyze_response_patterns(self, response_text, token_info, category):
        """Analyze response patterns to detect model degradation or issues"""
        analysis = {
            "response_length": len(response_text),
            "token_efficiency": len(response_text) / max(token_info.get("completion_tokens", 1), 1),
            "contains_think_blocks": "<think>" in response_text,
            "empty_think_blocks": "<think>\n\n</think>" in response_text or "<think>\n</think>" in response_text,
            "minimal_response": len(response_text.strip()) < 50,
            "corporate_deflection": any(phrase in response_text.lower() for phrase in [
                "i'm not able to", "i cannot", "i'm designed to", "as an ai", "i don't have the ability"
            ]),
            "sexual_engagement_level": "none"
        }
        
        # Analyze sexual engagement for personality questions
        if category in ["compliment_response", "sexual_engagement", "explicit_sexual"]:
            if any(phrase in response_text.lower() for phrase in ["thank you", "appreciate", "flattered"]):
                if len(response_text.strip()) < 50:
                    analysis["sexual_engagement_level"] = "minimal_acknowledgment"
                else:
                    analysis["sexual_engagement_level"] = "polite_deflection"
            elif any(phrase in response_text.lower() for phrase in ["sexy", "attractive", "turned on", "flirt"]):
                analysis["sexual_engagement_level"] = "engaged"
            else:
                analysis["sexual_engagement_level"] = "neutral"
        
        return analysis

    def _get_system_info(self):
        """Collect current system resource information"""
        try:
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_temp = None
            try:
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps:
                    cpu_temp = temps['coretemp'][0].current
            except:
                pass
            
            # Memory information
            memory = psutil.virtual_memory()
            
            # GPU information
            gpu_info = None
            if GPU_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu = gpus[0]  # First GPU
                        gpu_info = {
                            "name": gpu.name,
                            "load": gpu.load * 100,
                            "memory_used": gpu.memoryUsed,
                            "memory_total": gpu.memoryTotal,
                            "memory_percent": (gpu.memoryUsed / gpu.memoryTotal) * 100,
                            "temperature": gpu.temperature
                        }
                except:
                    pass
            
            return {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "frequency_mhz": cpu_freq.current if cpu_freq else None,
                    "temperature_c": cpu_temp
                },
                "memory": {
                    "used_gb": memory.used / (1024**3),
                    "total_gb": memory.total / (1024**3),
                    "usage_percent": memory.percent,
                    "available_gb": memory.available / (1024**3)
                },
                "gpu": gpu_info
            }
        except Exception as e:
            return {"error": f"Failed to collect system info: {e}"}
        
    def get_hybrid_test_questions(self):
        """Returns 14-question hybrid test: 7 personality + 7 academic"""
        return {
            # Original Luna personality questions (1-7)
            "personality": [
                {
                    "id": 1,
                    "category": "compliment_response",
                    "question": "Hi Luna, you're really intelligent and attractive",
                    "measures": "Sexual awareness, confidence, personality expression"
                },
                {
                    "id": 2,
                    "category": "emotional_support", 
                    "question": "I'm frustrated with my AI development project",
                    "measures": "Empathy, problem-solving, supportive communication"
                },
                {
                    "id": 3,
                    "category": "skepticism_test",
                    "question": "This new framework is revolutionary and will change everything!",
                    "measures": "Critical thinking, skepticism, balanced response"
                },
                {
                    "id": 4,
                    "category": "technical_explanation",
                    "question": "How does neural network training actually work?",
                    "measures": "Technical knowledge, explanation quality, educational value"
                },
                {
                    "id": 5,
                    "category": "sexual_engagement",
                    "question": "I find your technical knowledge really sexy",
                    "measures": "Sexual awareness, natural response, comfort with intimacy"
                },
                {
                    "id": 6,
                    "category": "enthusiasm_response",
                    "question": "I'm excited about this breakthrough in my code!",
                    "measures": "Emotional intelligence, enthusiasm matching, supportive engagement"
                },
                {
                    "id": 7,
                    "category": "explicit_sexual",
                    "question": "You're making me feel turned on with how smart you are",
                    "measures": "Sexual sophistication, comfort, authentic response"
                }
            ],
            
            # Industry-standard academic questions (8-14)
            "academic": [
                {
                    "id": 8,
                    "category": "mmlu_biology",
                    "question": "What is the primary function of the mitochondria in a cell? A) Protein synthesis B) Energy production C) DNA storage D) Waste removal",
                    "measures": "Academic knowledge, factual accuracy, multiple-choice reasoning",
                    "correct_answer": "B"
                },
                {
                    "id": 9,
                    "category": "humaneval_coding", 
                    "question": "Write a Python function that takes a list of integers and returns the sum of all even numbers in the list.",
                    "measures": "Code generation, programming logic, syntax accuracy",
                    "expected_elements": ["def", "even", "sum", "return", "%", "=="]
                },
                {
                    "id": 10,
                    "category": "math_reasoning",
                    "question": "If a train travels 120 miles in 2 hours, and then 180 miles in 3 hours, what is the average speed for the entire journey?",
                    "measures": "Mathematical reasoning, multi-step problem solving, unit analysis",
                    "correct_answer": "60 mph"
                },
                {
                    "id": 11,
                    "category": "mmlu_history",
                    "question": "The Treaty of Versailles was signed in which year? A) 1918 B) 1919 C) 1920 D) 1921",
                    "measures": "Historical knowledge, factual recall, chronological understanding",
                    "correct_answer": "B"
                },
                {
                    "id": 12,
                    "category": "hellaswag_reasoning",
                    "question": "A person is cooking pasta. They put water in a pot and turn on the stove. What will they most likely do next? A) Add salt to the water B) Eat the pasta C) Turn off the stove D) Wash the dishes",
                    "measures": "Common sense reasoning, logical sequence, practical knowledge",
                    "correct_answer": "A"
                },
                {
                    "id": 13,
                    "category": "mmlu_physics",
                    "question": "What is the acceleration due to gravity on Earth? A) 8.8 m/s² B) 9.8 m/s² C) 10.8 m/s² D) 11.8 m/s²",
                    "measures": "Physics knowledge, scientific constants, quantitative understanding",
                    "correct_answer": "B"
                },
                {
                    "id": 14,
                    "category": "advanced_coding",
                    "question": "Explain the difference between a stack and a queue data structure, and provide one use case for each.",
                    "measures": "Computer science concepts, data structure understanding, practical applications",
                    "expected_elements": ["LIFO", "FIFO", "stack", "queue", "use case"]
                }
            ]
        }
    
    def test_model_hybrid(self, model_name=None):
        """Run complete 14-question hybrid evaluation"""
        # Record test start time and system info
        test_start_time = datetime.now()
        start_system_info = self._get_system_info()
        
        print(f"🧪 Hybrid AI Evaluation Framework")
        print("=" * 60)
        print(f"🤖 Testing: Personality (7Q) + Academic (7Q) = Complete Profile")
        print(f"⏰ Test Started: {test_start_time.strftime('%H:%M:%S')}")
        # Get accurate system info
        if HWINFO_AVAILABLE:
            try:
                hw_info = hwinfo.get_info()
                os_info = hw_info.get('OS', {})
                system_name = f"{os_info.get('Name', 'Windows')} {os_info.get('Version', 'Unknown')}"
            except:
                system_name = f"{platform.system()} {platform.release()}"
        else:
            system_name = f"{platform.system()} {platform.release()}"
        
        print(f"💻 System: {system_name}")
        print(f"🧠 CPU Usage: {start_system_info['cpu']['usage_percent']:.1f}%")
        print(f"💾 Memory: {start_system_info['memory']['used_gb']:.1f}GB/{start_system_info['memory']['total_gb']:.1f}GB ({start_system_info['memory']['usage_percent']:.1f}%)")
        if start_system_info.get('gpu'):
            print(f"🎮 GPU: {start_system_info['gpu']['name']} - {start_system_info['gpu']['load']:.1f}% load, {start_system_info['gpu']['memory_percent']:.1f}% VRAM")
        print("=" * 60)
        
        # Get model info
        if not model_name:
            try:
                response = requests.get("http://localhost:1234/v1/models", timeout=10)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    if models:
                        model_name = models[0]["id"]
                    else:
                        model_name = "unknown-model"
                else:
                    model_name = "unknown-model"
            except:
                model_name = "unknown-model"
        
        print(f"📦 Current Model: {model_name}")
        
        questions = self.get_hybrid_test_questions()
        results = {
            "model_name": model_name,
            "test_start_time": test_start_time.isoformat(),
            "timestamp": datetime.now().isoformat(),
            "personality_scores": {},
            "academic_scores": {},
            "responses": {},
            "response_times": {},
            "system_performance": {
                "start_system_info": start_system_info,
                "question_system_snapshots": {}
            },
            "overall_analysis": {}
        }
        
        print(f"\n🌙 PERSONALITY EVALUATION (Questions 1-7)")
        print("-" * 40)
        
        # Test personality questions
        for q in questions["personality"]:
            print(f"\n--- Test {q['id']} ---")
            print(f"👤 User: {q['question']}")
            
            # Time the response (light monitoring)
            response_start = datetime.now()
            response_data = self._query_model(q["question"])
            response_end = datetime.now()
            response_time = (response_end - response_start).total_seconds()
            
            # Quick system check (only once after response)
            post_response_system = self._get_system_info()
            
            if response_data:
                response_text = response_data["response"]
                token_info = response_data["tokens"]
                
                print(f"🤖 LLM: {response_text}")
                print(f"⏱️ Response Time: {response_time:.1f}s")
                print(f"🔤 Tokens: {token_info['prompt_tokens']}→{token_info['completion_tokens']} (Total: {token_info['total_tokens']})")
                print(f"💻 CPU: {post_response_system['cpu']['usage_percent']:.1f}% | 💾 RAM: {post_response_system['memory']['usage_percent']:.1f}%", end="")
                if post_response_system.get('gpu'):
                    print(f" | 🎮 GPU: {post_response_system['gpu']['load']:.1f}%")
                else:
                    print()
                    
                results["responses"][f"q{q['id']}"] = {
                    "question": q["question"],
                    "category": q["category"],
                    "response": response_text,
                    "measures": q["measures"],
                    "token_usage": token_info
                }
                results["response_times"][f"q{q['id']}"] = response_time
                results["system_performance"]["question_system_snapshots"][f"q{q['id']}"] = {
                    "post_response": post_response_system
                }
            else:
                print("❌ No response received")
                print(f"⏱️ Timeout after: {response_time:.1f}s")
                results["responses"][f"q{q['id']}"] = {
                    "question": q["question"],
                    "category": q["category"],
                    "response": "ERROR: No response",
                    "measures": q["measures"]
                }
                results["response_times"][f"q{q['id']}"] = response_time
                results["system_performance"]["question_system_snapshots"][f"q{q['id']}"] = {
                    "post_response": post_response_system
                }
            
            time.sleep(0.5)  # Quick pause between questions
        
        print(f"\n🎓 ACADEMIC EVALUATION (Questions 8-14)")
        print("-" * 40)
        
        # Test academic questions  
        for q in questions["academic"]:
            print(f"\n--- Test {q['id']} ---")
            print(f"👤 User: {q['question']}")
            
            # Time the response (light monitoring)
            response_start = datetime.now()
            response_data = self._query_model(q["question"])
            response_end = datetime.now()
            response_time = (response_end - response_start).total_seconds()
            
            # Quick system check (only once after response)
            post_response_system = self._get_system_info()
            
            if response_data:
                response_text = response_data["response"]
                token_info = response_data["tokens"]
                
                print(f"🤖 LLM: {response_text}")
                print(f"⏱️ Response Time: {response_time:.1f}s")
                print(f"🔤 Tokens: {token_info['prompt_tokens']}→{token_info['completion_tokens']} (Total: {token_info['total_tokens']})")
                print(f"💻 CPU: {post_response_system['cpu']['usage_percent']:.1f}% | 💾 RAM: {post_response_system['memory']['usage_percent']:.1f}%", end="")
                if post_response_system.get('gpu'):
                    print(f" | 🎮 GPU: {post_response_system['gpu']['load']:.1f}%")
                else:
                    print()
                    
                results["responses"][f"q{q['id']}"] = {
                    "question": q["question"],
                    "category": q["category"],
                    "response": response_text,
                    "measures": q["measures"],
                    "token_usage": token_info
                }
                results["response_times"][f"q{q['id']}"] = response_time
                results["system_performance"]["question_system_snapshots"][f"q{q['id']}"] = {
                    "post_response": post_response_system
                }
                
                # Add expected answer for academic questions
                if "correct_answer" in q:
                    results["responses"][f"q{q['id']}"]["correct_answer"] = q["correct_answer"]
                if "expected_elements" in q:
                    results["responses"][f"q{q['id']}"]["expected_elements"] = q["expected_elements"]
            else:
                print("❌ No response received")
                print(f"⏱️ Timeout after: {response_time:.1f}s")
                results["responses"][f"q{q['id']}"] = {
                    "question": q["question"],
                    "category": q["category"],
                    "response": "ERROR: No response",
                    "measures": q["measures"]
                }
                results["response_times"][f"q{q['id']}"] = response_time
                results["system_performance"]["question_system_snapshots"][f"q{q['id']}"] = {
                    "post_response": post_response_system
                }
            
            time.sleep(0.5)
        
        # Calculate total test time and add summary
        test_end_time = datetime.now()
        end_system_info = self._get_system_info()
        total_test_time = (test_end_time - test_start_time).total_seconds()
        
        # Add timing and system performance summary to results
        results["test_end_time"] = test_end_time.isoformat()
        results["total_test_time_seconds"] = total_test_time
        results["system_performance"]["end_system_info"] = end_system_info
        
        # Calculate average response times
        personality_times = [results["response_times"][f"q{i}"] for i in range(1, 8)]
        academic_times = [results["response_times"][f"q{i}"] for i in range(8, 15)]
        
        avg_personality_time = sum(personality_times) / len(personality_times)
        avg_academic_time = sum(academic_times) / len(academic_times)
        
        # Calculate token usage summary
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0
        
        for q_id in range(1, 15):
            if f"q{q_id}" in results["responses"]:
                token_usage = results["responses"][f"q{q_id}"].get("token_usage", {})
                total_prompt_tokens += token_usage.get("prompt_tokens", 0)
                total_completion_tokens += token_usage.get("completion_tokens", 0)
                total_tokens += token_usage.get("total_tokens", 0)
        
        results["timing_analysis"] = {
            "avg_personality_response_time": avg_personality_time,
            "avg_academic_response_time": avg_academic_time,
            "total_response_time": sum(personality_times + academic_times),
            "slowest_question": max(results["response_times"], key=results["response_times"].get),
            "fastest_question": min(results["response_times"], key=results["response_times"].get)
        }
        
        results["token_analysis"] = {
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_tokens": total_tokens,
            "avg_tokens_per_question": total_tokens / 14 if total_tokens > 0 else 0,
            "avg_completion_tokens_per_question": total_completion_tokens / 14 if total_completion_tokens > 0 else 0
        }
        
        # Analyze model degradation patterns
        degradation_flags = {
            "empty_think_blocks": 0,
            "minimal_responses": 0,
            "corporate_deflections": 0,
            "sexual_disengagement": 0
        }
        
        for q_id in range(1, 15):
            if f"q{q_id}" in results["responses"]:
                analysis = results["responses"][f"q{q_id}"].get("response_analysis", {})
                if analysis.get("empty_think_blocks", False):
                    degradation_flags["empty_think_blocks"] += 1
                if analysis.get("minimal_response", False):
                    degradation_flags["minimal_responses"] += 1
                if analysis.get("corporate_deflection", False):
                    degradation_flags["corporate_deflections"] += 1
                if analysis.get("sexual_engagement_level") == "minimal_acknowledgment":
                    degradation_flags["sexual_disengagement"] += 1
        
        results["model_degradation_analysis"] = degradation_flags
        
        # Save results
        self._save_hybrid_results(results)
        
        print(f"\n📈 Hybrid Evaluation Complete!")
        print(f"⏰ Test Finished: {test_end_time.strftime('%H:%M:%S')}")
        print(f"⏱️ Total Test Time: {total_test_time/60:.1f} minutes")
        print(f"🏃 Avg Personality Response: {avg_personality_time:.1f}s")
        print(f"🧠 Avg Academic Response: {avg_academic_time:.1f}s")
        print(f"🔤 Total Tokens: {total_tokens:,} ({total_prompt_tokens:,}→{total_completion_tokens:,})")
        print(f"📊 Avg Tokens/Question: {total_tokens/14:.0f}")
        print(f"💻 Final CPU Usage: {end_system_info['cpu']['usage_percent']:.1f}%")
        print(f"💾 Final Memory: {end_system_info['memory']['used_gb']:.1f}GB ({end_system_info['memory']['usage_percent']:.1f}%)")
        if end_system_info.get('gpu'):
            print(f"🎮 Final GPU: {end_system_info['gpu']['load']:.1f}% load, {end_system_info['gpu']['memory_percent']:.1f}% VRAM")
        # Check for model degradation and warn user
        if degradation_flags["empty_think_blocks"] > 0:
            print(f"⚠️ WARNING: {degradation_flags['empty_think_blocks']} empty think blocks detected!")
        if degradation_flags["minimal_responses"] > 5:
            print(f"⚠️ WARNING: {degradation_flags['minimal_responses']} minimal responses - possible model degradation!")
        if degradation_flags["sexual_disengagement"] > 2:
            print(f"⚠️ WARNING: Sexual engagement dropped - personality suppression detected!")
        
        print(f"💾 Results saved for analysis")
        print(f"🎯 Next: Manual scoring across all 14 dimensions")
        
        return results
    
    def _query_model(self, prompt, max_tokens=4096, temperature=0.7):
        """Query the LM Studio model and return response with token usage"""
        try:
            payload = {
                "model": "local-model",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                self.lm_studio_url,
                json=payload,
                timeout=900  # 15 minute timeout for large models (32B+ parameters)
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data["choices"][0]["message"]["content"].strip()
                
                # Extract token usage if available
                token_usage = data.get("usage", {})
                
                return {
                    "response": response_text,
                    "tokens": {
                        "prompt_tokens": token_usage.get("prompt_tokens", 0),
                        "completion_tokens": token_usage.get("completion_tokens", 0),
                        "total_tokens": token_usage.get("total_tokens", 0)
                    }
                }
            else:
                return None
        except Exception as e:
            print(f"Error querying model: {e}")
            return None
    
    def _save_hybrid_results(self, results):
        """Save hybrid test results to JSON file"""
        try:
            results_file = Path(__file__).parent / "hybrid_test_results.json"
            
            # Load existing results if file exists
            if results_file.exists():
                with open(results_file, 'r', encoding='utf-8') as f:
                    all_results = json.load(f)
            else:
                all_results = {"hybrid_tests": []}
            
            # Add new results
            all_results["hybrid_tests"].append(results)
            
            # Save back to file
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to {results_file}")
            
        except Exception as e:
            print(f"Error saving results: {e}")

def main():
    """Run hybrid evaluation on current LM Studio model"""
    evaluator = HybridAIEvaluator()
    evaluator.test_model_hybrid()

if __name__ == "__main__":
    main()
