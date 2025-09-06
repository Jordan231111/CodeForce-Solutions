import subprocess
import sys
import time
import random

def compute_expected(a):
    b = sorted(a, reverse=True)
    m = 0
    i = 1
    for v in b:
        s = v + i
        if s > m:
            m = s
        i += 1
    return m + 1

def run_test_case(a):
    expected = compute_expected(a)
    n = len(a)
    test_input = f"{n}\n{' '.join(map(str, a))}\n"
    process = subprocess.Popen(
        ["pypy3.10", "Planting_Trees.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/Users/jordan/Documents/CodeForce"
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    if actual == str(expected):
        return True, f"PASSED: n={n}, a={a}, output={actual}"
    else:
        return False, f"FAILED: n={n}, a={a}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        ([2, 3, 4, 3],),
        ([1],),
        ([1, 1, 1, 1, 1, 1],),
        ([5, 4, 3, 2, 1, 1, 1],),
    ]

    results = []
    start_time = time.time()
    for (a,) in test_cases:
        success, message = run_test_case(a)
        results.append((success, message))
    end_time = time.time()

    print("Test Results:")
    all_passed = all(success for success, _ in results)
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_n=8, num_tests=100, verbose=False):
    passed = 0
    start = time.time()
    for _ in range(num_tests):
        n = random.randint(1, max_n)
        a = [random.randint(1, 10) for _ in range(n)]
        test_input = f"{n}\n{' '.join(map(str, a))}\n"

        proc_sol = subprocess.Popen(
            ["pypy3.10", "Planting_Trees.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/jordan/Documents/CodeForce"
        )
        out_sol, err_sol = proc_sol.communicate(test_input)

        proc_ref = subprocess.Popen(
            ["pypy3.10", "brute_planting_trees.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/jordan/Documents/CodeForce"
        )
        out_ref, err_ref = proc_ref.communicate(test_input)

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
    stress_test()


