#!/usr/bin/env python3
"""
Luna Context-Aware Response System
Complete integration of RAG + Personality + LM Studio for dynamic AI responses
"""

import sys
import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "Data" / "processing"))
sys.path.append(str(aios_root / "AI" / "personality"))

try:
    from rag_enhanced_personality_system import RAGEnhancedPersonalitySystem
    LUNA_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Luna system not available: {e}")
    LUNA_SYSTEM_AVAILABLE = False

class LunaContextAwareSystem:
    """
    Complete Luna AI system with context-aware personality and response generation
    """
    
    def __init__(self):
        if not LUNA_SYSTEM_AVAILABLE:
            raise ImportError("Luna system dependencies not available")
        
        # Initialize personality system
        self.personality_system = RAGEnhancedPersonalitySystem()
        
        # LM Studio configuration
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.model_name = "mistral-nemo-instruct-2407-abliterated@q8_0"
        
        # Response configuration
        self.max_tokens = 300
        self.temperature = 0.7
        
        # Session memory
        self.conversation_history = []
        self.session_context = {}
        
        print("✅ Luna Context-Aware System initialized")
    
    def is_lm_studio_available(self) -> bool:
        """Check if LM Studio is running and accessible"""
        try:
            response = requests.get("http://localhost:1234", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_context_aware_response(self, user_query: str, mode: str = "chat") -> Dict[str, Any]:
        """
        Generate a context-aware response using personality adaptation and RAG insights
        """
        try:
            # Step 1: Create enhanced personality profile
            recent_messages = [msg["content"] for msg in self.conversation_history[-10:]]
            enhanced_profile = self.personality_system.create_enhanced_personality_profile(
                user_query, recent_messages
            )
            
            # Step 2: Generate dynamic system prompt
            system_prompt = self.personality_system.generate_system_prompt(enhanced_profile)
            
            # Step 3: Get LM Studio response
            ai_response = self._get_lm_studio_response(user_query, system_prompt)
            
            # Step 4: Update conversation history
            self._update_conversation_history(user_query, ai_response, enhanced_profile)
            
            return {
                "response": ai_response,
                "personality_state": enhanced_profile["final_personality_state"].value,
                "confidence_score": enhanced_profile["confidence_score"],
                "user_patterns": enhanced_profile["user_patterns"],
                "context_used": len(enhanced_profile["context_history"]),
                "system_prompt_length": len(system_prompt),
                "adaptation_quality": enhanced_profile.get("adaptation_quality", "Unknown")
            }
            
        except Exception as e:
            return {
                "response": f"Error generating context-aware response: {e}",
                "error": str(e)
            }
    
    def _get_lm_studio_response(self, user_query: str, system_prompt: str) -> str:
        """Get response from LM Studio with dynamic system prompt"""
        if not self.is_lm_studio_available():
            return "LM Studio not available - using fallback response."
        
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": False
            }
            
            response = requests.post(self.lm_studio_url, json=payload, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"LM Studio error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"LM Studio error: {e}"
    
    def _update_conversation_history(self, user_query: str, ai_response: str, enhanced_profile: Dict[str, Any]):
        """Update conversation history with context metadata"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_query,
            "ai_response": ai_response,
            "personality_state": enhanced_profile["final_personality_state"].value,
            "confidence_score": enhanced_profile["confidence_score"],
            "context_used": len(enhanced_profile["context_history"])
        }
        
        self.conversation_history.append(entry)
        
        # Keep last 50 messages
        if len(self.conversation_history) > 50:
            self.conversation_history.pop(0)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        if not self.conversation_history:
            return {"message": "No conversation history in this session"}
        
        # Analyze session patterns
        personality_states = [entry["personality_state"] for entry in self.conversation_history]
        state_counts = {}
        for state in personality_states:
            state_counts[state] = state_counts.get(state, 0) + 1
        
        avg_confidence = sum(entry["confidence_score"] for entry in self.conversation_history) / len(self.conversation_history)
        
        return {
            "session_length": len(self.conversation_history),
            "personality_states_used": state_counts,
            "average_confidence": avg_confidence,
            "dominant_personality": max(state_counts.items(), key=lambda x: x[1])[0] if state_counts else "none",
            "adaptation_quality": "High" if avg_confidence > 0.7 else "Medium" if avg_confidence > 0.4 else "Low",
            "context_usage": sum(entry["context_used"] for entry in self.conversation_history)
        }
    
    def close(self):
        """Close all connections"""
        self.personality_system.close()


def test_luna_context_system():
    """Test the complete Luna context-aware system"""
    if not LUNA_SYSTEM_AVAILABLE:
        print("❌ Luna system not available")
        return
    
    print("🌙 Testing Luna Context-Aware System")
    print("=" * 60)
    
    try:
        luna = LunaContextAwareSystem()
        
        # Check LM Studio
        if luna.is_lm_studio_available():
            print("✅ LM Studio is available")
        else:
            print("⚠️ LM Studio not available - responses will be limited")
        
        # Test conversation scenarios
        test_scenarios = [
            ("Technical question", "How does the AIOS modular architecture work?"),
            ("Emotional query", "I'm feeling frustrated with this development"),
            ("Challenge request", "I want to debate AI consciousness with you")
        ]
        
        for scenario_name, query in test_scenarios:
            print(f"\n🔍 Scenario: {scenario_name}")
            print(f"Query: {query}")
            print("-" * 40)
            
            result = luna.generate_context_aware_response(query)
            
            print(f"Personality State: {result.get('personality_state', 'unknown')}")
            print(f"Confidence: {result.get('confidence_score', 0):.2f}")
            print(f"Context Used: {result.get('context_used', 0)} historical messages")
            print(f"Response: {result['response'][:200]}...")
        
        # Session summary
        summary = luna.get_session_summary()
        print(f"\n📊 Session Summary:")
        print(f"Messages: {summary['session_length']}")
        print(f"Dominant Personality: {summary['dominant_personality']}")
        print(f"Adaptation Quality: {summary['adaptation_quality']}")
        
        luna.close()
        print("\n✅ Luna Context-Aware System test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_luna_context_system()
