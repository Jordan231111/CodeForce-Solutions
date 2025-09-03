import subprocess
import sys
import time

def run_test_case(n, s, expected=None):
    test_input = f"1\n{n}\n{s}\n"
    proc_sol = subprocess.Popen(
        ["pypy3.10", "Min_Path_Count_Hard.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out_sol, err_sol = proc_sol.communicate(test_input)
    ans_sol = out_sol.strip()
    if expected is None:
        proc_br = subprocess.Popen(
            ["pypy3.10", "brute_Min_Path_Count_Hard.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_br, err_br = proc_br.communicate(test_input)
        expected = out_br.strip()
    ok = (ans_sol == expected)
    msg = f"n={n}, s={s}, got={ans_sol}, expected={expected}"
    return ok, ("PASSED: " + msg) if ok else ("FAILED: " + msg)

def run_all_tests():
    tests = []
    tests.append((3, "011", "4"))
    tests.append((4, "0000", "20"))
    tests.append((1, "1", "1"))
    tests.append((1, "0", "1"))
    tests.append((2, "11", None))
    tests.append((2, "01", None))
    tests.append((5, "10101", None))
    results = []
    start = time.time()
    for n, s, exp in tests:
        ok, message = run_test_case(n, s, exp)
        results.append((ok, message))
    end = time.time()
    all_ok = all(x for x,_ in results)
    print("Test Results:")
    for ok, msg in results:
        print(("\u2713" if ok else "\u2717"), msg)
    print(f"\nExecution time: {end - start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_ok else 'FAILED'}")

def stress_test(max_n=8, num_tests=200, seed=0):
    import random
    random.seed(seed)
    for _ in range(num_tests):
        n = random.randint(1, max_n)
        s = ''.join(random.choice('01') for _ in range(n))
        ok, msg = run_test_case(n, s, None)
        if not ok:
            print("\nMISMATCH FOUND:")
            print(msg)
            return
    print(f"Stress testing completed: {num_tests}/{num_tests} cases passed")

if __name__ == "__main__":
    run_all_tests()
    stress_test()


