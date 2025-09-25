"""
Documentation Cleanup Script

This script moves or archives original documentation files that have been consolidated
into new comprehensive documentation.
"""

import os
import shutil
from datetime import datetime

# Define source documentation files that have been consolidated
CONSOLIDATED_FILES = {
    "BlackwallV2_System_Architecture.md": "System Architecture",
    "T.R.E.E.S.md": "System Architecture",
    "BlackwallV2_TREES_Relationship_Fixed.md": "System Architecture",
    "Calculator_Summary.md": "UML Calculator and Nova AI",
    "Nova_AI_Documentation.md": "UML Calculator and Nova AI",
    "Travis_Miner_Biography.md": "Travis Miner Biography",
    "UML_Calculator_Manual.md": "Technical Reference",
    "UML_Calculator_Quick_Reference.md": "Technical Reference", 
    "UML_Calculator_User_Guide.md": "Technical Reference"
}

def create_archive_dir():
    """Create an archive directory for the original files."""
    archive_dir = os.path.join("d:", "UML Calculator", "docs", "archive")
    
    # Create archive directory if it doesn't exist
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Created archive directory: {archive_dir}")
    
    return archive_dir

def archive_files():
    """Archive the original documentation files."""
    archive_dir = create_archive_dir()
    housekeeping_dir = os.path.join("d:", "UML Calculator", "Housekeeping")
    
    # Check if the Housekeeping directory exists
    if not os.path.exists(housekeeping_dir):
        print(f"ERROR: Housekeeping directory not found at {housekeeping_dir}")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a timestamp subdirectory in the archive
    timestamp_dir = os.path.join(archive_dir, timestamp)
    os.makedirs(timestamp_dir)
    
    # Move each consolidated file to the archive
    for filename in CONSOLIDATED_FILES:
        source_path = os.path.join(housekeeping_dir, filename)
        if os.path.exists(source_path):
            dest_path = os.path.join(timestamp_dir, filename)
            shutil.copy2(source_path, dest_path)
            print(f"Archived: {filename} → {dest_path}")
        else:
            print(f"WARNING: Source file not found: {source_path}")
    
    print(f"\nArchived original documentation to: {timestamp_dir}")
    print("Original files remain in their locations. To remove them after verifying the new documentation, run this script with the --remove flag.")

def remove_files():
    """Remove the original documentation files after confirming."""
    housekeeping_dir = os.path.join("d:", "UML Calculator", "Housekeeping")
    
    print("\nWARNING: This will permanently remove the original documentation files.")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return
    
    # Remove each consolidated file
    for filename in CONSOLIDATED_FILES:
        source_path = os.path.join(housekeeping_dir, filename)
        if os.path.exists(source_path):
            os.remove(source_path)
            print(f"Removed: {source_path}")
        else:
            print(f"WARNING: File not found: {source_path}")
    
    print("\nOriginal documentation files have been removed.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        remove_files()
    else:
        archive_files()
        print("\nRun with --remove flag to delete original files after verifying the consolidated documentation:")
        print("python docs/cleanup_documentation.py --remove")
