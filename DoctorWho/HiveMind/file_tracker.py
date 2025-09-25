#!/usr/bin/env python3
"""
File Tracker for Luna Main Process
Tracks every single file that gets touched during execution
"""

import os
import sys
import json
import time
import psutil
import threading
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List, Any
import subprocess

class FileTracker:
    def __init__(self):
        self.touched_files = set()
        self.file_operations = []
        self.process_id = None
        self.start_time = None
        self.end_time = None
        self.monitoring = False
        
    def start_monitoring(self, process_id: int = None):
        """Start monitoring file operations"""
        self.process_id = process_id or os.getpid()
        self.start_time = datetime.now()
        self.monitoring = True
        
        print(f"🔍 Starting file tracking for process {self.process_id}")
        print(f"⏰ Started at: {self.start_time}")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_files)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring and generate report"""
        self.monitoring = False
        self.end_time = datetime.now()
        
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
            
        print(f"⏹️ File tracking stopped at: {self.end_time}")
        self._generate_report()
        
    def _monitor_files(self):
        """Monitor file operations in background thread"""
        try:
            process = psutil.Process(self.process_id)
            
            while self.monitoring:
                try:
                    # Get open files
                    open_files = process.open_files()
                    for file_info in open_files:
                        file_path = file_info.path
                        if file_path:
                            self.touched_files.add(file_path)
                            self.file_operations.append({
                                'timestamp': datetime.now().isoformat(),
                                'operation': 'open',
                                'file': file_path,
                                'fd': file_info.fd
                            })
                    
                    # Get memory maps (loaded libraries)
                    memory_maps = process.memory_maps()
                    for mmap in memory_maps:
                        if mmap.path and os.path.exists(mmap.path):
                            self.touched_files.add(mmap.path)
                            self.file_operations.append({
                                'timestamp': datetime.now().isoformat(),
                                'operation': 'memory_map',
                                'file': mmap.path,
                                'perms': mmap.perms
                            })
                    
                    time.sleep(0.1)  # Check every 100ms
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                    
        except Exception as e:
            print(f"❌ File monitoring error: {e}")
            
    def _generate_report(self):
        """Generate comprehensive file tracking report"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Categorize files
        python_files = []
        json_files = []
        log_files = []
        cache_files = []
        data_files = []
        config_files = []
        other_files = []
        
        for file_path in self.touched_files:
            if file_path.endswith('.py'):
                python_files.append(file_path)
            elif file_path.endswith('.json'):
                json_files.append(file_path)
            elif file_path.endswith('.log'):
                log_files.append(file_path)
            elif 'cache' in file_path.lower():
                cache_files.append(file_path)
            elif 'data' in file_path.lower() or file_path.endswith('.db'):
                data_files.append(file_path)
            elif file_path.endswith(('.yml', '.yaml', '.ini', '.cfg', '.conf')):
                config_files.append(file_path)
            else:
                other_files.append(file_path)
        
        # Generate report
        report = {
            'tracking_info': {
                'process_id': self.process_id,
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat(),
                'duration_seconds': duration,
                'total_files_touched': len(self.touched_files),
                'total_operations': len(self.file_operations)
            },
            'file_categories': {
                'python_files': {
                    'count': len(python_files),
                    'files': sorted(python_files)
                },
                'json_files': {
                    'count': len(json_files),
                    'files': sorted(json_files)
                },
                'log_files': {
                    'count': len(log_files),
                    'files': sorted(log_files)
                },
                'cache_files': {
                    'count': len(cache_files),
                    'files': sorted(cache_files)
                },
                'data_files': {
                    'count': len(data_files),
                    'files': sorted(data_files)
                },
                'config_files': {
                    'count': len(config_files),
                    'files': sorted(config_files)
                },
                'other_files': {
                    'count': len(other_files),
                    'files': sorted(other_files)
                }
            },
            'all_touched_files': sorted(list(self.touched_files)),
            'file_operations': self.file_operations
        }
        
        # Save report
        report_file = f"file_tracking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print(f"\n📊 FILE TRACKING REPORT")
        print(f"=" * 50)
        print(f"⏰ Duration: {duration:.2f} seconds")
        print(f"📁 Total files touched: {len(self.touched_files)}")
        print(f"🔄 Total operations: {len(self.file_operations)}")
        print(f"\n📂 FILE CATEGORIES:")
        print(f"   🐍 Python files: {len(python_files)}")
        print(f"   📄 JSON files: {len(json_files)}")
        print(f"   📝 Log files: {len(log_files)}")
        print(f"   💾 Cache files: {len(cache_files)}")
        print(f"   🗄️ Data files: {len(data_files)}")
        print(f"   ⚙️ Config files: {len(config_files)}")
        print(f"   📁 Other files: {len(other_files)}")
        print(f"\n💾 Report saved to: {report_file}")
        
        # Print critical files
        print(f"\n🔑 CRITICAL FILES:")
        critical_files = [
            'luna_main.py',
            'luna_personality_dna.json',
            'master_test_cache.json',
            'luna_persistent_memory.json'
        ]
        
        for critical in critical_files:
            found = [f for f in self.touched_files if critical in f]
            if found:
                print(f"   ✅ {critical}: {found[0]}")
            else:
                print(f"   ❌ {critical}: NOT FOUND")
        
        return report

def run_luna_with_tracking(questions: int = 5, model: str = "text-embedding-mlabonne_qwen3-0.6b-abliterated"):
    """Run Luna with file tracking"""
    
    # Start file tracker
    tracker = FileTracker()
    tracker.start_monitoring()
    
    try:
        print(f"🚀 Starting Luna with file tracking...")
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
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
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
        tracker.stop_monitoring()
        
        # Also check for any files created during the process
        print(f"\n🔍 CHECKING FOR NEW FILES...")
        check_for_new_files()

def check_for_new_files():
    """Check for any new files created during the process"""
    current_dir = Path.cwd()
    
    # Look for common file patterns
    patterns = [
        "*.json",
        "*.log", 
        "*.py",
        "*.md",
        "*.txt",
        "*.db",
        "*.cache"
    ]
    
    new_files = []
    for pattern in patterns:
        new_files.extend(current_dir.rglob(pattern))
    
    # Filter for recent files (last 5 minutes)
    recent_cutoff = time.time() - 300
    recent_files = [f for f in new_files if f.stat().st_mtime > recent_cutoff]
    
    if recent_files:
        print(f"📁 NEW FILES CREATED:")
        for file_path in sorted(recent_files):
            print(f"   📄 {file_path}")
    else:
        print(f"📁 No new files created")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Track files touched by Luna process")
    parser.add_argument("--questions", type=int, default=5, help="Number of questions")
    parser.add_argument("--model", type=str, default="text-embedding-mlabonne_qwen3-0.6b-abliterated", help="Model to use")
    
    args = parser.parse_args()
    
    run_luna_with_tracking(args.questions, args.model)
