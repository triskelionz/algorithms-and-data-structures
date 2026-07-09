"""A singly linked list with insert, delete, search, and in-place reversal.
"""

from __future__ import annotations

from typing import Any, Iterator, Optional


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value: Any, next: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next


class LinkedList:
    """A singly linked list. No random access, so lookups by position or
    value are O(n), but insertion at the head is O(1).
    """

    def __init__(self) -> None:
        self._head: Optional[Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return " -> ".join(repr(value) for value in self)

    def is_empty(self) -> bool:
        return self._head is None

    def push_front(self, value: Any) -> None:
        """Inserts `value` at the head. Time complexity: O(1)."""
        self._head = Node(value, self._head)
        self._size += 1

    def push_back(self, value: Any) -> None:
        """Inserts `value` at the tail. Time complexity: O(n) - the list
        must be walked to find the current tail.
        """
        new_node = Node(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def find(self, value: Any) -> bool:
        """Returns True if `value` is present. Time complexity: O(n)."""
        return any(existing == value for existing in self)

    def delete(self, value: Any) -> bool:
        """Removes the first node matching `value`.

        Time complexity: O(n) - the list must be walked to find the node.
        Returns True if a node was removed, False if `value` was not found.
        """
        previous: Optional[Node] = None
        current = self._head

        while current is not None:
            if current.value == value:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next
                self._size -= 1
                return True
            previous, current = current, current.next

        return False

    def to_list(self) -> list:
        return list(self)

    def reverse(self) -> None:
        """Reverses the list in place by re-pointing each node.next.

        Time complexity: O(n). Space complexity: O(1) - no new nodes are
        allocated, only pointers are rewired.
        """
        previous: Optional[Node] = None
        current = self._head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self._head = previous
