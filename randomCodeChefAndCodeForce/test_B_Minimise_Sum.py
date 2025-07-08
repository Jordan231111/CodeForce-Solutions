import subprocess
import time
import random
import itertools

SOLUTION_FILE = "B_Minimise_Sum.py"


def brute_solution(arr):
    n = len(arr)
    prefix_min_orig = list(itertools.accumulate(arr, min))
    best = sum(prefix_min_orig)
    # try no operation explicitly handled by initializing best
    for i in range(n):
        for j in range(i + 1, n):
            b = arr[:]
            b[i] += b[j]
            b[j] = 0
            prefix = list(itertools.accumulate(b, min))
            s = sum(prefix)
            if s < best:
                best = s
    return best


def run_test_case(arr):
    expected = brute_solution(arr)
    test_input = f"1\n{len(arr)}\n" + " ".join(map(str, arr)) + "\n"
    process = subprocess.Popen(
        ["pypy3.10", SOLUTION_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    actual = int(stdout.strip())
    return actual == expected, f"input={arr}, expected={expected}, got={actual}"


def run_all_tests():
    samples = [
        [1, 2],
        [1, 2, 3, 3],
        [3, 0, 2, 3],
    ]
    edge_cases = [
        [0, 0],
        [5, 4, 3, 2, 1],
    ]
    tests = samples + edge_cases
    passed_all = True
    for arr in tests:
        ok, msg = run_test_case(arr)
        print(("✓" if ok else "✗"), msg)
        passed_all &= ok
    print("Overall:", "PASSED" if passed_all else "FAILED")


if __name__ == "__main__":
    run_all_tests() 