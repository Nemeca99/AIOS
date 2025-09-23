# pathfinding.py
import heapq
from typing import Dict, List, Tuple

def dijkstra_shortest_path(registry, start_id, target_id, weight_fn):
    # weight_fn(u_id, v_id) -> cost
    dist = {start_id: 0}
    prev = {}
    q = [(0, start_id)]
    visited = set()
    while q:
        d,u = heapq.heappop(q)
        if u in visited: continue
        visited.add(u)
        if u == target_id:
            break
        node = registry.get(u)
        if not node: continue
        # neighbors: parent + children
        neighbors = []
        if node.parent: neighbors.append(node.parent)
        neighbors += node.children
        for v in neighbors:
            cost = weight_fn(u, v)
            nd = d + cost
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(q, (nd, v))
    if target_id not in dist:
        return None, float('inf')
    path = []
    cur = target_id
    while cur != start_id:
        path.append(cur)
        cur = prev[cur]
    path.append(start_id)
    path.reverse()
    return path, dist[target_id]
