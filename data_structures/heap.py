"""A binary min-heap implemented directly on a Python list.

Built manually (rather than delegating to `heapq`) so the sift-up /
sift-down mechanics that give a heap its O(log n) push and pop are
visible and testable.
"""

from __future__ import annotations

from typing import Generic, List, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """A binary min-heap: the smallest element is always at the root.

    Internally stored as a list where, for a node at index i, its children
    live at 2*i + 1 and 2*i + 2, and its parent lives at (i - 1) // 2.
    """

    def __init__(self) -> None:
        self._data: List[T] = []

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def peek(self) -> T:
        """Returns the smallest element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self._data[0]

    def push(self, value: T) -> None:
        """Inserts `value` and restores the heap property.

        Time complexity: O(log n) - the new element sifts up at most
        log2(n) levels.
        """
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """Removes and returns the smallest element.

        Time complexity: O(log n) - the replacement root sifts down at
        most log2(n) levels.
        """
        if self.is_empty():
            raise IndexError("pop from an empty heap")

        smallest = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return smallest

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._data[index] < self._data[parent]:
                self._data[index], self._data[parent] = self._data[parent], self._data[index]
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        size = len(self._data)
        while True:
            left, right = 2 * index + 1, 2 * index + 2
            smallest = index

            if left < size and self._data[left] < self._data[smallest]:
                smallest = left
            if right < size and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest == index:
                break

            self._data[index], self._data[smallest] = self._data[smallest], self._data[index]
            index = smallest


class PriorityQueue(Generic[T]):
    """A priority queue built on `MinHeap`: lower priority values are
    served first. Ties are broken by insertion order.
    """

    def __init__(self) -> None:
        self._heap: MinHeap = MinHeap()
        self._counter = 0

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return self._heap.is_empty()

    def push(self, item: T, priority: float) -> None:
        """Time complexity: O(log n), same as the underlying heap push."""
        self._heap.push((priority, self._counter, item))
        self._counter += 1

    def pop(self) -> T:
        """Time complexity: O(log n), same as the underlying heap pop."""
        _, _, item = self._heap.pop()
        return item
