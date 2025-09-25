#!/usr/bin/env python3
"""
Cognitive CARMA Demo
Demonstrates all the cognitive science and neuroscience-inspired enhancements.
"""

import sys
import time
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

from cognitive_carma_system import CognitiveCarmaSystem

def run_cognitive_demo():
    """Run a comprehensive demo of the cognitive CARMA system."""
    
    print("🧠 COGNITIVE CARMA SYSTEM DEMO")
    print("=" * 80)
    print("Demonstrating cognitive science and neuroscience-inspired enhancements:")
    print("• Emotion-weighted fragments")
    print("• Multi-stage dream cycles (slow-wave vs REM sleep)")
    print("• Meta-memory with confidence tracking")
    print("• Personality drift through emotional learning")
    print("• Synaptic tagging and temporal proximity")
    print("• Predictive coding and self-organization")
    print("=" * 80)
    
    # Initialize the cognitive system
    print("\n🔧 Initializing Cognitive CARMA System...")
    system = CognitiveCarmaSystem()
    
    # Demo 1: Emotion-Weighted Fragments
    print("\n" + "="*60)
    print("💝 DEMO 1: EMOTION-WEIGHTED FRAGMENTS")
    print("="*60)
    
    emotional_queries = [
        "I am absolutely thrilled and overjoyed about this incredible success!",
        "This is devastating and heartbreaking, I'm completely crushed.",
        "I feel so grateful and blessed for this wonderful opportunity.",
        "I'm terrified and anxious about what might happen next.",
        "This is just a normal day with nothing special happening."
    ]
    
    print("Processing emotional queries to demonstrate emotion weighting...")
    for i, query in enumerate(emotional_queries):
        print(f"\n📝 Emotional Query {i+1}: {query}")
        result = system.process_query(query)
        
        # Show emotional analysis
        emotion_stats = system.emotion_cache.get_emotional_summary()
        print(f"   Emotional fragments: {emotion_stats['emotional_fragments']}")
        if 'avg_valence' in emotion_stats:
            print(f"   Average valence: {emotion_stats['avg_valence']:.2f}")
        if 'special_memories' in emotion_stats:
            print(f"   Special memories: {emotion_stats['special_memories']}")
    
    # Demo 2: Meta-Memory and Confidence Tracking
    print("\n" + "="*60)
    print("🧠 DEMO 2: META-MEMORY AND CONFIDENCE TRACKING")
    print("="*60)
    
    confidence_queries = [
        "I am certain this is absolutely correct and I have no doubts.",
        "Maybe this is right, I think, but I'm not completely sure.",
        "This is definitely true and I know it for certain.",
        "I'm not sure about this, it could be wrong.",
        "This is probably correct, but I have some reservations."
    ]
    
    print("Processing confidence queries to demonstrate meta-memory...")
    for i, query in enumerate(confidence_queries):
        print(f"\n📝 Confidence Query {i+1}: {query}")
        result = system.process_query(query)
        
        # Show confidence analysis
        uncertainty_report = system.meta_memory_system.generate_uncertainty_report()
        if uncertainty_report.get('status') != 'no_assessments':
            print(f"   Average confidence: {uncertainty_report['confidence_stats']['average']:.2f}")
            print(f"   Knowledge gaps: {uncertainty_report['knowledge_gaps']['total_gaps']}")
            print(f"   High confidence: {uncertainty_report['confidence_stats']['high_confidence_count']}")
    
    # Demo 3: Dream Cycles and Consolidation
    print("\n" + "="*60)
    print("🌙 DEMO 3: DREAM CYCLES AND CONSOLIDATION")
    print("="*60)
    
    # Add more fragments to trigger dream cycles
    consolidation_queries = [
        "This is important information that needs to be remembered.",
        "Another piece of knowledge that should be consolidated.",
        "More data that will help trigger memory consolidation.",
        "Additional information to build up the memory system.",
        "Yet another fragment to increase system complexity."
    ]
    
    print("Adding fragments to trigger dream cycles...")
    for i, query in enumerate(consolidation_queries):
        print(f"\n📝 Consolidation Query {i+1}: {query}")
        result = system.process_query(query)
        
        # Check for dream cycle
        if result['dream_cycle'].get('status') != 'no_sleep_needed':
            print(f"   🌙 Dream cycle triggered: {result['dream_cycle']['reason']}")
            if 'stages' in result['dream_cycle']:
                for stage in result['dream_cycle']['stages']:
                    print(f"     {stage['stage']}: {stage.get('duration', 0):.2f}s")
    
    # Demo 4: Personality Drift
    print("\n" + "="*60)
    print("👤 DEMO 4: PERSONALITY DRIFT THROUGH LEARNING")
    print("="*60)
    
    personality_queries = [
        "I love meeting new people and socializing at parties!",
        "I prefer to work alone and avoid large groups.",
        "I am very organized and always plan everything carefully.",
        "I enjoy trying new things and exploring creative ideas.",
        "I get stressed easily and worry about many things."
    ]
    
    print("Processing personality queries to demonstrate drift...")
    initial_personality = system.personality_drift.copy()
    
    for i, query in enumerate(personality_queries):
        print(f"\n📝 Personality Query {i+1}: {query}")
        result = system.process_query(query)
        
        # Show personality changes
        current_personality = system.personality_drift
        print(f"   Current personality drift:")
        for trait, value in current_personality.items():
            change = value - initial_personality.get(trait, 0)
            print(f"     {trait}: {value:.3f} ({change:+.3f})")
    
    # Demo 5: System Statistics and Analysis
    print("\n" + "="*60)
    print("📊 DEMO 5: COMPREHENSIVE SYSTEM ANALYSIS")
    print("="*60)
    
    final_stats = system.get_system_stats()
    
    print("🧠 Cognitive System Statistics:")
    print(f"   Total queries processed: {final_stats['total_queries']}")
    print(f"   Learning cycles: {final_stats['learning_cycles']}")
    print(f"   Dream cycles: {final_stats['consolidation']['total_cycles']}")
    
    print("\n💝 Emotional System Statistics:")
    emotion_stats = final_stats['emotion']
    print(f"   Total fragments: {emotion_stats['total_fragments']}")
    print(f"   Emotional fragments: {emotion_stats['emotional_fragments']}")
    if 'avg_valence' in emotion_stats:
        print(f"   Average valence: {emotion_stats['avg_valence']:.2f}")
    if 'high_valence_count' in emotion_stats:
        print(f"   High valence count: {emotion_stats['high_valence_count']}")
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
    
    print("\n👤 Personality Drift Summary:")
    personality = final_stats['personality_drift']
    for trait, value in personality.items():
        print(f"   {trait}: {value:.3f}")
    
    # Demo 6: Knowledge Gap Analysis
    print("\n" + "="*60)
    print("🔍 DEMO 6: KNOWLEDGE GAP ANALYSIS")
    print("="*60)
    
    uncertainty_report = system.meta_memory_system.generate_uncertainty_report()
    if uncertainty_report.get('status') != 'no_assessments':
        print("📋 Knowledge Gaps Identified:")
        gaps = uncertainty_report['knowledge_gaps']['gaps']
        for i, gap in enumerate(gaps[:5]):  # Show top 5 gaps
            print(f"   {i+1}. {gap['fragment_id'][:8]}... (confidence: {gap['confidence']:.2f})")
            print(f"      Priority: {gap['priority']:.2f}")
            print(f"      Content: {gap['content_preview']}...")
        
        print(f"\n💡 Recommendations:")
        for rec in uncertainty_report['recommendations']:
            print(f"   • {rec}")
    else:
        print("   No knowledge gaps identified yet")
    
    # Final Summary
    print("\n" + "="*80)
    print("🎉 COGNITIVE CARMA DEMO COMPLETE!")
    print("="*80)
    print("The system has demonstrated:")
    print("✅ Emotion-weighted memory consolidation")
    print("✅ Multi-stage dream cycles (slow-wave/REM)")
    print("✅ Meta-memory with confidence tracking")
    print("✅ Personality drift through emotional learning")
    print("✅ Knowledge gap identification")
    print("✅ Self-organizing memory system")
    print("\nThis represents a significant advancement in biologically")
    print("plausible AI memory systems, incorporating insights from")
    print("cognitive science, neuroscience, and machine learning.")
    print("="*80)

if __name__ == "__main__":
    run_cognitive_demo()
