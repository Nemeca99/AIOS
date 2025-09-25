import os
import re

def count_entries(file_path):
    """Count the number of entries in a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            entries = re.findall(r'## From:', content)
            return len(entries)
    except Exception:
        return 0

def generate_report():
    """Generate a report of extracted insights"""
    base_dir = r"D:\UML Calculator\Conversations"
    
    # Define categories
    categories = [
        "uml_calculator",
        "trees",
        "nova_ai",
        "blackwall",
        "personal",
        "technical",
        "timeline"
    ]
    
    # Print report header
    print("\n" + "="*50)
    print(" "*15 + "CONVERSATION ANALYSIS REPORT")
    print("="*50 + "\n")
    
    # Check if files exist and count entries
    total_entries = 0
    has_files = False
    
    for category in categories:
        file_path = os.path.join(base_dir, f"{category}_extracts.md")
        if os.path.exists(file_path):
            entries = count_entries(file_path)
            total_entries += entries
            print(f"{category.replace('_', ' ').title():20} : {entries:5} entries")
            has_files = True
        else:
            print(f"{category.replace('_', ' ').title():20} : File not found")
    
    print("\n" + "-"*50)
    print(f"{'Total':20} : {total_entries:5} entries")
    print("-"*50 + "\n")
    
    if not has_files:
        print("No extract files found. Run conversation_analyzer.py first.")
    elif total_entries == 0:
        print("No entries found in extract files. Check the analyzer settings.")
    else:
        print("Next steps:")
        print("1. Review the extracted insights in the markdown files")
        print("2. Use insights_viewer.html for interactive exploration")
        print("3. Run integrate_insights.bat to add insights to documentation")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    generate_report()
