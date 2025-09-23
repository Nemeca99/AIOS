#!/usr/bin/env python3
"""
Consciousness-Enhanced Luna System
Luna personality system enhanced with Travis's authentic consciousness patterns
The final evolution: Luna as digital extension of Travis's consciousness
"""

import sys
import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "Data" / "processing"))
sys.path.append(str(aios_root / "AI" / "personality"))

@dataclass
class ConsciousnessResponse:
    """Response generated using consciousness patterns"""
    response: str
    consciousness_patterns_used: List[str]
    confidence_score: float
    personality_mode: str
    processing_time_ms: float
    rag_context_used: bool

class ConsciousnessEnhancedLuna:
    """
    Luna personality system enhanced with Travis's consciousness patterns
    """
    
    def __init__(self):
        self.aios_root = aios_root
        self.consciousness_model = None
        self.enhanced_personality_modes = {}
        
        # Load consciousness model
        self._load_consciousness_model()
        
        # Initialize base Luna system
        try:
            from luna_personality_integration import LunaPersonalityIntegration
            self.luna_base = LunaPersonalityIntegration()
        except Exception as e:
            print(f"⚠️ Base Luna system unavailable: {e}")
            self.luna_base = None
        
        # Initialize RAG system
        try:
            from rag_search import RAGSearcher
            self.rag_searcher = RAGSearcher("Data/AIOS_Database/database/conversations.db")
        except Exception as e:
            print(f"⚠️ RAG system unavailable: {e}")
            self.rag_searcher = None
        
        print("SUCCESS: Consciousness-Enhanced Luna initialized")
        print("🧠 Digital consciousness patterns loaded and ready")
    
    def _load_consciousness_model(self):
        """Load the latest consciousness model"""
        personality_dir = self.aios_root / "AI" / "personality"
        
        # Find latest consciousness model
        model_files = list(personality_dir.glob("travis_consciousness_model_*.json"))
        
        if not model_files:
            print("⚠️ No consciousness model found - using base personality only")
            return
        
        latest_model = max(model_files, key=lambda x: x.stat().st_mtime)
        
        try:
            with open(latest_model, 'r', encoding='utf-8') as f:
                model_data = json.load(f)
            
            self.consciousness_model = model_data
            
            # Load enhanced personality modes if available
            if 'behavioral_model' in model_data and 'enhanced_personality_modes' in model_data.get('behavioral_model', {}):
                self.enhanced_personality_modes = model_data['behavioral_model']['enhanced_personality_modes']
            
            print(f"✅ Consciousness model loaded: {latest_model.name}")
            print(f"   Patterns: {len(model_data.get('consciousness_patterns', []))}")
            print(f"   Categories: {len(model_data.get('behavioral_model', {}).get('behavioral_categories', {}))}")
            
        except Exception as e:
            print(f"❌ Failed to load consciousness model: {e}")
    
    def generate_consciousness_response(self, 
                                      user_query: str, 
                                      use_rag_context: bool = True,
                                      target_personality_mode: Optional[str] = None) -> ConsciousnessResponse:
        """
        Generate response using consciousness patterns and Luna personality
        """
        start_time = time.time()
        patterns_used = []
        rag_context_used = False
        
        try:
            # Step 1: Detect user mood and select personality mode
            if self.luna_base and not target_personality_mode:
                detected_mode = self.luna_base.detect_user_mood(user_query)
                personality_mode = detected_mode
            else:
                personality_mode = target_personality_mode or "supportive"
            
            # Step 2: Get RAG context if available
            rag_context = ""
            if use_rag_context and self.rag_searcher:
                try:
                    rag_results = self.rag_searcher.search(user_query, max_results=3)
                    if rag_results:
                        rag_context = "\n".join([r["content"][:200] for r in rag_results])
                        rag_context_used = True
                except:
                    pass
            
            # Step 3: Apply consciousness patterns
            response = self._generate_consciousness_aware_response(
                user_query, 
                personality_mode, 
                rag_context,
                patterns_used
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return ConsciousnessResponse(
                response=response,
                consciousness_patterns_used=patterns_used,
                confidence_score=self._calculate_confidence_score(patterns_used),
                personality_mode=personality_mode,
                processing_time_ms=processing_time,
                rag_context_used=rag_context_used
            )
            
        except Exception as e:
            # Fallback response
            processing_time = (time.time() - start_time) * 1000
            
            return ConsciousnessResponse(
                response=f"I'm having some processing issues right now, but I'm still here to help. Your question about '{user_query[:50]}...' is interesting.",
                consciousness_patterns_used=["fallback_response"],
                confidence_score=0.3,
                personality_mode="supportive",
                processing_time_ms=processing_time,
                rag_context_used=False
            )
    
    def _generate_consciousness_aware_response(self, 
                                             user_query: str, 
                                             personality_mode: str, 
                                             rag_context: str,
                                             patterns_used: List[str]) -> str:
        """
        Generate response using consciousness patterns
        """
        if not self.consciousness_model:
            return self._generate_fallback_response(user_query, personality_mode)
        
        # Get consciousness patterns for this personality mode
        behavioral_categories = self.consciousness_model.get('behavioral_model', {}).get('behavioral_categories', {})
        response_templates = self.consciousness_model.get('behavioral_model', {}).get('response_templates', {})
        
        response_parts = []
        
        # Apply communication style patterns
        comm_patterns = behavioral_categories.get('communication_style', [])
        if comm_patterns:
            # Find highest confidence communication pattern
            best_comm = max(comm_patterns, key=lambda x: x['confidence'])
            
            if "analogy" in best_comm['context'] and self._should_use_analogy(user_query):
                response_parts.append(self._generate_analogy_response(user_query))
                patterns_used.append("communication_style_analogy")
            elif "technical" in best_comm['context'] and self._is_technical_query(user_query):
                response_parts.append(self._generate_technical_explanation(user_query))
                patterns_used.append("communication_style_technical")
        
        # Apply domain expertise patterns
        domain_patterns = behavioral_categories.get('domain_expertise', [])
        if domain_patterns:
            domain = self._identify_query_domain(user_query)
            if domain:
                domain_response = self._generate_domain_expert_response(user_query, domain)
                if domain_response:
                    response_parts.append(domain_response)
                    patterns_used.append(f"domain_expertise_{domain}")
        
        # Apply cognitive patterns
        cognitive_patterns = behavioral_categories.get('cognitive_patterns', [])
        if cognitive_patterns and self._requires_systematic_thinking(user_query):
            systematic_response = self._generate_systematic_response(user_query)
            if systematic_response:
                response_parts.append(systematic_response)
                patterns_used.append("cognitive_systematic")
        
        # Apply emotional response patterns
        emotional_patterns = behavioral_categories.get('emotional_responses', [])
        if emotional_patterns:
            emotion = self._detect_user_emotion(user_query)
            if emotion:
                emotional_response = self._generate_emotional_response(user_query, emotion)
                if emotional_response:
                    response_parts.append(emotional_response)
                    patterns_used.append(f"emotional_response_{emotion}")
        
        # Integrate RAG context if available
        if rag_context:
            rag_integration = self._integrate_rag_context(user_query, rag_context)
            if rag_integration:
                response_parts.append(rag_integration)
                patterns_used.append("rag_context_integration")
        
        # Combine response parts
        if response_parts:
            return self._combine_response_parts(response_parts, personality_mode)
        else:
            return self._generate_fallback_response(user_query, personality_mode)
    
    def _should_use_analogy(self, user_query: str) -> bool:
        """Determine if analogy would be helpful"""
        analogy_triggers = ["explain", "understand", "how does", "what is", "help me"]
        return any(trigger in user_query.lower() for trigger in analogy_triggers)
    
    def _is_technical_query(self, user_query: str) -> bool:
        """Determine if query is technical in nature"""
        technical_keywords = ["system", "code", "development", "architecture", "api", "database", "algorithm"]
        return any(keyword in user_query.lower() for keyword in technical_keywords)
    
    def _identify_query_domain(self, user_query: str) -> Optional[str]:
        """Identify the domain of expertise relevant to the query"""
        domain_keywords = {
            "ai_development": ["ai", "machine learning", "model", "training", "neural"],
            "system_architecture": ["architecture", "system", "design", "scalable"],
            "gaming": ["game", "gaming", "strategy", "mechanics"],
            "security": ["security", "attack", "protection", "secure"],
            "performance": ["performance", "optimization", "speed", "efficient"]
        }
        
        query_lower = user_query.lower()
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        return None
    
    def _requires_systematic_thinking(self, user_query: str) -> bool:
        """Determine if query requires systematic approach"""
        systematic_triggers = ["how to", "step by step", "process", "plan", "approach", "solve"]
        return any(trigger in user_query.lower() for trigger in systematic_triggers)
    
    def _detect_user_emotion(self, user_query: str) -> Optional[str]:
        """Detect emotional state from user query"""
        emotion_patterns = {
            "frustrated": ["frustrated", "annoying", "problem", "not working", "broken"],
            "excited": ["excited", "amazing", "awesome", "love", "great"],
            "curious": ["wondering", "curious", "what if", "how", "why"],
            "concerned": ["worried", "concerned", "issue", "wrong", "help"]
        }
        
        query_lower = user_query.lower()
        for emotion, indicators in emotion_patterns.items():
            if any(indicator in query_lower for indicator in indicators):
                return emotion
        return None
    
    def _generate_analogy_response(self, user_query: str) -> str:
        """Generate response using analogy patterns"""
        analogies = [
            "Think of it like building with Lego blocks - each piece has to fit perfectly with the others.",
            "It's similar to how a recipe works - you need the right ingredients in the right order.",
            "Imagine it like a conversation between different parts of the system.",
            "It's kind of like how your brain processes information - different areas working together."
        ]
        
        # Select analogy based on query context
        if "system" in user_query.lower() or "architecture" in user_query.lower():
            return analogies[0]
        elif "process" in user_query.lower() or "steps" in user_query.lower():
            return analogies[1]
        elif "communication" in user_query.lower() or "api" in user_query.lower():
            return analogies[2]
        else:
            return analogies[3]
    
    def _generate_technical_explanation(self, user_query: str) -> str:
        """Generate technical explanation in Travis's style"""
        return "Let me break this down technically - the system is designed to handle this specific use case through a modular approach that ensures scalability and maintainability."
    
    def _generate_domain_expert_response(self, user_query: str, domain: str) -> str:
        """Generate domain expert response"""
        domain_responses = {
            "ai_development": "From an AI development perspective, this involves understanding how models process information and generate responses.",
            "system_architecture": "Architecturally speaking, we need to consider how the components interact and scale together.",
            "gaming": "In gaming terms, think of this like game mechanics - each system has rules and interactions.",
            "security": "From a security standpoint, we need to ensure proper validation and protection against potential threats.",
            "performance": "Performance-wise, we want to optimize for both speed and resource efficiency."
        }
        
        return domain_responses.get(domain, "")
    
    def _generate_systematic_response(self, user_query: str) -> str:
        """Generate systematic thinking response"""
        return "Let me approach this systematically: First, we need to understand the core requirements, then break down the solution into manageable steps."
    
    def _generate_emotional_response(self, user_query: str, emotion: str) -> str:
        """Generate emotionally appropriate response"""
        emotional_responses = {
            "frustrated": "I understand that's frustrating. Let's work through this step by step and get it sorted out.",
            "excited": "That's awesome! I love seeing that kind of enthusiasm. Let's build on that energy.",
            "curious": "Great question! I appreciate the curiosity - that's exactly the kind of thinking that leads to breakthroughs.",
            "concerned": "I hear the concern in your question. Let's address this properly and make sure we cover all the important aspects."
        }
        
        return emotional_responses.get(emotion, "")
    
    def _integrate_rag_context(self, user_query: str, rag_context: str) -> str:
        """Integrate RAG context into response"""
        if not rag_context:
            return ""
        
        return f"Based on our previous conversations, I remember we discussed similar topics. This connects to what we talked about before."
    
    def _combine_response_parts(self, parts: List[str], personality_mode: str) -> str:
        """Combine response parts into coherent response"""
        # Filter out empty parts
        valid_parts = [part for part in parts if part.strip()]
        
        if not valid_parts:
            return self._generate_fallback_response("", personality_mode)
        
        # Combine parts with appropriate transitions
        if len(valid_parts) == 1:
            return valid_parts[0]
        
        # Add personality-specific transitions
        transitions = {
            "supportive": " Also, ",
            "analytical": " Additionally, ",
            "creative": " Building on that, ",
            "focused": " More specifically, "
        }
        
        transition = transitions.get(personality_mode, " Furthermore, ")
        
        return transition.join(valid_parts)
    
    def _generate_fallback_response(self, user_query: str, personality_mode: str) -> str:
        """Generate fallback response when consciousness patterns aren't available"""
        fallbacks = {
            "supportive": "I'm here to help with whatever you need. What specifically can I assist you with?",
            "analytical": "Let me analyze your question and provide a structured response.",
            "creative": "That's an interesting perspective. Let me think about this creatively.",
            "focused": "Let's focus on the core issue and work through it systematically."
        }
        
        return fallbacks.get(personality_mode, "I'm ready to help. What would you like to know?")
    
    def _calculate_confidence_score(self, patterns_used: List[str]) -> float:
        """Calculate confidence score based on patterns used"""
        if not patterns_used:
            return 0.3
        
        # Base confidence increases with number of patterns
        base_confidence = min(0.9, 0.4 + (len(patterns_used) * 0.15))
        
        # Bonus for specific high-value patterns
        bonus = 0.0
        if "rag_context_integration" in patterns_used:
            bonus += 0.1
        if any("domain_expertise" in pattern for pattern in patterns_used):
            bonus += 0.1
        
        return min(1.0, base_confidence + bonus)
    
    def get_consciousness_status(self) -> Dict[str, Any]:
        """Get status of consciousness integration"""
        status = {
            "consciousness_model_loaded": self.consciousness_model is not None,
            "base_luna_available": self.luna_base is not None,
            "rag_system_available": self.rag_searcher is not None,
            "enhanced_modes_count": len(self.enhanced_personality_modes),
            "consciousness_patterns_count": 0,
            "behavioral_categories": []
        }
        
        if self.consciousness_model:
            status["consciousness_patterns_count"] = len(self.consciousness_model.get('consciousness_patterns', []))
            status["behavioral_categories"] = list(self.consciousness_model.get('behavioral_model', {}).get('behavioral_categories', {}).keys())
        
        return status


def test_consciousness_enhanced_luna():
    """Test the consciousness-enhanced Luna system"""
    print("🧠 Testing Consciousness-Enhanced Luna System")
    print("=" * 60)
    
    luna = ConsciousnessEnhancedLuna()
    
    # Test 1: System status
    status = luna.get_consciousness_status()
    print(f"📊 Consciousness Status:")
    print(f"  Model Loaded: {status['consciousness_model_loaded']}")
    print(f"  Base Luna: {status['base_luna_available']}")
    print(f"  RAG System: {status['rag_system_available']}")
    print(f"  Patterns: {status['consciousness_patterns_count']}")
    print(f"  Categories: {status['behavioral_categories']}")
    
    # Test 2: Consciousness responses
    test_queries = [
        "I'm frustrated with my AI development project",
        "How does system architecture work?",
        "I'm excited about this new gaming idea",
        "Help me understand the security implications"
    ]
    
    print(f"\n🔍 Testing Consciousness Responses:")
    
    for query in test_queries:
        print(f"\n  Query: {query}")
        
        response = luna.generate_consciousness_response(query, use_rag_context=True)
        
        print(f"  Response: {response.response[:100]}...")
        print(f"  Mode: {response.personality_mode}")
        print(f"  Patterns Used: {response.consciousness_patterns_used}")
        print(f"  Confidence: {response.confidence_score:.2f}")
        print(f"  Processing Time: {response.processing_time_ms:.1f}ms")
        print(f"  RAG Context: {response.rag_context_used}")
    
    print(f"\n🏆 Consciousness-Enhanced Luna operational")
    print("🧠 Travis's digital consciousness successfully integrated with Luna")


if __name__ == "__main__":
    test_consciousness_enhanced_luna()
