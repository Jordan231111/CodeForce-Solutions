import subprocess
import sys
import time
import random

SOLUTION_FILE = "Grid_Journey_Sum_Min_Flips.py"

def expected_sum(n, a, b):
    sa = [0]*(n+1)
    sb = [0]*(n+1)
    for i in range(1, n+1):
        sa[i] = sa[i-1] + (1 if a[i-1]=='1' else 0)
        sb[i] = sb[i-1] + (1 if b[i-1]=='1' else 0)
    ans = 0
    for x in range(1, n+1):
        for y in range(1, n+1):
            s = sa[x] + sb[y]
            ans += min(s, x + y - s)
    return str(ans)

def run_solution(n, a, b):
    test_input = f"1\n{n}\n{a}\n{b}\n"
    process = subprocess.Popen(
        ["pypy3.10", SOLUTION_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    return stdout.strip()

def run_test_case(n, a, b):
    expected = expected_sum(n, a, b)
    actual = run_solution(n, a, b)
    if actual == expected:
        return True, f"PASSED: n={n}, a={a}, b={b}, output={actual}"
    else:
        return False, f"FAILED: n={n}, a={a}, b={b}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = []
    test_cases.append((2, "11", "00"))
    test_cases.append((2, "01", "01"))
    test_cases.append((4, "1010", "1101"))
    test_cases.append((1, "0", "0"))
    test_cases.append((1, "1", "0"))

    results = []
    start_time = time.time()
    for n, a, b in test_cases:
        success, message = run_test_case(n, a, b)
        results.append((success, message))
    end_time = time.time()

    print("Test Results:")
    check = "\u2713"
    cross = "\u2717"
    for success, message in results:
        print(f"{check if success else cross} {message}")
    all_passed = all(s for s, _ in results)
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_n=50, num_tests=200, verbose=False):
    passed = 0
    start = time.time()
    for _ in range(num_tests):
        n = random.randint(1, max_n)
        a = ''.join(random.choice('01') for _ in range(n))
        b = ''.join(random.choice('01') for _ in range(n))
        test_input = f"1\n{n}\n{a}\n{b}\n"

        proc_sol = subprocess.Popen(
            ["pypy3.10", SOLUTION_FILE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, _ = proc_sol.communicate(test_input)

        proc_ref = subprocess.Popen(
            ["pypy3.10", "brute.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_ref, _ = proc_ref.communicate(test_input)

        if out_sol.strip() != out_ref.strip():
            print("\nMISMATCH FOUND:\nInput:\n", test_input, sep="")
            print("Output:", out_sol, "\nExpected:", out_ref)
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()


