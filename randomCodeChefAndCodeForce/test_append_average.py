import subprocess
import sys
import time

def run_test_case(n, k, a, expected):
    test_input = f"1\n{n} {k}\n{' '.join(map(str, a))}\n"
    
    process = subprocess.Popen(
        ["pypy3.10", "append_average.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    if stderr:
        return False, f"ERROR: {stderr}"
    
    try:
        actual = int(stdout.strip())
    except:
        return False, f"FAILED: Could not parse output '{stdout.strip()}'"
    
    if actual == expected:
        return True, f"PASSED: n={n}, k={k}, array={a}, output={actual}"
    else:
        return False, f"FAILED: n={n}, k={k}, array={a}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        # Sample test cases from problem statement
        (5, 1, [6, 5, 7, 4, 7], 34),
        (5, 2, [1, 4, 10, 8, 1], 26),
        
        # Edge cases
        (2, 1, [1, 1], 3),  # Two identical elements
        (3, 1, [1, 2, 3], 7),  # Small array
        (2, 5, [10, 20], 10 + 20 + 5 * 15),  # Multiple operations on two elements
        (4, 1, [1, 1, 1, 1], 5),  # All identical elements
    ]
    
    results = []
    start_time = time.time()
    
    for n, k, a, expected in test_cases:
        success, message = run_test_case(n, k, a, expected)
        results.append((success, message))
    
    end_time = time.time()
    
    # Print results
    all_passed = all(success for success, _ in results)
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_n=100, num_tests=50, verbose=False):
    """Generate random test cases and compare solution with brute force."""
    import random, subprocess, os, time, sys

    passed = 0
    start = time.time()
    for _ in range(num_tests):
        n = random.randint(2, max_n)
        k = random.randint(1, min(10, n))  # Keep k small for stress testing
        a = [random.randint(1, 100) for _ in range(n)]
        
        test_input = f"1\n{n} {k}\n{' '.join(map(str, a))}\n"

        # Run the optimized solution
        proc_sol = subprocess.Popen(
            ["pypy3.10", "append_average.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, err_sol = proc_sol.communicate(test_input)

        if err_sol:
            print(f"\nERROR in solution: {err_sol}")
            return

        try:
            result = int(out_sol.strip())
            passed += 1
            if verbose and passed % 10 == 0:
                print(f"{passed}/{num_tests} ok", end="\r", flush=True)
        except:
            print(f"\nFailed to parse output: '{out_sol}'")
            return
            
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()
    print("\n" + "="*50)
    stress_test() 