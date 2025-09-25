#!/usr/bin/env python3
"""
Emotion-Enhanced CARMA Cache
Adds emotional weighting and valence tracking to the fractal mycelium cache.
"""

import json
import time
import random
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import numpy as np

class EmotionEnhancedCache:
    """Enhanced cache with emotional weighting and valence tracking."""
    
    def __init__(self, base_cache):
        self.cache = base_cache
        self.emotion_weights = {}  # fragment_id -> emotion_data
        self.emotional_memories = {}  # High-valence memory tracking
        self.emotion_decay_rate = 0.95  # How quickly emotions fade
        self.emotion_boost_threshold = 0.7  # Threshold for emotional reinforcement
        
        print("💝 Emotion-Enhanced CARMA Cache Initialized")
        print(f"   Emotion decay rate: {self.emotion_decay_rate}")
        print(f"   Boost threshold: {self.emotion_boost_threshold}")
    
    def analyze_emotional_content(self, text: str) -> Dict[str, float]:
        """Analyze text for emotional content and return valence scores."""
        
        # Simple emotion detection based on keywords
        positive_words = [
            'happy', 'joy', 'excited', 'love', 'amazing', 'wonderful', 'great', 'excellent',
            'fantastic', 'beautiful', 'perfect', 'success', 'achievement', 'pride', 'grateful',
            'blessed', 'lucky', 'fortunate', 'delighted', 'thrilled', 'ecstatic', 'blissful'
        ]
        
        negative_words = [
            'sad', 'angry', 'frustrated', 'disappointed', 'hurt', 'pain', 'suffering', 'terrible',
            'awful', 'horrible', 'devastated', 'crushed', 'defeated', 'hopeless', 'despair',
            'fear', 'anxiety', 'worry', 'stress', 'tension', 'overwhelmed', 'exhausted'
        ]
        
        # Count emotional words
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate valence (-1 to 1)
        total_emotional_words = positive_count + negative_count
        if total_emotional_words == 0:
            valence = 0.0  # Neutral
        else:
            valence = (positive_count - negative_count) / total_emotional_words
        
        # Calculate intensity (0 to 1)
        intensity = min(total_emotional_words / 10.0, 1.0)  # Cap at 1.0
        
        # Calculate arousal (excitement level)
        arousal = min(len(text.split()) / 50.0, 1.0)  # Longer text = more arousal
        
        return {
            'valence': valence,  # -1 (negative) to 1 (positive)
            'intensity': intensity,  # 0 (weak) to 1 (strong)
            'arousal': arousal,  # 0 (calm) to 1 (excited)
            'emotional_score': abs(valence) * intensity * arousal  # Overall emotional impact
        }
    
    def add_emotional_fragment(self, fragment_id: str, content: str, metadata: Dict = None):
        """Add a fragment with emotional analysis."""
        
        # Analyze emotional content
        emotion_data = self.analyze_emotional_content(content)
        
        # Store emotion data
        self.emotion_weights[fragment_id] = {
            'valence': emotion_data['valence'],
            'intensity': emotion_data['intensity'],
            'arousal': emotion_data['arousal'],
            'emotional_score': emotion_data['emotional_score'],
            'created': time.time(),
            'last_accessed': time.time(),
            'access_count': 0,
            'emotional_boost': 1.0  # Multiplier for reinforcement
        }
        
        # If highly emotional, mark as special memory
        if emotion_data['emotional_score'] > self.emotion_boost_threshold:
            self.emotional_memories[fragment_id] = {
                'content': content,
                'emotion_data': emotion_data,
                'special_type': 'high_valence' if emotion_data['valence'] > 0 else 'high_negative',
                'created': time.time()
            }
            print(f"💝 High-emotion memory created: {fragment_id[:8]}... (valence: {emotion_data['valence']:.2f})")
        
        return emotion_data
    
    def get_emotional_weight(self, fragment_id: str) -> float:
        """Get the emotional weight for a fragment."""
        if fragment_id not in self.emotion_weights:
            return 1.0  # Default weight
        
        emotion_data = self.emotion_weights[fragment_id]
        
        # Calculate emotional weight based on:
        # 1. Emotional score (how emotional the content is)
        # 2. Recency (more recent = higher weight)
        # 3. Access count (more accessed = higher weight)
        
        emotional_score = emotion_data['emotional_score']
        recency_factor = math.exp(-(time.time() - emotion_data['last_accessed']) / 86400)  # 24h decay
        access_factor = 1.0 + (emotion_data['access_count'] * 0.1)  # Access boost
        
        weight = (1.0 + emotional_score) * recency_factor * access_factor * emotion_data['emotional_boost']
        
        return max(weight, 0.1)  # Minimum weight
    
    def access_fragment(self, fragment_id: str):
        """Record fragment access and update emotional weights."""
        if fragment_id in self.emotion_weights:
            self.emotion_weights[fragment_id]['last_accessed'] = time.time()
            self.emotion_weights[fragment_id]['access_count'] += 1
            
            # Apply emotional boost for high-valence memories
            emotion_data = self.emotion_weights[fragment_id]
            if emotion_data['emotional_score'] > 0.5:
                emotion_data['emotional_boost'] = min(emotion_data['emotional_boost'] * 1.05, 2.0)
    
    def decay_emotions(self):
        """Apply emotional decay over time."""
        current_time = time.time()
        
        for fragment_id, emotion_data in self.emotion_weights.items():
            # Decay emotional boost over time
            time_since_access = current_time - emotion_data['last_accessed']
            if time_since_access > 3600:  # 1 hour
                decay_factor = self.emotion_decay_rate ** (time_since_access / 3600)
                emotion_data['emotional_boost'] = max(emotion_data['emotional_boost'] * decay_factor, 1.0)
    
    def get_emotional_summary(self) -> Dict:
        """Get summary of emotional state of the cache."""
        if not self.emotion_weights:
            return {'total_fragments': 0, 'emotional_fragments': 0}
        
        total_fragments = len(self.emotion_weights)
        emotional_fragments = sum(1 for data in self.emotion_weights.values() 
                                if data['emotional_score'] > 0.1)
        
        avg_valence = np.mean([data['valence'] for data in self.emotion_weights.values()])
        avg_intensity = np.mean([data['intensity'] for data in self.emotion_weights.values()])
        avg_arousal = np.mean([data['arousal'] for data in self.emotion_weights.values()])
        
        high_valence_count = sum(1 for data in self.emotion_weights.values() 
                               if data['valence'] > 0.5)
        high_negative_count = sum(1 for data in self.emotion_weights.values() 
                                if data['valence'] < -0.5)
        
        return {
            'total_fragments': total_fragments,
            'emotional_fragments': emotional_fragments,
            'avg_valence': avg_valence,
            'avg_intensity': avg_intensity,
            'avg_arousal': avg_arousal,
            'high_valence_count': high_valence_count,
            'high_negative_count': high_negative_count,
            'special_memories': len(self.emotional_memories)
        }
    
    def find_emotional_fragments(self, valence_range: Tuple[float, float] = (-1.0, 1.0),
                                intensity_threshold: float = 0.0) -> List[str]:
        """Find fragments within specified emotional range."""
        matching_fragments = []
        
        for fragment_id, emotion_data in self.emotion_weights.items():
            valence = emotion_data['valence']
            intensity = emotion_data['intensity']
            
            if (valence_range[0] <= valence <= valence_range[1] and 
                intensity >= intensity_threshold):
                matching_fragments.append(fragment_id)
        
        return matching_fragments

if __name__ == "__main__":
    # Test the emotion-enhanced cache
    print("🧪 Testing Emotion-Enhanced Cache")
    
    # Mock base cache
    class MockCache:
        def __init__(self):
            self.file_registry = {}
    
    cache = MockCache()
    emotion_cache = EmotionEnhancedCache(cache)
    
    # Test emotional analysis
    test_texts = [
        "I am so happy and excited about this amazing achievement!",
        "This is terrible and I'm devastated by the horrible news.",
        "The weather is nice today.",
        "I love this beautiful sunset and feel so grateful for this moment."
    ]
    
    for i, text in enumerate(test_texts):
        fragment_id = f"test_{i}"
        emotion_data = emotion_cache.add_emotional_fragment(fragment_id, text)
        print(f"Text: {text[:50]}...")
        print(f"  Valence: {emotion_data['valence']:.2f}")
        print(f"  Intensity: {emotion_data['intensity']:.2f}")
        print(f"  Emotional Score: {emotion_data['emotional_score']:.2f}")
        print()
    
    # Test emotional summary
    summary = emotion_cache.get_emotional_summary()
    print("📊 Emotional Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
