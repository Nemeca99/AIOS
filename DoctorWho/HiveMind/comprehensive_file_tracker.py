#!/usr/bin/env python3
"""
Comprehensive File Tracker for Luna Main Process
Tracks every single file that gets touched during execution using multiple methods
"""

import os
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List, Any
import tempfile
import glob

class ComprehensiveFileTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.touched_files = set()
        self.created_files = set()
        self.modified_files = set()
        self.accessed_files = set()
        self.directories_created = set()
        
    def start_tracking(self):
        """Start file tracking by recording initial state"""
        self.start_time = datetime.now()
        print(f"🔍 Starting comprehensive file tracking...")
        print(f"⏰ Started at: {self.start_time}")
        
        # Record initial state of common directories
        self._record_initial_state()
        
    def stop_tracking(self):
        """Stop tracking and analyze changes"""
        self.end_time = datetime.now()
        print(f"⏹️ File tracking stopped at: {self.end_time}")
        
        # Analyze changes
        self._analyze_changes()
        self._generate_comprehensive_report()
        
    def _record_initial_state(self):
        """Record initial state of files and directories"""
        # Common directories to monitor
        monitor_dirs = [
            ".",
            "AI_Core",
            "Data", 
            "logs",
            "AI_Core/Nova AI/AI/personality",
            "AI_Core/Nova AI/AI/personality/embedder_cache",
            "AI_Core/Nova AI/AI/personality/learning_results",
            "AI_Core/Nova AI/AI/personality/master_test_results"
        ]
        
        for dir_path in monitor_dirs:
            if os.path.exists(dir_path):
                self._scan_directory(dir_path)
                
    def _scan_directory(self, dir_path: str):
        """Scan directory for files"""
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.accessed_files.add(file_path)
        except Exception as e:
            print(f"⚠️ Error scanning {dir_path}: {e}")
            
    def _analyze_changes(self):
        """Analyze what files were created/modified during the process"""
        # Check for new files in common directories
        self._check_for_new_files()
        self._check_for_modified_files()
        
    def _check_for_new_files(self):
        """Check for files created during the process"""
        # Get current timestamp
        current_time = time.time()
        
        # Check common file patterns
        patterns = [
            "**/*.json",
            "**/*.log",
            "**/*.py", 
            "**/*.md",
            "**/*.txt",
            "**/*.db",
            "**/*.cache",
            "**/*.tmp"
        ]
        
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    # Check if file was created after start time
                    file_time = os.path.getctime(file_path)
                    if file_time > self.start_time.timestamp():
                        self.created_files.add(file_path)
                        self.touched_files.add(file_path)
                except Exception:
                    pass
                    
    def _check_for_modified_files(self):
        """Check for files modified during the process"""
        current_time = time.time()
        
        # Check common file patterns
        patterns = [
            "**/*.json",
            "**/*.log", 
            "**/*.py",
            "**/*.md",
            "**/*.txt",
            "**/*.db",
            "**/*.cache"
        ]
        
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    # Check if file was modified after start time
                    file_time = os.path.getmtime(file_path)
                    if file_time > self.start_time.timestamp():
                        self.modified_files.add(file_path)
                        self.touched_files.add(file_path)
                except Exception:
                    pass
                    
    def _generate_comprehensive_report(self):
        """Generate comprehensive file tracking report"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Categorize files
        categories = self._categorize_files()
        
        # Generate report
        report = {
            'tracking_info': {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat(),
                'duration_seconds': duration,
                'total_files_touched': len(self.touched_files),
                'files_created': len(self.created_files),
                'files_modified': len(self.modified_files),
                'files_accessed': len(self.accessed_files)
            },
            'file_categories': categories,
            'created_files': sorted(list(self.created_files)),
            'modified_files': sorted(list(self.modified_files)),
            'all_touched_files': sorted(list(self.touched_files))
        }
        
        # Save report
        report_file = f"comprehensive_file_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print(f"\n📊 COMPREHENSIVE FILE TRACKING REPORT")
        print(f"=" * 60)
        print(f"⏰ Duration: {duration:.2f} seconds")
        print(f"📁 Total files touched: {len(self.touched_files)}")
        print(f"🆕 Files created: {len(self.created_files)}")
        print(f"✏️ Files modified: {len(self.modified_files)}")
        print(f"👀 Files accessed: {len(self.accessed_files)}")
        
        print(f"\n📂 FILE CATEGORIES:")
        for category, files in categories.items():
            print(f"   {category}: {len(files)} files")
            
        print(f"\n💾 Report saved to: {report_file}")
        
        # Print critical files
        self._print_critical_files()
        
        # Print detailed file lists
        self._print_detailed_lists()
        
        return report
        
    def _categorize_files(self) -> Dict[str, List[str]]:
        """Categorize files by type"""
        categories = {
            'python_files': [],
            'json_files': [],
            'log_files': [],
            'cache_files': [],
            'data_files': [],
            'config_files': [],
            'personality_files': [],
            'carma_files': [],
            'other_files': []
        }
        
        for file_path in self.touched_files:
            if file_path.endswith('.py'):
                categories['python_files'].append(file_path)
            elif file_path.endswith('.json'):
                categories['json_files'].append(file_path)
                if 'personality' in file_path.lower():
                    categories['personality_files'].append(file_path)
                elif 'carma' in file_path.lower() or 'fractal' in file_path.lower():
                    categories['carma_files'].append(file_path)
            elif file_path.endswith('.log'):
                categories['log_files'].append(file_path)
            elif 'cache' in file_path.lower():
                categories['cache_files'].append(file_path)
            elif 'data' in file_path.lower() or file_path.endswith('.db'):
                categories['data_files'].append(file_path)
            elif file_path.endswith(('.yml', '.yaml', '.ini', '.cfg', '.conf')):
                categories['config_files'].append(file_path)
            else:
                categories['other_files'].append(file_path)
                
        return categories
        
    def _print_critical_files(self):
        """Print critical files status"""
        print(f"\n🔑 CRITICAL FILES STATUS:")
        
        critical_files = {
            'luna_main.py': 'Main Luna script',
            'luna_personality_dna.json': 'Luna personality DNA',
            'master_test_cache.json': 'RAG cache file',
            'luna_persistent_memory.json': 'Persistent memory',
            'hive_mind_logger.py': 'Logging system',
            'carma_core.py': 'CARMA core system',
            'fractal_mycelium_cache.py': 'Mycelium cache'
        }
        
        for filename, description in critical_files.items():
            found = [f for f in self.touched_files if filename in f]
            if found:
                print(f"   ✅ {filename}: {found[0]} ({description})")
            else:
                print(f"   ❌ {filename}: NOT FOUND ({description})")
                
    def _print_detailed_lists(self):
        """Print detailed file lists"""
        print(f"\n📋 DETAILED FILE LISTS:")
        
        # Created files
        if self.created_files:
            print(f"\n🆕 FILES CREATED:")
            for file_path in sorted(self.created_files):
                print(f"   📄 {file_path}")
                
        # Modified files
        if self.modified_files:
            print(f"\n✏️ FILES MODIFIED:")
            for file_path in sorted(self.modified_files):
                print(f"   📝 {file_path}")
                
        # All touched files
        print(f"\n👀 ALL FILES TOUCHED:")
        for file_path in sorted(self.touched_files):
            status = ""
            if file_path in self.created_files:
                status = " [CREATED]"
            elif file_path in self.modified_files:
                status = " [MODIFIED]"
            print(f"   📁 {file_path}{status}")

def run_luna_with_comprehensive_tracking(questions: int = 3, model: str = "text-embedding-mlabonne_qwen3-0.6b-abliterated"):
    """Run Luna with comprehensive file tracking"""
    
    # Start file tracker
    tracker = ComprehensiveFileTracker()
    tracker.start_tracking()
    
    try:
        print(f"🚀 Starting Luna with comprehensive file tracking...")
        print(f"❓ Questions: {questions}")
        print(f"🤖 Model: {model}")
        print(f"🔍 File tracking: ENABLED")
        print(f"=" * 60)
        
        # Run Luna command
        cmd = [
            sys.executable, "luna_main.py",
            "--mode", "real_learning",
            "--questions", str(questions),
            "--testruns", "1",
            "--model", model
        ]
        
        print(f"💻 Command: {' '.join(cmd)}")
        print(f"=" * 60)
        
        # Execute command
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd(), encoding='utf-8', errors='ignore')
        
        print(f"📤 STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print(f"📤 STDERR:")
            print(result.stderr)
            
        print(f"📊 Return code: {result.returncode}")
        
    except Exception as e:
        print(f"❌ Error running Luna: {e}")
        
    finally:
        # Stop tracking and generate report
        tracker.stop_tracking()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive file tracking for Luna process")
    parser.add_argument("--questions", type=int, default=3, help="Number of questions")
    parser.add_argument("--model", type=str, default="text-embedding-mlabonne_qwen3-0.6b-abliterated", help="Model to use")
    
    args = parser.parse_args()
    
    run_luna_with_comprehensive_tracking(args.questions, args.model)
