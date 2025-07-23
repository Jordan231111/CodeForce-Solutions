import subprocess
import sys
import time

def run_test_case(test_input, expected):
    process = subprocess.Popen(
        ["pypy3.10", "t.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    actual = stdout.strip()
    
    if actual == expected:
        return True, f"PASSED: output={actual}"
    else:
        return False, f"FAILED: expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        ("1 1\n1 1 1 2\n", "499122177"),
        ("0 1\n", "0"),
        ("2 2\n1 1 1 2\n2 2 1 2\n", "748683265"),
    ]
    
    results = []
    start_time = time.time()
    
    for tin, exp in test_cases:
        success, message = run_test_case(tin, exp)
        results.append((success, message))
    
    end_time = time.time()
    
    all_passed = all(s for s,_ in results)
    print("Test Results:")
    for s, msg in results:
        print(f"{'✓' if s else '✗'} {msg}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")


def stress_test(max_m=20, max_n=10, num_tests=100, verbose=False):
    import random, subprocess, time
    passed = 0
    start = time.time()
    for _ in range(num_tests):
        m = random.randint(1, max_m)
        n = random.randint(0, max_n)
        test_input = f"{n} {m}\n"
        for __ in range(n):
            l = random.randint(1, m)
            r = random.randint(l, m)
            q = random.randint(2, 1000)
            p = random.randint(1, q-1)
            test_input += f"{l} {r} {p} {q}\n"
        
        proc_sol = subprocess.Popen(
            ["pypy3.10", "t.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, _ = proc_sol.communicate(test_input)
        
        proc_ref = subprocess.Popen(
            ["pypy3.10", "brute.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_ref, _ = proc_ref.communicate(test_input)
        
        if out_sol.strip() != out_ref.strip():
            print("\nMISMATCH FOUND:\nInput:\n", test_input)
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