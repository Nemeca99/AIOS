#!/usr/bin/env python3
"""
Provenance Log Rotation
Rotates and compresses NDJSON logs to prevent unbounded growth
"""

import gzip
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


class LogRotator:
    """Rotates and compresses provenance logs"""
    
    def __init__(self, 
                 log_dir: str = 'data_core/analytics',
                 max_size_mb: float = 50.0,
                 keep_rotations: int = 10):
        self.log_dir = Path(log_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.keep_rotations = keep_rotations
    
    def check_rotation_needed(self, log_file: Path) -> bool:
        """Check if log file needs rotation"""
        if not log_file.exists():
            return False
        
        size = log_file.stat().st_size
        return size > self.max_size_bytes
    
    def rotate_log(self, log_file: Path, compress: bool = True):
        """
        Rotate a log file
        
        Steps:
        1. Rename current log to timestamped backup
        2. Optionally compress backup
        3. Create fresh log file
        4. Prune old rotations
        """
        if not log_file.exists():
            print(f"Log file not found: {log_file}")
            return
        
        # Create rotation filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        rotation_file = log_file.with_suffix(f'.{timestamp}.ndjson')
        
        print(f"Rotating {log_file.name} -> {rotation_file.name}")
        
        # Rename current log
        shutil.move(str(log_file), str(rotation_file))
        
        # Compress if requested
        if compress:
            print(f"  Compressing...")
            compressed_file = rotation_file.with_suffix('.ndjson.gz')
            
            with open(rotation_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed
            rotation_file.unlink()
            
            # Calculate compression ratio
            original_size = log_file.stat().st_size if log_file.exists() else rotation_file.stat().st_size
            compressed_size = compressed_file.stat().st_size
            ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
            
            print(f"  Compressed: {original_size/1024:.1f}KB -> {compressed_size/1024:.1f}KB ({ratio:.1f}% reduction)")
        
        # Create fresh log
        log_file.touch()
        print(f"  Created fresh {log_file.name}")
        
        # Prune old rotations
        self._prune_rotations(log_file)
    
    def _prune_rotations(self, log_file: Path):
        """Keep only N most recent rotations"""
        # Find all rotations for this log
        pattern = f"{log_file.stem}.*.ndjson*"
        rotations = sorted(self.log_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Remove old rotations
        to_remove = rotations[self.keep_rotations:]
        
        if to_remove:
            print(f"  Pruning {len(to_remove)} old rotations")
            for old_file in to_remove:
                print(f"    Removing {old_file.name}")
                old_file.unlink()
    
    def rotate_all(self, compress: bool = True):
        """Rotate all NDJSON files in log directory that exceed size limit"""
        if not self.log_dir.exists():
            print(f"Log directory not found: {self.log_dir}")
            return
        
        ndjson_files = [f for f in self.log_dir.glob('*.ndjson') if not '.bak' in f.name]
        
        print("="*70)
        print("PROVENANCE LOG ROTATION")
        print("="*70)
        print(f"Max size: {self.max_size_bytes/1024/1024:.1f}MB")
        print(f"Keep rotations: {self.keep_rotations}")
        print(f"Compress: {compress}")
        print()
        
        rotated = 0
        for log_file in ndjson_files:
            size_mb = log_file.stat().st_size / 1024 / 1024
            
            if self.check_rotation_needed(log_file):
                print(f"\n{log_file.name} ({size_mb:.1f}MB) - ROTATING")
                self.rotate_log(log_file, compress=compress)
                rotated += 1
            else:
                print(f"{log_file.name} ({size_mb:.1f}MB) - OK")
        
        print("\n" + "="*70)
        print(f"Rotated {rotated} log files")
        print("="*70)
    
    def get_rotation_stats(self) -> Dict[str, Any]:
        """Get statistics about log rotations"""
        stats = {
            'active_logs': [],
            'rotations': [],
            'total_size_mb': 0.0
        }
        
        if not self.log_dir.exists():
            return stats
        
        # Active logs
        for log_file in self.log_dir.glob('*.ndjson'):
            if '.bak' in log_file.name or '.' in log_file.stem.split('_')[-1]:
                continue  # Skip backups and rotations
            
            size_mb = log_file.stat().st_size / 1024 / 1024
            stats['active_logs'].append({
                'name': log_file.name,
                'size_mb': size_mb,
                'needs_rotation': size_mb > (self.max_size_bytes / 1024 / 1024)
            })
            stats['total_size_mb'] += size_mb
        
        # Rotations
        for rot_file in self.log_dir.glob('*.ndjson.*'):
            if not rot_file.suffix in ['.gz', '.bak']:
                # Timestamped rotation
                size_mb = rot_file.stat().st_size / 1024 / 1024
                stats['rotations'].append({
                    'name': rot_file.name,
                    'size_mb': size_mb,
                    'compressed': rot_file.suffix == '.gz'
                })
        
        return stats


def main():
    """Main CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Provenance Log Rotator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Rotate command
    rotate_parser = subparsers.add_parser('rotate', help='Rotate logs')
    rotate_parser.add_argument('--no-compress', action='store_true', help='Do not compress rotations')
    rotate_parser.add_argument('--max-size', type=float, default=50.0, help='Max size in MB (default: 50)')
    rotate_parser.add_argument('--keep', type=int, default=10, help='Number of rotations to keep (default: 10)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show rotation statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'rotate':
        rotator = LogRotator(max_size_mb=args.max_size, keep_rotations=args.keep)
        rotator.rotate_all(compress=not args.no_compress)
    
    elif args.command == 'stats':
        rotator = LogRotator()
        stats = rotator.get_rotation_stats()
        
        print("="*70)
        print("LOG ROTATION STATISTICS")
        print("="*70)
        
        print("\nActive logs:")
        for log in stats['active_logs']:
            status = "NEEDS ROTATION" if log['needs_rotation'] else "OK"
            print(f"  {log['name']}: {log['size_mb']:.2f}MB - {status}")
        
        print(f"\nRotations: {len(stats['rotations'])} files")
        total_rotation_size = sum(r['size_mb'] for r in stats['rotations'])
        compressed_count = sum(1 for r in stats['rotations'] if r['compressed'])
        
        print(f"  Compressed: {compressed_count}/{len(stats['rotations'])}")
        print(f"  Total size: {total_rotation_size:.2f}MB")
        
        print(f"\nTotal log storage: {stats['total_size_mb'] + total_rotation_size:.2f}MB")
        print("="*70)


if __name__ == "__main__":
    main()

