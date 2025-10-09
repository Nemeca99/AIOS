#!/usr/bin/env python3
"""
Seed Documentation to CARMA
Loads core documentation files directly into CARMA's FractalCache
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

def create_fragment_id(content: str, source: str) -> str:
    """Create a unique fragment ID based on content hash"""
    hash_input = f"{source}:{content[:100]}"
    return f"doc_{hashlib.md5(hash_input.encode()).hexdigest()[:8]}"

def seed_documentation():
    """Load core documentation into CARMA cache"""
    
    # Essential documentation files
    core_docs = [
        "AIOS_CLEAN_PARADIGM.md",
        "data_core/docs/MAIN_README.md",
        "AIOS_MASTER_DOCUMENTATION.md",
        "README.md",
        "MATHEMATICAL_CONVERSATION_SYSTEM.md",
        "QEC_INTEGRATION_SUMMARY.md",
        "COMPREHENSIVE_ASSESSMENT.md",
        "RUNBOOK.md",
    ]
    
    print("=" * 70)
    print("SEEDING DOCUMENTATION TO CARMA")
    print("=" * 70)
    
    base_dir = Path(".")
    cache_dir = base_dir / "data_core" / "FractalCache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    fragments_added = 0
    total_chunks = 0
    
    for doc_path in core_docs:
        full_path = base_dir / doc_path
        
        if not full_path.exists():
            print(f"⚠️  Skipping {doc_path} (not found)")
            continue
        
        try:
            content = full_path.read_text(encoding='utf-8')
            
            # Split into 1500-char chunks (CARMA-friendly size)
            max_chunk_size = 1500
            chunks = []
            
            # Split by paragraphs first
            paragraphs = content.split('\n\n')
            current_chunk = []
            current_size = 0
            
            for para in paragraphs:
                para_size = len(para) + 2  # +2 for \n\n
                
                if current_size + para_size > max_chunk_size and current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [para]
                    current_size = para_size
                else:
                    current_chunk.append(para)
                    current_size += para_size
            
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
            
            # Save each chunk as a CARMA fragment
            for i, chunk in enumerate(chunks):
                fragment_id = create_fragment_id(chunk, doc_path)
                
                fragment_data = {
                    "content": chunk,
                    "metadata": {
                        "source": doc_path,
                        "type": "documentation",
                        "chunk": i + 1,
                        "total_chunks": len(chunks),
                        "added_at": datetime.now().isoformat(),
                        "category": "core_documentation"
                    },
                    "access_count": 0,
                    "last_accessed": None,
                    "reinforcement_weight": 1.0,
                    "tags": ["documentation", "core", doc_path.replace('.md', '').replace('/', '_')]
                }
                
                # Save as individual JSON file (CARMA's format)
                fragment_file = cache_dir / f"{fragment_id}.json"
                with open(fragment_file, 'w', encoding='utf-8') as f:
                    json.dump(fragment_data, f, indent=2, ensure_ascii=False)
                
                fragments_added += 1
                total_chunks += 1
            
            print(f"✅ {doc_path}: {len(chunks)} chunks → {fragments_added} fragments")
            
        except Exception as e:
            print(f"❌ Error loading {doc_path}: {e}")
    
    # Update the registry
    registry_path = cache_dir / "registry.json"
    
    try:
        if registry_path.exists():
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        else:
            registry = {"fragments": {}}
        
        # Add documentation fragments to registry
        for fragment_file in cache_dir.glob("doc_*.json"):
            fragment_id = fragment_file.stem
            if fragment_id not in registry.get("fragments", {}):
                with open(fragment_file, 'r', encoding='utf-8') as f:
                    frag = json.load(f)
                
                registry["fragments"][fragment_id] = {
                    "file": fragment_file.name,
                    "source": frag["metadata"]["source"],
                    "type": "documentation",
                    "access_count": 0,
                    "added_at": frag["metadata"]["added_at"]
                }
        
        # Save updated registry
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Registry updated: {len(registry['fragments'])} total fragments")
        
    except Exception as e:
        print(f"⚠️  Registry update error: {e}")
    
    print("\n" + "=" * 70)
    print(f"✅ SEEDING COMPLETE: {fragments_added} documentation fragments added")
    print("=" * 70)
    print("\nLuna now has access to:")
    print("  - AIOS architecture and paradigm")
    print("  - CARMA definition and details")
    print("  - Master documentation")
    print("  - Mathematical conversation system")
    print("  - QEC integration details")
    print("  - System assessment and runbook")
    print("\nShe can now answer questions accurately using her own documentation!")
    
    return fragments_added

if __name__ == "__main__":
    seed_documentation()

