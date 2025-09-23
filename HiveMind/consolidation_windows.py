#!/usr/bin/env python3
"""
Consolidation Windows for CARMA
Implements multi-stage dream cycles: slow-wave sleep vs REM sleep.
"""

import time
import random
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

SLOW_WAVE_COOLDOWN_SECONDS = 60
DEFAULT_SLOW_WAVE_THRESHOLD = 0.6
DEFAULT_REM_THRESHOLD = 0.8
DEFAULT_SLOW_WAVE_DURATION_S = 5
DEFAULT_REM_DURATION_S = 3
DEFAULT_COMPRESSION_RATIO = 0.7
DEFAULT_CLUSTERING_THRESHOLD = 0.5
DEFAULT_CREATIVE_LINKING_PROB = 0.3
DEFAULT_REPLAY_PROBABILITY = 0.4


class ConsolidationWindows:
    """Multi-stage dream cycle system with different sleep stages."""
    
    def __init__(self, cache, emotion_cache=None):
        self.cache = cache
        self.emotion_cache = emotion_cache
        
        # Sleep stage parameters
        self.slow_wave_threshold = DEFAULT_SLOW_WAVE_THRESHOLD
        self.rem_threshold = DEFAULT_REM_THRESHOLD
        self.consolidation_cycles = 0
        self.last_sleep_time = 0
        
        # Slow-wave sleep parameters (structural consolidation)
        self.slow_wave_duration = DEFAULT_SLOW_WAVE_DURATION_S
        self.compression_ratio = DEFAULT_COMPRESSION_RATIO
        self.clustering_threshold = DEFAULT_CLUSTERING_THRESHOLD
        
        # REM sleep parameters (associative consolidation)
        self.rem_duration = DEFAULT_REM_DURATION_S
        self.creative_linking_prob = DEFAULT_CREATIVE_LINKING_PROB
        self.replay_probability = DEFAULT_REPLAY_PROBABILITY
        
        print("🌙 Consolidation Windows Initialized")
        print(f"   Slow-wave threshold: {self.slow_wave_threshold}")
        print(f"   REM threshold: {self.rem_threshold}")
        print(f"   Slow-wave duration: {self.slow_wave_duration}s")
        print(f"   REM duration: {self.rem_duration}s")
    
    def should_trigger_sleep(self) -> Tuple[bool, str]:
        """Determine if sleep should be triggered and what stage."""
        current_time = time.time()
        
        # Check if enough time has passed since last sleep
        if current_time - self.last_sleep_time < SLOW_WAVE_COOLDOWN_SECONDS:
            return False, "cooldown"
        
        # Calculate sleep pressure based on fragment count and activity
        fragment_count = len(self.cache.file_registry)
        if fragment_count < 10:
            return False, "insufficient_fragments"
        
        # Calculate activity level (simplified)
        activity_level = min(fragment_count / 100.0, 1.0)
        
        # Add emotional pressure if emotion cache is available
        if self.emotion_cache:
            emotion_summary = self.emotion_cache.get_emotional_summary()
            emotional_pressure = emotion_summary.get('avg_intensity', 0.0)
            activity_level += emotional_pressure * 0.3
        
        # Determine sleep stage
        if activity_level >= self.rem_threshold:
            return True, "rem"
        elif activity_level >= self.slow_wave_threshold:
            return True, "slow_wave"
        else:
            return False, "low_activity"
    
    def slow_wave_sleep(self) -> Dict:
        """Slow-wave sleep: structural consolidation and compression."""
        print("🌊 Entering Slow-Wave Sleep (Structural Consolidation)")
        start_time = time.time()
        
        results = {
            'stage': 'slow_wave',
            'duration': 0,
            'fragments_processed': 0,
            'compressions': 0,
            'clusters_created': 0,
            'fragments_before': len(self.cache.file_registry),
            'fragments_after': 0
        }
        
        # Get fragments for processing
        fragments = list(self.cache.file_registry.items())
        random.shuffle(fragments)  # Randomize processing order
        
        processed_count = 0
        compressions = 0
        clusters_created = 0
        
        # Process fragments in batches
        batch_size = max(1, len(fragments) // 10)
        
        for i in range(0, len(fragments), batch_size):
            batch = fragments[i:i + batch_size]
            
            # Structural consolidation: compress similar fragments
            compressed_fragments = self._compress_fragments(batch)
            compressions += len(compressed_fragments)
            
            # Create clusters of related fragments
            clusters = self._create_clusters(batch)
            clusters_created += len(clusters)
            
            processed_count += len(batch)
            
            # Simulate processing time
            time.sleep(0.1)
        
        # Update results
        results['duration'] = time.time() - start_time
        results['fragments_processed'] = processed_count
        results['compressions'] = compressions
        results['clusters_created'] = clusters_created
        results['fragments_after'] = len(self.cache.file_registry)
        
        print(f"🌊 Slow-Wave Sleep Complete: {results['duration']:.2f}s")
        print(f"   Processed: {results['fragments_processed']} fragments")
        print(f"   Compressions: {results['compressions']}")
        print(f"   Clusters: {results['clusters_created']}")
        
        return results
    
    def rem_sleep(self) -> Dict:
        """REM sleep: associative consolidation and creative linking."""
        print("💭 Entering REM Sleep (Associative Consolidation)")
        start_time = time.time()
        
        results = {
            'stage': 'rem',
            'duration': 0,
            'fragments_replayed': 0,
            'creative_links': 0,
            'associations_created': 0,
            'emotional_processing': 0
        }
        
        # Get fragments for replay
        fragments = list(self.cache.file_registry.items())
        random.shuffle(fragments)
        
        replayed_count = 0
        creative_links = 0
        associations_created = 0
        emotional_processing = 0
        
        # Replay fragments with creative linking
        for fragment_id, fragment_data in fragments:
            if random.random() < self.replay_probability:
                # Replay fragment
                self._replay_fragment(fragment_id, fragment_data)
                replayed_count += 1
                
                # Creative linking
                if random.random() < self.creative_linking_prob:
                    links = self._create_creative_links(fragment_id, fragments)
                    creative_links += len(links)
                    associations_created += len(links)
                
                # Emotional processing if emotion cache available
                if self.emotion_cache and fragment_id in self.emotion_cache.emotion_weights:
                    self._process_emotional_memory(fragment_id)
                    emotional_processing += 1
                
                # Simulate processing time
                time.sleep(0.05)
        
        # Update results
        results['duration'] = time.time() - start_time
        results['fragments_replayed'] = replayed_count
        results['creative_links'] = creative_links
        results['associations_created'] = associations_created
        results['emotional_processing'] = emotional_processing
        
        print(f"💭 REM Sleep Complete: {results['duration']:.2f}s")
        print(f"   Replayed: {results['fragments_replayed']} fragments")
        print(f"   Creative links: {results['creative_links']}")
        print(f"   Emotional processing: {results['emotional_processing']}")
        
        return results
    
    def _compress_fragments(self, fragments: List[Tuple]) -> List[str]:
        """Compress similar fragments together."""
        compressed = []
        
        for fragment_id, fragment_data in fragments:
            content = fragment_data.get('content', '')
            
            # Simple compression: combine with similar fragments
            if len(content) > 100:  # Only compress longer fragments
                # Find similar fragments
                similar_fragments = self._find_similar_fragments(fragment_id, fragments)
                
                if similar_fragments:
                    # Create compressed version
                    compressed_content = self._create_compressed_content(fragment_id, similar_fragments)
                    compressed.append(fragment_id)
        
        return compressed
    
    def _create_clusters(self, fragments: List[Tuple]) -> List[List[str]]:
        """Create clusters of related fragments."""
        clusters = []
        processed = set()
        
        for fragment_id, fragment_data in fragments:
            if fragment_id in processed:
                continue
            
            cluster = [fragment_id]
            processed.add(fragment_id)
            
            # Find related fragments
            for other_id, other_data in fragments:
                if other_id in processed:
                    continue
                
                similarity = self._calculate_similarity(fragment_data, other_data)
                if similarity > self.clustering_threshold:
                    cluster.append(other_id)
                    processed.add(other_id)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def _replay_fragment(self, fragment_id: str, fragment_data: Dict):
        """Replay a fragment to strengthen its connections."""
        # Update access count
        if 'hits' in fragment_data:
            fragment_data['hits'] = fragment_data.get('hits', 0) + 1
        
        # Update last accessed time
        fragment_data['last_accessed'] = time.time()
        
        # Strengthen existing connections
        if 'connections' in fragment_data:
            for connection in fragment_data['connections']:
                connection['strength'] = connection.get('strength', 1.0) * 1.1
    
    def _create_creative_links(self, fragment_id: str, all_fragments: List[Tuple]) -> List[str]:
        """Create creative, unexpected links between fragments."""
        creative_links = []
        
        # Find fragments that are semantically distant but could be creatively linked
        for other_id, other_data in all_fragments:
            if other_id == fragment_id:
                continue
            
            # Creative linking based on content keywords
            if self._has_creative_potential(fragment_id, other_id):
                # Create creative connection
                self._add_creative_connection(fragment_id, other_id)
                creative_links.append(other_id)
        
        return creative_links
    
    def _process_emotional_memory(self, fragment_id: str):
        """Process emotional memories during REM sleep."""
        if not self.emotion_cache:
            return
        
        emotion_data = self.emotion_cache.emotion_weights.get(fragment_id)
        if not emotion_data:
            return
        
        # Strengthen emotional memories
        if emotion_data['emotional_score'] > 0.5:
            emotion_data['emotional_boost'] = min(emotion_data['emotional_boost'] * 1.1, 2.0)
        
        # Create emotional associations
        if emotion_data['valence'] > 0.7:  # Very positive
            # Link to other positive memories
            positive_fragments = self.emotion_cache.find_emotional_fragments((0.5, 1.0))
            for pos_frag in positive_fragments[:3]:  # Link to top 3 positive
                self._add_emotional_connection(fragment_id, pos_frag, 'positive_association')
    
    def _find_similar_fragments(self, fragment_id: str, fragments: List[Tuple]) -> List[str]:
        """Find fragments similar to the given one."""
        similar = []
        target_content = self.cache.file_registry[fragment_id].get('content', '')
        
        for other_id, other_data in fragments:
            if other_id == fragment_id:
                continue
            
            other_content = other_data.get('content', '')
            similarity = self._calculate_text_similarity(target_content, other_content)
            
            if similarity > 0.3:  # Similarity threshold
                similar.append(other_id)
        
        return similar
    
    def _calculate_similarity(self, frag1: Dict, frag2: Dict) -> float:
        """Calculate similarity between two fragments."""
        content1 = frag1.get('content', '')
        content2 = frag2.get('content', '')
        return self._calculate_text_similarity(content1, content2)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity calculation."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _create_compressed_content(self, fragment_id: str, similar_fragments: List[str]) -> str:
        """Create compressed content from similar fragments."""
        # Simple compression: take key phrases from each fragment
        compressed_parts = []
        
        for frag_id in similar_fragments[:3]:  # Limit to 3 similar fragments
            content = self.cache.file_registry[frag_id].get('content', '')
            # Take first sentence as key phrase
            first_sentence = content.split('.')[0]
            compressed_parts.append(first_sentence)
        
        return ' | '.join(compressed_parts)
    
    def _has_creative_potential(self, frag1_id: str, frag2_id: str) -> bool:
        """Check if two fragments have creative linking potential."""
        content1 = self.cache.file_registry[frag1_id].get('content', '')
        content2 = self.cache.file_registry[frag2_id].get('content', '')
        
        # Look for creative keywords that could link different topics
        creative_keywords = ['like', 'similar', 'reminds', 'connection', 'relates', 'compare']
        
        for keyword in creative_keywords:
            if keyword in content1.lower() and keyword in content2.lower():
                return True
        
        return False
    
    def _add_creative_connection(self, frag1_id: str, frag2_id: str):
        """Add a creative connection between fragments."""
        try:
            links = self.cache.semantic_links
            links.setdefault(frag1_id, [])
            links.setdefault(frag2_id, [])
            if frag2_id not in links[frag1_id]:
                links[frag1_id].append(frag2_id)
            if frag1_id not in links[frag2_id]:
                links[frag2_id].append(frag1_id)
        except Exception:
            return
    
    def _add_emotional_connection(self, frag1_id: str, frag2_id: str, connection_type: str):
        """Add an emotional connection between fragments."""
        try:
            # Tag the link with an emotional marker in fragment analysis metadata
            f1 = self.cache.file_registry.get(frag1_id, {})
            f2 = self.cache.file_registry.get(frag2_id, {})
            f1.setdefault('analysis', {}).setdefault('emotional_links', []).append({
                'target': frag2_id,
                'type': connection_type,
                'timestamp': time.time()
            })
            f2.setdefault('analysis', {}).setdefault('emotional_links', []).append({
                'target': frag1_id,
                'type': connection_type,
                'timestamp': time.time()
            })
            # Also ensure semantic link exists
            self._add_creative_connection(frag1_id, frag2_id)
        except Exception:
            return
    
    def run_dream_cycle(self) -> Dict:
        """Run a complete dream cycle with both sleep stages."""
        should_sleep, reason = self.should_trigger_sleep()
        
        if not should_sleep:
            return {'status': 'no_sleep_needed', 'reason': reason}
        
        print(f"😴 Triggering Dream Cycle (reason: {reason})")
        
        cycle_results = {
            'timestamp': time.time(),
            'reason': reason,
            'stages': [],
            'total_duration': 0
        }
        
        start_time = time.time()
        
        # Run slow-wave sleep first
        if reason in ['slow_wave', 'rem']:
            slow_wave_results = self.slow_wave_sleep()
            cycle_results['stages'].append(slow_wave_results)
        
        # Run REM sleep if needed
        if reason == 'rem':
            rem_results = self.rem_sleep()
            cycle_results['stages'].append(rem_results)
        
        cycle_results['total_duration'] = time.time() - start_time
        self.consolidation_cycles += 1
        self.last_sleep_time = time.time()
        
        print(f"😴 Dream Cycle Complete: {cycle_results['total_duration']:.2f}s")
        print(f"   Total cycles: {self.consolidation_cycles}")
        
        return cycle_results

if __name__ == "__main__":
    # Test the consolidation windows
    print("🧪 Testing Consolidation Windows")
    
    # Mock cache
    class MockCache:
        def __init__(self):
            self.file_registry = {
                'frag1': {'content': 'I love this beautiful sunset', 'hits': 5},
                'frag2': {'content': 'The weather is terrible today', 'hits': 3},
                'frag3': {'content': 'I am so happy and excited', 'hits': 8},
                'frag4': {'content': 'This is amazing and wonderful', 'hits': 6}
            }
    
    cache = MockCache()
    consolidation = ConsolidationWindows(cache)
    
    # Test dream cycle
    results = consolidation.run_dream_cycle()
    print(f"Dream cycle results: {results}")
