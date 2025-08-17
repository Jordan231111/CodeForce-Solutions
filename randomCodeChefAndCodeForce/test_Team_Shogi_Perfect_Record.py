import subprocess
import sys
import time
import random

SOLUTION = "Team_Shogi_Perfect_Record.py"

def expected_ans(n, m):
    return str(n * (m // 2) + (m % 2))

def run_test_case(n, m):
    test_input = f"1\n{n} {m}\n"
    process = subprocess.Popen(
        ["pypy3.10", SOLUTION],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    expected = expected_ans(n, m)
    if actual == expected:
        return True, f"PASSED: n={n}, m={m}, output={actual}"
    else:
        return False, f"FAILED: n={n}, m={m}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        (3, 3),
        (5, 1),
        (2, 10**9),
        (10**9, 1),
        (2, 2),
        (7, 1000000001),
    ]

    results = []
    start_time = time.time()

    for n, m in test_cases:
        success, message = run_test_case(n, m)
        results.append((success, message))

    end_time = time.time()

    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")

    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    all_passed = all(success for success, _ in results)
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed

def stress_test(num_tests=100):
    for _ in range(num_tests):
        n = random.randint(1, 10**9)
        m = random.randint(1, 10**9)
        ok, msg = run_test_case(n, m)
        if not ok:
            print("Mismatch:", msg)
            return
    print(f"Stress test: {num_tests}/{num_tests} passed")

if __name__ == "__main__":
    run_all_tests()


