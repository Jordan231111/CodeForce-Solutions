"""Unit tests for solution B_Make_It_Permutation.py

The tests ensure that:
1. The number of printed operations does not exceed 2·n.
2. After applying the operations, every column is a permutation of 1..n.

Run with:  pypy3.10 -m pytest -q
"""

import random
import subprocess
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
SOL = ROOT / "B_Make_It_Permutation.py"
PY = sys.executable  # assume PyPy3.10 when running in contest environment


def apply_ops(n: int, ops: List[List[int]]):
    """Apply row-restricted reversals to an identity matrix and return it."""
    mat = [[col for col in range(1, n + 1)] for _ in range(n)]
    for r, l, rr in ops:
        r -= 1
        l -= 1
        rr -= 1
        mat[r][l : rr + 1] = list(reversed(mat[r][l : rr + 1]))
    return mat


def columns_are_permutations(mat):
    n = len(mat)
    for c in range(n):
        if {mat[r][c] for r in range(n)} != set(range(1, n + 1)):
            return False
    return True


def run_case(n: int):
    proc = subprocess.run(
        [PY, str(SOL)],
        input=f"1\n{n}\n".encode(),
        stdout=subprocess.PIPE,
        check=True,
    )
    tokens = proc.stdout.decode().strip().split()
    k = int(tokens[0])
    ops = [list(map(int, tokens[1 + 3 * i : 4 + 3 * i])) for i in range(k)]

    assert k <= 2 * n, "Exceeded 2n operations"

    mat = apply_ops(n, ops)
    assert columns_are_permutations(mat), "Columns are not permutations"


def test_samples():
    for n in (3, 4):
        run_case(n)


def test_random():
    random.seed(0)
    for n in range(3, 31):
        run_case(n) 