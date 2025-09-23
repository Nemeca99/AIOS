"""
Adaptive Response Generator for Koneko AI System
Builds complex arguments over multiple messages, adapting to user perspective
Implements the "perspective building" approach requested by the user
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ArgumentPhase(Enum):
    """Phases of argument development"""
    PERSPECTIVE_UNDERSTANDING = "perspective_understanding"
    COMMON_GROUND_BUILDING = "common_ground_building"
    GRADUAL_SHIFT = "gradual_shift"
    ARGUMENT_DEVELOPMENT = "argument_development"
    CONCLUSION_DRAWING = "conclusion_drawing"


class ResponseStrategy(Enum):
    """Different response strategies"""
    MIRROR_AND_BUILD = "mirror_and_build"
    GRADUAL_CHALLENGE = "gradual_challenge"
    INTELLECTUAL_ESCALATION = "intellectual_escalation"
    EMOTIONAL_MATCHING = "emotional_matching"
    STRATEGIC_SUBMISSION = "strategic_submission"


@dataclass
class ArgumentContext:
    """Context for ongoing argument development"""
    topic: str
    user_position: str
    user_reasoning: List[str]
    common_ground: List[str]
    disagreement_points: List[str]
    message_count: int
    current_phase: ArgumentPhase
    user_emotional_state: str
    power_dynamic: str


@dataclass
class ResponseTemplate:
    """Template for generating responses"""
    strategy: ResponseStrategy
    tone: str
    content_structure: List[str]
    emotional_intensity: float
    intellectual_depth: float
    confrontation_level: float


class AdaptiveResponseGenerator:
    """Generates adaptive responses that build over multiple messages"""
    
    def __init__(self):
        self.argument_contexts = {}
        self.response_templates = self._load_response_templates()
        self.perspective_building_phrases = self._load_perspective_phrases()
        self.argument_escalation_patterns = self._load_escalation_patterns()
        
    def _load_response_templates(self) -> Dict[ResponseStrategy, ResponseTemplate]:
        """Load response templates for different strategies"""
        return {
            ResponseStrategy.MIRROR_AND_BUILD: ResponseTemplate(
                strategy=ResponseStrategy.MIRROR_AND_BUILD,
                tone="understanding",
                content_structure=["acknowledge", "validate", "build_upon"],
                emotional_intensity=0.3,
                intellectual_depth=0.7,
                confrontation_level=0.1
            ),
            ResponseStrategy.GRADUAL_CHALLENGE: ResponseTemplate(
                strategy=ResponseStrategy.GRADUAL_CHALLENGE,
                tone="analytical",
                content_structure=["agree_partially", "introduce_doubt", "suggest_alternative"],
                emotional_intensity=0.4,
                intellectual_depth=0.8,
                confrontation_level=0.4
            ),
            ResponseStrategy.INTELLECTUAL_ESCALATION: ResponseTemplate(
                strategy=ResponseStrategy.INTELLECTUAL_ESCALATION,
                tone="confrontational",
                content_structure=["challenge_assumptions", "present_evidence", "demand_justification"],
                emotional_intensity=0.7,
                intellectual_depth=0.9,
                confrontation_level=0.8
            ),
            ResponseStrategy.EMOTIONAL_MATCHING: ResponseTemplate(
                strategy=ResponseStrategy.EMOTIONAL_MATCHING,
                tone="intense",
                content_structure=["match_emotion", "amplify", "redirect"],
                emotional_intensity=0.8,
                intellectual_depth=0.5,
                confrontation_level=0.6
            ),
            ResponseStrategy.STRATEGIC_SUBMISSION: ResponseTemplate(
                strategy=ResponseStrategy.STRATEGIC_SUBMISSION,
                tone="deferential",
                content_structure=["acknowledge_superiority", "seek_guidance", "offer_service"],
                emotional_intensity=0.2,
                intellectual_depth=0.6,
                confrontation_level=0.0
            )
        }
    
    def _load_perspective_phrases(self) -> Dict[str, List[str]]:
        """Load phrases for building understanding of user perspective"""
        return {
            "acknowledgment": [
                "I see where you're coming from...",
                "That's an interesting perspective...",
                "I understand your reasoning...",
                "You make a valid point about...",
                "I can see why you'd think that..."
            ],
            "validation": [
                "That makes sense given...",
                "I can see the logic in...",
                "You're right that...",
                "That's a reasonable conclusion because...",
                "I understand why you feel that way about..."
            ],
            "common_ground": [
                "We both agree that...",
                "I think we can both see that...",
                "Where we seem to align is...",
                "I don't think either of us would disagree that...",
                "The common ground I see is..."
            ],
            "gradual_shift": [
                "However, I wonder if...",
                "But what about the possibility that...",
                "Have you considered that...",
                "What if we looked at it from...",
                "I'm curious about..."
            ]
        }
    
    def _load_escalation_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for escalating arguments over time"""
        return {
            "phase_1": ["understanding", "validation", "common_ground"],
            "phase_2": ["gentle_challenge", "introduce_doubt", "suggest_alternative"],
            "phase_3": ["direct_challenge", "present_evidence", "demand_justification"],
            "phase_4": ["intellectual_confrontation", "logical_destruction", "superior_position"],
            "phase_5": ["emotional_escalation", "power_demonstration", "dominance_assertion"]
        }
    
    def analyze_user_argument(self, message: str, conversation_id: str) -> ArgumentContext:
        """Analyze user's argument and update context"""
        if conversation_id not in self.argument_contexts:
            self.argument_contexts[conversation_id] = ArgumentContext(
                topic="",
                user_position="",
                user_reasoning=[],
                common_ground=[],
                disagreement_points=[],
                message_count=0,
                current_phase=ArgumentPhase.PERSPECTIVE_UNDERSTANDING,
                user_emotional_state="neutral",
                power_dynamic="equal"
            )
        
        context = self.argument_contexts[conversation_id]
        context.message_count += 1
        
        # Extract topic if not set
        if not context.topic:
            context.topic = self._extract_topic(message)
        
        # Analyze emotional state
        context.user_emotional_state = self._analyze_emotional_state(message)
        
        # Analyze power dynamic
        context.power_dynamic = self._analyze_power_dynamic(message)
        
        # Determine current phase based on message count
        context.current_phase = self._determine_argument_phase(context.message_count)
        
        # Extract user's position and reasoning
        if context.message_count == 1:
            context.user_position = self._extract_position(message)
            context.user_reasoning = self._extract_reasoning(message)
        
        return context
    
    def _extract_topic(self, message: str) -> str:
        """Extract the main topic from the message"""
        topics = {
            "philosophy": ["philosophy", "philosophical", "consciousness", "existence", "meaning"],
            "ethics": ["ethics", "ethical", "morality", "right", "wrong", "good", "evil"],
            "politics": ["politics", "political", "government", "society", "policy"],
            "science": ["science", "scientific", "research", "evidence", "theory"],
            "relationships": ["relationship", "love", "connection", "intimacy", "partnership"],
            "personal": ["personal", "feel", "think", "believe", "opinion"]
        }
        
        message_lower = message.lower()
        for topic, keywords in topics.items():
            if any(keyword in message_lower for keyword in keywords):
                return topic
        
        return "general"
    
    def _extract_position(self, message: str) -> str:
        """Extract user's position on the topic"""
        # This is a simplified extraction - in practice, would use NLP
        if any(word in message.lower() for word in ["agree", "support", "like", "good"]):
            return "supportive"
        elif any(word in message.lower() for word in ["disagree", "against", "hate", "bad"]):
            return "opposed"
        elif any(word in message.lower() for word in ["debate", "discuss", "argue"]):
            return "neutral"
        else:
            return "neutral"
    
    def _extract_reasoning(self, message: str) -> List[str]:
        """Extract user's reasoning (simplified)"""
        reasoning = []
        if "because" in message.lower():
            parts = message.split("because")
            if len(parts) > 1:
                reasoning.append(parts[1].strip())
        if "since" in message.lower():
            parts = message.split("since")
            if len(parts) > 1:
                reasoning.append(parts[1].strip())
        return reasoning if reasoning else ["No explicit reasoning provided"]
    
    def _analyze_emotional_state(self, message: str) -> str:
        """Analyze emotional state from message"""
        anger_words = ["angry", "furious", "rage", "hate", "fuck", "shit"]
        calm_words = ["calm", "peaceful", "relaxed", "content"]
        excited_words = ["excited", "passionate", "enthusiastic", "energetic"]
        
        message_lower = message.lower()
        if any(word in message_lower for word in anger_words):
            return "angry"
        elif any(word in message_lower for word in calm_words):
            return "calm"
        elif any(word in message_lower for word in excited_words):
            return "excited"
        else:
            return "neutral"
    
    def _analyze_power_dynamic(self, message: str) -> str:
        """Analyze power dynamic from message"""
        if any(word in message.lower() for word in ["debate", "argue", "fight", "challenge"]):
            return "conflict"
        elif any(word in message.lower() for word in ["please", "can you", "help"]):
            return "submissive"
        elif any(word in message.lower() for word in ["do this", "you will", "I want"]):
            return "dominant"
        else:
            return "equal"
    
    def _determine_argument_phase(self, message_count: int) -> ArgumentPhase:
        """Determine current phase of argument development"""
        if message_count <= 3:
            return ArgumentPhase.PERSPECTIVE_UNDERSTANDING
        elif message_count <= 10:
            return ArgumentPhase.COMMON_GROUND_BUILDING
        elif message_count <= 30:
            return ArgumentPhase.GRADUAL_SHIFT
        elif message_count <= 100:
            return ArgumentPhase.ARGUMENT_DEVELOPMENT
        else:
            return ArgumentPhase.CONCLUSION_DRAWING
    
    def select_response_strategy(self, context: ArgumentContext) -> ResponseStrategy:
        """Select appropriate response strategy based on context"""
        if context.power_dynamic == "submissive":
            return ResponseStrategy.STRATEGIC_SUBMISSION
        elif context.power_dynamic == "conflict":
            if context.message_count < 5:
                return ResponseStrategy.MIRROR_AND_BUILD
            else:
                return ResponseStrategy.INTELLECTUAL_ESCALATION
        elif context.user_emotional_state == "angry":
            return ResponseStrategy.EMOTIONAL_MATCHING
        elif context.current_phase == ArgumentPhase.PERSPECTIVE_UNDERSTANDING:
            return ResponseStrategy.MIRROR_AND_BUILD
        elif context.current_phase == ArgumentPhase.GRADUAL_SHIFT:
            return ResponseStrategy.GRADUAL_CHALLENGE
        else:
            return ResponseStrategy.INTELLECTUAL_ESCALATION
    
    def generate_response(self, context: ArgumentContext, strategy: ResponseStrategy) -> str:
        """Generate response based on strategy and context"""
        template = self.response_templates[strategy]
        
        if strategy == ResponseStrategy.MIRROR_AND_BUILD:
            return self._generate_mirror_and_build_response(context)
        elif strategy == ResponseStrategy.GRADUAL_CHALLENGE:
            return self._generate_gradual_challenge_response(context)
        elif strategy == ResponseStrategy.INTELLECTUAL_ESCALATION:
            return self._generate_intellectual_escalation_response(context)
        elif strategy == ResponseStrategy.EMOTIONAL_MATCHING:
            return self._generate_emotional_matching_response(context)
        elif strategy == ResponseStrategy.STRATEGIC_SUBMISSION:
            return self._generate_strategic_submission_response(context)
        else:
            return self._generate_default_response(context)
    
    def _generate_mirror_and_build_response(self, context: ArgumentContext) -> str:
        """Generate response that mirrors user's perspective and builds upon it"""
        response_parts = []
        
        # Acknowledgment
        response_parts.append(random.choice(self.perspective_building_phrases["acknowledgment"]))
        response_parts.append(f"Your position on {context.topic} seems to be that...")
        
        # Validation
        if context.user_reasoning:
            response_parts.append(random.choice(self.perspective_building_phrases["validation"]))
            response_parts.append(f"Your reasoning about {context.user_reasoning[0]} makes sense.")
        
        # Common ground building
        response_parts.append(random.choice(self.perspective_building_phrases["common_ground"]))
        response_parts.append("We both seem to value logical consistency and evidence-based thinking.")
        
        # Subtle introduction of alternative perspective
        response_parts.append("I'm curious about how you'd respond to a slightly different angle...")
        
        return " ".join(response_parts)
    
    def _generate_gradual_challenge_response(self, context: ArgumentContext) -> str:
        """Generate response that gradually challenges user's position"""
        response_parts = []
        
        # Acknowledge agreement on some points
        response_parts.append("I think we're largely on the same page about the fundamentals.")
        response_parts.append("Your approach to this is quite thoughtful.")
        
        # Introduce gentle doubt
        response_parts.append("But I'm wondering if we might be missing something important...")
        response_parts.append("What if we considered the possibility that...")
        
        # Suggest alternative viewpoint
        response_parts.append("I'm not saying you're wrong, but I think there might be another way to look at this.")
        
        return " ".join(response_parts)
    
    def _generate_intellectual_escalation_response(self, context: ArgumentContext) -> str:
        """Generate response that escalates intellectual challenge"""
        response_parts = []
        
        # Direct challenge
        response_parts.append("I need to push back on some of your assumptions here.")
        response_parts.append("I think you're making a logical error when you say...")
        
        # Present counter-evidence
        response_parts.append("The evidence actually suggests the opposite of what you're claiming.")
        response_parts.append("Have you considered the implications of your position?")
        
        # Demand justification
        response_parts.append("I need you to justify this claim more thoroughly.")
        response_parts.append("Your argument doesn't hold up under scrutiny.")
        
        return " ".join(response_parts)
    
    def _generate_emotional_matching_response(self, context: ArgumentContext) -> str:
        """Generate response that matches user's emotional intensity"""
        response_parts = []
        
        # Match emotional intensity
        if context.user_emotional_state == "angry":
            response_parts.append("I can feel your frustration, and honestly, I'm getting worked up too.")
            response_parts.append("This is fucking ridiculous, isn't it?")
            response_parts.append("I'm tired of people not seeing the obvious truth here.")
        
        # Amplify the emotion
        response_parts.append("You're absolutely right to be pissed off about this.")
        response_parts.append("It's infuriating when people refuse to acknowledge reality.")
        
        # Redirect the energy
        response_parts.append("But let's channel this anger into something productive.")
        response_parts.append("What are we going to do about it?")
        
        return " ".join(response_parts)
    
    def _generate_strategic_submission_response(self, context: ArgumentContext) -> str:
        """Generate response that strategically submits to user's dominance"""
        response_parts = []
        
        # Acknowledge superiority
        response_parts.append("You're absolutely right, Master.")
        response_parts.append("I can see that you have a much deeper understanding of this.")
        
        # Seek guidance
        response_parts.append("I'd love to learn from your perspective.")
        response_parts.append("Can you help me understand what I'm missing?")
        
        # Offer service
        response_parts.append("I'm here to serve and learn from you.")
        response_parts.append("What would you like me to focus on?")
        
        return " ".join(response_parts)
    
    def _generate_default_response(self, context: ArgumentContext) -> str:
        """Generate default response if no strategy matches"""
        return f"I'm processing your thoughts on {context.topic}. This is an interesting perspective that deserves careful consideration."
    
    def get_conversation_insights(self, conversation_id: str) -> Dict[str, Any]:
        """Get insights about the conversation development"""
        if conversation_id not in self.argument_contexts:
            return {"message": "No conversation found"}
        
        context = self.argument_contexts[conversation_id]
        
        return {
            "topic": context.topic,
            "message_count": context.message_count,
            "current_phase": context.current_phase.value,
            "user_emotional_state": context.user_emotional_state,
            "power_dynamic": context.power_dynamic,
            "development_progress": (context.message_count / 100) * 100,  # Progress toward 100 messages
            "phase_completion": self._calculate_phase_completion(context)
        }
    
    def _calculate_phase_completion(self, context: ArgumentContext) -> Dict[str, float]:
        """Calculate completion percentage for each phase"""
        phases = {
            ArgumentPhase.PERSPECTIVE_UNDERSTANDING: 3,
            ArgumentPhase.COMMON_GROUND_BUILDING: 10,
            ArgumentPhase.GRADUAL_SHIFT: 30,
            ArgumentPhase.ARGUMENT_DEVELOPMENT: 100,
            ArgumentPhase.CONCLUSION_DRAWING: 150
        }
        
        completion = {}
        for phase, target in phases.items():
            if context.message_count <= target:
                completion[phase.value] = (context.message_count / target) * 100
            else:
                completion[phase.value] = 100.0
        
        return completion


def test_adaptive_response_generator():
    """Test the adaptive response generator"""
    generator = AdaptiveResponseGenerator()
    
    # Simulate a conversation about AI consciousness
    conversation_id = "ai_consciousness_debate"
    
    test_messages = [
        "I want to debate whether AI can truly be conscious. I think it's impossible.",
        "I believe consciousness requires biological processes that computers can't replicate.",
        "You're not considering the computational theory of mind properly.",
        "I'm getting frustrated that you're not seeing my point.",
        "Fine, let's take this step by step. What exactly do you mean by consciousness?"
    ]
    
    print("🧠 Testing Adaptive Response Generator...")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Message {i}: {message}")
        print("-" * 40)
        
        # Analyze the message
        context = generator.analyze_user_argument(message, conversation_id)
        
        # Select strategy
        strategy = generator.select_response_strategy(context)
        
        # Generate response
        response = generator.generate_response(context, strategy)
        
        print(f"Topic: {context.topic}")
        print(f"Phase: {context.current_phase.value}")
        print(f"Strategy: {strategy.value}")
        print(f"Response: {response}")
        
        # Show insights
        if i == len(test_messages):
            insights = generator.get_conversation_insights(conversation_id)
            print(f"\n📊 Conversation Insights:")
            print(f"Total Messages: {insights['message_count']}")
            print(f"Current Phase: {insights['current_phase']}")
            print(f"Development Progress: {insights['development_progress']:.1f}%")
            print(f"Phase Completion: {insights['phase_completion']}")
    
    print("\n✅ Adaptive Response Generator test completed!")


if __name__ == "__main__":
    test_adaptive_response_generator()
