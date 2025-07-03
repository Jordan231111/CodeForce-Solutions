import random, os, sys

# Ensure project root is on path then import solution module directly.
sys.path.append(os.path.dirname(__file__))

import c as mod
import io

def check(n, k):
    p = mod.generate(n, k)
    assert sorted(p) == list(range(1, n + 1)), 'Not a permutation'
    diff_cnt = len({p[i] - (i + 1) for i in range(n)})
    assert diff_cnt == k, f'Expected {k} distinct diffs, got {diff_cnt}'


def run_small_cases():
    for n in range(1, 11):
        for k in range(1, n + 1):
            check(n, k)


def run_random():
    for _ in range(200):
        n = random.randint(1, 100)
        k = random.randint(1, n)
        check(n, k)


# Save original stdin/stdout
original_stdin = sys.stdin
original_stdout = sys.stdout

# Sample input (from problem statement) used for property-based verification
test_input = """5
1 1
2 1
2 2
4 2
6 3
"""

# Capture solution output
output_stream = io.StringIO()
sys.stdout = output_stream
sys.stdin = io.StringIO(test_input)

mod.solve()

# Restore stdio
sys.stdin = original_stdin
sys.stdout = original_stdout

print("Property-based check on official sample …", end=" ")

# Validate each produced permutation respects required properties
out_lines = output_stream.getvalue().strip().split("\n")
cases = [tuple(map(int, line.split())) for line in test_input.strip().split("\n")[1:]]
assert len(out_lines) == len(cases)

for (n, k), line in zip(cases, out_lines):
    p = list(map(int, line.split()))
    assert len(p) == n
    assert sorted(p) == list(range(1, n + 1))
    diffs = {p[i] - (i + 1) for i in range(n)}
    assert len(diffs) == k

print("PASSED ✓")

if __name__ == '__main__':
    run_small_cases()
    run_random()
    print('All tests passed.') 