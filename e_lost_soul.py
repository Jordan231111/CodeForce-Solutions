#!/usr/bin/env pypy3
"""
Codeforces Round – Problem E: Lost Soul

Quick explanation:
- We need to find the length of the longest common prefix that can be achieved
- For each position i, we have two options: either a[i] == b[i], or we can use
  a copy operation to make them equal
- Copy operations work by using a value from the same array at a position
  with different parity
- We also have the option to delete exactly one element

The solution works by considering two separate cases:
1. No deletion needed: Check for direct matches or consecutive equal values
2. Single deletion: Check if deleting an element makes a prefix matchable

Complexity:
- Time: O(n) - we scan the arrays linearly
- Space: O(n) - we store sets of seen values
"""
from sys import stdin, stdout
from typing import List, Set


def solve_case(n: int, a: List[int], b: List[int]) -> int:
    """Return the maximum prefix length achievable, possibly after deleting one item."""
    # Trivial cases first.
    if n == 0 or a[-1] == b[-1]:
        return n  # either empty or already fully equal

    seen: Set[int] = set()  # numbers that appear strictly to the right of current idx

    # Scan from right to left (editorial trick).
    for i in range(n - 2, -1, -1):
        # If we can already force a match at position i, answer is i+1.
        if (
            a[i] == b[i]               # direct match
            or a[i] == a[i + 1]        # copy from a[i+1]
            or b[i] == b[i + 1]        # copy from b[i+1]
            or a[i] in seen            # later copy into a[i]
            or b[i] in seen            # later copy into b[i]
        ):
            return i + 1

        # Otherwise, remember the values at position i+1 for future copies.
        seen.add(a[i + 1])
        seen.add(b[i + 1])

    # No earlier position works – answer is 0 (no prefix except possibly empty).
    return 0


def main() -> None:
    # Fast integer stream without building an intermediate list of tokens.
    data = map(int, stdin.buffer.read().split())
    it = iter(data)
    t = next(it, 0)
    out_lines: List[str] = []

    for _ in range(t):
        n = next(it)
        a = [next(it) for _ in range(n)]
        b = [next(it) for _ in range(n)]
        out_lines.append(str(solve_case(n, a, b)))

    stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()
