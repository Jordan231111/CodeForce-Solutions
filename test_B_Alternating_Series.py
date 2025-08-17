import subprocess
import sys
import time

def generate_expected(n):
    a = []
    for i in range(n):
        a.append(-1 if (i & 1) == 0 else 3)
    if (n & 1) == 0:
        a[-1] = 2
    return ' '.join(map(str,a))

def run_case(n):
    test_input = f"1\n{n}\n"
    p = subprocess.Popen([
        "pypy3.10", 
        "B_Alternating_Series.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate(test_input, timeout=5)
    out = out.strip()
    exp = generate_expected(n)
    return (out == exp), f"n={n}, expected='{exp}', got='{out}'"

def run_all_tests():
    tests = [2,3,4,5,10]
    results = []
    start = time.time()
    for n in tests:
        ok, msg = run_case(n)
        results.append((ok,msg))
    end = time.time()
    print("Test Results:")
    all_ok = True
    for ok, msg in results:
        mark = '✓' if ok else '✗'
        print(f"{mark} {msg}")
        all_ok &= ok
    print(f"\nExecution time: {end-start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_ok else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()


