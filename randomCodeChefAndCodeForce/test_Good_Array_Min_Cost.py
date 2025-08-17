import subprocess
import sys
import time
import random


def run_case(n, k):
    test_input = f"1\n{n} {k}\n"
    proc = subprocess.Popen(
        ["pypy3.10", "Good_Array_Min_Cost.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate(test_input)
    return out.strip()


def brute_min_cost(n, k):
    best = None

    def dfs(i, rem, prev):
        nonlocal best
        if i == n:
            if rem == 0:
                best = min(best, 0) if best is not None else 0
            return
        if rem < n - i:
            return
        start = 1
        end = rem - (n - i - 1)
        if end > 20:
            end = 20
        for x in range(start, end + 1):
            cost_here = (prev & x) if prev is not None else 0
            if best is not None and cost_here >= best:
                pass
            dfs(i + 1, rem - x, x)

    dfs(0, k, None)
    if best is None:
        return None
    return str(best)


def run_all_tests():
    cases = [
        (1, 2, "0"),
        (2, 3, "0"),
        (4, 5, "1"),
        (5, 5, "4"),
        (5, 6, "2"),
        (6, 100, "0"),
    ]

    results = []
    start = time.time()
    for n, k, expected in cases:
        got = run_case(n, k)
        ok = got == expected
        results.append((ok, f"n={n}, k={k}, got={got}, expected={expected}"))

    random.seed(0)
    for _ in range(30):
        n = random.randint(1, 6)
        k = random.randint(n, 12)
        got = run_case(n, k)
        exp = brute_min_cost(n, k)
        ok = got == exp
        results.append((ok, f"RANDOM n={n}, k={k}, got={got}, expected={exp}"))

    end = time.time()

    print("Test Results:")
    all_ok = True
    for ok, msg in results:
        mark = "\u2713" if ok else "\u2717"
        print(f"{mark} {msg}")
        all_ok &= ok
    print(f"\nExecution time: {end - start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_ok else 'FAILED'}")


if __name__ == "__main__":
    run_all_tests()


