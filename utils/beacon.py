#!/usr/bin/env python3
"""
Beacon System - Improved Fragment Discovery
Fixes fragment scanning and blank file detection
"""

import os
import json
import pathlib
import logging
from typing import List, Dict, Optional

log = logging.getLogger("beacon")

def find_fragments(cache_dir: str) -> List[Dict]:
    """Find all fragment files with improved scanning logic"""
    out = []
    p = pathlib.Path(cache_dir)
    
    if not p.exists():
        log.error("cache_dir missing: %s", cache_dir)
        return out
    
    # Recursive scan for all JSON files
    for fp in p.rglob("*.json"):
        try:
            data = json.loads(fp.read_text())
            frag_id = data.get("id") or fp.stem
            marker = data.get("blank", "false")  # expected marker
            size = fp.stat().st_size
            
            out.append({
                "path": str(fp),
                "id": frag_id,
                "size": size,
                "blank": marker,
                "level": data.get("level", 0),
                "parent_id": data.get("parent_id"),
                "children_ids": data.get("children_ids", [])
            })
        except Exception as e:
            log.warning("bad fragment file %s: %s", fp, e)
    
    log.info("find_fragments -> found %d fragment files", len(out))
    return out

def find_blank_files(cache_dir: str) -> List[Dict]:
    """Find files marked as blank or missing content"""
    fragments = find_fragments(cache_dir)
    blank_files = []
    
    for frag in fragments:
        # Check if file is marked as blank
        if frag.get("blank") == "true" or frag.get("blank") is True:
            blank_files.append(frag)
            continue
        
        # Check if file has no content
        try:
            with open(frag["path"], 'r') as f:
                data = json.load(f)
            content = data.get("content", "")
            if not content or content.strip() == "":
                blank_files.append(frag)
        except:
            # File might be corrupted or unreadable
            blank_files.append(frag)
    
    log.info("find_blank_files -> found %d blank files", len(blank_files))
    return blank_files

def create_blank_placeholder(file_path: str, file_id: str, level: int = 0) -> Dict:
    """Create a blank placeholder file"""
    placeholder = {
        "id": file_id,
        "level": level,
        "content": "",
        "blank": True,
        "reconstructed": False,
        "created": "2025-01-27T00:00:00Z",
        "placeholder_prompt": f"Reconstruct content for {file_id} at level {level}",
        "status": "blank"
    }
    
    # Write placeholder file
    with open(file_path, 'w') as f:
        json.dump(placeholder, f, indent=2)
    
    log.info("Created blank placeholder: %s", file_id)
    return placeholder

if __name__ == "__main__":
    import sys
    cache_dir = sys.argv[1] if len(sys.argv) > 1 else "Data/FractalCache"
    
    print(f"Scanning: {cache_dir}")
    fragments = find_fragments(cache_dir)
    print(f"Found {len(fragments)} fragments")
    
    blank_files = find_blank_files(cache_dir)
    print(f"Found {len(blank_files)} blank files")
    
    if fragments:
        print("Sample fragments:")
        for frag in fragments[:5]:
            print(f"  {frag['id']} (level {frag['level']}, size {frag['size']}, blank: {frag['blank']})")
