"""
Documentation Analysis Tool

This script identifies documentation files in the workspace and suggests
potential candidates for consolidation based on content similarity.
"""

import os
import re
import glob
import difflib
from collections import defaultdict

def find_markdown_files(root_dir):
    """Find all markdown files in the given directory and subdirectories."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, filename))
    return markdown_files

def extract_title(file_path):
    """Extract the title from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for a title in the format # Title
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()
            # If no title found, use the filename
            return os.path.basename(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return os.path.basename(file_path)

def calculate_content_similarity(file1, file2):
    """Calculate content similarity between two files."""
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            content1 = f1.read()
            content2 = f2.read()
            
            # Remove markdown formatting for better comparison
            content1 = re.sub(r'[#\*\[\]\(\)`]', '', content1)
            content2 = re.sub(r'[#\*\[\]\(\)`]', '', content2)
            
            # Calculate similarity ratio
            similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
            return similarity
    except Exception as e:
        print(f"Error comparing {file1} and {file2}: {e}")
        return 0.0

def group_by_topic(files):
    """Group files by topic based on filename patterns."""
    topics = defaultdict(list)
    
    # Define topic patterns
    patterns = {
        'UML Calculator': r'calc|uml|mathematical',
        'BlackwallV2': r'blackwall|system|architecture',
        'T.R.E.E.S': r'tree|recursive',
        'Nova AI': r'nova|ai',
        'Travis Miner': r'travis|miner|biography',
        'Integration': r'integrat|relationship',
        'Technical': r'technical|manual|guide|reference'
    }
    
    for file_path in files:
        file_name = os.path.basename(file_path).lower()
        assigned = False
        
        for topic, pattern in patterns.items():
            if re.search(pattern, file_name, re.IGNORECASE):
                topics[topic].append(file_path)
                assigned = True
                break
        
        if not assigned:
            topics['Other'].append(file_path)
    
    return topics

def find_consolidation_candidates(files, similarity_threshold=0.3):
    """Find files that could potentially be consolidated based on content similarity."""
    topics = group_by_topic(files)
    
    consolidation_candidates = []
    
    # For each topic, find files with similar content
    for topic, topic_files in topics.items():
        if len(topic_files) <= 1:
            continue
            
        for i in range(len(topic_files)):
            for j in range(i+1, len(topic_files)):
                file1 = topic_files[i]
                file2 = topic_files[j]
                
                similarity = calculate_content_similarity(file1, file2)
                
                if similarity >= similarity_threshold:
                    consolidation_candidates.append({
                        'topic': topic,
                        'file1': file1,
                        'file2': file2,
                        'similarity': similarity,
                        'title1': extract_title(file1),
                        'title2': extract_title(file2)
                    })
    
    return consolidation_candidates

def main():
    """Main function."""
    # Path to the workspace root (parent of the docs directory)
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    
    print(f"Analyzing documentation in: {workspace_root}")
    
    # Find all markdown files
    markdown_files = find_markdown_files(workspace_root)
    print(f"Found {len(markdown_files)} markdown files.")
    
    # Exclude files in the docs directory (already consolidated)
    consolidated_docs_dir = os.path.join(workspace_root, 'docs')
    markdown_files = [f for f in markdown_files if not f.startswith(consolidated_docs_dir)]
    print(f"Analyzing {len(markdown_files)} files (excluding already consolidated docs).")
    
    # Group files by topic
    topics = group_by_topic(markdown_files)
    print("\nFiles by topic:")
    for topic, files in topics.items():
        print(f"\n{topic} ({len(files)} files):")
        for file_path in files:
            print(f"  - {os.path.basename(file_path)} ({extract_title(file_path)})")
    
    # Find consolidation candidates
    candidates = find_consolidation_candidates(markdown_files)
    candidates.sort(key=lambda x: x['similarity'], reverse=True)
    
    print("\nConsolidation candidates (by similarity):")
    for candidate in candidates:
        print(f"\nTopic: {candidate['topic']} (Similarity: {candidate['similarity']:.2f})")
        print(f"  - {os.path.basename(candidate['file1'])}: {candidate['title1']}")
        print(f"  - {os.path.basename(candidate['file2'])}: {candidate['title2']}")
    
    # Generate consolidation suggestions
    print("\nConsolidation suggestions by topic:")
    for topic, files in topics.items():
        if len(files) <= 1:
            continue
            
        print(f"\n{topic} ({len(files)} files):")
        titles = [f"{os.path.basename(f)} ({extract_title(f)})" for f in files]
        print(f"  Suggestion: Consider combining these files into a comprehensive {topic} document:")
        for title in titles:
            print(f"    - {title}")

if __name__ == "__main__":
    main()
