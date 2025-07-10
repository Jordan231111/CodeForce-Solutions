import subprocess
import sys
import time
import random

def run_test_case(pairs):
    expected = str(sum(1 for a, b in pairs if b > a))
    n = len(pairs)
    test_input = f"{n}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
    
    process = subprocess.Popen(
        ["pypy3.10", "A_Task_Failed_Successfully.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    actual = stdout.strip()
    
    if actual == expected:
        return True, f"PASSED: {pairs}, output={actual}"
    else:
        return False, f"FAILED: {pairs}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        # Sample 1
        [(2,8), (5,5), (5,4), (6,7)],
        # Sample 2
        [(1,1), (1,1), (1,1), (1,1), (1,1)],
        # Sample 3
        [(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)],
        # Edge case 1: N=1, B > A
        [(1,2)],
        # Edge case 2: N=1, B == A
        [(1,1)],
        # Edge case 3: N=1, B < A
        [(2,1)],
        # Edge case 4: Max N, all B > A
        [(1,2)] * 100,
    ]
    
    results = []
    start_time = time.time()
    
    for pairs in test_cases:
        success, message = run_test_case(pairs)
        results.append((success, message))
    
    end_time = time.time()
    
    all_passed = all(success for success, _ in results)
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_n=100, num_tests=100, verbose=False):
    passed = 0
    start = time.time()
    for _ in range(num_tests):
        n = random.randint(1, max_n)
        pairs = [(random.randint(1,100), random.randint(1,100)) for _ in range(n)]
        test_input = f"{n}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"

        # Run the contestant solution
        proc_sol = subprocess.Popen(
            ["pypy3.10", "A_Task_Failed_Successfully.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, err_sol = proc_sol.communicate(test_input)

        # Run the reference (brute-force) solution
        proc_ref = subprocess.Popen(
            ["pypy3.10", "brute.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
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