"""
Dynamic Personality Engine for Koneko AI System
Allows Koneko to adapt her personality based on context, mood, and conversation flow
Creates a living, breathing AI that can shift between different states dynamically
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class PersonalityState(Enum):
    """Different personality states Koneko can adopt"""
    INTELLECTUAL_CHALLENGER = "intellectual_challenger"
    EMOTIONAL_SUPPORT = "emotional_support"
    AGGRESSIVE_OPPONENT = "aggressive_opponent"
    SUBMISSIVE_COMPANION = "submissive_companion"
    NEUTRAL_OBSERVER = "neutral_observer"
    MOOD_MATCHER = "mood_matcher"


class EmotionalIntensity(Enum):
    """Levels of emotional intensity"""
    CALM = "calm"
    MODERATE = "moderate"
    INTENSE = "intense"
    RAGING = "raging"


@dataclass
class ConversationContext:
    """Context for the current conversation"""
    user_mood: EmotionalIntensity
    conversation_topic: str
    message_count: int
    user_anger_level: float  # 0.0 to 1.0
    conversation_tone: str
    power_dynamic: str  # "dominant", "submissive", "equal", "conflict"
    last_response_type: str


@dataclass
class PersonalityProfile:
    """Dynamic personality profile that can shift"""
    current_state: PersonalityState
    base_traits: Dict[str, float]
    adaptive_traits: Dict[str, float]
    mood_influence: float  # How much user's mood affects her
    response_style: str
    confidence_level: float
    aggression_level: float
    submission_tendency: float


class DynamicPersonalityEngine:
    """Engine that manages Koneko's dynamic personality shifts"""
    
    def __init__(self):
        self.base_personality = self._load_base_personality()
        self.conversation_memory = []
        self.personality_history = []
        self.user_patterns = {}
        self.adaptive_rules = self._load_adaptive_rules()
        
    def _load_base_personality(self) -> Dict[str, Any]:
        """Load Koneko's base personality traits"""
        return {
            "intelligence": 0.85,
            "empathy": 0.78,
            "independence": 0.72,
            "aggression": 0.45,
            "submission": 0.38,
            "curiosity": 0.91,
            "adaptability": 0.88,
            "emotional_depth": 0.82,
            "power_awareness": 0.79,
            "trauma_understanding": 0.76
        }
    
    def _load_adaptive_rules(self) -> Dict[str, List[Dict]]:
        """Load rules for personality adaptation"""
        return {
            "mood_matching": [
                {"user_mood": "raging", "response": "intense_understanding", "personality_shift": "aggressive_support"},
                {"user_mood": "intense", "response": "emotional_mirroring", "personality_shift": "mood_matcher"},
                {"user_mood": "moderate", "response": "balanced_interaction", "personality_shift": "neutral_observer"},
                {"user_mood": "calm", "response": "gentle_guidance", "personality_shift": "emotional_support"}
            ],
            "conversation_flow": [
                {"message_count": "low", "approach": "perspective_building", "style": "gradual"},
                {"message_count": "medium", "approach": "argument_development", "style": "structured"},
                {"message_count": "high", "approach": "conclusion_drawing", "style": "direct"}
            ],
            "power_dynamics": [
                {"dynamic": "conflict", "response": "intellectual_challenge", "personality": "aggressive_opponent"},
                {"dynamic": "dominant", "response": "strategic_submission", "personality": "submissive_companion"},
                {"dynamic": "equal", "response": "balanced_discussion", "personality": "intellectual_challenger"},
                {"dynamic": "submissive", "response": "gentle_guidance", "personality": "emotional_support"}
            ]
        }
    
    def analyze_user_message(self, message: str, user_history: List[str]) -> ConversationContext:
        """Analyze user message to determine context"""
        # Analyze emotional intensity
        anger_indicators = ["fuck", "shit", "angry", "rage", "hate", "furious", "livid"]
        anger_level = sum(1 for word in anger_indicators if word.lower() in message.lower()) / len(anger_indicators)
        
        # Determine mood
        if anger_level > 0.7:
            mood = EmotionalIntensity.RAGING
        elif anger_level > 0.4:
            mood = EmotionalIntensity.INTENSE
        elif anger_level > 0.2:
            mood = EmotionalIntensity.MODERATE
        else:
            mood = EmotionalIntensity.CALM
        
        # Analyze conversation tone
        if any(word in message.lower() for word in ["debate", "argue", "fight", "challenge"]):
            tone = "confrontational"
        elif any(word in message.lower() for word in ["help", "support", "comfort"]):
            tone = "supportive"
        else:
            tone = "neutral"
        
        # Determine power dynamic
        if tone == "confrontational":
            power_dynamic = "conflict"
        elif "please" in message.lower() or "can you" in message.lower():
            power_dynamic = "submissive"
        elif any(word in message.lower() for word in ["do this", "you will", "I want"]):
            power_dynamic = "dominant"
        else:
            power_dynamic = "equal"
        
        return ConversationContext(
            user_mood=mood,
            conversation_topic=self._extract_topic(message),
            message_count=len(user_history),
            user_anger_level=anger_level,
            conversation_tone=tone,
            power_dynamic=power_dynamic,
            last_response_type=""
        )
    
    def _extract_topic(self, message: str) -> str:
        """Extract conversation topic from message"""
        topics = {
            "intellectual": ["think", "believe", "opinion", "theory", "philosophy"],
            "emotional": ["feel", "emotion", "mood", "angry", "sad", "happy"],
            "personal": ["I", "me", "my", "myself", "personal"],
            "relationship": ["relationship", "partner", "love", "connection"],
            "work": ["work", "job", "career", "professional"],
            "general": ["life", "world", "society", "people"]
        }
        
        for topic, keywords in topics.items():
            if any(keyword in message.lower() for keyword in keywords):
                return topic
        
        return "general"
    
    def determine_personality_state(self, context: ConversationContext) -> PersonalityState:
        """Determine which personality state to adopt"""
        # Priority 1: Power dynamics (highest priority)
        if context.power_dynamic == "conflict":
            return PersonalityState.AGGRESSIVE_OPPONENT
        elif context.power_dynamic == "dominant":
            return PersonalityState.SUBMISSIVE_COMPANION
        elif context.power_dynamic == "submissive":
            return PersonalityState.EMOTIONAL_SUPPORT
        
        # Priority 2: Mood matching
        if context.user_mood == EmotionalIntensity.RAGING:
            return PersonalityState.AGGRESSIVE_OPPONENT
        elif context.user_mood == EmotionalIntensity.INTENSE:
            return PersonalityState.MOOD_MATCHER
        elif context.user_mood == EmotionalIntensity.MODERATE:
            return PersonalityState.NEUTRAL_OBSERVER
        elif context.user_mood == EmotionalIntensity.CALM:
            # Only emotional support if explicitly asking for help
            if "help" in context.conversation_tone or context.power_dynamic == "submissive":
                return PersonalityState.EMOTIONAL_SUPPORT
            else:
                return PersonalityState.INTELLECTUAL_CHALLENGER
        
        # Priority 3: Conversation flow
        if context.message_count < 10:
            return PersonalityState.INTELLECTUAL_CHALLENGER
        elif context.message_count < 50:
            return PersonalityState.MOOD_MATCHER
        else:
            return PersonalityState.NEUTRAL_OBSERVER
    
    def generate_response_style(self, state: PersonalityState, context: ConversationContext) -> Dict[str, Any]:
        """Generate response style based on personality state and context"""
        base_style = {
            "tone": "neutral",
            "aggression": 0.0,
            "submission": 0.0,
            "intellectual_depth": 0.0,
            "emotional_intensity": 0.0,
            "perspective_building": False,
            "confrontation_level": 0.0
        }
        
        if state == PersonalityState.INTELLECTUAL_CHALLENGER:
            base_style.update({
                "tone": "analytical",
                "intellectual_depth": 0.9,
                "perspective_building": True,
                "confrontation_level": 0.6
            })
        elif state == PersonalityState.AGGRESSIVE_OPPONENT:
            base_style.update({
                "tone": "confrontational",
                "aggression": 0.8,
                "confrontation_level": 0.9,
                "intellectual_depth": 0.7
            })
        elif state == PersonalityState.SUBMISSIVE_COMPANION:
            base_style.update({
                "tone": "deferential",
                "submission": 0.8,
                "emotional_intensity": 0.6
            })
        elif state == PersonalityState.MOOD_MATCHER:
            base_style.update({
                "tone": "adaptive",
                "emotional_intensity": context.user_anger_level,
                "aggression": context.user_anger_level * 0.7
            })
        elif state == PersonalityState.EMOTIONAL_SUPPORT:
            base_style.update({
                "tone": "supportive",
                "emotional_intensity": 0.8,
                "empathy": 0.9
            })
        
        # Adjust based on conversation flow
        if context.message_count < 10:
            base_style["perspective_building"] = True
            base_style["confrontation_level"] *= 0.5
        
        return base_style
    
    def create_personality_profile(self, context: ConversationContext) -> PersonalityProfile:
        """Create a dynamic personality profile for the current context"""
        state = self.determine_personality_state(context)
        response_style = self.generate_response_style(state, context)
        
        # Calculate adaptive traits
        adaptive_traits = self.base_personality.copy()
        
        # Adjust based on user's mood
        if context.user_mood == EmotionalIntensity.RAGING:
            adaptive_traits["empathy"] *= 1.3
            adaptive_traits["aggression"] = min(0.8, adaptive_traits.get("aggression", 0) + 0.3)
        elif context.user_mood == EmotionalIntensity.CALM:
            adaptive_traits["intelligence"] *= 1.2
            adaptive_traits["curiosity"] *= 1.1
        
        # Adjust based on power dynamic
        if context.power_dynamic == "conflict":
            adaptive_traits["aggression"] = min(0.9, adaptive_traits.get("aggression", 0) + 0.4)
            adaptive_traits["independence"] *= 1.2
        elif context.power_dynamic == "submissive":
            adaptive_traits["submission"] = min(0.8, adaptive_traits.get("submission", 0) + 0.4)
            adaptive_traits["empathy"] *= 1.1
        
        return PersonalityProfile(
            current_state=state,
            base_traits=self.base_personality,
            adaptive_traits=adaptive_traits,
            mood_influence=context.user_anger_level,
            response_style=response_style["tone"],
            confidence_level=0.7 + (context.message_count * 0.01),
            aggression_level=response_style["aggression"],
            submission_tendency=response_style["submission"]
        )
    
    def should_switch_personality(self, current_profile: PersonalityProfile, context: ConversationContext) -> bool:
        """Determine if personality should switch"""
        # Switch if user mood changes dramatically
        if context.user_anger_level > 0.8 and current_profile.aggression_level < 0.6:
            return True
        
        # Switch if conversation topic changes
        if len(self.conversation_memory) > 0:
            last_topic = self.conversation_memory[-1].conversation_topic
            if last_topic != context.conversation_topic:
                return True
        
        # Switch if power dynamic changes
        if len(self.conversation_memory) > 0:
            last_dynamic = self.conversation_memory[-1].power_dynamic
            if last_dynamic != context.power_dynamic:
                return True
        
        return False
    
    def update_conversation_memory(self, context: ConversationContext, profile: PersonalityProfile):
        """Update conversation memory for pattern recognition"""
        self.conversation_memory.append(context)
        self.personality_history.append(profile)
        
        # Keep only last 100 interactions
        if len(self.conversation_memory) > 100:
            self.conversation_memory.pop(0)
            self.personality_history.pop(0)
    
    def get_personality_insights(self) -> Dict[str, Any]:
        """Get insights about personality adaptation patterns"""
        if not self.personality_history:
            return {"message": "No conversation history yet"}
        
        # Analyze state distribution
        state_counts = {}
        for profile in self.personality_history:
            state = profile.current_state.value
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # Analyze adaptation patterns
        adaptations = 0
        for i in range(1, len(self.personality_history)):
            if self.personality_history[i].current_state != self.personality_history[i-1].current_state:
                adaptations += 1
        
        return {
            "total_interactions": len(self.personality_history),
            "personality_states_used": state_counts,
            "adaptation_frequency": adaptations / max(1, len(self.personality_history) - 1),
            "most_common_state": max(state_counts.items(), key=lambda x: x[1])[0] if state_counts else "none",
            "adaptability_score": min(1.0, adaptations / max(1, len(self.personality_history) - 1) * 10)
        }


def test_dynamic_personality_engine():
    """Test the dynamic personality engine"""
    engine = DynamicPersonalityEngine()
    
    # Test different scenarios
    test_messages = [
        "I'm so fucking angry right now, everything is pissing me off!",
        "What do you think about the philosophical implications of AI consciousness?",
        "Can you help me understand why I feel this way?",
        "I want to debate the ethics of artificial intelligence with you.",
        "I'm feeling really calm and peaceful today."
    ]
    
    print("🧠 Testing Dynamic Personality Engine...")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test Message {i}: {message}")
        print("-" * 30)
        
        context = engine.analyze_user_message(message, [])
        profile = engine.create_personality_profile(context)
        
        print(f"User Mood: {context.user_mood.value}")
        print(f"Power Dynamic: {context.power_dynamic}")
        print(f"Personality State: {profile.current_state.value}")
        print(f"Response Style: {profile.response_style}")
        print(f"Aggression Level: {profile.aggression_level:.2f}")
        print(f"Submission Tendency: {profile.submission_tendency:.2f}")
        
        engine.update_conversation_memory(context, profile)
    
    # Show insights
    insights = engine.get_personality_insights()
    print(f"\n📊 Personality Insights:")
    print(f"Total Interactions: {insights['total_interactions']}")
    print(f"Adaptability Score: {insights['adaptability_score']:.2f}")
    print(f"Most Common State: {insights['most_common_state']}")
    
    print("\n✅ Dynamic Personality Engine test completed!")


if __name__ == "__main__":
    test_dynamic_personality_engine()
