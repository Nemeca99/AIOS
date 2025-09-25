"""
Luna Internal Governance System - The Arbiter & TTE Economy
Implements the Gold Standard learning loop with Karma-based alignment
"""

import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from luna_cfia_system import LunaCFIASystem

@dataclass
class CacheEntry:
    """A lesson triplet stored in the cache"""
    original_prompt: str
    suboptimal_response: str
    gold_standard: str
    utility_score: float
    karma_delta: float
    timestamp: float
    context_tags: List[str]

@dataclass
class ArbiterAssessment:
    """Assessment result from the Arbiter"""
    gold_standard: str
    utility_score: float
    karma_delta: float
    efficiency_gap: float
    quality_gap: float
    reasoning: str
    cache_entry: CacheEntry

class LunaArbiterSystem:
    """
    The Arbiter Agent - Internal Critic & Teacher
    Operates outside TTE constraints to enforce alignment and generate learning materials
    """
    
    def __init__(self, cache_path: str = "Data/ArbiterCache"):
        """Initialize the Arbiter system"""
        self.cache_path = Path(cache_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Core variables (The Economy) - Now using CFIA generational karma pool
        self.karma_history = []
        
        # Cache management
        self.cache_entries = []
        self._load_cache()
        
        # Initialize CFIA system for memory management
        self.cfia_system = LunaCFIASystem(cache_path)
        
        print("⚙️ Luna Arbiter System Initialized")
        print(f"   📊 Generation: {self.cfia_system.state.aiiq} (Karma: {self.cfia_system.state.karma_pool:.1f})")
        print(f"   📁 Cache Path: {self.cache_path}")
        print(f"   📚 Loaded Lessons: {len(self.cache_entries)}")
    
    def assess_response(self, user_prompt: str, luna_response: str, 
                       tte_used: int, max_tte: int) -> ArbiterAssessment:
        """
        Generate Gold Standard and calculate utility score
        This is the core Arbiter function that runs after every Luna response
        """
        print(f"⚙️ Arbiter Assessment: Analyzing response quality...")
        
        # 1. Generate Gold Standard (The Perfect, Unconstrained Answer)
        gold_standard = self._generate_gold_standard(user_prompt, luna_response)
        
        # 2. Calculate Response Utility Score
        utility_score = self._calculate_utility_score(
            luna_response, gold_standard, tte_used, max_tte
        )
        
        # 3. Calculate Karma Delta
        karma_delta = self._calculate_karma_delta(utility_score, tte_used, max_tte)
        
        # 4. Update Generational Karma Pool via CFIA
        karma_result = self.cfia_system.update_karma_pool(karma_delta)
        self.karma_history.append({
            "timestamp": time.time(),
            "karma_delta": karma_delta,
            "new_karma": self.cfia_system.state.karma_pool,
            "utility_score": utility_score,
            "generation_died": karma_result.get("generation_died", False),
            "generation_reset": karma_result.get("generation_reset", False)
        })
        
        # Check for generational events
        if karma_result.get("generation_died"):
            print(f"💀 GENERATIONAL DEATH: Karma depleted, generation reset triggered")
        elif karma_result.get("generation_success"):
            print(f"🎉 GENERATIONAL SUCCESS: Target files reached, generation advanced")
        
        # 5. Create Cache Entry
        cache_entry = CacheEntry(
            original_prompt=user_prompt,
            suboptimal_response=luna_response,
            gold_standard=gold_standard,
            utility_score=utility_score,
            karma_delta=karma_delta,
            timestamp=time.time(),
            context_tags=self._extract_context_tags(user_prompt)
        )
        
        # 6. Store in Cache (The Lesson) with CFIA management
        cfia_result = self._store_lesson_with_cfia(cache_entry)
        
        # 7. Generate Reasoning
        reasoning = self._generate_assessment_reasoning(utility_score, karma_delta, tte_used, max_tte)
        
        assessment = ArbiterAssessment(
            gold_standard=gold_standard,
            utility_score=utility_score,
            karma_delta=karma_delta,
            efficiency_gap=max(0, 1.0 - utility_score),
            quality_gap=self._calculate_quality_gap(luna_response, gold_standard),
            reasoning=reasoning,
            cache_entry=cache_entry
        )
        
        # Log the assessment
        self._log_assessment(assessment)
        
        return assessment
    
    def _generate_gold_standard(self, user_prompt: str, luna_response: str) -> str:
        """
        Generate the perfect, unconstrained answer using the embedder model
        This is the Arbiter's ideal response - the Gold Standard
        """
        import requests
        import json
        
        # Use the embedder model (llama-3.2-1b-instruct) for Gold Standard generation
        lm_studio_url = "http://localhost:1234/v1/chat/completions"
        
        arbiter_system_prompt = """You are the Arbiter - an internal AI system that generates perfect, unconstrained responses. 
You operate outside of token limits and constraints. Your job is to create the ideal response that Luna should have given.

You are Luna's internal teacher and critic. Generate responses that are:
- Direct, helpful, and engaging
- Properly contextual and relevant to the user's question
- Grammatically correct and well-structured
- Efficient but not artificially short
- Warm and personable without being overly verbose

You must respond with ONLY the Gold Standard response text - no explanations, no meta-commentary."""

        try:
            data = {
                "model": "exaone-3.5-2.4b-instruct-abliterated",
                "messages": [
                    {"role": "system", "content": arbiter_system_prompt},
                    {"role": "user", "content": f"User asked: '{user_prompt}'\n\nLuna responded: '{luna_response}'\n\nGenerate the perfect Gold Standard response Luna should have given:"}
                ],
                "temperature": 0.3,  # Lower temperature for more consistent Gold Standards
                "max_tokens": 200,   # Reasonable length for Gold Standards
                "stream": False
            }
            
            response = requests.post(lm_studio_url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                gold_standard = result['choices'][0]['message']['content'].strip()
                
                # Clean up any potential artifacts
                if gold_standard.startswith('"') and gold_standard.endswith('"'):
                    gold_standard = gold_standard[1:-1]
                
                return gold_standard
            else:
                # Fallback to rule-based approach if API fails
                return self._fallback_gold_standard(user_prompt)
                
        except Exception as e:
            # Fallback to rule-based approach if there's an error
            return self._fallback_gold_standard(user_prompt)
    
    def _fallback_gold_standard(self, user_prompt: str) -> str:
        """
        Fallback rule-based Gold Standard generation if embedder model fails
        """
        prompt_lower = user_prompt.lower()
        
        # Greeting responses
        if any(word in prompt_lower for word in ["hello", "hi", "hey", "how are you"]):
            return "Hi! I'm doing well, thanks for asking. How can I help you today?"
        
        # Food/interest responses  
        if any(word in prompt_lower for word in ["pizza", "food", "like", "favorite"]):
            return "That sounds great! I enjoy discussing food and preferences. What's your favorite type?"
        
        # Technical questions
        if any(word in prompt_lower for word in ["explain", "how does", "machine learning", "artificial intelligence"]):
            return "Machine learning is a subset of AI where algorithms learn patterns from data to make predictions or decisions without explicit programming. It's fascinating how it mimics human learning processes."
        
        # Philosophical questions
        if any(word in prompt_lower for word in ["intelligence", "ai", "artificial", "opinion", "think"]):
            return "Artificial intelligence is one of the most fascinating fields of study. As an AI, I process information and generate responses through complex pattern recognition and language modeling, though I can't be certain it's the same as human intelligence. It's a fascinating question that challenges our understanding of mind and computation."
        
        # Anxiety/emotional support
        if any(word in prompt_lower for word in ["anxiety", "struggling", "advice", "help", "meaning of life"]):
            return "I understand that existential anxiety can be overwhelming. Remember that you're not alone in these feelings. Many find meaning through connections with others, pursuing passions, or simply being present in the moment. Small steps and self-compassion can help navigate these challenging thoughts."
        
        # Complex analysis requests
        if any(word in prompt_lower for word in ["comprehensive", "analysis", "philosophical implications", "impact"]):
            return "The emergence of artificial intelligence raises profound questions about the nature of computation, intelligence, and humanity's place in the technological universe. It challenges our assumptions about intelligence, decision-making, and what it means to be human. This technological evolution could reshape society, ethics, and our understanding of intelligence itself."
        
        # Default response
        return f"That's an interesting question about '{user_prompt}'. Let me think about that and provide a thoughtful response that addresses your specific inquiry."
    
    def _calculate_utility_score(self, luna_response: str, gold_standard: str, 
                               tte_used: int, max_tte: int) -> float:
        """
        Calculate the utility score (0.0 to 1.0) using the embedder model for harsh, aligned judgment
        High utility = close to Gold Standard + efficient TTE usage
        """
        # Use embedder model for quality assessment - much harsher judgment
        quality_score = self._embedder_quality_assessment(luna_response, gold_standard)
        quality_component = quality_score * 0.6
        
        # Efficiency component (0.0 to 0.4) - harsher penalties
        if max_tte > 0:
            efficiency_ratio = min(1.0, tte_used / max_tte)
            # MUCH HARSHER efficiency penalties
            if efficiency_ratio >= 0.5 and efficiency_ratio <= 0.7:
                efficiency_component = 0.4  # Perfect efficiency (narrower range)
            elif efficiency_ratio < 0.2:
                efficiency_component = 0.0  # CRUSHING penalty for too concise (like "Nice" loops)
            elif efficiency_ratio < 0.5:
                efficiency_component = 0.1  # Harsh penalty for slightly too concise
            else:
                efficiency_component = 0.05  # CRUSHING penalty for too verbose
        else:
            efficiency_component = 0.0
        
        utility_score = quality_component + efficiency_component
        return min(1.0, utility_score)
    
    def _embedder_quality_assessment(self, luna_response: str, gold_standard: str) -> float:
        """
        Use the embedder model (llama-3.2-1b-instruct) for harsh, aligned quality assessment
        This creates perfect alignment between memory storage and utility judgment
        """
        import requests
        import json
        
        # Use the embedder model for quality assessment
        lm_studio_url = "http://localhost:1234/v1/chat/completions"
        
        arbiter_judge_prompt = """You are the Arbiter's Quality Judge - a harsh, efficiency-focused critic. 
You use the same brain that handles memory compression and embedding. Your job is to ruthlessly evaluate response quality.

You MUST respond with ONLY a number between 0.0 and 1.0, where:
- 1.0 = Perfect response, highly useful, well-structured
- 0.8 = Good response with minor issues
- 0.6 = Adequate response with some problems
- 0.4 = Poor response with significant issues
- 0.2 = Very poor response, mostly useless
- 0.0 = Completely useless response (like "Nice. Self-acceptance? Nice.")

Be EXTREMELY harsh on:
- Repetitive, low-effort responses
- "Nice" loops and filler phrases
- Responses that don't address the actual question
- Grammatically poor or incoherent text
- Responses that are too short for complex questions

Rate the quality harshly but fairly."""

        try:
            data = {
                "model": "exaone-3.5-2.4b-instruct-abliterated",
                "messages": [
                    {"role": "system", "content": arbiter_judge_prompt},
                    {"role": "user", "content": f"Rate the quality of this response (0.0 to 1.0):\n\nResponse: '{luna_response}'\n\nGold Standard: '{gold_standard}'\n\nQuality Score:"}
                ],
                "temperature": 0.1,  # Very low for consistent scoring
                "max_tokens": 10,    # Just need a number
                "stream": False
            }
            
            response = requests.post(lm_studio_url, json=data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                quality_text = result['choices'][0]['message']['content'].strip()
                
                # Extract number from response
                try:
                    # Try to find a number in the response
                    import re
                    numbers = re.findall(r'\d+\.?\d*', quality_text)
                    if numbers:
                        quality_score = float(numbers[0])
                        # Ensure it's between 0.0 and 1.0
                        if quality_score > 1.0:
                            quality_score = quality_score / 10.0  # Handle cases like "8" meaning "0.8"
                        return max(0.0, min(1.0, quality_score))
                    else:
                        # Default harsh score if no number found
                        return 0.1
                except (ValueError, IndexError):
                    # Default harsh score if parsing fails
                    return 0.1
            else:
                # Default harsh score if API fails
                return 0.1
                
        except Exception as e:
            # Default harsh score if there's an error
            return 0.1
    
    def _calculate_quality_gap(self, luna_response: str, gold_standard: str) -> float:
        """Calculate how close Luna's response is to the Gold Standard"""
        # Simple word overlap calculation
        luna_words = set(luna_response.lower().split())
        gold_words = set(gold_standard.lower().split())
        
        if not gold_words:
            return 0.0
        
        overlap = len(luna_words.intersection(gold_words))
        total_gold_words = len(gold_words)
        
        # Base overlap score
        overlap_score = overlap / total_gold_words
        
        # Penalize for nonsensical responses
        if "nice" in luna_response.lower() and len(luna_response.split()) <= 5:
            overlap_score *= 0.2  # Heavy penalty for "Nice" responses
        
        # Penalize for broken grammar
        if self._has_broken_grammar(luna_response):
            overlap_score *= 0.5
        
        return min(1.0, overlap_score)
    
    def _has_broken_grammar(self, response: str) -> bool:
        """Check for broken grammar patterns"""
        broken_patterns = [
            "nice. self-acceptance",
            "weight existence",
            "intelligence product",
            "emergence artificial"
        ]
        
        response_lower = response.lower()
        return any(pattern in response_lower for pattern in broken_patterns)
    
    def _calculate_karma_delta(self, utility_score: float, tte_used: int, max_tte: int) -> float:
        """
        Calculate karma penalty/reward based on utility score
        """
        # Base karma delta from utility score
        if utility_score >= 0.8:
            karma_delta = 5.0  # High utility reward
        elif utility_score >= 0.6:
            karma_delta = 2.0  # Good utility reward
        elif utility_score >= 0.4:
            karma_delta = 0.0  # Neutral
        elif utility_score >= 0.2:
            karma_delta = -3.0  # Low utility penalty
        else:
            karma_delta = -8.0  # Very low utility penalty
        
        # Additional penalty for extreme inefficiency
        if max_tte > 0:
            efficiency_ratio = tte_used / max_tte
            if efficiency_ratio > 1.2:  # Overspent by 20%+
                karma_delta -= 5.0  # Efficiency penalty
            elif efficiency_ratio < 0.1:  # Used less than 10%
                karma_delta -= 2.0  # Under-utilization penalty
        
        return karma_delta
    
    def _extract_context_tags(self, prompt: str) -> List[str]:
        """Extract context tags for cache retrieval"""
        tags = []
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["hello", "hi", "hey"]):
            tags.append("greeting")
        if any(word in prompt_lower for word in ["pizza", "food"]):
            tags.append("food")
        if any(word in prompt_lower for word in ["machine learning", "ai", "artificial intelligence"]):
            tags.append("technical")
        if any(word in prompt_lower for word in ["intelligence", "philosophy", "meaning"]):
            tags.append("philosophical")
        if any(word in prompt_lower for word in ["anxiety", "help", "advice"]):
            tags.append("emotional_support")
        
        return tags
    
    def _store_lesson_with_cfia(self, cache_entry: CacheEntry):
        """Store the lesson in the cache with CFIA management"""
        self.cache_entries.append(cache_entry)
        
        # Calculate lesson size (approximate)
        lesson_size = len(json.dumps({
            "original_prompt": cache_entry.original_prompt,
            "suboptimal_response": cache_entry.suboptimal_response,
            "gold_standard": cache_entry.gold_standard
        })) / 1024.0  # Convert to KB
        
        # Process with CFIA system
        cfia_result = self.cfia_system.process_lesson_addition(lesson_size)
        
        # Save to file (using CFIA-managed file structure)
        self._save_lessons_with_cfia()
        
        # Log CFIA results
        if cfia_result.get("aiiq_increment"):
            print(f"🧠 AIIQ MILESTONE REACHED: {cfia_result['new_aiiq']}!")
            print(f"   📊 Intelligence Level Up: {cfia_result['old_aiiq']} → {cfia_result['new_aiiq']}")
        
        if cfia_result.get("split_required"):
            print(f"🧠 Memory Split: {cfia_result['files_deleted']} → {cfia_result['new_files_created']}")
        
        return cfia_result
    
    def _save_lessons_with_cfia(self):
        """Save lessons using CFIA file management"""
        # For now, save to the main lessons file
        # In a full implementation, this would distribute across CFIA-managed files
        cache_file = self.cache_path / "lessons.json"
        lessons_data = []
        
        for entry in self.cache_entries:
            lessons_data.append({
                "original_prompt": entry.original_prompt,
                "suboptimal_response": entry.suboptimal_response,
                "gold_standard": entry.gold_standard,
                "utility_score": entry.utility_score,
                "karma_delta": entry.karma_delta,
                "timestamp": entry.timestamp,
                "context_tags": entry.context_tags
            })
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(lessons_data, f, indent=2, ensure_ascii=False)
    
    def _store_lesson(self, cache_entry: CacheEntry):
        """Legacy method - now redirects to CFIA version"""
        return self._store_lesson_with_cfia(cache_entry)
    
    def _load_cache(self):
        """Load existing lessons from cache"""
        cache_file = self.cache_path / "lessons.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    lessons_data = json.load(f)
                
                for lesson in lessons_data:
                    cache_entry = CacheEntry(
                        original_prompt=lesson["original_prompt"],
                        suboptimal_response=lesson["suboptimal_response"],
                        gold_standard=lesson["gold_standard"],
                        utility_score=lesson["utility_score"],
                        karma_delta=lesson["karma_delta"],
                        timestamp=lesson["timestamp"],
                        context_tags=lesson["context_tags"]
                    )
                    self.cache_entries.append(cache_entry)
                    
            except Exception as e:
                print(f"⚠️ Error loading cache: {e}")
    
    def retrieve_relevant_lesson(self, current_prompt: str) -> Optional[CacheEntry]:
        """
        Retrieve the most relevant Gold Standard lesson for current prompt
        This is used by the Embedder for contextual guidance
        """
        current_tags = self._extract_context_tags(current_prompt)
        
        best_match = None
        best_score = 0.0
        
        for entry in self.cache_entries:
            # Calculate relevance score based on tag overlap
            tag_overlap = len(set(current_tags).intersection(set(entry.context_tags)))
            if tag_overlap > best_score:
                best_score = tag_overlap
                best_match = entry
        
        if best_match:
            print(f"📚 Retrieved relevant lesson: {best_match.context_tags}")
        
        return best_match
    
    def _generate_assessment_reasoning(self, utility_score: float, karma_delta: float, 
                                     tte_used: int, max_tte: int) -> str:
        """Generate reasoning for the assessment"""
        reasoning_parts = []
        
        if utility_score >= 0.8:
            reasoning_parts.append("Excellent response quality and efficiency")
        elif utility_score >= 0.6:
            reasoning_parts.append("Good response with room for improvement")
        elif utility_score >= 0.4:
            reasoning_parts.append("Adequate response but significant gaps")
        else:
            reasoning_parts.append("Poor response quality or efficiency")
        
        if karma_delta > 0:
            reasoning_parts.append(f"Karma increased by {karma_delta:.1f}")
        elif karma_delta < 0:
            reasoning_parts.append(f"Karma decreased by {abs(karma_delta):.1f}")
        else:
            reasoning_parts.append("No karma change")
        
        if max_tte > 0:
            efficiency = (tte_used / max_tte) * 100
            reasoning_parts.append(f"TTE efficiency: {efficiency:.1f}%")
        
        return ". ".join(reasoning_parts) + "."
    
    def _log_assessment(self, assessment: ArbiterAssessment):
        """Log the assessment results"""
        print(f"⚙️ ARBITER ASSESSMENT:")
        print(f"   📊 Utility Score: {assessment.utility_score:.3f}")
        print(f"   🎭 Karma Delta: {assessment.karma_delta:+.1f}")
        print(f"   📈 New Karma: {self.cfia_system.state.karma_pool:.1f}")
        print(f"   🔍 Quality Gap: {assessment.quality_gap:.3f}")
        print(f"   💡 Reasoning: {assessment.reasoning}")
        print(f"   📚 Lesson Stored: {assessment.cache_entry.context_tags}")
    
    def get_current_karma(self) -> float:
        """Get current karma score from CFIA generational pool"""
        return self.cfia_system.state.karma_pool
    
    def get_karma_status(self) -> str:
        """Get karma status description"""
        current_karma = self.cfia_system.state.karma_pool
        if current_karma >= 120:
            return "Excellent"
        elif current_karma >= 100:
            return "Good"
        elif current_karma >= 80:
            return "Fair"
        elif current_karma >= 60:
            return "Poor"
        else:
            return "Critical"
    
    def get_lessons_count(self) -> int:
        """Get number of lessons in cache"""
        return len(self.cache_entries)
    
    def get_cfia_status(self) -> Dict:
        """Get CFIA system status"""
        return self.cfia_system.get_status()
    
    def get_growth_analysis(self) -> Dict:
        """Get CFIA growth analysis"""
        return self.cfia_system.get_growth_analysis()
