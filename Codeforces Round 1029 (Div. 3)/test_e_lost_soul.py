#!/usr/bin/env pypy3
"""Unit tests for E. Lost Soul solver (`e_lost_soul.py`)."""
import unittest
from e_lost_soul import solve_case


class TestLostSoul(unittest.TestCase):
    """Regression tests covering the official samples and a few edge cases."""

    def test_official_samples(self):
        # Sample input consolidated from the Codeforces statement (10 cases)
        t_input = """10
4
1 3 1 4
4 3 2 2
6
2 1 5 3 6 4
3 2 4 5 1 6
2
1 2
2 1
6
2 5 1 3 6 4
3 5 2 3 4 6
4
1 3 2 2
2 1 3 4
8
3 1 4 6 2 2 5 7
4 2 3 7 1 1 6 5
10
5 1 2 7 3 9 4 10 6 8
6 2 3 6 4 10 5 1 7 9
5
3 2 4 1 5
2 4 5 1 3
7
2 2 6 4 1 3 5
3 1 6 5 1 4 2
5
4 1 3 2 5
3 2 1 5 4"""
        expected_outputs = [3, 3, 0, 4, 3, 5, 6, 4, 5, 2]

        data = list(map(int, t_input.strip().split()))
        it = iter(data)
        _ = next(it)  # skip t
        for expected in expected_outputs:
            n = next(it)
            a = [next(it) for _ in range(n)]
            b = [next(it) for _ in range(n)]
            self.assertEqual(solve_case(n, a, b), expected)

    def test_small_edges(self):
        # 1-element arrays
        self.assertEqual(solve_case(1, [1], [1]), 1)
        self.assertEqual(solve_case(1, [1], [2]), 0)
        # 2 elements identical vs swapped
        self.assertEqual(solve_case(2, [1, 1], [1, 1]), 2)
        self.assertEqual(solve_case(2, [1, 2], [2, 1]), 0)


if __name__ == "__main__":
    unittest.main() 