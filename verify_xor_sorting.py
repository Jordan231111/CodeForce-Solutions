import subprocess
import random
from itertools import permutations

CPP_SOURCE = "xor_sorting.cpp"
BIN_NAME = "xor_sorting"

def compile_sources():
    subprocess.run([
        "g++-14", "-std=gnu++20", "-O2", "-pipe", CPP_SOURCE, "-o", BIN_NAME
    ], check=True, capture_output=True)

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

def get_solution(n, k):
    """Get solution from our program"""
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
        return None
    
    try:
        arr = list(map(int, output.split()))
        if len(arr) == n and sorted(arr) == list(range(1, n + 1)):
            return arr
    except:
        pass
    return None

def brute_force_solution(n, k):
    """Find if any permutation has f(perm) = k"""
    if n > 7:
        return None
    
    for perm in permutations(range(1, n + 1)):
        if compute_f(list(perm)) == k:
            return list(perm)
    return None

def find_counterexamples():
    compile_sources()
    
    print("Searching for counterexamples (cases where solution exists but we output -1)...\n")
    
    counterexamples = []
    
    for n in range(1, 8):
        for k in range(0, min(20, 2 * n)):
            our_solution = get_solution(n, k)
            brute_solution = brute_force_solution(n, k)
            
            if our_solution is None and brute_solution is not None:
                counterexamples.append((n, k, brute_solution))
                print(f"❌ COUNTEREXAMPLE: N={n}, K={k}")
                print(f"   We output: -1")
                print(f"   Valid solution exists: {brute_solution}")
                print(f"   Verification: f({brute_solution}) = {compute_f(brute_solution)}")
                print()
            elif our_solution is not None and brute_solution is None:
                print(f"⚠️  WARNING: N={n}, K={k}")
                print(f"   We output: {our_solution}")
                print(f"   But f({our_solution}) = {compute_f(our_solution)}")
                print()
            elif our_solution is not None:
                f_val = compute_f(our_solution)
                if f_val != k:
                    print(f"⚠️  INCORRECT: N={n}, K={k}")
                    print(f"   We output: {our_solution}")
                    print(f"   But f({our_solution}) = {f_val}")
                    print()
    
    if not counterexamples:
        print("✓ No counterexamples found for N ≤ 7, K < 20!")
        print("  The solution appears correct for small cases.")
    else:
        print(f"\nFound {len(counterexamples)} counterexamples")
    
    return counterexamples

if __name__ == "__main__":
    find_counterexamples()

