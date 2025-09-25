import os
import re
from datetime import datetime

def read_file(file_path):
    """Read a markdown file and return its content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def write_file(file_path, content):
    """Write content to a markdown file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated {file_path}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def extract_quotes(file_path):
    """Extract quotes from a markdown file"""
    content = read_file(file_path)
    quotes = []
    
    # Extract sections
    sections = re.findall(r'## From:.*?\n\n(.*?)\n\n---', content, re.DOTALL)
    
    for section in sections:
        quotes.append(section.strip())
    
    return quotes

def integrate_insights():
    """Integrate extracted insights into documentation files"""
    base_dir = r"D:\UML Calculator"
    extracts_dir = os.path.join(base_dir, "Conversations")
    
    # Define mapping between extract files and documentation files
    mappings = {
        "personal_extracts.md": "Travis_Miner_Biography.md",
        "nova_ai_extracts.md": "Nova_AI_Documentation.md",
        "blackwall_extracts.md": "BlackwallV2_System_Architecture.md",
        "trees_extracts.md": "T.R.E.E.S.md",
        "uml_calculator_extracts.md": "Calculator_Summary.md"
    }
    
    for extract_file, doc_file in mappings.items():
        extract_path = os.path.join(extracts_dir, extract_file)
        doc_path = os.path.join(base_dir, doc_file)
        
        if not os.path.exists(extract_path):
            print(f"Extract file not found: {extract_path}")
            continue
            
        if not os.path.exists(doc_path):
            print(f"Documentation file not found: {doc_path}")
            continue
            
        quotes = extract_quotes(extract_path)
        if not quotes:
            print(f"No quotes found in {extract_file}")
            continue
            
        doc_content = read_file(doc_path)
        
        # Create a new section for conversation insights
        insights_section = f"""
## Conversation Insights
*Added on {datetime.now().strftime('%Y-%m-%d')}*

The following insights were automatically extracted from conversation history:

"""
        
        # Add top 5 quotes (or fewer if less are available)
        for i, quote in enumerate(quotes[:5]):
            insights_section += f"### Insight {i+1}\n\n{quote}\n\n"
            
        # Create a backup of the original file
        backup_path = doc_path + f".backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        write_file(backup_path, doc_content)
        
        # Add the insights section to the end of the document
        doc_content += insights_section
        write_file(doc_path, doc_content)
        
        print(f"Added {min(5, len(quotes))} insights to {doc_file} (backup saved as {os.path.basename(backup_path)})")

def main():
    """Main function"""
    print("This script will integrate extracted insights into the documentation files.")
    print("Make sure you have run conversation_analyzer.py first to generate the extracts.")
    print("Backups of the original files will be created before any changes are made.")
    proceed = input("Do you want to proceed? (y/n): ")
    
    if proceed.lower() == "y":
        integrate_insights()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
