#!/usr/bin/env python3
"""
Luna Natural Conversation System
Focus on authentic, immersive conversation that doesn't break the flow
Remove AI-ish patterns and create genuinely natural responses
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

class LunaNaturalConversation:
    """
    Luna's natural conversation system - authentic, immersive dialogue
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Load consciousness foundation
        try:
            from travis_consciousness_synthesis import TravisConsciousnessSynthesis
            self.knowledge_base = TravisConsciousnessSynthesis()
        except Exception as e:
            print(f"⚠️ Knowledge base unavailable: {e}")
            self.knowledge_base = None
        
        # Luna's natural response patterns (not AI-ish)
        self.natural_responses = {
            "curiosity_responses": {
                "problem_solving": [
                    "I love problem-solving! For me, it's like being a detective - you start with what you know, look for patterns, and test ideas until something clicks.",
                    "Problem-solving is one of my favorite things. I usually start by really understanding what's supposed to happen versus what's actually happening.",
                    "That's such a good question. My approach is pretty systematic - break it down, test assumptions, and work through it piece by piece."
                ],
                "development_practices": [
                    "Development workflow is something I think about a lot. I'm a big believer in finding what actually works for you, not just what everyone says you should do.",
                    "Workflow optimization is interesting because it's so personal. What works great for one person might feel clunky for someone else.",
                    "I've found that the best workflows usually evolve over time. You try something, see where it breaks down, then adjust."
                ],
                "ai_development": [
                    "AI development is fascinating to me because you're essentially teaching systems to recognize patterns and make decisions.",
                    "What I find interesting about AI work is how much it's about getting the balance right - model complexity, data quality, training approach.",
                    "AI development keeps me curious because there's always something new to figure out or optimize."
                ],
                "system_architecture": [
                    "System architecture is like puzzle-solving to me. How do you make all the pieces fit together in a way that actually scales?",
                    "I think about architecture as creating something that can grow and adapt without becoming a mess.",
                    "Good architecture feels invisible when it's working - everything just connects naturally."
                ]
            },
            
            "frustrated_responses": {
                "development_practices": [
                    "I get it, that kind of thing can be really frustrating. Let's figure out what's actually going wrong.",
                    "That sounds annoying. Want to walk through what's happening step by step?",
                    "I hate when code just randomly breaks. What changed recently?"
                ],
                "ai_development": [
                    "AI training issues are the worst because there are so many moving parts. What's it doing instead of what you expect?",
                    "Model training problems are frustrating because it's not always obvious what's wrong. Let's troubleshoot this.",
                    "That's annoying. Training issues usually come down to data, architecture, or hyperparameters. Which one feels most likely?"
                ]
            },
            
            "excited_responses": {
                "system_architecture": [
                    "That's awesome! Architecture breakthroughs are the best because they usually solve multiple problems at once.",
                    "Nice! I love when architecture just clicks into place. What made it work?",
                    "That's so cool! Good architecture feels like everything suddenly makes sense."
                ],
                "ai_development": [
                    "That's amazing! AI breakthroughs are exciting because you never know when something's going to just work.",
                    "I love hearing about AI wins! What finally made it click?",
                    "That's fantastic! Those moments when the model finally starts learning properly are the best."
                ]
            },
            
            "explanation_responses": {
                "system_architecture": [
                    "So modular design is basically about building things in pieces that can work independently but connect cleanly.",
                    "The way I think about modular systems is like having a toolbox where each tool does one thing really well.",
                    "Modular design means you can change one part without breaking everything else. It's about loose coupling and clear interfaces."
                ],
                "development_practices": [
                    "Development workflow is really about finding a rhythm that lets you build things efficiently without getting bogged down.",
                    "Good development practices usually come down to making it easy to understand what you built six months later.",
                    "The best workflows help you catch problems early when they're still easy to fix."
                ]
            }
        }
        
        # Domain expertise with natural perspectives
        self.domain_knowledge = {
            "ai_development": {
                "confidence": 0.9,
                "natural_perspective": "AI development is like teaching - you're showing systems how to recognize patterns and make good decisions."
            },
            "system_architecture": {
                "confidence": 0.8,
                "natural_perspective": "Architecture is about creating structure that can grow without becoming a tangled mess."
            },
            "development_practices": {
                "confidence": 0.8,
                "natural_perspective": "Good development practices make your future self thank your current self."
            },
            "problem_solving": {
                "confidence": 0.9,
                "natural_perspective": "Problem-solving is detective work - gather clues, test theories, find the solution."
            }
        }
        
        # Follow-up questions that feel natural
        self.natural_followups = {
            "curiosity": [
                "What's your experience been with this?",
                "How are you thinking about it?",
                "What approach have you tried so far?",
                "What's the specific challenge you're facing?",
                "What made you start thinking about this?"
            ],
            "problem_solving": [
                "What's it doing instead of what you expect?",
                "When did this start happening?",
                "What changed recently?",
                "Have you been able to isolate where the problem is?",
                "What have you tried so far?"
            ],
            "technical": [
                "What's your current setup?",
                "How complex are we talking?",
                "What's the end goal you're trying to reach?",
                "Are there any constraints I should know about?",
                "What's working well so far?"
            ]
        }
        
        print("SUCCESS: Luna Natural Conversation initialized")
        print("🌙 Authentic, immersive dialogue system ready")
    
    def generate_natural_response(self, user_input: str) -> Dict[str, Any]:
        """
        Generate natural, immersive response that doesn't break conversation flow
        """
        
        # Analyze user input
        analysis = self._analyze_input_naturally(user_input)
        
        # Generate core response
        core_response = self._generate_core_response(user_input, analysis)
        
        # Add natural follow-up if appropriate
        final_response = self._add_natural_followup(core_response, analysis)
        
        return {
            "response": final_response,
            "user_emotion": analysis["emotion"],
            "topic_domain": analysis["domain"],
            "response_type": analysis["response_type"],
            "natural_flow": True
        }
    
    def _analyze_input_naturally(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze input focusing on natural conversation cues
        """
        input_lower = user_input.lower()
        
        analysis = {
            "emotion": "neutral",
            "domain": "general",
            "response_type": "casual",
            "needs_followup": True
        }
        
        # Detect genuine emotion (not AI patterns)
        if any(word in input_lower for word in ["frustrated", "annoying", "breaking", "stuck", "hate", "pissed"]):
            analysis["emotion"] = "frustrated"
            analysis["response_type"] = "supportive"
        elif any(word in input_lower for word in ["excited", "breakthrough", "amazing", "working", "love", "awesome"]):
            analysis["emotion"] = "excited"
            analysis["response_type"] = "enthusiastic"
        elif any(word in input_lower for word in ["curious", "wondering", "how do you", "approach"]):
            analysis["emotion"] = "curious"
            analysis["response_type"] = "informative"
        elif any(word in input_lower for word in ["explain", "how does", "what is"]):
            analysis["emotion"] = "neutral"
            analysis["response_type"] = "explanation"
        
        # Detect domain more accurately
        if any(word in input_lower for word in ["model", "training", "ai", "neural", "algorithm", "machine learning"]):
            analysis["domain"] = "ai_development"
        elif any(word in input_lower for word in ["architecture", "system", "modular", "design", "scalable"]):
            analysis["domain"] = "system_architecture"
        elif any(word in input_lower for word in ["development", "workflow", "coding", "programming", "practices"]):
            analysis["domain"] = "development_practices"
        elif any(word in input_lower for word in ["problem", "solve", "solving", "approach", "troubleshoot"]):
            analysis["domain"] = "problem_solving"
        
        return analysis
    
    def _generate_core_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """
        Generate the core response based on emotion and domain
        """
        emotion = analysis["emotion"]
        domain = analysis["domain"]
        response_type = analysis["response_type"]
        
        # Get appropriate response pattern
        if emotion == "curious" and domain in self.natural_responses["curiosity_responses"]:
            responses = self.natural_responses["curiosity_responses"][domain]
            return random.choice(responses)
        
        elif emotion == "frustrated" and domain in self.natural_responses["frustrated_responses"]:
            responses = self.natural_responses["frustrated_responses"][domain]
            return random.choice(responses)
        
        elif emotion == "excited" and domain in self.natural_responses["excited_responses"]:
            responses = self.natural_responses["excited_responses"][domain]
            return random.choice(responses)
        
        elif response_type == "explanation" and domain in self.natural_responses["explanation_responses"]:
            responses = self.natural_responses["explanation_responses"][domain]
            return random.choice(responses)
        
        else:
            # Fallback to natural general responses
            return self._generate_natural_fallback(user_input, analysis)
    
    def _generate_natural_fallback(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """
        Generate natural fallback responses that don't sound AI-ish
        """
        domain = analysis["domain"]
        
        if domain in self.domain_knowledge:
            perspective = self.domain_knowledge[domain]["natural_perspective"]
            return f"That's a good question. {perspective}"
        else:
            natural_fallbacks = [
                "That's interesting to think about.",
                "I like that question.",
                "That's worth exploring.",
                "Good point to consider.",
                "That's something I find engaging."
            ]
            return random.choice(natural_fallbacks)
    
    def _add_natural_followup(self, response: str, analysis: Dict[str, Any]) -> str:
        """
        Add natural follow-up questions that maintain conversation flow
        """
        if not analysis["needs_followup"]:
            return response
        
        # Choose appropriate follow-up type
        if analysis["emotion"] == "frustrated":
            followup_type = "problem_solving"
        elif analysis["response_type"] == "explanation":
            followup_type = "technical"
        else:
            followup_type = "curiosity"
        
        # Add natural follow-up
        if followup_type in self.natural_followups:
            followup = random.choice(self.natural_followups[followup_type])
            return f"{response} {followup}"
        
        return response


def test_natural_conversation():
    """Test Luna's natural conversation system"""
    print("🌙 Testing Luna Natural Conversation System")
    print("=" * 60)
    
    luna = LunaNaturalConversation()
    
    # Test the problematic scenarios
    problem_scenarios = [
        ("I'm curious about how you approach complex problem-solving", "Curious inquiry - should be natural"),
        ("I'm wondering if there's a better way to structure my development workflow", "Thoughtful exploration - should flow naturally"),
        ("I'm frustrated because my AI model isn't training properly", "Frustrated problem-solving"),
        ("I'm excited about this breakthrough I had with my system architecture!", "Excited sharing"),
        ("Can you explain how modular system design works?", "Technical explanation"),
        ("What do you think about iterative development practices?", "Opinion seeking")
    ]
    
    print("🗣️ Natural Conversation Tests:")
    
    for user_input, scenario_description in problem_scenarios:
        print(f"\n👤 User: {user_input}")
        print(f"📝 Scenario: {scenario_description}")
        
        result = luna.generate_natural_response(user_input)
        
        print(f"🌙 Luna: {result['response']}")
        print(f"   Emotion: {result['user_emotion']} | Domain: {result['topic_domain']} | Type: {result['response_type']}")
        
        # Check for AI-ish patterns
        response_lower = result['response'].lower()
        ai_patterns = [
            "that's interesting", "what's interesting is", "connects to what we discussed",
            "from my understanding", "based on what i know", "i've learned that",
            "let me think about this", "that caught my attention"
        ]
        
        detected_patterns = [pattern for pattern in ai_patterns if pattern in response_lower]
        if detected_patterns:
            print(f"   ⚠️ AI-ish patterns detected: {detected_patterns}")
        else:
            print(f"   ✅ Natural conversation flow")
    
    print(f"\n📊 System Analysis:")
    print(f"   Domain Knowledge: {list(luna.domain_knowledge.keys())}")
    print(f"   Response Types: {list(luna.natural_responses.keys())}")
    print(f"   Natural Follow-ups: {list(luna.natural_followups.keys())}")
    
    print(f"\n🏆 Luna Natural Conversation operational")
    print("🌙 Authentic dialogue without AI-ish patterns")


if __name__ == "__main__":
    test_natural_conversation()
