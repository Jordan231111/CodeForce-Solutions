import subprocess
import sys
import time
import os

CPP_SOURCE = "unconventional_pairs.cpp"
BIN_NAME = "unconventional_pairs"

def compile_sources():
    subprocess.run([
        "g++-14", "-std=gnu++20", "-O2", "-pipe", CPP_SOURCE, "-o", BIN_NAME
    ], check=True)

def run_test_case(test_input, expected):
    proc = subprocess.Popen(
        [f"./{BIN_NAME}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(test_input)
    actual = stdout.strip()
    
    if actual == expected:
        return True, f"PASSED: output={actual}"
    else:
        return False, f"FAILED: expected={expected}, got={actual}"

def run_all_tests():
    compile_sources()
    
    test_cases = [
        # Sample test case 1
        ("5\n2\n1 2\n4\n10 1 2 9\n6\n3 8 9 3 3 2\n8\n5 5 5 5 5 5 5 5\n4\n-5 -1 2 6\n", "1\n1\n1\n0\n4"),
        
        # Edge case: minimum n=2
        ("1\n2\n1 1\n", "0"),
        
        # Edge case: all same values
        ("1\n4\n7 7 7 7\n", "0"),
        
        # Edge case: large differences
        ("1\n4\n-1000000000 -999999999 999999999 1000000000\n", "1"),
        
        # Edge case: consecutive integers
        ("1\n6\n1 2 3 4 5 6\n", "1"),
    ]

    results = []
    start_time = time.time()

    for i, (test_input, expected) in enumerate(test_cases, 1):
        success, message = run_test_case(test_input, expected)
        results.append((success, f"Test {i}: {message}"))

    end_time = time.time()

    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")

    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    all_passed = all(success for success, _ in results)
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
