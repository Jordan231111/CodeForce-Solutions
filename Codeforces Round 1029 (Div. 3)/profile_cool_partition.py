#!/usr/bin/env pypy3
"""Profile C_Cool_Partition.solve_case on a large random input."""
import random
import cProfile
import pstats
from C_Cool_Partition import solve_case


def run_profile(n=200_000):
    rng = random.Random(42)
    arr = [rng.randint(1, n) for _ in range(n)]
    profiler = cProfile.Profile()
    profiler.enable()
    solve_case(n, arr)
    profiler.disable()
    stats = pstats.Stats(profiler).strip_dirs().sort_stats("cumtime")
    stats.print_stats(15)  # print top 15 entries


if __name__ == "__main__":
    run_profile() 