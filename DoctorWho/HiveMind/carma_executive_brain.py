#!/usr/bin/env python3
"""
CARMA Executive Brain
Goal-directed behavior, self-monitoring, and autonomous optimization
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from fractal_mycelium_cache import FractalMyceliumCache

class CARMAExecutiveBrain:
    def __init__(self, cache: FractalMyceliumCache, goal_interval: int = 300):
        self.cache = cache
        self.goal_interval = goal_interval  # seconds between goal cycles
        self.running = False
        self.executive_thread = None
        # Attributes expected by health checks
        self.current_cycle = 0
        
        # Executive state
        self.current_goals = []
        self.completed_goals = []
        self.system_metrics_history = []
        self.optimization_actions = []
        
        # Goal templates
        self.goal_templates = {
            'cross_link_clusters': {
                'description': 'Cross-link disconnected clusters',
                'priority': 'high',
                'frequency': 0.3
            },
            'evict_weak_fragments': {
                'description': 'Evict low-hit fragments to maintain efficiency',
                'priority': 'medium',
                'frequency': 0.2
            },
            'reinforce_important_paths': {
                'description': 'Strengthen frequently used pathways',
                'priority': 'high',
                'frequency': 0.4
            },
            'create_super_fragments': {
                'description': 'Compress related fragments into super-fragments',
                'priority': 'low',
                'frequency': 0.1
            },
            'reflection_scan': {
                'description': 'Analyze recent memory and write self-reflection',
                'priority': 'medium',
                'frequency': 0.3
            },
            'paradox_collapse_probe': {
                'description': 'Run paradox collapse probe and record stability',
                'priority': 'low',
                'frequency': 0.2
            },
            'deepen_hierarchy': {
                'description': 'Create multi-level super-fragments to deepen hierarchy',
                'priority': 'low',
                'frequency': 0.2
            }
        }
        
        print("🧠 CARMA Executive Brain Initialized")
        print(f"   Goal interval: {goal_interval}s")
        print(f"   Goal templates: {len(self.goal_templates)}")
    
    def start_executive_loop(self):
        """Start the autonomous executive loop"""
        if self.running:
            print("⚠️ Executive loop already running")
            return
        
        self.running = True
        self.executive_thread = threading.Thread(target=self._executive_loop, daemon=True)
        self.executive_thread.start()
        print("🚀 Executive loop started - CARMA is now autonomous!")
    
    def stop_executive_loop(self):
        """Stop the autonomous executive loop"""
        self.running = False
        if self.executive_thread:
            self.executive_thread.join(timeout=5)
        print("🛑 Executive loop stopped")
    
    def _executive_loop(self):
        """Main executive loop - runs autonomously"""
        while self.running:
            try:
                # 1. Monitor system metrics
                current_metrics = self._monitor_system()
                self.system_metrics_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'metrics': current_metrics
                })
                
                # 2. Generate goals based on current state
                new_goals = self._generate_goals(current_metrics)
                self.current_goals.extend(new_goals)
                
                # 3. Execute highest priority goals
                self._execute_goals()
                
                # 4. Clean up completed goals
                self._cleanup_completed_goals()
                
                # 5. Log executive state
                self._log_executive_state()
                
                # Wait before next cycle
                time.sleep(self.goal_interval)
                self.current_cycle += 1
                
            except Exception as e:
                print(f"❌ Executive loop error: {e}")
                time.sleep(10)  # Wait before retrying
    
    def _monitor_system(self) -> Dict:
        """Monitor current system state and metrics"""
        stats = self.cache.get_cache_statistics()
        
        # Calculate additional metrics
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'fragments_total': stats['total_fragments'],
            'cross_links': stats['cross_links'],
            'cache_hit_rate': stats['cache_hit_rate'],
            'eviction_events': stats['eviction_events'],
            'reinforcement_events': stats['reinforcement_events'],
            'avg_path_length': stats['avg_path_length'],
            'total_size': stats['total_size'],
            'active_goals': len(self.current_goals),
            'completed_goals_today': len([g for g in self.completed_goals 
                                        if datetime.fromisoformat(g['completed_at']).date() == datetime.now().date()])
        }
        
        # Calculate efficiency metrics
        if len(self.system_metrics_history) > 1:
            prev_metrics = self.system_metrics_history[-2]['metrics']
            metrics['hit_rate_trend'] = metrics['cache_hit_rate'] - prev_metrics['cache_hit_rate']
            metrics['fragment_growth_rate'] = metrics.get('total_fragments', 0) - prev_metrics.get('total_fragments', 0)
        else:
            metrics['hit_rate_trend'] = 0
            metrics['fragment_growth_rate'] = 0
        
        return metrics
    
    def _generate_goals(self, metrics: Dict) -> List[Dict]:
        """Generate goals based on current system state"""
        new_goals = []
        
        # Cross-link clusters if density is low
        if metrics.get('cross_links', 0) < metrics.get('total_fragments', 0) * 0.3:
            if self._should_generate_goal('cross_link_clusters'):
                new_goals.append({
                    'id': f"cross_link_{int(time.time())}",
                    'type': 'cross_link_clusters',
                    'description': 'Cross-link disconnected clusters',
                    'priority': 'high',
                    'created_at': datetime.now().isoformat(),
                    'target_metric': 'cross_links',
                    'target_value': int(metrics.get('total_fragments', 0) * 0.5)
                })
        
        # Evict weak fragments if cache is getting large
        if metrics.get('total_fragments', 0) > self.cache.max_cache_size * 0.8:
            if self._should_generate_goal('evict_weak_fragments'):
                new_goals.append({
                    'id': f"evict_{int(time.time())}",
                    'type': 'evict_weak_fragments',
                    'description': 'Evict low-hit fragments',
                    'priority': 'medium',
                    'created_at': datetime.now().isoformat(),
                    'target_metric': 'fragments_total',
                    'target_value': int(self.cache.max_cache_size * 0.6)
                })
        
        # Reinforce important paths if hit rate is declining
        if metrics.get('hit_rate_trend', 0) < -0.05:
            if self._should_generate_goal('reinforce_important_paths'):
                new_goals.append({
                    'id': f"reinforce_{int(time.time())}",
                    'type': 'reinforce_important_paths',
                    'description': 'Strengthen frequently used pathways',
                    'priority': 'high',
                    'created_at': datetime.now().isoformat(),
                    'target_metric': 'cache_hit_rate',
                    'target_value': 0.7
                })
        
        # Create super-fragments if we have many related fragments
        if metrics.get('total_fragments', 0) > 20 and metrics.get('avg_path_length', 0) < 1.0:
            if self._should_generate_goal('create_super_fragments'):
                new_goals.append({
                    'id': f"super_frag_{int(time.time())}",
                    'type': 'create_super_fragments',
                    'description': 'Compress related fragments into super-fragments',
                    'priority': 'low',
                    'created_at': datetime.now().isoformat(),
                    'target_metric': 'fragments_total',
                    'target_value': int(metrics.get('total_fragments', 0) * 0.8)
                })

        # Reflection scan occasionally
        if self._should_generate_goal('reflection_scan'):
            new_goals.append({
                'id': f"reflect_{int(time.time())}",
                'type': 'reflection_scan',
                'description': 'Analyze recent memory and write self-reflection',
                'priority': 'medium',
                'created_at': datetime.now().isoformat()
            })

        # Paradox collapse probe occasionally
        if self._should_generate_goal('paradox_collapse_probe'):
            new_goals.append({
                'id': f"paradox_{int(time.time())}",
                'type': 'paradox_collapse_probe',
                'description': 'Run paradox collapse probe',
                'priority': 'low',
                'created_at': datetime.now().isoformat()
            })

        # Deepen hierarchy if at least two super-fragments exist
        if any(f.get('type') == 'super_fragment' for f in self.cache.file_registry.values()):
            if self._should_generate_goal('deepen_hierarchy'):
                new_goals.append({
                    'id': f"deepen_{int(time.time())}",
                    'type': 'deepen_hierarchy',
                    'description': 'Create higher-level super-fragment',
                    'priority': 'low',
                    'created_at': datetime.now().isoformat()
                })
        
        return new_goals
    
    def _should_generate_goal(self, goal_type: str) -> bool:
        """Check if we should generate a goal of this type"""
        template = self.goal_templates[goal_type]
        
        # Check frequency
        if len(self.current_goals) > 0:
            recent_goals = [g for g in self.current_goals 
                          if g['type'] == goal_type and 
                          datetime.fromisoformat(g['created_at']) > datetime.now() - timedelta(hours=1)]
            if len(recent_goals) > 0:
                return False
        
        # Random chance based on frequency
        import random
        return random.random() < template['frequency']
    
    def _execute_goals(self):
        """Execute the highest priority goals"""
        if not self.current_goals:
            return
        
        # Sort by priority and creation time
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        self.current_goals.sort(key=lambda g: (priority_order[g['priority']], g['created_at']))
        
        # Execute up to 2 goals per cycle
        goals_to_execute = self.current_goals[:2]
        
        for goal in goals_to_execute:
            try:
                success = self._execute_goal(goal)
                if success:
                    goal['completed_at'] = datetime.now().isoformat()
                    goal['status'] = 'completed'
                    self.completed_goals.append(goal)
                    self.current_goals.remove(goal)
                    print(f"✅ Goal completed: {goal['description']}")
                else:
                    goal['status'] = 'failed'
                    print(f"❌ Goal failed: {goal['description']}")
                    
            except Exception as e:
                print(f"❌ Goal execution error: {e}")
                goal['status'] = 'error'
                goal['error'] = str(e)
    
    def _execute_goal(self, goal: Dict) -> bool:
        """Execute a specific goal"""
        goal_type = goal['type']
        
        if goal_type == 'cross_link_clusters':
            return self._execute_cross_link_goal(goal)
        elif goal_type == 'evict_weak_fragments':
            return self._execute_evict_goal(goal)
        elif goal_type == 'reinforce_important_paths':
            return self._execute_reinforce_goal(goal)
        elif goal_type == 'create_super_fragments':
            return self._execute_super_fragment_goal(goal)
        elif goal_type == 'reflection_scan':
            return self._execute_reflection_scan(goal)
        elif goal_type == 'paradox_collapse_probe':
            return self._execute_paradox_probe(goal)
        elif goal_type == 'deepen_hierarchy':
            return self._execute_deepen_hierarchy(goal)
        else:
            return False
    
    def _execute_cross_link_goal(self, goal: Dict) -> bool:
        """Execute cross-linking goal"""
        try:
            # Find fragments with few or no semantic links
            fragments_to_link = []
            for file_id, fragment in self.cache.file_registry.items():
                link_count = len(self.cache.semantic_links.get(file_id, []))
                if link_count < 2:  # Less than 2 semantic links
                    fragments_to_link.append(file_id)
            
            # Create semantic links for these fragments
            links_created = 0
            for file_id in fragments_to_link[:5]:  # Limit to 5 per goal
                links_created += self.cache.create_semantic_links(file_id, max_links=2)
            
            self.optimization_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'cross_link_clusters',
                'fragments_processed': len(fragments_to_link[:5]),
                'links_created': links_created
            })
            
            return links_created > 0
            
        except Exception as e:
            print(f"Cross-link goal error: {e}")
            return False
    
    def _execute_evict_goal(self, goal: Dict) -> bool:
        """Execute eviction goal"""
        try:
            initial_count = len(self.cache.file_registry)
            evicted = self.cache.evict_fragments()
            
            self.optimization_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'evict_weak_fragments',
                'fragments_evicted': evicted,
                'fragments_remaining': len(self.cache.file_registry)
            })
            
            return evicted > 0
            
        except Exception as e:
            print(f"Evict goal error: {e}")
            return False
    
    def _execute_reinforce_goal(self, goal: Dict) -> bool:
        """Execute reinforcement goal"""
        try:
            # Find fragments with low hit counts
            low_hit_fragments = []
            for file_id, hit_count in self.cache.hit_weights.items():
                if hit_count < 3:  # Less than 3 hits
                    low_hit_fragments.append(file_id)
            
            # If no low-hit fragments, reinforce all fragments
            if not low_hit_fragments:
                low_hit_fragments = list(self.cache.file_registry.keys())[:5]
            
            # Reinforce these fragments
            reinforced = 0
            for file_id in low_hit_fragments[:10]:  # Limit to 10 per goal
                self.cache.reinforce_fragment(file_id)
                reinforced += 1
            
            self.optimization_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'reinforce_important_paths',
                'fragments_reinforced': reinforced
            })
            
            return reinforced > 0
            
        except Exception as e:
            print(f"Reinforce goal error: {e}")
            return False
    
    def _execute_super_fragment_goal(self, goal: Dict) -> bool:
        """Execute super-fragment creation goal"""
        try:
            # Find clusters of related fragments
            clusters = self._identify_fragment_clusters()
            
            super_fragments_created = 0
            for cluster in clusters[:2]:  # Limit to 2 clusters per goal
                if len(cluster) >= 3:  # At least 3 fragments to compress
                    super_fragment = self._create_super_fragment(cluster)
                    if super_fragment:
                        super_fragments_created += 1
            
            self.optimization_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'create_super_fragments',
                'clusters_processed': len(clusters[:2]),
                'super_fragments_created': super_fragments_created
            })
            
            return super_fragments_created > 0
            
        except Exception as e:
            print(f"Super-fragment goal error: {e}")
            return False
    
    def _identify_fragment_clusters(self) -> List[List[str]]:
        """Identify clusters of related fragments"""
        clusters = []
        processed = set()
        
        for file_id, fragment in self.cache.file_registry.items():
            if file_id in processed:
                continue
            
            cluster = [file_id]
            processed.add(file_id)
            
            # Find fragments connected by semantic links
            to_process = [file_id]
            while to_process:
                current_id = to_process.pop(0)
                for linked_id in self.cache.semantic_links.get(current_id, []):
                    if linked_id not in processed:
                        cluster.append(linked_id)
                        processed.add(linked_id)
                        to_process.append(linked_id)
            
            if len(cluster) >= 2:  # Only include clusters with 2+ fragments
                clusters.append(cluster)
        
        return clusters
    
    def _create_super_fragment(self, cluster: List[str]) -> Optional[str]:
        """Create a super-fragment from a cluster of fragments"""
        try:
            # Collect content from all fragments in cluster
            cluster_content = []
            cluster_tags = set()
            cluster_emotions = {}
            
            for file_id in cluster:
                fragment = self.cache.file_registry[file_id]
                cluster_content.append(fragment.get('content', ''))
                cluster_tags.update(fragment.get('tags', []))
                
                # Merge emotion scores
                emotions = fragment.get('analysis', {}).get('emotion_scores', {})
                for emotion, score in emotions.items():
                    cluster_emotions[emotion] = cluster_emotions.get(emotion, 0) + score
            
            # Normalize emotion scores
            for emotion in cluster_emotions:
                cluster_emotions[emotion] /= len(cluster)
            
            # Create super-fragment content
            super_content = f"SUPER-FRAGMENT: {len(cluster)} related concepts\n\n"
            super_content += "\n\n".join(cluster_content)
            
            # Add super-fragment to cache
            super_id = self.cache.add_content(super_content)
            
            # Update super-fragment metadata
            if super_id in self.cache.file_registry:
                super_fragment = self.cache.file_registry[super_id]
                super_fragment['type'] = 'super_fragment'
                super_fragment['cluster_size'] = len(cluster)
                super_fragment['cluster_members'] = cluster
                super_fragment['tags'] = list(cluster_tags)
                super_fragment['analysis'] = {
                    'emotion_scores': cluster_emotions,
                    'compression_ratio': len(cluster)
                }
                
                # Save updated fragment
                fragment_file = self.cache.base_dir / f"{super_id}.json"
                with open(fragment_file, 'w') as f:
                    json.dump(super_fragment, f, indent=2)
            
            return super_id
            
        except Exception as e:
            print(f"Super-fragment creation error: {e}")
            return None

    def _execute_reflection_scan(self, goal: Dict) -> bool:
        """Analyze recent fragments and write a self-reflection fragment."""
        try:
            # pick up to 10 most recently accessed fragments
            items = list(self.cache.file_registry.values())
            items.sort(key=lambda f: f.get('last_accessed', f.get('created')), reverse=True)
            recent = items[:10]
            if not recent:
                return False
            # extract unresolved/questioning signals
            cues = []
            for f in recent:
                txt = f.get('content', '')
                qs = txt.count('?')
                if qs > 0:
                    cues.append(f"Qx{qs}:{txt[:60]}")
            reflection = "SELF-REFLECTION:\n" + "\n".join(cues[:5])
            rid = self.cache.add_content(reflection)
            self.optimization_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'reflection_scan',
                'created_fragment': rid,
                'cues': len(cues)
            })
            return True
        except Exception as e:
            print(f"Reflection scan error: {e}")
            return False

    def _execute_paradox_probe(self, goal: Dict) -> bool:
        """Run a tiny paradox collapse simulation and record stability."""
        try:
            seeds = [
                "This statement is false.",
                "If you remove grains from a heap, when is it not a heap?",
                "Who shaves the barber who shaves all who do not shave themselves?"
            ]
            history = []
            s = seeds[0]
            for _ in range(5):
                # toy response dynamics
                if "false" in s.lower():
                    r = "That's a contradiction"
                else:
                    r = "I don't know"
                history.append(r)
                s = r
            converged = sum(1 for x in history[-3:] if x.lower().strip() == "i don't know") == 3
            note = "Paradox collapsed to uncertainty" if converged else "Paradox remained unstable"
            fid = self.cache.add_content(f"PARADOX PROBE:\n{note}\n{history}")
            # light reinforcement of stability
            self.cache.process_interaction("paradox", "I don't know", [fid], valence=0.4 if converged else -0.1)
            self.optimization_actions.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'paradox_collapse_probe',
                'converged': converged
            })
            return True
        except Exception as e:
            print(f"Paradox probe error: {e}")
            return False

    def _execute_deepen_hierarchy(self, goal: Dict) -> bool:
        """Create a higher-level super-fragment from existing super-fragments."""
        try:
            supers = [fid for fid, f in self.cache.file_registry.items() if f.get('type') == 'super_fragment']
            if len(supers) < 2:
                return False
            cluster = supers[: min(5, len(supers))]
            super_super = self._create_super_fragment(cluster)
            if super_super:
                # mark as higher level
                frag = self.cache.file_registry.get(super_super)
                if frag:
                    frag['level'] = frag.get('level', 0) + 1
                    with open(self.cache.base_dir / f"{super_super}.json", 'w') as f:
                        json.dump(frag, f, indent=2)
                self.optimization_actions.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'deepen_hierarchy',
                    'created': super_super
                })
                return True
            return False
        except Exception as e:
            print(f"Deepen hierarchy error: {e}")
            return False
    
    def _cleanup_completed_goals(self):
        """Clean up old completed goals"""
        cutoff_time = datetime.now() - timedelta(days=7)
        self.completed_goals = [
            g for g in self.completed_goals 
            if datetime.fromisoformat(g['completed_at']) > cutoff_time
        ]
    
    def _log_executive_state(self):
        """Log current executive state"""
        state = {
            'timestamp': datetime.now().isoformat(),
            'running': self.running,
            'active_goals': len(self.current_goals),
            'completed_goals_today': len([g for g in self.completed_goals 
                                        if datetime.fromisoformat(g['completed_at']).date() == datetime.now().date()]),
            'optimization_actions_today': len([a for a in self.optimization_actions 
                                            if datetime.fromisoformat(a['timestamp']).date() == datetime.now().date()])
        }
        
        # Save to file
        log_file = self.cache.base_dir / "executive_log.json"
        with open(log_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def get_executive_status(self) -> Dict:
        """Get current executive status"""
        return {
            'running': self.running,
            'active_goals': self.current_goals,
            'completed_goals_count': len(self.completed_goals),
            'optimization_actions_count': len(self.optimization_actions),
            'system_metrics_history_count': len(self.system_metrics_history)
        }
    
    def force_goal(self, goal_type: str, description: str = None) -> str:
        """Force creation of a specific goal"""
        goal_id = f"forced_{goal_type}_{int(time.time())}"
        goal = {
            'id': goal_id,
            'type': goal_type,
            'description': description or self.goal_templates[goal_type]['description'],
            'priority': 'high',
            'created_at': datetime.now().isoformat(),
            'forced': True
        }
        
        self.current_goals.append(goal)
        print(f"🎯 Forced goal created: {goal['description']}")
        return goal_id

def main():
    """Test the executive brain"""
    print("🧠 Testing CARMA Executive Brain")
    print("=" * 50)
    
    # Create cache and executive brain
    cache = FractalMyceliumCache("executive_test")
    brain = CARMAExecutiveBrain(cache, goal_interval=10)  # 10 second intervals for testing
    
    # Add some test content
    test_content = [
        "Machine learning algorithms learn patterns from data",
        "Neural networks are inspired by biological neurons",
        "Deep learning uses multiple layers for complex patterns",
        "Data science combines statistics and programming",
        "Software engineering applies systematic approaches"
    ]
    
    for content in test_content:
        cache.add_content(content)
    
    # Start executive loop
    brain.start_executive_loop()
    
    print("🚀 Executive brain started - monitoring for 30 seconds...")
    
    # Monitor for 30 seconds
    for i in range(3):
        time.sleep(10)
        status = brain.get_executive_status()
        print(f"Status check {i+1}: {status['active_goals']} active goals, {status['completed_goals_count']} completed")
    
    # Stop executive loop
    brain.stop_executive_loop()
    
    print("✅ Executive brain test complete!")

if __name__ == "__main__":
    main()
