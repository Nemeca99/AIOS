import json
import os
import re
import datetime
from collections import defaultdict, Counter

class TimelineCorrelationAnalyzer:
    """
    Tool to analyze the timeline of idea development and show correlations
    """
    
    def __init__(self, json_path="../OpenAIExport/conversations.json"):
        self.json_path = json_path
        self.conversations = None
        self.load_conversations()
        
    def load_conversations(self):
        """Load conversations from JSON"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.conversations = json.load(file)
                print(f"Successfully loaded {len(self.conversations)} conversations for timeline analysis.")
        except FileNotFoundError:
            print(f"Error: Could not find {self.json_path}")
            self.conversations = []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.json_path}")
            self.conversations = []
    
    def extract_timeline_data(self):
        """Extract timeline data from conversations"""
        timeline_data = []
        
        for idx, conversation in enumerate(self.conversations):
            title = conversation.get("title", f"Conversation-{idx}")
            create_time = conversation.get("create_time", 0)
            update_time = conversation.get("update_time", create_time)
            
            # Convert timestamps
            try:
                create_date = datetime.datetime.fromtimestamp(create_time) if create_time else None
                update_date = datetime.datetime.fromtimestamp(update_time) if update_time else None
            except (ValueError, OSError):
                create_date = None
                update_date = None
            
            # Extract key concepts from title and content
            concepts = self.extract_concepts_from_conversation(conversation)
            
            timeline_data.append({
                "title": title,
                "create_time": create_time,
                "update_time": update_time,
                "create_date": create_date,
                "update_date": update_date,
                "concepts": concepts,
                "conversation_id": idx
            })
        
        # Sort by creation time
        timeline_data.sort(key=lambda x: x['create_time'] if x['create_time'] else 0)
        return timeline_data
    
    def extract_concepts_from_conversation(self, conversation):
        """Extract key concepts from a conversation"""
        concepts = set()
        
        # Concept patterns to look for
        concept_patterns = {
            "uml_calculator": [r"UML", r"Universal Mathematical Language", r"Calculator", r"mathematical", r"symbolic"],
            "trees": [r"T\.R\.E\.E\.S", r"recursive", r"entropy", r"RIS", r"recursion"],
            "nova_ai": [r"Nova", r"Archive", r"Builder", r"Child", r"Architect", r"memory system"],
            "blackwall": [r"Blackwall", r"BlackwallV2", r"Lyra", r"biomimetic", r"emotional"],
            "philosophy": [r"consciousness", r"ethics", r"morality", r"philosophy", r"meaning"],
            "technical": [r"implementation", r"architecture", r"system", r"framework"],
            "personal": [r"personal", r"life", r"experience", r"family", r"trauma", r"marriage"],
            "scientific": [r"research", r"theory", r"hypothesis", r"proof", r"validation"],
            "creative": [r"creative", r"innovation", r"design", r"art", r"vision"],
            "practical": [r"application", r"real-world", r"practical", r"implementation"]
        }
        
        # Get conversation text
        conv_text = self.get_conversation_text(conversation)
        
        # Find concepts
        for category, patterns in concept_patterns.items():
            for pattern in patterns:
                if re.search(pattern, conv_text, re.IGNORECASE):
                    concepts.add(category)
                    break
        
        return list(concepts)
    
    def get_conversation_text(self, conversation):
        """Extract all text from a conversation"""
        text_parts = []
        
        # Add title
        if "title" in conversation:
            text_parts.append(conversation["title"])
        
        # Extract message content
        if "mapping" in conversation:
            for value in conversation["mapping"].values():
                if value and "message" in value and value["message"]:
                    message_data = value["message"]
                    if "content" in message_data and "parts" in message_data["content"]:
                        for part in message_data["content"]["parts"]:
                            if isinstance(part, str):
                                text_parts.append(part)
        
        return " ".join(text_parts)
    
    def analyze_concept_evolution(self, timeline_data):
        """Analyze how concepts evolved over time"""
        evolution_data = defaultdict(list)
        
        for entry in timeline_data:
            if entry['create_date']:
                for concept in entry['concepts']:
                    evolution_data[concept].append({
                        "date": entry['create_date'],
                        "title": entry['title'],
                        "conversation_id": entry['conversation_id']
                    })
        
        # Calculate concept introduction dates and frequency over time
        concept_stats = {}
        for concept, occurrences in evolution_data.items():
            if occurrences:
                first_appearance = min(occ['date'] for occ in occurrences)
                last_appearance = max(occ['date'] for occ in occurrences)
                concept_stats[concept] = {
                    "first_appearance": first_appearance,
                    "last_appearance": last_appearance,
                    "total_conversations": len(occurrences),
                    "occurrences": occurrences
                }
        
        return evolution_data, concept_stats
    
    def find_concept_correlations(self, timeline_data):
        """Find concepts that tend to appear together"""
        correlations = defaultdict(lambda: defaultdict(int))
        concept_pairs = defaultdict(int)
        
        for entry in timeline_data:
            concepts = entry['concepts']
            # Count co-occurrences
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    pair = tuple(sorted([concept1, concept2]))
                    concept_pairs[pair] += 1
                    correlations[concept1][concept2] += 1
                    correlations[concept2][concept1] += 1
        
        return dict(correlations), dict(concept_pairs)
    
    def analyze_development_phases(self, timeline_data):
        """Identify distinct phases in development based on concept clusters"""
        if not timeline_data or not any(entry['create_date'] for entry in timeline_data):
            return []
        
        # Group by time periods (months)
        monthly_concepts = defaultdict(lambda: defaultdict(int))
        
        for entry in timeline_data:
            if entry['create_date']:
                month_key = entry['create_date'].strftime("%Y-%m")
                for concept in entry['concepts']:
                    monthly_concepts[month_key][concept] += 1
        
        # Identify phases based on dominant concepts
        phases = []
        for month, concepts in sorted(monthly_concepts.items()):
            if concepts:
                dominant_concepts = sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:3]
                phases.append({
                    "period": month,
                    "dominant_concepts": dominant_concepts,
                    "total_conversations": sum(concepts.values()),
                    "concept_diversity": len(concepts)
                })
        
        return phases
    
    def generate_timeline_report(self, output_file="timeline_correlation_report.md"):
        """Generate comprehensive timeline correlation report"""
        print("Extracting timeline data...")
        timeline_data = self.extract_timeline_data()
        
        print("Analyzing concept evolution...")
        evolution_data, concept_stats = self.analyze_concept_evolution(timeline_data)
        
        print("Finding concept correlations...")
        correlations, concept_pairs = self.find_concept_correlations(timeline_data)
        
        print("Analyzing development phases...")
        phases = self.analyze_development_phases(timeline_data)
        
        # Generate report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Timeline Correlation Analysis Report\n\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overview
            f.write("## Overview\n\n")
            valid_dates = [entry for entry in timeline_data if entry['create_date']]
            if valid_dates:
                earliest = min(entry['create_date'] for entry in valid_dates)
                latest = max(entry['create_date'] for entry in valid_dates)
                f.write(f"- Analysis period: {earliest.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}\n")
                f.write(f"- Total conversations: {len(timeline_data)}\n")
                f.write(f"- Conversations with valid dates: {len(valid_dates)}\n")
                f.write(f"- Total concepts tracked: {len(concept_stats)}\n\n")
            else:
                f.write("- No conversations with valid timestamps found\n\n")
            
            # Concept evolution
            f.write("## Concept Evolution Timeline\n\n")
            if concept_stats:
                for concept, stats in sorted(concept_stats.items(), key=lambda x: x[1]['first_appearance']):
                    f.write(f"### {concept.replace('_', ' ').title()}\n\n")
                    f.write(f"- **First appearance**: {stats['first_appearance'].strftime('%Y-%m-%d')}\n")
                    f.write(f"- **Last appearance**: {stats['last_appearance'].strftime('%Y-%m-%d')}\n")
                    f.write(f"- **Total conversations**: {stats['total_conversations']}\n")
                    
                    # Show key conversations
                    f.write("- **Key conversations**:\n")
                    for occ in sorted(stats['occurrences'], key=lambda x: x['date'])[:5]:
                        f.write(f"  - {occ['date'].strftime('%Y-%m-%d')}: {occ['title']}\n")
                    f.write("\n")
            
            # Development phases
            f.write("## Development Phases\n\n")
            if phases:
                for phase in phases:
                    f.write(f"### {phase['period']}\n\n")
                    f.write(f"- **Total conversations**: {phase['total_conversations']}\n")
                    f.write(f"- **Concept diversity**: {phase['concept_diversity']} different concepts\n")
                    f.write("- **Dominant concepts**:\n")
                    for concept, count in phase['dominant_concepts']:
                        f.write(f"  - {concept.replace('_', ' ').title()}: {count} mentions\n")
                    f.write("\n")
            
            # Concept correlations
            f.write("## Concept Correlations\n\n")
            f.write("Concepts that frequently appear together in conversations:\n\n")
            
            # Sort concept pairs by frequency
            top_pairs = sorted(concept_pairs.items(), key=lambda x: x[1], reverse=True)[:15]
            for (concept1, concept2), count in top_pairs:
                f.write(f"- **{concept1.replace('_', ' ').title()}** + **{concept2.replace('_', ' ').title()}**: {count} conversations\n")
            f.write("\n")
            
            # Individual concept correlation networks
            f.write("## Concept Networks\n\n")
            for concept, connections in sorted(correlations.items()):
                if connections:
                    f.write(f"### {concept.replace('_', ' ').title()} Network\n\n")
                    sorted_connections = sorted(connections.items(), key=lambda x: x[1], reverse=True)[:5]
                    for connected_concept, count in sorted_connections:
                        f.write(f"- Connected to **{connected_concept.replace('_', ' ').title()}**: {count} shared conversations\n")
                    f.write("\n")
        
        print(f"Timeline correlation report generated: {output_file}")
        return timeline_data, concept_stats, phases, correlations

def main():
    analyzer = TimelineCorrelationAnalyzer()
    timeline_data, concept_stats, phases, correlations = analyzer.generate_timeline_report()
    
    print("\nTimeline Correlation Analysis Complete!")
    print(f"Analyzed {len(timeline_data)} conversations")
    print(f"Tracked {len(concept_stats)} concepts")
    print(f"Identified {len(phases)} development phases")

if __name__ == "__main__":
    main()
