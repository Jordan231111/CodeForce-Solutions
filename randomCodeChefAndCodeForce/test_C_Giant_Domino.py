import subprocess
import sys
import time
import random

SOLUTION_FILE = "C_Giant_Domino.py"
BRUTE_FILE = "brute.py"

def run_test_case(N, S_list, expected):
    test_input = f"1\n{N}\n{' '.join(map(str, S_list))}\n"
    process = subprocess.Popen(
        ["pypy3.10", SOLUTION_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    try:
        actual = int(actual)
    except:
        actual = -999
    if actual == expected:
        return True, f"PASSED: N={N}, S={S_list}"
    else:
        return False, f"FAILED: N={N}, S={S_list}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        (4, [1,3,2,5], 4),
        (2, [1,2], 2),
        (2, [1,3], -1),
        (3, [1,2,4], 3),
        (3, [4,1,2], 2),
        (3, [1,10,3], -1),
        (4, [1,2,3,5], 4),
        # Edge case: N=2, direct decreasing
        (2, [5,1], 2),
        # Edge case: equal sizes
        (2, [1,1], 2),
        # Edge case: impossible climbing
        (3, [1,2,5], -1),  # 1->2: ok, 2->5:2>=2.5 no, 1->5 no
    ]
    results = []
    start_time = time.time()
    for params in test_cases:
        success, message = run_test_case(*params)
        results.append((success, message))
    end_time = time.time()
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    all_passed = all(success for success, _ in results)
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_n=20, num_tests=100, verbose=False):
    passed = 0
    start = time.time()
    for _ in range(num_tests):
        N = random.randint(2, max_n)
        S = [random.randint(1, 10**9) for _ in range(N)]
        test_input = f"1\n{N}\n{' '.join(map(str, S))}\n"
        proc_sol = subprocess.Popen(
            ["pypy3.10", SOLUTION_FILE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, err_sol = proc_sol.communicate(test_input)
        proc_ref = subprocess.Popen(
            ["pypy3.10", BRUTE_FILE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_ref, err_ref = proc_ref.communicate(test_input)
        if out_sol.strip() != out_ref.strip():
            print("\nMISMATCH FOUND:\nInput:\n", test_input, sep="")
            print("Output:", out_sol.strip(), "\nExpected:", out_ref.strip())
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()
    stress_test() 