#!/usr/bin/env pypy3
"""Unit tests for C_Cool_Partition.py

Each test case calls the `solve_case` function with a crafted array and
verifies that the returned maximum number of segments matches the
expected value.
"""
import unittest
from C_Cool_Partition import solve_case


class TestCoolPartition(unittest.TestCase):
    """Test suite for the Cool Partition problem (CF 1980C)"""

    def test_single_element(self):
        """Single element array should always yield one segment."""
        self.assertEqual(solve_case(1, [42]), 1)

    def test_two_identical_elements(self):
        """[x, x] can be split into two valid segments."""
        self.assertEqual(solve_case(2, [5, 5]), 2)

    def test_two_distinct_elements(self):
        """[a, b] (a != b) cannot be split; expect one segment."""
        self.assertEqual(solve_case(2, [1, 2]), 1)

    def test_duplicates_allow_more_segments(self):
        """Array with duplicates enabling multiple short segments."""
        self.assertEqual(solve_case(5, [1, 1, 1, 1, 1]), 5)

    def test_increasing_elements(self):
        """Strictly increasing array forces a single segment."""
        self.assertEqual(solve_case(4, [1, 2, 3, 4]), 1)

    def test_alternating(self):
        """Alternating small set causing limited segments."""
        self.assertEqual(solve_case(6, [1, 2, 1, 2, 1, 2]), 3)


if __name__ == "__main__":
    unittest.main() 