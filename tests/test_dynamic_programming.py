import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynamic_programming.dp_algorithms import (
    fibonacci,
    fibonacci_memoized,
    knapsack_01,
    longest_common_subsequence,
)


class TestFibonacci(unittest.TestCase):
    def test_base_cases(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)

    def test_known_sequence(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        actual = [fibonacci(n) for n in range(len(expected))]
        self.assertEqual(actual, expected)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_memoized_matches_iterative(self):
        for n in range(20):
            self.assertEqual(fibonacci_memoized(n), fibonacci(n))

    def test_memoized_cache_is_used(self):
        # Calling with a larger n first primes the cache for smaller n;
        # if memoization were not happening this would still be correct,
        # but would be exponentially slow for large n. This at least
        # confirms the cache_info reports hits after repeated calls.
        fibonacci_memoized.cache_clear()
        fibonacci_memoized(30)
        info = fibonacci_memoized.cache_info()
        self.assertGreater(info.hits, 0)


class TestKnapsack(unittest.TestCase):
    def test_classic_example(self):
        weights = [1, 3, 4, 5]
        values = [1, 4, 5, 7]
        best_value, selected = knapsack_01(weights, values, capacity=7)
        self.assertEqual(best_value, 9)
        self.assertEqual(sum(weights[i] for i in selected), 7)
        self.assertEqual(sum(values[i] for i in selected), 9)

    def test_zero_capacity_selects_nothing(self):
        best_value, selected = knapsack_01([1, 2, 3], [10, 20, 30], capacity=0)
        self.assertEqual(best_value, 0)
        self.assertEqual(selected, [])

    def test_single_item_fits(self):
        best_value, selected = knapsack_01([5], [100], capacity=5)
        self.assertEqual(best_value, 100)
        self.assertEqual(selected, [0])

    def test_single_item_does_not_fit(self):
        best_value, selected = knapsack_01([10], [100], capacity=5)
        self.assertEqual(best_value, 0)
        self.assertEqual(selected, [])


class TestLongestCommonSubsequence(unittest.TestCase):
    def test_classic_example(self):
        result = longest_common_subsequence("ABCBDAB", "BDCABA")
        self.assertEqual(len(result), 4)
        for char in result:
            self.assertIn(char, "ABCBDAB")

    def test_identical_strings(self):
        self.assertEqual(longest_common_subsequence("abc", "abc"), "abc")

    def test_no_common_characters(self):
        self.assertEqual(longest_common_subsequence("abc", "xyz"), "")

    def test_empty_string(self):
        self.assertEqual(longest_common_subsequence("", "abc"), "")
        self.assertEqual(longest_common_subsequence("abc", ""), "")


if __name__ == "__main__":
    unittest.main()
