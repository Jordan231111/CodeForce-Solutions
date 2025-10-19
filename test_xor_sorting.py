import subprocess
import sys
import time
import os

CPP_SOURCE = "xor_sorting.cpp"
BIN_NAME = "xor_sorting"

def compile_sources():
    subprocess.run([
        "g++-14", "-std=gnu++20", "-O2", "-pipe", CPP_SOURCE, "-o", BIN_NAME
    ], check=True)

def compute_f(arr):
    """Compute f(arr) - minimum K to sort array"""
    n = len(arr)
    if arr == sorted(arr):
        return 0
    
    for k in range(2 * n):
        test_arr = arr[:]
        for _ in range(n * n):
            sorted_flag = True
            for i in range(n - 1):
                if test_arr[i] > test_arr[i + 1]:
                    sorted_flag = False
                    if (test_arr[i] ^ test_arr[i + 1]) <= k:
                        test_arr[i], test_arr[i + 1] = test_arr[i + 1], test_arr[i]
            if sorted_flag:
                return k
    return -1

def run_test_case(n, k):
    test_input = f"1\n{n} {k}\n"
    
    proc = subprocess.Popen(
        [f"./{BIN_NAME}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(test_input)
    
    output = stdout.strip()
    
    if output == "-1":
        return True, f"N={n}, K={k}: No solution (output -1)"
    
    try:
        arr = list(map(int, output.split()))
        
        if len(arr) != n:
            return False, f"N={n}, K={k}: Wrong length {len(arr)}"
        
        if sorted(arr) != list(range(1, n + 1)):
            return False, f"N={n}, K={k}: Not a permutation"
        
        f_val = compute_f(arr)
        
        if f_val == k:
            return True, f"N={n}, K={k}: PASSED (array={arr}, f={f_val})"
        else:
            return False, f"N={n}, K={k}: FAILED (array={arr}, f={f_val}, expected={k})"
    
    except Exception as e:
        return False, f"N={n}, K={k}: Parse error - {e}"

def run_all_tests():
    compile_sources()
    
    test_cases = [
        (4, 0),
        (2, 2),
        (5, 4),
        (6, 7),
        (1, 0),
        (3, 3),
        (3, 2),
        (4, 5),
        (5, 1),
    ]
    
    results = []
    start_time = time.time()
    
    for n, k in test_cases:
        success, message = run_test_case(n, k)
        results.append((success, message))
    
    end_time = time.time()
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    all_passed = all(success for success, _ in results)
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()

