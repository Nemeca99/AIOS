#!/usr/bin/env python3
"""
Organize Essential Files for Luna System
Moves only the necessary files to KEEP folder and filters out unnecessary ones
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class EssentialFileOrganizer:
    def __init__(self):
        self.keep_dir = Path("KEEP")
        self.keep_dir.mkdir(exist_ok=True)
        
        # Essential file categories
        self.essential_files = {
            'python_files': [],
            'config_files': [],
            'data_files': [],
            'cache_files': [],
            'temp_files': []
        }
        
        # Files to exclude (unnecessary)
        self.exclude_patterns = [
            'test_*.py',
            '*_test.py', 
            '*_backup.py',
            'ablation_*.py',
            'experiment_*.py',
            'debug_*.py',
            'temp_*.py',
            '*.tmp',
            '*.log',
            '*.url',
            '__pycache__',
            '.git',
            '.vscode',
            'node_modules'
        ]
        
    def organize_files(self):
        """Organize all essential files into KEEP folder"""
        print("🚀 Starting essential file organization...")
        
        # Create subdirectories
        self._create_subdirectories()
        
        # Move Python files
        self._move_python_files()
        
        # Move configuration files
        self._move_config_files()
        
        # Move data files
        self._move_data_files()
        
        # Move cache files
        self._move_cache_files()
        
        # Move temporary files (if needed)
        self._move_temp_files()
        
        # Generate summary
        self._generate_summary()
        
    def _create_subdirectories(self):
        """Create organized subdirectories"""
        subdirs = [
            'python_core',
            'python_carma',
            'python_enterprise',
            'python_support',
            'config',
            'data_fractalcache',
            'data_system',
            'cache',
            'temp'
        ]
        
        for subdir in subdirs:
            (self.keep_dir / subdir).mkdir(exist_ok=True)
            
    def _move_python_files(self):
        """Move essential Python files"""
        print("🐍 Moving Python files...")
        
        # Core Luna files
        core_files = [
            'luna_main.py',
            'hive_mind_logger.py',
            'simple_luna_test.py',
            'overnight_test.py'
        ]
        
        # CARMA system files
        carma_files = [
            'carma_core.py',
            'fractal_mycelium_cache.py',
            'carma_mycelium_network.py',
            'carma_executive_brain.py',
            'carma_meta_memory.py',
            'carma_100_percent_consciousness.py'
        ]
        
        # Enterprise files
        enterprise_files = [
            'pi_based_encryption.py',
            'global_api_distribution.py',
            'enterprise_features.py',
            'carma_encrypted_api_server.py',
            'global_carma_api_server.py'
        ]
        
        # Support files
        support_files = [
            'simple_embedder.py',
            'system_constants.py',
            'cache_operations.py',
            'embedding_operations.py',
            'recovery_operations.py'
        ]
        
        # Move files to appropriate subdirectories
        self._move_files_to_category(core_files, 'python_core')
        self._move_files_to_category(carma_files, 'python_carma')
        self._move_files_to_category(enterprise_files, 'python_enterprise')
        self._move_files_to_category(support_files, 'python_support')
        
    def _move_config_files(self):
        """Move configuration files"""
        print("⚙️ Moving configuration files...")
        
        config_files = [
            'AI_Core/Nova AI/AI/personality/luna_personality_dna.json',
            'AI_Core/Nova AI/AI/personality/luna_persistent_memory.json',
            'AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json',
            'README.md'
        ]
        
        for file_path in config_files:
            if os.path.exists(file_path):
                dest_path = self.keep_dir / 'config' / os.path.basename(file_path)
                shutil.copy2(file_path, dest_path)
                self.essential_files['config_files'].append(str(dest_path))
                print(f"   ✅ {file_path} -> {dest_path}")
                
    def _move_data_files(self):
        """Move essential data files"""
        print("🗄️ Moving data files...")
        
        # System data files
        system_data_files = [
            'Data/audit_log.json',
            'Data/billing_metrics.json', 
            'Data/key_rotation.json'
        ]
        
        for file_path in system_data_files:
            if os.path.exists(file_path):
                dest_path = self.keep_dir / 'data_system' / os.path.basename(file_path)
                shutil.copy2(file_path, dest_path)
                self.essential_files['data_files'].append(str(dest_path))
                print(f"   ✅ {file_path} -> {dest_path}")
        
        # FractalCache files (sample - not all 377)
        fractal_cache_dir = Path("Data/FractalCache")
        if fractal_cache_dir.exists():
            # Copy first 50 files as sample
            count = 0
            for file_path in fractal_cache_dir.glob("*.json"):
                if count >= 50:  # Limit to 50 files for now
                    break
                dest_path = self.keep_dir / 'data_fractalcache' / file_path.name
                shutil.copy2(file_path, dest_path)
                self.essential_files['data_files'].append(str(dest_path))
                count += 1
            print(f"   ✅ Copied {count} FractalCache files (sample)")
            
    def _move_cache_files(self):
        """Move cache files"""
        print("💾 Moving cache files...")
        
        cache_files = [
            'AI_Core/Nova AI/AI/personality/embedder_cache/master_test_cache.json'
        ]
        
        for file_path in cache_files:
            if os.path.exists(file_path):
                dest_path = self.keep_dir / 'cache' / os.path.basename(file_path)
                shutil.copy2(file_path, dest_path)
                self.essential_files['cache_files'].append(str(dest_path))
                print(f"   ✅ {file_path} -> {dest_path}")
                
    def _move_temp_files(self):
        """Move essential temporary files (if any)"""
        print("🗂️ Checking temporary files...")
        
        # Don't move temp files - they're not essential
        print("   ⏭️ Skipping temporary files (not essential for deployment)")
        
    def _move_files_to_category(self, file_list, category):
        """Move files to specific category directory"""
        for file_path in file_list:
            if os.path.exists(file_path):
                dest_path = self.keep_dir / category / os.path.basename(file_path)
                shutil.copy2(file_path, dest_path)
                self.essential_files['python_files'].append(str(dest_path))
                print(f"   ✅ {file_path} -> {dest_path}")
                
    def _generate_summary(self):
        """Generate organization summary"""
        print("\n📊 ESSENTIAL FILE ORGANIZATION SUMMARY")
        print("=" * 60)
        
        total_files = sum(len(files) for files in self.essential_files.values())
        
        print(f"📁 Total essential files organized: {total_files}")
        print(f"📂 Organized into: {self.keep_dir}")
        
        for category, files in self.essential_files.items():
            if files:
                print(f"\n{category.replace('_', ' ').title()}: {len(files)} files")
                for file_path in files[:5]:  # Show first 5 files
                    print(f"   📄 {file_path}")
                if len(files) > 5:
                    print(f"   ... and {len(files) - 5} more files")
        
        # Save detailed report
        report = {
            'organized_at': datetime.now().isoformat(),
            'total_files': total_files,
            'categories': self.essential_files,
            'keep_directory': str(self.keep_dir)
        }
        
        report_file = self.keep_dir / 'organization_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n💾 Organization report saved to: {report_file}")
        
        # Create requirements.txt
        self._create_requirements_txt()
        
    def _create_requirements_txt(self):
        """Create requirements.txt for the essential files"""
        requirements = [
            "numpy>=1.21.0",
            "requests>=2.25.0",
            "psutil>=5.8.0",
            "pathlib",
            "json",
            "sqlite3",
            "threading",
            "queue",
            "signal",
            "atexit",
            "shutil",
            "glob",
            "tempfile",
            "datetime",
            "time",
            "random",
            "re",
            "sys",
            "os",
            "subprocess",
            "argparse",
            "statistics",
            "traceback"
        ]
        
        req_file = self.keep_dir / 'requirements.txt'
        with open(req_file, 'w') as f:
            for req in requirements:
                f.write(f"{req}\n")
                
        print(f"📋 Requirements file created: {req_file}")

def main():
    """Main function"""
    print("🚀 Starting Essential File Organization...")
    
    organizer = EssentialFileOrganizer()
    organizer.organize_files()
    
    print(f"\n✅ Essential file organization complete!")
    print(f"📁 All essential files moved to: KEEP/")
    print(f"🎯 Ready for deployment with minimal file set")

if __name__ == "__main__":
    main()
