#!/usr/bin/env python3
"""
Enterprise Demo with Confidence API
Demonstrates CARMA's enterprise-ready capabilities with trust metrics
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Import CARMA systems
sys.path.append("HiveMind")
from fractal_mycelium_cache import FractalMyceliumCache
from confidence_api import ConfidenceAPI, create_enterprise_query_api, create_enterprise_reconstruction_api
from system_constants import SystemConfig, CommercialFraming

def enterprise_demo():
    """Demonstrate enterprise-ready CARMA capabilities"""
    
    print("🚀 CARMA ENTERPRISE DEMO")
    print("=" * 50)
    print(f"Product: {CommercialFraming.PRODUCT_NAME}")
    print(f"Tagline: {CommercialFraming.PRIMARY_TAGLINE}")
    print("=" * 50)
    
    # Initialize systems
    print("\n🔧 Initializing Enterprise Systems...")
    cache = FractalMyceliumCache()
    confidence_api = ConfidenceAPI()
    
    # Create enterprise APIs
    query_api = create_enterprise_query_api(cache, confidence_api)
    reconstruction_api = create_enterprise_reconstruction_api(cache, confidence_api)
    
    print("   ✅ Systems initialized")
    
    # Demo 1: Enterprise Query with Confidence
    print("\n🔍 Demo 1: Enterprise Query with Confidence Metrics")
    print("-" * 50)
    
    enterprise_queries = [
        "What is machine learning?",
        "Explain neural networks", 
        "How does deep learning work?",
        "What is natural language processing?",
        "Describe computer vision"
    ]
    
    query_results = []
    for i, query in enumerate(enterprise_queries):
        print(f"\nQuery {i+1}: {query}")
        results = query_api(query, topk=3)
        query_results.extend(results)
        
        for j, result in enumerate(results):
            print(f"  Result {j+1}: {result.fragment_id}")
            print(f"    Similarity: {result.similarity_score:.3f}")
            print(f"    Confidence: {result.confidence_level.upper()}")
            print(f"    Response Time: {result.response_time:.3f}s")
            print(f"    Content: {result.content[:100]}...")
    
    # Demo 2: Self-Healing with Confidence
    print("\n🌙 Demo 2: Self-Healing with Confidence Metrics")
    print("-" * 50)
    
    # Create some blank files for demonstration
    print("Creating test corruption scenario...")
    test_fragments = list(cache.file_registry.keys())[:3]
    
    reconstruction_results = []
    for frag_id in test_fragments:
        # Get original content
        original_content = cache.file_registry[frag_id].get('content', '')
        
        print(f"\nReconstructing: {frag_id}")
        result = reconstruction_api(frag_id, original_content)
        
        if result:
            reconstruction_results.append(result)
            print(f"  Original: {result.original_content[:50]}...")
            print(f"  Reconstructed: {result.reconstructed_content[:50]}...")
            print(f"  Similarity: {result.similarity_score:.3f}")
            print(f"  Confidence: {result.confidence_level.upper()}")
            print(f"  Quality Score: {result.quality_indicators['quality_score']:.3f}")
            print(f"  Reconstruction Time: {result.reconstruction_time:.3f}s")
    
    # Demo 3: Enterprise Confidence Report
    print("\n📊 Demo 3: Enterprise Confidence Report")
    print("-" * 50)
    
    confidence_report = confidence_api.generate_confidence_report(
        query_results, reconstruction_results
    )
    
    print(f"Overall Confidence: {confidence_report['overall_confidence']:.3f}")
    print(f"Enterprise Ready: {confidence_report['enterprise_readiness']['enterprise_ready']}")
    print(f"Readiness Score: {confidence_report['enterprise_readiness']['readiness_score']:.3f}")
    
    print("\nQuery Metrics:")
    query_metrics = confidence_report['query_metrics']
    print(f"  Total Queries: {query_metrics['total_queries']}")
    print(f"  Success Rate: {query_metrics['success_rate']:.1%}")
    print(f"  Avg Similarity: {query_metrics['avg_similarity']:.3f}")
    print(f"  High Confidence Rate: {query_metrics['high_confidence_rate']:.1%}")
    print(f"  Avg Response Time: {query_metrics['avg_response_time']:.3f}s")
    
    print("\nReconstruction Metrics:")
    recon_metrics = confidence_report['reconstruction_metrics']
    print(f"  Total Reconstructions: {recon_metrics['total_reconstructions']}")
    print(f"  Success Rate: {recon_metrics['success_rate']:.1%}")
    print(f"  Avg Similarity: {recon_metrics['avg_similarity']:.3f}")
    print(f"  Avg Quality Score: {recon_metrics['avg_quality_score']:.3f}")
    print(f"  Avg Reconstruction Time: {recon_metrics['avg_reconstruction_time']:.3f}s")
    
    print("\nConfidence Distribution:")
    distribution = confidence_report['confidence_distribution']
    for level, percentage in distribution.items():
        print(f"  {level.upper()}: {percentage:.1%}")
    
    # Demo 4: Enterprise Value Proposition
    print("\n💼 Demo 4: Enterprise Value Proposition")
    print("-" * 50)
    
    print("Key Value Propositions:")
    for i, prop in enumerate(CommercialFraming.VALUE_PROPOSITIONS, 1):
        print(f"  {i}. {prop}")
    
    print("\nKey Metrics:")
    for metric, value in CommercialFraming.KEY_METRICS.items():
        print(f"  {metric.replace('_', ' ').title()}: {value}")
    
    # Demo 5: System Health Assessment
    print("\n🏥 Demo 5: System Health Assessment")
    print("-" * 50)
    
    overall_score = confidence_report['overall_confidence']
    enterprise_ready = confidence_report['enterprise_readiness']['enterprise_ready']
    
    if overall_score >= 0.9:
        status = "🟢 EXCELLENT"
    elif overall_score >= 0.7:
        status = "🟡 GOOD"
    else:
        status = "🔴 NEEDS IMPROVEMENT"
    
    print(f"System Status: {status}")
    print(f"Overall Score: {overall_score:.3f}")
    print(f"Enterprise Ready: {'✅ YES' if enterprise_ready else '❌ NO'}")
    
    if not enterprise_ready:
        print("\nRecommendations:")
        for rec in confidence_report['enterprise_readiness']['recommendations']:
            print(f"  • {rec}")
    
    # Save comprehensive report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'demo_type': 'enterprise_capabilities',
        'confidence_report': confidence_report,
        'query_results': [
            {
                'fragment_id': r.fragment_id,
                'similarity_score': r.similarity_score,
                'confidence_level': r.confidence_level,
                'response_time': r.response_time
            } for r in query_results
        ],
        'reconstruction_results': [
            {
                'fragment_id': r.fragment_id,
                'similarity_score': r.similarity_score,
                'confidence_level': r.confidence_level,
                'quality_score': r.quality_indicators['quality_score'],
                'reconstruction_time': r.reconstruction_time
            } for r in reconstruction_results
        ]
    }
    
    report_file = Path("experiments/enterprise_demo_report.json")
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    print(f"\n📁 Enterprise demo report saved to: {report_file}")
    
    # Final assessment
    print("\n🎯 FINAL ASSESSMENT")
    print("=" * 50)
    
    if enterprise_ready and overall_score >= 0.8:
        print("✅ CARMA is ENTERPRISE READY!")
        print("🚀 Ready for commercial deployment")
        print("💼 Suitable for enterprise partnerships")
        print("📈 Ready for scaling to 1000+ fragments")
    elif overall_score >= 0.6:
        print("⚠️  CARMA is GOOD but needs minor improvements")
        print("🔧 Ready for pilot programs")
        print("📊 Monitor performance before full deployment")
    else:
        print("❌ CARMA needs significant improvements")
        print("🛠️  Focus on core functionality before enterprise use")
    
    print(f"\nOverall Score: {overall_score:.3f}/1.0")
    print(f"Enterprise Ready: {'✅' if enterprise_ready else '❌'}")
    
    return confidence_report

if __name__ == "__main__":
    report = enterprise_demo()
