
import subprocess
import sys
import time

def run_test_case(test_input, expected):
    # Run the solution
    process = subprocess.Popen(
        ["pypy3.10", "sugar_limit.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    # Check output
    actual = stdout.strip()
    
    if actual == expected:
        return True, f"PASSED: output={actual}"
    else:
        return False, f"FAILED: expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        # Sample test case 3
        ("1\n1\n1\n9\n", "0"),
        # Edge case: all negative A
        ("1\n2\n-3 -4\n1 2\n", "0"),
        # Edge case: single positive with B=3, A=5
        ("1\n1\n5\n3\n", "2"),
        # Edge case: single positive with B=0, A=10
        ("1\n1\n10\n0\n", "10"),
        # Another edge case: multiple, including negative and zero; max satisfaction 5 by choosing I=1 and eating the snack with A=6, B=1.
        ("1\n4\n6 -2 0 4\n1 2 3 5\n", "5"),
        # But let's calculate, suppose I=1, only 6, 6-1=5
        # If I=5, 6>5 B=1<=5, -2>5 no, 0>5 no, 4>5 no, 6-5=1
        # Yes, max 5
    ]
    
    results = []
    start_time = time.time()
    
    for test_input, expected in test_cases:
        success, message = run_test_case(test_input, expected)
        results.append((success, message))
    
    end_time = time.time()
    
    # Print results
    all_passed = all(success for success, _ in results)
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

# ---- New helper for randomised stress testing ----
def stress_test(max_n=10**5, num_tests=100, verbose=False):
    """Generate random test cases and compare solution with reference."""
    import random, subprocess, os, time, sys

    passed = 0
    start = time.time()
    for _ in range(num_tests):
        # Generate random test case
        n = random.randint(1, 100)
        a = [random.randint(-100, 100) for _ in range(n)]
        b = [random.randint(0, 100) for _ in range(n)]
        test_input = f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"
        
        # Run the contestant solution
        proc_sol = subprocess.Popen(
            ["pypy3.10", "sugar_limit.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, err_sol = proc_sol.communicate(test_input)

        # Compute reference by brute force (same logic, since small N)
        ans = 0
        for I in range(101):
            sum_a = 0
            cnt = 0
            for j in range(n):
                if b[j] <= I and a[j] > I:
                    sum_a += a[j]
                    cnt += 1
            val = sum_a - cnt * I
            ans = max(ans, val)
        out_ref = str(ans)

        if out_sol.strip() != out_ref:
            print("\nMISMATCH FOUND:\nInput:\n", test_input, sep="")
            print("Output:", out_sol.strip(), "\nExpected:", out_ref)
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()
    stress_test(num_tests=100) 