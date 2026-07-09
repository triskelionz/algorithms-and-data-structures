import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.heap import MinHeap, PriorityQueue
from data_structures.linked_list import LinkedList


class TestMinHeap(unittest.TestCase):
    def test_pop_returns_ascending_order(self):
        heap: MinHeap = MinHeap()
        for value in [5, 3, 8, 1, 9, 2]:
            heap.push(value)

        result = [heap.pop() for _ in range(len(heap))]
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])

    def test_peek_does_not_remove(self):
        heap: MinHeap = MinHeap()
        heap.push(4)
        heap.push(1)
        self.assertEqual(heap.peek(), 1)
        self.assertEqual(len(heap), 2)

    def test_pop_from_empty_raises(self):
        heap: MinHeap = MinHeap()
        with self.assertRaises(IndexError):
            heap.pop()

    def test_single_element(self):
        heap: MinHeap = MinHeap()
        heap.push(42)
        self.assertEqual(heap.pop(), 42)
        self.assertTrue(heap.is_empty())

    def test_duplicate_values(self):
        heap: MinHeap = MinHeap()
        for value in [3, 3, 1, 1, 2]:
            heap.push(value)
        result = [heap.pop() for _ in range(len(heap))]
        self.assertEqual(result, [1, 1, 2, 3, 3])


class TestPriorityQueue(unittest.TestCase):
    def test_lower_priority_served_first(self):
        queue: PriorityQueue = PriorityQueue()
        queue.push("low", priority=1)
        queue.push("high", priority=10)
        queue.push("medium", priority=5)

        self.assertEqual(queue.pop(), "low")
        self.assertEqual(queue.pop(), "medium")
        self.assertEqual(queue.pop(), "high")

    def test_ties_broken_by_insertion_order(self):
        queue: PriorityQueue = PriorityQueue()
        queue.push("first", priority=1)
        queue.push("second", priority=1)

        self.assertEqual(queue.pop(), "first")
        self.assertEqual(queue.pop(), "second")


class TestLinkedList(unittest.TestCase):
    def test_push_front_and_iteration_order(self):
        linked_list = LinkedList()
        linked_list.push_front(2)
        linked_list.push_front(1)
        self.assertEqual(linked_list.to_list(), [1, 2])

    def test_push_back_and_iteration_order(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back(2)
        self.assertEqual(linked_list.to_list(), [1, 2])

    def test_find(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back(2)
        self.assertTrue(linked_list.find(2))
        self.assertFalse(linked_list.find(99))

    def test_delete_head(self):
        linked_list = LinkedList()
        for value in [1, 2, 3]:
            linked_list.push_back(value)
        self.assertTrue(linked_list.delete(1))
        self.assertEqual(linked_list.to_list(), [2, 3])

    def test_delete_middle(self):
        linked_list = LinkedList()
        for value in [1, 2, 3]:
            linked_list.push_back(value)
        self.assertTrue(linked_list.delete(2))
        self.assertEqual(linked_list.to_list(), [1, 3])

    def test_delete_missing_value_returns_false(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        self.assertFalse(linked_list.delete(99))

    def test_reverse(self):
        linked_list = LinkedList()
        for value in [1, 2, 3, 4]:
            linked_list.push_back(value)
        linked_list.reverse()
        self.assertEqual(linked_list.to_list(), [4, 3, 2, 1])

    def test_len_tracks_size(self):
        linked_list = LinkedList()
        self.assertEqual(len(linked_list), 0)
        linked_list.push_back(1)
        linked_list.push_back(2)
        self.assertEqual(len(linked_list), 2)
        linked_list.delete(1)
        self.assertEqual(len(linked_list), 1)


if __name__ == "__main__":
    unittest.main()
