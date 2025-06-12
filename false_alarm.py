#!/usr/bin/env python3
"""Codeforces Round Problem: A. False Alarm
Solves whether Yousef can press a button once to get past all doors.

Algorithm:
1. Identify the first and last closed doors.
2. The time interval between passing the first and last closed doors is
   (last - first + 1) seconds.  This must not exceed the button duration `x`.
   Equivalently, (last - first) < x.
3. Output YES if the condition holds, else NO.

Time complexity: O(n) per test case, memory O(1).
"""
import sys
from typing import List

def can_pass(n: int, x: int, doors: List[int]) -> bool:
    """Return True if Yousef can reach the exit using the button at most once."""
    # Find indices of first and last closed doors (state == 1).
    first = last = None
    for i, d in enumerate(doors):
        if d == 1:
            if first is None:
                first = i
            last = i
    # According to problem statement, there is at least one closed door.
    # Safety fallback in case of malformed input.
    if first is None or last is None:
        return True
    return (last - first) < x

def main() -> None:
    data_iter = iter(sys.stdin.read().strip().split())
    t = int(next(data_iter))
    out_lines: List[str] = []
    for _ in range(t):
        n = int(next(data_iter))
        x = int(next(data_iter))
        doors = [int(next(data_iter)) for _ in range(n)]
        out_lines.append("YES" if can_pass(n, x, doors) else "NO")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
