import subprocess
import sys
import time

def run_test_case(lines, expected):
    test_input = "\n".join(lines) + "\n"
    process = subprocess.Popen(
        ["pypy3.10", "A_Sequence_Queries.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    if actual == expected.strip():
        return True, f"PASSED: output={actual}"
    else:
        return False, f"FAILED: expected=\n{expected}\n---- got ----\n{actual}\nSTDERR=\n{stderr}"

def run_all_tests():
    tests = []
    tests.append(([
        "6",
        "1 0",
        "1 1",
        "1 0",
        "2 2 3",
        "1 2",
        "2 0 5"
    ], "1\n5"))

    tests.append(([
        "2",
        "1 0",
        "2 0 1"
    ], "0"))

    tests.append(([
        "10",
        "1 0",
        "1 1",
        "2 0 2",
        "2 0 2",
        "1 0",
        "1 5",
        "2 0 5",
        "2 2 6",
        "1 6",
        "1 9"
    ], "1\n0\n0\n0"))

    results = []
    start = time.time()
    for lines, expected in tests:
        ok, msg = run_test_case(lines, expected)
        results.append((ok, msg))
    end = time.time()

    print("Test Results:")
    for ok, msg in results:
        print(("\u2713" if ok else "\u2717"), msg)
    all_passed = all(ok for ok, _ in results)
    print(f"\nExecution time: {end - start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

def stress_test(max_q=200, num_tests=200):
    import random
    for _ in range(num_tests):
        Q = random.randint(1, max_q)
        ops = []
        present = [0]
        next_val = 1
        for i in range(Q):
            if random.random() < 0.6 or len(present) == 1:
                x = random.choice(present)
                ops.append(f"1 {x}")
                present.append(next_val)
                next_val += 1
            else:
                if len(present) >= 2:
                    x, y = random.sample(present, 2)
                    ops.append(f"2 {x} {y}")
        test_input = "\n".join([str(Q)] + ops) + "\n"
        p1 = subprocess.Popen(["pypy3.10", "A_Sequence_Queries.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out1, err1 = p1.communicate(test_input)
        p2 = subprocess.Popen(["pypy3.10", "brute_A_Sequence_Queries.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out2, err2 = p2.communicate(test_input)
        if out1.strip() != out2.strip():
            print("\nMISMATCH FOUND:\nInput:\n", test_input, sep="")
            print("Solution:\n", out1, sep="")
            print("Brute:\n", out2, sep="")
            return
    print("\nStress testing completed without mismatches.")

if __name__ == "__main__":
    run_all_tests()
    stress_test()


