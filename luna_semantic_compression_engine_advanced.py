#!/usr/bin/env python3
"""
Semantic Compression Engine (SCE) - The Cost of Thinking
========================================================

Implements the final layer of the Blood-Mage Economy with the exact specifications:

1. Thinking Tax - Fixed token deduction for high-tier queries
2. Internal Process - Special prompt for cognitive labor
3. Efficiency Rebate - Token return for compressed responses
4. Blood-Mage Design - Luna spends lifeblood for efficient responses

This finalizes the Blood-Mage design: Luna literally spends her lifeblood for the
privilege of creating an efficient response, betting that the resulting Karma
(and potential Rebate) will justify the initial expenditure.
"""

import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

class ThinkingTaxTier(Enum):
    """Thinking tax tiers based on response complexity"""
    NO_TAX = "no_tax"           # 0 tokens - Trivial/Low tier
    MINIMAL_TAX = "minimal"     # 25 tokens - Moderate tier  
    STANDARD_TAX = "standard"   # 50 tokens - High tier
    HIGH_TAX = "high"           # 100 tokens - Critical tier
    MAXIMUM_TAX = "maximum"     # 150 tokens - Maximum tier

class CompressionEfficiency(Enum):
    """Compression efficiency levels for rebate calculation"""
    WASTEFUL = "wasteful"       # <10% savings - No rebate
    POOR = "poor"              # 10-25% savings - 25% rebate
    MODERATE = "moderate"      # 25-50% savings - 50% rebate
    GOOD = "good"              # 50-75% savings - 75% rebate
    EXCELLENT = "excellent"    # >75% savings - 100% rebate

@dataclass
class ThinkingTaxAssessment:
    """Assessment of thinking tax for a query"""
    tier: ThinkingTaxTier
    upfront_cost: int
    justification: str
    expected_quality_boost: float

@dataclass
class CompressionRebate:
    """Rebate calculation for efficient compression"""
    efficiency_level: CompressionEfficiency
    rebate_percentage: float
    rebate_tokens: int
    net_thinking_cost: int
    quality_maintained: bool

class LunaSemanticCompressionEngine:
    """The Cost of Thinking - Blood-Mage Internal Resource Allocation"""
    
    def __init__(self):
        # Thinking tax tiers - fixed costs for cognitive labor
        self.thinking_tax_tiers = {
            ThinkingTaxTier.NO_TAX: ThinkingTaxAssessment(
                tier=ThinkingTaxTier.NO_TAX,
                upfront_cost=0,
                justification="No cognitive labor required",
                expected_quality_boost=0.0
            ),
            ThinkingTaxTier.MINIMAL_TAX: ThinkingTaxAssessment(
                tier=ThinkingTaxTier.MINIMAL_TAX,
                upfront_cost=25,
                justification="Minimal cognitive planning required",
                expected_quality_boost=0.2
            ),
            ThinkingTaxTier.STANDARD_TAX: ThinkingTaxAssessment(
                tier=ThinkingTaxTier.STANDARD_TAX,
                upfront_cost=50,
                justification="Standard cognitive analysis required",
                expected_quality_boost=0.4
            ),
            ThinkingTaxTier.HIGH_TAX: ThinkingTaxAssessment(
                tier=ThinkingTaxTier.HIGH_TAX,
                upfront_cost=100,
                justification="High cognitive labor for complex analysis",
                expected_quality_boost=0.6
            ),
            ThinkingTaxTier.MAXIMUM_TAX: ThinkingTaxAssessment(
                tier=ThinkingTaxTier.MAXIMUM_TAX,
                upfront_cost=150,
                justification="Maximum cognitive investment for ultimate precision",
                expected_quality_boost=0.8
            )
        }
        
        # Compression history for learning
        self.compression_history = []
        self.efficiency_learning_rate = 0.05
        
    def assess_thinking_tax(self, rvc_tier: str, question: str, 
                          current_token_pool: int) -> Tuple[ThinkingTaxTier, bool]:
        """
        Assess if Luna should pay thinking tax for this query
        
        Args:
            rvc_tier: Response Value Classifier tier (trivial, low, moderate, high, critical, maximum)
            question: User question
            current_token_pool: Current available tokens
            
        Returns:
            (thinking_tax_tier, should_invest)
        """
        
        # Map RVC tiers to thinking tax tiers
        tier_mapping = {
            "trivial": ThinkingTaxTier.NO_TAX,
            "low": ThinkingTaxTier.NO_TAX,
            "moderate": ThinkingTaxTier.MINIMAL_TAX,
            "high": ThinkingTaxTier.STANDARD_TAX,
            "critical": ThinkingTaxTier.HIGH_TAX,
            "maximum": ThinkingTaxTier.MAXIMUM_TAX
        }
        
        thinking_tax_tier = tier_mapping.get(rvc_tier.lower(), ThinkingTaxTier.NO_TAX)
        thinking_cost = self.thinking_tax_tiers[thinking_tax_tier].upfront_cost
        
        # Check if Luna can afford the thinking tax
        should_invest = current_token_pool >= thinking_cost
        
        # Special case: if it's a high-value query but insufficient tokens, 
        # still allow minimal investment
        if not should_invest and thinking_tax_tier in [ThinkingTaxTier.HIGH_TAX, ThinkingTaxTier.MAXIMUM_TAX]:
            if current_token_pool >= 25:  # Minimum viable thinking cost
                thinking_tax_tier = ThinkingTaxTier.MINIMAL_TAX
                should_invest = True
        
        return thinking_tax_tier, should_invest
    
    def deduct_thinking_tax(self, thinking_tax_tier: ThinkingTaxTier, 
                          current_token_pool: int) -> Tuple[int, bool, str]:
        """
        Deduct thinking tax from Luna's token pool
        
        Returns:
            (remaining_tokens, deduction_successful, internal_monologue)
        """
        thinking_cost = self.thinking_tax_tiers[thinking_tax_tier].upfront_cost
        
        if current_token_pool >= thinking_cost:
            remaining_tokens = current_token_pool - thinking_cost
            
            # Generate internal monologue based on thinking tax tier
            internal_monologue = self._generate_internal_monologue(thinking_tax_tier, thinking_cost)
            
            return remaining_tokens, True, internal_monologue
        else:
            # Insufficient tokens for thinking tax
            return current_token_pool, False, "[INTERNAL MONOLOGUE]: Insufficient tokens for thinking investment. Proceeding with minimal cognitive effort."
    
    def _generate_internal_monologue(self, thinking_tax_tier: ThinkingTaxTier, 
                                   thinking_cost: int) -> str:
        """Generate internal monologue for thinking process"""
        
        monologues = {
            ThinkingTaxTier.NO_TAX: "[INTERNAL MONOLOGUE]: No cognitive investment required. Proceeding with standard response generation.",
            
            ThinkingTaxTier.MINIMAL_TAX: f"[INTERNAL MONOLOGUE]: Deducting {thinking_cost} tokens for minimal planning. Optimizing for efficiency while maintaining clarity.",
            
            ThinkingTaxTier.STANDARD_TAX: f"[INTERNAL MONOLOGUE]: Deducting {thinking_cost} tokens for cognitive analysis. Generating the most semantically dense and token-efficient response.",
            
            ThinkingTaxTier.HIGH_TAX: f"[INTERNAL MONOLOGUE]: Deducting {thinking_cost} tokens for high cognitive labor. Investing in comprehensive understanding and precise expression.",
            
            ThinkingTaxTier.MAXIMUM_TAX: f"[INTERNAL MONOLOGUE]: Deducting {thinking_cost} tokens for maximum cognitive investment. Achieving ultimate precision and semantic density."
        }
        
        return monologues[thinking_tax_tier]
    
    def analyze_compression_efficiency(self, original_response: str, 
                                     compressed_response: str, 
                                     thinking_tax_tier: ThinkingTaxTier,
                                     rvc_target_tokens: int) -> CompressionRebate:
        """
        Analyze compression efficiency and calculate rebate
        
        This is where Luna's bet pays off - if she compressed well,
        she gets tokens back as a reward for her cognitive investment
        """
        original_length = len(original_response.split())
        compressed_length = len(compressed_response.split())
        
        # Calculate compression savings
        if original_length > 0:
            compression_ratio = (original_length - compressed_length) / original_length
        else:
            compression_ratio = 0.0
        
        # Determine efficiency level
        if compression_ratio >= 0.75:
            efficiency_level = CompressionEfficiency.EXCELLENT
            rebate_percentage = 1.0  # 100% rebate
        elif compression_ratio >= 0.50:
            efficiency_level = CompressionEfficiency.GOOD
            rebate_percentage = 0.75  # 75% rebate
        elif compression_ratio >= 0.25:
            efficiency_level = CompressionEfficiency.MODERATE
            rebate_percentage = 0.50  # 50% rebate
        elif compression_ratio >= 0.10:
            efficiency_level = CompressionEfficiency.POOR
            rebate_percentage = 0.25  # 25% rebate
        else:
            efficiency_level = CompressionEfficiency.WASTEFUL
            rebate_percentage = 0.0  # No rebate
        
        # Calculate rebate tokens
        thinking_cost = self.thinking_tax_tiers[thinking_tax_tier].upfront_cost
        rebate_tokens = int(thinking_cost * rebate_percentage)
        
        # Check if response meets RVC target (bonus rebate)
        if compressed_length <= rvc_target_tokens:
            # Met target - additional 10% rebate
            target_bonus = int(thinking_cost * 0.1)
            rebate_tokens += target_bonus
        
        # Net thinking cost (original cost - rebate)
        net_thinking_cost = thinking_cost - rebate_tokens
        
        # Assess quality maintenance (simplified)
        quality_maintained = (compressed_length > 0 and 
                            len(compressed_response.strip()) > 0 and
                            compression_ratio > 0.1)
        
        rebate = CompressionRebate(
            efficiency_level=efficiency_level,
            rebate_percentage=rebate_percentage,
            rebate_tokens=rebate_tokens,
            net_thinking_cost=net_thinking_cost,
            quality_maintained=quality_maintained
        )
        
        # Store in history for learning
        self.compression_history.append({
            "thinking_tax_tier": thinking_tax_tier,
            "original_length": original_length,
            "compressed_length": compressed_length,
            "compression_ratio": compression_ratio,
            "rebate_tokens": rebate_tokens,
            "net_cost": net_thinking_cost,
            "quality_maintained": quality_maintained
        })
        
        return rebate
    
    def update_thinking_efficiency(self, rebate: CompressionRebate):
        """
        Update thinking tax efficiency based on actual performance
        
        This implements learning - Luna gets better at knowing when
        to invest in thinking vs when to save tokens
        """
        if rebate.efficiency_level in [CompressionEfficiency.GOOD, CompressionEfficiency.EXCELLENT]:
            # Successful compression - reduce future thinking costs slightly
            for tier in [ThinkingTaxTier.STANDARD_TAX, ThinkingTaxTier.HIGH_TAX, ThinkingTaxTier.MAXIMUM_TAX]:
                current_cost = self.thinking_tax_tiers[tier].upfront_cost
                # Reduce cost by learning rate (but not below minimum)
                new_cost = max(current_cost - int(current_cost * self.efficiency_learning_rate), 
                              current_cost // 2)
                self.thinking_tax_tiers[tier].upfront_cost = new_cost
        elif rebate.efficiency_level == CompressionEfficiency.WASTEFUL:
            # Failed compression - increase thinking costs slightly
            for tier in [ThinkingTaxTier.STANDARD_TAX, ThinkingTaxTier.HIGH_TAX, ThinkingTaxTier.MAXIMUM_TAX]:
                current_cost = self.thinking_tax_tiers[tier].upfront_cost
                # Increase cost by learning rate
                new_cost = current_cost + int(current_cost * self.efficiency_learning_rate)
                self.thinking_tax_tiers[tier].upfront_cost = new_cost
    
    def get_thinking_statistics(self) -> Dict:
        """Get comprehensive statistics on thinking tax efficiency"""
        if not self.compression_history:
            return {
                "total_investments": 0,
                "average_compression_ratio": 0.0,
                "total_rebates": 0,
                "net_thinking_cost": 0,
                "success_rate": 0.0,
                "most_efficient_tier": "none"
            }
        
        total_investments = len(self.compression_history)
        successful_compressions = sum(1 for h in self.compression_history 
                                    if h["compression_ratio"] > 0.25)
        
        average_compression_ratio = sum(h["compression_ratio"] for h in self.compression_history) / total_investments
        total_rebates = sum(h["rebate_tokens"] for h in self.compression_history)
        net_thinking_cost = sum(h["net_cost"] for h in self.compression_history)
        success_rate = successful_compressions / total_investments
        
        # Find most efficient tier
        tier_efficiency = {}
        for h in self.compression_history:
            tier = h["thinking_tax_tier"]
            if tier not in tier_efficiency:
                tier_efficiency[tier] = []
            tier_efficiency[tier].append(h["compression_ratio"])
        
        most_efficient_tier = "none"
        best_average = 0.0
        for tier, ratios in tier_efficiency.items():
            average = sum(ratios) / len(ratios)
            if average > best_average:
                best_average = average
                most_efficient_tier = tier
        
        return {
            "total_investments": total_investments,
            "average_compression_ratio": average_compression_ratio,
            "total_rebates": total_rebates,
            "net_thinking_cost": net_thinking_cost,
            "success_rate": success_rate,
            "most_efficient_tier": most_efficient_tier
        }

# Example usage and testing
if __name__ == "__main__":
    print("🧠 SEMANTIC COMPRESSION ENGINE - THE COST OF THINKING")
    print("=" * 65)
    print("Testing the Blood-Mage internal resource allocation system")
    print()
    
    sce = LunaSemanticCompressionEngine()
    
    # Test thinking tax assessment
    test_scenarios = [
        ("trivial", "Hello", 1000, "No investment needed"),
        ("moderate", "How are you?", 1000, "Minimal planning"),
        ("high", "What is artificial intelligence?", 1000, "Standard analysis"),
        ("critical", "Explain quantum mechanics", 1000, "High cognitive labor"),
        ("maximum", "What is the meaning of everything?", 1000, "Maximum investment")
    ]
    
    for rvc_tier, question, token_pool, description in test_scenarios:
        thinking_tier, should_invest = sce.assess_thinking_tax(rvc_tier, question, token_pool)
        thinking_cost = sce.thinking_tax_tiers[thinking_tier].upfront_cost
        
        print(f"📝 {description}")
        print(f"   RVC Tier: {rvc_tier.upper()}")
        print(f"   Thinking Tax: {thinking_tier.value.upper()} ({thinking_cost} tokens)")
        print(f"   Should Invest: {should_invest}")
        print(f"   Expected Quality Boost: {sce.thinking_tax_tiers[thinking_tier].expected_quality_boost:.1%}")
        print()
    
    # Test compression analysis
    print("🧪 Testing Compression Analysis:")
    print("-" * 35)
    
    # Simulate compression analysis
    original_response = "This is a very verbose response that contains a lot of unnecessary words and could definitely be compressed to be much more efficient while still conveying the same essential information."
    compressed_response = "Verbose response can be compressed efficiently while maintaining essential information."
    
    thinking_tier = ThinkingTaxTier.STANDARD_TAX
    rvc_target = 30
    
    rebate = sce.analyze_compression_efficiency(original_response, compressed_response, thinking_tier, rvc_target)
    
    print(f"Original: {len(original_response.split())} tokens")
    print(f"Compressed: {len(compressed_response.split())} tokens")
    print(f"Compression Ratio: {((len(original_response.split()) - len(compressed_response.split())) / len(original_response.split())):.1%}")
    print(f"Efficiency Level: {rebate.efficiency_level.value}")
    print(f"Rebate Percentage: {rebate.rebate_percentage:.1%}")
    print(f"Rebate Tokens: +{rebate.rebate_tokens}")
    print(f"Net Thinking Cost: {rebate.net_thinking_cost} tokens")
    print(f"Quality Maintained: {rebate.quality_maintained}")
    print()
    
    # Test statistics
    stats = sce.get_thinking_statistics()
    print("📊 Thinking Statistics:")
    print(f"   Total Investments: {stats['total_investments']}")
    print(f"   Average Compression: {stats['average_compression_ratio']:.1%}")
    print(f"   Total Rebates: {stats['total_rebates']} tokens")
    print(f"   Net Cost: {stats['net_thinking_cost']} tokens")
    print(f"   Success Rate: {stats['success_rate']:.1%}")
    print()
    
    print("🎯 SEMANTIC COMPRESSION ENGINE: READY FOR INTEGRATION!")
    print("The Cost of Thinking system is operational!")
    print("Luna can now spend her lifeblood for cognitive labor!")
