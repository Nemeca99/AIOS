#!/usr/bin/env python3
"""
Load Core Documentation to CARMA
Loads ONLY essential documentation files into CARMA so Luna has accurate context
"""

from pathlib import Path
from main import AIOSClean

def load_core_docs():
    """Load only the most essential documentation into memory"""
    
    # CRITICAL documentation files Luna needs for accurate answers
    core_docs = {
        "AIOS_CLEAN_PARADIGM.md": "Core AIOS architecture and paradigm",
        "data_core/docs/MAIN_README.md": "CARMA definition and architecture",
        "AIOS_MASTER_DOCUMENTATION.md": "Master system documentation",
        "README.md": "Project overview",
        "MATHEMATICAL_CONVERSATION_SYSTEM.md": "Conversation routing system",
        "QEC_INTEGRATION_SUMMARY.md": "Quality control integration",
    }
    
    print("=" * 70)
    print("LOADING CORE DOCUMENTATION TO CARMA")
    print("=" * 70)
    
    base_dir = Path(".")
    fragments_to_add = []
    
    for doc_path, description in core_docs.items():
        full_path = base_dir / doc_path
        if full_path.exists():
            try:
                content = full_path.read_text(encoding='utf-8')
                
                # Split into reasonable chunks (2000 chars each)
                chunks = []
                lines = content.split('\n')
                current_chunk = []
                current_size = 0
                
                for line in lines:
                    line_size = len(line) + 1  # +1 for \n
                    
                    if current_size + line_size > 2000 and current_chunk:
                        chunks.append('\n'.join(current_chunk))
                        current_chunk = [line]
                        current_size = line_size
                    else:
                        current_chunk.append(line)
                        current_size += line_size
                
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                
                for i, chunk in enumerate(chunks):
                    fragment_id = f"doc_{doc_path.replace('/', '_').replace('.md', '')}_{i+1}"
                    fragments_to_add.append({
                        'id': fragment_id,
                        'content': chunk,
                        'source': doc_path,
                        'description': description,
                        'chunk': i+1,
                        'total_chunks': len(chunks)
                    })
                
                print(f"✅ Loaded: {doc_path} ({len(chunks)} chunks)")
            except Exception as e:
                print(f"❌ Error loading {doc_path}: {e}")
        else:
            print(f"⚠️  Not found: {doc_path}")
    
    print(f"\n📊 Total fragments to add: {len(fragments_to_add)}")
    
    # Now write these to a file that CARMA can load on startup
    import json
    doc_cache_path = base_dir / "data_core" / "FractalCache" / "documentation_fragments.json"
    
    with open(doc_cache_path, 'w', encoding='utf-8') as f:
        json.dump({
            'fragments': fragments_to_add,
            'loaded_at': str(Path.cwd()),
            'total_count': len(fragments_to_add)
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Documentation cache saved to: {doc_cache_path}")
    print(f"\n✅ Luna can now access {len(fragments_to_add)} documentation fragments for accurate answers!")
    
    return fragments_to_add

if __name__ == "__main__":
    fragments = load_core_docs()

