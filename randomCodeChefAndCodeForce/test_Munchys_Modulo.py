import subprocess
import sys
import time


def brute(arr):
    n = len(arr)
    best = 0
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                v = arr[i] % (arr[j] + arr[k])
                if v > best:
                    best = v
    return best


def run_test_case(arr):
    expected = brute(arr)
    t_input = f"1\n{len(arr)}\n{' '.join(map(str, arr))}\n"
    proc = subprocess.Popen(
        ["pypy3.10", "Munchys_Modulo.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate(t_input)
    return out.strip() == str(expected), f"Input: {arr} Expected: {expected} Got: {out.strip()}"


def run_all_tests():
    test_cases = [
        [1, 2, 3],
        [1, 3, 3],
        [5, 5, 5],
        [10, 1, 1],
        [10, 9, 1, 1],
    ]
    results = []
    start = time.time()
    for case in test_cases:
        ok, msg = run_test_case(case)
        results.append((ok, msg))
    end = time.time()
    for ok, msg in results:
        print(f"{'✓' if ok else '✗'} {msg}")
    print(f"Execution time: {end - start:.4f}s")


if __name__ == "__main__":
    run_all_tests() 