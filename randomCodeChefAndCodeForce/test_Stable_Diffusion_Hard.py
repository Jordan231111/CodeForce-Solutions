import subprocess
import sys
import time
import random


def run_case(a):
    t_input = "1\n{}\n{}\n".format(len(a), " ".join(map(str, a)))
    p = subprocess.Popen([
        "pypy3.10", 
        "/Users/jordan/Documents/CodeForce/Stable_Diffusion_Hard.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(t_input)
    return out.strip()


def brute(a):
    p = subprocess.Popen([
        "pypy3.10", 
        "/Users/jordan/Documents/CodeForce/brute_Stable_Diffusion_Hard.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Directly import could be faster, but keep process isolation
    import importlib.util, runpy, os, tempfile
    # Fallback: compute in-process
    from brute_Stable_Diffusion_Hard import brute_count
    return str(brute_count(a))


def run_samples():
    samples = [
        ([1,2], "3"),
        ([2,1,2,1,2], "13"),
        ([1,2,2,1,2,1], "20"),
    ]
    results = []
    for a, expected in samples:
        got = run_case(a)
        results.append((got == expected, f"sample a={a} expected={expected} got={got}"))
    return results


def edge_tests():
    cases = [
        [1],
        [2],
        [1,1,1,1,1,1],
        [2,2,2,2,2],
        [1,2,1,2],
        [2,1,2,1],
    ]
    results = []
    from brute_Stable_Diffusion_Hard import brute_count
    for a in cases:
        expected = str(brute_count(a))
        got = run_case(a)
        results.append((got == expected, f"edge a={a} expected={expected} got={got}"))
    return results


def stress_tests(num=200):
    results = []
    from brute_Stable_Diffusion_Hard import brute_count
    for _ in range(num):
        n = random.randint(1, 30)
        a = [random.randint(1,2) for __ in range(n)]
        expected = str(brute_count(a))
        got = run_case(a)
        if got != expected:
            results.append((False, f"MISMATCH a={a} expected={expected} got={got}"))
            break
        results.append((True, f"ok n={n}"))
    return results


def main():
    results = []
    results += run_samples()
    results += edge_tests()
    results += stress_tests(200)
    all_ok = all(ok for ok, _ in results)
    print("Test Results:")
    for ok, msg in results:
        print(("✓" if ok else "✗"), msg)
    print("Overall:", "PASSED" if all_ok else "FAILED")


if __name__ == "__main__":
    main()


