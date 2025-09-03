import subprocess
import sys
import time

def run_case(n, pts, X, Y):
    lines = ["1", str(n)]
    for x,y in pts:
        lines.append(f"{x} {y}")
    lines.append(f"{X} {Y}")
    inp = "\n".join(lines) + "\n"
    p = subprocess.Popen([
        "pypy3.10", "D_For_the_Champion.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp, timeout=5)
    return out.strip()

def run_all_tests():
    tests = []
    tests.append((1, [(0,0)], 100, 99, "100 99"))
    tests.append((4, [(1,1),(2,2),(3,3),(-1,-1)], -1, 0, "-1 0"))
    tests.append((1, [(10**9,-10**9)], -10**9, 10**9, f"{-10**9} {10**9}"))
    tests.append((100, [(i, -i) for i in range(-50,50)], 0, 0, "0 0"))

    results = []
    start = time.time()
    for n, pts, X, Y, expected in tests:
        got = run_case(n, pts, X, Y)
        ok = got == expected
        results.append((ok, f"n={n}, expected={expected}, got={got}"))
    end = time.time()

    print("Test Results:")
    for ok, msg in results:
        print(("✓" if ok else "✗") + " " + msg)
    print(f"\nExecution time: {end-start:.4f} seconds")
    print(f"Overall: {'PASSED' if all(ok for ok,_ in results) else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()


