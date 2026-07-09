"""Graph traversal and shortest-path algorithms on an adjacency-list graph.

All three algorithms below operate on the same `Graph` representation so
their behavior and complexity can be compared directly.
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Dict, Hashable, Iterable, List, Optional, Tuple


class Graph:
    """A directed, optionally weighted graph stored as an adjacency list.

    Adding an edge is O(1). Space usage is O(V + E).
    """

    def __init__(self) -> None:
        self._adjacency: Dict[Hashable, List[Tuple[Hashable, float]]] = {}

    def add_node(self, node: Hashable) -> None:
        self._adjacency.setdefault(node, [])

    def add_edge(self, source: Hashable, target: Hashable, weight: float = 1.0, bidirectional: bool = False) -> None:
        self.add_node(source)
        self.add_node(target)
        self._adjacency[source].append((target, weight))
        if bidirectional:
            self._adjacency[target].append((source, weight))

    def neighbors(self, node: Hashable) -> List[Tuple[Hashable, float]]:
        return self._adjacency.get(node, [])

    @property
    def nodes(self) -> Iterable[Hashable]:
        return self._adjacency.keys()


def bfs(graph: Graph, start: Hashable) -> List[Hashable]:
    """Breadth-first traversal order starting from `start`.

    Time complexity: O(V + E) - every node is visited once and every edge
    is inspected once.
    Space complexity: O(V) for the visited set and the queue.
    """
    if start not in graph.nodes:
        return []

    visited = {start}
    order: List[Hashable] = []
    queue: deque = deque([start])

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor, _ in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs(graph: Graph, start: Hashable) -> List[Hashable]:
    """Depth-first traversal order starting from `start`, implemented
    iteratively with an explicit stack (no recursion limit concerns).

    Time complexity: O(V + E).
    Space complexity: O(V) for the visited set and the stack.
    """
    if start not in graph.nodes:
        return []

    visited = set()
    order: List[Hashable] = []
    stack: List[Hashable] = [start]

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        order.append(current)
        for neighbor, _ in reversed(graph.neighbors(current)):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def dijkstra(graph: Graph, start: Hashable) -> Dict[Hashable, float]:
    """Single-source shortest path distances using a binary-heap priority queue.

    Assumes non-negative edge weights. Nodes unreachable from `start` are
    omitted from the result.

    Time complexity: O((V + E) log V) - each node is popped from the heap
    once, and each edge may trigger one heap push.
    Space complexity: O(V) for the distance map and the heap.
    """
    distances: Dict[Hashable, float] = {start: 0.0}
    visited = set()
    heap: List[Tuple[float, Hashable]] = [(0.0, start)]

    while heap:
        current_distance, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.neighbors(current):
            candidate = current_distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))

    return distances


def shortest_path(graph: Graph, start: Hashable, end: Hashable) -> Optional[List[Hashable]]:
    """Reconstructs the shortest path from `start` to `end` using Dijkstra.

    Returns None if `end` is unreachable from `start`.
    Time complexity: O((V + E) log V), dominated by the Dijkstra call.
    """
    predecessors: Dict[Hashable, Hashable] = {}
    distances: Dict[Hashable, float] = {start: 0.0}
    visited = set()
    heap: List[Tuple[float, Hashable]] = [(0.0, start)]

    while heap:
        current_distance, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        for neighbor, weight in graph.neighbors(current):
            candidate = current_distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                predecessors[neighbor] = current
                heapq.heappush(heap, (candidate, neighbor))

    if end not in distances:
        return None

    path = [end]
    while path[-1] != start:
        path.append(predecessors[path[-1]])
    path.reverse()
    return path
