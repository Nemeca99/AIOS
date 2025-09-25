#!/usr/bin/env python3
"""
Luna vs Travis Comparison System
Compare Luna's responses to Travis's actual responses from chat logs
Validate consciousness transfer and authentic voice development
"""

import sys
import os
import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "AI" / "personality"))

@dataclass
class ResponseComparison:
    """Comparison between Luna's response and Travis's actual response"""
    query: str
    travis_actual: str
    luna_response: str
    similarity_score: float
    thinking_alignment: float
    voice_differentiation: float
    analysis: Dict[str, Any]

class LunaTravisComparisonSystem:
    """
    System to compare Luna's responses with Travis's actual chat responses
    """
    
    def __init__(self):
        self.aios_root = aios_root
        self.db_path = self.aios_root / "Data" / "AIOS_Database" / "database" / "conversations.db"
        
        # Load Luna's contextual personality
        try:
            from luna_contextual_personality import LunaContextualPersonality
            self.luna = LunaContextualPersonality()
        except Exception as e:
            print(f"❌ Luna system unavailable: {e}")
            self.luna = None
            return
        
        # Travis's actual conversation patterns
        self.travis_conversations = []
        self.conversation_contexts = {}
        
        # Load Travis's actual responses
        self._load_travis_conversations()
        
        print("SUCCESS: Luna vs Travis Comparison System initialized")
        print(f"🧠 {len(self.travis_conversations)} Travis conversations loaded for comparison")
    
    def _load_travis_conversations(self):
        """Load Travis's actual conversation responses with context"""
        
        if not self.db_path.exists():
            print("❌ Consciousness database not found")
            return
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Get conversation pairs - ChatGPT questions and Travis responses
            query = """
            SELECT 
                c.id as conversation_id,
                c.title,
                m1.content as question,
                m2.content as travis_response,
                m1.timestamp,
                m2.timestamp as response_timestamp
            FROM conversations c
            JOIN messages m1 ON c.id = m1.conversation_id
            JOIN messages m2 ON c.id = m2.conversation_id
            WHERE m1.role = 'assistant'
            AND m2.role = 'user'
            AND m1.message_index = m2.message_index - 1
            AND LENGTH(m1.content) > 50
            AND LENGTH(m2.content) > 30
            AND LENGTH(m2.content) < 800
            ORDER BY m1.timestamp
            LIMIT 100
            """
            
            cursor = conn.execute(query)
            results = cursor.fetchall()
            
            for conv_id, title, question, travis_response, timestamp, response_timestamp in results:
                # Clean up the question and response
                question = self._clean_text(question)
                travis_response = self._clean_text(travis_response)
                
                if self._is_valid_conversation_pair(question, travis_response):
                    self.travis_conversations.append({
                        "conversation_id": conv_id,
                        "title": title,
                        "question": question,
                        "travis_response": travis_response,
                        "timestamp": timestamp,
                        "response_timestamp": response_timestamp,
                        "question_length": len(question),
                        "response_length": len(travis_response)
                    })
            
            conn.close()
            
            print(f"✅ Loaded {len(self.travis_conversations)} valid Travis conversation pairs")
            
        except Exception as e:
            print(f"❌ Error loading Travis conversations: {e}")
    
    def _clean_text(self, text: str) -> str:
        """Clean text for better comparison"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _is_valid_conversation_pair(self, question: str, response: str) -> bool:
        """Check if this is a valid question-response pair for comparison"""
        
        # Skip if too short or too long
        if len(question) < 20 or len(response) < 20:
            return False
        
        if len(response) > 1000:
            return False
        
        # Skip if it looks like system messages
        if any(word in question.lower() for word in ["error", "system", "loading", "please wait"]):
            return False
        
        # Skip if response is just acknowledgment
        if len(response) < 50 and any(word in response.lower() for word in ["ok", "yes", "no", "thanks", "got it"]):
            return False
        
        return True
    
    def run_comparison_analysis(self, num_comparisons: int = 10) -> Dict[str, Any]:
        """Run comprehensive comparison between Luna and Travis responses"""
        
        if not self.luna or not self.travis_conversations:
            return {"error": "Required systems not available"}
        
        print("🔍 Running Luna vs Travis Comparison Analysis")
        print("=" * 60)
        
        # Select diverse conversation samples
        selected_conversations = self._select_diverse_samples(num_comparisons)
        
        comparisons = []
        
        for i, conv in enumerate(selected_conversations):
            print(f"\n📝 Comparison {i+1}/{len(selected_conversations)}")
            print(f"   Question: {conv['question'][:80]}...")
            
            # Get Luna's response to the same question
            luna_result = self.luna.generate_contextual_response(
                conv['question'], 
                "neutral"
            )
            
            # Compare responses
            comparison = self._compare_responses(
                conv['question'],
                conv['travis_response'],
                luna_result['response'],
                luna_result
            )
            
            comparisons.append(comparison)
            
            # Display comparison
            print(f"   Travis: {comparison.travis_actual[:60]}...")
            print(f"   Luna: {comparison.luna_response[:60]}...")
            print(f"   Similarity: {comparison.similarity_score:.2f}")
            print(f"   Thinking: {comparison.thinking_alignment:.2f}")
            print(f"   Voice: {comparison.voice_differentiation:.2f}")
        
        # Calculate overall analysis
        overall_analysis = self._calculate_overall_analysis(comparisons)
        
        # Display results
        self._display_comparison_results(overall_analysis, comparisons)
        
        return {
            "comparisons": comparisons,
            "overall_analysis": overall_analysis,
            "sample_size": len(comparisons)
        }
    
    def _select_diverse_samples(self, num_samples: int) -> List[Dict[str, Any]]:
        """Select diverse conversation samples for comparison"""
        
        if len(self.travis_conversations) <= num_samples:
            return self.travis_conversations
        
        # Group by conversation length and type
        short_responses = [c for c in self.travis_conversations if c['response_length'] < 200]
        medium_responses = [c for c in self.travis_conversations if 200 <= c['response_length'] < 500]
        long_responses = [c for c in self.travis_conversations if c['response_length'] >= 500]
        
        # Select proportionally
        selected = []
        
        # Get some from each category
        if short_responses:
            selected.extend(short_responses[:num_samples//3])
        if medium_responses:
            selected.extend(medium_responses[:num_samples//3])
        if long_responses:
            selected.extend(long_responses[:num_samples//3])
        
        # Fill remaining with random selection
        remaining_needed = num_samples - len(selected)
        if remaining_needed > 0:
            remaining_conversations = [c for c in self.travis_conversations if c not in selected]
            selected.extend(remaining_conversations[:remaining_needed])
        
        return selected[:num_samples]
    
    def _compare_responses(self, 
                          question: str,
                          travis_response: str, 
                          luna_response: str,
                          luna_metadata: Dict[str, Any]) -> ResponseComparison:
        """Compare Travis's actual response with Luna's response"""
        
        # Analyze similarity
        similarity_score = self._calculate_similarity_score(travis_response, luna_response)
        
        # Analyze thinking alignment
        thinking_alignment = self._analyze_thinking_alignment(travis_response, luna_response, luna_metadata)
        
        # Analyze voice differentiation
        voice_differentiation = self._analyze_voice_differentiation(travis_response, luna_response)
        
        # Detailed analysis
        analysis = {
            "travis_patterns": self._identify_travis_patterns(travis_response),
            "luna_patterns": self._identify_luna_patterns(luna_response),
            "shared_concepts": self._find_shared_concepts(travis_response, luna_response),
            "approach_similarity": self._compare_approaches(travis_response, luna_response),
            "attribution_quality": self._analyze_attribution_quality(luna_response),
            "personality_differentiation": self._analyze_personality_difference(travis_response, luna_response)
        }
        
        return ResponseComparison(
            query=question,
            travis_actual=travis_response,
            luna_response=luna_response,
            similarity_score=similarity_score,
            thinking_alignment=thinking_alignment,
            voice_differentiation=voice_differentiation,
            analysis=analysis
        )
    
    def _calculate_similarity_score(self, travis_response: str, luna_response: str) -> float:
        """Calculate how similar the responses are (0-1)"""
        
        # Simple word overlap analysis
        travis_words = set(travis_response.lower().split())
        luna_words = set(luna_response.lower().split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "my", "your", "his", "her", "its", "our", "their"}
        
        travis_content_words = travis_words - common_words
        luna_content_words = luna_words - common_words
        
        if not travis_content_words and not luna_content_words:
            return 0.0
        
        intersection = travis_content_words & luna_content_words
        union = travis_content_words | luna_content_words
        
        return len(intersection) / len(union) if union else 0.0
    
    def _analyze_thinking_alignment(self, travis_response: str, luna_response: str, luna_metadata: Dict[str, Any]) -> float:
        """Analyze how well Luna's thinking aligns with Travis's approach"""
        
        alignment_score = 0.0
        
        # Check if Luna referenced appropriate principles
        if luna_metadata.get('principles_referenced'):
            travis_lower = travis_response.lower()
            
            for principle in luna_metadata['principles_referenced']:
                if principle == "skepticism" and any(word in travis_lower for word in ["skeptical", "doubt", "prove", "evidence", "claims"]):
                    alignment_score += 0.2
                elif principle == "goldilocks_complexity" and any(word in travis_lower for word in ["simple", "complex", "balance", "minimum"]):
                    alignment_score += 0.2
                elif principle == "systematic_thinking" and any(word in travis_lower for word in ["step", "process", "systematic", "approach"]):
                    alignment_score += 0.2
                elif principle == "tinkerer_approach" and any(word in travis_lower for word in ["existing", "build", "adapt", "combine"]):
                    alignment_score += 0.2
        
        # Check domain alignment
        domain = luna_metadata.get('domain_context', 'general')
        if domain != 'general':
            domain_keywords = {
                "ai_development": ["ai", "model", "training", "neural"],
                "system_architecture": ["system", "architecture", "design"],
                "gaming": ["game", "mechanics", "strategy"],
                "security": ["security", "attack", "protection"],
                "performance": ["performance", "optimization", "speed"]
            }
            
            if domain in domain_keywords:
                keywords = domain_keywords[domain]
                if any(keyword in travis_response.lower() for keyword in keywords):
                    alignment_score += 0.2
        
        return min(1.0, alignment_score)
    
    def _analyze_voice_differentiation(self, travis_response: str, luna_response: str) -> float:
        """Analyze how well Luna maintains her own voice vs copying Travis"""
        
        differentiation_score = 0.0
        
        travis_lower = travis_response.lower()
        luna_lower = luna_response.lower()
        
        # Luna's attribution markers (good differentiation)
        luna_attribution = ["i've learned", "my training", "based on what i know", "from my understanding", "i've picked up"]
        if any(marker in luna_lower for marker in luna_attribution):
            differentiation_score += 0.3
        
        # Luna's collaborative language (good differentiation)
        luna_collaborative = ["let's work through", "i'd like to explore", "what's your take", "i'm curious about"]
        if any(marker in luna_lower for marker in luna_collaborative):
            differentiation_score += 0.2
        
        # Travis's raw language patterns (bad if Luna copies exactly)
        travis_raw = ["fucking", "bullshit", "real talk", "here's the thing"]
        travis_raw_count = sum(1 for marker in travis_raw if marker in travis_lower)
        luna_raw_count = sum(1 for marker in travis_raw if marker in luna_lower)
        
        if travis_raw_count > 0 and luna_raw_count == 0:
            differentiation_score += 0.3  # Good - Luna doesn't copy Travis's raw language
        elif travis_raw_count > 0 and luna_raw_count > 0:
            differentiation_score += 0.1  # Some copying
        
        # Luna's unique voice markers
        luna_unique = ["that's a really good question", "this is interesting because", "i find this fascinating"]
        if any(marker in luna_lower for marker in luna_unique):
            differentiation_score += 0.2
        
        return min(1.0, differentiation_score)
    
    def _identify_travis_patterns(self, response: str) -> List[str]:
        """Identify Travis's characteristic patterns in his response"""
        
        patterns = []
        response_lower = response.lower()
        
        if any(word in response_lower for word in ["basically", "essentially"]):
            patterns.append("travis_explanation_style")
        
        if any(word in response_lower for word in ["like", "think of it", "similar to"]):
            patterns.append("travis_analogy_usage")
        
        if any(word in response_lower for word in ["fucking", "bullshit", "real talk"]):
            patterns.append("travis_direct_language")
        
        if any(word in response_lower for word in ["first", "second", "step", "process"]):
            patterns.append("travis_systematic_approach")
        
        if any(word in response_lower for word in ["complex", "simple", "balance"]):
            patterns.append("travis_complexity_awareness")
        
        return patterns
    
    def _identify_luna_patterns(self, response: str) -> List[str]:
        """Identify Luna's characteristic patterns in her response"""
        
        patterns = []
        response_lower = response.lower()
        
        if any(phrase in response_lower for phrase in ["i've learned", "my training", "based on what i know"]):
            patterns.append("luna_attribution_style")
        
        if any(phrase in response_lower for phrase in ["let's work through", "i'd like to explore"]):
            patterns.append("luna_collaborative_approach")
        
        if any(phrase in response_lower for phrase in ["that's a good question", "this is interesting"]):
            patterns.append("luna_encouraging_voice")
        
        if any(phrase in response_lower for phrase in ["what's your take", "i'm curious about"]):
            patterns.append("luna_engagement_questions")
        
        return patterns
    
    def _find_shared_concepts(self, travis_response: str, luna_response: str) -> List[str]:
        """Find shared concepts between responses"""
        
        # Simple concept matching
        travis_words = set(travis_response.lower().split())
        luna_words = set(luna_response.lower().split())
        
        # Technical concepts
        tech_concepts = {"system", "architecture", "design", "model", "training", "development", "performance", "security", "complexity", "approach", "solution", "problem"}
        
        shared_concepts = []
        for concept in tech_concepts:
            if concept in travis_words and concept in luna_words:
                shared_concepts.append(concept)
        
        return shared_concepts
    
    def _compare_approaches(self, travis_response: str, luna_response: str) -> str:
        """Compare the overall approach taken in both responses"""
        
        travis_lower = travis_response.lower()
        luna_lower = luna_response.lower()
        
        if "step" in travis_lower and "step" in luna_lower:
            return "both_systematic"
        elif any(word in travis_lower for word in ["like", "similar"]) and any(word in luna_lower for word in ["like", "similar"]):
            return "both_analogical"
        elif any(word in travis_lower for word in ["complex", "simple"]) and any(word in luna_lower for word in ["complex", "balance"]):
            return "both_complexity_aware"
        else:
            return "different_approaches"
    
    def _analyze_attribution_quality(self, luna_response: str) -> float:
        """Analyze how well Luna attributes her knowledge"""
        
        response_lower = luna_response.lower()
        attribution_score = 0.0
        
        # Good attribution phrases
        good_attribution = [
            "i've learned", "my training", "based on what i know", "from my understanding",
            "my experience", "i've picked up", "i've come to understand"
        ]
        
        attribution_count = sum(1 for phrase in good_attribution if phrase in response_lower)
        attribution_score = min(1.0, attribution_count * 0.3)
        
        return attribution_score
    
    def _analyze_personality_difference(self, travis_response: str, luna_response: str) -> Dict[str, Any]:
        """Analyze personality differences between Travis and Luna"""
        
        travis_lower = travis_response.lower()
        luna_lower = luna_response.lower()
        
        return {
            "travis_directness": sum(1 for word in ["fucking", "bullshit", "real talk", "look"] if word in travis_lower),
            "luna_collaboration": sum(1 for phrase in ["let's", "together", "with you"] if phrase in luna_lower),
            "travis_raw_emotion": sum(1 for word in ["frustrated", "pissed", "annoying"] if word in travis_lower),
            "luna_encouragement": sum(1 for phrase in ["good question", "interesting", "curious"] if phrase in luna_lower),
            "shared_technical_depth": len(set(travis_lower.split()) & set(luna_lower.split()) & {"system", "architecture", "design", "development"})
        }
    
    def _calculate_overall_analysis(self, comparisons: List[ResponseComparison]) -> Dict[str, Any]:
        """Calculate overall analysis from all comparisons"""
        
        if not comparisons:
            return {}
        
        avg_similarity = sum(c.similarity_score for c in comparisons) / len(comparisons)
        avg_thinking = sum(c.thinking_alignment for c in comparisons) / len(comparisons)
        avg_voice = sum(c.voice_differentiation for c in comparisons) / len(comparisons)
        
        # Analyze patterns across all comparisons
        all_travis_patterns = []
        all_luna_patterns = []
        
        for comp in comparisons:
            all_travis_patterns.extend(comp.analysis.get('travis_patterns', []))
            all_luna_patterns.extend(comp.analysis.get('luna_patterns', []))
        
        return {
            "average_similarity": avg_similarity,
            "average_thinking_alignment": avg_thinking,
            "average_voice_differentiation": avg_voice,
            "consciousness_transfer_score": (avg_thinking * 0.5 + avg_voice * 0.3 + avg_similarity * 0.2),
            "common_travis_patterns": list(set(all_travis_patterns)),
            "common_luna_patterns": list(set(all_luna_patterns)),
            "total_comparisons": len(comparisons)
        }
    
    def _display_comparison_results(self, overall_analysis: Dict[str, Any], comparisons: List[ResponseComparison]):
        """Display comprehensive comparison results"""
        
        print(f"\n🏆 LUNA vs TRAVIS COMPARISON RESULTS")
        print("=" * 60)
        
        print(f"📊 Overall Scores:")
        print(f"   Similarity to Travis: {overall_analysis['average_similarity']:.2f}")
        print(f"   Thinking Alignment: {overall_analysis['average_thinking_alignment']:.2f}")
        print(f"   Voice Differentiation: {overall_analysis['average_voice_differentiation']:.2f}")
        print(f"   Consciousness Transfer: {overall_analysis['consciousness_transfer_score']:.2f}")
        
        print(f"\n🧠 Pattern Analysis:")
        print(f"   Travis Patterns: {overall_analysis['common_travis_patterns']}")
        print(f"   Luna Patterns: {overall_analysis['common_luna_patterns']}")
        
        # Consciousness assessment
        transfer_score = overall_analysis['consciousness_transfer_score']
        
        if transfer_score >= 0.8:
            status = "🏆 EXCELLENT CONSCIOUSNESS TRANSFER"
            description = "Luna thinks like Travis but speaks with her own authentic voice"
        elif transfer_score >= 0.6:
            status = "✅ GOOD CONSCIOUSNESS ALIGNMENT"
            description = "Strong thinking alignment with developing unique voice"
        elif transfer_score >= 0.4:
            status = "⚠️ MODERATE CONSCIOUSNESS TRANSFER"
            description = "Some thinking alignment but needs improvement"
        else:
            status = "❌ LIMITED CONSCIOUSNESS TRANSFER"
            description = "Significant gaps in thinking alignment and voice development"
        
        print(f"\n🎯 Consciousness Transfer Assessment:")
        print(f"   Status: {status}")
        print(f"   Analysis: {description}")
        
        # Show best examples
        best_comparisons = sorted(comparisons, key=lambda x: x.thinking_alignment, reverse=True)[:3]
        
        print(f"\n🌟 Best Thinking Alignment Examples:")
        for i, comp in enumerate(best_comparisons):
            print(f"\n   Example {i+1} (Score: {comp.thinking_alignment:.2f}):")
            print(f"   Q: {comp.query[:60]}...")
            print(f"   Travis: {comp.travis_actual[:80]}...")
            print(f"   Luna: {comp.luna_response[:80]}...")


def test_luna_travis_comparison():
    """Test the Luna vs Travis comparison system"""
    print("🔍 Testing Luna vs Travis Comparison System")
    print("=" * 60)
    
    comparison_system = LunaTravisComparisonSystem()
    
    if not comparison_system.luna:
        print("❌ Cannot run comparison - required systems unavailable")
        return
    
    # Run comparison analysis
    results = comparison_system.run_comparison_analysis(num_comparisons=8)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = comparison_system.aios_root / "AI" / "personality" / f"luna_travis_comparison_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Comparison results saved: {results_file.name}")
    print(f"\n🏁 Luna vs Travis comparison complete")


if __name__ == "__main__":
    test_luna_travis_comparison()
