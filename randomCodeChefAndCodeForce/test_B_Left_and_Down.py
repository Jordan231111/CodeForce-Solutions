import subprocess
import sys
import time
import math

SOL_FILE = "B_Left_and_Down.py"


def expected_cost(a, b, k):
    g = math.gcd(a, b)
    thr = max((a + k - 1) // k, (b + k - 1) // k)
    return 1 if g >= thr else 2


def run_test_case(a, b, k):
    test_input = f"1\n{a} {b} {k}\n"
    process = subprocess.Popen(
        ["pypy3.10", SOL_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    expected = str(expected_cost(a, b, k))
    if actual == expected:
        return True, f"PASSED: ({a}, {b}, {k}) => {actual}"
    else:
        msg = f"FAILED: ({a}, {b}, {k}) expected {expected}, got {actual}"
        if stderr:
            msg += f" | stderr: {stderr.strip()}"
        return False, msg


def run_all_tests():
    test_cases = [
        (3, 5, 15),
        (2, 3, 1),
        (12, 18, 8),
        (9, 7, 5),
        (1, 1, 1),
        (10 ** 18, 1, 1),
    ]
    results = []
    start_time = time.time()
    for a, b, k in test_cases:
        success, message = run_test_case(a, b, k)
        results.append((success, message))
    end_time = time.time()
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    all_passed = all(s for s, _ in results)
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")


if __name__ == "__main__":
    run_all_tests() 