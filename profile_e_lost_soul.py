#!/usr/bin/env pypy3
"""Profile e_lost_soul.solve_case on a large random instance."""
import random, cProfile, pstats, io
from e_lost_soul import solve_case

N = 200_000
random.seed(0)
a = [random.randint(1, 10**9) for _ in range(N)]
b = [random.randint(1, 10**9) for _ in range(N)]

pr = cProfile.Profile()
pr.enable()
solve_case(N, a, b)
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats(20)
print(s.getvalue()) 