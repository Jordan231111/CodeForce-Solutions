import subprocess
import sys
import time

def greedy_final_len(A, B):
    a = A[:]
    m = len(B)
    while True:
        r = min(len(a), m)
        pos = -1
        for i in range(r - 1, -1, -1):
            if a[i] == B[i]:
                pos = i
                break
        if pos == -1:
            break
        del a[pos]
    return len(a)

def run_test_case(cases):
    t = len(cases)
    parts = [str(t)]
    expected_lines = []
    for n, m, A, B in cases:
        parts.append(f"{n} {m}")
        parts.append(" ".join(map(str, A)))
        parts.append(" ".join(map(str, B)))
        expected_lines.append(str(greedy_final_len(A, B)))
    test_input = "\n".join(parts) + "\n"

    process = subprocess.Popen(
        ["pypy3.10", "solution.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="."
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip().splitlines()
    expected = expected_lines
    ok = actual == expected
    msg = f"cases={t}, expected={' | '.join(expected)}, got={' | '.join(actual)}"
    return ok, msg

def run_all_tests():
    test_cases = [
        (4, 2, [0, 0, 0, 1], [1, 0]),
        (4, 1, [0, 0, 0, 1], [1]),
        (3, 2, [1, 0, 1], [1, 1]),
        (1, 1, [0], [0]),
        (1, 1, [1], [0]),
        (5, 5, [0,0,0,0,0], [0,0,0,0,0]),
        (5, 2, [1,0,0,0,0], [0,1]),
    ]

    results = []
    start_time = time.time()

    success, message = run_test_case(test_cases)
    results.append((success, message))

    end_time = time.time()

    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all(s for s, _ in results) else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()


