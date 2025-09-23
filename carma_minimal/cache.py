# cache.py
import os, json, math, random, time
from fragments import make_fragment, Fragment
from typing import Dict, List, Tuple
import heapq
import numpy as np

class CarmaCache:
    def __init__(self, max_file_size=1024*1024, max_splits=6, max_fragments=1000):
        self.registry: Dict[str, Fragment] = {}
        self.max_file_size = max_file_size
        self.max_splits = max_splits
        self.max_fragments = max_fragments

    def create_fragment(self, content:str, parent=None, level=0, tags=None) -> Fragment:
        f = make_fragment(content, parent, level, tags)
        self.registry[f.id] = f
        if parent:
            p = self.registry.get(parent)
            if p:
                p.children.append(f.id)
        self._enforce_size()
        return f

    def _enforce_size(self):
        # simple eviction by hits ascending when over size
        if len(self.registry) <= self.max_fragments: return
        items = sorted(self.registry.values(), key=lambda x: (x.hits, x.last_access))
        for f in items[:len(self.registry)-self.max_fragments]:
            self.registry.pop(f.id, None)

    def find_relevant(self, query_embedding, topk=5):
        # naive embedding cosine search: if embeddings missing returns random
        scores = []
        for f in self.registry.values():
            if f.embedding is not None and query_embedding is not None:
                a = np.array(f.embedding)
                b = np.array(query_embedding)
                score = float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-12))
            else:
                score = random.random()*0.1
            scores.append((score, f.id))
        scores.sort(reverse=True)
        result = [self.registry[_id] for _, _id in scores[:topk]]
        for r in result:
            r.hits += 1
            r.last_access = time.time()
        return result

    def split_fragment_if_needed(self, frag_id, split_threshold_ratio=0.8):
        f = self.registry.get(frag_id)
        if not f: return []
        if f.size < int(self.max_file_size*split_threshold_ratio): return []
        # naive split: split content into N pieces
        num_splits = min(4, self.max_splits)
        chunk = math.ceil(len(f.content) / num_splits)
        new_ids = []
        for i in range(num_splits):
            piece = f.content[i*chunk:(i+1)*chunk]
            if not piece: continue
            nf = self.create_fragment(piece, parent=f.id, level=f.level+1)
            new_ids.append(nf.id)
        return new_ids

    def add_embedding(self, frag_id, emb):
        if frag_id in self.registry:
            self.registry[frag_id].embedding = list(emb)
