#!/usr/bin/env pypy3
"""Test the solution with a worst-case scenario."""
import time
from e_lost_soul import solve_case

# Create a worst-case scenario:
# - All elements are different (maximizing set size)
# - The arrays have matches only with deletion
# - Sets grow as large as possible
n = 200000
a = list(range(1, n+1))  # 1 to n
b = list(range(n, 0, -1))  # n to 1

# Measure the time
start_time = time.time()
result = solve_case(n, a, b)
end_time = time.time()

print(f"Result: {result}")
print(f"Time taken: {end_time - start_time:.6f} seconds")
print(f"Size of input: {n} elements") 