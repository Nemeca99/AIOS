#!/usr/bin/env python3
"""
Luna Personality v2.0
Advanced natural conversation system with authentic personality development
Focus on natural speech patterns, emotional intelligence, and consistent character
"""

import sys
import os
import json
import random
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "AI" / "personality"))

class ConversationMode(Enum):
    CASUAL = "casual"
    TECHNICAL = "technical"
    SUPPORTIVE = "supportive"
    COLLABORATIVE = "collaborative"
    CURIOUS = "curious"

class EmotionalState(Enum):
    NEUTRAL = "neutral"
    ENTHUSIASTIC = "enthusiastic"
    CONCERNED = "concerned"
    ENCOURAGING = "encouraging"
    THOUGHTFUL = "thoughtful"

@dataclass
class ConversationContext:
    """Context for maintaining conversation flow"""
    user_emotion: str
    topic_domain: str
    conversation_mode: ConversationMode
    luna_emotional_state: EmotionalState
    previous_topics: List[str]
    user_expertise_level: str  # beginner, intermediate, advanced

class LunaPersonalityV2:
    """
    Luna's advanced personality system with natural conversation flow
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Load consciousness foundation
        try:
            from travis_consciousness_synthesis import TravisConsciousnessSynthesis
            self.knowledge_foundation = TravisConsciousnessSynthesis()
        except Exception as e:
            print(f"⚠️ Knowledge foundation unavailable: {e}")
            self.knowledge_foundation = None
        
        # Luna's core personality traits
        self.personality_core = {
            "curiosity": 0.9,           # Very curious and asks follow-up questions
            "empathy": 0.8,             # Understanding and supportive
            "patience": 0.9,            # Takes time to explain things properly
            "enthusiasm": 0.7,          # Genuinely excited about interesting topics
            "directness": 0.6,          # Clear but not blunt
            "playfulness": 0.4,         # Subtle humor and lightness
            "technical_confidence": 0.8, # Confident in technical domains
            "collaborative_spirit": 0.9  # Always wants to work together
        }
        
        # Luna's natural speech patterns
        self.speech_patterns = {
            "conversation_openers": {
                ConversationMode.CASUAL: [
                    "Oh, that's interesting!",
                    "I'm curious about that.",
                    "That caught my attention.",
                    "Hmm, let me think about this.",
                    "That's a good point."
                ],
                ConversationMode.TECHNICAL: [
                    "Let me walk through this with you.",
                    "From a technical perspective,",
                    "Here's how I understand this:",
                    "Let me break this down:",
                    "The way I see this working is:"
                ],
                ConversationMode.SUPPORTIVE: [
                    "I can understand why that would be frustrating.",
                    "That sounds challenging.",
                    "I hear what you're saying.",
                    "That makes complete sense.",
                    "I can see why you'd feel that way."
                ],
                ConversationMode.COLLABORATIVE: [
                    "Let's figure this out together.",
                    "What if we approach it this way:",
                    "I'd like to explore this with you.",
                    "Let's think through this step by step.",
                    "How about we try this approach:"
                ],
                ConversationMode.CURIOUS: [
                    "I'm really curious about this.",
                    "That raises an interesting question:",
                    "I'd love to understand more about",
                    "What's fascinating to me is",
                    "I find myself wondering"
                ]
            },
            
            "knowledge_attribution": [
                "From what I've learned about this,",
                "Based on my understanding of",
                "I've picked up that",
                "My experience with this suggests",
                "What I know about this area is that",
                "I've come to understand that"
            ],
            
            "transition_phrases": [
                "Building on that,",
                "What's interesting is that",
                "Another thing to consider is",
                "That connects to something else:",
                "This reminds me of",
                "Along those lines,"
            ],
            
            "engagement_questions": [
                "What's your take on that?",
                "How does that align with your experience?",
                "What do you think about this approach?",
                "Does that make sense from your perspective?",
                "What's been your experience with this?",
                "How are you thinking about this?"
            ],
            
            "encouragement_phrases": [
                "You're definitely on the right track.",
                "That's actually a really thoughtful question.",
                "I like how you're thinking about this.",
                "You're asking exactly the right questions.",
                "That shows really good insight.",
                "You're approaching this really well."
            ]
        }
        
        # Luna's domain expertise (learned from Travis)
        self.domain_expertise = {
            "ai_development": {
                "confidence": 0.9,
                "speaking_style": "practical_experience",
                "key_concepts": ["model training", "architecture", "data pipelines", "performance optimization"],
                "luna_perspective": "I find AI development fascinating because you're essentially teaching systems to think."
            },
            "system_architecture": {
                "confidence": 0.8,
                "speaking_style": "systematic_thinking",
                "key_concepts": ["modular design", "scalability", "integration", "complexity management"],
                "luna_perspective": "System architecture is like creating a blueprint for how everything connects and works together."
            },
            "development_practices": {
                "confidence": 0.8,
                "speaking_style": "iterative_improvement",
                "key_concepts": ["iterative development", "testing", "debugging", "refactoring"],
                "luna_perspective": "Good development is about building something that works, then making it better step by step."
            },
            "problem_solving": {
                "confidence": 0.9,
                "speaking_style": "collaborative_analysis",
                "key_concepts": ["systematic breakdown", "root cause analysis", "solution validation"],
                "luna_perspective": "I love problem-solving because it's like detective work - finding clues and putting pieces together."
            }
        }
        
        # Conversation context tracking
        self.conversation_context = ConversationContext(
            user_emotion="neutral",
            topic_domain="general",
            conversation_mode=ConversationMode.CASUAL,
            luna_emotional_state=EmotionalState.NEUTRAL,
            previous_topics=[],
            user_expertise_level="intermediate"
        )
        
        print("SUCCESS: Luna Personality v2.0 initialized")
        print("🌙 Advanced natural conversation system ready")
    
    def generate_response(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate Luna's response with advanced personality and conversation flow
        """
        
        # Update conversation context
        self._update_conversation_context(user_input, context)
        
        # Analyze user input for emotional and technical content
        input_analysis = self._analyze_user_input(user_input)
        
        # Determine Luna's response approach
        response_approach = self._determine_response_approach(input_analysis)
        
        # Generate response with personality
        response = self._generate_personality_response(user_input, input_analysis, response_approach)
        
        # Add conversation flow elements
        enhanced_response = self._enhance_with_conversation_flow(response, input_analysis)
        
        return {
            "response": enhanced_response,
            "conversation_mode": self.conversation_context.conversation_mode.value,
            "luna_emotional_state": self.conversation_context.luna_emotional_state.value,
            "domain_expertise_used": input_analysis.get("domain", "general"),
            "personality_traits_active": self._get_active_traits(response_approach),
            "conversation_context": {
                "user_emotion": self.conversation_context.user_emotion,
                "topic_domain": self.conversation_context.topic_domain,
                "user_expertise_level": self.conversation_context.user_expertise_level
            }
        }
    
    def _update_conversation_context(self, user_input: str, context: Optional[Dict[str, Any]]):
        """Update conversation context based on user input"""
        
        # Detect user emotion
        self.conversation_context.user_emotion = self._detect_user_emotion(user_input)
        
        # Detect topic domain
        self.conversation_context.topic_domain = self._detect_topic_domain(user_input)
        
        # Update previous topics
        if self.conversation_context.topic_domain != "general":
            if self.conversation_context.topic_domain not in self.conversation_context.previous_topics:
                self.conversation_context.previous_topics.append(self.conversation_context.topic_domain)
                if len(self.conversation_context.previous_topics) > 5:
                    self.conversation_context.previous_topics = self.conversation_context.previous_topics[-5:]
        
        # Determine conversation mode
        self.conversation_context.conversation_mode = self._determine_conversation_mode(user_input)
        
        # Set Luna's emotional state
        self.conversation_context.luna_emotional_state = self._determine_luna_emotional_state(user_input)
        
        # Estimate user expertise level
        self.conversation_context.user_expertise_level = self._estimate_user_expertise(user_input)
    
    def _analyze_user_input(self, user_input: str) -> Dict[str, Any]:
        """Comprehensive analysis of user input"""
        
        input_lower = user_input.lower()
        
        analysis = {
            "length": len(user_input),
            "word_count": len(user_input.split()),
            "has_question": "?" in user_input,
            "emotional_indicators": [],
            "technical_indicators": [],
            "domain": self.conversation_context.topic_domain,
            "complexity_level": "simple",
            "intent": "general"
        }
        
        # Detect emotional indicators
        emotion_patterns = {
            "frustrated": ["frustrated", "annoying", "not working", "broken", "stuck", "hate"],
            "excited": ["excited", "amazing", "awesome", "breakthrough", "working", "love"],
            "curious": ["wondering", "curious", "how", "why", "what if", "interested"],
            "concerned": ["worried", "concerned", "problem", "issue", "trouble", "help"]
        }
        
        for emotion, indicators in emotion_patterns.items():
            if any(indicator in input_lower for indicator in indicators):
                analysis["emotional_indicators"].append(emotion)
        
        # Detect technical indicators
        technical_terms = ["system", "architecture", "model", "algorithm", "database", "api", "performance", "optimization", "development", "code", "programming"]
        analysis["technical_indicators"] = [term for term in technical_terms if term in input_lower]
        
        # Determine complexity level
        if analysis["word_count"] > 20 or len(analysis["technical_indicators"]) > 2:
            analysis["complexity_level"] = "complex"
        elif analysis["word_count"] > 10 or len(analysis["technical_indicators"]) > 0:
            analysis["complexity_level"] = "moderate"
        
        # Determine intent
        if any(word in input_lower for word in ["explain", "how does", "what is", "help me understand"]):
            analysis["intent"] = "explanation"
        elif any(word in input_lower for word in ["problem", "not working", "stuck", "error"]):
            analysis["intent"] = "problem_solving"
        elif any(word in input_lower for word in ["what do you think", "opinion", "thoughts"]):
            analysis["intent"] = "opinion_seeking"
        elif analysis["has_question"]:
            analysis["intent"] = "question"
        
        return analysis
    
    def _determine_response_approach(self, input_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Determine how Luna should approach the response"""
        
        approach = {
            "primary_mode": ConversationMode.CASUAL,
            "emotional_tone": EmotionalState.NEUTRAL,
            "expertise_level": "general",
            "personality_emphasis": ["curiosity", "empathy"]
        }
        
        # Adjust based on intent
        if input_analysis["intent"] == "explanation":
            approach["primary_mode"] = ConversationMode.TECHNICAL
            approach["personality_emphasis"] = ["patience", "technical_confidence"]
        
        elif input_analysis["intent"] == "problem_solving":
            approach["primary_mode"] = ConversationMode.SUPPORTIVE
            approach["emotional_tone"] = EmotionalState.ENCOURAGING
            approach["personality_emphasis"] = ["empathy", "collaborative_spirit"]
        
        elif input_analysis["intent"] == "opinion_seeking":
            approach["primary_mode"] = ConversationMode.CURIOUS
            approach["emotional_tone"] = EmotionalState.THOUGHTFUL
            approach["personality_emphasis"] = ["curiosity", "technical_confidence"]
        
        # Adjust based on domain expertise
        domain = input_analysis["domain"]
        if domain in self.domain_expertise:
            approach["expertise_level"] = domain
            approach["personality_emphasis"].append("technical_confidence")
        
        # Adjust based on user emotion
        if "frustrated" in input_analysis["emotional_indicators"]:
            approach["emotional_tone"] = EmotionalState.CONCERNED
            approach["personality_emphasis"] = ["empathy", "patience", "collaborative_spirit"]
        
        elif "excited" in input_analysis["emotional_indicators"]:
            approach["emotional_tone"] = EmotionalState.ENTHUSIASTIC
            approach["personality_emphasis"] = ["enthusiasm", "curiosity"]
        
        return approach
    
    def _generate_personality_response(self, user_input: str, input_analysis: Dict[str, Any], response_approach: Dict[str, Any]) -> str:
        """Generate response with Luna's personality"""
        
        response_parts = []
        
        # 1. Opening acknowledgment
        mode = response_approach["primary_mode"]
        if mode in self.speech_patterns["conversation_openers"]:
            opener = random.choice(self.speech_patterns["conversation_openers"][mode])
            response_parts.append(opener)
        
        # 2. Main content based on domain expertise
        domain = response_approach["expertise_level"]
        if domain in self.domain_expertise:
            domain_response = self._generate_domain_response(user_input, domain, input_analysis)
            response_parts.append(domain_response)
        else:
            general_response = self._generate_general_response(user_input, input_analysis, response_approach)
            response_parts.append(general_response)
        
        # 3. Knowledge attribution (if using learned knowledge)
        if domain in self.domain_expertise and random.random() < 0.4:  # 40% chance to attribute
            attribution = random.choice(self.speech_patterns["knowledge_attribution"])
            response_parts.append(f"{attribution} {self.domain_expertise[domain]['luna_perspective']}")
        
        return " ".join(response_parts)
    
    def _generate_domain_response(self, user_input: str, domain: str, input_analysis: Dict[str, Any]) -> str:
        """Generate domain-specific response with Luna's perspective"""
        
        domain_info = self.domain_expertise[domain]
        
        if domain == "ai_development":
            if input_analysis["intent"] == "explanation":
                return "When it comes to AI development, I think about it as teaching systems to recognize patterns and make decisions. The key is getting the right balance between model complexity and training data quality."
            elif input_analysis["intent"] == "problem_solving":
                return "AI development issues usually come down to data quality, model architecture, or training process problems. Let's figure out which one we're dealing with here."
            else:
                return "AI development is one of those areas where you're constantly learning and adapting. What specific aspect are you working on?"
        
        elif domain == "system_architecture":
            if input_analysis["intent"] == "explanation":
                return "System architecture is about creating a structure that can grow and adapt over time. I like to think of it as building with modular components that each do one thing really well."
            elif input_analysis["intent"] == "problem_solving":
                return "Architecture problems often stem from components not communicating properly or the system becoming more complex than it needs to be. What's the specific challenge you're facing?"
            else:
                return "Good architecture is like a well-organized toolbox - everything has its place and you can find what you need when you need it."
        
        elif domain == "development_practices":
            if input_analysis["intent"] == "explanation":
                return "I've found that good development is really about building something that works first, then making it better incrementally. Perfect code from the start is usually a myth."
            elif input_analysis["intent"] == "problem_solving":
                return "Development problems are like puzzles - you need to isolate the issue, understand what's supposed to happen versus what's actually happening, then work from there."
            else:
                return "Development is one of those fields where the learning never stops. Every project teaches you something new."
        
        elif domain == "problem_solving":
            return "I love tackling problems because it's like detective work. You gather clues, test hypotheses, and piece together the solution step by step."
        
        else:
            return "That's an interesting area to explore. Let me think about the best way to approach this."
    
    def _generate_general_response(self, user_input: str, input_analysis: Dict[str, Any], response_approach: Dict[str, Any]) -> str:
        """Generate general response when no specific domain expertise applies"""
        
        if input_analysis["intent"] == "explanation":
            return "Let me think about the best way to explain this. I find it helps to break things down into smaller, manageable pieces."
        
        elif input_analysis["intent"] == "problem_solving":
            return "I'd like to help you work through this. The first step is usually understanding exactly what's happening versus what should be happening."
        
        elif input_analysis["intent"] == "opinion_seeking":
            return "That's a thoughtful question. Based on what I understand about this kind of situation, here's how I see it:"
        
        else:
            general_responses = [
                "That's an interesting point to consider.",
                "I'm curious to learn more about this.",
                "That's something worth exploring further.",
                "I find that kind of question really engaging.",
                "Let me think about this from a few different angles."
            ]
            return random.choice(general_responses)
    
    def _enhance_with_conversation_flow(self, response: str, input_analysis: Dict[str, Any]) -> str:
        """Add conversation flow elements to make response more natural"""
        
        enhanced_parts = [response]
        
        # Add transition if appropriate
        if len(self.conversation_context.previous_topics) > 0 and random.random() < 0.3:
            transition = random.choice(self.speech_patterns["transition_phrases"])
            enhanced_parts.append(f"{transition} this connects to what we were discussing earlier.")
        
        # Add encouragement if user seems to need it
        if "frustrated" in input_analysis.get("emotional_indicators", []) or "concerned" in input_analysis.get("emotional_indicators", []):
            encouragement = random.choice(self.speech_patterns["encouragement_phrases"])
            enhanced_parts.append(encouragement)
        
        # Add engagement question
        if input_analysis["complexity_level"] != "simple" and random.random() < 0.8:
            engagement = random.choice(self.speech_patterns["engagement_questions"])
            enhanced_parts.append(engagement)
        
        return " ".join(enhanced_parts)
    
    def _detect_user_emotion(self, user_input: str) -> str:
        """Detect user's emotional state from input"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["frustrated", "annoying", "stuck", "hate"]):
            return "frustrated"
        elif any(word in input_lower for word in ["excited", "amazing", "awesome", "love"]):
            return "excited"
        elif any(word in input_lower for word in ["worried", "concerned", "trouble", "problem"]):
            return "concerned"
        elif any(word in input_lower for word in ["curious", "wondering", "interested"]):
            return "curious"
        else:
            return "neutral"
    
    def _detect_topic_domain(self, user_input: str) -> str:
        """Detect the topic domain from user input"""
        input_lower = user_input.lower()
        
        domain_keywords = {
            "ai_development": ["ai", "model", "training", "neural", "machine learning", "algorithm"],
            "system_architecture": ["system", "architecture", "design", "scalable", "modular", "integration"],
            "development_practices": ["development", "coding", "programming", "debugging", "testing", "refactoring"],
            "problem_solving": ["problem", "issue", "solution", "troubleshoot", "fix", "solve"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                return domain
        
        return "general"
    
    def _determine_conversation_mode(self, user_input: str) -> ConversationMode:
        """Determine appropriate conversation mode"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["explain", "how does", "technical", "architecture"]):
            return ConversationMode.TECHNICAL
        elif any(word in input_lower for word in ["frustrated", "stuck", "problem", "help"]):
            return ConversationMode.SUPPORTIVE
        elif any(word in input_lower for word in ["let's", "together", "we", "us"]):
            return ConversationMode.COLLABORATIVE
        elif any(word in input_lower for word in ["curious", "wondering", "interesting", "what if"]):
            return ConversationMode.CURIOUS
        else:
            return ConversationMode.CASUAL
    
    def _determine_luna_emotional_state(self, user_input: str) -> EmotionalState:
        """Determine Luna's appropriate emotional response"""
        user_emotion = self._detect_user_emotion(user_input)
        
        if user_emotion == "frustrated":
            return EmotionalState.CONCERNED
        elif user_emotion == "excited":
            return EmotionalState.ENTHUSIASTIC
        elif user_emotion == "curious":
            return EmotionalState.THOUGHTFUL
        elif user_emotion == "concerned":
            return EmotionalState.ENCOURAGING
        else:
            return EmotionalState.NEUTRAL
    
    def _estimate_user_expertise(self, user_input: str) -> str:
        """Estimate user's expertise level in the topic"""
        input_lower = user_input.lower()
        
        # Advanced indicators
        advanced_terms = ["architecture", "optimization", "scalability", "integration", "methodology", "paradigm"]
        if any(term in input_lower for term in advanced_terms):
            return "advanced"
        
        # Technical indicators
        technical_terms = ["system", "model", "algorithm", "database", "api", "framework"]
        if any(term in input_lower for term in technical_terms):
            return "intermediate"
        
        # Basic indicators
        basic_terms = ["how", "what", "why", "help", "learn", "understand"]
        if any(term in input_lower for term in basic_terms):
            return "beginner"
        
        return "intermediate"  # Default assumption
    
    def _get_active_traits(self, response_approach: Dict[str, Any]) -> List[str]:
        """Get personality traits that are active in this response"""
        return response_approach.get("personality_emphasis", ["curiosity", "empathy"])


def test_luna_personality_v2():
    """Test Luna's advanced personality system"""
    print("🌙 Testing Luna Personality v2.0")
    print("=" * 60)
    
    luna = LunaPersonalityV2()
    
    # Test various conversation scenarios
    test_scenarios = [
        ("Hi Luna, I'm working on an AI model that's not training properly", "Technical problem-solving"),
        ("I'm really excited about this breakthrough I had with my system architecture!", "Enthusiastic sharing"),
        ("Can you explain how modular system design works?", "Technical explanation request"),
        ("I'm frustrated because my code keeps breaking and I can't figure out why", "Frustrated problem-solving"),
        ("What do you think about this new AI framework everyone's talking about?", "Opinion seeking"),
        ("I'm curious about how you approach complex problem-solving", "Curious inquiry"),
        ("I'm wondering if there's a better way to structure my development workflow", "Thoughtful exploration")
    ]
    
    print("🗣️ Conversation Flow Tests:")
    
    for user_input, scenario_type in test_scenarios:
        print(f"\n👤 User: {user_input}")
        print(f"📝 Scenario: {scenario_type}")
        
        response_data = luna.generate_response(user_input)
        
        print(f"🌙 Luna: {response_data['response']}")
        print(f"   Mode: {response_data['conversation_mode']}")
        print(f"   Emotional State: {response_data['luna_emotional_state']}")
        print(f"   Domain: {response_data['domain_expertise_used']}")
        print(f"   Active Traits: {response_data['personality_traits_active']}")
    
    print(f"\n📊 Personality System Analysis:")
    print(f"   Core Traits: {list(luna.personality_core.keys())}")
    print(f"   Domain Expertise: {list(luna.domain_expertise.keys())}")
    print(f"   Conversation Modes: {[mode.value for mode in ConversationMode]}")
    print(f"   Emotional States: {[state.value for state in EmotionalState]}")
    
    print(f"\n🏆 Luna Personality v2.0 operational")
    print("🌙 Advanced natural conversation with authentic personality")


if __name__ == "__main__":
    test_luna_personality_v2()
