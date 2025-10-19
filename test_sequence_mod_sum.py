import subprocess
import sys
import time


def run_solution(inp: str) -> str:
    proc = subprocess.Popen(
        ["pypy3.10", "sequence_mod_sum.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate(inp, timeout=5)
    if proc.returncode != 0:
        raise RuntimeError(f"Solution exited with {proc.returncode}: {err}")
    return out.strip()


def run_brute(inp: str) -> str:
    proc = subprocess.Popen(
        ["python3", "brute_sequence_mod_sum.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate(inp, timeout=5)
    if proc.returncode != 0:
        raise RuntimeError(f"Brute exited with {proc.returncode}: {err}")
    return out.strip()


def sample_tests():
    sample_input = "2\n5 3\n2 3\n"
    brute_out = run_brute(sample_input)
    actual = run_solution(sample_input)
    ok = True
    b_lines = [list(map(int, ln.split())) for ln in brute_out.splitlines()]
    a_lines = [list(map(int, ln.split())) for ln in actual.splitlines()]
    if len(b_lines) != len(a_lines):
        ok = False
    else:
        for b, a in zip(b_lines, a_lines):
            if a[-1] != b[-1]:
                ok = False
                break
    return ok, f"Sample test last values: brute={brute_out!r}, sol={actual!r}"


def edge_tests():
    tests = [
        ("1\n2 0\n", "1 1"),
        ("1\n2 1\n", "2 3"),
        ("1\n3 0\n", "1 1 1"),
        ("1\n3 1\n", None),
        ("1\n4 6\n", None),
    ]
    results = []
    for inp, expected in tests:
        actual = run_solution(inp)
        if expected is None:
            # Validate constraints: sum of mods equals k and non-decreasing
            arr = list(map(int, actual.split()))
            n_k = list(map(int, inp.split()))
            n, k = n_k[-2], n_k[-1]
            ok = True
            if len(arr) != n:
                ok = False
            if any(arr[i] > arr[i+1] for i in range(n-1)):
                ok = False
            s = 0
            for i in range(n-1):
                s += arr[i+1] % arr[i]
            if s != k:
                ok = False
            results.append((ok, f"Edge check n={n},k={k}: got={actual!r}, sum={s}"))
        else:
            ok = actual == expected
            results.append((ok, f"Edge test input={inp.strip()}: expected={expected!r}, got={actual!r}"))
    return results


def stress_test(iterations=50, max_n=6, max_k=20):
    import random

    for _ in range(iterations):
        n = random.randint(2, max_n)
        k = random.randint(0, max_k)
        inp = f"1\n{n} {k}\n"
        brute_out = run_brute(inp).strip()
        sol_out = run_solution(inp).strip()
        b_arr = list(map(int, brute_out.split()))
        s_arr = list(map(int, sol_out.split()))
        if b_arr[-1] != s_arr[-1]:
            msg = f"Mismatch last for n={n}, k={k}: brute_last={b_arr[-1]}, sol_last={s_arr[-1]}"
            return False, msg
        ok = True
        if any(s_arr[i] > s_arr[i+1] for i in range(len(s_arr)-1)):
            ok = False
        s = 0
        for i in range(len(s_arr)-1):
            s += s_arr[i+1] % s_arr[i]
        if s != k:
            ok = False
        if not ok:
            return False, f"Constraint failure n={n},k={k}, arr={sol_out} sum={s}"
    return True, f"Stress test passed for {iterations} cases"


def run_all():
    print("Running tests...")
    all_results = []
    ok, msg = sample_tests()
    all_results.append((ok, msg))
    for res in edge_tests():
        all_results.append(res)
    ok, msg = stress_test()
    all_results.append((ok, msg))

    passed = True
    for ok, msg in all_results:
        symbol = "✓" if ok else "✗"
        print(f"{symbol} {msg}")
        if not ok:
            passed = False

    print("Overall:", "PASSED" if passed else "FAILED")


if __name__ == "__main__":
    run_all()

