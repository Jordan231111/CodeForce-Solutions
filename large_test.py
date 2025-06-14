#!/usr/bin/env pypy3
"""Test the solution with a large input."""
import time
from e_lost_soul import solve_case

# Create a large test case similar to the one in the screenshot
n = 200000
a = [1] * n  # All elements are 1
b = [1] * n  # All elements are 1

# Measure the time
start_time = time.time()
result = solve_case(n, a, b)
end_time = time.time()

print(f"Result: {result}")
print(f"Time taken: {end_time - start_time:.6f} seconds")
print(f"Size of input: {n} elements") 