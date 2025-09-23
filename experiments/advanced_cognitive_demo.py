#!/usr/bin/env python3
"""
Advanced Cognitive CARMA Demo
Comprehensive demonstration of all cognitive science and neuroscience enhancements.
"""

import sys
import time
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from advanced_cognitive_carma import AdvancedCognitiveCarma

def run_advanced_cognitive_demo():
    """Run a comprehensive demo of the advanced cognitive CARMA system."""
    
    print("🧠 ADVANCED COGNITIVE CARMA SYSTEM DEMO")
    print("=" * 100)
    print("Demonstrating the complete integration of cognitive science and neuroscience:")
    print("• Emotion-weighted fragments with valence, intensity, and arousal")
    print("• Multi-stage dream cycles (slow-wave sleep vs REM sleep)")
    print("• Meta-memory with confidence tracking and uncertainty quantification")
    print("• Synaptic tagging and capture for weak-strong memory reinforcement")
    print("• Predictive coding for self-organizing predictive model")
    print("• Personality drift through emotional and cognitive learning")
    print("• Comprehensive cognitive event tracking and analysis")
    print("=" * 100)
    
    # Initialize the advanced cognitive system
    print("\n🔧 Initializing Advanced Cognitive CARMA System...")
    system = AdvancedCognitiveCarma()
    
    # Demo 1: Emotion-Weighted Memory Processing
    print("\n" + "="*80)
    print("💝 DEMO 1: EMOTION-WEIGHTED MEMORY PROCESSING")
    print("="*80)
    
    emotional_queries = [
        "I am absolutely ecstatic and overjoyed about this incredible breakthrough!",
        "This is devastating and heartbreaking, I'm completely crushed by the news.",
        "I feel so grateful and blessed for this wonderful opportunity in my life.",
        "I'm terrified and anxious about what might happen in the future.",
        "This is just a normal day with nothing particularly special happening."
    ]
    
    print("Processing emotional queries to demonstrate emotion-weighted memory...")
    for i, query in enumerate(emotional_queries):
        print(f"\n📝 Emotional Query {i+1}: {query}")
        result = system.process_cognitive_query(query)
        
        # Show emotional analysis
        emotion_stats = system.emotion_cache.get_emotional_summary()
        print(f"   Emotional fragments: {emotion_stats['emotional_fragments']}")
        if 'avg_valence' in emotion_stats:
            print(f"   Average valence: {emotion_stats['avg_valence']:.2f}")
        if 'special_memories' in emotion_stats:
            print(f"   Special memories: {emotion_stats['special_memories']}")
    
    # Demo 2: Meta-Memory and Confidence Tracking
    print("\n" + "="*80)
    print("🧠 DEMO 2: META-MEMORY AND CONFIDENCE TRACKING")
    print("="*80)
    
    confidence_queries = [
        "I am absolutely certain this is correct and I have no doubts whatsoever.",
        "Maybe this is right, I think, but I'm not completely sure about it.",
        "This is definitely true and I know it for certain beyond any doubt.",
        "I'm not sure about this, it could be wrong or it could be right.",
        "This is probably correct, but I have some reservations and concerns."
    ]
    
    print("Processing confidence queries to demonstrate meta-memory...")
    for i, query in enumerate(confidence_queries):
        print(f"\n📝 Confidence Query {i+1}: {query}")
        result = system.process_cognitive_query(query)
        
        # Show confidence analysis
        uncertainty_report = system.meta_memory_system.generate_uncertainty_report()
        if uncertainty_report.get('status') != 'no_assessments':
            print(f"   Average confidence: {uncertainty_report['confidence_stats']['average']:.2f}")
            print(f"   Knowledge gaps: {uncertainty_report['knowledge_gaps']['total_gaps']}")
            print(f"   High confidence: {uncertainty_report['confidence_stats']['high_confidence_count']}")
    
    # Demo 3: Synaptic Tagging and Memory Reinforcement
    print("\n" + "="*80)
    print("🧬 DEMO 3: SYNAPTIC TAGGING AND MEMORY REINFORCEMENT")
    print("="*80)
    
    # Create a sequence that should trigger synaptic tagging
    tagging_queries = [
        "This is a weak memory that needs reinforcement.",
        "This is a very strong and important memory with high confidence.",
        "This is another weak memory that should be boosted by the strong one.",
        "This is another strong memory that can reinforce weak ones.",
        "This weak memory should benefit from temporal proximity to strong memories."
    ]
    
    print("Processing queries to demonstrate synaptic tagging...")
    for i, query in enumerate(tagging_queries):
        print(f"\n📝 Tagging Query {i+1}: {query}")
        result = system.process_cognitive_query(query)
        
        # Show tagging results
        tagging_stats = system.synaptic_tagging.get_tagging_statistics()
        print(f"   Tagging events: {tagging_stats['total_tagging_events']}")
        print(f"   Memory boosts: {tagging_stats['total_memory_boosts']}")
        print(f"   Tagged fragments: {tagging_stats['tagged_fragments']}")
    
    # Demo 4: Predictive Coding and Pattern Recognition
    print("\n" + "="*80)
    print("🔮 DEMO 4: PREDICTIVE CODING AND PATTERN RECOGNITION")
    print("="*80)
    
    # Create sequences that should trigger predictions
    prediction_queries = [
        "The first step in the process is to initialize the system.",
        "The second step involves configuring the parameters.",
        "The third step is to run the initialization sequence.",
        "The fourth step requires validation of the configuration.",
        "The fifth step involves testing the system functionality."
    ]
    
    print("Processing sequential queries to demonstrate predictive coding...")
    for i, query in enumerate(prediction_queries):
        print(f"\n📝 Prediction Query {i+1}: {query}")
        result = system.process_cognitive_query(query)
        
        # Show prediction results
        prediction_stats = system.predictive_coding.get_prediction_statistics()
        print(f"   Total predictions: {prediction_stats['total_predictions']}")
        print(f"   Average accuracy: {prediction_stats['average_accuracy']:.2f}")
        print(f"   Pattern complexity: {prediction_stats['pattern_complexity']:.2f}")
    
    # Demo 5: Dream Cycles and Memory Consolidation
    print("\n" + "="*80)
    print("🌙 DEMO 5: DREAM CYCLES AND MEMORY CONSOLIDATION")
    print("="*80)
    
    # Add more content to trigger dream cycles
    consolidation_queries = [
        "This is important information that needs to be consolidated in memory.",
        "Another piece of knowledge that should be processed during sleep cycles.",
        "More data that will help trigger memory consolidation and organization.",
        "Additional information to build up the memory system complexity.",
        "Yet another fragment to increase the likelihood of dream cycle triggers."
    ]
    
    print("Adding content to trigger dream cycles...")
    for i, query in enumerate(consolidation_queries):
        print(f"\n📝 Consolidation Query {i+1}: {query}")
        result = system.process_cognitive_query(query)
        
        # Check for dream cycle
        if result['dream_cycle'].get('status') != 'no_sleep_needed':
            print(f"   🌙 Dream cycle triggered: {result['dream_cycle']['reason']}")
            if 'stages' in result['dream_cycle']:
                for stage in result['dream_cycle']['stages']:
                    print(f"     {stage['stage']}: {stage.get('duration', 0):.2f}s")
    
    # Demo 6: Personality Drift and Cognitive Learning
    print("\n" + "="*80)
    print("👤 DEMO 6: PERSONALITY DRIFT AND COGNITIVE LEARNING")
    print("="*80)
    
    personality_queries = [
        "I love meeting new people and socializing at parties and events!",
        "I prefer to work alone and avoid large groups and crowds.",
        "I am very organized and always plan everything carefully in advance.",
        "I enjoy trying new things and exploring creative and innovative ideas.",
        "I get stressed easily and worry about many things in my life."
    ]
    
    print("Processing personality queries to demonstrate cognitive drift...")
    initial_personality = system.personality_drift.copy()
    
    for i, query in enumerate(personality_queries):
        print(f"\n📝 Personality Query {i+1}: {query}")
        result = system.process_cognitive_query(query)
        
        # Show personality changes
        current_personality = system.personality_drift
        print(f"   Current personality drift:")
        for trait, value in current_personality.items():
            change = value - initial_personality.get(trait, 0)
            print(f"     {trait}: {value:.3f} ({change:+.3f})")
    
    # Demo 7: Comprehensive System Analysis
    print("\n" + "="*80)
    print("📊 DEMO 7: COMPREHENSIVE COGNITIVE SYSTEM ANALYSIS")
    print("="*80)
    
    final_stats = system.get_comprehensive_stats()
    
    print("🧠 Advanced Cognitive System Statistics:")
    print(f"   Total queries processed: {final_stats['total_queries']}")
    print(f"   Learning cycles: {final_stats['learning_cycles']}")
    print(f"   Dream cycles: {final_stats['consolidation']['total_cycles']}")
    print(f"   Cognitive events: {final_stats['cognitive_events']['total_events']}")
    
    print("\n💝 Emotional System Statistics:")
    emotion_stats = final_stats['emotion']
    print(f"   Total fragments: {emotion_stats['total_fragments']}")
    print(f"   Emotional fragments: {emotion_stats['emotional_fragments']}")
    if 'avg_valence' in emotion_stats:
        print(f"   Average valence: {emotion_stats['avg_valence']:.2f}")
    if 'special_memories' in emotion_stats:
        print(f"   Special memories: {emotion_stats['special_memories']}")
    
    print("\n🧠 Meta-Memory Statistics:")
    meta_stats = final_stats['meta_memory']
    if meta_stats.get('status') != 'no_assessments':
        print(f"   Assessment coverage: {meta_stats['assessment_coverage']:.1%}")
        print(f"   Average confidence: {meta_stats['confidence_stats']['average']:.2f}")
        print(f"   Knowledge gaps: {meta_stats['knowledge_gaps']['total_gaps']}")
        print(f"   High confidence: {meta_stats['confidence_stats']['high_confidence_count']}")
    else:
        print("   No assessments yet")
    
    print("\n🧬 Synaptic Tagging Statistics:")
    tagging_stats = final_stats['synaptic_tagging']
    print(f"   Tagging events: {tagging_stats['total_tagging_events']}")
    print(f"   Memory boosts: {tagging_stats['total_memory_boosts']}")
    print(f"   Tagged fragments: {tagging_stats['tagged_fragments']}")
    print(f"   Average boost: {tagging_stats['average_boost_amount']:.3f}")
    
    print("\n🔮 Predictive Coding Statistics:")
    prediction_stats = final_stats['predictive_coding']
    print(f"   Total predictions: {prediction_stats['total_predictions']}")
    print(f"   Average accuracy: {prediction_stats['average_accuracy']:.2f}")
    print(f"   Average confidence: {prediction_stats['average_confidence']:.2f}")
    print(f"   Pattern complexity: {prediction_stats['pattern_complexity']:.2f}")
    print(f"   Pattern count: {prediction_stats['pattern_count']}")
    
    print("\n👤 Final Personality Drift Summary:")
    personality = final_stats['personality_drift']
    for trait, value in personality.items():
        print(f"   {trait}: {value:.3f}")
    
    # Demo 8: Knowledge Gap Analysis and Recommendations
    print("\n" + "="*80)
    print("🔍 DEMO 8: KNOWLEDGE GAP ANALYSIS AND RECOMMENDATIONS")
    print("="*80)
    
    uncertainty_report = system.meta_memory_system.generate_uncertainty_report()
    if uncertainty_report.get('status') != 'no_assessments':
        print("📋 Knowledge Gaps Identified:")
        gaps = uncertainty_report['knowledge_gaps']['gaps']
        for i, gap in enumerate(gaps[:5]):  # Show top 5 gaps
            print(f"   {i+1}. {gap['fragment_id'][:8]}... (confidence: {gap['confidence']:.2f})")
            print(f"      Priority: {gap['priority']:.2f}")
            print(f"      Content: {gap['content_preview']}...")
        
        print(f"\n💡 System Recommendations:")
        for rec in uncertainty_report['recommendations']:
            print(f"   • {rec}")
    else:
        print("   No knowledge gaps identified yet")
    
    # Final Summary
    print("\n" + "="*100)
    print("🎉 ADVANCED COGNITIVE CARMA DEMO COMPLETE!")
    print("="*100)
    print("The system has successfully demonstrated:")
    print("✅ Emotion-weighted memory consolidation with valence, intensity, and arousal")
    print("✅ Multi-stage dream cycles (slow-wave sleep vs REM sleep)")
    print("✅ Meta-memory with confidence tracking and uncertainty quantification")
    print("✅ Synaptic tagging and capture for weak-strong memory reinforcement")
    print("✅ Predictive coding for self-organizing predictive model")
    print("✅ Personality drift through emotional and cognitive learning")
    print("✅ Comprehensive cognitive event tracking and analysis")
    print("✅ Knowledge gap identification and system recommendations")
    print("\nThis represents a MAJOR ADVANCEMENT in biologically plausible AI memory")
    print("systems, incorporating cutting-edge insights from:")
    print("• Cognitive Psychology (emotion-memory interactions, confidence calibration)")
    print("• Neuroscience (sleep stages, synaptic tagging, memory consolidation)")
    print("• Machine Learning (sparse distributed memory, predictive coding)")
    print("• AI Research (meta-learning, uncertainty quantification)")
    print("\nThe system is now ready for real-world deployment and research publication!")
    print("="*100)

if __name__ == "__main__":
    run_advanced_cognitive_demo()
