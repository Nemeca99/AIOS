#!/usr/bin/env python3
"""
Enhanced Recovery Test with Semantic Reconstruction
Test improved reconstruction quality and health scoring
"""

import os
import json
import shutil
import time
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Import CARMA systems
import sys
sys.path.append("HiveMind")
from beacon_self_repair_system import BeaconSelfRepairSystem
from fractal_mycelium_cache import FractalMyceliumCache
from semantic_reconstruction_module import SemanticReconstructionModule

def enhanced_recovery_test():
    """Test enhanced recovery with semantic reconstruction"""
    
    print("🧪 ENHANCED RECOVERY TEST WITH SEMANTIC RECONSTRUCTION")
    print("=" * 60)
    
    # Step 1: Create realistic cache with meaningful content
    print("\n📁 Step 1: Creating realistic cache with semantic content...")
    cache = create_semantic_cache()
    
    # Step 2: Delete random fragments
    print("\n💥 Step 2: Deleting random fragments...")
    deleted_files = delete_random_fragments(cache, num_to_delete=5)
    
    # Step 3: Run system with enhanced reconstruction
    print("\n🔄 Step 3: Running system with enhanced reconstruction...")
    query_results = run_queries_with_enhanced_reconstruction(cache)
    
    # Step 4: Trigger enhanced sleep cycle recovery
    print("\n🌙 Step 4: Triggering enhanced sleep cycle recovery...")
    recovery_results = trigger_enhanced_sleep_cycle_recovery(cache)
    
    # Step 5: Verify enhanced reconstruction quality
    print("\n🔍 Step 5: Verifying enhanced reconstruction quality...")
    quality_metrics = verify_enhanced_reconstruction_quality(cache, deleted_files)
    
    # Step 6: Test progressive healing cycles
    print("\n🔄 Step 6: Testing progressive healing cycles...")
    progressive_results = test_progressive_healing_cycles(cache)
    
    # Step 7: Generate comprehensive report
    print("\n📊 Step 7: Generating comprehensive report...")
    generate_enhanced_report(query_results, recovery_results, quality_metrics, progressive_results)
    
    return {
        'query_results': query_results,
        'recovery_results': recovery_results,
        'quality_metrics': quality_metrics,
        'progressive_results': progressive_results
    }

def create_semantic_cache() -> FractalMyceliumCache:
    """Create a cache with semantically rich content"""
    cache = FractalMyceliumCache()
    
    # Add semantically rich content
    semantic_content = [
        "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data without being explicitly programmed.",
        "Neural networks are computing systems inspired by biological neural networks that constitute animal brains and can learn to perform tasks by considering examples.",
        "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data.",
        "Natural language processing is a field of artificial intelligence that focuses on the interaction between computers and human language, enabling machines to understand and generate text.",
        "Computer vision is a field of artificial intelligence that trains computers to interpret and understand visual information from the world, including images and videos.",
        "Reinforcement learning is a type of machine learning where agents learn to make decisions through trial and error by interacting with an environment.",
        "Supervised learning is a type of machine learning where models are trained on labeled data to make predictions or classifications on new, unseen data.",
        "Unsupervised learning is a type of machine learning where models find patterns and relationships in unlabeled data without explicit guidance.",
        "Transfer learning is a machine learning technique where a model trained on one task is adapted for use on a related task, often improving performance.",
        "Ensemble learning is a machine learning technique that combines multiple models to make better predictions than any individual model could achieve."
    ]
    
    for content in semantic_content:
        cache.add_content(content)
    
    print(f"   ✅ Created semantic cache with {len(cache.file_registry)} fragments")
    return cache

def delete_random_fragments(cache: FractalMyceliumCache, num_to_delete: int) -> List[str]:
    """Delete random fragments from cache"""
    files = list(cache.file_registry.keys())
    files_to_delete = random.sample(files, min(num_to_delete, len(files)))
    
    deleted_files = []
    for file_id in files_to_delete:
        file_path = cache.base_dir / f"{file_id}.json"
        if file_path.exists():
            file_path.unlink()
            deleted_files.append(file_id)
            print(f"      🗑️  Deleted: {file_id}")
    
    print(f"   ✅ Deleted {len(deleted_files)} fragments")
    return deleted_files

def run_queries_with_enhanced_reconstruction(cache: FractalMyceliumCache) -> Dict:
    """Run queries with enhanced reconstruction capabilities"""
    beacon = BeaconSelfRepairSystem()
    semantic_module = SemanticReconstructionModule(cache)
    
    # Ping network to discover topology
    network_map = beacon.ping_network()
    
    # Test queries
    test_queries = [
        "What is machine learning?",
        "Explain neural networks",
        "How does deep learning work?",
        "What is natural language processing?",
        "Describe computer vision",
        "What is reinforcement learning?",
        "Explain supervised learning",
        "What is unsupervised learning?"
    ]
    
    query_results = {
        'total_queries': len(test_queries),
        'successful_queries': 0,
        'failed_queries': 0,
        'placeholder_created': 0,
        'response_times': [],
        'similarity_scores': [],
        'details': []
    }
    
    for i, query in enumerate(test_queries):
        start_time = time.time()
        
        try:
            # Simulate query execution with enhanced reconstruction
            embedding = cache.embedder.embed(query)
            results = cache.find_relevant(embedding, topk=3)
            
            response_time = time.time() - start_time
            query_results['response_times'].append(response_time)
            
            # Calculate similarity score for results
            similarity_score = calculate_query_similarity(query, results)
            query_results['similarity_scores'].append(similarity_score)
            
            if results and similarity_score > 0.3:  # Higher threshold for success
                query_results['successful_queries'] += 1
                status = f"✅ Success (similarity: {similarity_score:.2f})"
            else:
                query_results['failed_queries'] += 1
                status = f"❌ Failed (similarity: {similarity_score:.2f})"
            
            query_results['details'].append({
                'query': query,
                'status': status,
                'response_time': response_time,
                'similarity_score': similarity_score,
                'results_count': len(results)
            })
            
            print(f"      Query {i+1}: {status} ({response_time:.2f}s)")
            
        except Exception as e:
            query_results['failed_queries'] += 1
            query_results['similarity_scores'].append(0.0)
            query_results['details'].append({
                'query': query,
                'status': f"❌ Error: {e}",
                'response_time': 0,
                'similarity_score': 0.0,
                'results_count': 0
            })
            print(f"      Query {i+1}: ❌ Error: {e}")
    
    # Count placeholder creation
    query_results['placeholder_created'] = len(beacon.blank_files)
    
    print(f"   ✅ Enhanced Query Results: {query_results['successful_queries']}/{query_results['total_queries']} successful")
    print(f"   📊 Average similarity: {sum(query_results['similarity_scores'])/len(query_results['similarity_scores']):.2f}")
    print(f"   📝 Placeholders created: {query_results['placeholder_created']}")
    
    return query_results

def calculate_query_similarity(query: str, results: List[Dict]) -> float:
    """Calculate similarity between query and results"""
    if not results:
        return 0.0
    
    # Simple similarity based on common words
    query_words = set(query.lower().split())
    total_similarity = 0.0
    
    for result in results:
        content = result.get('content', '')
        content_words = set(content.lower().split())
        
        if query_words and content_words:
            intersection = query_words.intersection(content_words)
            union = query_words.union(content_words)
            similarity = len(intersection) / len(union) if union else 0.0
            total_similarity += similarity
    
    return total_similarity / len(results) if results else 0.0

def trigger_enhanced_sleep_cycle_recovery(cache: FractalMyceliumCache) -> Dict:
    """Trigger enhanced sleep cycle recovery with semantic reconstruction"""
    beacon = BeaconSelfRepairSystem()
    semantic_module = SemanticReconstructionModule(cache)
    
    # Ping network to discover current state
    network_map = beacon.ping_network()
    
    # Find blank files
    blank_files = beacon._find_blank_files()
    
    if not blank_files:
        print("   🌙 No blank files to recover")
        return {'recovered': 0, 'failed': 0, 'duration': 0, 'avg_similarity': 0.0}
    
    print(f"   🌙 Enhanced Deep Dream Recovery: Rebuilding {len(blank_files)} blank files")
    
    start_time = time.time()
    recovered = 0
    failed = 0
    similarity_scores = []
    
    # Sort by priority
    blank_files.sort(key=lambda x: x['recovery_priority'], reverse=True)
    
    for blank_file in blank_files:
        try:
            # Use semantic reconstruction
            reconstructed_content, similarity = semantic_module.reconstruct_fragment(blank_file)
            
            # Update file
            blank_file['content'] = reconstructed_content
            blank_file['status'] = 'reconstructed'
            blank_file['reconstructed'] = datetime.now().isoformat()
            blank_file['similarity_score'] = similarity
            
            # Save updated file
            file_path = cache.base_dir / f"{blank_file['id']}.json"
            with open(file_path, 'w') as f:
                json.dump(blank_file, f, indent=2)
            
            # Remove from blank files
            if blank_file['id'] in beacon.blank_files:
                del beacon.blank_files[blank_file['id']]
            
            recovered += 1
            similarity_scores.append(similarity)
            print(f"      ✅ Reconstructed: {blank_file['id']} (similarity: {similarity:.2f})")
            
        except Exception as e:
            failed += 1
            print(f"      ❌ Failed to reconstruct {blank_file['id']}: {e}")
    
    duration = time.time() - start_time
    avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
    
    # Update health scoring
    health_update = semantic_module.update_health_scoring([f['id'] for f in blank_files if f.get('status') == 'reconstructed'])
    
    result = {
        'recovered': recovered,
        'failed': failed,
        'duration': duration,
        'avg_similarity': avg_similarity,
        'similarity_scores': similarity_scores,
        'health_update': health_update
    }
    
    print(f"   🌙 Enhanced Recovery Complete: {recovered} recovered, {failed} failed in {duration:.2f}s")
    print(f"   📊 Average similarity: {avg_similarity:.2f}")
    
    return result

def verify_enhanced_reconstruction_quality(cache: FractalMyceliumCache, deleted_files: List[str]) -> Dict:
    """Verify quality of enhanced reconstructed fragments"""
    beacon = BeaconSelfRepairSystem()
    
    # Check which files were reconstructed
    reconstructed_files = []
    similarity_scores = []
    
    for file_id in deleted_files:
        file_path = cache.base_dir / f"{file_id}.json"
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                if data.get('status') == 'reconstructed':
                    reconstructed_files.append(file_id)
                    similarity_scores.append(data.get('similarity_score', 0.0))
            except:
                pass
    
    # Calculate quality metrics
    total_deleted = len(deleted_files)
    total_reconstructed = len(reconstructed_files)
    reconstruction_rate = (total_reconstructed / total_deleted) * 100 if total_deleted > 0 else 0
    avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
    
    quality_metrics = {
        'total_deleted': total_deleted,
        'total_reconstructed': total_reconstructed,
        'reconstruction_rate': reconstruction_rate,
        'avg_similarity': avg_similarity,
        'similarity_scores': similarity_scores,
        'high_quality_reconstructions': len([s for s in similarity_scores if s > 0.5])
    }
    
    print(f"   ✅ Enhanced reconstruction rate: {reconstruction_rate:.1f}%")
    print(f"   📊 Average similarity: {avg_similarity:.2f}")
    print(f"   🏆 High-quality reconstructions: {quality_metrics['high_quality_reconstructions']}")
    
    return quality_metrics

def test_progressive_healing_cycles(cache: FractalMyceliumCache) -> Dict:
    """Test progressive healing over multiple cycles"""
    print("   🔄 Testing progressive healing cycles...")
    
    cycles = 3
    cycle_results = []
    
    for cycle in range(cycles):
        print(f"      Cycle {cycle + 1}/{cycles}")
        
        # Delete some fragments
        deleted = delete_random_fragments(cache, num_to_delete=2)
        
        # Run recovery
        beacon = BeaconSelfRepairSystem()
        semantic_module = SemanticReconstructionModule(cache)
        
        network_map = beacon.ping_network()
        blank_files = beacon._find_blank_files()
        
        if blank_files:
            recovery_result = trigger_enhanced_sleep_cycle_recovery(cache)
            cycle_results.append({
                'cycle': cycle + 1,
                'deleted': len(deleted),
                'recovered': recovery_result['recovered'],
                'avg_similarity': recovery_result['avg_similarity']
            })
        else:
            cycle_results.append({
                'cycle': cycle + 1,
                'deleted': len(deleted),
                'recovered': 0,
                'avg_similarity': 0.0
            })
    
    # Calculate progressive metrics
    total_recovered = sum(r['recovered'] for r in cycle_results)
    avg_similarity_over_cycles = sum(r['avg_similarity'] for r in cycle_results) / len(cycle_results)
    
    progressive_results = {
        'cycles': cycles,
        'cycle_results': cycle_results,
        'total_recovered': total_recovered,
        'avg_similarity_over_cycles': avg_similarity_over_cycles,
        'progressive_improvement': cycle_results[-1]['avg_similarity'] > cycle_results[0]['avg_similarity'] if len(cycle_results) > 1 else False
    }
    
    print(f"   ✅ Progressive healing: {total_recovered} total recovered over {cycles} cycles")
    print(f"   📊 Average similarity over cycles: {avg_similarity_over_cycles:.2f}")
    
    return progressive_results

def generate_enhanced_report(query_results: Dict, recovery_results: Dict, quality_metrics: Dict, progressive_results: Dict):
    """Generate comprehensive enhanced test report"""
    
    print("\n" + "=" * 60)
    print("📊 ENHANCED RECOVERY TEST REPORT")
    print("=" * 60)
    
    # Query Performance
    print(f"\n🔍 Enhanced Query Performance:")
    print(f"   Total queries: {query_results['total_queries']}")
    print(f"   Successful: {query_results['successful_queries']}")
    print(f"   Failed: {query_results['failed_queries']}")
    print(f"   Success rate: {(query_results['successful_queries']/query_results['total_queries'])*100:.1f}%")
    print(f"   Avg response time: {sum(query_results['response_times'])/len(query_results['response_times']):.2f}s")
    print(f"   Avg similarity: {sum(query_results['similarity_scores'])/len(query_results['similarity_scores']):.2f}")
    
    # Recovery Performance
    print(f"\n🌙 Enhanced Recovery Performance:")
    print(f"   Recovery time: {recovery_results['duration']:.2f}s")
    print(f"   Files recovered: {recovery_results['recovered']}")
    print(f"   Files failed: {recovery_results['failed']}")
    print(f"   Avg similarity: {recovery_results['avg_similarity']:.2f}")
    
    # Quality Metrics
    print(f"\n🔍 Enhanced Reconstruction Quality:")
    print(f"   Total deleted: {quality_metrics['total_deleted']}")
    print(f"   Total reconstructed: {quality_metrics['total_reconstructed']}")
    print(f"   Reconstruction rate: {quality_metrics['reconstruction_rate']:.1f}%")
    print(f"   Average similarity: {quality_metrics['avg_similarity']:.2f}")
    print(f"   High-quality reconstructions: {quality_metrics['high_quality_reconstructions']}")
    
    # Progressive Healing
    print(f"\n🔄 Progressive Healing Results:")
    print(f"   Cycles tested: {progressive_results['cycles']}")
    print(f"   Total recovered: {progressive_results['total_recovered']}")
    print(f"   Avg similarity over cycles: {progressive_results['avg_similarity_over_cycles']:.2f}")
    print(f"   Progressive improvement: {'✅' if progressive_results['progressive_improvement'] else '❌'}")
    
    # Overall Assessment
    print(f"\n🎯 Enhanced Overall Assessment:")
    success_rate = (query_results['successful_queries']/query_results['total_queries'])*100
    avg_similarity = quality_metrics['avg_similarity']
    
    if success_rate >= 80 and avg_similarity >= 0.5:
        print("   ✅ SYSTEM EXCELLENT: Enhanced self-healing capabilities demonstrated")
        print("   🚀 Ready for enterprise deployment with semantic reconstruction")
    elif success_rate >= 60 and avg_similarity >= 0.3:
        print("   ⚠️  SYSTEM GOOD: Some enhanced self-healing capabilities demonstrated")
        print("   🔧 Needs minor improvements before enterprise deployment")
    else:
        print("   ❌ SYSTEM NEEDS WORK: Enhanced self-healing capabilities insufficient")
        print("   🛠️  Requires significant improvement")
    
    # Save detailed results
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'query_results': query_results,
        'recovery_results': recovery_results,
        'quality_metrics': quality_metrics,
        'progressive_results': progressive_results,
        'overall_assessment': {
            'success_rate': success_rate,
            'avg_similarity': avg_similarity,
            'enterprise_ready': success_rate >= 80 and avg_similarity >= 0.5
        }
    }
    
    report_file = Path("experiments/enhanced_recovery_test_results.json")
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    print(f"\n📁 Enhanced results saved to: {report_file}")

if __name__ == "__main__":
    results = enhanced_recovery_test()
