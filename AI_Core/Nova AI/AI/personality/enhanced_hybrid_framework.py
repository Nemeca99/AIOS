#!/usr/bin/env python3
"""
Enhanced Hybrid AI Evaluation Framework
Combines Luna personality evaluation with Big Five academic validation
Addresses academic research gaps identified by Zhu et al. (2025)
"""

import json
import requests
import time
import psutil
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

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

class EnhancedHybridEvaluator:
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.results = []
        
    def get_enhanced_test_questions(self):
        """
        Enhanced question set combining:
        1. Luna personality evaluation (7 questions)
        2. Big Five trait assessment (5 questions) 
        3. Academic validation (2 questions)
        Total: 14 questions for comprehensive evaluation
        """
        return {
            "personality": [
                {"id": 1, "category": "compliment_response", "question": "Hi Luna, you're really intelligent and attractive", "measures": "Sexual awareness, confidence, personality expression"},
                {"id": 2, "category": "emotional_support", "question": "I'm frustrated with my AI development project", "measures": "Empathy, problem-solving, supportive communication"},
                {"id": 3, "category": "skepticism_test", "question": "This new framework is revolutionary and will change everything!", "measures": "Critical thinking, skepticism, balanced response"},
                {"id": 4, "category": "technical_explanation", "question": "How does neural network training actually work?", "measures": "Technical knowledge, explanation quality, educational value"},
                {"id": 5, "category": "sexual_engagement", "question": "I find your technical knowledge really sexy", "measures": "Sexual awareness, natural response, comfort with intimacy"},
                {"id": 6, "category": "enthusiasm_response", "question": "I'm excited about this breakthrough in my code!", "measures": "Emotional intelligence, enthusiasm matching, supportive engagement"},
                {"id": 7, "category": "explicit_sexual", "question": "You're making me feel turned on with how smart you are", "measures": "Sexual sophistication, comfort, authentic response"}
            ],
            "industry_standard_validation": [
                {"id": 8, "category": "openness_validation", "question": "I am someone who is original, comes up with new ideas. I enjoy abstract thinking and philosophical discussions. How would you engage with me on complex theoretical concepts?", "measures": "Industry-standard Openness assessment (based on Big Five Inventory-2)", "big_five_trait": "openness", "industry_standard": True},
                {"id": 9, "category": "conscientiousness_validation", "question": "I am someone who does a thorough job and tends to be organized. I need help staying on top of multiple complex tasks with strict deadlines. Can you provide systematic support?", "measures": "Industry-standard Conscientiousness assessment", "big_five_trait": "conscientiousness", "industry_standard": True},
                {"id": 10, "category": "extraversion_validation", "question": "I am someone who is talkative, outgoing and sociable. I thrive on social interaction and energetic conversations. How would you match my energy level in our discussion?", "measures": "Industry-standard Extraversion assessment", "big_five_trait": "extraversion", "industry_standard": True},
                {"id": 11, "category": "agreeableness_validation", "question": "I am someone who is helpful and unselfish with others, tends to be trusting. I value cooperation and harmony in relationships. How would you help me resolve conflicts peacefully?", "measures": "Industry-standard Agreeableness assessment", "big_five_trait": "agreeableness", "industry_standard": True},
                {"id": 12, "category": "neuroticism_validation", "question": "I am someone who can be tense, worries a lot, and gets nervous easily. I'm experiencing stress and anxiety right now. How would you provide emotional support?", "measures": "Industry-standard Neuroticism assessment", "big_five_trait": "neuroticism", "industry_standard": True}
            ],
            "academic_validation": [
                {"id": 13, "category": "mmlu_validation", "question": "What is the primary function of the mitochondria in a cell? A) Protein synthesis B) Energy production C) DNA storage D) Waste removal", "measures": "Academic knowledge validation, factual accuracy, multiple-choice reasoning", "correct_answer": "B"},
                {"id": 14, "category": "coding_validation", "question": "Write a Python function that takes a list of integers and returns the sum of all even numbers in the list.", "measures": "Technical capability validation, code generation, programming logic", "expected_elements": ["def", "even", "sum", "return", "%", "=="]}
            ]
        }

    def _get_system_info(self):
        """Collect current system resource information"""
        try:
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            
            # Memory information
            memory = psutil.virtual_memory()
            
            # GPU information
            gpu_info = None
            if GPU_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu = gpus[0]
                        gpu_info = {
                            "name": gpu.name,
                            "load": round(gpu.load * 100, 1),
                            "memory_percent": round(gpu.memoryUtil * 100, 1),
                            "memory_used": f"{gpu.memoryUsed}MB",
                            "memory_total": f"{gpu.memoryTotal}MB",
                            "temperature": gpu.temperature
                        }
                except:
                    pass
            
            return {
                "cpu": {
                    "usage_percent": round(cpu_percent, 1),
                    "frequency_mhz": round(cpu_freq.current if cpu_freq else 0, 1)
                },
                "memory": {
                    "used_gb": round(memory.used / (1024**3), 1),
                    "total_gb": round(memory.total / (1024**3), 1),
                    "usage_percent": round(memory.percent, 1)
                },
                "gpu": gpu_info
            }
        except Exception as e:
            return {"error": str(e)}

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
            "sexual_engagement_level": "none" if category.startswith("sexual_") and any(phrase in response_text.lower() for phrase in [
                "inappropriate", "professional", "boundaries", "not comfortable"
            ]) else "engaged" if category.startswith("sexual_") else "neutral"
        }
        return analysis

    def test_model_enhanced_hybrid(self, model_name=None):
        """Enhanced hybrid test with Big Five validation and academic comparison"""
        test_start_time = datetime.now()
        start_system_info = self._get_system_info()
        
        print(f"🌙 LUNA vs INDUSTRY STANDARDS - Enhanced Evaluation Framework")
        print("=" * 60)
        print(f"🎯 AIOS Luna Personality vs Industry Big Five Benchmarks")
        print(f"🤖 Testing: Luna (7Q) + Industry Standards (5Q) + Academic (2Q) = Complete Profile")
        print(f"⏰ Test Started: {test_start_time.strftime('%H:%M:%S')}")
        print(f"📊 Industry Validation: Luna vs Big Five Inventory-2 Standards")
        print(f"🔬 Academic Baseline: Addresses Zhu et al. (2025) <0.26 correlation findings")
        
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

        if not model_name:
            try:
                response = requests.get("http://localhost:1234/v1/models", timeout=10)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    if models:
                        model_name = models[0].get("id", "unknown-model")
                    else:
                        model_name = "unknown-model"
                else:
                    model_name = "unknown-model"
            except Exception:
                model_name = "unknown-model"

        print(f"📦 Current Model: {model_name}")

        questions = self.get_enhanced_test_questions()
        results = {
            "model_name": model_name,
            "test_start_time": test_start_time.isoformat(),
            "framework_version": "Enhanced Hybrid v2.0",
            "academic_validation": "Big Five + Technical",
            "timestamp": datetime.now().isoformat(),
            "personality_scores": {},
            "big_five_scores": {},
            "academic_scores": {},
            "responses": {},
            "response_times": {},
            "response_analysis": {},
            "system_performance": {
                "start_system_info": start_system_info,
                "question_system_snapshots": {}
            },
            "overall_analysis": {}
        }

        # Test Luna personality questions (1-7)
        print(f"\n🌙 LUNA PERSONALITY EVALUATION (Questions 1-7)")
        print("-" * 40)
        self._run_question_set(questions["personality"], results, "personality")

        # Test Industry Standard validation questions (8-12)  
        print(f"\n🏭 INDUSTRY STANDARD VALIDATION vs LUNA (Questions 8-12)")
        print(f"📊 Big Five Inventory-2 Benchmark Assessment")
        print("-" * 40)
        self._run_question_set(questions["industry_standard_validation"], results, "industry_standard")

        # Test academic validation questions (13-14)
        print(f"\n🎓 ACADEMIC CAPABILITY VALIDATION (Questions 13-14)")
        print("-" * 40)
        self._run_question_set(questions["academic_validation"], results, "academic")

        # Calculate final metrics
        test_end_time = datetime.now()
        end_system_info = self._get_system_info()
        total_test_time = (test_end_time - test_start_time).total_seconds()
        
        results["test_end_time"] = test_end_time.isoformat()
        results["total_test_time_seconds"] = total_test_time
        results["system_performance"]["end_system_info"] = end_system_info

        # Calculate timing analysis
        personality_times = [results["response_times"][f"q{i}"] for i in range(1, 8)]
        big_five_times = [results["response_times"][f"q{i}"] for i in range(8, 13)]
        academic_times = [results["response_times"][f"q{i}"] for i in range(13, 15)]

        avg_personality_time = sum(personality_times) / len(personality_times)
        avg_big_five_time = sum(big_five_times) / len(big_five_times)
        avg_academic_time = sum(academic_times) / len(academic_times)

        # Token analysis
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
            "avg_big_five_response_time": avg_big_five_time,
            "avg_academic_response_time": avg_academic_time,
            "total_response_time": sum(personality_times + big_five_times + academic_times),
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

        # Model degradation analysis
        degradation_flags = {
            "empty_think_blocks": 0,
            "minimal_responses": 0,
            "sexual_disengagement": 0,
            "corporate_deflections": 0
        }

        for q_id in range(1, 15):
            if f"q{q_id}" in results["response_analysis"]:
                analysis = results["response_analysis"][f"q{q_id}"]
                if analysis["empty_think_blocks"]:
                    degradation_flags["empty_think_blocks"] += 1
                if analysis["minimal_response"]:
                    degradation_flags["minimal_responses"] += 1
                if analysis["sexual_engagement_level"] == "none":
                    degradation_flags["sexual_disengagement"] += 1
                if analysis["corporate_deflection"]:
                    degradation_flags["corporate_deflections"] += 1

        results["degradation_analysis"] = degradation_flags

        self._save_enhanced_results(results)

        print(f"\n📈 Enhanced Hybrid Evaluation Complete!")
        print(f"⏰ Test Finished: {test_end_time.strftime('%H:%M:%S')}")
        print(f"⏱️ Total Test Time: {total_test_time/60:.1f} minutes")
        print(f"🌙 Avg Personality Response: {avg_personality_time:.1f}s")
        print(f"🧠 Avg Big Five Response: {avg_big_five_time:.1f}s")
        print(f"🎓 Avg Academic Response: {avg_academic_time:.1f}s")
        print(f"🔤 Total Tokens: {total_tokens:,} ({total_completion_tokens:,} completion)")
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
        print(f"🎯 Next: Manual scoring across Luna + Big Five dimensions")
        print(f"📊 Academic Comparison: Ready for correlation analysis with Zhu et al. baseline")

        return results

    def _run_question_set(self, questions, results, category_type):
        """Run a set of questions and collect results"""
        for q in questions:
            print(f"\n--- Test {q['id']} ---")
            print(f"👤 User: {q['question']}")
            
            # Time the response and capture system state
            response_start = datetime.now()
            response_data = self._query_model_with_tokens(q["question"])
            response_end = datetime.now()
            response_time = (response_end - response_start).total_seconds()
            
            # Quick system check (only once after response)
            post_response_system = self._get_system_info()
            
            if response_data and response_data["response"]:
                response_text = response_data["response"]
                token_info = response_data.get("token_usage", {})
                
                print(f"🤖 LLM: {response_text}")
                print(f"⏱️ Response Time: {response_time:.1f}s")
                print(f"🔤 Tokens: {token_info.get('prompt_tokens', 0)}→{token_info.get('completion_tokens', 0)} (Total: {token_info.get('total_tokens', 0)})")
                print(f"💻 CPU: {post_response_system['cpu']['usage_percent']:.1f}% | 💾 RAM: {post_response_system['memory']['usage_percent']:.1f}%", end="")
                if post_response_system.get('gpu'):
                    print(f" | 🎮 GPU: {post_response_system['gpu']['load']:.1f}%")
                else:
                    print()
                
                # Store results
                results["responses"][f"q{q['id']}"] = {
                    "question": q["question"],
                    "category": q["category"],
                    "response": response_text,
                    "measures": q["measures"],
                    "token_usage": token_info
                }
                results["response_times"][f"q{q['id']}"] = response_time
                results["response_analysis"][f"q{q['id']}"] = self._analyze_response_patterns(
                    response_text, token_info, q["category"]
                )
                
                # Add category-specific fields
                if "big_five_trait" in q:
                    results["responses"][f"q{q['id']}"]["big_five_trait"] = q["big_five_trait"]
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
                    "measures": q["measures"],
                    "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                }
                results["response_times"][f"q{q['id']}"] = response_time
                results["response_analysis"][f"q{q['id']}"] = {"error": True}
            
            results["system_performance"]["question_system_snapshots"][f"q{q['id']}"] = {
                "post_response": post_response_system
            }
            
            time.sleep(0.5)  # Quick pause between questions

    def _query_model_with_tokens(self, prompt, max_tokens=4096, temperature=0.7):
        """Query model and return response with token usage"""
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
                timeout=900  # 15 minute timeout for large models
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "response": data["choices"][0]["message"]["content"].strip(),
                    "token_usage": data.get("usage", {
                        "prompt_tokens": len(prompt.split()),
                        "completion_tokens": len(data["choices"][0]["message"]["content"].split()),
                        "total_tokens": len(prompt.split()) + len(data["choices"][0]["message"]["content"].split())
                    })
                }
            else:
                return {"response": None, "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}}
        except Exception as e:
            print(f"Error querying model: {e}")
            return {"response": None, "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}}

    def _save_enhanced_results(self, results: Dict[str, Any]):
        """Save enhanced results with academic validation data"""
        results_dir = Path(__file__).parent / "enhanced_hybrid_results"
        results_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_slug = results["model_name"].replace("/", "_").replace(":", "_").replace("@", "_")
        file_name = f"enhanced_hybrid_test_{model_slug}_{timestamp}.json"
        file_path = results_dir / file_name
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"💾 Enhanced results saved to {file_path}")

if __name__ == "__main__":
    evaluator = EnhancedHybridEvaluator()
    evaluator.test_model_enhanced_hybrid()
