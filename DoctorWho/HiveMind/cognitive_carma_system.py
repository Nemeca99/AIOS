#!/usr/bin/env python3
"""
Cognitive CARMA System
Integrates all cognitive science and neuroscience-inspired enhancements.
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from fractal_mycelium_cache import FractalMyceliumCache
from carma_100_percent_consciousness import CARMA100PercentConsciousness
from carma_executive_brain import CARMAExecutiveBrain
from carma_meta_memory import CARMAMetaMemory
from emotion_enhanced_cache import EmotionEnhancedCache
from consolidation_windows import ConsolidationWindows
from meta_memory_system import MetaMemorySystem

class CognitiveCarmaSystem:
    """Complete cognitive CARMA system with all enhancements."""
    
    def __init__(self, base_dir: str = "Data/FractalCache"):
        print("🧠 Initializing Cognitive CARMA System")
        print("=" * 60)
        
        # Initialize base CARMA components
        self.cache = FractalMyceliumCache(base_dir)
        self.executive = CARMAExecutiveBrain(self.cache)
        self.meta_memory = CARMAMetaMemory(self.cache)
        self.consciousness = CARMA100PercentConsciousness(self.cache, self.executive, self.meta_memory)
        
        # Initialize cognitive enhancements
        self.emotion_cache = EmotionEnhancedCache(self.cache)
        self.consolidation = ConsolidationWindows(self.cache, self.emotion_cache)
        self.meta_memory_system = MetaMemorySystem(self.cache, self.emotion_cache)
        
        # System state
        self.total_queries = 0
        self.learning_cycles = 0
        self.personality_drift = {
            'conscientiousness': 0.0,
            'openness': 0.0,
            'extraversion': 0.0,
            'agreeableness': 0.0,
            'neuroticism': 0.0
        }
        
        print("✅ Cognitive CARMA System Initialized")
        print(f"   Base cache: {len(self.cache.file_registry)} fragments")
        print(f"   Emotion tracking: Enabled")
        print(f"   Consolidation windows: Enabled")
        print(f"   Meta-memory: Enabled")
    
    def process_query(self, query: str, context: Dict = None) -> Dict:
        """Process a query through the complete cognitive system."""
        
        self.total_queries += 1
        start_time = time.time()
        
        print(f"\n🔍 Processing Query #{self.total_queries}: {query[:50]}...")
        
        # 1. Generate embedding for query
        query_embedding = self.cache.embedder.embed(query)
        
        # 2. Find relevant fragments
        relevant_fragments = self.cache.find_relevant(query_embedding, topk=5)
        
        # 3. Assess confidence for each fragment
        fragment_confidences = {}
        for fragment in relevant_fragments:
            if hasattr(fragment, 'id'):
                frag_id = fragment.id
                content = fragment.content
            else:
                frag_id = fragment.get('file_id', 'unknown')
                content = fragment.get('content', '')
            
            confidence_data = self.meta_memory_system.assess_confidence(frag_id, content, context)
            fragment_confidences[frag_id] = confidence_data
        
        # 4. Apply emotional weighting
        emotional_weights = {}
        for fragment in relevant_fragments:
            if hasattr(fragment, 'id'):
                frag_id = fragment.id
            else:
                frag_id = fragment.get('file_id', 'unknown')
            
            emotional_weight = self.emotion_cache.get_emotional_weight(frag_id)
            emotional_weights[frag_id] = emotional_weight
            
            # Record access for emotional memory
            self.emotion_cache.access_fragment(frag_id)
        
        # 5. Generate response (simplified)
        response = self._generate_cognitive_response(query, relevant_fragments, 
                                                   fragment_confidences, emotional_weights)
        
        # 6. Update personality based on emotional content
        self._update_personality_drift(query, response, emotional_weights)
        
        # 7. Check for dream cycle trigger
        dream_results = self.consolidation.run_dream_cycle()
        
        # 8. Apply emotional decay
        self.emotion_cache.decay_emotions()
        
        processing_time = time.time() - start_time
        
        # Compile results
        results = {
            'query': query,
            'response': response,
            'processing_time': processing_time,
            'fragments_found': len(relevant_fragments),
            'fragment_confidences': fragment_confidences,
            'emotional_weights': emotional_weights,
            'dream_cycle': dream_results,
            'personality_drift': self.personality_drift.copy(),
            'system_stats': self.get_system_stats()
        }
        
        print(f"✅ Query processed in {processing_time:.2f}s")
        print(f"   Fragments: {len(relevant_fragments)}")
        print(f"   Dream cycle: {dream_results.get('status', 'none')}")
        
        return results
    
    def _generate_cognitive_response(self, query: str, fragments: List, 
                                   confidences: Dict, emotional_weights: Dict) -> str:
        """Generate a response using cognitive enhancements."""
        
        # Simple response generation (in real system, this would use LLM)
        response_parts = [f"Based on {len(fragments)} relevant fragments:"]
        
        for i, fragment in enumerate(fragments[:3]):  # Use top 3 fragments
            if hasattr(fragment, 'id'):
                frag_id = fragment.id
                content = fragment.content
            else:
                frag_id = fragment.get('file_id', 'unknown')
                content = fragment.get('content', '')
            
            confidence = confidences.get(frag_id, {}).get('confidence', 0.5)
            emotional_weight = emotional_weights.get(frag_id, 1.0)
            
            # Add confidence indicator
            if confidence > 0.7:
                confidence_indicator = " (high confidence)"
            elif confidence > 0.3:
                confidence_indicator = " (medium confidence)"
            else:
                confidence_indicator = " (uncertain)"
            
            # Add emotional indicator
            if emotional_weight > 1.5:
                emotional_indicator = " [emotional memory]"
            else:
                emotional_indicator = ""
            
            response_parts.append(f"  {i+1}. {content[:100]}...{confidence_indicator}{emotional_indicator}")
        
        return "\n".join(response_parts)
    
    def _update_personality_drift(self, query: str, response: str, emotional_weights: Dict):
        """Update personality drift based on emotional content."""
        
        # Analyze emotional content of query and response
        query_emotion = self.emotion_cache.analyze_emotional_content(query)
        response_emotion = self.emotion_cache.analyze_emotional_content(response)
        
        # Update personality based on emotional patterns
        valence = (query_emotion['valence'] + response_emotion['valence']) / 2
        intensity = (query_emotion['intensity'] + response_emotion['intensity']) / 2
        
        # Map emotions to Big Five traits (simplified)
        if valence > 0.5 and intensity > 0.3:
            # Positive emotions increase extraversion and agreeableness
            self.personality_drift['extraversion'] += 0.01
            self.personality_drift['agreeableness'] += 0.01
        elif valence < -0.5 and intensity > 0.3:
            # Negative emotions increase neuroticism
            self.personality_drift['neuroticism'] += 0.01
        
        # High intensity increases openness
        if intensity > 0.5:
            self.personality_drift['openness'] += 0.005
        
        # Long responses increase conscientiousness
        if len(response) > 200:
            self.personality_drift['conscientiousness'] += 0.005
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics."""
        
        # Base cache stats
        cache_stats = {
            'total_fragments': len(self.cache.file_registry),
            'fragments_with_embeddings': sum(1 for frag in self.cache.file_registry.values() 
                                           if 'embedding' in frag and frag['embedding'] is not None)
        }
        
        # Emotion stats
        emotion_stats = self.emotion_cache.get_emotional_summary()
        
        # Meta-memory stats
        uncertainty_report = self.meta_memory_system.generate_uncertainty_report()
        
        # Consolidation stats
        consolidation_stats = {
            'total_cycles': self.consolidation.consolidation_cycles,
            'last_sleep': self.consolidation.last_sleep_time
        }
        
        return {
            'cache': cache_stats,
            'emotion': emotion_stats,
            'meta_memory': uncertainty_report,
            'consolidation': consolidation_stats,
            'personality_drift': self.personality_drift,
            'total_queries': self.total_queries,
            'learning_cycles': self.learning_cycles
        }
    
    def run_learning_session(self, queries: List[str], context: Dict = None) -> Dict:
        """Run a complete learning session with multiple queries."""
        
        print(f"\n🧠 Starting Learning Session with {len(queries)} queries")
        print("=" * 60)
        
        session_start = time.time()
        session_results = []
        
        for i, query in enumerate(queries):
            print(f"\n📝 Query {i+1}/{len(queries)}")
            result = self.process_query(query, context)
            session_results.append(result)
            
            # Trigger learning cycle every 5 queries
            if (i + 1) % 5 == 0:
                self.learning_cycles += 1
                print(f"🔄 Learning cycle {self.learning_cycles} triggered")
        
        session_duration = time.time() - session_start
        
        # Generate session summary
        session_summary = {
            'queries_processed': len(queries),
            'session_duration': session_duration,
            'avg_processing_time': sum(r['processing_time'] for r in session_results) / len(session_results),
            'dream_cycles_triggered': sum(1 for r in session_results if r['dream_cycle'].get('status') != 'no_sleep_needed'),
            'personality_drift': self.personality_drift.copy(),
            'final_system_stats': self.get_system_stats()
        }
        
        print(f"\n✅ Learning Session Complete: {session_duration:.2f}s")
        print(f"   Dream cycles: {session_summary['dream_cycles_triggered']}")
        print(f"   Personality drift: {self.personality_drift}")
        
        return session_summary

if __name__ == "__main__":
    # Test the complete cognitive CARMA system
    print("🧪 Testing Cognitive CARMA System")
    
    # Initialize system
    system = CognitiveCarmaSystem()
    
    # Test queries
    test_queries = [
        "I am so happy and excited about this amazing achievement!",
        "This is terrible and I'm devastated by the horrible news.",
        "The weather is nice today and I feel peaceful.",
        "I love this beautiful sunset and feel so grateful for this moment.",
        "I am certain this is correct and I have high confidence in it.",
        "Maybe this is right, I think, but I'm not completely sure.",
        "This is definitely true and I know it for certain."
    ]
    
    # Run learning session
    results = system.run_learning_session(test_queries)
    
    print("\n📊 Final System Stats:")
    stats = system.get_system_stats()
    for category, data in stats.items():
        print(f"  {category}: {data}")
