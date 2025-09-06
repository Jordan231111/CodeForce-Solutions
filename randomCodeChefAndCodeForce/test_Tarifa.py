import subprocess
import sys
import time

def run_case(x, spends):
    n = len(spends)
    test_input = f"{x}\n{n}\n" + "\n".join(map(str, spends)) + "\n"
    proc = subprocess.Popen(
        ["pypy3.10", "Tarifa.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate(test_input)
    return out.strip()

def expected(x, spends):
    return str(x*(len(spends)+1) - sum(spends))

def run_all_tests():
    tests = []
    tests.append((10, [5, 15, 5]))
    tests.append((1, []))
    tests.append((100, [0]*100))
    tests.append((5, [5,5,5,5,5]))

    results = []
    start = time.time()
    for x, s in tests:
        got = run_case(x, s)
        exp = expected(x, s)
        ok = got == exp
        results.append((ok, f"x={x}, n={len(s)}, expected={exp}, got={got}"))
    end = time.time()

    print("Test Results:")
    for ok, msg in results:
        print(("✓" if ok else "✗") + " " + msg)
    all_ok = all(ok for ok, _ in results)
    print(f"\nExecution time: {end-start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_ok else 'FAILED'}")

def stress_test(max_n=1000, num_tests=100):
    import random
    for _ in range(num_tests):
        x = random.randint(1, 100)
        n = random.randint(0, 50)
        spends = [random.randint(0, 10000) for _ in range(n)]
        got = run_case(x, spends)
        exp = expected(x, spends)
        if got != exp:
            print("Mismatch:")
            print(x, n, spends)
            print("got:", got, "exp:", exp)
            return
    print("Stress testing completed with no mismatches")

if __name__ == "__main__":
    run_all_tests()


