#!/usr/bin/env python3
"""
Recovery Operations Module
Centralized recovery and self-healing operations
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from system_constants import RecoveryConfig, FilePaths, SystemMessages, DefaultValues
from cache_operations import CacheOperations
from embedding_operations import EmbeddingOperations, EmbeddingSimilarity

class RecoveryOperations:
    """Centralized recovery operations"""
    
    @staticmethod
    def create_blank_placeholder(file_id: str, level: int, base_dir: Path, 
                                placeholder_prompt: Optional[str] = None) -> bool:
        """Create blank placeholder file for recovery"""
        try:
            placeholder_data = {
                "id": file_id,
                "content": "",
                "level": level,
                "hits": DefaultValues.DEFAULT_HITS,
                "blank": True,
                "created_at": time.time(),
                "placeholder_prompt": placeholder_prompt or DefaultValues.DEFAULT_PLACEHOLDER_PROMPT.format(
                    file_id=file_id, level=level
                ),
                "status": "blank"
            }
            
            success = CacheOperations.save_fragment(file_id, placeholder_data, base_dir)
            if success:
                print(SystemMessages.CREATED_BLANK_PLACEHOLDER.format(file_id=file_id))
            return success
        except Exception as e:
            print(f"❌ Failed to create blank placeholder {file_id}: {e}")
            return False
    
    @staticmethod
    def find_blank_fragments(base_dir: Path) -> List[Dict[str, Any]]:
        """Find all blank fragments in cache"""
        blank_fragments = []
        
        try:
            for file_path in base_dir.glob("*.json"):
                if file_path.name == "registry.json":
                    continue
                
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    if CacheOperations.is_blank_fragment(data):
                        blank_fragments.append({
                            "id": data.get("id", file_path.stem),
                            "level": data.get("level", 0),
                            "placeholder_prompt": data.get("placeholder_prompt", ""),
                            "file_path": str(file_path)
                        })
                except Exception as e:
                    print(f"⚠️  Could not process {file_path}: {e}")
                    continue
            
            return blank_fragments
        except Exception as e:
            print(f"❌ Failed to find blank fragments: {e}")
            return []
    
    @staticmethod
    def reconstruct_fragment(file_id: str, original_content: str, embedder, 
                           cache_dir: Path, embed_cache_path: Path) -> Tuple[str, float]:
        """Reconstruct fragment content using semantic reconstruction"""
        try:
            from experiments.semantic_reconstruct import attempt_reconstruct
            
            metadata = {
                "id": file_id,
                "placeholder_prompt": original_content[:200] + "..." if len(original_content) > 200 else original_content
            }
            
            reconstructed_content, similarity_score = attempt_reconstruct(
                embedder, metadata, str(embed_cache_path), str(cache_dir)
            )
            
            return reconstructed_content or "", similarity_score or 0.0
            
        except Exception as e:
            print(f"❌ Reconstruction failed for {file_id}: {e}")
            return "", 0.0
    
    @staticmethod
    def update_fragment_content(file_id: str, new_content: str, similarity_score: float, 
                              base_dir: Path) -> bool:
        """Update fragment with reconstructed content"""
        try:
            # Load existing fragment
            fragment_data = CacheOperations.load_fragment(file_id, base_dir)
            if not fragment_data:
                return False
            
            # Update content
            fragment_data.update({
                "content": new_content,
                "blank": False,
                "similarity_score": similarity_score,
                "reconstructed_at": time.time(),
                "status": "reconstructed"
            })
            
            # Save updated fragment
            success = CacheOperations.save_fragment(file_id, fragment_data, base_dir)
            if success:
                print(SystemMessages.RECONSTRUCTION_SUCCESS.format(
                    file_id=file_id, similarity=similarity_score
                ))
            return success
            
        except Exception as e:
            print(f"❌ Failed to update fragment {file_id}: {e}")
            return False

class SemanticReconstruction:
    """Semantic reconstruction operations"""
    
    def __init__(self, cache, embedder):
        self.cache = cache
        self.embedder = embedder
        self.embed_cache_path = Path(FilePaths.EMBEDDER_CACHE)
    
    def reconstruct_blank_fragments(self, blank_fragments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Reconstruct multiple blank fragments"""
        start_time = time.time()
        results = {
            "reconstructed": 0,
            "failed": 0,
            "total_similarity": 0.0,
            "reconstruction_times": [],
            "details": []
        }
        
        print(f"🌙 Semantic Recovery: Rebuilding {len(blank_fragments)} blank files")
        
        for fragment in blank_fragments:
            file_id = fragment["id"]
            original_content = fragment.get("placeholder_prompt", "")
            
            # Reconstruct fragment
            fragment_start = time.time()
            reconstructed_content, similarity_score = RecoveryOperations.reconstruct_fragment(
                file_id, original_content, self.embedder, 
                self.cache.base_dir, self.embed_cache_path
            )
            fragment_time = time.time() - fragment_start
            
            if reconstructed_content and similarity_score > 0:
                # Update fragment
                success = RecoveryOperations.update_fragment_content(
                    file_id, reconstructed_content, similarity_score, self.cache.base_dir
                )
                
                if success:
                    results["reconstructed"] += 1
                    results["total_similarity"] += similarity_score
                    results["reconstruction_times"].append(fragment_time)
                    results["details"].append({
                        "file_id": file_id,
                        "similarity": similarity_score,
                        "reconstruction_time": fragment_time,
                        "status": "success"
                    })
                else:
                    results["failed"] += 1
                    results["details"].append({
                        "file_id": file_id,
                        "similarity": 0.0,
                        "reconstruction_time": fragment_time,
                        "status": "failed"
                    })
            else:
                results["failed"] += 1
                results["details"].append({
                    "file_id": file_id,
                    "similarity": 0.0,
                    "reconstruction_time": fragment_time,
                    "status": "failed"
                })
        
        total_time = time.time() - start_time
        avg_similarity = results["total_similarity"] / results["reconstructed"] if results["reconstructed"] > 0 else 0.0
        
        print(SystemMessages.RECOVERY_COMPLETE.format(
            recovered=results["reconstructed"],
            failed=results["failed"],
            duration=total_time
        ))
        print(f"📊 Average similarity: {avg_similarity:.2f}")
        
        results["total_time"] = total_time
        results["avg_similarity"] = avg_similarity
        
        return results

class ProgressiveHealing:
    """Progressive healing operations"""
    
    def __init__(self, cache, embedder):
        self.cache = cache
        self.embedder = embedder
        self.reconstruction = SemanticReconstruction(cache, embedder)
    
    def run_healing_cycles(self, num_cycles: int = RecoveryConfig.MAX_HEALING_CYCLES) -> Dict[str, Any]:
        """Run multiple healing cycles"""
        print(f"🔄 Testing progressive healing cycles...")
        
        cycle_results = []
        total_recovered = 0
        total_similarity = 0.0
        
        for cycle in range(num_cycles):
            print(f"   Cycle {cycle + 1}/{num_cycles}")
            
            # Create some blank files for testing
            blank_fragments = self._create_test_blanks(2)
            if not blank_fragments:
                break
            
            # Reconstruct blanks
            cycle_result = self.reconstruction.reconstruct_blank_fragments(blank_fragments)
            cycle_results.append(cycle_result)
            
            total_recovered += cycle_result["reconstructed"]
            total_similarity += cycle_result["total_similarity"]
        
        avg_similarity = total_similarity / total_recovered if total_recovered > 0 else 0.0
        
        print(SystemMessages.PROGRESSIVE_HEALING.format(
            total=total_recovered,
            cycles=num_cycles
        ))
        print(f"📊 Average similarity over cycles: {avg_similarity:.2f}")
        
        return {
            "cycles": num_cycles,
            "total_recovered": total_recovered,
            "avg_similarity": avg_similarity,
            "cycle_results": cycle_results,
            "progressive_improvement": self._calculate_improvement(cycle_results)
        }
    
    def _create_test_blanks(self, count: int) -> List[Dict[str, Any]]:
        """Create test blank fragments"""
        blank_fragments = []
        
        try:
            # Get existing fragments to create blanks from
            existing_fragments = list(self.cache.file_registry.keys())[:count]
            
            for frag_id in existing_fragments:
                # Create blank placeholder
                blank_id = f"{frag_id}_blank_{int(time.time())}"
                level = self.cache.file_registry[frag_id].get("level", 0)
                
                success = RecoveryOperations.create_blank_placeholder(
                    blank_id, level, self.cache.base_dir
                )
                
                if success:
                    blank_fragments.append({
                        "id": blank_id,
                        "level": level,
                        "placeholder_prompt": f"Reconstruct content for {blank_id} at level {level}",
                        "file_path": str(self.cache.base_dir / f"{blank_id}.json")
                    })
            
            print(f"   ✅ Created {len(blank_fragments)} blank placeholders")
            return blank_fragments
            
        except Exception as e:
            print(f"❌ Failed to create test blanks: {e}")
            return []
    
    def _calculate_improvement(self, cycle_results: List[Dict[str, Any]]) -> bool:
        """Calculate if there's progressive improvement"""
        if len(cycle_results) < 2:
            return False
        
        similarities = [cycle["avg_similarity"] for cycle in cycle_results]
        
        # Check if there's improvement over cycles
        for i in range(1, len(similarities)):
            if similarities[i] - similarities[i-1] < RecoveryConfig.HEALING_IMPROVEMENT_THRESHOLD:
                return False
        
        return True

class RecoveryAssessment:
    """Recovery assessment and reporting"""
    
    @staticmethod
    def assess_recovery_quality(reconstruction_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of recovery results"""
        total_reconstructed = reconstruction_results["reconstructed"]
        total_failed = reconstruction_results["failed"]
        avg_similarity = reconstruction_results["avg_similarity"]
        
        # Calculate reconstruction rate
        reconstruction_rate = total_reconstructed / (total_reconstructed + total_failed) if (total_reconstructed + total_failed) > 0 else 0.0
        
        # Calculate high-quality reconstructions
        high_quality_count = sum(1 for detail in reconstruction_results["details"] 
                               if detail["similarity"] >= RecoveryConfig.HIGH_QUALITY_THRESHOLD)
        
        # Calculate recovery score
        reconstruction_score = reconstruction_rate * 0.7 + (avg_similarity / 1.0) * 0.3
        
        return {
            "reconstruction_rate": reconstruction_rate,
            "avg_similarity": avg_similarity,
            "high_quality_reconstructions": high_quality_count,
            "reconstruction_score": reconstruction_score,
            "total_reconstructed": total_reconstructed,
            "total_failed": total_failed
        }
    
    @staticmethod
    def generate_recovery_report(reconstruction_results: Dict[str, Any], 
                               progressive_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate comprehensive recovery report"""
        assessment = RecoveryAssessment.assess_recovery_quality(reconstruction_results)
        
        report = {
            "timestamp": time.time(),
            "recovery_performance": assessment,
            "reconstruction_details": reconstruction_results["details"],
            "progressive_healing": progressive_results
        }
        
        # Add overall assessment
        if assessment["reconstruction_score"] >= RecoveryConfig.HIGH_QUALITY_THRESHOLD:
            report["overall_assessment"] = "EXCELLENT"
        elif assessment["reconstruction_score"] >= 0.5:
            report["overall_assessment"] = "GOOD"
        else:
            report["overall_assessment"] = "NEEDS_IMPROVEMENT"
        
        return report
