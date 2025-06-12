#!/usr/bin/env pypy3
"""Tests for false_alarm.py"""
import unittest
from false_alarm import can_pass

class TestFalseAlarm(unittest.TestCase):
    """Test cases for the false alarm problem"""

    def test_single_closed_door(self):
        """Test case with only one closed door"""
        self.assertTrue(can_pass(5, 10, [0, 0, 1, 0, 0]))

    def test_multiple_closed_doors_within_x(self):
        """Test case where closed doors are within x seconds"""
        # first=1, last=3. last-first=2. 2 < 3 is True.
        self.assertTrue(can_pass(5, 3, [0, 1, 1, 1, 0]))

    def test_doors_exceeding_x(self):
        """Test case where closed doors exceed x seconds"""
        # first=0, last=4. last-first=4. 4 < 2 is False.
        self.assertFalse(can_pass(5, 2, [1, 0, 0, 0, 1]))

    def test_all_doors_closed(self):
        """Test case where all doors are closed"""
        # first=0, last=3. last-first=3. 3 < 4 is True.
        self.assertTrue(can_pass(4, 4, [1, 1, 1, 1]))

    def test_first_and_last_doors_closed(self):
        """Test case with first and last doors closed"""
        # first=0, last=4. last-first=4. 4 < 5 is True.
        self.assertTrue(can_pass(5, 5, [1, 0, 0, 0, 1]))

    def test_no_closed_doors(self):
        """Test case with no closed doors (should pass based on implementation)"""
        self.assertTrue(can_pass(5, 10, [0, 0, 0, 0, 0]))

    def test_tight_condition_fail(self):
        """Test case with a tight condition that fails"""
        # first=1, last=2. last-first=1. 1 < 1 is False.
        self.assertFalse(can_pass(5, 1, [0, 1, 1, 0, 0]))

    def test_tight_condition_pass(self):
        """Test case with a tight condition that passes"""
        # first=1, last=2. last-first=1. 1 < 2 is True.
        self.assertTrue(can_pass(5, 2, [0, 1, 1, 0, 0]))

    def test_large_input_pass(self):
        """Test with large input that should pass"""
        n = 10**5
        x = n
        doors = [0] * n
        doors[0] = 1
        doors[n-1] = 1
        # last - first = (n-1) - 0 = n-1. n-1 < n is True.
        self.assertTrue(can_pass(n, x, doors))

    def test_large_input_fail(self):
        """Test with large input that should fail"""
        n = 10**5
        x = n - 1
        doors = [0] * n
        doors[0] = 1
        doors[n-1] = 1
        # last - first = n-1. n-1 < n-1 is False.
        self.assertFalse(can_pass(n, x, doors))

if __name__ == "__main__":
    unittest.main()
