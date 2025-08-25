import subprocess
import sys
import time

def run_test_case(n, arr):
    expected = None
    from collections import Counter
    c = Counter(arr)
    mx = max(c.values())
    c1 = c.get(1,0)
    expected = str(min(n - c1, 1 + n - mx))
    test_input = f"1\n{n}\n" + " ".join(map(str, arr)) + "\n"
    process = subprocess.Popen([
        "pypy3.10", "Fence_Colouring.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    return (actual == expected, f"n={n}, arr={arr[:10]}{'...' if len(arr)>10 else ''}, expected={expected}, got={actual}")

def run_all_tests():
    tests = []
    tests.append((5, [1,2,3,4,5]))
    tests.append((4, [2,2,2,2]))
    tests.append((6, [1,1,1,1,1,1]))
    tests.append((6, [2,1,2,1,2,1]))
    tests.append((2, [2,1]))
    results = []
    start = time.time()
    for n, arr in tests:
        ok, msg = run_test_case(n, arr)
        results.append((ok, msg))
    end = time.time()
    print("Test Results:")
    for ok, msg in results:
        print(("\u2713" if ok else "\u2717") + " " + msg)
    print(f"\nExecution time: {end-start:.4f} seconds")
    print("Overall:", "PASSED" if all(ok for ok,_ in results) else "FAILED")

if __name__ == "__main__":
    run_all_tests()

