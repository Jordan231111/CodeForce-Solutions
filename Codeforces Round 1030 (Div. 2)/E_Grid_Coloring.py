#!/usr/bin/env pypy3
"""Codeforces 2118E – Grid Coloring
===================================

Task (concise)
--------------
For each odd-sized grid `n × m` (`1 ≤ n, m ≤ 4 999`, `n·m` odd, and
`Σ n·m ≤ 5 000` per test file) output **any** ordering of the `n·m` cell
coordinates such that when the cells are coloured one-by-one in the given
order, **no already coloured cell ever has more than three coloured 4-neighbours**.
A 4-neighbour is a cell that shares a side (same row & adjacent column or
same column & adjacent row).

Key observation
---------------
The degree of a grid cell (number of 4-neighbours) is
    • 4 for interior cells,
    • ≤3 for boundary cells.
When we colour *row by row from top-left to bottom-right* (standard
lexicographic scan order):
    • at the moment we colour a cell, its *bottom* neighbour is still
      uncoloured because we have not reached the next row yet;
    • its *right* neighbour is uncoloured because we have not reached the
      next column yet,
so **at most two of its neighbours (top and/or left) are coloured**.
Therefore every cell's penalty is ≤2 ≤ 3, which fulfils the requirement.

Construction
------------
For every test case simply output the coordinates in lexicographic order
(`row = 1..n`, for each row `col = 1..m`).  This scan uses only
`O(n·m)` time and `O(1)` extra memory and obviously respects the input
limits (`Σ n·m ≤ 5 000`).

Correctness proof
-----------------
Consider an arbitrary cell `(i, j)` (1-indexed) processed by the algorithm.
The coloured neighbours at that moment can only be
    • `(i, j-1)` if `j > 1` (left), and
    • `(i-1, j)` if `i > 1` (top)
because the scan has not reached any cell in a future row or a future column
of the current row yet.  Hence the number of previously coloured neighbours
is 0, 1 or 2, never exceeding 3.  ∎

Complexities
------------
Time   `O(n·m)` per test case (single pass output).
Memory `O(1)` apart from the output buffer.

Fast-Fail checklist
-------------------
✓ Single forward scan, no extra passes.  ✓ Zero hash-lookups.
✓ Early exit impossible — entire ordering required.

"""
import sys
from typing import List

def solve(test_input: bytes) -> str:  # helper for the test module
    it = iter(map(int, test_input.split()))
    t = next(it)
    out_lines: List[str] = []
    for _ in range(t):
        n = next(it)
        m = next(it)
        # Simple row-major scan (lexicographic order).  When colouring a
        # cell (r, c) only its top neighbour (r-1, c) and left neighbour
        # (r, c-1) can already be coloured, so the invariant "≤ 3 coloured
        # neighbours" is trivially satisfied (in fact, ≤ 2).

        for r in range(1, n + 1):
            for c in range(1, m + 1):
                out_lines.append(f"{r} {c}")
        out_lines.append("")  # blank line after each test case
    # remove the very last blank line for cleaner output
    if out_lines and out_lines[-1] == "":
        out_lines.pop()
    return "\n".join(out_lines)

def main() -> None:
    sys.stdout.write(solve(sys.stdin.buffer.read()))

if __name__ == "__main__":
    main()
