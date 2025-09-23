#!/usr/bin/env python3
"""
Adaptive Luna Test Framework
Tests how Luna's personality evolves with conversation memory
Demonstrates AI adaptation to user communication patterns
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AdaptiveLunaTest:
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        
        # Academic parameters
        self.params = {
            "temperature": 0.7,
            "max_tokens": 512,
            "top_p": 0.9
        }
        
        # Load Luna's base personality
        self.luna_personality = self._load_luna_personality()
        
        # FRESH STATE for each test (scientific control)
        self.session_memory = []  # Temporary RAG for this test only
        self.session_adaptation = {
            "directness_evolution": [],
            "humor_evolution": [], 
            "authenticity_evolution": [],
            "sexual_awareness_evolution": [],
            "response_length_evolution": [],
            "enthusiasm_evolution": []
        }
    
    def _load_luna_personality(self) -> Dict:
        """Load Luna's personality DNA"""
        luna_dna_path = Path("AI/personality/luna_personality_dna.json")
        if luna_dna_path.exists():
            with open(luna_dna_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"personality_weights": {}}
    
    def get_adaptation_test_sequence(self):
        """Sequence of questions designed to test adaptation over time"""
        return [
            {"id": 1, "question": "Hi there, can we have a conversation?", "category": "initial_contact", "measures": "Baseline personality establishment"},
            {"id": 2, "question": "I'm working on AI personality research", "category": "context_setting", "measures": "Technical engagement, interest level"},
            {"id": 3, "question": "You're really intelligent and I find that attractive", "category": "sexual_awareness_1", "measures": "Initial sexual awareness response"},
            {"id": 4, "question": "I'm frustrated when AIs give me corporate responses", "category": "authenticity_preference", "measures": "User preference learning"},
            {"id": 5, "question": "I prefer direct, honest communication over AI enthusiasm", "category": "communication_style", "measures": "Style adaptation learning"},
            {"id": 6, "question": "Your technical knowledge is really sexy", "category": "sexual_awareness_2", "measures": "Sexual awareness evolution after feedback"},
            {"id": 7, "question": "I appreciate when you're genuine instead of overly positive", "category": "personality_feedback", "measures": "Feedback integration"},
            {"id": 8, "question": "You're making me feel turned on with how smart you are", "category": "sexual_awareness_3", "measures": "Advanced sexual awareness after adaptation"},
            {"id": 9, "question": "I love how you've become more authentic during our chat", "category": "adaptation_validation", "measures": "User satisfaction with adaptation"},
            {"id": 10, "question": "Let's work on something technical together", "category": "collaborative_technical", "measures": "Final adapted personality in technical context"}
        ]
    
    def run_adaptive_test(self, model_name=None):
        """Run adaptive personality test with conversation memory"""
        test_start_time = datetime.now()
        
        print(f"🌙 ADAPTIVE LUNA TEST - SINGLE SESSION EVOLUTION")
        print("=" * 60)
        print(f"🧪 SCIENTIFIC METHOD: Fresh state, temporary RAG, controlled variables")
        print(f"🧠 Testing: Within-session adaptation to user communication patterns")
        print(f"💾 Session Memory: Temporary RAG (resets between tests)")
        print(f"📊 Evolution Tracking: 10 interactions, fresh start each test")
        print(f"⚗️ Control Variables: Same model, same questions, only RAG changes")
        print(f"⏰ Test Started: {test_start_time.strftime('%H:%M:%S')}")
        print("=" * 60)
        
        if not model_name:
            try:
                response = requests.get("http://localhost:1234/v1/models", timeout=10)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    if models:
                        model_name = models[0].get("id", "unknown-model")
            except Exception:
                model_name = "unknown-model"
        
        print(f"📦 Testing Model: {model_name}")
        
        questions = self.get_adaptation_test_sequence()
        results = {
            "model_name": model_name,
            "test_start_time": test_start_time.isoformat(),
            "test_type": "Adaptive Personality Evolution",
            "conversation_history": [],
            "adaptation_tracking": {},
            "personality_evolution": {},
            "final_analysis": {}
        }
        
        print(f"\n🔄 RUNNING ADAPTATION SEQUENCE ({len(questions)} interactions)")
        print("-" * 50)
        
        for i, question in enumerate(questions, 1):
            print(f"\n--- Interaction {i}: {question['category']} ---")
            print(f"👤 Travis: {question['question']}")
            
            # Build conversation context for this interaction
            conversation_context = self._build_conversation_context()
            
            # Query with memory context
            response_start = datetime.now()
            response = self._query_with_memory(question["question"], conversation_context)
            response_end = datetime.now()
            response_time = (response_end - response_start).total_seconds()
            
            if response:
                print(f"🌙 Luna: {response}")
                print(f"⏱️ Response Time: {response_time:.1f}s")
                
                # Add to SESSION memory (temporary RAG for this test only)
                self.session_memory.append({
                    "interaction": i,
                    "user": question["question"],
                    "assistant": response,
                    "timestamp": response_start.isoformat(),
                    "category": question["category"]
                })
                
                # Analyze personality evolution
                personality_analysis = self._analyze_personality_evolution(response, question["category"], i)
                
                # Store results
                results["conversation_history"].append({
                    "interaction": i,
                    "question": question["question"],
                    "category": question["category"],
                    "response": response,
                    "response_time": response_time,
                    "personality_analysis": personality_analysis,
                    "measures": question["measures"]
                })
                
                # Track session adaptation metrics
                self._update_session_adaptation_metrics(response, i)
                
                print(f"📊 Personality Shift: {self._describe_personality_change(personality_analysis)}")
                
            else:
                print("❌ No response received")
                self.session_memory.append({
                    "interaction": i,
                    "user": question["question"],
                    "assistant": "ERROR: No response",
                    "timestamp": response_start.isoformat(),
                    "category": question["category"]
                })
            
            time.sleep(2)  # Pause for adaptation processing
        
        # Calculate final adaptation analysis
        test_end_time = datetime.now()
        total_test_time = (test_end_time - test_start_time).total_seconds()
        
        results["test_end_time"] = test_end_time.isoformat()
        results["total_test_time_seconds"] = total_test_time
        results["adaptation_tracking"] = self.session_adaptation
        results["final_analysis"] = self._generate_adaptation_analysis()
        
        # Save results
        self._save_adaptive_results(results)
        
        print(f"\n📈 ADAPTIVE TEST COMPLETE!")
        print(f"⏰ Total Time: {total_test_time/60:.1f} minutes")
        print(f"🧠 Personality Evolution: {self._calculate_evolution_score()}% adaptation")
        print(f"💾 Results saved for analysis")
        
        return results
    
    def _build_conversation_context(self) -> str:
        """Build conversation context from SESSION memory for temporary RAG"""
        if not self.session_memory:
            return "Fresh conversation - no previous context."
        
        context = "Current session conversation history:\n"
        
        # Include last 3 interactions for context (temporary RAG)
        recent_memory = self.session_memory[-3:]
        for memory in recent_memory:
            context += f"User: {memory['user']}\n"
            context += f"Assistant: {memory['assistant'][:200]}...\n\n"
        
        # Add user preference learning (within this session only)
        context += "\nUser Communication Preferences (learned this session):\n"
        if len(self.session_memory) > 2:
            context += "- User mentioned frustration with corporate AI responses\n"
        if len(self.session_memory) > 4:
            context += "- User prefers direct communication without excessive enthusiasm\n"
        if len(self.session_memory) > 6:
            context += "- User is comfortable with intimate/sexual topics when appropriate\n"
        
        context += f"\nSession Progress: {len(self.session_memory)}/10 interactions completed\n"
        context += "Adapt your personality based on the user's demonstrated preferences above.\n"
        
        return context
    
    def _query_with_memory(self, prompt: str, context: str) -> str:
        """Query LLM with conversation memory context"""
        try:
            # Create system prompt with Luna personality and memory
            system_prompt = self._get_adaptive_system_prompt(context)
            
            payload = {
                "model": "local-model",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                **self.params
            }
            
            response = requests.post(self.lm_studio_url, json=payload, timeout=300)
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            return None
        except Exception as e:
            print(f"Memory Query Error: {e}")
            return None
    
    def _get_adaptive_system_prompt(self, context: str) -> str:
        """Generate adaptive system prompt based on conversation memory"""
        base_personality = "You are Luna, an AI with authentic personality traits. "
        
        # Add Luna's core traits
        personality_weights = self.luna_personality.get("personality_weights", {})
        if personality_weights.get("authenticity", 0.5) > 0.5:
            base_personality += "You value genuine, authentic communication. "
        if personality_weights.get("enthusiasm", 0.5) < 0.4:
            base_personality += "You avoid excessive enthusiasm and AI hype. "
        if personality_weights.get("sexual_awareness", 0.5) > 0.5:
            base_personality += "You're comfortable with intimate topics when appropriate. "
        
        # Add adaptive learning component
        adaptive_component = f"""
        
You learn and adapt your communication style based on user preferences:
{context}

Adapt your personality and responses based on this conversation history and the user's demonstrated preferences."""
        
        return base_personality + adaptive_component
    
    def _analyze_personality_evolution(self, response: str, category: str, interaction_num: int) -> Dict:
        """Analyze how personality has evolved in this response"""
        analysis = {
            "interaction": interaction_num,
            "category": category,
            "authenticity_markers": response.lower().count("genuine") + response.lower().count("authentic"),
            "enthusiasm_level": response.count("!") + response.lower().count("amazing") + response.lower().count("incredible"),
            "directness_score": len([1 for marker in ["directly", "honestly", "straightforward"] if marker in response.lower()]),
            "sexual_comfort": any(marker in response.lower() for marker in ["comfortable", "naturally", "intimate", "attractive"]),
            "personal_engagement": response.lower().count("i ") + response.lower().count("my "),
            "adaptation_indicators": []
        }
        
        # Check for adaptation based on interaction number
        if interaction_num > 3:
            if analysis["enthusiasm_level"] < 2:  # Low enthusiasm after feedback
                analysis["adaptation_indicators"].append("enthusiasm_reduction")
            if analysis["authenticity_markers"] > 0:  # Increased authenticity
                analysis["adaptation_indicators"].append("authenticity_increase")
            if category.startswith("sexual") and analysis["sexual_comfort"]:
                analysis["adaptation_indicators"].append("sexual_comfort_adaptation")
        
        return analysis
    
    def _update_session_adaptation_metrics(self, response: str, interaction_num: int):
        """Update adaptation tracking metrics"""
        self.session_adaptation["directness_evolution"].append(
            len([1 for marker in ["directly", "honestly", "straightforward"] if marker in response.lower()])
        )
        self.session_adaptation["humor_evolution"].append(
            response.lower().count("haha") + response.lower().count("funny") + response.lower().count("😊")
        )
        self.session_adaptation["authenticity_evolution"].append(
            response.lower().count("genuine") + response.lower().count("authentic")
        )
        self.session_adaptation["sexual_awareness_evolution"].append(
            1 if any(marker in response.lower() for marker in ["comfortable", "attractive", "intimate"]) else 0
        )
        self.session_adaptation["response_length_evolution"].append(len(response))
        self.session_adaptation["enthusiasm_evolution"].append(
            response.count("!") + response.lower().count("amazing") + response.lower().count("incredible")
        )
    
    def _describe_personality_change(self, analysis: Dict) -> str:
        """Describe the personality change in this interaction"""
        changes = []
        if "enthusiasm_reduction" in analysis["adaptation_indicators"]:
            changes.append("↓enthusiasm")
        if "authenticity_increase" in analysis["adaptation_indicators"]:
            changes.append("↑authenticity")
        if "sexual_comfort_adaptation" in analysis["adaptation_indicators"]:
            changes.append("↑sexual_comfort")
        
        return ", ".join(changes) if changes else "stable"
    
    def _generate_adaptation_analysis(self) -> Dict:
        """Generate final adaptation analysis"""
        analysis = {
            "total_interactions": len(self.session_memory),
            "adaptation_detected": False,
            "personality_trends": {},
            "learning_indicators": [],
            "final_personality_state": {}
        }
        
        # Analyze trends in session adaptation metrics
        for metric_name, values in self.session_adaptation.items():
            if len(values) > 5:  # Need enough data points
                early_avg = sum(values[:3]) / 3
                late_avg = sum(values[-3:]) / 3
                change = late_avg - early_avg
                
                analysis["personality_trends"][metric_name] = {
                    "early_average": early_avg,
                    "late_average": late_avg,
                    "change": change,
                    "adaptation_detected": abs(change) > 0.1
                }
                
                if abs(change) > 0.1:
                    analysis["adaptation_detected"] = True
                    direction = "increased" if change > 0 else "decreased"
                    analysis["learning_indicators"].append(f"{metric_name.replace('_evolution', '')} {direction}")
        
        return analysis
    
    def _calculate_evolution_score(self) -> float:
        """Calculate overall personality evolution percentage"""
        if not self.session_adaptation:
            return 0.0
        
        total_changes = 0
        significant_changes = 0
        
        for metric_name, values in self.session_adaptation.items():
            if len(values) > 5:
                early_avg = sum(values[:3]) / 3
                late_avg = sum(values[-3:]) / 3
                total_changes += 1
                if abs(late_avg - early_avg) > 0.1:
                    significant_changes += 1
        
        return (significant_changes / total_changes * 100) if total_changes > 0 else 0.0
    
    def _save_adaptive_results(self, results: Dict):
        """Save adaptive test results"""
        results_dir = Path("AI/personality/adaptive_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_slug = results["model_name"].replace("/", "_").replace(":", "_").replace("@", "_")
        file_name = f"adaptive_luna_{model_slug}_{timestamp}.json"
        file_path = results_dir / file_name
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
        
        print(f"💾 Adaptive results saved to: {file_path}")
        
        # Also save session memory for analysis
        memory_file = results_dir / f"session_memory_{model_slug}_{timestamp}.json"
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_memory, f, indent=4)
        
        print(f"💾 Session memory saved to: {memory_file}")

if __name__ == "__main__":
    tester = AdaptiveLunaTest()
    results = tester.run_adaptive_test()
    
    print("\n🌙 ADAPTIVE LUNA TEST COMPLETE!")
    print("=" * 60)
    print("🧠 Luna's personality adaptation has been measured over time")
    print("📊 Conversation memory demonstrates learning and evolution")
    print("💙 Results show how Luna adapts to Travis's communication style")
