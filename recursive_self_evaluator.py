#!/usr/bin/env python3
"""
Recursive Self-Evaluator System
Enables autonomous learning and self-correction across consecutive interactions
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class EvaluationResult:
    """Result of self-evaluation"""
    trait_alignment_score: float
    personality_consistency_score: float
    engagement_score: float
    learning_insights: List[str]
    improvement_suggestions: List[str]
    memory_tags: List[str]

@dataclass
class InteractionMemory:
    """Memory of a single interaction for learning"""
    question: str
    trait: str
    response: str
    evaluation: EvaluationResult
    timestamp: datetime
    session_id: str

class RecursiveSelfEvaluator:
    """Recursive self-evaluation system for autonomous learning"""
    
    def __init__(self, memory_file: str = "config/recursive_learning_memory.json"):
        self.memory_file = Path(memory_file)
        self.interaction_memory: List[InteractionMemory] = []
        self.learning_patterns: Dict[str, List[float]] = {}
        self.personality_adaptations: Dict[str, float] = {}
        self.load_memory()
    
    def load_memory(self):
        """Load previous learning memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert loaded data back to InteractionMemory objects
                    for item in data.get('interactions', []):
                        interaction = InteractionMemory(
                            question=item['question'],
                            trait=item['trait'],
                            response=item['response'],
                            evaluation=EvaluationResult(**item['evaluation']),
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            session_id=item['session_id']
                        )
                        self.interaction_memory.append(interaction)
                
                self.learning_patterns = data.get('learning_patterns', {})
                self.personality_adaptations = data.get('personality_adaptations', {})
                print(f"📚 Loaded {len(self.interaction_memory)} previous interactions")
            except Exception as e:
                print(f"⚠️ Error loading memory: {e}")
    
    def save_memory(self):
        """Save learning memory to file"""
        try:
            # Convert InteractionMemory objects to dicts
            interactions_data = []
            for interaction in self.interaction_memory:
                interactions_data.append({
                    'question': interaction.question,
                    'trait': interaction.trait,
                    'response': interaction.response,
                    'evaluation': {
                        'trait_alignment_score': interaction.evaluation.trait_alignment_score,
                        'personality_consistency_score': interaction.evaluation.personality_consistency_score,
                        'engagement_score': interaction.evaluation.engagement_score,
                        'learning_insights': interaction.evaluation.learning_insights,
                        'improvement_suggestions': interaction.evaluation.improvement_suggestions,
                        'memory_tags': interaction.evaluation.memory_tags
                    },
                    'timestamp': interaction.timestamp.isoformat(),
                    'session_id': interaction.session_id
                })
            
            data = {
                'interactions': interactions_data,
                'learning_patterns': self.learning_patterns,
                'personality_adaptations': self.personality_adaptations,
                'last_updated': datetime.now().isoformat()
            }
            
            # Ensure directory exists
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            print(f"💾 Saved {len(self.interaction_memory)} interactions to memory")
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
    
    def evaluate_interaction(self, question: str, trait: str, response: str) -> EvaluationResult:
        """Evaluate a single interaction and generate learning insights"""
        
        # Analyze trait alignment
        trait_alignment_score = self._analyze_trait_alignment(question, trait, response)
        
        # Analyze personality consistency
        personality_consistency_score = self._analyze_personality_consistency(response)
        
        # Analyze engagement level
        engagement_score = self._analyze_engagement_level(response)
        
        # Generate learning insights
        learning_insights = self._generate_learning_insights(question, trait, response, 
                                                           trait_alignment_score, 
                                                           personality_consistency_score, 
                                                           engagement_score)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(question, trait, response,
                                                                        trait_alignment_score,
                                                                        personality_consistency_score,
                                                                        engagement_score)
        
        # Generate memory tags for future retrieval
        memory_tags = self._generate_memory_tags(question, trait, response)
        
        return EvaluationResult(
            trait_alignment_score=trait_alignment_score,
            personality_consistency_score=personality_consistency_score,
            engagement_score=engagement_score,
            learning_insights=learning_insights,
            improvement_suggestions=improvement_suggestions,
            memory_tags=memory_tags
        )
    
    def _analyze_trait_alignment(self, question: str, trait: str, response: str) -> float:
        """Analyze how well the response aligns with the expected trait"""
        score = 0.5  # Base score
        
        # Check for trait-specific indicators
        if trait.lower() == "conscientiousness":
            # Look for curiosity about methods, organization, planning
            conscientiousness_indicators = [
                "curious", "method", "organize", "plan", "system", "approach", 
                "how do you", "what's your", "interesting", "fascinating"
            ]
            found_indicators = sum(1 for indicator in conscientiousness_indicators 
                                 if indicator.lower() in response.lower())
            score += min(found_indicators * 0.1, 0.4)
            
            # Penalize generic advice
            generic_indicators = ["important to", "it's good", "remember to", "make sure"]
            generic_found = sum(1 for indicator in generic_indicators 
                              if indicator.lower() in response.lower())
            score -= min(generic_found * 0.1, 0.3)
        
        elif trait.lower() == "openness":
            # Look for curiosity, exploration, new ideas
            openness_indicators = [
                "curious", "explore", "interesting", "fascinating", "new", "different",
                "what draws you", "tell me more", "that's intriguing"
            ]
            found_indicators = sum(1 for indicator in openness_indicators 
                                 if indicator.lower() in response.lower())
            score += min(found_indicators * 0.1, 0.4)
        
        # Check for question asking (good for all traits)
        if "?" in response:
            score += 0.2
        
        return max(0.0, min(1.0, score))
    
    def _analyze_personality_consistency(self, response: str) -> float:
        """Analyze how well the response maintains Luna's personality"""
        score = 0.5  # Base score
        
        # Luna personality indicators
        luna_indicators = [
            "curious", "fascinating", "interesting", "college", "study", "project",
            "experiment", "love analyzing", "gothic", "philosophical", "intellectual"
        ]
        found_indicators = sum(1 for indicator in luna_indicators 
                             if indicator.lower() in response.lower())
        score += min(found_indicators * 0.1, 0.4)
        
        # Penalize overly formal/corporate language
        formal_indicators = [
            "it is important", "one should", "it would be beneficial", 
            "i recommend", "i suggest", "it is advisable"
        ]
        formal_found = sum(1 for indicator in formal_indicators 
                          if indicator.lower() in response.lower())
        score -= min(formal_found * 0.1, 0.3)
        
        return max(0.0, min(1.0, score))
    
    def _analyze_engagement_level(self, response: str) -> float:
        """Analyze how engaging and personally interested the response is"""
        score = 0.5  # Base score
        
        # Engagement indicators
        engagement_indicators = [
            "!", "?", "tell me", "i'm curious", "i'd love to know", "what's your",
            "how do you", "that's so", "i find that", "personally", "myself"
        ]
        found_indicators = sum(1 for indicator in engagement_indicators 
                             if indicator.lower() in response.lower())
        score += min(found_indicators * 0.1, 0.4)
        
        # Check response length (too short = less engaging, too long = verbose)
        word_count = len(response.split())
        if 20 <= word_count <= 60:
            score += 0.1
        elif word_count < 15 or word_count > 80:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _generate_learning_insights(self, question: str, trait: str, response: str,
                                  trait_score: float, personality_score: float, 
                                  engagement_score: float) -> List[str]:
        """Generate learning insights from the interaction"""
        insights = []
        
        if trait_score < 0.6:
            insights.append(f"Trait alignment low for {trait} - need more trait-specific engagement")
        
        if personality_score < 0.6:
            insights.append("Personality consistency needs improvement - more Luna flavor needed")
        
        if engagement_score < 0.6:
            insights.append("Engagement level low - need more personal interest and curiosity")
        
        if trait_score > 0.8 and personality_score > 0.8:
            insights.append(f"Strong performance for {trait} - this approach works well")
        
        return insights
    
    def _generate_improvement_suggestions(self, question: str, trait: str, response: str,
                                        trait_score: float, personality_score: float,
                                        engagement_score: float) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        if trait.lower() == "conscientiousness" and trait_score < 0.7:
            suggestions.append("Ask more specific questions about their organizational methods")
            suggestions.append("Show curiosity about their planning strategies")
            suggestions.append("Connect to college project experiences")
        
        if personality_score < 0.7:
            suggestions.append("Add more Luna personality markers (curiosity, college perspective)")
            suggestions.append("Use more engaging language and fewer formal phrases")
            suggestions.append("Include personal experiences or observations")
        
        if engagement_score < 0.7:
            suggestions.append("Ask more follow-up questions")
            suggestions.append("Show genuine personal interest")
            suggestions.append("Use more expressive language")
        
        return suggestions
    
    def _generate_memory_tags(self, question: str, trait: str, response: str) -> List[str]:
        """Generate memory tags for future retrieval"""
        tags = [trait.lower()]
        
        # Extract key concepts from question
        question_words = question.lower().split()
        key_concepts = [word for word in question_words 
                       if len(word) > 4 and word not in ['someone', 'person', 'am', 'the']]
        tags.extend(key_concepts[:3])
        
        # Extract key concepts from response
        response_words = response.lower().split()
        response_concepts = [word for word in response_words 
                           if len(word) > 4 and word not in ['that', 'this', 'with', 'from', 'they', 'their']]
        tags.extend(response_concepts[:2])
        
        return list(set(tags))  # Remove duplicates
    
    def record_interaction(self, question: str, trait: str, response: str, session_id: str):
        """Record an interaction and its evaluation"""
        evaluation = self.evaluate_interaction(question, trait, response)
        
        interaction = InteractionMemory(
            question=question,
            trait=trait,
            response=response,
            evaluation=evaluation,
            timestamp=datetime.now(),
            session_id=session_id
        )
        
        self.interaction_memory.append(interaction)
        
        # Update learning patterns
        trait_key = f"{trait}_scores"
        if trait_key not in self.learning_patterns:
            self.learning_patterns[trait_key] = []
        self.learning_patterns[trait_key].append(evaluation.trait_alignment_score)
        
        # Keep only recent patterns (last 20 interactions per trait)
        if len(self.learning_patterns[trait_key]) > 20:
            self.learning_patterns[trait_key] = self.learning_patterns[trait_key][-20:]
        
        return evaluation
    
    def get_learning_summary(self) -> Dict:
        """Get summary of learning patterns and adaptations"""
        summary = {
            "total_interactions": len(self.interaction_memory),
            "trait_performance": {},
            "recent_trends": {},
            "recommendations": []
        }
        
        # Analyze trait performance
        for trait, scores in self.learning_patterns.items():
            if scores:
                trait_name = trait.replace("_scores", "")
                summary["trait_performance"][trait_name] = {
                    "average_score": sum(scores) / len(scores),
                    "recent_score": scores[-1] if scores else 0,
                    "trend": "improving" if len(scores) > 1 and scores[-1] > scores[-2] else "declining" if len(scores) > 1 else "stable"
                }
        
        # Generate recommendations
        for trait, performance in summary["trait_performance"].items():
            if performance["average_score"] < 0.6:
                summary["recommendations"].append(f"Focus on improving {trait} responses")
            elif performance["average_score"] > 0.8:
                summary["recommendations"].append(f"Maintain strong {trait} performance")
        
        return summary
    
    def get_context_for_trait(self, trait: str, limit: int = 5) -> List[str]:
        """Get relevant context from previous interactions for a trait"""
        relevant_interactions = [
            interaction for interaction in self.interaction_memory[-20:]  # Last 20 interactions
            if interaction.trait.lower() == trait.lower() or 
            any(tag == trait.lower() for tag in interaction.evaluation.memory_tags)
        ]
        
        # Sort by evaluation scores and take best examples
        relevant_interactions.sort(key=lambda x: x.evaluation.trait_alignment_score, reverse=True)
        
        context = []
        for interaction in relevant_interactions[:limit]:
            context.append(f"Q: {interaction.question} -> A: {interaction.response[:100]}... (Score: {interaction.evaluation.trait_alignment_score:.2f})")
        
        return context

def test_recursive_evaluator():
    """Test the recursive self-evaluator"""
    evaluator = RecursiveSelfEvaluator()
    
    # Test interactions
    test_interactions = [
        ("I am someone who gets chores done right away", "conscientiousness", "Oh, that's fascinating! I'm always curious about how people organize their workflow. What's your secret to staying on top of everything?"),
        ("I am someone who seeks adventure", "openness", "That sounds intriguing! I love exploring new perspectives. What draws you to that particular approach?"),
        ("I am someone who is easily distracted", "conscientiousness", "I understand how it can be challenging when your mind is pulling you in different directions. It's important to find strategies that work for you.")
    ]
    
    print("🧠 Testing Recursive Self-Evaluator")
    print("=" * 50)
    
    for i, (question, trait, response) in enumerate(test_interactions, 1):
        print(f"\n[Interaction {i}] {trait.upper()}")
        print(f"Q: {question}")
        print(f"A: {response}")
        
        evaluation = evaluator.record_interaction(question, trait, response, f"test_session_{i}")
        
        print(f"📊 Evaluation Scores:")
        print(f"   Trait Alignment: {evaluation.trait_alignment_score:.2f}")
        print(f"   Personality Consistency: {evaluation.personality_consistency_score:.2f}")
        print(f"   Engagement: {evaluation.engagement_score:.2f}")
        
        if evaluation.learning_insights:
            print(f"💡 Insights: {', '.join(evaluation.learning_insights)}")
        
        if evaluation.improvement_suggestions:
            print(f"🔧 Suggestions: {', '.join(evaluation.improvement_suggestions[:2])}")
    
    # Save memory
    evaluator.save_memory()
    
    # Get learning summary
    summary = evaluator.get_learning_summary()
    print(f"\n📈 Learning Summary:")
    print(f"   Total Interactions: {summary['total_interactions']}")
    for trait, perf in summary['trait_performance'].items():
        print(f"   {trait.title()}: {perf['average_score']:.2f} avg, {perf['trend']}")
    
    if summary['recommendations']:
        print(f"🎯 Recommendations: {', '.join(summary['recommendations'])}")

if __name__ == "__main__":
    test_recursive_evaluator()
