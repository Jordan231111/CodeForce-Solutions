#!/usr/bin/env pypy3
"""Stress-test e_lost_soul on the suspected test-15 pattern."""
from e_lost_soul import solve_case
import time
n = 200_000
# pattern   1 200000 1 200000 ...  for a;  the same for b but shifted
vals = [1, 200000] * (n//2)
a = vals[:]                       # 1 200000 1 200000 …
b = vals[::-1]                    # 200000 1 200000 1 …
start = time.time()
print('answer =', solve_case(n, a, b))
print('elapsed = %.4f s' % (time.time() - start)) 