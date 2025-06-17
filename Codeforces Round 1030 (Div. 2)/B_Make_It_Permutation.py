"""Codeforces Round 2118B - Make It Permutation
=================================================
Given an initially identical matrix whose every row is the identity permutation
[1, 2, ..., n], we must perform at most 2·n reversal operations so that every
column also becomes a permutation of 1..n.  An operation selects a row *i* and
reverses its sub-array A[i][l..r].

Construction (≤ 2·n operations)
--------------------------------
For each row index i (1-indexed):
1. Reverse the prefix [1..i].
2. If i < n, reverse the suffix [i+1..n].

Row i becomes:
    [i, i-1, …, 1, n, n-1, …, i+1].

Proof that columns are permutations:
Let j be the column index.
• If j ≤ i, the element in row i, column j equals i - (j - 1).
• Otherwise (j > i), it equals n - (j - (i+1)).
Both expressions are bijective over i ∈ [1..n], hence every column is a
permutation of 1..n.

Operation count: Row n requires only the first reversal, so total operations
= (2·(n-1) + 1) = 2·n - 1 ≤ 2·n.

Complexities:
    Time   O(n) per test case (operation list generation)
    Memory O(1)

"""

import sys
from typing import List, Tuple

def generate_operations(n: int) -> List[Tuple[int, int, int]]:
    """Return a valid sequence of operations (≤ 2n) for given n."""
    ops: List[Tuple[int, int, int]] = []
    for row in range(1, n + 1):
        # 1) Reverse prefix [1 .. row]
        ops.append((row, 1, row))
        # 2) Reverse suffix [row+1 .. n] when non-empty
        if row < n:
            ops.append((row, row + 1, n))
    # Total ops = 2n-1
    return ops

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    t = data[0]
    idx = 1
    out_lines: List[str] = []
    for _ in range(t):
        n = data[idx]
        idx += 1
        ops = generate_operations(n)
        out_lines.append(str(len(ops)))
        out_lines.extend(f"{i} {l} {r}" for i, l, r in ops)
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":  # pragma: no cover
    main()