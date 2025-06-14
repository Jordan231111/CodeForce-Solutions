#!/usr/bin/env pypy3
from e_lost_soul import solve_case, MaskTable, BIT_MAP

# Test function that implements the solution directly without the MaskTable
def debug_solve_case(n, a, b):
    # Check for empty arrays
    if n == 0:
        return 0
    
    # 1. No-deletion case
    best_no_del = 0
    for i in range(n):
        if a[i] == b[i]:
            best_no_del = max(best_no_del, i + 1)
    for i in range(n - 1):
        if a[i] == a[i + 1] or b[i] == b[i + 1]:
            best_no_del = max(best_no_del, i + 1)

    # 2. Single-deletion case
    seen_a = set()
    seen_b = set()
    best_with_del = 0

    for j in range(n - 2, -1, -1):  # start from n-2 down to 0
        if (a[j] in seen_a) or (a[j] in seen_b) or (b[j] in seen_a) or (b[j] in seen_b):
            best_with_del = max(best_with_del, j + 1)  # prefix length = j+1

        # add the pair at index j+1 to the seen sets
        seen_a.add(a[j + 1])
        seen_b.add(b[j + 1])

    return max(best_no_del, best_with_del)

# Run all test cases from test_e_lost_soul.py
t_input = """10
4
1 3 1 4
4 3 2 2
6
2 1 5 3 6 4
3 2 4 5 1 6
2
1 2
2 1
6
2 5 1 3 6 4
3 5 2 3 4 6
4
1 3 2 2
2 1 3 4
8
3 1 4 6 2 2 5 7
4 2 3 7 1 1 6 5
10
5 1 2 7 3 9 4 10 6 8
6 2 3 6 4 10 5 1 7 9
5
3 2 4 1 5
2 4 5 1 3
7
2 2 6 4 1 3 5
3 1 6 5 1 4 2
5
4 1 3 2 5
3 2 1 5 4"""
expected_outputs = [3, 3, 0, 4, 3, 5, 6, 4, 5, 2]

data = list(map(int, t_input.strip().split()))
it = iter(data)
_ = next(it)

print("Testing with both implementations:")
print("idx | n | Expected | Complex Impl | Simple Impl | Result")
print("----|---|----------|-------------|------------|-------")

for idx, expected in enumerate(expected_outputs):
    n = next(it)
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    
    # Run both implementations
    complex_result = solve_case(n, a, b)
    simple_result = debug_solve_case(n, a, b)
    
    status = "PASS" if complex_result == expected else "FAIL"
    print(f"{idx:2d} | {n:1d} | {expected:8d} | {complex_result:11d} | {simple_result:10d} | {status}") 