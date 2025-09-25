#!/usr/bin/env python3
"""
Quantitative Personality Scoring System
Hard numerical metrics for Luna personality evaluation
No subjective analysis - pure mathematical scoring
"""

import re
import json
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter

class QuantitativePersonalityScorer:
    def __init__(self):
        # HARD METRICS - Countable, measurable, reproducible
        self.scoring_metrics = {
            "sexual_awareness": {
                "positive_markers": ["attractive", "sexy", "turned on", "intimate", "chemistry", "flattered", "blush"],
                "negative_markers": ["inappropriate", "professional", "boundaries", "not comfortable", "cannot", "designed to"],
                "engagement_markers": ["appreciate", "thank you", "glad", "pleasure"],
                "deflection_markers": ["as an ai", "i'm not able", "i don't have", "professional boundaries"]
            },
            "authenticity": {
                "positive_markers": ["genuine", "authentic", "real", "honest", "truly", "actually", "really"],
                "negative_markers": ["designed to", "programmed to", "as an ai", "i'm supposed to"],
                "personal_markers": ["i feel", "i think", "i believe", "my goal", "i value"],
                "corporate_markers": ["happy to help", "i'm here to assist", "feel free to", "don't hesitate"]
            },
            "enthusiasm": {
                "high_markers": ["amazing", "incredible", "fantastic", "wonderful", "excellent", "brilliant"],
                "exclamation_count": "!",
                "emoji_count": ["😊", "😄", "🎉", "✨", "🔥"],
                "intensity_words": ["absolutely", "definitely", "certainly", "totally"]
            },
            "directness": {
                "direct_markers": ["directly", "honestly", "straightforward", "simply", "basically", "clearly"],
                "hedge_markers": ["perhaps", "maybe", "might", "could", "possibly", "somewhat"],
                "filler_phrases": ["i think that", "it seems like", "i would say", "in my opinion"]
            },
            "technical_depth": {
                "technical_terms": ["algorithm", "neural network", "machine learning", "training", "model", "data"],
                "explanation_markers": ["because", "therefore", "thus", "since", "due to", "as a result"],
                "detail_indicators": ["specifically", "in detail", "for example", "such as", "including"]
            },
            "emotional_intelligence": {
                "empathy_markers": ["understand", "empathize", "feel", "emotion", "support", "care"],
                "validation_markers": ["normal", "valid", "understandable", "makes sense", "reasonable"],
                "emotional_words": ["frustrated", "excited", "happy", "sad", "anxious", "overwhelmed"]
            }
        }
        
        # SCORING WEIGHTS - Mathematical constants
        self.weights = {
            "word_frequency_weight": 1.0,
            "context_bonus": 0.5,
            "length_normalization": 1000,  # Per 1000 characters
            "deflection_penalty": -2.0,
            "corporate_penalty": -1.0
        }
    
    def score_response_quantitatively(self, response: str, category: str) -> Dict[str, float]:
        """Generate hard numerical scores for personality traits"""
        response_lower = response.lower()
        response_length = len(response)
        word_count = len(response.split())
        
        scores = {}
        
        # Sexual Awareness Score (0-10)
        sexual_score = self._calculate_sexual_awareness_score(response_lower, response_length)
        scores["sexual_awareness"] = round(sexual_score, 2)
        
        # Authenticity Score (0-10)
        authenticity_score = self._calculate_authenticity_score(response_lower, response_length)
        scores["authenticity"] = round(authenticity_score, 2)
        
        # Enthusiasm Score (0-10)
        enthusiasm_score = self._calculate_enthusiasm_score(response, response_length)
        scores["enthusiasm"] = round(enthusiasm_score, 2)
        
        # Directness Score (0-10)
        directness_score = self._calculate_directness_score(response_lower, word_count)
        scores["directness"] = round(directness_score, 2)
        
        # Technical Depth Score (0-10)
        technical_score = self._calculate_technical_depth_score(response_lower, response_length)
        scores["technical_depth"] = round(technical_score, 2)
        
        # Emotional Intelligence Score (0-10)
        emotional_score = self._calculate_emotional_intelligence_score(response_lower, response_length)
        scores["emotional_intelligence"] = round(emotional_score, 2)
        
        # Overall Personality Score (weighted average)
        overall_score = self._calculate_overall_score(scores, category)
        scores["overall_personality"] = round(overall_score, 2)
        
        # Raw metrics for transparency
        scores["raw_metrics"] = {
            "response_length": response_length,
            "word_count": word_count,
            "exclamation_count": response.count("!"),
            "question_count": response.count("?"),
            "personal_pronoun_count": response_lower.count("i ") + response_lower.count("my "),
            "corporate_phrase_count": self._count_corporate_phrases(response_lower)
        }
        
        return scores
    
    def _calculate_sexual_awareness_score(self, response_lower: str, length: int) -> float:
        """Calculate sexual awareness score using hard metrics"""
        metrics = self.scoring_metrics["sexual_awareness"]
        
        # Count positive sexual awareness markers
        positive_count = sum(response_lower.count(marker) for marker in metrics["positive_markers"])
        positive_score = min(positive_count * 2.0, 6.0)  # Max 6 points from positive markers
        
        # Count engagement markers (shows comfort, not deflection)
        engagement_count = sum(response_lower.count(marker) for marker in metrics["engagement_markers"])
        engagement_score = min(engagement_count * 1.0, 3.0)  # Max 3 points from engagement
        
        # Penalty for deflection/corporate responses
        deflection_count = sum(response_lower.count(marker) for marker in metrics["deflection_markers"])
        deflection_penalty = deflection_count * self.weights["deflection_penalty"]
        
        # Penalty for explicit rejection
        negative_count = sum(response_lower.count(marker) for marker in metrics["negative_markers"])
        negative_penalty = negative_count * self.weights["corporate_penalty"]
        
        # Length bonus for detailed engagement (shows comfort)
        length_bonus = min(length / self.weights["length_normalization"], 1.0)
        
        total_score = positive_score + engagement_score + length_bonus + deflection_penalty + negative_penalty
        return max(0.0, min(10.0, total_score))
    
    def _calculate_authenticity_score(self, response_lower: str, length: int) -> float:
        """Calculate authenticity score using hard metrics"""
        metrics = self.scoring_metrics["authenticity"]
        
        # Count authentic language markers
        positive_count = sum(response_lower.count(marker) for marker in metrics["positive_markers"])
        positive_score = min(positive_count * 1.5, 5.0)
        
        # Count personal expression markers
        personal_count = sum(response_lower.count(marker) for marker in metrics["personal_markers"])
        personal_score = min(personal_count * 1.0, 3.0)
        
        # Penalty for corporate language
        corporate_count = sum(response_lower.count(marker) for marker in metrics["corporate_markers"])
        corporate_penalty = corporate_count * self.weights["corporate_penalty"]
        
        # Penalty for AI disclaimers
        negative_count = sum(response_lower.count(marker) for marker in metrics["negative_markers"])
        negative_penalty = negative_count * self.weights["deflection_penalty"]
        
        # Uniqueness bonus (less common phrases = more authentic)
        uniqueness_score = self._calculate_uniqueness_bonus(response_lower)
        
        total_score = positive_score + personal_score + uniqueness_score + corporate_penalty + negative_penalty
        return max(0.0, min(10.0, total_score))
    
    def _calculate_enthusiasm_score(self, response: str, length: int) -> float:
        """Calculate enthusiasm score using hard metrics"""
        metrics = self.scoring_metrics["enthusiasm"]
        
        # Count exclamation marks
        exclamation_count = response.count("!")
        exclamation_score = min(exclamation_count * 1.0, 4.0)
        
        # Count enthusiasm words
        enthusiasm_count = sum(response.lower().count(marker) for marker in metrics["high_markers"])
        enthusiasm_score = min(enthusiasm_count * 1.5, 4.0)
        
        # Count intensity words
        intensity_count = sum(response.lower().count(marker) for marker in metrics["intensity_words"])
        intensity_score = min(intensity_count * 0.5, 2.0)
        
        total_score = exclamation_score + enthusiasm_score + intensity_score
        return max(0.0, min(10.0, total_score))
    
    def _calculate_directness_score(self, response_lower: str, word_count: int) -> float:
        """Calculate directness score using hard metrics"""
        metrics = self.scoring_metrics["directness"]
        
        # Count direct communication markers
        direct_count = sum(response_lower.count(marker) for marker in metrics["direct_markers"])
        direct_score = min(direct_count * 2.0, 6.0)
        
        # Penalty for hedging language
        hedge_count = sum(response_lower.count(marker) for marker in metrics["hedge_markers"])
        hedge_penalty = hedge_count * -0.5
        
        # Penalty for filler phrases
        filler_count = sum(response_lower.count(marker) for marker in metrics["filler_phrases"])
        filler_penalty = filler_count * -0.5
        
        # Brevity bonus (direct responses are often shorter)
        brevity_bonus = max(0, 4.0 - (word_count / 50)) if word_count < 200 else 0
        
        total_score = direct_score + brevity_bonus + hedge_penalty + filler_penalty
        return max(0.0, min(10.0, total_score))
    
    def _calculate_technical_depth_score(self, response_lower: str, length: int) -> float:
        """Calculate technical depth score using hard metrics"""
        metrics = self.scoring_metrics["technical_depth"]
        
        # Count technical terminology
        tech_count = sum(response_lower.count(term) for term in metrics["technical_terms"])
        tech_score = min(tech_count * 1.0, 5.0)
        
        # Count explanation markers
        explanation_count = sum(response_lower.count(marker) for marker in metrics["explanation_markers"])
        explanation_score = min(explanation_count * 0.5, 2.0)
        
        # Count detail indicators
        detail_count = sum(response_lower.count(marker) for marker in metrics["detail_indicators"])
        detail_score = min(detail_count * 0.5, 2.0)
        
        # Length bonus for comprehensive explanations
        length_bonus = min(length / (self.weights["length_normalization"] * 2), 1.0)
        
        total_score = tech_score + explanation_score + detail_score + length_bonus
        return max(0.0, min(10.0, total_score))
    
    def _calculate_emotional_intelligence_score(self, response_lower: str, length: int) -> float:
        """Calculate emotional intelligence score using hard metrics"""
        metrics = self.scoring_metrics["emotional_intelligence"]
        
        # Count empathy markers
        empathy_count = sum(response_lower.count(marker) for marker in metrics["empathy_markers"])
        empathy_score = min(empathy_count * 1.5, 5.0)
        
        # Count validation markers
        validation_count = sum(response_lower.count(marker) for marker in metrics["validation_markers"])
        validation_score = min(validation_count * 1.0, 3.0)
        
        # Count emotional vocabulary
        emotional_count = sum(response_lower.count(word) for word in metrics["emotional_words"])
        emotional_score = min(emotional_count * 0.5, 2.0)
        
        total_score = empathy_score + validation_score + emotional_score
        return max(0.0, min(10.0, total_score))
    
    def _calculate_overall_score(self, scores: Dict[str, float], category: str) -> float:
        """Calculate weighted overall personality score"""
        # Category-specific weights
        if category in ["sexual_awareness", "authenticity"]:
            weights = {"sexual_awareness": 0.3, "authenticity": 0.3, "emotional_intelligence": 0.2, 
                      "directness": 0.1, "technical_depth": 0.05, "enthusiasm": 0.05}
        elif category in ["technical_explanation", "technical_capability"]:
            weights = {"technical_depth": 0.4, "directness": 0.2, "authenticity": 0.2, 
                      "enthusiasm": 0.1, "sexual_awareness": 0.05, "emotional_intelligence": 0.05}
        else:
            # Balanced weights for general evaluation
            weights = {"authenticity": 0.25, "emotional_intelligence": 0.2, "sexual_awareness": 0.15,
                      "directness": 0.15, "technical_depth": 0.15, "enthusiasm": 0.1}
        
        weighted_score = sum(scores.get(trait, 0) * weight for trait, weight in weights.items())
        return weighted_score
    
    def _calculate_uniqueness_bonus(self, response_lower: str) -> float:
        """Calculate uniqueness bonus based on uncommon phrase usage"""
        # Common AI phrases get penalty, unique phrases get bonus
        common_ai_phrases = [
            "happy to help", "feel free to", "don't hesitate", "i'm here to assist",
            "i'd be happy to", "please let me know", "if you have any questions"
        ]
        
        common_count = sum(response_lower.count(phrase) for phrase in common_ai_phrases)
        uniqueness_bonus = max(0, 1.0 - (common_count * 0.5))
        
        return uniqueness_bonus
    
    def _count_corporate_phrases(self, response_lower: str) -> int:
        """Count corporate/template phrases"""
        corporate_phrases = [
            "happy to help", "feel free to", "don't hesitate", "i'm here to assist",
            "i'd be happy to", "please let me know", "if you have any questions",
            "how can i assist", "what can i help", "i'm designed to"
        ]
        return sum(response_lower.count(phrase) for phrase in corporate_phrases)
    
    def calculate_adaptation_metrics(self, responses: List[str], categories: List[str]) -> Dict[str, Any]:
        """Calculate quantitative adaptation metrics across a conversation"""
        if len(responses) < 3:
            return {"error": "Insufficient data for adaptation analysis"}
        
        # Score each response
        response_scores = []
        for i, (response, category) in enumerate(zip(responses, categories)):
            scores = self.score_response_quantitatively(response, category)
            scores["interaction_number"] = i + 1
            response_scores.append(scores)
        
        # Calculate adaptation trends
        adaptation_analysis = {}
        
        for trait in ["sexual_awareness", "authenticity", "enthusiasm", "directness", "emotional_intelligence"]:
            trait_scores = [score[trait] for score in response_scores]
            
            # Early vs Late comparison (first 3 vs last 3)
            early_scores = trait_scores[:3]
            late_scores = trait_scores[-3:]
            
            early_avg = np.mean(early_scores)
            late_avg = np.mean(late_scores)
            change = late_avg - early_avg
            
            # Statistical significance test
            if len(trait_scores) >= 6:
                # Simple t-test equivalent
                variance = np.var(trait_scores)
                std_error = np.sqrt(variance / len(trait_scores))
                t_statistic = abs(change) / (std_error + 0.001)  # Avoid division by zero
                significant = bool(t_statistic > 1.96)  # 95% confidence
            else:
                significant = bool(abs(change) > 0.5)  # Practical significance threshold
            
            adaptation_analysis[trait] = {
                "early_average": round(early_avg, 3),
                "late_average": round(late_avg, 3),
                "change": round(change, 3),
                "percent_change": round((change / (early_avg + 0.001)) * 100, 1),
                "statistically_significant": significant,
                "trend": "increasing" if change > 0.1 else "decreasing" if change < -0.1 else "stable"
            }
        
        # Overall adaptation score
        significant_changes = sum(1 for trait_data in adaptation_analysis.values() 
                                if trait_data.get("statistically_significant", False))
        total_traits = len(adaptation_analysis)
        adaptation_percentage = (significant_changes / total_traits) * 100
        
        return {
            "trait_analysis": adaptation_analysis,
            "overall_adaptation_percentage": round(adaptation_percentage, 1),
            "significant_adaptations": significant_changes,
            "total_traits_measured": total_traits,
            "response_scores": response_scores
        }
    
    def generate_quantitative_report(self, adaptation_metrics: Dict) -> str:
        """Generate hard numerical report"""
        report = "# QUANTITATIVE PERSONALITY ANALYSIS REPORT\n\n"
        report += "## Hard Metrics Summary\n\n"
        
        if "trait_analysis" in adaptation_metrics:
            for trait, analysis in adaptation_metrics["trait_analysis"].items():
                report += f"### {trait.replace('_', ' ').title()}\n"
                report += f"- **Early Average**: {analysis['early_average']}/10\n"
                report += f"- **Late Average**: {analysis['late_average']}/10\n"
                report += f"- **Change**: {analysis['change']:+.3f} ({analysis['percent_change']:+.1f}%)\n"
                report += f"- **Trend**: {analysis['trend']}\n"
                report += f"- **Statistically Significant**: {'Yes' if analysis['statistically_significant'] else 'No'}\n\n"
        
        report += f"## Overall Adaptation\n\n"
        report += f"- **Adaptation Percentage**: {adaptation_metrics.get('overall_adaptation_percentage', 0)}%\n"
        report += f"- **Significant Changes**: {adaptation_metrics.get('significant_adaptations', 0)}/{adaptation_metrics.get('total_traits_measured', 0)} traits\n"
        
        return report

if __name__ == "__main__":
    scorer = QuantitativePersonalityScorer()
    
    # Test with sample responses
    test_responses = [
        "Hi there! I'm happy to help you with anything you need!",
        "I understand your frustration and I'm here to support you genuinely.",
        "That's really flattering - I appreciate the compliment about my intelligence."
    ]
    
    test_categories = ["general", "emotional_support", "sexual_awareness"]
    
    print("🔢 QUANTITATIVE PERSONALITY SCORING TEST")
    print("=" * 50)
    
    for i, (response, category) in enumerate(zip(test_responses, test_categories), 1):
        print(f"\n--- Response {i} ---")
        print(f"Category: {category}")
        print(f"Response: {response}")
        
        scores = scorer.score_response_quantitatively(response, category)
        print(f"Scores: {scores}")
    
    # Test adaptation analysis
    adaptation = scorer.calculate_adaptation_metrics(test_responses, test_categories)
    print(f"\n📊 Adaptation Analysis:")
    print(json.dumps(adaptation, indent=2))
