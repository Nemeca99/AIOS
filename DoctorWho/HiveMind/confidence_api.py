#!/usr/bin/env python3
"""
Confidence API
Returns similarity scores and confidence metrics for enterprise trust
"""

import json
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass
from .system_constants import SystemConfig, AssessmentCriteria

@dataclass
class QueryResult:
    """Structured query result with confidence metrics"""
    fragment_id: str
    content: str
    similarity_score: float
    confidence_level: str
    response_time: float
    fragment_level: int
    hit_count: int
    status: str

@dataclass
class ReconstructionResult:
    """Structured reconstruction result with confidence metrics"""
    fragment_id: str
    original_content: str
    reconstructed_content: str
    similarity_score: float
    confidence_level: str
    reconstruction_time: float
    method_used: str
    quality_indicators: Dict

class ConfidenceAPI:
    """API for confidence scoring and trust metrics"""
    
    def __init__(self):
        self.confidence_thresholds = {
            'high': SystemConfig.ENTERPRISE_SIMILARITY_THRESHOLD,  # 0.7
            'medium': 0.5,
            'low': 0.3
        }
    
    def calculate_confidence_level(self, similarity_score: float) -> str:
        """Calculate confidence level based on similarity score"""
        if similarity_score >= self.confidence_thresholds['high']:
            return 'high'
        elif similarity_score >= self.confidence_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def create_query_result(self, fragment_id: str, content: str, similarity_score: float, 
                          response_time: float, fragment_level: int = 0, 
                          hit_count: int = 0, status: str = 'active') -> QueryResult:
        """Create a structured query result with confidence metrics"""
        confidence_level = self.calculate_confidence_level(similarity_score)
        
        return QueryResult(
            fragment_id=fragment_id,
            content=content,
            similarity_score=similarity_score,
            confidence_level=confidence_level,
            response_time=response_time,
            fragment_level=fragment_level,
            hit_count=hit_count,
            status=status
        )
    
    def create_reconstruction_result(self, fragment_id: str, original_content: str,
                                  reconstructed_content: str, similarity_score: float,
                                  reconstruction_time: float, method_used: str = 'semantic') -> ReconstructionResult:
        """Create a structured reconstruction result with confidence metrics"""
        confidence_level = self.calculate_confidence_level(similarity_score)
        
        # Calculate quality indicators
        quality_indicators = self._calculate_quality_indicators(
            original_content, reconstructed_content, similarity_score
        )
        
        return ReconstructionResult(
            fragment_id=fragment_id,
            original_content=original_content,
            reconstructed_content=reconstructed_content,
            similarity_score=similarity_score,
            confidence_level=confidence_level,
            reconstruction_time=reconstruction_time,
            method_used=method_used,
            quality_indicators=quality_indicators
        )
    
    def _calculate_quality_indicators(self, original: str, reconstructed: str, 
                                    similarity_score: float) -> Dict:
        """Calculate quality indicators for reconstruction"""
        return {
            'length_ratio': len(reconstructed) / len(original) if original else 0.0,
            'word_overlap': self._calculate_word_overlap(original, reconstructed),
            'semantic_similarity': similarity_score,
            'content_completeness': min(1.0, len(reconstructed) / 100),  # Normalized completeness
            'quality_score': self._calculate_overall_quality(original, reconstructed, similarity_score)
        }
    
    def _calculate_word_overlap(self, text1: str, text2: str) -> float:
        """Calculate word overlap between two texts"""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_overall_quality(self, original: str, reconstructed: str, 
                                 similarity_score: float) -> float:
        """Calculate overall quality score"""
        word_overlap = self._calculate_word_overlap(original, reconstructed)
        length_ratio = len(reconstructed) / len(original) if original else 0.0
        
        # Weighted combination of factors
        quality = (
            similarity_score * 0.5 +  # Semantic similarity
            word_overlap * 0.3 +      # Word overlap
            min(1.0, length_ratio) * 0.2  # Length appropriateness
        )
        
        return min(1.0, max(0.0, quality))
    
    def generate_confidence_report(self, query_results: List[QueryResult], 
                                reconstruction_results: List[ReconstructionResult]) -> Dict:
        """Generate a comprehensive confidence report"""
        # Calculate query confidence metrics
        query_metrics = self._calculate_query_metrics(query_results)
        
        # Calculate reconstruction confidence metrics
        reconstruction_metrics = self._calculate_reconstruction_metrics(reconstruction_results)
        
        # Calculate overall system confidence
        overall_confidence = self._calculate_overall_confidence(query_metrics, reconstruction_metrics)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_confidence': overall_confidence,
            'query_metrics': query_metrics,
            'reconstruction_metrics': reconstruction_metrics,
            'confidence_distribution': self._calculate_confidence_distribution(query_results, reconstruction_results),
            'enterprise_readiness': self._assess_enterprise_readiness(overall_confidence, query_metrics, reconstruction_metrics)
        }
    
    def _calculate_query_metrics(self, results: List[QueryResult]) -> Dict:
        """Calculate query confidence metrics"""
        if not results:
            return {'avg_confidence': 0.0, 'success_rate': 0.0, 'avg_response_time': 0.0}
        
        total_similarity = sum(r.similarity_score for r in results)
        high_confidence_count = sum(1 for r in results if r.confidence_level == 'high')
        total_response_time = sum(r.response_time for r in results)
        
        return {
            'total_queries': len(results),
            'avg_similarity': total_similarity / len(results),
            'avg_confidence': self._confidence_to_numeric(results),
            'high_confidence_rate': high_confidence_count / len(results),
            'success_rate': sum(1 for r in results if r.similarity_score > 0.2) / len(results),
            'avg_response_time': total_response_time / len(results),
            'confidence_distribution': {
                'high': sum(1 for r in results if r.confidence_level == 'high'),
                'medium': sum(1 for r in results if r.confidence_level == 'medium'),
                'low': sum(1 for r in results if r.confidence_level == 'low')
            }
        }
    
    def _calculate_reconstruction_metrics(self, results: List[ReconstructionResult]) -> Dict:
        """Calculate reconstruction confidence metrics"""
        if not results:
            return {'avg_confidence': 0.0, 'success_rate': 0.0, 'avg_quality': 0.0}
        
        total_similarity = sum(r.similarity_score for r in results)
        high_confidence_count = sum(1 for r in results if r.confidence_level == 'high')
        total_quality = sum(r.quality_indicators['quality_score'] for r in results)
        total_time = sum(r.reconstruction_time for r in results)
        
        return {
            'total_reconstructions': len(results),
            'avg_similarity': total_similarity / len(results) if results else 0.0,
            'avg_confidence': self._confidence_to_numeric(results),
            'high_confidence_rate': high_confidence_count / len(results) if results else 0.0,
            'success_rate': sum(1 for r in results if r.similarity_score > 0.5) / len(results) if results else 0.0,
            'avg_quality_score': total_quality / len(results) if results else 0.0,
            'avg_reconstruction_time': total_time / len(results) if results else 0.0,
            'confidence_distribution': {
                'high': sum(1 for r in results if r.confidence_level == 'high'),
                'medium': sum(1 for r in results if r.confidence_level == 'medium'),
                'low': sum(1 for r in results if r.confidence_level == 'low')
            }
        }
    
    def _confidence_to_numeric(self, results: List) -> float:
        """Convert confidence levels to numeric scores"""
        if not results:
            return 0.0
        
        total_score = 0.0
        for result in results:
            if result.confidence_level == 'high':
                total_score += 1.0
            elif result.confidence_level == 'medium':
                total_score += 0.6
            else:  # low
                total_score += 0.3
        
        return total_score / len(results)
    
    def _calculate_confidence_distribution(self, query_results: List[QueryResult], 
                                         reconstruction_results: List[ReconstructionResult]) -> Dict:
        """Calculate overall confidence distribution"""
        all_results = list(query_results) + list(reconstruction_results)
        
        if not all_results:
            return {'high': 0, 'medium': 0, 'low': 0}
        
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        for result in all_results:
            distribution[result.confidence_level] += 1
        
        # Convert to percentages
        total = len(all_results)
        return {k: v / total for k, v in distribution.items()}
    
    def _calculate_overall_confidence(self, query_metrics: Dict, reconstruction_metrics: Dict) -> float:
        """Calculate overall system confidence"""
        query_weight = 0.3
        reconstruction_weight = 0.7
        
        overall = (
            query_metrics['avg_confidence'] * query_weight +
            reconstruction_metrics['avg_confidence'] * reconstruction_weight
        )
        
        return min(1.0, max(0.0, overall))
    
    def _assess_enterprise_readiness(self, overall_confidence: float, 
                                   query_metrics: Dict, reconstruction_metrics: Dict) -> Dict:
        """Assess enterprise readiness based on confidence metrics"""
        criteria = {
            'overall_confidence': overall_confidence >= 0.7,
            'query_success_rate': query_metrics['success_rate'] >= SystemConfig.ENTERPRISE_QUERY_SUCCESS_RATE,
            'reconstruction_success_rate': reconstruction_metrics['success_rate'] >= SystemConfig.ENTERPRISE_RECONSTRUCTION_RATE,
            'avg_response_time': query_metrics['avg_response_time'] <= SystemConfig.ENTERPRISE_RECOVERY_TIME_SECONDS,
            'high_confidence_rate': ((query_metrics.get('high_confidence_rate', 0) + reconstruction_metrics.get('high_confidence_rate', 0)) / 2) >= 0.5
        }
        
        ready_count = sum(criteria.values())
        total_criteria = len(criteria)
        
        return {
            'enterprise_ready': ready_count >= total_criteria * 0.8,  # 80% of criteria must be met
            'readiness_score': ready_count / total_criteria,
            'criteria_met': criteria,
            'recommendations': self._generate_recommendations(criteria)
        }
    
    def _generate_recommendations(self, criteria: Dict) -> List[str]:
        """Generate recommendations based on unmet criteria"""
        recommendations = []
        
        if not criteria['overall_confidence']:
            recommendations.append("Improve overall confidence scores through better semantic matching")
        
        if not criteria['query_success_rate']:
            recommendations.append("Enhance query processing to achieve higher success rates")
        
        if not criteria['reconstruction_success_rate']:
            recommendations.append("Improve reconstruction algorithms for better success rates")
        
        if not criteria['avg_response_time']:
            recommendations.append("Optimize response times for enterprise requirements")
        
        if not criteria['high_confidence_rate']:
            recommendations.append("Focus on achieving higher confidence levels in results")
        
        return recommendations

# === ENTERPRISE API FUNCTIONS ===

def create_enterprise_query_api(cache, confidence_api: ConfidenceAPI):
    """Create enterprise-ready query API with confidence metrics"""
    
    def query_with_confidence(query: str, topk: int = 3) -> List[QueryResult]:
        """Query with confidence metrics for enterprise use"""
        start_time = time.time()
        
        try:
            # Embed query
            embedding = cache.embedder.embed(query)
            
            # Find relevant fragments
            results = cache.find_relevant(embedding, topk)
            
            response_time = time.time() - start_time
            
            # Convert to confidence API results
            confidence_results = []
            for result in results:
                confidence_result = confidence_api.create_query_result(
                    fragment_id=result.id,
                    content=result.content,
                    similarity_score=result.score,
                    response_time=response_time,
                    fragment_level=getattr(result, 'level', 0),
                    hit_count=getattr(result, 'hits', 0),
                    status=getattr(result, 'status', 'active')
                )
                confidence_results.append(confidence_result)
            
            return confidence_results
            
        except Exception as e:
            # Return empty results on error
            return []
    
    return query_with_confidence

def create_enterprise_reconstruction_api(cache, confidence_api: ConfidenceAPI):
    """Create enterprise-ready reconstruction API with confidence metrics"""
    
    def reconstruct_with_confidence(fragment_id: str, original_content: str) -> Optional[ReconstructionResult]:
        """Reconstruct fragment with confidence metrics for enterprise use"""
        start_time = time.time()
        
        try:
            # Use existing reconstruction logic
            from experiments.semantic_reconstruct import attempt_reconstruct
            
            embed_cache_path = "AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json"
            cache_dir = str(cache.base_dir)
            
            metadata = {
                'id': fragment_id,
                'placeholder_prompt': original_content[:200] + "..."
            }
            
            reconstructed_content, similarity_score = attempt_reconstruct(
                cache.embedder,
                metadata,
                embed_cache_path,
                cache_dir
            )
            
            reconstruction_time = time.time() - start_time
            
            # Create confidence result
            confidence_result = confidence_api.create_reconstruction_result(
                fragment_id=fragment_id,
                original_content=original_content,
                reconstructed_content=reconstructed_content,
                similarity_score=similarity_score,
                reconstruction_time=reconstruction_time,
                method_used='semantic'
            )
            
            return confidence_result
            
        except Exception as e:
            return None
    
    return reconstruct_with_confidence
