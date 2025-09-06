import subprocess
import random

SOL = "Sort_Points_MultipleN.py"
BRUTE = "brute_Sort_Points_MultipleN.py"


def run_case(n, k, p):
    test_input = f"{n} {k}\n" + " ".join(map(str, p)) + "\n"
    proc = subprocess.Popen([
        "pypy3.10", SOL
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(test_input)
    return out.strip()


def run_bruteforce(n, k, p):
    test_input = f"{n} {k}\n" + " ".join(map(str, p)) + "\n"
    proc = subprocess.Popen([
        "pypy3.10", BRUTE
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(test_input)
    return out.strip()


def sample_tests():
    cases = []
    n, k = 3, 2
    p = [1, 6, 5, 3, 2, 4]
    cases.append((n, k, p, "2"))

    n, k = 1, 1
    p = [1]
    cases.append((n, k, p, "0"))

    results = []
    for n, k, p, expected in cases:
        got = run_case(n, k, p)
        results.append((got == expected, f"Sample n={n},k={k}: expected={expected}, got={got}"))
    return results


def edge_tests():
    results = []
    n, k = 2, 1
    p = [2, 1]
    results.append((run_case(n, k, p) == run_bruteforce(n, k, p), "Edge small n=2"))
    return results


def stress_tests(num=30):
    results = []
    for _ in range(num):
        n = random.randint(1, 3)
        k = random.randint(1, 3)
        m = n * k
        p = list(range(1, m + 1))
        random.shuffle(p)
        got = run_case(n, k, p)
        exp = run_bruteforce(n, k, p)
        results.append((got == exp, f"Stress n={n} k={k}: got={got}, exp={exp}"))
        if got != exp:
            break
    return results


def run_all():
    tests = []
    tests += sample_tests()
    tests += edge_tests()
    tests += stress_tests(20)

    ok = all(s for s, _ in tests)
    print("Test Results:")
    for s, msg in tests:
        print(f"{'✓' if s else '✗'} {msg}")
    print(f"Overall: {'PASSED' if ok else 'FAILED'}")


if __name__ == "__main__":
    run_all()


