#!/usr/bin/env python3
"""
Unified Cognitive CARMA System
Complete integration of all cognitive science and neuroscience enhancements.
"""

import sys
import time
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

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
from synaptic_tagging_system import SynapticTaggingSystem
from predictive_coding_system import PredictiveCodingSystem

# Constants
DEFAULT_CACHE_DIR = "Data/FractalCache"
MAX_MEMORY_SEQUENCE = 20
TOP_FRAGMENT_DETAILS = 3

class UnifiedCognitiveCarma:
    """Unified CARMA system with all cognitive enhancements integrated."""
    
    def __init__(self, base_dir: str = DEFAULT_CACHE_DIR):
        print("🧠 Initializing Unified Cognitive CARMA System")
        print("=" * 80)
        
        # Initialize base CARMA components
        self.cache = FractalMyceliumCache(base_dir)
        self.executive = CARMAExecutiveBrain(self.cache)
        self.meta_memory = CARMAMetaMemory(self.cache)
        self.consciousness = CARMA100PercentConsciousness(self.cache, self.executive, self.meta_memory)
        
        # Initialize cognitive enhancements
        self.emotion_cache = EmotionEnhancedCache(self.cache)
        self.consolidation = ConsolidationWindows(self.cache, self.emotion_cache)
        self.meta_memory_system = MetaMemorySystem(self.cache, self.emotion_cache)
        self.synaptic_tagging = SynapticTaggingSystem(self.cache, self.emotion_cache, self.meta_memory_system)
        self.predictive_coding = PredictiveCodingSystem(self.cache, self.emotion_cache, self.meta_memory_system)
        
        # System state
        self.total_queries = 0
        self.learning_cycles = 0
        self.cognitive_events = []
        self.personality_drift = {
            'conscientiousness': 0.0,
            'openness': 0.0,
            'extraversion': 0.0,
            'agreeableness': 0.0,
            'neuroticism': 0.0
        }
        
        # Memory sequence for predictive coding
        self.memory_sequence = []
        
        # Load existing cache if available
        self._load_existing_cache()
        
        print("✅ Unified Cognitive CARMA System Initialized")
        print(f"   Base cache: {len(self.cache.file_registry)} fragments")
        print(f"   Emotion tracking: Enabled")
        print(f"   Consolidation windows: Enabled")
        print(f"   Meta-memory: Enabled")
        print(f"   Synaptic tagging: Enabled")
        print(f"   Predictive coding: Enabled")
        print("=" * 80)
    
    def _load_existing_cache(self):
        """Load existing cache if available."""
        cache_file = f"{DEFAULT_CACHE_DIR}/registry.json"
        if Path(cache_file).exists():
            try:
                self.cache.load_registry()
                print(f"📂 Loaded existing cache: {len(self.cache.file_registry)} fragments")
                
                # Ensure embeddings are built
                self._ensure_embeddings()
                
            except Exception as e:
                print(f"⚠️  Error loading cache: {e}")
        else:
            print("📂 No existing cache found, starting fresh")
    
    def _ensure_embeddings(self):
        """Ensure all fragments have embeddings."""
        fragments_needing_embeddings = []
        for frag_id, frag_data in self.cache.file_registry.items():
            if 'embedding' not in frag_data or frag_data['embedding'] is None:
                fragments_needing_embeddings.append(frag_id)
        
        if fragments_needing_embeddings:
            print(f"🔗 Building embeddings for {len(fragments_needing_embeddings)} fragments...")
            for frag_id in fragments_needing_embeddings:
                frag_data = self.cache.file_registry[frag_id]
                content = frag_data.get('content', '')
                if content:
                    embedding = self.cache.embedder.embed(content)
                    if embedding:
                        frag_data['embedding'] = embedding
            print("✅ Embeddings built")
        
        # Build index
        try:
            self.cache.ensure_embedding_index()
            print("✅ Index built")
        except Exception as e:
            print(f"⚠️  Index build warning: {e}")
    
    def process_query(self, query: str, context: Dict = None) -> Dict:
        """Process a query through the complete unified cognitive system."""
        
        self.total_queries += 1
        start_time = time.time()
        
        print(f"\n🔍 Processing Query #{self.total_queries}: {query[:50]}...")
        
        # 1. Add query as a fragment with emotional analysis
        frag_id = self.cache.create_fragment(query)
        self.emotion_cache.add_emotional_fragment(frag_id, query)
        
        # 2. Generate embedding for query
        query_embedding = self.cache.embedder.embed(query)
        
        # 3. Find relevant fragments using embeddings
        relevant_fragments = self.cache.find_relevant_fragments(query, max_results=5)
        
        # 4. Process through synaptic tagging
        tagging_results = []
        for fragment in relevant_fragments:
            frag_id = fragment.get('file_id', 'unknown')
            tagging_result = self.synaptic_tagging.process_memory_access(frag_id)
            tagging_results.append(tagging_result)
        
        # 5. Assess confidence and emotional content
        fragment_confidences = {}
        emotional_weights = {}
        
        for fragment in relevant_fragments:
            frag_id = fragment.get('file_id', 'unknown')
            content = fragment.get('content', '')
            
            # Confidence assessment
            confidence_data = self.meta_memory_system.assess_confidence(frag_id, content, context)
            fragment_confidences[frag_id] = confidence_data
            
            # Emotional weighting
            emotional_weight = self.emotion_cache.get_emotional_weight(frag_id)
            emotional_weights[frag_id] = emotional_weight
            
            # Record access for emotional memory
            self.emotion_cache.access_fragment(frag_id)
        
        # 6. Update memory sequence for predictive coding
        fragment_ids = [f.get('file_id', 'unknown') for f in relevant_fragments]
        self.memory_sequence.extend(fragment_ids)
        if len(self.memory_sequence) > MAX_MEMORY_SEQUENCE:  # Keep last N fragments
            self.memory_sequence = self.memory_sequence[-MAX_MEMORY_SEQUENCE:]
        
        # 7. Make predictions
        prediction_results = self.predictive_coding.process_sequence(self.memory_sequence)
        
        # 8. Generate cognitive response
        response = self._generate_cognitive_response(query, relevant_fragments, 
                                                   fragment_confidences, emotional_weights, 
                                                   prediction_results)
        
        # 9. Update personality based on all cognitive factors
        self._update_cognitive_personality(query, response, emotional_weights, 
                                         fragment_confidences, prediction_results)
        
        # 10. Check for dream cycle trigger
        dream_results = self.consolidation.run_dream_cycle()
        
        # 11. Apply cognitive decay
        self.emotion_cache.decay_emotions()
        self.synaptic_tagging.decay_tags()
        
        processing_time = time.time() - start_time
        
        # Record cognitive event
        cognitive_event = {
            'timestamp': time.time(),
            'query': query,
            'processing_time': processing_time,
            'fragments_found': len(relevant_fragments),
            'tagging_events': len([r for r in tagging_results if r['tagging_triggered']]),
            'predictions_made': len(prediction_results['predictions']),
            'dream_cycle_triggered': dream_results.get('status') != 'no_sleep_needed',
            'personality_drift': self.personality_drift.copy()
        }
        self.cognitive_events.append(cognitive_event)
        
        # Compile comprehensive results
        results = {
            'query': query,
            'response': response,
            'processing_time': processing_time,
            'fragments_found': len(relevant_fragments),
            'fragment_confidences': fragment_confidences,
            'emotional_weights': emotional_weights,
            'tagging_results': tagging_results,
            'prediction_results': prediction_results,
            'dream_cycle': dream_results,
            'personality_drift': self.personality_drift.copy(),
            'cognitive_event': cognitive_event,
            'system_stats': self.get_comprehensive_stats()
        }
        
        print(f"✅ Query processed in {processing_time:.2f}s")
        print(f"   Fragments: {len(relevant_fragments)}")
        print(f"   Tagging events: {cognitive_event['tagging_events']}")
        print(f"   Predictions: {cognitive_event['predictions_made']}")
        print(f"   Dream cycle: {dream_results.get('status', 'none')}")
        
        return results
    
    def _generate_cognitive_response(self, query: str, fragments: List, 
                                   confidences: Dict, emotional_weights: Dict,
                                   predictions: Dict) -> str:
        """Generate a response using all cognitive enhancements."""
        
        response_parts = [f"🧠 Cognitive Analysis: {query}"]
        response_parts.append(f"📊 Found {len(fragments)} relevant fragments")
        
        # Add fragment analysis
        for i, fragment in enumerate(fragments[:TOP_FRAGMENT_DETAILS]):  # Use top N fragments
            frag_id = fragment.get('file_id', 'unknown')
            content = fragment.get('content', '')
            
            confidence = confidences.get(frag_id, {}).get('confidence', 0.5)
            emotional_weight = emotional_weights.get(frag_id, 1.0)
            
            # Add cognitive indicators
            if confidence > 0.7:
                confidence_indicator = " (high confidence)"
            elif confidence > 0.3:
                confidence_indicator = " (medium confidence)"
            else:
                confidence_indicator = " (uncertain)"
            
            if emotional_weight > 1.5:
                emotional_indicator = " [emotional memory]"
            else:
                emotional_indicator = ""
            
            response_parts.append(f"  {i+1}. {content[:100]}...{confidence_indicator}{emotional_indicator}")
        
        # Add prediction insights
        if predictions['predictions']:
            response_parts.append(f"\n🔮 Predictive Insights:")
            for pred in predictions['predictions'][:2]:  # Top 2 predictions
                response_parts.append(f"  • {pred['fragment_id'][:8]}... (confidence: {pred['confidence']:.2f})")
        
        # Add personality insights
        if any(abs(v) > 0.01 for v in self.personality_drift.values()):
            response_parts.append(f"\n👤 Personality Drift:")
            for trait, value in self.personality_drift.items():
                if abs(value) > 0.01:
                    response_parts.append(f"  • {trait}: {value:+.3f}")
        
        return "\n".join(response_parts)
    
    def _update_cognitive_personality(self, query: str, response: str, 
                                    emotional_weights: Dict, confidences: Dict,
                                    predictions: Dict):
        """Update personality based on all cognitive factors."""
        
        # Analyze emotional content
        query_emotion = self.emotion_cache.analyze_emotional_content(query)
        response_emotion = self.emotion_cache.analyze_emotional_content(response)
        
        # Calculate cognitive factors
        avg_confidence = sum(c.get('confidence', 0.5) for c in confidences.values()) / max(len(confidences), 1)
        avg_emotional_weight = sum(emotional_weights.values()) / max(len(emotional_weights), 1)
        prediction_confidence = predictions.get('confidence', 0.0)
        
        # Update personality based on multiple factors
        valence = (query_emotion['valence'] + response_emotion['valence']) / 2
        intensity = (query_emotion['intensity'] + response_emotion['intensity']) / 2
        
        # Emotional personality updates
        if valence > 0.5 and intensity > 0.3:
            self.personality_drift['extraversion'] += 0.01
            self.personality_drift['agreeableness'] += 0.01
        elif valence < -0.5 and intensity > 0.3:
            self.personality_drift['neuroticism'] += 0.01
        
        # Confidence-based updates
        if avg_confidence > 0.7:
            self.personality_drift['conscientiousness'] += 0.005
        elif avg_confidence < 0.3:
            self.personality_drift['neuroticism'] += 0.005
        
        # Prediction-based updates
        if prediction_confidence > 0.6:
            self.personality_drift['openness'] += 0.003
        
        # Emotional weight updates
        if avg_emotional_weight > 1.5:
            self.personality_drift['extraversion'] += 0.002
    
    def get_comprehensive_stats(self) -> Dict:
        """Get comprehensive statistics from all cognitive systems."""
        
        # Base cache stats
        cache_stats = {
            'total_fragments': len(self.cache.file_registry),
            'fragments_with_embeddings': sum(1 for frag in self.cache.file_registry.values() 
                                           if 'embedding' in frag and frag['embedding'] is not None)
        }
        
        # Emotion stats
        emotion_stats = self.emotion_cache.get_emotional_summary()
        
        # Meta-memory stats
        meta_memory_stats = self.meta_memory_system.generate_uncertainty_report()
        
        # Synaptic tagging stats
        tagging_stats = self.synaptic_tagging.get_tagging_statistics()
        
        # Predictive coding stats
        prediction_stats = self.predictive_coding.get_prediction_statistics()
        
        # Consolidation stats
        consolidation_stats = {
            'total_cycles': self.consolidation.consolidation_cycles,
            'last_sleep': self.consolidation.last_sleep_time
        }
        
        # Cognitive events stats
        recent_events = self.cognitive_events[-10:] if self.cognitive_events else []
        cognitive_stats = {
            'total_events': len(self.cognitive_events),
            'recent_events': len(recent_events),
            'avg_processing_time': sum(e['processing_time'] for e in recent_events) / max(len(recent_events), 1),
            'tagging_events': sum(e['tagging_events'] for e in recent_events),
            'prediction_events': sum(e['predictions_made'] for e in recent_events),
            'dream_cycles': sum(1 for e in recent_events if e['dream_cycle_triggered'])
        }
        
        return {
            'cache': cache_stats,
            'emotion': emotion_stats,
            'meta_memory': meta_memory_stats,
            'synaptic_tagging': tagging_stats,
            'predictive_coding': prediction_stats,
            'consolidation': consolidation_stats,
            'cognitive_events': cognitive_stats,
            'personality_drift': self.personality_drift,
            'total_queries': self.total_queries,
            'learning_cycles': self.learning_cycles
        }
    
    def run_comprehensive_test(self, test_queries: List[str]) -> Dict:
        """Run a comprehensive test of the unified system."""
        
        print(f"\n🧠 Running Comprehensive Test with {len(test_queries)} queries")
        print("=" * 80)
        
        test_start = time.time()
        test_results = []
        
        for i, query in enumerate(test_queries):
            print(f"\n📝 Test Query {i+1}/{len(test_queries)}")
            result = self.process_query(query)
            test_results.append(result)
            
            # Trigger learning cycle every 5 queries
            if (i + 1) % 5 == 0:
                self.learning_cycles += 1
                print(f"🔄 Learning cycle {self.learning_cycles} triggered")
        
        test_duration = time.time() - test_start
        
        # Generate comprehensive test summary
        test_summary = {
            'queries_processed': len(test_queries),
            'test_duration': test_duration,
            'avg_processing_time': sum(r['processing_time'] for r in test_results) / len(test_results),
            'total_tagging_events': sum(r['cognitive_event']['tagging_events'] for r in test_results),
            'total_predictions': sum(r['cognitive_event']['predictions_made'] for r in test_results),
            'dream_cycles_triggered': sum(1 for r in test_results if r['dream_cycle'].get('status') != 'no_sleep_needed'),
            'personality_drift': self.personality_drift.copy(),
            'final_system_stats': self.get_comprehensive_stats()
        }
        
        print(f"\n✅ Comprehensive Test Complete: {test_duration:.2f}s")
        print(f"   Tagging events: {test_summary['total_tagging_events']}")
        print(f"   Predictions: {test_summary['total_predictions']}")
        print(f"   Dream cycles: {test_summary['dream_cycles_triggered']}")
        print(f"   Personality drift: {self.personality_drift}")
        
        return test_summary

if __name__ == "__main__":
    # Test the unified cognitive CARMA system
    print("🧪 Testing Unified Cognitive CARMA System")
    
    # Initialize system
    system = UnifiedCognitiveCarma()
    
    # Test queries with cognitive complexity
    test_queries = [
        "I am absolutely thrilled about this amazing scientific discovery!",
        "This research shows that memory consolidation happens during sleep.",
        "I'm not entirely sure about this hypothesis, but it seems plausible.",
        "The neural networks in the brain form complex interconnected patterns.",
        "I feel confident that this approach will lead to breakthroughs.",
        "Maybe we should consider alternative explanations for this phenomenon.",
        "The emotional impact of this discovery cannot be overstated.",
        "I predict that future research will validate these findings.",
        "This is a weak memory that might get reinforced by stronger ones.",
        "The cognitive architecture shows remarkable self-organizing properties."
    ]
    
    # Run comprehensive test
    results = system.run_comprehensive_test(test_queries)
    
    print("\n📊 Final System Stats:")
    stats = system.get_comprehensive_stats()
    for category, data in stats.items():
        print(f"  {category}: {data}")
