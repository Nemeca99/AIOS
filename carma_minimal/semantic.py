# semantic.py
import numpy as np
from typing import List
def fake_embed(text: str, dim=128):
    # placeholder: deterministic pseudo-embedding (for tests)
    rng = np.random.RandomState(len(text))
    v = rng.randn(dim)
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
