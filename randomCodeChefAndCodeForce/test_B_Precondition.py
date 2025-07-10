import subprocess
import sys
import time
import random

alpall = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def check_condition(S, T):
    for i in range(1, len(S)):
        if S[i].isupper() and S[i-1] not in T:
            return "No"
    return "Yes"

def run_test_case(S, T):
    expected = check_condition(S, T)
    test_input = f"{S}\n{T}\n"
    
    process = subprocess.Popen(
        ["pypy3.10", "B_Precondition.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    actual = stdout.strip()
    
    if actual == expected:
        return True, f"PASSED: S='{S}', T='{T}', output={actual}"
    else:
        return False, f"FAILED: S='{S}', T='{T}', expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        ("AtCoder", "Total"),  # Sample 1
        ("aBCdE", "abcdcba"),  # Sample 2
        ("abcde", "XYZ"),      # Sample 3
        # Edge cases
        ("AB", "A"),          # Edge: Uppercase preceded by matching uppercase
        ("AB", "a"),          # Edge: Case mismatch in check
        ("A", "X"),           # Edge: Single character
        ("aB", "a"),          # Edge: Lower preceded upper
        ("AA", "B")           # Edge: Same letters but not in T
    ]
    
    results = []
    start_time = time.time()
    
    for S, T in test_cases:
        success, message = run_test_case(S, T)
        results.append((success, message))
    
    end_time = time.time()
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    all_passed = all(success for success, _ in results)
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

# ---- New helper for randomised stress testing ----
def stress_test(num_tests=100, verbose=False):
    """Generate random test cases and verify solution."""
    passed = 0
    start = time.time()
    for _ in range(num_tests):
        n = random.randint(1, 100)
        m = random.randint(1, 100)
        S = ''.join(random.choice(alpall) for _ in range(n))
        T = ''.join(random.choice(alpall) for _ in range(m))
        test_input = f"{S}\n{T}\n"

        expected = check_condition(S, T)

        proc_sol = subprocess.Popen(
            ["pypy3.10", "B_Precondition.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, err_sol = proc_sol.communicate(test_input)
        out_sol = out_sol.strip()

        if out_sol != expected:
            print("\nMISMATCH FOUND:\nInput:\n", test_input, sep="")
            print("Output:", out_sol, "\nExpected:", expected)
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()
    stress_test() 