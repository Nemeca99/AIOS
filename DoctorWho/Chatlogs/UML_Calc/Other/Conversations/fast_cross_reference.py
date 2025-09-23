import os
import re
from collections import defaultdict, Counter

class FastCrossReferenceAnalyzer:
    """
    Faster cross-reference analyzer that works with existing extract files
    """
    
    def __init__(self, conversations_dir="."):
        self.conversations_dir = conversations_dir
        # Use existing extract files for faster processing
        self.extract_files = [
            "uml_calculator_extracts.md",
            "trees_extracts.md", 
            "nova_ai_extracts.md",
            "blackwall_extracts.md",
            "personal_extracts.md",
            "technical_extracts.md",
            "philosophy_extracts.md"
        ]
        
    def load_extract_samples(self, max_entries_per_file=500):
        """Load sample entries from each file for faster processing"""
        extracts = {}
        
        print("📂 Loading extract file samples...")
        for filename in self.extract_files:
            filepath = os.path.join(self.conversations_dir, filename)
            if os.path.exists(filepath):
                category = filename.replace("_extracts.md", "")
                entries = self.parse_extract_file_sample(filepath, max_entries_per_file)
                extracts[category] = entries
                print(f"✓ Loaded {len(entries)} sample entries from {filename}")
            else:
                print(f"✗ File not found: {filename}")
        
        return extracts
    
    def parse_extract_file_sample(self, filepath, max_entries):
        """Parse sample entries from extract file"""
        entries = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return entries
        
        # Split by conversation headers
        sections = re.split(r'## From: (.+)', content)
        
        entries_count = 0
        for i in range(1, len(sections), 2):
            if entries_count >= max_entries:
                break
                
            if i + 1 < len(sections):
                conversation_title = sections[i].strip()
                section_content = sections[i + 1]
                
                # Split individual entries by ---
                individual_entries = section_content.split('---')
                
                for entry in individual_entries[:5]:  # Max 5 entries per conversation
                    if entries_count >= max_entries:
                        break
                        
                    entry = entry.strip()
                    if entry and len(entry) > 30:
                        # Extract key terms quickly
                        key_terms = self.extract_key_terms_fast(entry)
                        entries.append({
                            "conversation": conversation_title,
                            "content": entry[:200] + "..." if len(entry) > 200 else entry,
                            "key_terms": key_terms
                        })
                        entries_count += 1
        
        return entries
    
    def extract_key_terms_fast(self, text):
        """Fast key term extraction"""
        # Common words to ignore
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'a', 'an'}
        
        # Extract words and filter
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        key_terms = [word for word in words if word not in stop_words]
        
        # Count frequency and return top terms
        term_counts = Counter(key_terms)
        return [term for term, count in term_counts.most_common(10)]
    
    def find_simple_connections(self, extracts):
        """Find simple connections between categories"""
        connections = defaultdict(lambda: defaultdict(list))
        
        print("🔗 Finding connections between categories...")
        categories = list(extracts.keys())
        
        for i, cat1 in enumerate(categories):
            for cat2 in categories[i+1:]:
                print(f"  Analyzing {cat1} ↔ {cat2}")
                shared_terms = self.find_shared_terms(extracts[cat1], extracts[cat2])
                if shared_terms:
                    connections[cat1][cat2] = shared_terms
                    connections[cat2][cat1] = shared_terms
        
        return dict(connections)
    
    def find_shared_terms(self, entries1, entries2):
        """Find shared terms between two categories"""
        # Collect all terms from each category
        terms1 = set()
        terms2 = set()
        
        for entry in entries1:
            terms1.update(entry['key_terms'])
        
        for entry in entries2:
            terms2.update(entry['key_terms'])
        
        # Find intersection
        shared = terms1.intersection(terms2)
        
        if len(shared) < 2:  # Need at least 2 shared terms to be meaningful
            return []
        
        # Create simple shared concept objects
        shared_concepts = []
        for term in list(shared)[:5]:  # Top 5 shared terms
            examples1 = [e for e in entries1 if term in e['key_terms']][:2]
            examples2 = [e for e in entries2 if term in e['key_terms']][:2]
            
            if examples1 and examples2:
                shared_concepts.append({
                    "term": term,
                    "examples_cat1": examples1,
                    "examples_cat2": examples2
                })
        
        return shared_concepts
    
    def analyze_conversation_overlap(self, extracts):
        """Quick analysis of conversation overlap"""
        conversation_categories = defaultdict(set)
        
        for category, entries in extracts.items():
            for entry in entries:
                conversation_categories[entry['conversation']].add(category)
        
        # Find multi-category conversations
        multi_category = {}
        for conv, categories in conversation_categories.items():
            if len(categories) > 1:
                multi_category[conv] = list(categories)
        
        return multi_category
    
    def generate_fast_report(self, output_file="fast_cross_reference_report.md"):
        """Generate a fast cross-reference report"""
        print("🚀 Starting Fast Cross-Reference Analysis...")
        
        # Load sample data
        extracts = self.load_extract_samples()
        
        if not extracts:
            print("✗ No extract files found")
            return
        
        # Find connections
        connections = self.find_simple_connections(extracts)
        
        # Analyze conversation overlap
        multi_category = self.analyze_conversation_overlap(extracts)
        
        # Generate report
        print("📝 Generating report...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Fast Cross-Reference Analysis Report\n\n")
            f.write("Based on sample analysis of extract files.\n\n")
            
            # Overview
            f.write("## Overview\n\n")
            total_entries = sum(len(entries) for entries in extracts.values())
            f.write(f"- Sample entries analyzed: {total_entries:,}\n")
            f.write(f"- Categories: {len(extracts)}\n")
            f.write(f"- Conversations with multiple categories: {len(multi_category)}\n\n")
            
            # Category sizes
            f.write("### Sample Sizes by Category\n\n")
            for category, entries in sorted(extracts.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"- **{category.replace('_', ' ').title()}**: {len(entries)} sample entries\n")
            f.write("\n")
            
            # Connections
            f.write("## Cross-Category Connections\n\n")
            connection_count = 0
            for cat1, cat_connections in connections.items():
                if cat_connections:
                    f.write(f"### {cat1.replace('_', ' ').title()}\n\n")
                    for cat2, shared_concepts in cat_connections.items():
                        if shared_concepts:
                            connection_count += 1
                            f.write(f"#### Connected to {cat2.replace('_', ' ').title()}\n\n")
                            f.write(f"**Shared terms:** {', '.join([c['term'] for c in shared_concepts])}\n\n")
                            
                            # Show one example
                            if shared_concepts:
                                concept = shared_concepts[0]
                                f.write(f"**Example connection via '{concept['term']}':**\n")
                                if concept['examples_cat1']:
                                    f.write(f"- {cat1}: {concept['examples_cat1'][0]['content']}\n")
                                if concept['examples_cat2']:
                                    f.write(f"- {cat2}: {concept['examples_cat2'][0]['content']}\n")
                                f.write("\n")
            
            # Multi-category conversations
            f.write("## Multi-Category Conversations\n\n")
            f.write("Conversations that appear in multiple insight categories:\n\n")
            
            for conv, categories in sorted(multi_category.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
                f.write(f"### {conv}\n")
                f.write(f"**Categories:** {', '.join(categories)}\n\n")
        
        print(f"✅ Fast cross-reference report generated: {output_file}")
        print(f"📊 Found {connection_count} category connections")
        print(f"🔗 Identified {len(multi_category)} multi-category conversations")
        
        return connections, multi_category

def main():
    analyzer = FastCrossReferenceAnalyzer()
    connections, multi_category = analyzer.generate_fast_report()

if __name__ == "__main__":
    main()
