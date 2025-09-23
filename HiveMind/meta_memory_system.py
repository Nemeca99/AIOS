#!/usr/bin/env python3
"""
Meta-Memory System for CARMA
Implements confidence tracking and "knowing what you don't know".
"""

import time
import random
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

UNCERTAINTY_THRESHOLD_DEFAULT = 0.3
CONFIDENCE_THRESHOLD_DEFAULT = 0.7
CONFIDENCE_DECAY_RATE_DEFAULT = 0.98
LEARNING_RATE_DEFAULT = 0.1
UNCERTAINTY_BOOST_DEFAULT = 1.2


class MetaMemorySystem:
    """Meta-memory system that tracks confidence and uncertainty."""
    
    def __init__(self, cache, emotion_cache=None):
        self.cache = cache
        self.emotion_cache = emotion_cache
        
        # Confidence tracking
        self.confidence_scores = {}  # fragment_id -> confidence_data
        self.uncertainty_threshold = UNCERTAINTY_THRESHOLD_DEFAULT
        self.confidence_threshold = CONFIDENCE_THRESHOLD_DEFAULT
        
        # Learning tracking
        self.learning_events = []  # Track learning events
        self.knowledge_gaps = {}  # Track what we don't know
        self.confidence_history = {}  # Track confidence over time
        
        # Meta-cognitive parameters
        self.confidence_decay_rate = CONFIDENCE_DECAY_RATE_DEFAULT
        self.learning_rate = LEARNING_RATE_DEFAULT
        self.uncertainty_boost = UNCERTAINTY_BOOST_DEFAULT
        
        print("🧠 Meta-Memory System Initialized")
        print(f"   Uncertainty threshold: {self.uncertainty_threshold}")
        print(f"   Confidence threshold: {self.confidence_threshold}")
        print(f"   Learning rate: {self.learning_rate}")
    
    def assess_confidence(self, fragment_id: str, content: str, context: Dict = None) -> Dict:
        """Assess confidence level for a fragment."""
        
        # Calculate base confidence from various factors
        base_confidence = self._calculate_base_confidence(fragment_id, content, context)
        
        # Apply emotional weighting if available
        if self.emotion_cache and fragment_id in self.emotion_cache.emotion_weights:
            emotion_data = self.emotion_cache.emotion_weights[fragment_id]
            emotional_confidence = self._calculate_emotional_confidence(emotion_data)
            base_confidence = (base_confidence + emotional_confidence) / 2
        
        # Apply recency factor
        recency_factor = self._calculate_recency_factor(fragment_id)
        
        # Apply consistency factor
        consistency_factor = self._calculate_consistency_factor(fragment_id, content)
        
        # Calculate final confidence
        final_confidence = base_confidence * recency_factor * consistency_factor
        final_confidence = max(0.0, min(1.0, final_confidence))  # Clamp to [0, 1]
        
        # Store confidence data
        self.confidence_scores[fragment_id] = {
            'confidence': final_confidence,
            'base_confidence': base_confidence,
            'recency_factor': recency_factor,
            'consistency_factor': consistency_factor,
            'last_assessed': time.time(),
            'assessment_count': self.confidence_scores.get(fragment_id, {}).get('assessment_count', 0) + 1,
            'uncertainty_level': 1.0 - final_confidence,
            'confidence_category': self._categorize_confidence(final_confidence)
        }
        
        return self.confidence_scores[fragment_id]
    
    def _calculate_base_confidence(self, fragment_id: str, content: str, context: Dict = None) -> float:
        """Calculate base confidence from content and context."""
        
        # Start with content-based confidence
        content_confidence = self._assess_content_confidence(content)
        
        # Add context-based confidence
        context_confidence = 0.5  # Default
        if context:
            context_confidence = self._assess_context_confidence(context)
        
        # Add fragment history confidence
        history_confidence = self._assess_history_confidence(fragment_id)
        
        # Combine factors
        base_confidence = (content_confidence * 0.4 + 
                          context_confidence * 0.3 + 
                          history_confidence * 0.3)
        
        return base_confidence
    
    def _assess_content_confidence(self, content: str) -> float:
        """Assess confidence based on content characteristics."""
        
        # Longer content tends to be more confident
        length_factor = min(len(content) / 100.0, 1.0)
        
        # Specific content tends to be more confident
        specificity_indicators = ['exactly', 'precisely', 'specifically', 'definitely', 'certainly']
        specificity_count = sum(1 for indicator in specificity_indicators if indicator in content.lower())
        specificity_factor = min(specificity_count / 3.0, 1.0)
        
        # Uncertainty indicators reduce confidence
        uncertainty_indicators = ['maybe', 'perhaps', 'might', 'could', 'possibly', 'unclear', 'unsure']
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in content.lower())
        uncertainty_factor = max(0.0, 1.0 - (uncertainty_count / 3.0))
        
        # Question marks reduce confidence
        question_factor = 0.5 if '?' in content else 1.0
        
        # Combine factors
        confidence = (length_factor * 0.3 + 
                     specificity_factor * 0.3 + 
                     uncertainty_factor * 0.2 + 
                     question_factor * 0.2)
        
        return confidence
    
    def _assess_context_confidence(self, context: Dict) -> float:
        """Assess confidence based on context."""
        
        # Source reliability
        source_confidence = context.get('source_reliability', 0.5)
        
        # Recency of information
        recency = context.get('recency', 0.5)
        recency_confidence = math.exp(-recency / 30)  # 30-day decay
        
        # Consistency with other sources
        consistency = context.get('consistency', 0.5)
        
        # Combine context factors
        context_confidence = (source_confidence * 0.4 + 
                            recency_confidence * 0.3 + 
                            consistency * 0.3)
        
        return context_confidence
    
    def _assess_history_confidence(self, fragment_id: str) -> float:
        """Assess confidence based on fragment history."""
        
        if fragment_id not in self.confidence_scores:
            return 0.5  # Default for new fragments
        
        history = self.confidence_scores[fragment_id]
        
        # More assessments = higher confidence
        assessment_count = history.get('assessment_count', 1)
        assessment_factor = min(assessment_count / 10.0, 1.0)
        
        # Recent assessments = higher confidence
        last_assessed = history.get('last_assessed', time.time())
        recency_factor = math.exp(-(time.time() - last_assessed) / 86400)  # 24-hour decay
        
        # Historical confidence trend
        historical_confidence = history.get('confidence', 0.5)
        
        # Combine history factors
        history_confidence = (assessment_factor * 0.3 + 
                            recency_factor * 0.3 + 
                            historical_confidence * 0.4)
        
        return history_confidence
    
    def _calculate_emotional_confidence(self, emotion_data: Dict) -> float:
        """Calculate confidence based on emotional content."""
        
        valence = emotion_data.get('valence', 0.0)
        intensity = emotion_data.get('intensity', 0.0)
        
        # High intensity emotions can affect confidence
        if intensity > 0.7:
            # Very positive or very negative emotions can increase confidence
            if abs(valence) > 0.5:
                return 0.8
            else:
                return 0.6
        else:
            # Neutral emotions maintain moderate confidence
            return 0.5
    
    def _calculate_recency_factor(self, fragment_id: str) -> float:
        """Calculate recency factor for confidence."""
        
        if fragment_id not in self.cache.file_registry:
            return 0.5
        
        fragment_data = self.cache.file_registry[fragment_id]
        created_time = fragment_data.get('created', time.time())
        
        # Ensure created_time is a number
        if isinstance(created_time, str):
            try:
                created_time = float(created_time)
            except ValueError:
                created_time = time.time()
        
        # More recent fragments have higher confidence
        age_days = (time.time() - created_time) / 86400
        recency_factor = math.exp(-age_days / 7)  # 7-day decay
        
        return recency_factor
    
    def _calculate_consistency_factor(self, fragment_id: str, content: str) -> float:
        """Calculate consistency factor for confidence."""
        
        # Check consistency with similar fragments
        similar_fragments = self._find_similar_fragments(fragment_id)
        
        if not similar_fragments:
            return 0.5  # No similar fragments to compare
        
        # Calculate consistency score
        consistency_scores = []
        for similar_id in similar_fragments:
            if similar_id in self.confidence_scores:
                similar_confidence = self.confidence_scores[similar_id]['confidence']
                consistency_scores.append(similar_confidence)
        
        if not consistency_scores:
            return 0.5
        
        # Consistency is based on how similar the confidence scores are
        avg_confidence = sum(consistency_scores) / len(consistency_scores)
        variance = sum((score - avg_confidence) ** 2 for score in consistency_scores) / len(consistency_scores)
        consistency_factor = max(0.0, 1.0 - variance)
        
        return consistency_factor
    
    def _categorize_confidence(self, confidence: float) -> str:
        """Categorize confidence level."""
        if confidence >= self.confidence_threshold:
            return "high"
        elif confidence >= self.uncertainty_threshold:
            return "medium"
        else:
            return "low"
    
    def _find_similar_fragments(self, fragment_id: str) -> List[str]:
        """Find fragments similar to the given one."""
        # This would use the cache's similarity search
        # For now, return empty list
        return []
    
    def identify_knowledge_gaps(self) -> List[Dict]:
        """Identify areas where confidence is low (knowledge gaps)."""
        
        knowledge_gaps = []
        
        for fragment_id, confidence_data in self.confidence_scores.items():
            confidence = confidence_data['confidence']
            uncertainty = confidence_data['uncertainty_level']
            
            if uncertainty > (1.0 - self.uncertainty_threshold):
                gap = {
                    'fragment_id': fragment_id,
                    'confidence': confidence,
                    'uncertainty': uncertainty,
                    'category': confidence_data['confidence_category'],
                    'content_preview': self.cache.file_registry.get(fragment_id, {}).get('content', '')[:100],
                    'priority': self._calculate_gap_priority(fragment_id, uncertainty)
                }
                knowledge_gaps.append(gap)
        
        # Sort by priority
        knowledge_gaps.sort(key=lambda x: x['priority'], reverse=True)
        
        return knowledge_gaps
    
    def _calculate_gap_priority(self, fragment_id: str, uncertainty: float) -> float:
        """Calculate priority for addressing a knowledge gap."""
        
        # Base priority from uncertainty level
        priority = uncertainty
        
        # Boost priority for frequently accessed fragments
        fragment_data = self.cache.file_registry.get(fragment_id, {})
        access_count = fragment_data.get('hits', 0)
        access_boost = min(access_count / 10.0, 1.0)
        priority += access_boost * 0.3
        
        # Boost priority for emotional fragments
        if self.emotion_cache and fragment_id in self.emotion_cache.emotion_weights:
            emotion_data = self.emotion_cache.emotion_weights[fragment_id]
            emotional_boost = emotion_data.get('emotional_score', 0.0)
            priority += emotional_boost * 0.2
        
        return priority
    
    def generate_uncertainty_report(self) -> Dict:
        """Generate a report on system uncertainty and knowledge gaps."""
        
        total_fragments = len(self.cache.file_registry)
        assessed_fragments = len(self.confidence_scores)
        
        if assessed_fragments == 0:
            return {'status': 'no_assessments', 'total_fragments': total_fragments}
        
        # Calculate confidence statistics
        confidences = [data['confidence'] for data in self.confidence_scores.values()]
        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)
        
        # Count by category
        high_confidence = sum(1 for data in self.confidence_scores.values() 
                            if data['confidence_category'] == 'high')
        medium_confidence = sum(1 for data in self.confidence_scores.values() 
                              if data['confidence_category'] == 'medium')
        low_confidence = sum(1 for data in self.confidence_scores.values() 
                           if data['confidence_category'] == 'low')
        
        # Identify knowledge gaps
        knowledge_gaps = self.identify_knowledge_gaps()
        
        report = {
            'timestamp': time.time(),
            'total_fragments': total_fragments,
            'assessed_fragments': assessed_fragments,
            'assessment_coverage': assessed_fragments / total_fragments if total_fragments > 0 else 0,
            'confidence_stats': {
                'average': avg_confidence,
                'minimum': min_confidence,
                'maximum': max_confidence,
                'high_confidence_count': high_confidence,
                'medium_confidence_count': medium_confidence,
                'low_confidence_count': low_confidence
            },
            'knowledge_gaps': {
                'total_gaps': len(knowledge_gaps),
                'high_priority_gaps': len([g for g in knowledge_gaps if g['priority'] > 0.7]),
                'gaps': knowledge_gaps[:10]  # Top 10 gaps
            },
            'recommendations': self._generate_recommendations(avg_confidence, len(knowledge_gaps))
        }
        
        return report
    
    def _generate_recommendations(self, avg_confidence: float, gap_count: int) -> List[str]:
        """Generate recommendations based on confidence analysis."""
        
        recommendations = []
        
        if avg_confidence < 0.5:
            recommendations.append("Overall confidence is low - consider gathering more reliable information")
        
        if gap_count > 10:
            recommendations.append("Many knowledge gaps detected - focus on high-priority areas")
        
        if avg_confidence > 0.8:
            recommendations.append("High confidence system - consider exploring new areas")
        
        if gap_count == 0:
            recommendations.append("No major knowledge gaps - system is well-calibrated")
        
        return recommendations
    
    def learn_from_feedback(self, fragment_id: str, feedback: Dict):
        """Learn from feedback to improve confidence assessment."""
        
        if fragment_id not in self.confidence_scores:
            return
        
        # Extract feedback information
        correct = feedback.get('correct', None)
        confidence_rating = feedback.get('confidence_rating', None)
        
        if correct is not None:
            # Adjust confidence based on correctness
            current_confidence = self.confidence_scores[fragment_id]['confidence']
            
            if correct:
                # Increase confidence
                new_confidence = min(1.0, current_confidence + self.learning_rate)
            else:
                # Decrease confidence
                new_confidence = max(0.0, current_confidence - self.learning_rate)
            
            self.confidence_scores[fragment_id]['confidence'] = new_confidence
            
            # Record learning event
            self.learning_events.append({
                'timestamp': time.time(),
                'fragment_id': fragment_id,
                'feedback': feedback,
                'old_confidence': current_confidence,
                'new_confidence': new_confidence
            })
        
        if confidence_rating is not None:
            # Adjust based on human confidence rating
            current_confidence = self.confidence_scores[fragment_id]['confidence']
            target_confidence = confidence_rating / 10.0  # Assume 1-10 scale
            
            # Gradual adjustment toward target
            new_confidence = current_confidence + (target_confidence - current_confidence) * self.learning_rate
            new_confidence = max(0.0, min(1.0, new_confidence))
            
            self.confidence_scores[fragment_id]['confidence'] = new_confidence

if __name__ == "__main__":
    # Test the meta-memory system
    print("🧪 Testing Meta-Memory System")
    
    # Mock cache
    class MockCache:
        def __init__(self):
            self.file_registry = {
                'frag1': {'content': 'I am certain this is correct', 'hits': 5, 'created': time.time()},
                'frag2': {'content': 'Maybe this is right, I think', 'hits': 3, 'created': time.time() - 86400},
                'frag3': {'content': 'This is definitely true', 'hits': 8, 'created': time.time() - 3600}
            }
    
    cache = MockCache()
    meta_memory = MetaMemorySystem(cache)
    
    # Test confidence assessment
    for fragment_id in cache.file_registry:
        content = cache.file_registry[fragment_id]['content']
        confidence_data = meta_memory.assess_confidence(fragment_id, content)
        print(f"Fragment {fragment_id}: {content[:30]}...")
        print(f"  Confidence: {confidence_data['confidence']:.2f}")
        print(f"  Category: {confidence_data['confidence_category']}")
        print()
    
    # Test uncertainty report
    report = meta_memory.generate_uncertainty_report()
    print("📊 Uncertainty Report:")
    print(f"  Average confidence: {report['confidence_stats']['average']:.2f}")
    print(f"  Knowledge gaps: {report['knowledge_gaps']['total_gaps']}")
    print(f"  Recommendations: {report['recommendations']}")
