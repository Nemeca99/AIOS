# semantic.py
import numpy as np
from typing import List, Optional

_DEFAULT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_FALLBACK_DIMENSION = 128

_embedder = None

def _get_embedder():
    global _embedder
    if _embedder is not None:
        return _embedder
    try:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(_DEFAULT_EMBED_MODEL)
        return _embedder
    except Exception:
        _embedder = False
        return None

def embed_text(text: str) -> List[float]:
    """Return a real embedding for text. Falls back to deterministic vector if model unavailable."""
    model = _get_embedder()
    if model is not None:
        vec = model.encode([text], normalize_embeddings=True)[0]
        return vec.tolist()
    # Deterministic fallback
    rng = np.random.RandomState(len(text))
    v = rng.randn(_FALLBACK_DIMENSION)
    v = v / (np.linalg.norm(v)+1e-12)
    return v.tolist()

def jaccard_tags(a: List[str], b: List[str]):
    if not a and not b: return 0.0
    sa, sb = set(a), set(b)
    inter = len(sa & sb)
    union = len(sa | sb) or 1
    return inter / union

def make_crosslinks(cache, threshold=0.3):
    ids = list(cache.registry.keys())
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            a = cache.registry[ids[i]]
            b = cache.registry[ids[j]]
            # combine tag similarity + cosine on embedding if available
            tag_sim = jaccard_tags(a.tags, b.tags)
            emb_sim = 0.0
            if a.embedding is not None and b.embedding is not None:
                av = np.array(a.embedding); bv = np.array(b.embedding)
                emb_sim = float(np.dot(av,bv)/(np.linalg.norm(av)*np.linalg.norm(bv)+1e-12))
            score = 0.6*tag_sim + 0.4*emb_sim
            if score >= threshold:
                # add bidirectional cross-link
                if b.id not in a.children:
                    a.children.append(b.id)
                if a.id not in b.children:
                    b.children.append(a.id)
