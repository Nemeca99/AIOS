#!/usr/bin/env python3
"""
Complete File Dependency Map for Luna Main Process
Shows every single file that gets touched during execution
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List, Any

class CompleteFileDependencyMap:
    def __init__(self):
        self.all_files = set()
        self.python_files = set()
        self.json_files = set()
        self.config_files = set()
        self.data_files = set()
        self.cache_files = set()
        self.log_files = set()
        self.temp_files = set()
        
    def scan_system_files(self):
        """Scan for all system files that Luna touches"""
        print("🔍 Scanning complete file dependency map...")
        
        # Core Python files
        self._scan_python_files()
        
        # Configuration files
        self._scan_config_files()
        
        # Data files
        self._scan_data_files()
        
        # Cache files
        self._scan_cache_files()
        
        # Log files
        self._scan_log_files()
        
        # Temporary files
        self._scan_temp_files()
        
        # External dependencies
        self._scan_external_dependencies()
        
    def _scan_python_files(self):
        """Scan for Python files"""
        print("🐍 Scanning Python files...")
        
        # Core Luna files
        core_files = [
            "luna_main.py",
            "hive_mind_logger.py",
            "carma_core.py",
            "fractal_mycelium_cache.py",
            "carma_mycelium_network.py",
            "carma_executive_brain.py",
            "carma_meta_memory.py",
            "carma_100_percent_consciousness.py",
            "pi_based_encryption.py",
            "global_api_distribution.py",
            "enterprise_features.py",
            "carma_encrypted_api_server.py",
            "global_carma_api_server.py",
            "simple_embedder.py",
            "system_constants.py",
            "cache_operations.py",
            "embedding_operations.py",
            "recovery_operations.py"
        ]
        
        for file in core_files:
            if os.path.exists(file):
                self.python_files.add(file)
                self.all_files.add(file)
                
        # Scan for additional Python files
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.python_files.add(file_path)
                    self.all_files.add(file_path)
                    
    def _scan_config_files(self):
        """Scan for configuration files"""
        print("⚙️ Scanning configuration files...")
        
        config_files = [
            "AI_Core/Nova AI/AI/personality/luna_personality_dna.json",
            "AI_Core/Nova AI/AI/personality/luna_persistent_memory.json",
            "AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json",
            "requirements.txt",
            "docker-compose.yml",
            "Dockerfile",
            "README.md"
        ]
        
        for file in config_files:
            if os.path.exists(file):
                self.config_files.add(file)
                self.all_files.add(file)
                
    def _scan_data_files(self):
        """Scan for data files"""
        print("🗄️ Scanning data files...")
        
        # Database files
        db_files = [
            "F:/AI_Datasets/AIOS_Database/database/conversations.db"
        ]
        
        for file in db_files:
            if os.path.exists(file):
                self.data_files.add(file)
                self.all_files.add(file)
                
        # FractalCache files
        fractal_cache_dir = "Data/FractalCache"
        if os.path.exists(fractal_cache_dir):
            for root, dirs, files in os.walk(fractal_cache_dir):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        self.data_files.add(file_path)
                        self.all_files.add(file_path)
                        
        # Other data files
        data_files = [
            "Data/audit_log.json",
            "Data/billing_metrics.json",
            "Data/key_rotation.json"
        ]
        
        for file in data_files:
            if os.path.exists(file):
                self.data_files.add(file)
                self.all_files.add(file)
                
    def _scan_cache_files(self):
        """Scan for cache files"""
        print("💾 Scanning cache files...")
        
        cache_dirs = [
            "AI_Core/Nova AI/AI/personality/embedder_cache",
            "AI_Core/Nova AI/AI/personality/learning_results",
            "AI_Core/Nova AI/AI/personality/master_test_results"
        ]
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                for root, dirs, files in os.walk(cache_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.cache_files.add(file_path)
                        self.all_files.add(file_path)
                        
    def _scan_log_files(self):
        """Scan for log files"""
        print("📝 Scanning log files...")
        
        log_dirs = [
            "logs",
            "log",
            "AI_Core/Nova AI/AI/personality/logs"
        ]
        
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                for root, dirs, files in os.walk(log_dir):
                    for file in files:
                        if file.endswith('.log'):
                            file_path = os.path.join(root, file)
                            self.log_files.add(file_path)
                            self.all_files.add(file_path)
                            
    def _scan_temp_files(self):
        """Scan for temporary files"""
        print("🗂️ Scanning temporary files...")
        
        temp_dirs = [
            "C:/Users/nemec/AppData/Local/Temp/hive_mind_recovery",
            "C:/Users/nemec/AppData/Local/Temp"
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if 'luna' in file.lower() or 'hive_mind' in file.lower():
                            file_path = os.path.join(root, file)
                            self.temp_files.add(file_path)
                            self.all_files.add(file_path)
                            
    def _scan_external_dependencies(self):
        """Scan for external dependencies"""
        print("🔗 Scanning external dependencies...")
        
        # Python packages
        try:
            result = subprocess.run([sys.executable, "-c", "import sys; print('\\n'.join(sys.path))"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for path in result.stdout.strip().split('\n'):
                    if path and os.path.exists(path):
                        self.all_files.add(f"PYTHON_PATH: {path}")
        except Exception as e:
            print(f"⚠️ Could not scan Python paths: {e}")
            
    def generate_complete_map(self):
        """Generate complete file dependency map"""
        print("\n📊 COMPLETE FILE DEPENDENCY MAP")
        print("=" * 60)
        
        # Count files by category
        categories = {
            'Python Files': len(self.python_files),
            'Configuration Files': len(self.config_files),
            'Data Files': len(self.data_files),
            'Cache Files': len(self.cache_files),
            'Log Files': len(self.log_files),
            'Temporary Files': len(self.temp_files),
            'Total Files': len(self.all_files)
        }
        
        print(f"📁 FILE CATEGORIES:")
        for category, count in categories.items():
            print(f"   {category}: {count}")
            
        # Generate detailed report
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_files': len(self.all_files),
            'categories': {
                'python_files': sorted(list(self.python_files)),
                'config_files': sorted(list(self.config_files)),
                'data_files': sorted(list(self.data_files)),
                'cache_files': sorted(list(self.cache_files)),
                'log_files': sorted(list(self.log_files)),
                'temp_files': sorted(list(self.temp_files))
            },
            'all_files': sorted(list(self.all_files))
        }
        
        # Save report
        report_file = f"complete_file_dependency_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n💾 Complete dependency map saved to: {report_file}")
        
        # Print critical files
        self._print_critical_files()
        
        # Print file lists
        self._print_file_lists()
        
        return report
        
    def _print_critical_files(self):
        """Print critical files status"""
        print(f"\n🔑 CRITICAL FILES STATUS:")
        
        critical_files = {
            'luna_main.py': 'Main Luna script',
            'hive_mind_logger.py': 'Logging system',
            'carma_core.py': 'CARMA core system',
            'fractal_mycelium_cache.py': 'Mycelium cache system',
            'luna_personality_dna.json': 'Luna personality DNA',
            'luna_persistent_memory.json': 'Persistent memory',
            'master_test_cache.json': 'RAG cache file',
            'conversations.db': 'Main database'
        }
        
        for filename, description in critical_files.items():
            found = [f for f in self.all_files if filename in f]
            if found:
                print(f"   ✅ {filename}: {found[0]} ({description})")
            else:
                print(f"   ❌ {filename}: NOT FOUND ({description})")
                
    def _print_file_lists(self):
        """Print detailed file lists"""
        print(f"\n📋 DETAILED FILE LISTS:")
        
        # Python files
        if self.python_files:
            print(f"\n🐍 PYTHON FILES ({len(self.python_files)}):")
            for file_path in sorted(self.python_files):
                print(f"   📄 {file_path}")
                
        # Configuration files
        if self.config_files:
            print(f"\n⚙️ CONFIGURATION FILES ({len(self.config_files)}):")
            for file_path in sorted(self.config_files):
                print(f"   ⚙️ {file_path}")
                
        # Data files
        if self.data_files:
            print(f"\n🗄️ DATA FILES ({len(self.data_files)}):")
            for file_path in sorted(self.data_files):
                print(f"   🗄️ {file_path}")
                
        # Cache files
        if self.cache_files:
            print(f"\n💾 CACHE FILES ({len(self.cache_files)}):")
            for file_path in sorted(self.cache_files):
                print(f"   💾 {file_path}")
                
        # Log files
        if self.log_files:
            print(f"\n📝 LOG FILES ({len(self.log_files)}):")
            for file_path in sorted(self.log_files):
                print(f"   📝 {file_path}")
                
        # Temporary files
        if self.temp_files:
            print(f"\n🗂️ TEMPORARY FILES ({len(self.temp_files)}):")
            for file_path in sorted(self.temp_files):
                print(f"   🗂️ {file_path}")

def main():
    """Main function"""
    print("🚀 Starting Complete File Dependency Map Generation...")
    
    mapper = CompleteFileDependencyMap()
    mapper.scan_system_files()
    mapper.generate_complete_map()
    
    print(f"\n✅ Complete file dependency map generated!")
    print(f"📊 Total files identified: {len(mapper.all_files)}")

if __name__ == "__main__":
    main()
