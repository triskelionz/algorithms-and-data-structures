# Algorithms and Data Structures

A curated collection of classic algorithms and data structures, implemented from scratch in Python and organized by topic. Every module favors clarity over cleverness: readable code, explicit complexity analysis, and unit tests that document expected behavior.

## Why this repository

This is meant to demonstrate the fundamentals that sit underneath most engineering and evaluation work: how to reason about correctness, trace an algorithm step by step, and back a claim ("this runs in O(n log n)") with a working implementation and tests rather than intuition alone.

## Structure

| Path | Contents |
| --- | --- |
| `graphs/graph.py` | Adjacency-list `Graph`, breadth-first search, depth-first search, Dijkstra shortest path |
| `dynamic_programming/dp_algorithms.py` | Memoized Fibonacci, 0/1 Knapsack, Longest Common Subsequence |
| `data_structures/heap.py` | Binary min-heap / priority queue built on a plain list |
| `data_structures/linked_list.py` | Singly linked list with insert, delete, search, and reverse |
| `tests/` | Unit tests covering each module |

## Complexity summary

| Algorithm | Time | Space | Notes |
| --- | --- | --- | --- |
| BFS | O(V + E) | O(V) | Shortest path in unweighted graphs |
| DFS | O(V + E) | O(V) | Reachability, cycle detection, topological ordering |
| Dijkstra (heap) | O((V + E) log V) | O(V) | Shortest path with non-negative weights |
| 0/1 Knapsack | O(n * W) | O(n * W) | n items, capacity W |
| Longest Common Subsequence | O(n * m) | O(n * m) | Sequences of length n and m |
| Fibonacci (memoized) | O(n) | O(n) | vs. O(2^n) for the naive recursive version |
| Binary heap push/pop | O(log n) | O(n) | n elements currently in the heap |
| Linked list search | O(n) | O(1) | Singly linked, no random access |

## Running the tests

No dependencies beyond the Python standard library.

```bash
git clone https://github.com/triskelionz/algorithms-and-data-structures.git
cd algorithms-and-data-structures
python -m unittest discover -s tests -v
```

## Design notes

- Every public function has a docstring stating its time and space complexity, not just what it does.
- Data structures are implemented without relying on high-level standard-library shortcuts (e.g. the heap is a manual array-based binary heap, not a thin wrapper around `heapq`), so the underlying mechanics stay visible.
- Tests cover typical cases, edge cases (empty input, single node, disconnected graphs), and at least one case that pins down the expected complexity-relevant behavior (e.g. memoization actually being used).

## License

MIT
