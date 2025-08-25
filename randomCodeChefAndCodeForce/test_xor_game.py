import subprocess
import sys
import time

def run_test_case(test_input, expected_output):
    process = subprocess.Popen(
        ["pypy3.10", "xor_game.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    if stderr:
        return False, f"ERROR: {stderr}"
    
    actual_lines = stdout.strip().split('\n')
    expected_lines = expected_output.strip().split('\n')
    
    if actual_lines == expected_lines:
        return True, f"PASSED: output={stdout.strip()}"
    else:
        return False, f"FAILED: expected={expected_output.strip()}, got={stdout.strip()}"

def run_all_tests():
    test_cases = [
        # Sample test cases from problem statement
        ("""5
2
1 1
2
1 2
4
1 0 3 4
4
16 17 18 19
9
15 27 18 23 99 64 16 0 37""", """0
2
3
1
36"""),
    ]
    
    results = []
    start_time = time.time()
    
    for test_input, expected_output in test_cases:
        success, message = run_test_case(test_input, expected_output)
        results.append((success, message))
    
    end_time = time.time()
    
    # Print results
    all_passed = all(success for success, _ in results)
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()
