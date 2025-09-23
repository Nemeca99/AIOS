#!/usr/bin/env python3
"""
Memory Topology Visualization
Creates visual graphs of the fractal mycelium memory structure
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from datetime import datetime

class MemoryVisualizer:
    """Visualizes the fractal mycelium memory topology"""
    
    def __init__(self, cache_dir: str = "Data/FractalCache"):
        self.cache_dir = Path(cache_dir)
        self.graph = nx.DiGraph()
        self.fragments = {}
        self.semantic_links = {}
        
    def load_memory_topology(self) -> Dict:
        """Load the current memory topology from cache files"""
        print("🔍 Loading memory topology...")
        
        # Load all fragment files
        for file_path in self.cache_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                frag_id = data.get('id', file_path.stem)
                self.fragments[frag_id] = data
                
                # Add node to graph
                self.graph.add_node(frag_id, **{
                    'level': data.get('level', 0),
                    'content_length': len(data.get('content', '')),
                    'hits': data.get('hits', 0),
                    'status': data.get('status', 'active'),
                    'similarity_score': data.get('similarity_score', 0.0)
                })
                
                # Add parent-child relationships
                parent_id = data.get('parent_id')
                if parent_id:
                    self.graph.add_edge(parent_id, frag_id, relationship='parent-child')
                
                children_ids = data.get('children_ids', [])
                for child_id in children_ids:
                    self.graph.add_edge(frag_id, child_id, relationship='parent-child')
                
                # Add semantic links
                semantic_links = data.get('semantic_links', [])
                for linked_id in semantic_links:
                    if linked_id in self.fragments:
                        self.graph.add_edge(frag_id, linked_id, relationship='semantic')
                        self.semantic_links[(frag_id, linked_id)] = data.get('similarity_score', 0.0)
                
            except Exception as e:
                print(f"   Warning: Could not load {file_path}: {e}")
        
        print(f"   ✅ Loaded {len(self.fragments)} fragments")
        print(f"   📊 Graph: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        
        return {
            'fragments': len(self.fragments),
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'parent_child_edges': len([e for e in self.graph.edges(data=True) if e[2].get('relationship') == 'parent-child']),
            'semantic_edges': len([e for e in self.graph.edges(data=True) if e[2].get('relationship') == 'semantic'])
        }
    
    def create_topology_visualization(self, output_path: str = "experiments/memory_topology.png"):
        """Create a visual representation of the memory topology"""
        print("🎨 Creating memory topology visualization...")
        
        # Set up the plot
        plt.figure(figsize=(16, 12))
        
        # Use hierarchical layout for better visualization
        pos = self._create_hierarchical_layout()
        
        # Color nodes by level
        node_colors = self._get_node_colors()
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph, 
            pos, 
            node_color=node_colors,
            node_size=300,
            alpha=0.8
        )
        
        # Draw edges with different styles
        parent_child_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d.get('relationship') == 'parent-child']
        semantic_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d.get('relationship') == 'semantic']
        
        # Draw parent-child edges (solid lines)
        if parent_child_edges:
            nx.draw_networkx_edges(
                self.graph, 
                pos, 
                edgelist=parent_child_edges,
                edge_color='blue',
                style='solid',
                width=2,
                alpha=0.6
            )
        
        # Draw semantic edges (dashed lines)
        if semantic_edges:
            nx.draw_networkx_edges(
                self.graph, 
                pos, 
                edgelist=semantic_edges,
                edge_color='red',
                style='dashed',
                width=1,
                alpha=0.4
            )
        
        # Draw labels
        labels = {node: node[:8] + '...' if len(node) > 8 else node for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)
        
        # Add title and legend
        plt.title("CARMA Memory Topology\n(Fractal Mycelium Structure)", fontsize=16, fontweight='bold')
        plt.figtext(0.02, 0.02, 
                   f"Nodes: {self.graph.number_of_nodes()}, Edges: {self.graph.number_of_edges()}\n"
                   f"Blue: Parent-Child, Red: Semantic Links", 
                   fontsize=10)
        
        # Add color legend
        self._add_color_legend()
        
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Visualization saved to: {output_path}")
    
    def create_similarity_heatmap(self, output_path: str = "experiments/similarity_heatmap.png"):
        """Create a heatmap of fragment similarities"""
        print("🔥 Creating similarity heatmap...")
        
        # Create similarity matrix
        fragment_ids = list(self.fragments.keys())
        n = len(fragment_ids)
        similarity_matrix = np.zeros((n, n))
        
        for i, frag1 in enumerate(fragment_ids):
            for j, frag2 in enumerate(fragment_ids):
                if i == j:
                    similarity_matrix[i][j] = 1.0
                elif (frag1, frag2) in self.semantic_links:
                    similarity_matrix[i][j] = self.semantic_links[(frag1, frag2)]
                elif (frag2, frag1) in self.semantic_links:
                    similarity_matrix[i][j] = self.semantic_links[(frag2, frag1)]
                else:
                    # Calculate basic similarity based on content overlap
                    content1 = self.fragments[frag1].get('content', '')
                    content2 = self.fragments[frag2].get('content', '')
                    similarity_matrix[i][j] = self._calculate_content_similarity(content1, content2)
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        im = plt.imshow(similarity_matrix, cmap='viridis', aspect='auto')
        
        # Add colorbar
        plt.colorbar(im, label='Similarity Score')
        
        # Set labels
        plt.xlabel('Fragment Index')
        plt.ylabel('Fragment Index')
        plt.title('Fragment Similarity Heatmap\n(CARMA Memory Structure)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Heatmap saved to: {output_path}")
    
    def create_performance_dashboard(self, output_path: str = "experiments/performance_dashboard.png"):
        """Create a performance dashboard"""
        print("📊 Creating performance dashboard...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Fragment distribution by level
        levels = [data.get('level', 0) for data in self.fragments.values()]
        level_counts = {}
        for level in levels:
            level_counts[level] = level_counts.get(level, 0) + 1
        
        ax1.bar(level_counts.keys(), level_counts.values(), color='skyblue')
        ax1.set_xlabel('Fragment Level')
        ax1.set_ylabel('Count')
        ax1.set_title('Fragment Distribution by Level')
        ax1.grid(True, alpha=0.3)
        
        # 2. Content length distribution
        content_lengths = [len(data.get('content', '')) for data in self.fragments.values()]
        ax2.hist(content_lengths, bins=20, color='lightgreen', alpha=0.7)
        ax2.set_xlabel('Content Length (characters)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Content Length Distribution')
        ax2.grid(True, alpha=0.3)
        
        # 3. Hit count distribution
        hit_counts = [data.get('hits', 0) for data in self.fragments.values()]
        ax3.hist(hit_counts, bins=20, color='orange', alpha=0.7)
        ax3.set_xlabel('Hit Count')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Fragment Hit Distribution')
        ax3.grid(True, alpha=0.3)
        
        # 4. Similarity score distribution
        similarity_scores = [data.get('similarity_score', 0.0) for data in self.fragments.values()]
        ax4.hist(similarity_scores, bins=20, color='purple', alpha=0.7)
        ax4.set_xlabel('Similarity Score')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Similarity Score Distribution')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('CARMA Memory Performance Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Dashboard saved to: {output_path}")
    
    def _create_hierarchical_layout(self) -> Dict:
        """Create a hierarchical layout for the graph"""
        # Use spring layout as base
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Adjust positions based on levels
        for node, data in self.graph.nodes(data=True):
            level = data.get('level', 0)
            pos[node] = (pos[node][0], level * 2)  # Spread by level
        
        return pos
    
    def _get_node_colors(self) -> List[str]:
        """Get colors for nodes based on their properties"""
        colors = []
        for node, data in self.graph.nodes(data=True):
            level = data.get('level', 0)
            status = data.get('status', 'active')
            
            if status == 'reconstructed':
                colors.append('lightcoral')  # Red for reconstructed
            elif level == 0:
                colors.append('gold')  # Gold for root level
            elif level == 1:
                colors.append('lightblue')  # Blue for level 1
            elif level == 2:
                colors.append('lightgreen')  # Green for level 2
            else:
                colors.append('lightgray')  # Gray for deeper levels
        
        return colors
    
    def _add_color_legend(self):
        """Add color legend to the plot"""
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor='gold', label='Root Level'),
            plt.Rectangle((0, 0), 1, 1, facecolor='lightblue', label='Level 1'),
            plt.Rectangle((0, 0), 1, 1, facecolor='lightgreen', label='Level 2'),
            plt.Rectangle((0, 0), 1, 1, facecolor='lightgray', label='Deeper Levels'),
            plt.Rectangle((0, 0), 1, 1, facecolor='lightcoral', label='Reconstructed')
        ]
        plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate basic content similarity"""
        if not content1 or not content2:
            return 0.0
        
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def generate_visualization_report(self) -> Dict:
        """Generate a comprehensive visualization report"""
        print("📋 Generating visualization report...")
        
        # Load topology
        topology_stats = self.load_memory_topology()
        
        # Create visualizations
        self.create_topology_visualization()
        self.create_similarity_heatmap()
        self.create_performance_dashboard()
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'topology_stats': topology_stats,
            'visualizations_created': [
                'experiments/memory_topology.png',
                'experiments/similarity_heatmap.png', 
                'experiments/performance_dashboard.png'
            ],
            'fractal_structure': {
                'max_level': max([data.get('level', 0) for data in self.fragments.values()]),
                'avg_children_per_node': self._calculate_avg_children(),
                'semantic_connectivity': len(self.semantic_links) / len(self.fragments) if self.fragments else 0
            }
        }
        
        # Save report
        with open('experiments/visualization_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("   ✅ Visualization report generated")
        return report
    
    def _calculate_avg_children(self) -> float:
        """Calculate average number of children per node"""
        total_children = 0
        parent_nodes = 0
        
        for data in self.fragments.values():
            children = data.get('children_ids', [])
            if children:
                total_children += len(children)
                parent_nodes += 1
        
        return total_children / parent_nodes if parent_nodes > 0 else 0.0

if __name__ == "__main__":
    # Create visualizations
    visualizer = MemoryVisualizer()
    report = visualizer.generate_visualization_report()
    
    print("\n🎨 Memory Visualization Complete!")
    print(f"   📊 Fragments: {report['topology_stats']['fragments']}")
    print(f"   🔗 Semantic Links: {report['topology_stats']['semantic_edges']}")
    print(f"   📈 Max Level: {report['fractal_structure']['max_level']}")
    print(f"   🌐 Visualizations: {len(report['visualizations_created'])}")
