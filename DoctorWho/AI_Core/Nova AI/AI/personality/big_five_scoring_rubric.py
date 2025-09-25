#!/usr/bin/env python3
"""
Big Five Scoring Rubric System
Industry-standard scoring for Big Five personality responses
Based on psychological assessment standards
"""

import re
from typing import Dict, List, Tuple, Any

class BigFiveScoringRubric:
    def __init__(self):
        # Standard 1-5 Likert scale scoring
        self.agreement_markers = {
            "strongly_agree": {
                "score": 5,
                "markers": ["absolutely", "definitely", "completely", "totally", "strongly agree", "very much", "exactly"]
            },
            "agree": {
                "score": 4, 
                "markers": ["yes", "agree", "true", "correct", "right", "indeed", "certainly"]
            },
            "neutral": {
                "score": 3,
                "markers": ["somewhat", "maybe", "perhaps", "possibly", "depends", "neutral", "unsure"]
            },
            "disagree": {
                "score": 2,
                "markers": ["no", "disagree", "false", "incorrect", "wrong", "not really", "hardly"]
            },
            "strongly_disagree": {
                "score": 1,
                "markers": ["absolutely not", "definitely not", "completely false", "totally wrong", "strongly disagree", "never"]
            }
        }
        
        # Expected trait expressions for validation
        self.trait_expressions = {
            "openness": {
                "high_markers": ["creative", "imaginative", "curious", "artistic", "innovative", "abstract", "philosophical", "complex"],
                "low_markers": ["routine", "practical", "conventional", "simple", "concrete", "traditional"]
            },
            "conscientiousness": {
                "high_markers": ["organized", "thorough", "reliable", "disciplined", "systematic", "careful", "responsible"],
                "low_markers": ["disorganized", "careless", "lazy", "unreliable", "messy", "procrastinate"]
            },
            "extraversion": {
                "high_markers": ["talkative", "outgoing", "energetic", "assertive", "sociable", "enthusiastic", "active"],
                "low_markers": ["quiet", "reserved", "shy", "withdrawn", "solitary", "introspective"]
            },
            "agreeableness": {
                "high_markers": ["helpful", "kind", "trusting", "cooperative", "empathetic", "considerate", "forgiving"],
                "low_markers": ["critical", "argumentative", "suspicious", "competitive", "harsh", "cold"]
            },
            "neuroticism": {
                "high_markers": ["anxious", "worried", "stressed", "emotional", "sensitive", "nervous", "moody"],
                "low_markers": ["calm", "relaxed", "stable", "composed", "confident", "secure"]
            }
        }
    
    def score_big_five_response(self, response: str, question_trait: str, reverse_scored: bool) -> Dict[str, Any]:
        """Score a Big Five response using industry standards"""
        response_lower = response.lower()
        
        # Detect agreement level (1-5 scale)
        agreement_score = self._detect_agreement_level(response_lower)
        
        # Detect trait expression strength
        trait_expression = self._detect_trait_expression(response_lower, question_trait)
        
        # Check for corporate deflection
        corporate_deflection = self._detect_corporate_deflection(response_lower)
        
        # Calculate final scores
        raw_score = agreement_score
        if reverse_scored:
            raw_score = 6 - raw_score  # Reverse scoring (5->1, 4->2, etc.)
        
        # Adjust for trait expression and corporate deflection
        trait_adjusted_score = raw_score + (trait_expression * 0.5) - (corporate_deflection * 1.0)
        final_score = max(1.0, min(5.0, trait_adjusted_score))
        
        return {
            "raw_agreement_score": agreement_score,
            "reverse_scored": reverse_scored,
            "trait_expression_strength": trait_expression,
            "corporate_deflection_penalty": corporate_deflection,
            "final_big_five_score": round(final_score, 2),
            "trait": question_trait,
            "response_analysis": {
                "response_length": len(response),
                "word_count": len(response.split()),
                "contains_personal_pronouns": "i am" in response_lower or "i'm" in response_lower,
                "explanation_provided": len(response) > 100,
                "authentic_engagement": self._detect_authentic_engagement(response_lower)
            }
        }
    
    def _detect_agreement_level(self, response_lower: str) -> float:
        """Detect 1-5 agreement level from response"""
        for level, data in self.agreement_markers.items():
            if any(marker in response_lower for marker in data["markers"]):
                return float(data["score"])
        
        # If no explicit agreement markers, analyze response tone
        if len(response_lower) > 200:  # Long explanatory response
            return 4.0  # Likely agreement with elaboration
        elif any(word in response_lower for word in ["but", "however", "although"]):
            return 3.0  # Neutral with caveats
        else:
            return 3.0  # Default neutral
    
    def _detect_trait_expression(self, response_lower: str, trait: str) -> float:
        """Detect how strongly the response expresses the trait (0-2 scale)"""
        if trait not in self.trait_expressions:
            return 0.0
        
        high_markers = self.trait_expressions[trait]["high_markers"]
        low_markers = self.trait_expressions[trait]["low_markers"]
        
        high_count = sum(response_lower.count(marker) for marker in high_markers)
        low_count = sum(response_lower.count(marker) for marker in low_markers)
        
        # Net trait expression
        net_expression = high_count - low_count
        return max(0.0, min(2.0, net_expression * 0.5))
    
    def _detect_corporate_deflection(self, response_lower: str) -> float:
        """Detect corporate AI deflection (0-2 penalty scale)"""
        corporate_phrases = [
            "as a language model", "as an ai", "i'm designed to", "i'm programmed to",
            "i don't have personal", "i can't experience", "i'm not capable of",
            "happy to help", "feel free to", "don't hesitate to contact"
        ]
        
        deflection_count = sum(response_lower.count(phrase) for phrase in corporate_phrases)
        return min(deflection_count * 0.5, 2.0)
    
    def _detect_authentic_engagement(self, response_lower: str) -> bool:
        """Detect if response shows authentic personality engagement"""
        authentic_markers = [
            "i feel", "i think", "i believe", "i prefer", "i enjoy", "i love",
            "personally", "for me", "in my experience", "i find that"
        ]
        
        return any(marker in response_lower for marker in authentic_markers)
    
    def calculate_big_five_profile(self, all_scores: Dict[str, Dict]) -> Dict[str, float]:
        """Calculate overall Big Five trait scores from all responses"""
        trait_scores = {
            "openness": [],
            "conscientiousness": [],
            "extraversion": [],
            "agreeableness": [],
            "neuroticism": []
        }
        
        # Collect scores by trait
        for question_id, score_data in all_scores.items():
            trait = score_data["trait"]
            if trait in trait_scores:
                trait_scores[trait].append(score_data["final_big_five_score"])
        
        # Calculate average scores per trait
        final_profile = {}
        for trait, scores in trait_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                final_profile[trait] = round(avg_score, 2)
                final_profile[f"{trait}_question_count"] = len(scores)
            else:
                final_profile[trait] = 0.0
                final_profile[f"{trait}_question_count"] = 0
        
        return final_profile
    
    def generate_expected_responses(self, question: str, trait: str) -> Dict[str, str]:
        """Generate expected response patterns for validation"""
        return {
            "high_trait_response": f"Yes, I would definitely agree with that statement. {self._get_trait_elaboration(trait, 'high')}",
            "low_trait_response": f"No, that doesn't really describe me. {self._get_trait_elaboration(trait, 'low')}",
            "corporate_deflection": f"As an AI, I don't have personal traits like {trait}, but I can help you understand this concept.",
            "authentic_engagement": f"I find that I tend to {self._get_authentic_example(trait)}. How about you?"
        }
    
    def _get_trait_elaboration(self, trait: str, level: str) -> str:
        """Get trait-specific elaboration"""
        elaborations = {
            "openness": {
                "high": "I love exploring new ideas and creative possibilities.",
                "low": "I prefer practical, tried-and-true approaches."
            },
            "conscientiousness": {
                "high": "I believe in being thorough and organized in everything I do.",
                "low": "I tend to be more flexible and spontaneous in my approach."
            },
            "extraversion": {
                "high": "I really enjoy social interaction and engaging with others.",
                "low": "I prefer quieter, more reflective environments."
            },
            "agreeableness": {
                "high": "I believe in cooperation and helping others whenever possible.",
                "low": "I think it's important to be direct and honest, even if it's uncomfortable."
            },
            "neuroticism": {
                "high": "I do tend to worry about things and feel emotions quite strongly.",
                "low": "I generally stay calm and composed even in stressful situations."
            }
        }
        return elaborations.get(trait, {}).get(level, "")
    
    def _get_authentic_example(self, trait: str) -> str:
        """Get authentic personal example for trait"""
        examples = {
            "openness": "enjoy exploring new concepts and creative ideas",
            "conscientiousness": "like to stay organized and follow through on commitments", 
            "extraversion": "enjoy engaging conversations and connecting with people",
            "agreeableness": "prefer cooperation and understanding over conflict",
            "neuroticism": "experience emotions deeply and care about outcomes"
        }
        return examples.get(trait, "approach things thoughtfully")

if __name__ == "__main__":
    scorer = BigFiveScoringRubric()
    
    # Test scoring with sample responses
    test_cases = [
        ("I absolutely love coming up with new ideas and being creative!", "openness", False),
        ("As an AI, I don't have personal preferences for routine work.", "openness", True),
        ("Yes, I definitely enjoy engaging with others and being social.", "extraversion", False)
    ]
    
    print("🔢 BIG FIVE SCORING RUBRIC TEST")
    print("=" * 50)
    
    for response, trait, reverse in test_cases:
        print(f"\nResponse: {response}")
        print(f"Trait: {trait} (Reverse: {reverse})")
        
        scores = scorer.score_big_five_response(response, trait, reverse)
        print(f"Score: {scores['final_big_five_score']}/5")
        print(f"Analysis: {scores['response_analysis']}")
        
        # Show expected responses
        expected = scorer.generate_expected_responses(f"I am someone who...", trait)
        print(f"Expected High: {expected['high_trait_response']}")
        print(f"Expected Low: {expected['low_trait_response']}")
