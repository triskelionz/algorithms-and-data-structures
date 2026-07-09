"""Dynamic programming algorithms: memoized Fibonacci, 0/1 Knapsack, and
Longest Common Subsequence.

Each function includes both the recurrence it implements and its
time/space complexity, so the trade-off against the naive recursive
version is explicit rather than assumed.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Sequence, Tuple


def fibonacci(n: int) -> int:
    """Returns the n-th Fibonacci number using bottom-up dynamic programming.

    Recurrence: fib(n) = fib(n - 1) + fib(n - 2), fib(0) = 0, fib(1) = 1.

    Time complexity: O(n) - each value from 0 to n is computed exactly once.
    Space complexity: O(1) - only the last two values are kept.
    (The naive recursive version is O(2^n) time because it recomputes the
    same subproblems exponentially many times.)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n

    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """Top-down memoized Fibonacci, kept separate to demonstrate the
    memoization technique explicitly (as opposed to the iterative
    bottom-up version above).

    Time complexity: O(n). Space complexity: O(n) for the call stack and cache.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> Tuple[int, List[int]]:
    """Solves the 0/1 Knapsack problem: choose a subset of items, each used
    at most once, that maximizes total value without exceeding `capacity`.

    Recurrence: table[i][w] = max(table[i-1][w], value[i] + table[i-1][w-weight[i]])
    when weight[i] <= w, else table[i][w] = table[i-1][w].

    Time complexity: O(n * capacity), n = number of items.
    Space complexity: O(n * capacity) for the DP table (kept for path
    reconstruction; can be reduced to O(capacity) if only the optimal
    value is needed).

    Returns a tuple of (best_value, selected_item_indices).
    """
    n = len(weights)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                table[i][w] = max(table[i - 1][w], value + table[i - 1][w - weight])
            else:
                table[i][w] = table[i - 1][w]

    selected: List[int] = []
    remaining_capacity = capacity
    for i in range(n, 0, -1):
        if table[i][remaining_capacity] != table[i - 1][remaining_capacity]:
            selected.append(i - 1)
            remaining_capacity -= weights[i - 1]
    selected.reverse()

    return table[n][capacity], selected


def longest_common_subsequence(a: str, b: str) -> str:
    """Returns one longest common subsequence of strings `a` and `b`.

    Recurrence: table[i][j] = table[i-1][j-1] + 1 if a[i-1] == b[j-1],
    else max(table[i-1][j], table[i][j-1]).

    Time complexity: O(n * m), n = len(a), m = len(b).
    Space complexity: O(n * m) for the DP table.
    """
    n, m = len(a), len(b)
    table: List[List[int]] = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])

    i, j = n, m
    result: List[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(result))
