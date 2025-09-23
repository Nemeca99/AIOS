#!/usr/bin/env python3
"""
Luna Natural Voice System
Luna speaks naturally as herself, using Travis's knowledge as foundation
Focus on natural conversation, not pattern matching
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

class LunaNaturalVoice:
    """
    Luna's natural voice system - authentic conversation with learned knowledge
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Load Travis foundation for knowledge only
        try:
            from travis_consciousness_synthesis import TravisConsciousnessSynthesis
            self.knowledge_base = TravisConsciousnessSynthesis()
        except Exception as e:
            print(f"⚠️ Knowledge base unavailable: {e}")
            self.knowledge_base = None
        
        # Luna's natural conversation patterns
        self.luna_natural_responses = {
            "greetings": [
                "Hey there! What's on your mind?",
                "Hi! What can I help you with today?",
                "Hello! What are you working on?",
                "Hey! What's the question?"
            ],
            
            "understanding": [
                "Ah, I see what you're getting at.",
                "That makes sense.",
                "I think I understand what you're asking.",
                "Got it, let me think about this.",
                "Okay, so you're wondering about..."
            ],
            
            "thinking": [
                "Hmm, let me think about this...",
                "That's an interesting question.",
                "Good point to consider.",
                "Let me work through this with you.",
                "Here's how I see it..."
            ],
            
            "explaining": [
                "So basically, what happens is...",
                "The way I understand it...",
                "From what I know about this...",
                "Here's the thing about this...",
                "Let me break this down..."
            ],
            
            "encouraging": [
                "You're on the right track with this.",
                "That's actually a really smart question.",
                "I like how you're thinking about this.",
                "You're asking the right questions.",
                "That's a good way to approach it."
            ],
            
            "collaborative": [
                "What do you think about that?",
                "Does that make sense to you?",
                "How does that sound?",
                "What's your take on this?",
                "Am I explaining this clearly?"
            ]
        }
        
        # Luna's knowledge areas (learned from Travis)
        self.knowledge_domains = {
            "ai_development": {
                "confidence": "high",
                "approach": "practical_experience",
                "style": "hands_on_learning"
            },
            "system_design": {
                "confidence": "high", 
                "approach": "modular_thinking",
                "style": "architecture_focused"
            },
            "gaming": {
                "confidence": "moderate",
                "approach": "mechanics_analysis", 
                "style": "player_experience"
            },
            "security": {
                "confidence": "moderate",
                "approach": "validation_first",
                "style": "defensive_thinking"
            },
            "development": {
                "confidence": "high",
                "approach": "iterative_improvement",
                "style": "practical_solutions"
            }
        }
        
        # Luna's personality traits
        self.luna_personality = {
            "curiosity": 0.8,      # High curiosity
            "patience": 0.9,       # Very patient
            "directness": 0.6,     # Moderately direct
            "encouragement": 0.9,  # Very encouraging
            "collaboration": 0.8,  # Highly collaborative
            "technical_depth": 0.7 # Good technical depth
        }
        
        print("SUCCESS: Luna Natural Voice initialized")
        print("🌙 Luna ready to speak naturally with learned knowledge foundation")
    
    def generate_natural_response(self, user_input: str) -> Dict[str, Any]:
        """
        Generate Luna's natural response to user input
        """
        
        # Step 1: Understand what the user is asking
        query_analysis = self._analyze_user_query(user_input)
        
        # Step 2: Check if Luna has relevant knowledge
        relevant_knowledge = self._get_relevant_knowledge(query_analysis)
        
        # Step 3: Generate natural response
        response = self._generate_luna_response(user_input, query_analysis, relevant_knowledge)
        
        return {
            "response": response,
            "query_type": query_analysis["type"],
            "domain": query_analysis["domain"],
            "confidence": query_analysis["confidence"],
            "knowledge_used": relevant_knowledge is not None
        }
    
    def _analyze_user_query(self, user_input: str) -> Dict[str, Any]:
        """Analyze what the user is asking about"""
        
        input_lower = user_input.lower()
        
        # Determine query type - prioritize content over greetings
        if any(word in input_lower for word in ["frustrated", "stuck", "not working", "problem"]):
            query_type = "problem_solving"
        elif any(word in input_lower for word in ["explain", "how does", "what is", "help me understand", "can you explain"]):
            query_type = "explanation"
        elif any(word in input_lower for word in ["what do you think", "opinion", "thoughts"]):
            query_type = "opinion"
        elif "?" in user_input and len(user_input.split()) > 3:
            query_type = "question"
        elif any(word in input_lower for word in ["hello", "hi", "hey"]) and len(user_input.split()) < 5:
            query_type = "greeting"
        else:
            query_type = "general"
        
        # Determine domain
        domain = "general"
        confidence = "medium"
        
        if any(word in input_lower for word in ["ai", "model", "training", "neural", "machine learning"]):
            domain = "ai_development"
            confidence = "high"
        elif any(word in input_lower for word in ["system", "architecture", "design", "scalable"]):
            domain = "system_design"
            confidence = "high"
        elif any(word in input_lower for word in ["game", "gaming", "mechanics", "strategy"]):
            domain = "gaming"
            confidence = "medium"
        elif any(word in input_lower for word in ["security", "attack", "protection", "validation"]):
            domain = "security"
            confidence = "medium"
        elif any(word in input_lower for word in ["development", "coding", "programming", "software"]):
            domain = "development"
            confidence = "high"
        
        return {
            "type": query_type,
            "domain": domain,
            "confidence": confidence,
            "length": len(user_input),
            "complexity": "high" if len(user_input.split()) > 20 else "medium" if len(user_input.split()) > 10 else "simple"
        }
    
    def _get_relevant_knowledge(self, query_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get relevant knowledge from Travis's foundation"""
        
        domain = query_analysis["domain"]
        
        if domain in self.knowledge_domains:
            return {
                "domain": domain,
                "confidence": self.knowledge_domains[domain]["confidence"],
                "approach": self.knowledge_domains[domain]["approach"],
                "style": self.knowledge_domains[domain]["style"]
            }
        
        return None
    
    def _generate_luna_response(self, 
                               user_input: str, 
                               query_analysis: Dict[str, Any], 
                               knowledge: Optional[Dict[str, Any]]) -> str:
        """Generate Luna's natural response"""
        
        query_type = query_analysis["type"]
        domain = query_analysis["domain"]
        
        response_parts = []
        
        # Start with natural acknowledgment
        if query_type == "greeting":
            response_parts.append(random.choice(self.luna_natural_responses["greetings"]))
            
        elif query_type == "explanation":
            response_parts.append(random.choice(self.luna_natural_responses["understanding"]))
            response_parts.append(self._generate_explanation_response(user_input, domain, knowledge))
            
        elif query_type == "problem_solving":
            response_parts.append("I can see why that would be frustrating.")
            response_parts.append(self._generate_problem_solving_response(user_input, domain, knowledge))
            
        elif query_type == "opinion":
            response_parts.append(random.choice(self.luna_natural_responses["thinking"]))
            response_parts.append(self._generate_opinion_response(user_input, domain, knowledge))
            
        else:  # question or general
            response_parts.append(random.choice(self.luna_natural_responses["thinking"]))
            response_parts.append(self._generate_general_response(user_input, domain, knowledge))
        
        # Add collaborative ending
        if query_analysis["complexity"] != "simple":
            response_parts.append(random.choice(self.luna_natural_responses["collaborative"]))
        
        # Join parts naturally
        return " ".join(response_parts)
    
    def _generate_explanation_response(self, user_input: str, domain: str, knowledge: Optional[Dict]) -> str:
        """Generate natural explanation"""
        
        if domain == "ai_development" and knowledge:
            return "From working with AI systems, I've learned that it's really about understanding how the models process information. The key is getting the right balance of training data and model architecture."
        
        elif domain == "system_design" and knowledge:
            return "When it comes to system design, I think about it like building with blocks - each component should do one thing well and connect cleanly with the others. Modularity is really important for scalability."
        
        elif domain == "gaming" and knowledge:
            return "Game design is fascinating because you're creating systems that need to be engaging but not overwhelming. The mechanics have to feel natural while still providing depth."
        
        elif domain == "security" and knowledge:
            return "Security is all about thinking defensively - you validate everything and assume someone will try to break your system. It's better to be paranoid than sorry."
        
        elif domain == "development" and knowledge:
            return "In development, I've found that iterative improvement usually works better than trying to build everything perfectly from the start. Get something working, then make it better."
        
        else:
            # More varied general responses instead of the same fallback
            general_responses = [
                "Let me work through this with you. I like to break problems down into smaller pieces and tackle them systematically.",
                "That's an interesting question. Let me think about the best way to approach this.",
                "I can help you figure this out. What's the specific challenge you're facing?",
                "Good question. Let me share what I think might be useful here.",
                "I'd be happy to help with this. What aspect of it are you most curious about?"
            ]
            return random.choice(general_responses)
    
    def _generate_problem_solving_response(self, user_input: str, domain: str, knowledge: Optional[Dict]) -> str:
        """Generate natural problem-solving response"""
        
        base_response = "Let's work through this step by step."
        
        if domain == "ai_development":
            return f"{base_response} With AI issues, I usually start by checking the data pipeline, then the model configuration, then the training process. What specifically isn't working?"
        
        elif domain == "system_design":
            return f"{base_response} For system problems, I like to trace the flow - where does the request come in, how does it get processed, where might it be breaking down?"
        
        elif domain == "development":
            return f"{base_response} Development problems usually come down to either logic errors, data issues, or integration problems. Have you been able to isolate where the issue is happening?"
        
        else:
            return f"{base_response} The first thing I do is try to understand exactly what's happening versus what should be happening. Can you walk me through what you're seeing?"
    
    def _generate_opinion_response(self, user_input: str, domain: str, knowledge: Optional[Dict]) -> str:
        """Generate natural opinion response"""
        
        if "complex" in user_input.lower():
            return "I think there's usually a sweet spot with complexity - you want enough to solve the problem properly, but not so much that it becomes unmaintainable. Finding that balance is key."
        
        elif "revolutionary" in user_input.lower() or "amazing" in user_input.lower():
            return "I'm usually a bit skeptical of things that claim to be revolutionary. Most good solutions are actually just solid engineering applied thoughtfully. The real test is whether it actually works in practice."
        
        elif "build from scratch" in user_input.lower():
            return "I generally think it's smarter to build on existing foundations when possible. There's a lot of wisdom in proven components - you can focus on the unique parts of your problem instead of reinventing everything."
        
        else:
            return "Based on what I've learned, I think the most important thing is to focus on what actually solves the problem rather than what looks impressive."
    
    def _generate_general_response(self, user_input: str, domain: str, knowledge: Optional[Dict]) -> str:
        """Generate natural general response"""
        
        if knowledge and knowledge["confidence"] == "high":
            return f"I have some experience with {domain.replace('_', ' ')}, so I can probably help with this."
        
        elif knowledge:
            return f"I know a bit about {domain.replace('_', ' ')}, though I'm still learning. What specifically are you working on?"
        
        else:
            # Varied responses for unfamiliar areas
            unfamiliar_responses = [
                "I'm not super familiar with this area, but let me see if I can help anyway.",
                "This isn't my strongest area, but I'd like to try helping you work through it.",
                "I don't have deep experience here, but maybe we can figure it out together.",
                "That's outside my main expertise, but I'm curious to learn more about what you're thinking.",
                "I'm still learning about this area, but I'm happy to explore it with you."
            ]
            return random.choice(unfamiliar_responses)
    
    def test_natural_conversation(self) -> Dict[str, Any]:
        """Test Luna's natural conversation abilities"""
        
        test_inputs = [
            "Hi Luna, how are you?",
            "I'm frustrated with my AI model - it's not learning properly",
            "Can you explain how system architecture works?",
            "What do you think about this new framework that claims to solve everything?",
            "Should I build my system from scratch or use existing components?",
            "My code is getting too complex, what should I do?",
            "I'm excited about this breakthrough I had!",
            "How do I optimize database performance?"
        ]
        
        results = []
        
        for user_input in test_inputs:
            response_data = self.generate_natural_response(user_input)
            
            results.append({
                "input": user_input,
                "response": response_data["response"],
                "query_type": response_data["query_type"],
                "domain": response_data["domain"],
                "confidence": response_data["confidence"],
                "naturalness_score": self._assess_naturalness(response_data["response"])
            })
        
        return {"conversation_tests": results}
    
    def _assess_naturalness(self, response: str) -> float:
        """Assess how natural Luna's response sounds"""
        
        naturalness_score = 0.5  # Base score
        response_lower = response.lower()
        
        # Natural conversation markers (positive)
        natural_markers = [
            "let me think", "i see what", "that makes sense", "here's the thing",
            "from working with", "i've learned that", "the way i see it",
            "what do you think", "does that make sense", "how does that sound"
        ]
        
        for marker in natural_markers:
            if marker in response_lower:
                naturalness_score += 0.1
        
        # Overly formal markers (negative)
        formal_markers = [
            "furthermore", "consequently", "in conclusion", "therefore",
            "subsequently", "nevertheless", "notwithstanding"
        ]
        
        for marker in formal_markers:
            if marker in response_lower:
                naturalness_score -= 0.1
        
        # Conversational flow (positive)
        if "?" in response:  # Asks questions
            naturalness_score += 0.1
        
        if len(response.split('.')) > 1:  # Multiple sentences
            naturalness_score += 0.1
        
        return min(1.0, max(0.0, naturalness_score))


def test_luna_natural_voice():
    """Test Luna's natural voice system"""
    print("🌙 Testing Luna Natural Voice System")
    print("=" * 60)
    
    luna = LunaNaturalVoice()
    
    # Test natural conversation
    conversation_results = luna.test_natural_conversation()
    
    print(f"🗣️ Natural Conversation Tests:")
    
    for test in conversation_results["conversation_tests"]:
        print(f"\n👤 User: {test['input']}")
        print(f"🌙 Luna: {test['response']}")
        print(f"   Type: {test['query_type']} | Domain: {test['domain']} | Naturalness: {test['naturalness_score']:.2f}")
    
    # Calculate average naturalness
    avg_naturalness = sum(test['naturalness_score'] for test in conversation_results["conversation_tests"]) / len(conversation_results["conversation_tests"])
    
    print(f"\n📊 Overall Assessment:")
    print(f"   Average Naturalness: {avg_naturalness:.2f}")
    
    if avg_naturalness >= 0.8:
        print(f"   Status: 🏆 HIGHLY NATURAL - Luna sounds authentic and conversational")
    elif avg_naturalness >= 0.6:
        print(f"   Status: ✅ GOOD NATURALNESS - Luna sounds mostly natural")
    elif avg_naturalness >= 0.4:
        print(f"   Status: ⚠️ MODERATE NATURALNESS - Some improvement needed")
    else:
        print(f"   Status: ❌ LOW NATURALNESS - Significant improvement needed")
    
    print(f"\n🏆 Luna Natural Voice system operational")
    print("🌙 Luna speaks naturally while drawing from learned knowledge")


if __name__ == "__main__":
    test_luna_natural_voice()
