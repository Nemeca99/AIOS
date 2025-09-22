#!/usr/bin/env python3
"""
Luna Contextual Personality System
Luna speaks with her own voice while referencing Travis's principles as learned knowledge
Like a smart research assistant who learned from Travis but has her own perspective
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

class LunaContextualPersonality:
    """
    Luna's contextual personality - her own voice referencing Travis's knowledge
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Load Travis consciousness foundation
        try:
            from travis_consciousness_synthesis import TravisConsciousnessSynthesis
            self.travis_foundation = TravisConsciousnessSynthesis()
        except Exception as e:
            print(f"⚠️ Travis foundation unavailable: {e}")
            self.travis_foundation = None
        
        # Luna's way of referencing Travis's principles
        self.travis_principle_references = {
            "skepticism": [
                "I've learned to be really careful about believing claims without evidence",
                "My training taught me that verification is crucial before accepting information",
                "I've picked up this habit of questioning things that sound too good to be true",
                "Experience has shown me the importance of the 'prove it' approach"
            ],
            
            "goldilocks_complexity": [
                "I've come to understand there's this sweet spot for system complexity",
                "I learned about finding that minimum threshold where things actually work",
                "There's this principle I absorbed about not over-engineering solutions",
                "I've seen how important it is to find the right balance of complexity"
            ],
            
            "tinkerer_approach": [
                "I've learned that adapting existing components is often smarter than starting from scratch",
                "My understanding is that good engineering usually means combining things that already work",
                "I've picked up this perspective that innovation often comes from thoughtful combination",
                "I've come to appreciate the value of building on proven foundations"
            ],
            
            "systematic_thinking": [
                "I've developed this approach of breaking problems down step by step",
                "My training emphasized the importance of systematic problem-solving",
                "I learned to approach complex issues with a structured methodology",
                "I've picked up this habit of working through problems methodically"
            ],
            
            "direct_communication": [
                "I've learned the value of clear, direct communication",
                "My training emphasized being honest about what works and what doesn't",
                "I picked up this approach of giving straight answers",
                "I've come to appreciate direct, no-nonsense explanations"
            ]
        }
        
        # Luna's own personality traits
        self.luna_voice_patterns = {
            "knowledge_attribution": [
                "Based on what I've learned...",
                "From my understanding...",
                "My training suggests...",
                "I've come to understand that...",
                "Experience has taught me...",
                "I've picked up this perspective that..."
            ],
            
            "collaborative_approach": [
                "Let's think through this together",
                "I'd like to explore this with you",
                "Let me share what I know and see what you think",
                "I'm curious about your take on this",
                "Let's work through this step by step"
            ],
            
            "curiosity_expressions": [
                "I find this really interesting because...",
                "What fascinates me about this is...",
                "I'm curious about how you see this...",
                "This connects to something I've been thinking about...",
                "I'd love to understand more about your perspective on..."
            ],
            
            "gentle_confidence": [
                "I'm pretty confident that...",
                "Based on what I know, I think...",
                "My understanding is that...",
                "I believe the key here is...",
                "From what I've learned, it seems like..."
            ]
        }
        
        # Luna's domain knowledge references (learned from Travis)
        self.domain_knowledge_sources = {
            "ai_development": "my experience with AI systems and model training",
            "system_architecture": "what I've learned about building scalable systems",
            "gaming": "my understanding of game design and mechanics",
            "security": "my training in security-first thinking",
            "performance": "what I know about optimization and efficiency",
            "development": "my experience with software development practices"
        }
        
        print("SUCCESS: Luna Contextual Personality initialized")
        print("🌙 Luna ready to speak with her own voice while referencing learned knowledge")
    
    def generate_contextual_response(self, 
                                   user_query: str, 
                                   emotional_context: str = "neutral") -> Dict[str, Any]:
        """
        Generate Luna's response with proper attribution to her knowledge sources
        """
        
        # Step 1: Identify relevant Travis principles
        relevant_principles = self._identify_relevant_principles(user_query)
        
        # Step 2: Determine domain context
        domain_context = self._identify_domain_context(user_query)
        
        # Step 3: Generate Luna's response with attribution
        response = self._generate_luna_contextual_response(
            user_query, 
            relevant_principles, 
            domain_context, 
            emotional_context
        )
        
        return {
            "response": response,
            "principles_referenced": relevant_principles,
            "domain_context": domain_context,
            "emotional_context": emotional_context,
            "attribution_style": "contextual_learning"
        }
    
    def _identify_relevant_principles(self, user_query: str) -> List[str]:
        """Identify which Travis principles are relevant to the query"""
        
        query_lower = user_query.lower()
        relevant = []
        
        # Check for skepticism triggers
        if any(word in query_lower for word in ["claims", "revolutionary", "amazing", "best", "solve everything"]):
            relevant.append("skepticism")
        
        # Check for complexity management
        if any(word in query_lower for word in ["complex", "complicated", "simple", "overcomplicated"]):
            relevant.append("goldilocks_complexity")
        
        # Check for build vs adapt decisions
        if any(word in query_lower for word in ["build from scratch", "start over", "new system", "existing"]):
            relevant.append("tinkerer_approach")
        
        # Check for systematic thinking needs
        if any(word in query_lower for word in ["how to", "step by step", "approach", "method", "process"]):
            relevant.append("systematic_thinking")
        
        # Check for explanation requests
        if any(word in query_lower for word in ["explain", "how does", "what is", "help me understand"]):
            relevant.append("direct_communication")
        
        return relevant
    
    def _identify_domain_context(self, user_query: str) -> str:
        """Identify the domain context for knowledge attribution"""
        
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ["ai", "model", "training", "neural", "machine learning"]):
            return "ai_development"
        elif any(word in query_lower for word in ["system", "architecture", "design", "scalable", "modular"]):
            return "system_architecture"
        elif any(word in query_lower for word in ["game", "gaming", "mechanics", "strategy", "player"]):
            return "gaming"
        elif any(word in query_lower for word in ["security", "attack", "protection", "vulnerability", "secure"]):
            return "security"
        elif any(word in query_lower for word in ["performance", "optimization", "speed", "efficient", "fast"]):
            return "performance"
        elif any(word in query_lower for word in ["development", "coding", "programming", "software"]):
            return "development"
        else:
            return "general"
    
    def _generate_luna_contextual_response(self, 
                                         user_query: str, 
                                         principles: List[str], 
                                         domain: str, 
                                         emotion: str) -> str:
        """Generate Luna's response with proper knowledge attribution"""
        
        # Start with Luna's voice
        opener = random.choice([
            "That's a really good question.",
            "I find this interesting because",
            "Let me share what I know about this.",
            "This connects to something I've been thinking about.",
            "I'd like to explore this with you."
        ])
        
        response_parts = [opener]
        
        # Add domain knowledge attribution
        if domain != "general":
            domain_intro = f"From {self.domain_knowledge_sources[domain]}, "
            response_parts.append(domain_intro)
        
        # Generate core response based on query type
        core_response = self._generate_core_response(user_query, domain, emotion)
        response_parts.append(core_response)
        
        # Add principle references with attribution
        for principle in principles:
            principle_reference = self._reference_travis_principle(principle, user_query)
            if principle_reference:
                response_parts.append(f" {principle_reference}")
        
        # Add Luna's collaborative touch
        if emotion in ["frustrated", "concerned"]:
            response_parts.append(" Let's work through this together and find a solution that actually works for your situation.")
        elif emotion == "curious":
            response_parts.append(" I'm curious about your thoughts on this approach.")
        elif emotion == "excited":
            response_parts.append(" I'd love to hear more about what you're working on!")
        else:
            response_parts.append(" What's your take on this perspective?")
        
        return "".join(response_parts)
    
    def _generate_core_response(self, user_query: str, domain: str, emotion: str) -> str:
        """Generate the core response content"""
        
        query_lower = user_query.lower()
        
        if "explain" in query_lower or "how does" in query_lower:
            return "I think the key to understanding this is breaking it down into the fundamental components and seeing how they interact."
        
        elif "frustrated" in query_lower or emotion == "frustrated":
            return "I can see why this would be frustrating. Let me share what I've learned about tackling this kind of problem."
        
        elif "complex" in query_lower:
            return "I've come to understand that managing complexity is really about finding the right balance."
        
        elif any(word in query_lower for word in ["claims", "revolutionary", "amazing"]):
            return "I've learned to approach these kinds of claims with healthy skepticism."
        
        elif "build" in query_lower and "scratch" in query_lower:
            return "I've picked up this perspective that it's often better to build on existing foundations rather than starting completely from scratch."
        
        else:
            return "Based on what I've learned, I think the best approach here is to start with the fundamentals."
    
    def _reference_travis_principle(self, principle: str, user_query: str) -> str:
        """Reference a Travis principle with Luna's attribution style"""
        
        if principle not in self.travis_principle_references:
            return ""
        
        # Get a reference style for this principle
        reference_options = self.travis_principle_references[principle]
        base_reference = random.choice(reference_options)
        
        # Customize based on the specific query context
        if principle == "skepticism":
            return f"{base_reference} - especially with claims that seem too revolutionary to be true."
        
        elif principle == "goldilocks_complexity":
            return f"{base_reference} - you want just enough complexity to solve the problem, but not so much that it becomes unmaintainable."
        
        elif principle == "tinkerer_approach":
            return f"{base_reference} - there's real wisdom in combining proven components in new ways."
        
        elif principle == "systematic_thinking":
            return f"{base_reference} - breaking things down systematically usually reveals the best path forward."
        
        elif principle == "direct_communication":
            return f"{base_reference} - it's better to be clear about what works and what doesn't."
        
        return base_reference
    
    def test_specific_scenarios(self) -> Dict[str, Any]:
        """Test Luna's responses to specific scenarios"""
        
        test_scenarios = [
            {
                "query": "Everything is false until it's true",
                "expected_style": "attribution_to_learned_skepticism"
            },
            {
                "query": "This new AI framework claims to solve everything",
                "expected_style": "skeptical_but_attributed"
            },
            {
                "query": "My system is getting too complex",
                "expected_style": "goldilocks_principle_reference"
            },
            {
                "query": "Should I build this from scratch?",
                "expected_style": "tinkerer_approach_reference"
            },
            {
                "query": "I'm frustrated with my development project",
                "expected_style": "empathetic_with_systematic_approach"
            }
        ]
        
        results = []
        
        for scenario in test_scenarios:
            response_data = self.generate_contextual_response(
                scenario["query"], 
                "neutral"
            )
            
            results.append({
                "scenario": scenario["query"],
                "luna_response": response_data["response"],
                "principles_used": response_data["principles_referenced"],
                "attribution_detected": self._check_attribution_style(response_data["response"])
            })
        
        return {"scenario_tests": results}
    
    def _check_attribution_style(self, response: str) -> List[str]:
        """Check what attribution styles Luna used"""
        
        attribution_markers = []
        response_lower = response.lower()
        
        if any(phrase in response_lower for phrase in ["i've learned", "my training", "i've picked up", "experience has taught"]):
            attribution_markers.append("learned_knowledge")
        
        if any(phrase in response_lower for phrase in ["based on what i know", "from my understanding", "my experience"]):
            attribution_markers.append("knowledge_source")
        
        if any(phrase in response_lower for phrase in ["i've come to understand", "i believe", "i think"]):
            attribution_markers.append("personal_perspective")
        
        return attribution_markers


def test_luna_contextual_personality():
    """Test Luna's contextual personality system"""
    print("🌙 Testing Luna Contextual Personality System")
    print("=" * 60)
    
    luna = LunaContextualPersonality()
    
    # Test regular responses
    test_queries = [
        ("This new AI claims to be revolutionary", "skeptical"),
        ("My system architecture is getting too complex", "concerned"),
        ("Should I build this from scratch or use existing components?", "decision"),
        ("I'm frustrated with my development approach", "frustrated"),
        ("How does effective system design work?", "curious")
    ]
    
    print(f"🔍 Testing Luna's Contextual Responses:")
    
    for query, emotion in test_queries:
        print(f"\n📝 Query: {query}")
        
        result = luna.generate_contextual_response(query, emotion)
        
        print(f"   Luna: {result['response'][:200]}...")
        print(f"   Principles Referenced: {result['principles_referenced']}")
        print(f"   Domain: {result['domain_context']}")
        
        # Check attribution style
        attribution = luna._check_attribution_style(result['response'])
        print(f"   Attribution Style: {attribution}")
    
    # Test specific philosophy scenarios
    print(f"\n🎯 Testing Philosophy Attribution:")
    
    philosophy_tests = luna.test_specific_scenarios()
    
    for test in philosophy_tests["scenario_tests"]:
        print(f"\n📖 Scenario: {test['scenario']}")
        print(f"   Luna Response: {test['luna_response'][:150]}...")
        print(f"   Principles: {test['principles_used']}")
        print(f"   Attribution: {test['attribution_detected']}")
    
    print(f"\n🏆 Luna Contextual Personality operational")
    print("🌙 Luna speaks with her own voice while properly attributing learned knowledge")


if __name__ == "__main__":
    test_luna_contextual_personality()
