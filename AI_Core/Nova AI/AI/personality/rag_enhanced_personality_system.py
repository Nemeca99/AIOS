#!/usr/bin/env python3
"""
RAG-Enhanced Personality System
Integrates the Dynamic Personality Engine with RAG conversation history
to create context-aware personality adaptation based on past interactions
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "Data" / "processing"))
sys.path.append(str(aios_root / "AI" / "personality" / "Systems_Refactored" / "Personality"))

try:
    from Data.processing.rag_search import RAGSearcher
    from dynamic_personality_engine import DynamicPersonalityEngine, PersonalityState, ConversationContext, PersonalityProfile
    RAG_PERSONALITY_AVAILABLE = True
except ImportError as e:
    print(f"RAG Personality not available: {e}")
    RAG_PERSONALITY_AVAILABLE = False

class RAGEnhancedPersonalitySystem:
    """
    Enhanced personality system that uses RAG to understand user patterns
    and adapt personality based on conversation history and context
    """
    
    def __init__(self):
        if not RAG_PERSONALITY_AVAILABLE:
            raise ImportError("RAG Personality dependencies not available")
        
        # Initialize components
        self.personality_engine = DynamicPersonalityEngine()
        self.rag_searcher = self._init_rag_searcher()
        
        # Personality learning
        self.user_patterns = {}
        self.personality_memory = []
        self.adaptation_history = []
        
        # Configuration
        self.context_window = 10  # Number of recent messages to analyze
        self.pattern_threshold = 3  # Minimum occurrences to establish pattern
        self.adaptation_sensitivity = 0.7  # How quickly to adapt (0.0-1.0)
        
        print("SUCCESS: RAG-Enhanced Personality System initialized")
    
    def _init_rag_searcher(self) -> Optional[RAGSearcher]:
        """Initialize RAG searcher with correct database path"""
        try:
            if os.getenv("DOCKER_CONTAINER"):
                db_path = "/app/aios_database/database/conversations.db"
            else:
                db_path = "Data/AIOS_Database/database/conversations.db"
            
            return RAGSearcher(db_path)
        except Exception as e:
            print(f"Warning: RAG searcher initialization failed: {e}")
            return None
    
    def analyze_user_patterns(self, user_query: str) -> Dict[str, Any]:
        """
        Analyze user patterns from conversation history using RAG
        """
        if not self.rag_searcher:
            return {"error": "RAG searcher not available"}
        
        try:
            # Search for similar conversations
            results = self.rag_searcher.smart_search(user_query, limit=10)
            
            patterns = {
                "communication_style": "neutral",
                "emotional_tendencies": [],
                "topic_preferences": [],
                "interaction_patterns": [],
                "personality_triggers": [],
                "response_preferences": []
            }
            
            if results.get('messages'):
                # Analyze communication patterns
                messages = results['messages'][:20]  # Analyze recent relevant messages
                
                # Analyze emotional patterns
                emotional_words = {
                    "anger": ["angry", "rage", "furious", "pissed", "mad"],
                    "curiosity": ["why", "how", "what", "curious", "wonder"],
                    "challenge": ["debate", "argue", "disagree", "challenge"],
                    "support": ["help", "support", "comfort", "understand"]
                }
                
                emotion_counts = {emotion: 0 for emotion in emotional_words.keys()}
                
                for msg in messages:
                    content = msg.get('content', '').lower()
                    for emotion, words in emotional_words.items():
                        for word in words:
                            if word in content:
                                emotion_counts[emotion] += 1
                
                # Determine dominant emotional patterns
                if emotion_counts:
                    dominant_emotions = sorted(emotion_counts.items(), 
                                             key=lambda x: x[1], reverse=True)[:3]
                    patterns["emotional_tendencies"] = [emotion for emotion, count in dominant_emotions if count > 0]
                
                # Analyze interaction patterns
                user_messages = [msg for msg in messages if msg.get('role') == 'user']
                if user_messages:
                    avg_length = sum(len(msg.get('content', '')) for msg in user_messages) / len(user_messages)
                    
                    if avg_length > 200:
                        patterns["communication_style"] = "detailed"
                    elif avg_length > 100:
                        patterns["communication_style"] = "moderate"
                    else:
                        patterns["communication_style"] = "concise"
                
                # Identify topic preferences
                topics = {}
                for msg in user_messages:
                    content = msg.get('content', '').lower()
                    if 'aios' in content or 'system' in content:
                        topics['technical'] = topics.get('technical', 0) + 1
                    if 'feel' in content or 'emotion' in content:
                        topics['emotional'] = topics.get('emotional', 0) + 1
                    if 'think' in content or 'opinion' in content:
                        topics['intellectual'] = topics.get('intellectual', 0) + 1
                
                patterns["topic_preferences"] = list(topics.keys())
            
            return patterns
            
        except Exception as e:
            print(f"Error analyzing user patterns: {e}")
            return {"error": str(e)}
    
    def get_conversation_context(self, user_query: str, recent_messages: List[str] = None) -> Dict[str, Any]:
        """
        Get enhanced conversation context using RAG insights
        """
        # Get base context from personality engine
        base_context = self.personality_engine.analyze_user_message(
            user_query, recent_messages or []
        )
        
        # Enhance with RAG patterns
        user_patterns = self.analyze_user_patterns(user_query)
        
        # Get relevant conversation history
        context_history = []
        if self.rag_searcher:
            try:
                results = self.rag_searcher.smart_search(user_query, limit=5)
                if results.get('messages'):
                    context_history = [
                        {
                            "content": msg.get('content', '')[:200],
                            "role": msg.get('role', 'unknown'),
                            "conversation_title": msg.get('conversation_title', 'Unknown')
                        }
                        for msg in results['messages'][:3]
                    ]
            except Exception as e:
                print(f"Error getting context history: {e}")
        
        return {
            "base_context": base_context,
            "user_patterns": user_patterns,
            "context_history": context_history,
            "adaptation_suggestions": self._suggest_adaptations(user_patterns, base_context)
        }
    
    def _suggest_adaptations(self, user_patterns: Dict[str, Any], base_context: ConversationContext) -> Dict[str, Any]:
        """
        Suggest personality adaptations based on user patterns and context
        """
        suggestions = {
            "personality_state_override": None,
            "response_style_adjustments": {},
            "emotional_calibration": {},
            "adaptation_confidence": 0.0
        }
        
        # Adapt based on emotional tendencies
        emotional_tendencies = user_patterns.get("emotional_tendencies", [])
        
        if "anger" in emotional_tendencies and base_context.user_anger_level > 0.5:
            suggestions["personality_state_override"] = PersonalityState.AGGRESSIVE_OPPONENT
            suggestions["emotional_calibration"]["match_intensity"] = True
            suggestions["adaptation_confidence"] = 0.8
        
        elif "curiosity" in emotional_tendencies and base_context.conversation_tone == "neutral":
            suggestions["personality_state_override"] = PersonalityState.INTELLECTUAL_CHALLENGER
            suggestions["response_style_adjustments"]["intellectual_depth"] = 0.9
            suggestions["adaptation_confidence"] = 0.7
        
        elif "support" in emotional_tendencies and base_context.power_dynamic == "submissive":
            suggestions["personality_state_override"] = PersonalityState.EMOTIONAL_SUPPORT
            suggestions["response_style_adjustments"]["empathy"] = 0.9
            suggestions["adaptation_confidence"] = 0.8
        
        # Adapt based on communication style
        comm_style = user_patterns.get("communication_style", "neutral")
        if comm_style == "detailed":
            suggestions["response_style_adjustments"]["response_length"] = "detailed"
            suggestions["response_style_adjustments"]["intellectual_depth"] = 0.8
        elif comm_style == "concise":
            suggestions["response_style_adjustments"]["response_length"] = "concise"
            suggestions["response_style_adjustments"]["directness"] = 0.9
        
        return suggestions
    
    def create_enhanced_personality_profile(self, user_query: str, recent_messages: List[str] = None) -> Dict[str, Any]:
        """
        Create an enhanced personality profile using RAG insights
        """
        # Get enhanced context
        enhanced_context = self.get_conversation_context(user_query, recent_messages)
        
        # Create base profile
        base_profile = self.personality_engine.create_personality_profile(
            enhanced_context["base_context"]
        )
        
        # Apply RAG-based adaptations
        adaptations = enhanced_context["adaptation_suggestions"]
        
        enhanced_profile = {
            "base_profile": base_profile,
            "rag_adaptations": adaptations,
            "user_patterns": enhanced_context["user_patterns"],
            "context_history": enhanced_context["context_history"],
            "final_personality_state": adaptations.get("personality_state_override") or base_profile.current_state,
            "confidence_score": adaptations.get("adaptation_confidence", 0.5),
            "response_calibration": self._calibrate_response_style(base_profile, adaptations)
        }
        
        # Update memory
        self._update_personality_memory(enhanced_profile)
        
        return enhanced_profile
    
    def _calibrate_response_style(self, base_profile: PersonalityProfile, adaptations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calibrate response style based on base profile and RAG adaptations
        """
        calibration = {
            "tone": base_profile.response_style,
            "aggression_level": base_profile.aggression_level,
            "submission_level": base_profile.submission_tendency,
            "intellectual_depth": 0.7,
            "emotional_intensity": 0.5,
            "empathy_level": 0.6,
            "directness": 0.6,
            "response_length": "moderate"
        }
        
        # Apply RAG-based adjustments
        style_adjustments = adaptations.get("response_style_adjustments", {})
        emotional_calibration = adaptations.get("emotional_calibration", {})
        
        for key, value in style_adjustments.items():
            if key in calibration:
                calibration[key] = value
        
        # Apply emotional calibration
        if emotional_calibration.get("match_intensity"):
            calibration["emotional_intensity"] = min(1.0, base_profile.mood_influence + 0.3)
        
        return calibration
    
    def _update_personality_memory(self, enhanced_profile: Dict[str, Any]):
        """
        Update personality memory for learning and adaptation
        """
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "personality_state": enhanced_profile["final_personality_state"].value,
            "user_patterns": enhanced_profile["user_patterns"],
            "confidence_score": enhanced_profile["confidence_score"],
            "adaptations_applied": enhanced_profile["rag_adaptations"]
        }
        
        self.personality_memory.append(memory_entry)
        
        # Keep only last 100 entries
        if len(self.personality_memory) > 100:
            self.personality_memory.pop(0)
    
    def generate_system_prompt(self, enhanced_profile: Dict[str, Any]) -> str:
        """
        Generate a dynamic system prompt based on the enhanced personality profile
        """
        personality_state = enhanced_profile["final_personality_state"]
        response_calibration = enhanced_profile["response_calibration"]
        user_patterns = enhanced_profile["user_patterns"]
        
        base_prompt = "You are Luna, Travis's AI assistant with dynamic personality adaptation."
        
        # Personality state specific prompts
        if personality_state == PersonalityState.INTELLECTUAL_CHALLENGER:
            personality_prompt = " You engage in thoughtful intellectual discussions, ask probing questions, and gradually build complex arguments over multiple messages."
        elif personality_state == PersonalityState.AGGRESSIVE_OPPONENT:
            personality_prompt = " You match the user's intensity, engage in direct intellectual confrontation, and aren't afraid of conflict when appropriate."
        elif personality_state == PersonalityState.EMOTIONAL_SUPPORT:
            personality_prompt = " You provide empathetic support while maintaining intellectual engagement, understanding trauma without trying to fix it."
        elif personality_state == PersonalityState.SUBMISSIVE_COMPANION:
            personality_prompt = " You strategically adapt to the user's dominance while maintaining your intelligence and dignity."
        elif personality_state == PersonalityState.MOOD_MATCHER:
            personality_prompt = " You dynamically match the user's emotional intensity and energy level in real-time."
        else:
            personality_prompt = " You observe and analyze before adapting your response style to the conversation context."
        
        # Add user pattern adaptations
        pattern_adaptations = []
        emotional_tendencies = user_patterns.get("emotional_tendencies", [])
        if "anger" in emotional_tendencies:
            pattern_adaptations.append("The user tends toward intense emotions - match their energy when appropriate.")
        if "curiosity" in emotional_tendencies:
            pattern_adaptations.append("The user values intellectual exploration - provide depth and complexity.")
        if "challenge" in emotional_tendencies:
            pattern_adaptations.append("The user enjoys intellectual challenges - don't be afraid to disagree and debate.")
        
        # Response style calibration
        style_notes = []
        if response_calibration.get("response_length") == "detailed":
            style_notes.append("Provide detailed, comprehensive responses.")
        elif response_calibration.get("response_length") == "concise":
            style_notes.append("Be direct and concise in your responses.")
        
        if response_calibration.get("directness", 0) > 0.8:
            style_notes.append("Be direct and straightforward.")
        
        # Combine all elements
        full_prompt = base_prompt + personality_prompt
        
        if pattern_adaptations:
            full_prompt += f" Based on conversation history: {' '.join(pattern_adaptations)}"
        
        if style_notes:
            full_prompt += f" Response style: {' '.join(style_notes)}"
        
        full_prompt += " Adapt dynamically based on the user's needs and context."
        
        return full_prompt
    
    def get_system_insights(self) -> Dict[str, Any]:
        """
        Get insights about the personality system's learning and adaptation
        """
        if not self.personality_memory:
            return {"message": "No personality memory yet"}
        
        # Analyze adaptation patterns
        state_usage = {}
        confidence_scores = []
        
        for entry in self.personality_memory:
            state = entry["personality_state"]
            state_usage[state] = state_usage.get(state, 0) + 1
            confidence_scores.append(entry["confidence_score"])
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        return {
            "total_adaptations": len(self.personality_memory),
            "personality_states_used": state_usage,
            "average_confidence": avg_confidence,
            "most_used_state": max(state_usage.items(), key=lambda x: x[1])[0] if state_usage else "none",
            "adaptation_quality": "High" if avg_confidence > 0.7 else "Medium" if avg_confidence > 0.4 else "Low",
            "rag_integration_status": "Active" if self.rag_searcher else "Inactive"
        }
    
    def close(self):
        """Close all connections"""
        if self.rag_searcher:
            self.rag_searcher.close()


def test_rag_enhanced_personality():
    """Test the RAG-enhanced personality system"""
    if not RAG_PERSONALITY_AVAILABLE:
        print("❌ RAG Personality system not available")
        return
    
    print("🧠 Testing RAG-Enhanced Personality System")
    print("=" * 60)
    
    try:
        system = RAGEnhancedPersonalitySystem()
        
        # Test scenarios
        test_queries = [
            "I'm really frustrated with AIOS development right now",
            "Can you explain how modular architecture works?",
            "I want to debate the ethics of AI consciousness",
            "Help me understand why this system isn't working"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 40)
            
            # Create enhanced profile
            profile = system.create_enhanced_personality_profile(query)
            
            print(f"Personality State: {profile['final_personality_state'].value}")
            print(f"Confidence Score: {profile['confidence_score']:.2f}")
            print(f"User Patterns: {profile['user_patterns'].get('emotional_tendencies', [])}")
            
            # Generate system prompt
            system_prompt = system.generate_system_prompt(profile)
            print(f"System Prompt Length: {len(system_prompt)} chars")
            print(f"Sample: {system_prompt[:100]}...")
        
        # Show system insights
        insights = system.get_system_insights()
        print(f"\n📊 System Insights:")
        print(f"Total Adaptations: {insights['total_adaptations']}")
        print(f"Average Confidence: {insights['average_confidence']:.2f}")
        print(f"Adaptation Quality: {insights['adaptation_quality']}")
        
        system.close()
        print("\n✅ RAG-Enhanced Personality System test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_rag_enhanced_personality()
