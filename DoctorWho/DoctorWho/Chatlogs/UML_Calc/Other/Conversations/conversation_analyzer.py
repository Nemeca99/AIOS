import json
import os
import re
import datetime

class ConversationAnalyzer:
    """
    A class to analyze the OpenAI conversation exports and extract useful information
    """
    
    def __init__(self, json_path):
        """Initialize the analyzer with the path to the JSON export file"""
        self.json_path = json_path
        self.conversations = None
        self.load_conversations()
        
        # Categories to track with expanded search terms
        self.categories = {
            "uml_calculator": ["UML Calculator", "Universal Mathematical Language", "Calculator", "UML", "framework", 
                             "mathematics", "mathematical language", "symbolic", "equation", "fractal", "formula", 
                             "dimensional", "collapse", "operator"],
            "trees": ["T.R.E.E.S", "Recursive Entropy Engine", "RIS", "Recursive", "recursion", "emergent", "emergence", 
                    "entropy", "hive logic", "paradox field", "memory gravity", "heat compression", "firewall", 
                    "recursive self-classified intelligence", "temporal entanglement"],
            "nova_ai": ["Nova AI", "Nova", "Archive", "memory system", "Child", "Builder", "Architect", "whisper", "echoe", 
                      "shadow ai", "ghost brain", "shadow logic", "memory compression", "symbolic storage", "language kernel"],
            "blackwall": ["Blackwall", "BlackwallV2", "Lyra", "biomimetic", "personality", "emotions", "emotional", 
                        "recursive personality layering", "emotional encoding", "interface layer"],
            "personal": ["personal", "childhood", "marriage", "trauma", "biography", "life", "family", "kids", "education", 
                       "job", "money", "work", "career", "growing up", "school", "college", "university", "relationship"],
            "technical": ["architecture", "implementation", "code", "system design", "framework", "jarvis", "star trek", 
                        "memory structure", "language collapse", "containment", "thermodynamics", "recursive game theory", 
                        "logic shells", "error states", "recursive debugging"],
            "philosophy": ["morality", "ethics", "consciousness", "sentience", "philosophy", "existence", "meaning", "purpose", 
                         "free will", "identity", "self", "emergent consciousness", "emergent intelligence", "recursive intelligence"]
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
        if "mapping" in conversation:
            for node_id, node in conversation["mapping"].items():
                if "message" in node and node["message"]:
                    message = node["message"]
                    if "content" in message and "parts" in message["content"]:
                        author = message["author"]["role"]
                        content = " ".join([part for part in message["content"]["parts"] if isinstance(part, str)])
                        create_time = message.get("create_time")
                        if create_time:
                            try:
                                timestamp = datetime.datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                            except (OSError, ValueError):
                                timestamp = "Invalid timestamp"
                        else:
                            timestamp = "Unknown"
                        
                        messages.append({
                            "author": author,
                            "content": content,
                            "timestamp": timestamp
                        })
        return messages
    
    def categorize_message(self, message):
        """Categorize a message based on keywords"""
        categories = []
        content = message["content"].lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in content:
                    categories.append(category)
                    break
        
        # Look for advanced patterns
        advanced_patterns = self.find_advanced_patterns(content)
        categories.extend(advanced_patterns)
        
        return list(set(categories))  # Remove duplicates
    
    def find_advanced_patterns(self, content):
        """Find more complex patterns in the content"""
        patterns = {
            "personal": [
                r'(?i)(?:travis|i|he)(?:\s\w+){1,5}\s(?:grew up|was raised|experienced|suffered|overcame|developed|learned)',
                r'(?i)(?:childhood|early life|family|growing up|school|college|education)(?:\s\w+){1,5}\s(?:was|became|led to)',
                r'(?i)(?:marriage|relationship|partner|spouse|divorce|separation)(?:\s\w+){1,5}',
                r'(?i)(?:job|career|profession|work|money|finance|income)(?:\s\w+){1,5}\s(?:involved|consisted|provided|allowed)',
                r'(?i)(?:family|children|kids|parents|siblings)(?:\s\w+){1,5}\s(?:influenced|affected|shaped|taught|supported)'
            ],
            "trees": [
                r'(?i)recursive(?:\s\w+){1,5}\s(?:system|model|theory|framework|approach|logic|structure)',
                r'(?i)t\.r\.e\.e\.s\.(?:\s\w+){0,10}\s(?:was developed|is based on|functions|works|operates)',
                r'(?i)(?:entropy|recursion|ris)(?:\s\w+){1,5}\s(?:principle|theory|concept|foundation)'
            ],
            "uml_calculator": [
                r'(?i)(?:uml|calculator)(?:\s\w+){1,5}\s(?:calculates|computes|solves|processes|works by)',
                r'(?i)universal mathematical language(?:\s\w+){1,10}',
                r'(?i)mathematical(?:\s\w+){1,3}\s(?:framework|system|language|approach)'
            ],
            "nova_ai": [
                r'(?i)(?:nova|archive|builder|child|architect)(?:\s\w+){1,5}\s(?:ai|system|architecture|framework)',
                r'(?i)memory(?:\s\w+){1,5}\s(?:system|storage|retrieval|processing)',
                r'(?i)(?:whisper|echoe)(?:\s\w+){0,5}\s(?:module|component|system|interface)'
            ],
            "blackwall": [
                r'(?i)blackwall(?:\s\w+){0,10}\s(?:system|architecture|process|handles|manages)',
                r'(?i)biomimetic(?:\s\w+){1,5}\s(?:design|structure|system|approach)',
                r'(?i)emotional(?:\s\w+){1,5}\s(?:processing|handling|management|response)'
            ],
            "philosophy": [
                r'(?i)(?:morality|ethics|consciousness)(?:\s\w+){1,5}\s(?:framework|system|approach|theory)',
                r'(?i)(?:meaning|purpose|existence)(?:\s\w+){1,10}',
                r'(?i)philosophical(?:\s\w+){1,5}\s(?:foundation|basis|principle)'
            ],
            "timeline": [
                r'(?i)(?:developed|created|implemented|built|designed)(?:\s\w+){1,10}\s(?:in|during|on|at)\s(?:20\d{2}|\w+ 20\d{2})',
                r'(?i)(?:version|release|milestone|phase)(?:\s\w+){1,5}\s(?:was|became|occurred|happened)',
                r'(?i)(?:first|initial|early|latest)(?:\s\w+){1,3}\s(?:version|implementation|design|prototype)'
            ]
        }
        
        found_categories = []
        
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                if re.search(pattern, content):
                    found_categories.append(category)
                    break
        
        return found_categories
    
    def extract_quotes(self, content):
        """Extract potential quotes from a message content"""
        quotes = []
        
        # Look for quotes in various formats - simplified for performance
        quote_patterns = [
            r'"([^"]{20,300})"',  # Text in double quotes
            r"'([^']{20,300})'"   # Text in single quotes
        ]
        
        for pattern in quote_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) >= 20 and "system: " not in match.lower():
                    quotes.append(match.strip())
        
        # Extract sentences
        sentences = re.split(r'[.!?]', content)
        for sentence in sentences[:10]:  # Limit to first 10 sentences for performance
            sentence = sentence.strip()
            if len(sentence) >= 20 and sentence and sentence[0].isupper() and "system: " not in sentence.lower():
                quotes.append(sentence + ".")
        
        return quotes[:5]  # Limit to 5 quotes per message for performance
    
    def analyze_conversations(self, output_dir):
        """Analyze conversations and extract useful information"""
        if not self.conversations:
            print("No conversations to analyze.")
            return
            
        results = {
            "uml_calculator": [],
            "trees": [],
            "nova_ai": [],
            "blackwall": [],
            "personal": [],
            "technical": [],
            "philosophy": [],
            "timeline": []
        }
        
        # Create directory for the results
        os.makedirs(output_dir, exist_ok=True)
        
        # Process each conversation
        for idx, conversation in enumerate(self.conversations):
            print(f"Processing conversation {idx+1}/{len(self.conversations)}")
            
            # Extract conversation title or ID
            title = conversation.get("title", f"Conversation-{idx}")
            
            # Extract messages
            messages = self.extract_messages(conversation)
            
            # Process each message
            for msg in messages:
                if msg["author"] != "user":  # Only process assistant messages
                    continue
                    
                # Categorize message
                categories = self.categorize_message(msg)
                
                # Extract quotes
                quotes = self.extract_quotes(msg["content"])
                
                # Store categorized quotes
                for category in categories:
                    if category in results:
                        for quote in quotes:
                            results[category].append({
                                "quote": quote,
                                "conversation": title,
                                "timestamp": msg["timestamp"]
                            })
                
                # Check for timeline entries (development milestones)
                if any(word in msg["content"].lower() for word in ["developed", "created", "implemented", "milestone", "version"]):
                    results["timeline"].append({
                        "entry": msg["content"][:300] + "..." if len(msg["content"]) > 300 else msg["content"],
                        "conversation": title,
                        "timestamp": msg["timestamp"]
                    })
        
        # Write results to files
        for category, entries in results.items():
            if entries:
                with open(os.path.join(output_dir, f"{category}_extracts.md"), 'w', encoding='utf-8') as f:
                    f.write(f"# {category.replace('_', ' ').title()} Extracts\n\n")
                    f.write(f"Total entries: {len(entries)}\n\n")
                    
                    for entry in entries:
                        f.write(f"## From: {entry['conversation']} ({entry['timestamp']})\n\n")
                        f.write(f"{entry['quote'] if 'quote' in entry else entry['entry']}\n\n")
                        f.write("---\n\n")
                
                print(f"Wrote {len(entries)} entries to {category}_extracts.md")
        
        return results

def main():
    """Main function to run the analyzer"""
    json_path = r"D:\UML Calculator\OpenAIExport\conversations.json"
    output_dir = r"D:\UML Calculator\Conversations"
    
    analyzer = ConversationAnalyzer(json_path)
    results = analyzer.analyze_conversations(output_dir)
    
    print("Analysis complete. Results saved to the Conversations directory.")

if __name__ == "__main__":
    main()
