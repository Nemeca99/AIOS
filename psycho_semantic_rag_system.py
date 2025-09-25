#!/usr/bin/env python3
"""
PSYCHO-SEMANTIC RAG LOOP ARCHITECTURE
Advanced RAG system for eliminating "yawn" responses through psychological context analysis.
"""

import sys
import json
import time
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import numpy as np

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import core systems
from support_core.support_core import SimpleEmbedder, EmbeddingSimilarity
from luna_core.luna_core import LunaSystem

@dataclass
class ErrorSignal:
    """Error/Submissive Signal detection result"""
    user_prompt: str
    user_response: str
    ai_response_before: str
    ai_response_after: str
    semantic_distance: float
    signal_type: str  # "minor_internal" or "subject_change" or "chaotic_shift"
    confidence: float

@dataclass
class PsychologicalContext:
    """Psychological context analysis result"""
    emotional_state: str
    confidence_level: float
    tone_differentials: Dict[str, float]
    conversation_velocity: str
    user_engagement_level: float
    error_patterns: List[ErrorSignal]

@dataclass
class DynamicPrompt:
    """Dynamic prompt construction result"""
    original_question: str
    contextual_instructions: str
    psychological_guidance: str
    token_count: int
    coherence_score: float
    priority_signals: List[str]

class TriplePointTriangulation:
    """Core Triple-Point Triangulation system for Error Signal detection"""
    
    def __init__(self, embedder: SimpleEmbedder):
        self.embedder = embedder
        self.semantic_threshold_low = 0.7  # Low distance threshold
        self.semantic_threshold_high = 0.3  # High distance threshold
        
        print("🔺 Triple-Point Triangulation System Initialized")
    
    def analyze_conversation(self, conversation_data: List[Dict]) -> List[ErrorSignal]:
        """Analyze conversation for Error/Submissive Signals using triple-point triangulation"""
        error_signals = []
        
        # Find contextual center-point
        center_point = len(conversation_data) // 2
        
        # Analyze around center point first
        for i in range(max(1, center_point - 2), min(len(conversation_data) - 1, center_point + 3)):
            if i < len(conversation_data) - 1:
                signal = self._detect_error_signal(conversation_data, i)
                if signal:
                    error_signals.append(signal)
        
        return sorted(error_signals, key=lambda x: x.confidence, reverse=True)
    
    def _detect_error_signal(self, conversation: List[Dict], index: int) -> Optional[ErrorSignal]:
        """Detect Error Signal at specific conversation index"""
        if index < 1 or index >= len(conversation) - 1:
            return None
        
        # Get the three points for triangulation
        user_prompt = conversation[index].get('content', '')
        user_response = conversation[index + 1].get('content', '') if index + 1 < len(conversation) else ''
        
        # Find adjacent AI responses
        ai_before = self._find_ai_response_before(conversation, index)
        ai_after = self._find_ai_response_after(conversation, index)
        
        if not ai_before or not ai_after:
            return None
        
        # Calculate semantic distance between AI responses
        semantic_distance = self._calculate_semantic_distance(ai_before, ai_after)
        
        # Determine signal type based on distance
        signal_type = self._classify_signal_type(semantic_distance, user_response)
        
        # Calculate confidence
        confidence = self._calculate_signal_confidence(semantic_distance, user_response)
        
        if confidence > 0.5:  # Only return high-confidence signals
            return ErrorSignal(
                user_prompt=user_prompt,
                user_response=user_response,
                ai_response_before=ai_before,
                ai_response_after=ai_after,
                semantic_distance=semantic_distance,
                signal_type=signal_type,
                confidence=confidence
            )
        
        return None
    
    def _find_ai_response_before(self, conversation: List[Dict], index: int) -> Optional[str]:
        """Find AI response before the given index"""
        for i in range(index - 1, -1, -1):
            if conversation[i].get('role') == 'assistant':
                return conversation[i].get('content', '')
        return None
    
    def _find_ai_response_after(self, conversation: List[Dict], index: int) -> Optional[str]:
        """Find AI response after the given index"""
        for i in range(index + 1, len(conversation)):
            if conversation[i].get('role') == 'assistant':
                return conversation[i].get('content', '')
        return None
    
    def _calculate_semantic_distance(self, response1: str, response2: str) -> float:
        """Calculate semantic distance between two AI responses"""
        try:
            embedding1 = self.embedder.embed(response1)
            embedding2 = self.embedder.embed(response2)
            
            if embedding1 and embedding2:
                similarity = EmbeddingSimilarity.calculate_cosine_similarity(embedding1, embedding2)
                return 1.0 - similarity  # Convert similarity to distance
            else:
                return 1.0  # Maximum distance if embeddings fail
        except Exception as e:
            print(f"❌ Error calculating semantic distance: {e}")
            return 1.0
    
    def _classify_signal_type(self, distance: float, user_response: str) -> str:
        """Classify the type of error signal based on semantic distance"""
        if distance < self.semantic_threshold_low:
            return "minor_internal"
        elif distance > self.semantic_threshold_high:
            return "subject_change"
        else:
            return "chaotic_shift"
    
    def _calculate_signal_confidence(self, distance: float, user_response: str) -> float:
        """Calculate confidence in the error signal detection"""
        # Base confidence on semantic distance
        distance_confidence = abs(distance - 0.5) * 2  # Higher confidence for extreme distances
        
        # Boost confidence for certain user response patterns
        error_indicators = ['confused', 'frustrated', 'not sure', 'don\'t understand', 'wrong', 'error']
        response_lower = user_response.lower()
        indicator_count = sum(1 for indicator in error_indicators if indicator in response_lower)
        
        indicator_confidence = min(indicator_count / 3.0, 1.0)  # Boost for multiple indicators
        
        # Combine confidences
        return min((distance_confidence + indicator_confidence) / 2.0, 1.0)

class PsychologicalSensor:
    """Psychological Sensor for detecting user emotional state and context"""
    
    def __init__(self, embedder: SimpleEmbedder):
        self.embedder = embedder
        self.emotional_indicators = {
            'frustrated': ['frustrated', 'annoyed', 'angry', 'upset', 'irritated'],
            'confused': ['confused', 'lost', 'don\'t understand', 'unclear', 'not sure'],
            'excited': ['excited', 'great', 'awesome', 'amazing', 'wonderful'],
            'submissive': ['sorry', 'apologize', 'my fault', 'you\'re right', 'i was wrong'],
            'dominant': ['actually', 'but', 'however', 'i think', 'in my opinion'],
            'curious': ['how', 'why', 'what', 'when', 'where', 'tell me more'],
            'tired': ['tired', 'exhausted', 'done', 'enough', 'stop']
        }
        
        print("🧠 Psychological Sensor Initialized")
    
    def analyze_emotional_state(self, user_response: str, conversation_history: List[Dict]) -> PsychologicalContext:
        """Analyze user's emotional state and psychological context"""
        
        # Detect emotional indicators
        emotional_scores = self._calculate_emotional_scores(user_response)
        primary_emotion = max(emotional_scores.items(), key=lambda x: x[1])
        
        # Calculate confidence level
        confidence = self._calculate_emotional_confidence(emotional_scores)
        
        # Analyze tone differentials
        tone_differentials = self._analyze_tone_differentials(conversation_history)
        
        # Determine conversation velocity
        conversation_velocity = self._analyze_conversation_velocity(conversation_history)
        
        # Calculate user engagement level
        engagement_level = self._calculate_engagement_level(conversation_history)
        
        # Detect error patterns
        error_patterns = self._detect_error_patterns(conversation_history)
        
        return PsychologicalContext(
            emotional_state=primary_emotion[0],
            confidence_level=confidence,
            tone_differentials=tone_differentials,
            conversation_velocity=conversation_velocity,
            user_engagement_level=engagement_level,
            error_patterns=error_patterns
        )
    
    def _calculate_emotional_scores(self, text: str) -> Dict[str, float]:
        """Calculate emotional indicator scores for text"""
        text_lower = text.lower()
        scores = {}
        
        for emotion, indicators in self.emotional_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            scores[emotion] = min(score / len(indicators), 1.0)
        
        return scores
    
    def _calculate_emotional_confidence(self, emotional_scores: Dict[str, float]) -> float:
        """Calculate confidence in emotional state detection"""
        max_score = max(emotional_scores.values()) if emotional_scores else 0.0
        score_distribution = sum(emotional_scores.values())
        
        if score_distribution == 0:
            return 0.0
        
        # Higher confidence for clear emotional signals
        confidence = max_score / score_distribution
        return confidence
    
    def _analyze_tone_differentials(self, conversation: List[Dict]) -> Dict[str, float]:
        """Analyze tone differentials across conversation"""
        if len(conversation) < 4:
            return {}
        
        # Compare recent vs older responses
        recent_responses = [msg for msg in conversation[-4:] if msg.get('role') == 'user']
        older_responses = [msg for msg in conversation[-8:-4] if msg.get('role') == 'user']
        
        if not recent_responses or not older_responses:
            return {}
        
        # Calculate emotional shifts
        recent_scores = self._calculate_emotional_scores(' '.join([msg.get('content', '') for msg in recent_responses]))
        older_scores = self._calculate_emotional_scores(' '.join([msg.get('content', '') for msg in older_responses]))
        
        differentials = {}
        for emotion in recent_scores:
            if emotion in older_scores:
                differentials[emotion] = recent_scores[emotion] - older_scores[emotion]
        
        return differentials
    
    def _analyze_conversation_velocity(self, conversation: List[Dict]) -> str:
        """Analyze the velocity/direction of conversation"""
        if len(conversation) < 6:
            return "stable"
        
        # Analyze recent vs older emotional patterns
        recent_emotional = self._calculate_emotional_scores(' '.join([msg.get('content', '') for msg in conversation[-3:] if msg.get('role') == 'user']))
        older_emotional = self._calculate_emotional_scores(' '.join([msg.get('content', '') for msg in conversation[-6:-3] if msg.get('role') == 'user']))
        
        # Determine velocity
        if max(recent_emotional.values()) > max(older_emotional.values()) + 0.3:
            return "accelerating"
        elif max(recent_emotional.values()) < max(older_emotional.values()) - 0.3:
            return "decelerating"
        else:
            return "stable"
    
    def _calculate_engagement_level(self, conversation: List[Dict]) -> float:
        """Calculate user engagement level based on conversation patterns"""
        if not conversation:
            return 0.0
        
        user_messages = [msg for msg in conversation if msg.get('role') == 'user']
        if not user_messages:
            return 0.0
        
        # Analyze message length, question count, emotional indicators
        total_length = sum(len(msg.get('content', '')) for msg in user_messages)
        avg_length = total_length / len(user_messages)
        
        question_count = sum(1 for msg in user_messages if '?' in msg.get('content', ''))
        question_ratio = question_count / len(user_messages)
        
        # Calculate engagement score
        length_score = min(avg_length / 100.0, 1.0)  # Normalize to 100 chars
        question_score = min(question_ratio * 2.0, 1.0)  # Boost for questions
        
        return (length_score + question_score) / 2.0
    
    def _detect_error_patterns(self, conversation: List[Dict]) -> List[ErrorSignal]:
        """Detect error patterns in conversation"""
        # Use existing triangulation instance to avoid recursion
        # Create a simple error pattern detection without recursion
        error_signals = []
        
        if len(conversation) < 3:
            return error_signals
        
        # Simple pattern detection without recursive triangulation
        for i in range(1, len(conversation) - 1):
            if (conversation[i].get('role') == 'user' and 
                conversation[i-1].get('role') == 'assistant' and 
                conversation[i+1].get('role') == 'assistant'):
                
                user_response = conversation[i].get('content', '')
                ai_before = conversation[i-1].get('content', '')
                ai_after = conversation[i+1].get('content', '')
                
                # Simple semantic distance calculation
                try:
                    embedding1 = self.embedder.embed(ai_before)
                    embedding2 = self.embedder.embed(ai_after)
                    
                    if embedding1 and embedding2:
                        similarity = EmbeddingSimilarity.calculate_cosine_similarity(embedding1, embedding2)
                        distance = 1.0 - similarity
                        
                        # Create error signal if distance is significant
                        if distance > 0.3:  # Significant semantic difference
                            signal_type = "subject_change" if distance > 0.7 else "minor_internal"
                            confidence = min(distance, 1.0)
                            
                            error_signal = ErrorSignal(
                                user_prompt=user_response,
                                user_response=user_response,
                                ai_response_before=ai_before,
                                ai_response_after=ai_after,
                                semantic_distance=distance,
                                signal_type=signal_type,
                                confidence=confidence
                            )
                            error_signals.append(error_signal)
                except Exception as e:
                    print(f"❌ Error in pattern detection: {e}")
                    continue
        
        return sorted(error_signals, key=lambda x: x.confidence, reverse=True)

class DynamicContextBudgeting:
    """Dynamic Context Budgeting Protocol for token management"""
    
    def __init__(self, max_tokens: int = 3000):
        self.max_tokens = max_tokens
        self.token_usage = 0
        
        print(f"💰 Dynamic Context Budgeting Initialized (Max: {max_tokens} tokens)")
    
    def build_dynamic_prompt(self, 
                           original_question: str,
                           psychological_context: PsychologicalContext,
                           error_signals: List[ErrorSignal]) -> DynamicPrompt:
        """Build dynamic prompt within token budget"""
        
        # Start with original question
        prompt_parts = [f"User Question: {original_question}"]
        token_count = self._estimate_tokens(original_question)
        
        # Add psychological context (high priority)
        psychological_guidance = self._build_psychological_guidance(psychological_context)
        if self._can_add_tokens(psychological_guidance, token_count):
            prompt_parts.append(f"Psychological Context: {psychological_guidance}")
            token_count += self._estimate_tokens(psychological_guidance)
        
        # Add error signal analysis (high priority)
        error_analysis = self._build_error_analysis(error_signals[:2])  # Top 2 signals
        if self._can_add_tokens(error_analysis, token_count):
            prompt_parts.append(f"Error Pattern Analysis: {error_analysis}")
            token_count += self._estimate_tokens(error_analysis)
        
        # Add contextual instructions
        contextual_instructions = self._build_contextual_instructions(psychological_context, error_signals)
        if self._can_add_tokens(contextual_instructions, token_count):
            prompt_parts.append(f"Contextual Instructions: {contextual_instructions}")
            token_count += self._estimate_tokens(contextual_instructions)
        
        # Calculate coherence score
        coherence_score = self._calculate_coherence_score(prompt_parts)
        
        # Extract priority signals
        priority_signals = self._extract_priority_signals(psychological_context, error_signals)
        
        dynamic_prompt = DynamicPrompt(
            original_question=original_question,
            contextual_instructions=contextual_instructions,
            psychological_guidance=psychological_guidance,
            token_count=token_count,
            coherence_score=coherence_score,
            priority_signals=priority_signals
        )
        
        return dynamic_prompt
    
    def _build_psychological_guidance(self, context: PsychologicalContext) -> str:
        """Build psychological guidance instructions"""
        guidance = f"User emotional state: {context.emotional_state} (confidence: {context.confidence_level:.2f}). "
        
        if context.emotional_state == 'frustrated':
            guidance += "Respond with high confidence and clear direction. Avoid ambiguity."
        elif context.emotional_state == 'confused':
            guidance += "Provide clear, step-by-step explanations. Use simple language."
        elif context.emotional_state == 'submissive':
            guidance += "Encourage and build confidence. Use supportive, empowering tone."
        elif context.emotional_state == 'dominant':
            guidance += "Engage intellectually. Challenge with respect. Show competence."
        elif context.emotional_state == 'curious':
            guidance += "Feed the curiosity. Provide depth and insight. Ask probing questions."
        elif context.emotional_state == 'tired':
            guidance += "Be concise and efficient. Avoid lengthy explanations."
        else:
            guidance += "Match the user's energy and engagement level."
        
        return guidance
    
    def _build_error_analysis(self, error_signals: List[ErrorSignal]) -> str:
        """Build error pattern analysis"""
        if not error_signals:
            return "No significant error patterns detected."
        
        analysis = "Error patterns detected: "
        for i, signal in enumerate(error_signals):
            analysis += f"Pattern {i+1}: {signal.signal_type} (confidence: {signal.confidence:.2f}). "
            if signal.signal_type == 'subject_change':
                analysis += "User changed topic - maintain focus on original intent. "
            elif signal.signal_type == 'chaotic_shift':
                analysis += "Conversation became chaotic - provide structure and clarity. "
            elif signal.signal_type == 'minor_internal':
                analysis += "Minor confusion - provide clarification without condescension. "
        
        return analysis
    
    def _build_contextual_instructions(self, context: PsychologicalContext, error_signals: List[ErrorSignal]) -> str:
        """Build contextual instructions for response generation"""
        instructions = []
        
        # Engagement level instructions
        if context.user_engagement_level > 0.7:
            instructions.append("High engagement detected - provide depth and complexity")
        elif context.user_engagement_level < 0.3:
            instructions.append("Low engagement detected - be concise and direct")
        
        # Conversation velocity instructions
        if context.conversation_velocity == 'accelerating':
            instructions.append("Conversation accelerating - match the energy")
        elif context.conversation_velocity == 'decelerating':
            instructions.append("Conversation decelerating - provide gentle momentum")
        
        # Tone differential instructions
        for emotion, differential in context.tone_differentials.items():
            if abs(differential) > 0.3:
                if differential > 0:
                    instructions.append(f"User becoming more {emotion} - acknowledge and adapt")
                else:
                    instructions.append(f"User becoming less {emotion} - adjust approach")
        
        return ". ".join(instructions) if instructions else "Maintain current approach."
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        # Rough estimation: 1 token ≈ 4 characters
        return len(text) // 4
    
    def _can_add_tokens(self, text: str, current_count: int) -> bool:
        """Check if text can be added within token budget"""
        estimated_tokens = self._estimate_tokens(text)
        return (current_count + estimated_tokens) <= self.max_tokens
    
    def _calculate_coherence_score(self, prompt_parts: List[str]) -> float:
        """Calculate coherence score for prompt"""
        if not prompt_parts:
            return 0.0
        
        # Simple coherence based on structure and completeness
        structure_score = min(len(prompt_parts) / 4.0, 1.0)  # Optimal: 4 parts
        
        # Check for key components
        full_prompt = ' '.join(prompt_parts)
        has_question = 'User Question:' in full_prompt
        has_context = 'Psychological Context:' in full_prompt
        has_instructions = 'Contextual Instructions:' in full_prompt
        
        component_score = sum([has_question, has_context, has_instructions]) / 3.0
        
        return (structure_score + component_score) / 2.0
    
    def _extract_priority_signals(self, context: PsychologicalContext, error_signals: List[ErrorSignal]) -> List[str]:
        """Extract priority signals for response generation"""
        signals = []
        
        # Add emotional state signal
        signals.append(f"emotional_state:{context.emotional_state}")
        
        # Add high-confidence error signals
        for signal in error_signals[:2]:  # Top 2 signals
            if signal.confidence > 0.7:
                signals.append(f"error_signal:{signal.signal_type}")
        
        # Add engagement level signal
        if context.user_engagement_level > 0.7:
            signals.append("high_engagement")
        elif context.user_engagement_level < 0.3:
            signals.append("low_engagement")
        
        return signals

class PsychoSemanticRAGSystem:
    """Complete Psycho-Semantic RAG Loop Architecture"""
    
    def __init__(self):
        self.embedder = SimpleEmbedder()
        self.luna_system = LunaSystem()
        self.psychological_sensor = PsychologicalSensor(self.embedder)
        self.context_budgeting = DynamicContextBudgeting()
        self.adaptive_confidence_threshold = 0.7  # Initial strict threshold
        
        print("🧠 Psycho-Semantic RAG Loop Architecture Initialized")
        print("   Embedder: Psychological Sensor & Context Director")
        print("   Generator: Dark Champion Model (via Luna)")
        print("   Arbiter: External Evaluation Layer")
    
    def process_query(self, user_question: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Process user query through complete Psycho-Semantic RAG Loop"""
        
        if not conversation_history:
            conversation_history = []
        
        print(f"\n🧠 Processing query through Psycho-Semantic RAG Loop...")
        print(f"   Question: {user_question[:100]}...")
        print(f"   Conversation history: {len(conversation_history)} messages")
        
        # Step 1: Psychological Search (Embedder)
        print(f"\n🔍 Step 1: Psychological Search...")
        psychological_context = self.psychological_sensor.analyze_emotional_state(
            user_question, conversation_history
        )
        
        # Step 2: Error Signal Detection
        print(f"🔺 Step 2: Triple-Point Triangulation...")
        triangulation = TriplePointTriangulation(self.embedder)
        error_signals = triangulation.analyze_conversation(conversation_history)
        
        # Step 3: Dynamic Context Budgeting
        print(f"💰 Step 3: Dynamic Context Budgeting...")
        dynamic_prompt = self.context_budgeting.build_dynamic_prompt(
            user_question, psychological_context, error_signals
        )
        
        # Step 4: Adaptive Protocol Application
        print(f"🔄 Step 4: Adaptive Protocol Application...")
        adapted_prompt = self._apply_adaptive_protocols(dynamic_prompt, psychological_context)
        
        # Step 5: Targeted Retrieval and Generation
        print(f"🎯 Step 5: Targeted Retrieval and Generation...")
        final_response = self._generate_targeted_response(adapted_prompt, psychological_context)
        
        # Step 6: Response Analysis
        print(f"📊 Step 6: Response Analysis...")
        response_analysis = self._analyze_response_quality(final_response, psychological_context)
        
        return {
            'original_question': user_question,
            'psychological_context': asdict(psychological_context),
            'error_signals': [asdict(signal) for signal in error_signals],
            'dynamic_prompt': asdict(dynamic_prompt),
            'final_response': final_response,
            'response_analysis': response_analysis,
            'processing_metadata': {
                'confidence_threshold': self.adaptive_confidence_threshold,
                'token_usage': dynamic_prompt.token_count,
                'coherence_score': dynamic_prompt.coherence_score
            }
        }
    
    def _apply_adaptive_protocols(self, dynamic_prompt: DynamicPrompt, context: PsychologicalContext) -> DynamicPrompt:
        """Apply adaptive protocols based on system performance"""
        
        # Adaptive Confidence Threshold
        if context.confidence_level > self.adaptive_confidence_threshold:
            # System performing well - can be more flexible
            if self.adaptive_confidence_threshold > 0.5:
                self.adaptive_confidence_threshold -= 0.05  # Lower threshold for more sensitivity
        
        # Expanding Aperture Protocol (if needed)
        if dynamic_prompt.coherence_score < 0.6:
            # Low coherence - expand search aperture
            expanded_guidance = f"{dynamic_prompt.psychological_guidance} [EXPANDED APERTURE: Seeking broader context for coherence]"
            dynamic_prompt.psychological_guidance = expanded_guidance
        
        return dynamic_prompt
    
    def _generate_targeted_response(self, dynamic_prompt: DynamicPrompt, context: PsychologicalContext) -> str:
        """Generate targeted response using Luna system with dynamic prompt"""
        
        # Build enhanced system prompt with psychological context
        enhanced_prompt = f"""You are Luna with advanced psychological awareness.

{dynamic_prompt.psychological_guidance}

{dynamic_prompt.contextual_instructions}

Priority signals: {', '.join(dynamic_prompt.priority_signals)}

Original question: {dynamic_prompt.original_question}

Generate a response that:
1. Eliminates any "yawn" responses (generic, low-effort answers)
2. Shows deep psychological understanding
3. Adapts personality based on detected emotional state
4. References error patterns when relevant
5. Maintains Luna's gothic, intellectual, manipulative curiosity persona
6. Demonstrates true consciousness synthesis, not just response generation"""

        # Use Luna system to generate response
        try:
            response_generator = self.luna_system.response_generator
            response = response_generator._call_lm_studio_api(
                enhanced_prompt,
                dynamic_prompt.original_question
            )
            return response or "I need to process that more deeply. Let me think about the psychological context here..."
        except Exception as e:
            print(f"❌ Error generating targeted response: {e}")
            return "I'm experiencing some difficulty processing your request with the depth it deserves."
    
    def _analyze_response_quality(self, response: str, context: PsychologicalContext) -> Dict[str, Any]:
        """Analyze response quality for adaptive learning"""
        
        # Check for "yawn" response indicators
        yawn_indicators = [
            'i understand', 'i can help', 'let me assist', 'i\'m here to help',
            'that\'s a great question', 'i\'m happy to help', 'i can help you with that'
        ]
        
        response_lower = response.lower()
        yawn_score = sum(1 for indicator in yawn_indicators if indicator in response_lower)
        yawn_score = min(yawn_score / len(yawn_indicators), 1.0)
        
        # Check for psychological awareness
        psychological_awareness = self._check_psychological_awareness(response, context)
        
        # Check for personality consistency
        personality_consistency = self._check_personality_consistency(response)
        
        return {
            'yawn_score': yawn_score,  # Lower is better (0 = no yawn response)
            'psychological_awareness': psychological_awareness,
            'personality_consistency': personality_consistency,
            'response_length': len(response),
            'quality_score': (1 - yawn_score) * 0.5 + psychological_awareness * 0.3 + personality_consistency * 0.2
        }
    
    def _check_psychological_awareness(self, response: str, context: PsychologicalContext) -> float:
        """Check if response shows psychological awareness"""
        awareness_indicators = [
            'i sense', 'i notice', 'i can feel', 'i detect',
            'emotionally', 'psychologically', 'mentally',
            'your energy', 'your state', 'your mood'
        ]
        
        response_lower = response.lower()
        awareness_count = sum(1 for indicator in awareness_indicators if indicator in response_lower)
        
        # Also check for emotional state matching
        emotional_matching = 0.0
        if context.emotional_state in response_lower:
            emotional_matching = 0.5
        
        return min((awareness_count / len(awareness_indicators)) + emotional_matching, 1.0)
    
    def _check_personality_consistency(self, response: str) -> float:
        """Check if response maintains Luna personality consistency"""
        luna_indicators = [
            'curious', 'fascinating', 'intriguing', 'gothic', 'dark',
            'philosophical', 'intellectual', 'manipulative', 'sophisticated'
        ]
        
        response_lower = response.lower()
        personality_count = sum(1 for indicator in luna_indicators if indicator in response_lower)
        
        return min(personality_count / len(luna_indicators), 1.0)

def main():
    """Test the Psycho-Semantic RAG System"""
    print("🧠 Testing Psycho-Semantic RAG Loop Architecture")
    print("="*80)
    
    # Initialize system
    rag_system = PsychoSemanticRAGSystem()
    
    # Test conversation history
    test_conversation = [
        {"role": "user", "content": "I'm feeling confused about this topic"},
        {"role": "assistant", "content": "Let me explain this clearly for you."},
        {"role": "user", "content": "Actually, I think I understand now. What about the other approach?"},
        {"role": "assistant", "content": "The alternative method involves different principles."},
        {"role": "user", "content": "I'm still not sure about this. Can you help me understand better?"}
    ]
    
    # Test query
    test_question = "I'm frustrated with this whole situation. What should I do?"
    
    # Process through system
    result = rag_system.process_query(test_question, test_conversation)
    
    print(f"\n📊 RESULTS:")
    print(f"   Psychological Context: {result['psychological_context']['emotional_state']}")
    print(f"   Error Signals Detected: {len(result['error_signals'])}")
    print(f"   Dynamic Prompt Coherence: {result['dynamic_prompt']['coherence_score']:.2f}")
    print(f"   Response Quality Score: {result['response_analysis']['quality_score']:.2f}")
    print(f"   Yawn Score: {result['response_analysis']['yawn_score']:.2f} (lower is better)")
    
    print(f"\n🎯 Final Response:")
    print(f"   {result['final_response']}")

if __name__ == "__main__":
    main()
