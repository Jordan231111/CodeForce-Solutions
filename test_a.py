import subprocess
import sys
import time

def expected_formula(n: int) -> int:
    m3 = (n - 1) // 3
    m5 = (n - 1) // 5
    m15 = (n - 1) // 15
    return 3 * m3 * (m3 + 1) // 2 + 5 * m5 * (m5 + 1) // 2 - 15 * m15 * (m15 + 1) // 2

def expected_brut(n: int) -> int:
    return sum(i for i in range(1, n) if i % 3 == 0 or i % 5 == 0)

def run_test_case(n: int):
    test_input = f"{n}\n"
    process = subprocess.Popen(
        ["pypy3.10", "a.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/Users/jordan/Documents/CodeForce",
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    expected = str(expected_formula(n))
    if actual == expected:
        return True, f"PASSED: n={n}, output={actual}"
    else:
        return False, f"FAILED: n={n}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        1,
        2,
        3,
        5,
        6,
        10,
        100,
        1000,
        10**6 + 1,
    ]

    results = []
    start_time = time.time()
    for n in test_cases:
        success, message = run_test_case(n)
        results.append((success, message))
    end_time = time.time()

    all_passed = all(success for success, _ in results)
    print("Test Results:")
    for success, message in results:
        mark = '✓' if success else '✗'
        print(f"{mark} {message}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_n: int = 10000, num_tests: int = 200, verbose: bool = False):
    import random

    passed = 0
    start = time.time()
    for t in range(num_tests):
        n = random.randint(1, max_n)
        brute = expected_brut(n)
        fast = expected_formula(n)
        if brute != fast:
            print("\nMISMATCH FOUND:\nInput:\n", n, sep="")
            print("Expected (brute):", brute, "\nGot (formula):", fast)
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()
    stress_test()

 