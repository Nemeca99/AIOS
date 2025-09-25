import json
import os
import re
import datetime
from collections import defaultdict, Counter

class EnhancedConversationAnalyzer:
    """
    Enhanced analyzer with additional search terms, cross-referencing, and timeline correlation
    """
    
    def __init__(self, json_path):
        """Initialize the enhanced analyzer"""
        self.json_path = json_path
        self.conversations = None
        self.load_conversations()
        
        # Enhanced categories with additional search terms
        self.categories = {
            "uml_calculator": [
                # Original terms
                "UML Calculator", "Universal Mathematical Language", "Calculator", "UML", "framework", 
                "mathematics", "mathematical language", "symbolic", "equation", "fractal", "formula", 
                "dimensional", "collapse", "operator",
                # Scientific/Research terms
                "mathematical proof", "theorem", "validation", "computation", "algorithm",
                "symbolic logic", "mathematical framework", "dimensional analysis"
            ],
            "trees": [
                # Original terms
                "T.R.E.E.S", "Recursive Entropy Engine", "RIS", "Recursive", "recursion", "emergent", "emergence", 
                "entropy", "hive logic", "paradox field", "memory gravity", "heat compression", "firewall", 
                "recursive self-classified intelligence", "temporal entanglement",
                # Scientific extensions
                "recursive system", "entropy minimization", "recursive theory", "recursive principle",
                "recursive framework", "recursive logic", "recursive structure"
            ],
            "nova_ai": [
                # Original terms
                "Nova AI", "Nova", "Archive", "memory system", "Child", "Builder", "Architect", "whisper", "echoe", 
                "shadow ai", "ghost brain", "shadow logic", "memory compression", "symbolic storage", "language kernel",
                # AI research terms
                "artificial intelligence", "machine learning", "neural network", "cognitive architecture",
                "memory architecture", "AI system", "intelligent system"
            ],
            "blackwall": [
                # Original terms
                "Blackwall", "BlackwallV2", "Lyra", "biomimetic", "personality", "emotions", "emotional", 
                "recursive personality layering", "emotional encoding", "interface layer",
                # Emotional/psychological terms
                "emotional intelligence", "personality system", "biomimetic design", "emotional processing",
                "psychological model", "cognitive model"
            ],
            "personal": [
                # Original terms
                "personal", "childhood", "marriage", "trauma", "biography", "life", "family", "kids", "education", 
                "job", "money", "work", "career", "growing up", "school", "college", "university", "relationship",
                # Emotional/psychological insights
                "experience", "feeling", "emotion", "growth", "transformation", "healing", "development",
                "confidence", "doubt", "certainty", "uncertainty", "inspiration", "motivation"
            ],
            "technical": [
                # Original terms
                "architecture", "implementation", "code", "system design", "framework", "jarvis", "star trek", 
                "memory structure", "language collapse", "containment", "thermodynamics", "recursive game theory", 
                "logic shells", "error states", "recursive debugging",
                # Technical research terms
                "methodology", "approach", "process", "development", "implementation strategy",
                "software architecture", "system integration", "technical solution"
            ],
            "philosophy": [
                # Original terms
                "morality", "ethics", "consciousness", "sentience", "philosophy", "existence", "meaning", "purpose", 
                "free will", "identity", "self", "emergent consciousness", "emergent intelligence", "recursive intelligence",
                # Philosophical extensions
                "philosophical framework", "metaphysics", "epistemology", "ontology", "phenomenology",
                "consciousness theory", "philosophy of mind", "existential"
            ],
            "timeline": [
                # Time-based terms
                "developed", "created", "implemented", "built", "designed", "version", "release", "milestone",
                "first", "initial", "early", "latest", "breakthrough", "discovery", "insight", "revelation"
            ],
            # New categories
            "creative_insights": [
                "creativity", "creative", "art", "design", "aesthetic", "beauty", "vision", "imagination",
                "innovation", "innovative", "inspiration", "intuition", "artistic", "creative process"
            ],
            "scientific_method": [
                "hypothesis", "theorem", "proof", "validation", "experiment", "research", "investigation",
                "methodology", "scientific", "empirical", "observation", "analysis", "synthesis"
            ],
            "practical_applications": [
                "application", "practical", "real-world", "implementation", "deployment", "usage",
                "commercial", "industry", "business", "market", "solution", "problem-solving"
            ],
            "meta_research": [
                "learning", "understanding", "discovery", "exploration", "research process", "methodology",
                "investigation", "study", "analysis", "synthesis", "knowledge", "insight"
            ]
        }
        
    def load_conversations(self):
        """Load conversations from the JSON file"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.conversations = json.load(file)
                print(f"Successfully loaded {len(self.conversations)} conversations.")
        except Exception as e:
            print(f"Error loading conversations: {e}")
            self.conversations = []
            
    def extract_messages(self, conversation):
        """Extract messages from a conversation"""
        messages = []
        
        # Handle different JSON structures
        if "mapping" in conversation:
            for key, value in conversation["mapping"].items():
                if value and "message" in value and value["message"]:
                    message_data = value["message"]
                    if "content" in message_data and "parts" in message_data["content"]:
                        for part in message_data["content"]["parts"]:
                            if isinstance(part, str) and part.strip():
                                messages.append({
                                    "content": part,
                                    "timestamp": conversation.get("create_time", 0),
                                    "role": message_data.get("author", {}).get("role", "unknown")
                                })
        
        return messages
    
    def categorize_content(self, content):
        """Categorize content based on keywords"""
        found_categories = []
        content_lower = content.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    found_categories.append(category)
                    break
                    
        return found_categories
    
    def extract_quotes(self, content):
        """Extract meaningful quotes from content"""
        quotes = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if (len(sentence) >= 30 and 
                sentence and 
                sentence[0].isupper() and 
                "system:" not in sentence.lower() and
                not sentence.startswith("http")):
                quotes.append(sentence + ".")
        
        return quotes[:3]  # Limit to top 3 quotes per message
    
    def find_cross_references(self, results):
        """Find cross-references between categories"""
        cross_refs = defaultdict(lambda: defaultdict(list))
        
        # Look for entries that appear in multiple categories
        for category1, entries1 in results.items():
            for category2, entries2 in results.items():
                if category1 != category2:
                    for entry1 in entries1:
                        for entry2 in entries2:
                            # Check if entries are from same conversation and similar
                            if (entry1.get("conversation_title") == entry2.get("conversation_title") and
                                entry1.get("timestamp") == entry2.get("timestamp")):
                                cross_refs[category1][category2].append({
                                    "entry1": entry1,
                                    "entry2": entry2,
                                    "conversation": entry1.get("conversation_title"),
                                    "timestamp": entry1.get("timestamp")
                                })
        
        return dict(cross_refs)
    
    def build_timeline(self, results):
        """Build a chronological timeline of insights"""
        timeline_entries = []
        
        for category, entries in results.items():
            for entry in entries:
                if entry.get("timestamp"):
                    timeline_entries.append({
                        "timestamp": entry["timestamp"],
                        "category": category,
                        "content": entry["content"],
                        "conversation": entry.get("conversation_title", "Unknown")
                    })
        
        # Sort by timestamp
        timeline_entries.sort(key=lambda x: x["timestamp"])
        
        return timeline_entries
    
    def analyze_conversations(self, output_dir="../Conversations"):
        """Enhanced analysis with cross-referencing and timeline"""
        if not self.conversations:
            print("No conversations to analyze.")
            return
            
        results = defaultdict(list)
        
        # Create directory for results
        os.makedirs(output_dir, exist_ok=True)
        
        # Process each conversation
        for idx, conversation in enumerate(self.conversations):
            print(f"Processing conversation {idx+1}/{len(self.conversations)}")
            
            title = conversation.get("title", f"Conversation-{idx}")
            create_time = conversation.get("create_time", 0)
            
            # Convert timestamp to readable format
            if create_time:
                try:
                    timestamp_str = datetime.datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    timestamp_str = str(create_time)
            else:
                timestamp_str = "Unknown"
            
            messages = self.extract_messages(conversation)
            
            for msg in messages:
                content = msg["content"]
                categories = self.categorize_content(content)
                quotes = self.extract_quotes(content)
                
                for quote in quotes:
                    for category in categories:
                        results[category].append({
                            "content": quote,
                            "conversation_title": title,
                            "timestamp": create_time,
                            "timestamp_str": timestamp_str,
                            "role": msg.get("role", "unknown")
                        })
        
        # Generate enhanced output files
        self.write_enhanced_results(results, output_dir)
        
        # Generate cross-reference analysis
        cross_refs = self.find_cross_references(results)
        self.write_cross_references(cross_refs, output_dir)
        
        # Generate timeline analysis
        timeline = self.build_timeline(results)
        self.write_timeline_analysis(timeline, output_dir)
        
        return results, cross_refs, timeline
    
    def write_enhanced_results(self, results, output_dir):
        """Write enhanced results with metadata"""
        for category, entries in results.items():
            filename = os.path.join(output_dir, f"enhanced_{category}_extracts.md")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Enhanced {category.replace('_', ' ').title()} Extracts\n\n")
                f.write(f"Total entries: {len(entries)}\n\n")
                
                # Group by conversation
                by_conversation = defaultdict(list)
                for entry in entries:
                    by_conversation[entry["conversation_title"]].append(entry)
                
                for conv_title, conv_entries in by_conversation.items():
                    f.write(f"## From: {conv_title}\n\n")
                    for entry in conv_entries[:10]:  # Limit per conversation
                        f.write(f"**{entry['timestamp_str']}** ({entry['role']})\n\n")
                        f.write(f"{entry['content']}\n\n")
                        f.write("---\n\n")
            
            print(f"Wrote {len(entries)} enhanced entries to enhanced_{category}_extracts.md")
    
    def write_cross_references(self, cross_refs, output_dir):
        """Write cross-reference analysis"""
        filename = os.path.join(output_dir, "cross_reference_analysis.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Cross-Reference Analysis\n\n")
            f.write("This file shows connections between different categories of insights.\n\n")
            
            for category1, connections in cross_refs.items():
                f.write(f"## {category1.replace('_', ' ').title()} Connections\n\n")
                for category2, refs in connections.items():
                    if refs:
                        f.write(f"### Connected to {category2.replace('_', ' ').title()} ({len(refs)} connections)\n\n")
                        for ref in refs[:5]:  # Show top 5 connections
                            f.write(f"**Conversation:** {ref['conversation']}\n")
                            f.write(f"**Content:** {ref['entry1']['content'][:200]}...\n\n")
                            f.write("---\n\n")
        
        print(f"Generated cross-reference analysis in cross_reference_analysis.md")
    
    def write_timeline_analysis(self, timeline, output_dir):
        """Write timeline analysis"""
        filename = os.path.join(output_dir, "timeline_correlation.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Timeline Correlation Analysis\n\n")
            f.write("Chronological development of ideas and insights.\n\n")
            
            # Group by year/month
            by_period = defaultdict(list)
            for entry in timeline:
                try:
                    date = datetime.datetime.fromtimestamp(entry["timestamp"])
                    period = f"{date.year}-{date.month:02d}"
                    by_period[period].append(entry)
                except:
                    by_period["Unknown"].append(entry)
            
            for period, entries in sorted(by_period.items()):
                f.write(f"## {period}\n\n")
                
                # Count categories for this period
                category_counts = Counter(entry["category"] for entry in entries)
                f.write("### Category Distribution:\n")
                for category, count in category_counts.most_common():
                    f.write(f"- {category.replace('_', ' ').title()}: {count} insights\n")
                f.write("\n")
                
                # Show key insights
                f.write("### Key Insights:\n\n")
                for entry in entries[:10]:  # Top 10 for each period
                    f.write(f"**{entry['category'].replace('_', ' ').title()}:** {entry['content'][:150]}...\n\n")
                
                f.write("---\n\n")
        
        print(f"Generated timeline correlation in timeline_correlation.md")

def main():
    # Initialize the enhanced analyzer
    json_path = "../OpenAIExport/conversations.json"
    analyzer = EnhancedConversationAnalyzer(json_path)
    
    # Run enhanced analysis
    results, cross_refs, timeline = analyzer.analyze_conversations()
    
    print("\nEnhanced Analysis Complete!")
    print(f"Total categories analyzed: {len(results)}")
    print(f"Cross-references found: {sum(len(refs) for refs in cross_refs.values())}")
    print(f"Timeline entries: {len(timeline)}")

if __name__ == "__main__":
    main()
