import json
import os
import re
import datetime
from collections import defaultdict

class OptimizedEnhancedAnalyzer:
    """
    Optimized version with progress tracking and memory efficiency
    """
    
    def __init__(self, json_path):
        self.json_path = json_path
        self.conversations = None
        self.load_conversations()
        
        # Focused categories to avoid overwhelming processing
        self.categories = {
            "uml_calculator": [
                "UML Calculator", "Universal Mathematical Language", "UML", "mathematical", 
                "symbolic", "equation", "dimensional", "operator", "calculation"
            ],
            "trees": [
                "T.R.E.E.S", "Recursive Entropy Engine", "RIS", "recursive", "recursion", 
                "entropy", "memory gravity", "recursive system"
            ],
            "nova_ai": [
                "Nova AI", "Nova", "Archive", "Builder", "Child", "Architect", 
                "memory system", "AI system"
            ],
            "blackwall": [
                "Blackwall", "BlackwallV2", "Lyra", "biomimetic", "emotional", 
                "personality", "emotional processing"
            ],
            "personal": [
                "personal", "life", "family", "experience", "childhood", "marriage", 
                "trauma", "education", "career"
            ],
            "technical": [
                "implementation", "architecture", "system", "framework", "code", 
                "technical", "development"
            ],
            "philosophy": [
                "consciousness", "ethics", "philosophy", "meaning", "existence", 
                "intelligence", "morality"
            ],
            "creative": [
                "creative", "creativity", "innovation", "design", "vision", 
                "inspiration", "art"
            ],
            "scientific": [
                "research", "hypothesis", "theory", "validation", "experiment", 
                "scientific", "methodology"
            ]
        }
        
    def load_conversations(self):
        """Load conversations from JSON"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.conversations = json.load(file)
                print(f"✓ Loaded {len(self.conversations)} conversations")
        except Exception as e:
            print(f"✗ Error loading conversations: {e}")
            self.conversations = []
            
    def extract_messages(self, conversation):
        """Extract messages efficiently"""
        messages = []
        
        if "mapping" in conversation:
            for value in conversation["mapping"].values():
                if (value and "message" in value and value["message"] and 
                    "content" in value["message"] and "parts" in value["message"]["content"]):
                    
                    for part in value["message"]["content"]["parts"]:
                        if isinstance(part, str) and len(part.strip()) > 20:  # Filter short messages
                            messages.append({
                                "content": part,
                                "timestamp": conversation.get("create_time", 0),
                                "role": value["message"].get("author", {}).get("role", "unknown")
                            })
        
        return messages[:10]  # Limit to first 10 messages per conversation for efficiency
    
    def categorize_content_fast(self, content):
        """Fast categorization using simple string matching"""
        found_categories = []
        content_lower = content.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    found_categories.append(category)
                    break  # Only need one match per category
                    
        return found_categories
    
    def extract_quotes_fast(self, content):
        """Fast quote extraction"""
        # Split into sentences and take meaningful ones
        sentences = re.split(r'[.!?]', content)
        quotes = []
        
        for sentence in sentences[:5]:  # Only check first 5 sentences
            sentence = sentence.strip()
            if (30 <= len(sentence) <= 200 and  # Reasonable length
                sentence and sentence[0].isupper() and 
                "system:" not in sentence.lower()):
                quotes.append(sentence + ".")
                if len(quotes) >= 2:  # Limit to 2 quotes per message
                    break
        
        return quotes
    
    def analyze_conversations_optimized(self, output_dir="../Conversations"):
        """Optimized analysis with progress tracking"""
        if not self.conversations:
            print("✗ No conversations to analyze")
            return
            
        results = defaultdict(list)
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n📊 Processing {len(self.conversations)} conversations...")
        
        # Process conversations in batches
        batch_size = 10
        for batch_start in range(0, len(self.conversations), batch_size):
            batch_end = min(batch_start + batch_size, len(self.conversations))
            print(f"Processing batch {batch_start//batch_size + 1}/{(len(self.conversations) + batch_size - 1)//batch_size} (conversations {batch_start+1}-{batch_end})")
            
            for idx in range(batch_start, batch_end):
                conversation = self.conversations[idx]
                title = conversation.get("title", f"Conversation-{idx}")
                create_time = conversation.get("create_time", 0)
                
                # Convert timestamp
                try:
                    timestamp_str = datetime.datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S") if create_time else "Unknown"
                except:
                    timestamp_str = "Unknown"
                
                messages = self.extract_messages(conversation)
                
                for msg in messages:
                    content = msg["content"]
                    categories = self.categorize_content_fast(content)
                    quotes = self.extract_quotes_fast(content)
                    
                    for quote in quotes:
                        for category in categories:
                            results[category].append({
                                "content": quote,
                                "conversation_title": title,
                                "timestamp": create_time,
                                "timestamp_str": timestamp_str,
                                "role": msg.get("role", "unknown")
                            })
        
        # Write results
        print("\n💾 Writing results...")
        for category, entries in results.items():
            filename = os.path.join(output_dir, f"optimized_{category}_extracts.md")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Optimized {category.replace('_', ' ').title()} Extracts\n\n")
                f.write(f"Total entries: {len(entries)}\n\n")
                
                # Sort by timestamp and group by conversation
                entries.sort(key=lambda x: x["timestamp"])
                
                current_conv = None
                for entry in entries:
                    if entry["conversation_title"] != current_conv:
                        current_conv = entry["conversation_title"]
                        f.write(f"## From: {current_conv}\n\n")
                    
                    f.write(f"**{entry['timestamp_str']}** ({entry['role']})\n\n")
                    f.write(f"{entry['content']}\n\n")
                    f.write("---\n\n")
            
            print(f"✓ Wrote {len(entries)} entries to optimized_{category}_extracts.md")
        
        return results

def main():
    json_path = "../OpenAIExport/conversations.json"
    analyzer = OptimizedEnhancedAnalyzer(json_path)
    
    print("🚀 Starting Optimized Enhanced Analysis...")
    results = analyzer.analyze_conversations_optimized()
    
    print(f"\n✅ Analysis Complete!")
    print(f"📈 Total categories: {len(results)}")
    total_entries = sum(len(entries) for entries in results.values())
    print(f"📝 Total entries extracted: {total_entries:,}")

if __name__ == "__main__":
    main()
