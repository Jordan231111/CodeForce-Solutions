import subprocess
import sys
import time
import random

def run_test_case(n):
    test_input = f"1\n{n} 3\n"
    proc_sol = subprocess.Popen(
        ["pypy3.10", "Permutation_Counting_Easy.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out_sol, err_sol = proc_sol.communicate(test_input)

    proc_ref = subprocess.Popen(
        ["pypy3.10", "brute_Permutation_Counting_Easy.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out_ref, err_ref = proc_ref.communicate(test_input)

    actual = out_sol.strip()
    expected = out_ref.strip()
    if expected == "-1":
        return True, f"SKIPPED-BRUTE: n={n}, output={actual}"
    if actual == expected:
        return True, f"PASSED: n={n}, output={actual}"
    else:
        return False, f"FAILED: n={n}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [2,3,4,5,6,7,8,9]
    results = []
    start_time = time.time()
    for n in test_cases:
        success, message = run_test_case(n)
        results.append((success, message))
    end_time = time.time()
    all_passed = all(success for success, _ in results)
    print("Test Results:")
    for success, message in results:
        tick = '✓' if success else '✗'
        print(f"{tick} {message}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def run_samples():
    samples = {
        2: "0",
        3: "2",
        4: "4",
        6: "80",
        10: "252292730",
    }
    print("\nSample Checks:")
    all_ok = True
    for n, expected in samples.items():
        test_input = f"1\n{n} 3\n"
        proc_sol = subprocess.Popen(
            ["pypy3.10", "Permutation_Counting_Easy.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, _ = proc_sol.communicate(test_input)
        actual = out_sol.strip()
        ok = (actual == expected)
        all_ok &= ok
        tick = '✓' if ok else '✗'
        print(f"{tick} n={n}, expected={expected}, got={actual}")
    print("Samples:", "PASSED" if all_ok else "FAILED")

def stress_test(max_n=9, num_tests=100):
    for _ in range(num_tests):
        n = random.randint(2, max_n)
        ok, msg = run_test_case(n)
        if not ok:
            print(msg)
            return
    print(f"Stress testing completed: {num_tests}/{num_tests} cases passed")

if __name__ == "__main__":
    run_all_tests()
    run_samples()

import subprocess
import sys
import time

def run_test_case(N, K, expected):
    test_input = f"1\n{N} {K}\n"
    
    process = subprocess.Popen(
        ["pypy3.10", "Permutation_Counting_Easy.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    if stderr:
        return False, f"FAILED: N={N}, K={K}, stderr={stderr.strip()}"
    
    actual = stdout.strip()
    
    if actual == str(expected):
        return True, f"PASSED: N={N}, K={K}, output={actual}"
    else:
        return False, f"FAILED: N={N}, K={K}, expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        (2, 3, 0),
        (3, 3, 2),
        (4, 3, 4),
        (6, 3, 80),
        (10, 3, 72576),
        (190000, 3, 252292730),
        (1, 3, 1),
        (5, 3, 8)
    ]
    
    results = []
    start_time = time.time()
    
    for N, K, expected in test_cases:
        success, message = run_test_case(N, K, expected)
        results.append((success, message))
    
    end_time = time.time()
    
    all_passed = all(success for success, _ in results)
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def brute_force_small(N, K):
    """Brute force solution for small N to verify correctness"""
    from itertools import permutations
    
    count = 0
    for perm in permutations(range(1, N+1)):
        valid = True
        for i in range(len(perm) - 1):
            if (perm[i] + perm[i+1]) % K == 0:
                valid = False
                break
        if valid:
            count += 1
    return count % 998244353

def verify_small_cases():
    print("\nVerifying small cases with brute force:")
    for N in range(1, 8):
        K = 3
        brute_result = brute_force_small(N, K)
        
        test_input = f"1\n{N} {K}\n"
        process = subprocess.Popen(
            ["pypy3.10", "Permutation_Counting_Easy.py"], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(test_input)
        
        if stderr:
            print(f"✗ N={N}: Error in solution - {stderr.strip()}")
            continue
            
        actual = int(stdout.strip())
        
        if actual == brute_result:
            print(f"✓ N={N}: {actual} (matches brute force)")
        else:
            print(f"✗ N={N}: expected {brute_result} (brute), got {actual} (solution)")

if __name__ == "__main__":
    run_all_tests()
    verify_small_cases()
