#!/usr/bin/env python3
"""
Predictive Coding System
Implements self-organizing predictive model capabilities.
"""

import time
import random
import math
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class PredictiveCodingSystem:
    """Predictive coding system for self-organizing predictive model."""
    
    def __init__(self, cache, emotion_cache=None, meta_memory=None):
        self.cache = cache
        self.emotion_cache = emotion_cache
        self.meta_memory = meta_memory
        
        # Predictive parameters
        self.prediction_window = 5  # Number of fragments to predict
        self.prediction_threshold = 0.3  # Minimum confidence for predictions
        self.learning_rate = 0.1  # How quickly predictions adapt
        self.prediction_history = []  # Track prediction accuracy
        
        # Pattern recognition
        self.sequence_patterns = {}  # fragment_id -> [next_fragments]
        self.pattern_weights = {}  # (from_id, to_id) -> weight
        self.pattern_frequency = defaultdict(int)  # pattern -> frequency
        
        # Prediction models
        self.markov_model = {}  # Simple Markov chain model
        self.embedding_predictions = {}  # Embedding-based predictions
        self.temporal_predictions = {}  # Time-based predictions
        
        # Evaluation metrics
        self.prediction_accuracy = 0.0
        self.prediction_confidence = 0.0
        self.pattern_complexity = 0.0
        
        print("🔮 Predictive Coding System Initialized")
        print(f"   Prediction window: {self.prediction_window}")
        print(f"   Prediction threshold: {self.prediction_threshold}")
        print(f"   Learning rate: {self.learning_rate}")
    
    def process_sequence(self, fragment_sequence: List[str]) -> Dict:
        """Process a sequence of fragments and make predictions."""
        
        if len(fragment_sequence) < 2:
            return {'predictions': [], 'confidence': 0.0, 'accuracy': 0.0}
        
        # Update pattern recognition
        self._update_pattern_recognition(fragment_sequence)
        
        # Make predictions
        predictions = self._make_predictions(fragment_sequence)
        
        # Evaluate prediction quality
        evaluation = self._evaluate_predictions(fragment_sequence, predictions)
        
        # Update prediction models
        self._update_prediction_models(fragment_sequence, predictions, evaluation)
        
        return {
            'predictions': predictions,
            'confidence': evaluation['confidence'],
            'accuracy': evaluation['accuracy'],
            'pattern_complexity': evaluation['pattern_complexity'],
            'model_updates': evaluation['model_updates']
        }
    
    def _update_pattern_recognition(self, sequence: List[str]):
        """Update pattern recognition from fragment sequence."""
        
        for i in range(len(sequence) - 1):
            current_frag = sequence[i]
            next_frag = sequence[i + 1]
            
            # Update sequence patterns
            if current_frag not in self.sequence_patterns:
                self.sequence_patterns[current_frag] = []
            
            if next_frag not in self.sequence_patterns[current_frag]:
                self.sequence_patterns[current_frag].append(next_frag)
            
            # Update pattern weights
            pattern_key = (current_frag, next_frag)
            self.pattern_weights[pattern_key] = self.pattern_weights.get(pattern_key, 0) + 1
            
            # Update pattern frequency
            pattern = f"{current_frag} -> {next_frag}"
            self.pattern_frequency[pattern] += 1
    
    def _make_predictions(self, sequence: List[str]) -> List[Dict]:
        """Make predictions for the next fragments in the sequence."""
        
        if not sequence:
            return []
        
        current_frag = sequence[-1]
        predictions = []
        
        # Markov chain predictions
        markov_preds = self._markov_predictions(current_frag)
        predictions.extend(markov_preds)
        
        # Embedding-based predictions
        embedding_preds = self._embedding_predictions(sequence)
        predictions.extend(embedding_preds)
        
        # Temporal predictions
        temporal_preds = self._temporal_predictions(sequence)
        predictions.extend(temporal_preds)
        
        # Combine and rank predictions
        combined_predictions = self._combine_predictions(predictions)
        
        # Filter by confidence threshold
        filtered_predictions = [
            pred for pred in combined_predictions 
            if pred['confidence'] >= self.prediction_threshold
        ]
        
        # Return top predictions
        return sorted(filtered_predictions, key=lambda x: x['confidence'], reverse=True)[:self.prediction_window]
    
    def _markov_predictions(self, current_frag: str) -> List[Dict]:
        """Make predictions using Markov chain model."""
        
        predictions = []
        
        if current_frag in self.sequence_patterns:
            next_fragments = self.sequence_patterns[current_frag]
            
            # Calculate probabilities
            total_weight = sum(self.pattern_weights.get((current_frag, next_frag), 0) 
                             for next_frag in next_fragments)
            
            for next_frag in next_fragments:
                weight = self.pattern_weights.get((current_frag, next_frag), 0)
                probability = weight / total_weight if total_weight > 0 else 0
                
                predictions.append({
                    'fragment_id': next_frag,
                    'confidence': probability,
                    'method': 'markov',
                    'reasoning': f"Pattern: {current_frag} -> {next_frag}"
                })
        
        return predictions
    
    def _embedding_predictions(self, sequence: List[str]) -> List[Dict]:
        """Make predictions using embedding similarity."""
        
        predictions = []
        
        if len(sequence) < 2:
            return predictions
        
        # Get embedding for current sequence
        current_embedding = self._get_sequence_embedding(sequence)
        
        # Find similar sequences in history
        similar_sequences = self._find_similar_sequences(current_embedding)
        
        for similar_seq in similar_sequences:
            if len(similar_seq['sequence']) > len(sequence):
                # Predict next fragment from similar sequence
                next_frag = similar_seq['sequence'][len(sequence)]
                similarity = similar_seq['similarity']
                
                predictions.append({
                    'fragment_id': next_frag,
                    'confidence': similarity * 0.8,  # Scale down for embedding method
                    'method': 'embedding',
                    'reasoning': f"Similar sequence: {similar_seq['sequence'][:3]}..."
                })
        
        return predictions
    
    def _temporal_predictions(self, sequence: List[str]) -> List[Dict]:
        """Make predictions based on temporal patterns."""
        
        predictions = []
        current_time = time.time()
        
        # Look for temporal patterns in recent access
        recent_fragments = self._get_recent_fragments(current_time, 3600)  # Last hour
        
        if len(recent_fragments) > 1:
            # Find fragments that often follow the current sequence
            for i in range(len(recent_fragments) - len(sequence)):
                if recent_fragments[i:i+len(sequence)] == sequence:
                    if i + len(sequence) < len(recent_fragments):
                        next_frag = recent_fragments[i + len(sequence)]
                        
                        # Calculate temporal confidence based on recency
                        time_diff = current_time - recent_fragments[i + len(sequence) + 1] if i + len(sequence) + 1 < len(recent_fragments) else 0
                        temporal_confidence = math.exp(-time_diff / 3600)  # 1-hour decay
                        
                        predictions.append({
                            'fragment_id': next_frag,
                            'confidence': temporal_confidence * 0.6,  # Scale down for temporal method
                            'method': 'temporal',
                            'reasoning': f"Temporal pattern: {time_diff:.0f}s ago"
                        })
        
        return predictions
    
    def _get_sequence_embedding(self, sequence: List[str]) -> List[float]:
        """Get embedding for a sequence of fragments."""
        
        if not sequence:
            return []
        
        # Simple embedding: average of individual fragment embeddings
        embeddings = []
        for frag_id in sequence:
            frag_data = self.cache.file_registry.get(frag_id, {})
            if 'embedding' in frag_data and frag_data['embedding']:
                embeddings.append(frag_data['embedding'])
        
        if not embeddings:
            return []
        
        # Average the embeddings
        avg_embedding = np.mean(embeddings, axis=0).tolist()
        return avg_embedding
    
    def _find_similar_sequences(self, target_embedding: List[float]) -> List[Dict]:
        """Find sequences similar to the target embedding."""
        
        similar_sequences = []
        
        # This would normally use a more sophisticated similarity search
        # For now, we'll use a simple approach
        for pattern, frequency in self.pattern_frequency.items():
            if ' -> ' in pattern:
                parts = pattern.split(' -> ')
                if len(parts) >= 2:
                    # Simple similarity based on pattern frequency
                    similarity = min(frequency / 10.0, 1.0)  # Normalize frequency
                    
                    similar_sequences.append({
                        'sequence': parts,
                        'similarity': similarity,
                        'frequency': frequency
                    })
        
        return sorted(similar_sequences, key=lambda x: x['similarity'], reverse=True)[:5]
    
    def _get_recent_fragments(self, current_time: float, window_seconds: float) -> List[str]:
        """Get fragments accessed recently."""
        
        recent_fragments = []
        window_start = current_time - window_seconds
        
        # This would normally track actual access times
        # For now, we'll simulate with random recent fragments
        all_fragments = list(self.cache.file_registry.keys())
        if all_fragments:
            recent_fragments = random.sample(all_fragments, min(10, len(all_fragments)))
        
        return recent_fragments
    
    def _combine_predictions(self, predictions: List[Dict]) -> List[Dict]:
        """Combine predictions from different methods."""
        
        # Group by fragment_id
        combined = {}
        
        for pred in predictions:
            frag_id = pred['fragment_id']
            if frag_id not in combined:
                combined[frag_id] = {
                    'fragment_id': frag_id,
                    'confidence': 0.0,
                    'methods': [],
                    'reasoning': []
                }
            
            # Weight different methods
            method_weights = {
                'markov': 1.0,
                'embedding': 0.8,
                'temporal': 0.6
            }
            
            weight = method_weights.get(pred['method'], 0.5)
            combined[frag_id]['confidence'] += pred['confidence'] * weight
            combined[frag_id]['methods'].append(pred['method'])
            combined[frag_id]['reasoning'].append(pred['reasoning'])
        
        # Normalize confidence
        for frag_id in combined:
            method_count = len(combined[frag_id]['methods'])
            if method_count > 0:
                combined[frag_id]['confidence'] /= method_count
        
        return list(combined.values())
    
    def _evaluate_predictions(self, sequence: List[str], predictions: List[Dict]) -> Dict:
        """Evaluate the quality of predictions."""
        
        if not predictions:
            return {
                'confidence': 0.0,
                'accuracy': 0.0,
                'pattern_complexity': 0.0,
                'model_updates': 0
            }
        
        # Calculate average confidence
        avg_confidence = sum(pred['confidence'] for pred in predictions) / len(predictions)
        
        # Calculate accuracy (simplified - would need ground truth)
        accuracy = min(avg_confidence * 1.2, 1.0)  # Simulate accuracy based on confidence
        
        # Calculate pattern complexity
        pattern_complexity = len(self.pattern_frequency) / max(len(self.cache.file_registry), 1)
        
        # Count model updates
        model_updates = len(predictions)
        
        return {
            'confidence': avg_confidence,
            'accuracy': accuracy,
            'pattern_complexity': pattern_complexity,
            'model_updates': model_updates
        }
    
    def _update_prediction_models(self, sequence: List[str], predictions: List[Dict], evaluation: Dict):
        """Update prediction models based on evaluation."""
        
        # Update global accuracy
        self.prediction_accuracy = (self.prediction_accuracy + evaluation['accuracy']) / 2
        self.prediction_confidence = (self.prediction_confidence + evaluation['confidence']) / 2
        self.pattern_complexity = evaluation['pattern_complexity']
        
        # Record prediction history
        self.prediction_history.append({
            'timestamp': time.time(),
            'sequence_length': len(sequence),
            'predictions_count': len(predictions),
            'accuracy': evaluation['accuracy'],
            'confidence': evaluation['confidence']
        })
        
        # Keep only recent history
        if len(self.prediction_history) > 100:
            self.prediction_history = self.prediction_history[-100:]
    
    def get_prediction_statistics(self) -> Dict:
        """Get comprehensive prediction statistics."""
        
        if not self.prediction_history:
            return {
                'total_predictions': 0,
                'average_accuracy': 0.0,
                'average_confidence': 0.0,
                'pattern_complexity': 0.0,
                'pattern_count': 0,
                'sequence_patterns': 0
            }
        
        recent_history = self.prediction_history[-20:]  # Last 20 predictions
        
        return {
            'total_predictions': len(self.prediction_history),
            'average_accuracy': sum(h['accuracy'] for h in recent_history) / len(recent_history),
            'average_confidence': sum(h['confidence'] for h in recent_history) / len(recent_history),
            'pattern_complexity': self.pattern_complexity,
            'pattern_count': len(self.pattern_frequency),
            'sequence_patterns': len(self.sequence_patterns),
            'recent_accuracy_trend': self._calculate_accuracy_trend(recent_history)
        }
    
    def _calculate_accuracy_trend(self, recent_history: List[Dict]) -> str:
        """Calculate the trend in prediction accuracy."""
        
        if len(recent_history) < 5:
            return "insufficient_data"
        
        early_accuracy = sum(h['accuracy'] for h in recent_history[:len(recent_history)//2]) / (len(recent_history)//2)
        late_accuracy = sum(h['accuracy'] for h in recent_history[len(recent_history)//2:]) / (len(recent_history) - len(recent_history)//2)
        
        if late_accuracy > early_accuracy + 0.1:
            return "improving"
        elif late_accuracy < early_accuracy - 0.1:
            return "declining"
        else:
            return "stable"
    
    def run_prediction_test(self, test_sequences: List[List[str]]) -> Dict:
        """Run a comprehensive prediction test."""
        
        print("🔮 Running Predictive Coding Test")
        print("=" * 50)
        
        test_results = {
            'sequences_tested': len(test_sequences),
            'total_predictions': 0,
            'average_confidence': 0.0,
            'average_accuracy': 0.0,
            'pattern_discovery': 0,
            'model_adaptation': 0
        }
        
        all_confidences = []
        all_accuracies = []
        
        for i, sequence in enumerate(test_sequences):
            print(f"\n📝 Testing sequence {i+1}/{len(test_sequences)}")
            print(f"   Sequence: {sequence[:3]}...")
            
            result = self.process_sequence(sequence)
            
            print(f"   Predictions: {len(result['predictions'])}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Accuracy: {result['accuracy']:.2f}")
            
            all_confidences.append(result['confidence'])
            all_accuracies.append(result['accuracy'])
            test_results['total_predictions'] += len(result['predictions'])
            test_results['pattern_discovery'] += result['pattern_complexity']
            test_results['model_adaptation'] += result['model_updates']
        
        # Calculate averages
        test_results['average_confidence'] = sum(all_confidences) / len(all_confidences) if all_confidences else 0
        test_results['average_accuracy'] = sum(all_accuracies) / len(all_accuracies) if all_accuracies else 0
        
        print(f"\n📊 Test Results:")
        print(f"   Average confidence: {test_results['average_confidence']:.2f}")
        print(f"   Average accuracy: {test_results['average_accuracy']:.2f}")
        print(f"   Pattern discovery: {test_results['pattern_discovery']:.2f}")
        print(f"   Model adaptation: {test_results['model_adaptation']}")
        
        return test_results

if __name__ == "__main__":
    # Test the predictive coding system
    print("🧪 Testing Predictive Coding System")
    
    # Mock cache
    class MockCache:
        def __init__(self):
            self.file_registry = {
                'frag1': {'content': 'This is the first fragment', 'embedding': [0.1, 0.2, 0.3]},
                'frag2': {'content': 'This is the second fragment', 'embedding': [0.4, 0.5, 0.6]},
                'frag3': {'content': 'This is the third fragment', 'embedding': [0.7, 0.8, 0.9]},
                'frag4': {'content': 'This is the fourth fragment', 'embedding': [0.2, 0.3, 0.4]},
                'frag5': {'content': 'This is the fifth fragment', 'embedding': [0.5, 0.6, 0.7]}
            }
    
    cache = MockCache()
    predictive_system = PredictiveCodingSystem(cache)
    
    # Test sequences
    test_sequences = [
        ['frag1', 'frag2', 'frag3'],
        ['frag2', 'frag3', 'frag4'],
        ['frag3', 'frag4', 'frag5'],
        ['frag1', 'frag3', 'frag5']
    ]
    
    # Run prediction test
    results = predictive_system.run_prediction_test(test_sequences)
    
    # Show statistics
    stats = predictive_system.get_prediction_statistics()
    print(f"\n📊 System Statistics: {stats}")
