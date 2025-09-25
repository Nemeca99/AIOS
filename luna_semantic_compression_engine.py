#!/usr/bin/env python3
"""
Semantic Compression Engine - The Cost of Thinking
=================================================

Implements the final layer of the Blood-Mage Economy: internal resource allocation
for thinking processes with risk/reward economics.

Key Concepts:
1. Thinking Cost - Upfront token deduction for complex reasoning
2. Compression Bonus - Efficiency rewards for compressed responses
3. Risk/Reward Decision - Luna must decide if thinking cost is worth it
4. Internal Resource Allocation - Even reasoning has economic consequences
"""

import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

class ThinkingMode(Enum):
    """Different modes of thinking with associated costs"""
    INSTANT = "instant"          # No thinking cost, immediate response
    QUICK_ANALYSIS = "quick"     # 10-20 tokens thinking cost
    DEEP_ANALYSIS = "deep"       # 30-50 tokens thinking cost
    PHILOSOPHICAL = "philosophical"  # 50-100 tokens thinking cost
    MAXIMUM_COMPLEXITY = "maximum"   # 100+ tokens thinking cost

class CompressionResult(Enum):
    """Results of compression analysis"""
    HIGHLY_EFFICIENT = "highly_efficient"  # >50% token savings
    EFFICIENT = "efficient"                # 25-50% token savings
    MODERATE = "moderate"                  # 10-25% token savings
    INEFFICIENT = "inefficient"            # <10% token savings
    WASTEFUL = "wasteful"                  # No savings or increased tokens

@dataclass
class ThinkingCost:
    """Cost of thinking process"""
    mode: ThinkingMode
    upfront_cost: int
    estimated_compression_savings: int
    risk_level: float  # 0.0 to 1.0
    expected_quality_boost: float  # 0.0 to 1.0

@dataclass
class CompressionAnalysis:
    """Analysis of response compression"""
    original_length: int
    compressed_length: int
    thinking_cost: int
    net_savings: int
    efficiency_ratio: float
    compression_result: CompressionResult
    quality_maintained: bool

class LunaSemanticCompressionEngine:
    """The Cost of Thinking - Internal Resource Allocation System"""
    
    def __init__(self):
        self.thinking_costs = {
            ThinkingMode.INSTANT: ThinkingCost(
                mode=ThinkingMode.INSTANT,
                upfront_cost=0,
                estimated_compression_savings=0,
                risk_level=0.0,
                expected_quality_boost=0.0
            ),
            ThinkingMode.QUICK_ANALYSIS: ThinkingCost(
                mode=ThinkingMode.QUICK_ANALYSIS,
                upfront_cost=15,
                estimated_compression_savings=20,
                risk_level=0.2,
                expected_quality_boost=0.3
            ),
            ThinkingMode.DEEP_ANALYSIS: ThinkingCost(
                mode=ThinkingMode.DEEP_ANALYSIS,
                upfront_cost=40,
                estimated_compression_savings=60,
                risk_level=0.4,
                expected_quality_boost=0.6
            ),
            ThinkingMode.PHILOSOPHICAL: ThinkingCost(
                mode=ThinkingMode.PHILOSOPHICAL,
                upfront_cost=75,
                estimated_compression_savings=100,
                risk_level=0.6,
                expected_quality_boost=0.8
            ),
            ThinkingMode.MAXIMUM_COMPLEXITY: ThinkingCost(
                mode=ThinkingMode.MAXIMUM_COMPLEXITY,
                upfront_cost=150,
                estimated_compression_savings=200,
                risk_level=0.8,
                expected_quality_boost=0.9
            )
        }
        
        self.compression_history = []
        self.efficiency_learning_rate = 0.1
        
    def assess_thinking_requirement(self, question: str, context: Dict, 
                                  current_token_pool: int) -> Tuple[ThinkingMode, bool]:
        """
        Assess if Luna should invest in thinking cost for this question
        
        Returns:
            (thinking_mode, should_invest)
        """
        
        # Analyze question complexity
        complexity_score = self._analyze_question_complexity(question)
        emotional_stakes = context.get('emotional_stakes', 0.0)
        response_priority = context.get('response_priority', 'low')
        
        # Calculate risk/reward ratio
        available_tokens = current_token_pool
        
        # Determine thinking mode based on complexity and stakes
        if complexity_score < 0.2 and emotional_stakes < 0.1:
            thinking_mode = ThinkingMode.INSTANT
            should_invest = False
        elif complexity_score < 0.4 and emotional_stakes < 0.3:
            thinking_mode = ThinkingMode.QUICK_ANALYSIS
            should_invest = available_tokens > 50
        elif complexity_score < 0.6 and emotional_stakes < 0.5:
            thinking_mode = ThinkingMode.DEEP_ANALYSIS
            should_invest = available_tokens > 100
        elif complexity_score < 0.8 and emotional_stakes < 0.7:
            thinking_mode = ThinkingMode.PHILOSOPHICAL
            should_invest = available_tokens > 200
        else:
            thinking_mode = ThinkingMode.MAXIMUM_COMPLEXITY
            should_invest = available_tokens > 300
        
        # Additional factors
        if response_priority == 'critical':
            should_invest = True
        elif response_priority == 'low':
            should_invest = False
        
        return thinking_mode, should_invest
    
    def deduct_thinking_cost(self, thinking_mode: ThinkingMode, 
                           current_token_pool: int) -> Tuple[int, bool]:
        """
        Deduct thinking cost from token pool
        
        Returns:
            (remaining_tokens, deduction_successful)
        """
        thinking_cost = self.thinking_costs[thinking_mode]
        
        if current_token_pool >= thinking_cost.upfront_cost:
            remaining_tokens = current_token_pool - thinking_cost.upfront_cost
            return remaining_tokens, True
        else:
            # Insufficient tokens for thinking cost
            return current_token_pool, False
    
    def apply_thinking_enhancement(self, question: str, thinking_mode: ThinkingMode) -> str:
        """
        Apply thinking enhancement to the question based on thinking mode
        
        This simulates Luna's internal reasoning process
        """
        thinking_cost = self.thinking_costs[thinking_mode]
        
        if thinking_mode == ThinkingMode.INSTANT:
            return question
        
        # Add thinking context based on mode
        thinking_contexts = {
            ThinkingMode.QUICK_ANALYSIS: "\n[THINKING: Quick analysis mode - optimizing for efficiency while maintaining clarity]",
            ThinkingMode.DEEP_ANALYSIS: "\n[THINKING: Deep analysis mode - comprehensive understanding with precise expression]",
            ThinkingMode.PHILOSOPHICAL: "\n[THINKING: Philosophical mode - exploring deeper meanings and implications]",
            ThinkingMode.MAXIMUM_COMPLEXITY: "\n[THINKING: Maximum complexity mode - ultimate precision and depth of understanding]"
        }
        
        enhanced_question = question + thinking_contexts.get(thinking_mode, "")
        return enhanced_question
    
    def analyze_compression_efficiency(self, original_response: str, 
                                     compressed_response: str, 
                                     thinking_cost: int) -> CompressionAnalysis:
        """
        Analyze the efficiency of compression after thinking investment
        
        Returns comprehensive analysis of compression results
        """
        original_length = len(original_response.split())
        compressed_length = len(compressed_response.split())
        
        # Calculate savings
        token_savings = original_length - compressed_length
        net_savings = token_savings - thinking_cost
        
        # Calculate efficiency ratio
        if original_length > 0:
            efficiency_ratio = token_savings / original_length
        else:
            efficiency_ratio = 0.0
        
        # Determine compression result
        if efficiency_ratio > 0.5:
            compression_result = CompressionResult.HIGHLY_EFFICIENT
        elif efficiency_ratio > 0.25:
            compression_result = CompressionResult.EFFICIENT
        elif efficiency_ratio > 0.1:
            compression_result = CompressionResult.MODERATE
        elif efficiency_ratio > 0.0:
            compression_result = CompressionResult.INEFFICIENT
        else:
            compression_result = CompressionResult.WASTEFUL
        
        # Assess quality maintenance (simplified)
        quality_maintained = compressed_length > 0 and len(compressed_response.strip()) > 0
        
        analysis = CompressionAnalysis(
            original_length=original_length,
            compressed_length=compressed_length,
            thinking_cost=thinking_cost,
            net_savings=net_savings,
            efficiency_ratio=efficiency_ratio,
            compression_result=compression_result,
            quality_maintained=quality_maintained
        )
        
        # Store in history for learning
        self.compression_history.append(analysis)
        
        return analysis
    
    def calculate_compression_bonus(self, analysis: CompressionAnalysis) -> int:
        """
        Calculate efficiency bonus based on compression analysis
        
        Returns tokens to add back to pool as reward
        """
        bonus_multipliers = {
            CompressionResult.HIGHLY_EFFICIENT: 1.5,
            CompressionResult.EFFICIENT: 1.2,
            CompressionResult.MODERATE: 1.0,
            CompressionResult.INEFFICIENT: 0.8,
            CompressionResult.WASTEFUL: 0.5
        }
        
        base_bonus = max(0, analysis.net_savings)
        multiplier = bonus_multipliers[analysis.compression_result]
        
        # Quality bonus
        if analysis.quality_maintained:
            quality_bonus = int(base_bonus * 0.2)
        else:
            quality_bonus = 0
        
        total_bonus = int(base_bonus * multiplier) + quality_bonus
        
        return total_bonus
    
    def update_thinking_efficiency(self, analysis: CompressionAnalysis):
        """
        Update thinking cost estimates based on actual performance
        
        This implements learning from experience
        """
        if analysis.compression_result in [CompressionResult.HIGHLY_EFFICIENT, CompressionResult.EFFICIENT]:
            # Successful compression - reduce risk estimates
            for mode in ThinkingMode:
                if mode != ThinkingMode.INSTANT:
                    cost = self.thinking_costs[mode]
                    cost.risk_level = max(0.0, cost.risk_level - self.efficiency_learning_rate * 0.1)
                    cost.expected_quality_boost = min(1.0, cost.expected_quality_boost + self.efficiency_learning_rate * 0.05)
        else:
            # Failed compression - increase risk estimates
            for mode in ThinkingMode:
                if mode != ThinkingMode.INSTANT:
                    cost = self.thinking_costs[mode]
                    cost.risk_level = min(1.0, cost.risk_level + self.efficiency_learning_rate * 0.1)
                    cost.expected_quality_boost = max(0.0, cost.expected_quality_boost - self.efficiency_learning_rate * 0.05)
    
    def get_thinking_efficiency_stats(self) -> Dict:
        """
        Get statistics on thinking efficiency over time
        
        Returns comprehensive efficiency statistics
        """
        if not self.compression_history:
            return {
                "total_analyses": 0,
                "average_efficiency": 0.0,
                "success_rate": 0.0,
                "total_net_savings": 0,
                "most_efficient_mode": "none"
            }
        
        total_analyses = len(self.compression_history)
        successful_analyses = sum(1 for a in self.compression_history 
                                if a.compression_result in [CompressionResult.HIGHLY_EFFICIENT, CompressionResult.EFFICIENT])
        
        average_efficiency = sum(a.efficiency_ratio for a in self.compression_history) / total_analyses
        success_rate = successful_analyses / total_analyses
        total_net_savings = sum(a.net_savings for a in self.compression_history)
        
        # Find most efficient mode (simplified - would need mode tracking)
        most_efficient_mode = "deep_analysis"  # Placeholder
        
        return {
            "total_analyses": total_analyses,
            "average_efficiency": average_efficiency,
            "success_rate": success_rate,
            "total_net_savings": total_net_savings,
            "most_efficient_mode": most_efficient_mode
        }
    
    def _analyze_question_complexity(self, question: str) -> float:
        """
        Analyze question complexity for thinking mode selection
        
        Returns complexity score from 0.0 to 1.0
        """
        question_lower = question.lower()
        complexity_indicators = {
            # High complexity indicators
            "explain": 0.8, "analyze": 0.8, "compare": 0.7, "contrast": 0.7,
            "why": 0.6, "how": 0.6, "what if": 0.7, "imagine": 0.6,
            "philosophy": 0.9, "intelligence": 0.9, "meaning": 0.8,
            "quantum": 0.9, "relativity": 0.9, "algorithm": 0.8,
            
            # Medium complexity indicators  
            "describe": 0.5, "tell me about": 0.4, "what is": 0.4,
            "difference": 0.6, "similar": 0.5, "relationship": 0.6,
            
            # Low complexity indicators
            "hello": 0.1, "hi": 0.1, "how are you": 0.2, "good morning": 0.2,
            "yes": 0.1, "no": 0.1, "thanks": 0.1, "ok": 0.1
        }
        
        max_complexity = 0.0
        for indicator, complexity in complexity_indicators.items():
            if indicator in question_lower:
                max_complexity = max(max_complexity, complexity)
        
        # Length factor
        word_count = len(question.split())
        length_factor = min(1.0, word_count / 20.0)  # Normalize to 20 words
        
        # Combine factors
        final_complexity = max(max_complexity, length_factor * 0.3)
        
        return min(1.0, final_complexity)

# Example usage and testing
if __name__ == "__main__":
    print("🧠 SEMANTIC COMPRESSION ENGINE - THE COST OF THINKING")
    print("=" * 60)
    
    engine = LunaSemanticCompressionEngine()
    
    # Test thinking requirement assessment
    test_questions = [
        "Hello",
        "How are you?", 
        "What is artificial intelligence?",
        "Explain quantum mechanics and its philosophical implications",
        "What is the meaning of life, the universe, and everything?"
    ]
    
    current_token_pool = 1000
    
    for question in test_questions:
        context = {"emotional_stakes": 0.3, "response_priority": "moderate"}
        thinking_mode, should_invest = engine.assess_thinking_requirement(question, context, current_token_pool)
        
        print(f"\n📝 Question: '{question}'")
        print(f"   Thinking Mode: {thinking_mode.value}")
        print(f"   Should Invest: {should_invest}")
        print(f"   Upfront Cost: {engine.thinking_costs[thinking_mode].upfront_cost} tokens")
        print(f"   Risk Level: {engine.thinking_costs[thinking_mode].risk_level:.1%}")
        print(f"   Expected Quality Boost: {engine.thinking_costs[thinking_mode].expected_quality_boost:.1%}")
    
    print(f"\n🎯 SEMANTIC COMPRESSION ENGINE: READY FOR INTEGRATION!")
    print("The Cost of Thinking system is operational!")
