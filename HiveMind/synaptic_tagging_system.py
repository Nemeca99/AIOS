#!/usr/bin/env python3
"""
Synaptic Tagging and Capture (STC) System
Implements temporal proximity reinforcement for weak-strong memory interactions.
"""

import time
import random
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import deque

class SynapticTaggingSystem:
    """Synaptic tagging system for temporal proximity reinforcement."""
    
    def __init__(self, cache, emotion_cache=None, meta_memory=None):
        self.cache = cache
        self.emotion_cache = emotion_cache
        self.meta_memory = meta_memory
        
        # Temporal tracking
        self.temporal_window = 300  # 5 minutes in seconds
        self.weak_memory_threshold = 0.3  # Below this = weak memory
        self.strong_memory_threshold = 0.7  # Above this = strong memory
        self.tagging_window = 60  # 1 minute tagging window
        
        # Memory traces
        self.memory_traces = {}  # fragment_id -> trace_data
        self.temporal_sequence = deque(maxlen=100)  # Recent memory access sequence
        self.tagging_events = []  # Track tagging events
        
        # Reinforcement parameters
        self.tagging_strength = 0.2  # How much weak memories get boosted
        self.capture_probability = 0.8  # Probability of successful capture
        self.decay_rate = 0.95  # How quickly tags decay
        
        print("🧬 Synaptic Tagging System Initialized")
        print(f"   Temporal window: {self.temporal_window}s")
        print(f"   Weak threshold: {self.weak_memory_threshold}")
        print(f"   Strong threshold: {self.strong_memory_threshold}")
        print(f"   Tagging strength: {self.tagging_strength}")
    
    def process_memory_access(self, fragment_id: str, access_time: float = None) -> Dict:
        """Process a memory access and check for synaptic tagging opportunities."""
        
        if access_time is None:
            access_time = time.time()
        
        # Add to temporal sequence
        self.temporal_sequence.append({
            'fragment_id': fragment_id,
            'timestamp': access_time,
            'strength': self._get_memory_strength(fragment_id)
        })
        
        # Check for tagging opportunities
        tagging_result = self._check_tagging_opportunities(fragment_id, access_time)
        
        # Update memory trace
        self._update_memory_trace(fragment_id, access_time, tagging_result)
        
        return tagging_result
    
    def _get_memory_strength(self, fragment_id: str) -> float:
        """Get the current strength of a memory fragment."""
        
        # Base strength from cache
        fragment_data = self.cache.file_registry.get(fragment_id, {})
        base_strength = fragment_data.get('hits', 0) / 10.0  # Normalize hits
        base_strength = min(base_strength, 1.0)  # Cap at 1.0
        
        # Add emotional boost if available
        if self.emotion_cache and fragment_id in self.emotion_cache.emotion_weights:
            emotional_weight = self.emotion_cache.get_emotional_weight(fragment_id)
            base_strength = (base_strength + emotional_weight) / 2
        
        # Add confidence boost if available
        if self.meta_memory and fragment_id in self.meta_memory.confidence_scores:
            confidence = self.meta_memory.confidence_scores[fragment_id]['confidence']
            base_strength = (base_strength + confidence) / 2
        
        return base_strength
    
    def _check_tagging_opportunities(self, fragment_id: str, access_time: float) -> Dict:
        """Check if this memory access triggers synaptic tagging."""
        
        current_strength = self._get_memory_strength(fragment_id)
        tagging_result = {
            'fragment_id': fragment_id,
            'timestamp': access_time,
            'strength': current_strength,
            'tagging_triggered': False,
            'weak_memories_boosted': [],
            'strong_memory_source': None
        }
        
        # Check if this is a strong memory that could boost weak ones
        if current_strength >= self.strong_memory_threshold:
            weak_memories = self._find_weak_memories_in_window(access_time)
            
            if weak_memories:
                tagging_result['tagging_triggered'] = True
                tagging_result['strong_memory_source'] = fragment_id
                
                # Boost weak memories
                for weak_mem in weak_memories:
                    if self._attempt_tagging_capture(weak_mem['fragment_id'], fragment_id):
                        boost_amount = self._calculate_boost_amount(weak_mem['strength'], current_strength)
                        self._apply_memory_boost(weak_mem['fragment_id'], boost_amount)
                        
                        tagging_result['weak_memories_boosted'].append({
                            'fragment_id': weak_mem['fragment_id'],
                            'boost_amount': boost_amount,
                            'original_strength': weak_mem['strength']
                        })
        
        # Check if this weak memory can be boosted by recent strong memories
        elif current_strength <= self.weak_memory_threshold:
            recent_strong = self._find_recent_strong_memories(access_time)
            
            if recent_strong:
                for strong_mem in recent_strong:
                    if self._attempt_tagging_capture(fragment_id, strong_mem['fragment_id']):
                        boost_amount = self._calculate_boost_amount(current_strength, strong_mem['strength'])
                        self._apply_memory_boost(fragment_id, boost_amount)
                        
                        tagging_result['tagging_triggered'] = True
                        tagging_result['weak_memories_boosted'].append({
                            'fragment_id': fragment_id,
                            'boost_amount': boost_amount,
                            'original_strength': current_strength
                        })
                        tagging_result['strong_memory_source'] = strong_mem['fragment_id']
                        break
        
        # Record tagging event
        if tagging_result['tagging_triggered']:
            self.tagging_events.append(tagging_result)
        
        return tagging_result
    
    def _find_weak_memories_in_window(self, access_time: float) -> List[Dict]:
        """Find weak memories that appeared recently."""
        
        weak_memories = []
        window_start = access_time - self.temporal_window
        
        # Check recent memory sequence
        for mem_trace in self.temporal_sequence:
            if (mem_trace['timestamp'] >= window_start and 
                mem_trace['timestamp'] < access_time and
                mem_trace['strength'] <= self.weak_memory_threshold):
                
                weak_memories.append(mem_trace)
        
        return weak_memories
    
    def _find_recent_strong_memories(self, access_time: float) -> List[Dict]:
        """Find strong memories that appeared recently."""
        
        strong_memories = []
        window_start = access_time - self.temporal_window
        
        # Check recent memory sequence
        for mem_trace in self.temporal_sequence:
            if (mem_trace['timestamp'] >= window_start and 
                mem_trace['timestamp'] < access_time and
                mem_trace['strength'] >= self.strong_memory_threshold):
                
                strong_memories.append(mem_trace)
        
        return strong_memories
    
    def _attempt_tagging_capture(self, weak_fragment_id: str, strong_fragment_id: str) -> bool:
        """Attempt to capture a weak memory with a strong memory."""
        
        # Check if fragments are semantically related
        if not self._are_fragments_related(weak_fragment_id, strong_fragment_id):
            return False
        
        # Check temporal proximity
        weak_trace = self.memory_traces.get(weak_fragment_id, {})
        strong_trace = self.memory_traces.get(strong_fragment_id, {})
        
        if not weak_trace or not strong_trace:
            return False
        
        time_diff = abs(weak_trace.get('last_access', 0) - strong_trace.get('last_access', 0))
        if time_diff > self.tagging_window:
            return False
        
        # Probability-based capture
        return random.random() < self.capture_probability
    
    def _are_fragments_related(self, frag1_id: str, frag2_id: str) -> bool:
        """Check if two fragments are semantically related."""
        
        frag1_data = self.cache.file_registry.get(frag1_id, {})
        frag2_data = self.cache.file_registry.get(frag2_id, {})
        
        content1 = frag1_data.get('content', '')
        content2 = frag2_data.get('content', '')
        
        # Simple semantic similarity check
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return False
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        similarity = intersection / union if union > 0 else 0
        return similarity > 0.1  # 10% word overlap threshold
    
    def _calculate_boost_amount(self, weak_strength: float, strong_strength: float) -> float:
        """Calculate how much to boost a weak memory."""
        
        # Boost is proportional to the strength difference
        strength_diff = strong_strength - weak_strength
        boost_amount = strength_diff * self.tagging_strength
        
        # Cap the boost
        max_boost = 0.5  # Maximum 50% boost
        return min(boost_amount, max_boost)
    
    def _apply_memory_boost(self, fragment_id: str, boost_amount: float):
        """Apply a boost to a memory fragment."""
        
        if fragment_id not in self.cache.file_registry:
            return
        
        fragment_data = self.cache.file_registry[fragment_id]
        
        # Increase hit count
        current_hits = fragment_data.get('hits', 0)
        boost_hits = int(boost_amount * 10)  # Convert boost to hit increase
        fragment_data['hits'] = current_hits + boost_hits
        
        # Add tagging metadata
        if 'synaptic_tags' not in fragment_data:
            fragment_data['synaptic_tags'] = []
        
        fragment_data['synaptic_tags'].append({
            'timestamp': time.time(),
            'boost_amount': boost_amount,
            'source': 'synaptic_tagging'
        })
        
        # Update memory trace
        if fragment_id in self.memory_traces:
            self.memory_traces[fragment_id]['total_boost'] = self.memory_traces[fragment_id].get('total_boost', 0) + boost_amount
            self.memory_traces[fragment_id]['last_boost'] = time.time()
    
    def _update_memory_trace(self, fragment_id: str, access_time: float, tagging_result: Dict):
        """Update the memory trace for a fragment."""
        
        if fragment_id not in self.memory_traces:
            self.memory_traces[fragment_id] = {
                'first_access': access_time,
                'last_access': access_time,
                'access_count': 0,
                'total_boost': 0,
                'tagging_events': []
            }
        
        trace = self.memory_traces[fragment_id]
        trace['last_access'] = access_time
        trace['access_count'] += 1
        
        if tagging_result['tagging_triggered']:
            trace['tagging_events'].append(tagging_result)
    
    def get_tagging_statistics(self) -> Dict:
        """Get statistics about synaptic tagging activity."""
        
        total_events = len(self.tagging_events)
        total_boosts = sum(len(event['weak_memories_boosted']) for event in self.tagging_events)
        
        # Calculate average boost amounts
        all_boosts = []
        for event in self.tagging_events:
            for boost in event['weak_memories_boosted']:
                all_boosts.append(boost['boost_amount'])
        
        avg_boost = sum(all_boosts) / len(all_boosts) if all_boosts else 0
        
        # Count fragments with synaptic tags
        tagged_fragments = 0
        for fragment_data in self.cache.file_registry.values():
            if 'synaptic_tags' in fragment_data and fragment_data['synaptic_tags']:
                tagged_fragments += 1
        
        return {
            'total_tagging_events': total_events,
            'total_memory_boosts': total_boosts,
            'average_boost_amount': avg_boost,
            'tagged_fragments': tagged_fragments,
            'temporal_sequence_length': len(self.temporal_sequence),
            'memory_traces_count': len(self.memory_traces)
        }
    
    def decay_tags(self):
        """Apply decay to synaptic tags over time."""
        
        current_time = time.time()
        
        for fragment_id, fragment_data in self.cache.file_registry.items():
            if 'synaptic_tags' in fragment_data:
                # Decay old tags
                for tag in fragment_data['synaptic_tags']:
                    age = current_time - tag['timestamp']
                    if age > 3600:  # 1 hour
                        tag['boost_amount'] *= self.decay_rate
                
                # Remove very weak tags
                fragment_data['synaptic_tags'] = [
                    tag for tag in fragment_data['synaptic_tags'] 
                    if tag['boost_amount'] > 0.01
                ]

if __name__ == "__main__":
    # Test the synaptic tagging system
    print("🧪 Testing Synaptic Tagging System")
    
    # Mock cache
    class MockCache:
        def __init__(self):
            self.file_registry = {
                'weak1': {'content': 'This is a weak memory', 'hits': 1},
                'weak2': {'content': 'Another weak memory', 'hits': 2},
                'strong1': {'content': 'This is a strong memory', 'hits': 8},
                'strong2': {'content': 'Another strong memory', 'hits': 9}
            }
    
    cache = MockCache()
    tagging_system = SynapticTaggingSystem(cache)
    
    # Simulate memory access sequence
    print("\n📝 Simulating memory access sequence...")
    
    # Access weak memory
    result1 = tagging_system.process_memory_access('weak1')
    print(f"Weak memory access: {result1}")
    
    # Access strong memory (should trigger tagging)
    result2 = tagging_system.process_memory_access('strong1')
    print(f"Strong memory access: {result2}")
    
    # Access another weak memory
    result3 = tagging_system.process_memory_access('weak2')
    print(f"Another weak memory access: {result3}")
    
    # Show statistics
    stats = tagging_system.get_tagging_statistics()
    print(f"\n📊 Tagging Statistics: {stats}")
