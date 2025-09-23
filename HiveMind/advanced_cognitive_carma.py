#!/usr/bin/env python3
"""
Advanced Cognitive CARMA System
Complete integration of all cognitive science and neuroscience enhancements.
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
from synaptic_tagging_system import SynapticTaggingSystem
from predictive_coding_system import PredictiveCodingSystem

class AdvancedCognitiveCarma:
    """Complete cognitive CARMA system with all enhancements."""
    
    def __init__(self, base_dir: str = "Data/FractalCache"):
        print("🧠 Initializing Advanced Cognitive CARMA System")
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
        
        print("✅ Advanced Cognitive CARMA System Initialized")
        print(f"   Base cache: {len(self.cache.file_registry)} fragments")
        print(f"   Emotion tracking: Enabled")
        print(f"   Consolidation windows: Enabled")
        print(f"   Meta-memory: Enabled")
        print(f"   Synaptic tagging: Enabled")
        print(f"   Predictive coding: Enabled")
    
    def process_cognitive_query(self, query: str, context: Dict = None) -> Dict:
        """Process a query through the complete cognitive system."""
        
        self.total_queries += 1
        start_time = time.time()
        
        print(f"\n🔍 Processing Cognitive Query #{self.total_queries}: {query[:50]}...")
        
        # 1. Generate embedding for query
        query_embedding = self.cache.embedder.embed(query)
        
        # 2. Find relevant fragments
        relevant_fragments = self.cache.find_relevant(query_embedding, topk=5)
        
        # 3. Process through synaptic tagging
        tagging_results = []
        for fragment in relevant_fragments:
            if hasattr(fragment, 'id'):
                frag_id = fragment.id
            else:
                frag_id = fragment.get('file_id', 'unknown')
            
            tagging_result = self.synaptic_tagging.process_memory_access(frag_id)
            tagging_results.append(tagging_result)
        
        # 4. Assess confidence and emotional content
        fragment_confidences = {}
        emotional_weights = {}
        
        for fragment in relevant_fragments:
            if hasattr(fragment, 'id'):
                frag_id = fragment.id
                content = fragment.content
            else:
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
        
        # 5. Update memory sequence for predictive coding
        fragment_ids = [f.id if hasattr(f, 'id') else f.get('file_id', 'unknown') for f in relevant_fragments]
        self.memory_sequence.extend(fragment_ids)
        if len(self.memory_sequence) > 20:  # Keep last 20 fragments
            self.memory_sequence = self.memory_sequence[-20:]
        
        # 6. Make predictions
        prediction_results = self.predictive_coding.process_sequence(self.memory_sequence)
        
        # 7. Generate cognitive response
        response = self._generate_cognitive_response(query, relevant_fragments, 
                                                   fragment_confidences, emotional_weights, 
                                                   prediction_results)
        
        # 8. Update personality based on all cognitive factors
        self._update_cognitive_personality(query, response, emotional_weights, 
                                         fragment_confidences, prediction_results)
        
        # 9. Check for dream cycle trigger
        dream_results = self.consolidation.run_dream_cycle()
        
        # 10. Apply cognitive decay
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
        
        print(f"✅ Cognitive query processed in {processing_time:.2f}s")
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
        for i, fragment in enumerate(fragments[:3]):  # Use top 3 fragments
            if hasattr(fragment, 'id'):
                frag_id = fragment.id
                content = fragment.content
            else:
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
    
    def run_cognitive_learning_session(self, queries: List[str], context: Dict = None) -> Dict:
        """Run a complete cognitive learning session."""
        
        print(f"\n🧠 Starting Cognitive Learning Session with {len(queries)} queries")
        print("=" * 80)
        
        session_start = time.time()
        session_results = []
        
        for i, query in enumerate(queries):
            print(f"\n📝 Cognitive Query {i+1}/{len(queries)}")
            result = self.process_cognitive_query(query, context)
            session_results.append(result)
            
            # Trigger learning cycle every 5 queries
            if (i + 1) % 5 == 0:
                self.learning_cycles += 1
                print(f"🔄 Cognitive learning cycle {self.learning_cycles} triggered")
        
        session_duration = time.time() - session_start
        
        # Generate comprehensive session summary
        session_summary = {
            'queries_processed': len(queries),
            'session_duration': session_duration,
            'avg_processing_time': sum(r['processing_time'] for r in session_results) / len(session_results),
            'total_tagging_events': sum(r['cognitive_event']['tagging_events'] for r in session_results),
            'total_predictions': sum(r['cognitive_event']['predictions_made'] for r in session_results),
            'dream_cycles_triggered': sum(1 for r in session_results if r['dream_cycle'].get('status') != 'no_sleep_needed'),
            'personality_drift': self.personality_drift.copy(),
            'final_system_stats': self.get_comprehensive_stats()
        }
        
        print(f"\n✅ Cognitive Learning Session Complete: {session_duration:.2f}s")
        print(f"   Tagging events: {session_summary['total_tagging_events']}")
        print(f"   Predictions: {session_summary['total_predictions']}")
        print(f"   Dream cycles: {session_summary['dream_cycles_triggered']}")
        print(f"   Personality drift: {self.personality_drift}")
        
        return session_summary

if __name__ == "__main__":
    # Test the advanced cognitive CARMA system
    print("🧪 Testing Advanced Cognitive CARMA System")
    
    # Initialize system
    system = AdvancedCognitiveCarma()
    
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
    
    # Run cognitive learning session
    results = system.run_cognitive_learning_session(test_queries)
    
    print("\n📊 Final Cognitive System Stats:")
    stats = system.get_comprehensive_stats()
    for category, data in stats.items():
        print(f"  {category}: {data}")
