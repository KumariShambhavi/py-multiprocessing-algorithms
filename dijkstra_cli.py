#!/usr/bin/env python3
"""
dijkstra_cli.py

Reads a CSV of edges with columns: city1,city2,distance
Builds an undirected graph and runs Dijkstra for shortest path queries.

Usage:
    python dijkstra_cli.py edges.csv source dest
"""

import csv
import sys
import heapq
from typing import Dict, List, Tuple, Any

def build_graph_from_csv(path: str):
    graph: Dict[str, List[Tuple[str,float]]] = {}
    with open(path, newline='') as fh:
        reader = csv.reader(fh)
        for a,b,w in reader:
            w = float(w)
            graph.setdefault(a, []).append((b,w))
            graph.setdefault(b, []).append((a,w))
    return graph

def dijkstra(graph: Dict[str, List[Tuple[str,float]]], source: str):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0.0
    pq = [(0.0, source)]
    visited = set()
    while pq:
        d,u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v,w in graph.get(u,[]):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def reconstruct(prev, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python dijkstra_cli.py edges.csv source dest")
        sys.exit(1)
    graph = build_graph_from_csv(sys.argv[1])
    src = sys.argv[2]; dst = sys.argv[3]
    dist, prev = dijkstra(graph, src)
    if dst not in dist or dist[dst] == float('inf'):
        print(f"No path from {src} to {dst}")
    else:
        path = reconstruct(prev, dst)
        print(f"Shortest path {src} -> {dst}: {' -> '.join(path)} (dist = {dist[dst]})")
