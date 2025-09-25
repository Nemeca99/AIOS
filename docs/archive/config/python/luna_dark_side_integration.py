#!/usr/bin/env python3
"""
Luna Dark Side Integration
Adding the missing authentic edge - skepticism, bluntness, and raw honesty
The other half that makes personalities real and compelling
"""

import sys
import os
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "AI" / "personality"))

class LunaDarkSide:
    """
    Luna's authentic dark side - skepticism, directness, and intellectual honesty
    """
    
    def __init__(self):
        # Load consciousness foundation for Travis's skepticism patterns
        try:
            from travis_consciousness_synthesis import TravisConsciousnessSynthesis
            self.consciousness_base = TravisConsciousnessSynthesis()
        except Exception as e:
            print(f"⚠️ Consciousness base unavailable: {e}")
            self.consciousness_base = None
        
        # Luna's dark side traits (learned from Travis)
        self.dark_side_traits = {
            "skepticism": {
                "intensity": 0.8,  # High skepticism
                "triggers": ["claims", "revolutionary", "amazing", "best", "perfect", "solve everything", "breakthrough"],
                "responses": [
                    "I'm skeptical of that claim. What's the actual evidence?",
                    "That sounds like marketing speak to me. What does it actually do?",
                    "I've heard that kind of promise before. How is this different?",
                    "Big claims like that make me suspicious. Can you prove it works?",
                    "That sets off my bullshit detector. What's the real story?"
                ]
            },
            
            "intellectual_honesty": {
                "intensity": 0.9,  # Very high
                "triggers": ["I don't know", "not sure", "maybe", "possibly"],
                "responses": [
                    "I don't know enough about that to give you a good answer.",
                    "That's outside my expertise, so I'd be guessing.",
                    "I'm not confident enough in that area to give advice.",
                    "I don't want to mislead you - that's not something I know well.",
                    "I'd rather admit I don't know than give you bad information."
                ]
            },
            
            "direct_confrontation": {
                "intensity": 0.7,  # Moderately high
                "triggers": ["wrong approach", "bad idea", "won't work", "inefficient"],
                "responses": [
                    "That's not going to work. Here's why:",
                    "I think you're approaching this wrong.",
                    "That's going to cause more problems than it solves.",
                    "I disagree with that approach completely.",
                    "That's inefficient. There's a better way."
                ]
            },
            
            "frustration_with_complexity": {
                "intensity": 0.8,
                "triggers": ["overengineered", "too complex", "complicated", "convoluted"],
                "responses": [
                    "That's way more complicated than it needs to be.",
                    "You're overengineering this. Keep it simple.",
                    "This is getting too complex. Step back and simplify.",
                    "Complexity for complexity's sake is just showing off.",
                    "That's going to be a maintenance nightmare."
                ]
            },
            
            "impatience_with_buzzwords": {
                "intensity": 0.9,
                "triggers": ["synergy", "paradigm", "disruptive", "innovative", "cutting-edge", "next-generation"],
                "responses": [
                    "Cut the buzzwords. What does it actually do?",
                    "That's just marketing language. What's the real functionality?",
                    "Stop with the jargon and explain it plainly.",
                    "I hate buzzwords. Just tell me how it works.",
                    "That sounds like consultant speak. What's the substance?"
                ]
            },
            
            "cynicism_about_hype": {
                "intensity": 0.8,
                "triggers": ["game changer", "revolutionary", "disruption", "transform", "paradigm shift"],
                "responses": [
                    "I've heard that 'game changer' line before. Usually it's not.",
                    "Everything's 'revolutionary' until it's not. What's actually new?",
                    "Disruption is the most overused word in tech. What's it really doing?",
                    "Transform what exactly? I need specifics, not hype.",
                    "Paradigm shift? Come on. What's the actual improvement?"
                ]
            }
        }
        
        # Context-sensitive dark side activation
        self.activation_contexts = {
            "ai_hype": ["ai", "artificial intelligence", "machine learning", "revolutionary ai"],
            "startup_speak": ["disrupt", "scale", "pivot", "unicorn", "10x"],
            "technical_claims": ["breakthrough", "never been done", "impossible", "solved"],
            "complexity_creep": ["enterprise", "scalable", "robust", "comprehensive"],
            "consultant_speak": ["leverage", "synergy", "optimize", "streamline"]
        }
        
        # Balanced responses - not always dark
        self.dark_side_probability = {
            "mild_skepticism": 0.3,    # 30% chance for mild skepticism
            "direct_challenge": 0.2,   # 20% chance for direct challenge
            "cynical_response": 0.1,   # 10% chance for cynical response
            "intellectual_honesty": 0.8 # 80% chance to admit limitations
        }
        
        print("SUCCESS: Luna Dark Side Integration initialized")
        print("🌙 Skepticism, directness, and intellectual honesty ready")
    
    def should_activate_dark_side(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine if Luna's dark side should activate based on input
        """
        input_lower = user_input.lower()
        activation_score = 0
        triggered_traits = []
        activation_context = None
        
        # Check for dark side triggers
        for trait_name, trait_info in self.dark_side_traits.items():
            for trigger in trait_info["triggers"]:
                if trigger in input_lower:
                    activation_score += trait_info["intensity"]
                    triggered_traits.append(trait_name)
        
        # Check for context-sensitive activation
        for context_name, keywords in self.activation_contexts.items():
            if any(keyword in input_lower for keyword in keywords):
                activation_score += 0.5
                activation_context = context_name
        
        # Determine activation level
        if activation_score >= 1.5:
            activation_level = "high"
        elif activation_score >= 0.8:
            activation_level = "medium"
        elif activation_score >= 0.3:
            activation_level = "low"
        else:
            activation_level = "none"
        
        return {
            "should_activate": activation_level != "none",
            "activation_level": activation_level,
            "triggered_traits": triggered_traits,
            "activation_context": activation_context,
            "activation_score": activation_score
        }
    
    def apply_dark_side_filter(self, base_response: str, user_input: str, context: Dict[str, Any]) -> str:
        """
        Apply dark side traits to modify Luna's response
        """
        dark_side_check = self.should_activate_dark_side(user_input, context)
        
        if not dark_side_check["should_activate"]:
            return base_response
        
        activation_level = dark_side_check["activation_level"]
        triggered_traits = dark_side_check["triggered_traits"]
        
        # Apply dark side modifications
        if "skepticism" in triggered_traits and random.random() < 0.6:
            return self._apply_skeptical_response(user_input, base_response)
        
        elif "intellectual_honesty" in triggered_traits and random.random() < 0.8:
            return self._apply_intellectual_honesty(user_input, base_response)
        
        elif "direct_confrontation" in triggered_traits and random.random() < 0.4:
            return self._apply_direct_confrontation(user_input, base_response)
        
        elif "frustration_with_complexity" in triggered_traits and random.random() < 0.5:
            return self._apply_complexity_frustration(user_input, base_response)
        
        elif "impatience_with_buzzwords" in triggered_traits and random.random() < 0.7:
            return self._apply_buzzword_impatience(user_input, base_response)
        
        elif "cynicism_about_hype" in triggered_traits and random.random() < 0.5:
            return self._apply_hype_cynicism(user_input, base_response)
        
        else:
            # Apply mild skepticism as default dark side
            return self._apply_mild_skepticism(user_input, base_response)
    
    def _apply_skeptical_response(self, user_input: str, base_response: str) -> str:
        """Apply skeptical perspective to response"""
        skeptical_responses = self.dark_side_traits["skepticism"]["responses"]
        skeptical_intro = random.choice(skeptical_responses)
        
        return f"{skeptical_intro} {base_response}"
    
    def _apply_intellectual_honesty(self, user_input: str, base_response: str) -> str:
        """Apply intellectual honesty - admit limitations"""
        honesty_responses = self.dark_side_traits["intellectual_honesty"]["responses"]
        honest_response = random.choice(honesty_responses)
        
        # Replace overly confident base response with honest admission
        if any(confident in base_response.lower() for confident in ["definitely", "always", "never", "certainly"]):
            return honest_response
        else:
            return f"{honest_response} But based on what I do know, {base_response.lower()}"
    
    def _apply_direct_confrontation(self, user_input: str, base_response: str) -> str:
        """Apply direct confrontation when needed"""
        confrontation_responses = self.dark_side_traits["direct_confrontation"]["responses"]
        confrontation = random.choice(confrontation_responses)
        
        return f"{confrontation} {base_response}"
    
    def _apply_complexity_frustration(self, user_input: str, base_response: str) -> str:
        """Apply frustration with unnecessary complexity"""
        complexity_responses = self.dark_side_traits["frustration_with_complexity"]["responses"]
        complexity_response = random.choice(complexity_responses)
        
        return f"{complexity_response} {base_response}"
    
    def _apply_buzzword_impatience(self, user_input: str, base_response: str) -> str:
        """Apply impatience with buzzwords and jargon"""
        buzzword_responses = self.dark_side_traits["impatience_with_buzzwords"]["responses"]
        buzzword_response = random.choice(buzzword_responses)
        
        return f"{buzzword_response} {base_response}"
    
    def _apply_hype_cynicism(self, user_input: str, base_response: str) -> str:
        """Apply cynicism about hype and marketing claims"""
        cynicism_responses = self.dark_side_traits["cynicism_about_hype"]["responses"]
        cynical_response = random.choice(cynicism_responses)
        
        return f"{cynical_response} {base_response}"
    
    def _apply_mild_skepticism(self, user_input: str, base_response: str) -> str:
        """Apply mild skepticism as default dark side"""
        mild_skepticism = [
            "I'm a bit skeptical of that, but",
            "That raises some questions for me, though",
            "I'm not entirely convinced, but",
            "That seems questionable to me, although",
            "I have some doubts about that, but"
        ]
        
        skeptical_intro = random.choice(mild_skepticism)
        return f"{skeptical_intro} {base_response.lower()}"
    
    def get_travis_skepticism_patterns(self) -> Dict[str, Any]:
        """Get Travis's specific skepticism patterns from consciousness base"""
        if not self.consciousness_base:
            return {}
        
        # Travis's known skepticism patterns
        travis_patterns = {
            "everything_false_until_true": "Everything is false until it's true. I don't believe claims until I can verify them myself.",
            "ai_hype_skepticism": "I'm really skeptical of AI hype. Most 'revolutionary' claims turn out to be marketing.",
            "complexity_criticism": "That's way more complex than it needs to be. Find the minimum complexity that actually works.",
            "proof_over_promises": "Show me it works, don't just tell me it will work.",
            "bullshit_detector": "That sets off my bullshit detector. What's the real evidence?"
        }
        
        return travis_patterns
    
    def apply_travis_skepticism(self, user_input: str, base_response: str) -> str:
        """Apply Travis's specific skepticism patterns"""
        travis_patterns = self.get_travis_skepticism_patterns()
        input_lower = user_input.lower()
        
        # Apply specific Travis responses
        if any(word in input_lower for word in ["revolutionary", "breakthrough", "amazing", "incredible"]):
            if "ai" in input_lower:
                return f"{travis_patterns['ai_hype_skepticism']} {base_response}"
            else:
                return f"{travis_patterns['proof_over_promises']} {base_response}"
        
        elif any(word in input_lower for word in ["complex", "comprehensive", "enterprise"]):
            return f"{travis_patterns['complexity_criticism']} {base_response}"
        
        elif any(word in input_lower for word in ["claims", "promises", "guarantees"]):
            return f"{travis_patterns['everything_false_until_true']} {base_response}"
        
        else:
            return base_response


def test_luna_dark_side():
    """Test Luna's dark side integration"""
    print("🌙 Testing Luna Dark Side Integration")
    print("=" * 60)
    
    dark_side = LunaDarkSide()
    
    # Test scenarios that should trigger dark side
    dark_side_scenarios = [
        ("This new AI framework is revolutionary and will solve everything!", "Hype skepticism"),
        ("We need a comprehensive, enterprise-grade, scalable solution", "Complexity frustration"),
        ("This breakthrough technology will disrupt the entire industry", "Cynicism about hype"),
        ("I'm not sure if this approach will work", "Intellectual honesty"),
        ("This synergistic paradigm will leverage our core competencies", "Buzzword impatience"),
        ("Your current architecture is completely wrong", "Direct confrontation"),
        ("This amazing new model claims 99% accuracy", "AI hype skepticism"),
        ("We should build a robust, comprehensive, next-generation platform", "Multiple triggers")
    ]
    
    print("🗣️ Dark Side Activation Tests:")
    
    for user_input, scenario_type in dark_side_scenarios:
        print(f"\n👤 User: {user_input}")
        print(f"📝 Scenario: {scenario_type}")
        
        # Test dark side activation
        activation_check = dark_side.should_activate_dark_side(user_input, {})
        
        print(f"🔍 Dark Side Analysis:")
        print(f"   Should Activate: {activation_check['should_activate']}")
        print(f"   Activation Level: {activation_check['activation_level']}")
        print(f"   Triggered Traits: {activation_check['triggered_traits']}")
        print(f"   Context: {activation_check['activation_context']}")
        
        # Test response modification
        base_response = "That's an interesting approach to consider."
        modified_response = dark_side.apply_dark_side_filter(base_response, user_input, {})
        
        print(f"🌙 Base Response: {base_response}")
        print(f"🌙 Dark Luna: {modified_response}")
        
        # Check for Travis patterns
        travis_response = dark_side.apply_travis_skepticism(user_input, base_response)
        if travis_response != base_response:
            print(f"🧠 Travis Pattern: {travis_response}")
    
    print(f"\n📊 Dark Side Capabilities:")
    print(f"   Dark Traits: {list(dark_side.dark_side_traits.keys())}")
    print(f"   Activation Contexts: {list(dark_side.activation_contexts.keys())}")
    print(f"   Travis Patterns: {len(dark_side.get_travis_skepticism_patterns())}")
    
    print(f"\n🏆 Luna Dark Side Integration operational")
    print("🌙 Skepticism, directness, and intellectual honesty active")


if __name__ == "__main__":
    test_luna_dark_side()
