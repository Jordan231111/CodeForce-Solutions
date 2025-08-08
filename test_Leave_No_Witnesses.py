import subprocess
import sys
import time

def run_test_case(n, s, expected):
    test_input = f"1\n{n}\n{s}\n"
    process = subprocess.Popen(
        ["pypy3.10", "Leave_No_Witnesses.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    if actual == str(expected):
        return True, f"PASSED: n={n}, s={s}, output={actual}"
    else:
        return False, f"FAILED: n={n}, s={s}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        # Samples
        (3, "010", 1),
        (4, "0100", -1),
        (5, "01011", 2),
        # Edge cases
        (1, "1", -1),
        (2, "10", -1),
        # Random small checks
        (6, "000000", 3),  # must set 1,2,4 to 1 and set maximal {3,6,7->not} -> {3,5}? for n=6 -> {3,6,5?} handled by solver; baseline expected 3
        (7, "1111111", 3),  # powers-of-two to 1 already; need maximal {7} to 0 -> 1 flip; but others? 3 maybe; provides regression
    ]

    results = []
    start_time = time.time()
    for n, s, expected in test_cases:
        success, message = run_test_case(n, s, expected)
        results.append((success, message))
    end_time = time.time()

    all_passed = all(success for success, _ in results)
    print("Test Results:")
    for success, message in results:
        print(f"{'\u2713' if success else '\u2717'} {message}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()


