import json
import os
from collections import defaultdict, Counter
import re

class CrossReferenceAnalyzer:
    """
    Tool to find connections and patterns across different extract files
    """
    
    def __init__(self, conversations_dir="."):
        self.conversations_dir = conversations_dir
        self.extract_files = [
            "uml_calculator_extracts.md",
            "trees_extracts.md", 
            "nova_ai_extracts.md",
            "blackwall_extracts.md",
            "personal_extracts.md",
            "technical_extracts.md",
            "philosophy_extracts.md",
            "timeline_extracts.md"
        ]
        
    def load_extracts(self):
        """Load all extract files and parse them"""
        extracts = {}
        
        for filename in self.extract_files:
            filepath = os.path.join(self.conversations_dir, filename)
            if os.path.exists(filepath):
                category = filename.replace("_extracts.md", "")
                extracts[category] = self.parse_extract_file(filepath)
                print(f"Loaded {len(extracts[category])} entries from {filename}")
            else:
                print(f"File not found: {filename}")
        
        return extracts
    
    def parse_extract_file(self, filepath):
        """Parse an extract file and return structured data"""
        entries = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by conversation headers
        sections = re.split(r'## From: (.+)', content)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                conversation_title = sections[i].strip()
                section_content = sections[i + 1]
                
                # Split individual entries by ---
                individual_entries = section_content.split('---')
                
                for entry in individual_entries:
                    entry = entry.strip()
                    if entry and len(entry) > 10:
                        entries.append({
                            "conversation": conversation_title,
                            "content": entry,
                            "word_count": len(entry.split()),
                            "keywords": self.extract_keywords(entry)
                        })
        
        return entries
    
    def extract_keywords(self, text):
        """Extract key terms from text"""
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        return list(set(keywords))  # Remove duplicates
    
    def find_concept_connections(self, extracts):
        """Find connections between categories based on shared concepts"""
        connections = defaultdict(lambda: defaultdict(list))
        
        categories = list(extracts.keys())
        
        for i, cat1 in enumerate(categories):
            for j, cat2 in enumerate(categories[i+1:], i+1):
                shared_concepts = self.find_shared_concepts(extracts[cat1], extracts[cat2])
                if shared_concepts:
                    connections[cat1][cat2] = shared_concepts
                    connections[cat2][cat1] = shared_concepts
        
        return dict(connections)
    
    def find_shared_concepts(self, entries1, entries2):
        """Find shared concepts between two sets of entries"""
        shared = []
        
        # Get all keywords from each category
        keywords1 = set()
        keywords2 = set()
        
        for entry in entries1:
            keywords1.update(entry['keywords'])
        
        for entry in entries2:
            keywords2.update(entry['keywords'])
        
        # Find intersection
        common_keywords = keywords1.intersection(keywords2)
        
        # Find entries that contain these common keywords
        for keyword in common_keywords:
            matching_entries1 = [e for e in entries1 if keyword in e['keywords']]
            matching_entries2 = [e for e in entries2 if keyword in e['keywords']]
            
            if matching_entries1 and matching_entries2:
                shared.append({
                    "concept": keyword,
                    "entries_cat1": matching_entries1[:3],  # Top 3
                    "entries_cat2": matching_entries2[:3],  # Top 3
                    "frequency": len(matching_entries1) + len(matching_entries2)
                })
        
        # Sort by frequency
        shared.sort(key=lambda x: x['frequency'], reverse=True)
        return shared[:10]  # Top 10 shared concepts
    
    def analyze_conversation_patterns(self, extracts):
        """Analyze patterns across conversations"""
        conversation_analysis = defaultdict(lambda: defaultdict(int))
        category_by_conversation = defaultdict(list)
        
        for category, entries in extracts.items():
            for entry in entries:
                conv = entry['conversation']
                conversation_analysis[conv][category] += 1
                category_by_conversation[conv].append(category)
        
        # Find conversations that span multiple categories
        multi_category_conversations = {}
        for conv, categories in category_by_conversation.items():
            unique_categories = set(categories)
            if len(unique_categories) > 1:
                multi_category_conversations[conv] = {
                    "categories": list(unique_categories),
                    "category_counts": dict(Counter(categories))
                }
        
        return dict(conversation_analysis), multi_category_conversations
    
    def generate_cross_reference_report(self, output_file="cross_reference_report.md"):
        """Generate comprehensive cross-reference report"""
        print("Loading extracts...")
        extracts = self.load_extracts()
        
        print("Finding concept connections...")
        connections = self.find_concept_connections(extracts)
        
        print("Analyzing conversation patterns...")
        conv_analysis, multi_category = self.analyze_conversation_patterns(extracts)
        
        # Generate report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Cross-Reference Analysis Report\n\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overview
            f.write("## Overview\n\n")
            total_entries = sum(len(entries) for entries in extracts.values())
            f.write(f"- Total entries analyzed: {total_entries:,}\n")
            f.write(f"- Categories: {len(extracts)}\n")
            f.write(f"- Conversations with multiple categories: {len(multi_category)}\n\n")
            
            # Category sizes
            f.write("### Category Sizes\n\n")
            for category, entries in sorted(extracts.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"- **{category.replace('_', ' ').title()}**: {len(entries):,} entries\n")
            f.write("\n")
            
            # Concept connections
            f.write("## Concept Connections Between Categories\n\n")
            for cat1, connections_dict in connections.items():
                if connections_dict:
                    f.write(f"### {cat1.replace('_', ' ').title()} Connections\n\n")
                    for cat2, shared_concepts in connections_dict.items():
                        if shared_concepts:
                            f.write(f"#### With {cat2.replace('_', ' ').title()}\n\n")
                            for concept in shared_concepts[:5]:  # Top 5
                                f.write(f"**Shared Concept: {concept['concept']}** (frequency: {concept['frequency']})\n\n")
                                f.write("Sample entries:\n")
                                for entry in concept['entries_cat1'][:2]:
                                    f.write(f"- {cat1}: {entry['content'][:100]}...\n")
                                for entry in concept['entries_cat2'][:2]:
                                    f.write(f"- {cat2}: {entry['content'][:100]}...\n")
                                f.write("\n")
            
            # Multi-category conversations
            f.write("## Multi-Category Conversations\n\n")
            f.write("Conversations that span multiple insight categories:\n\n")
            
            for conv, data in sorted(multi_category.items(), key=lambda x: len(x[1]['categories']), reverse=True)[:20]:
                f.write(f"### {conv}\n\n")
                f.write(f"**Categories involved:** {', '.join(data['categories'])}\n\n")
                f.write("**Entry distribution:**\n")
                for category, count in sorted(data['category_counts'].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"- {category.replace('_', ' ').title()}: {count} entries\n")
                f.write("\n")
        
        print(f"Cross-reference report generated: {output_file}")
        return connections, multi_category

def main():
    analyzer = CrossReferenceAnalyzer()
    connections, multi_category = analyzer.generate_cross_reference_report()
    
    print("\nCross-Reference Analysis Complete!")
    print(f"Found connections between {len(connections)} category pairs")
    print(f"Identified {len(multi_category)} multi-category conversations")

if __name__ == "__main__":
    import datetime
    main()
