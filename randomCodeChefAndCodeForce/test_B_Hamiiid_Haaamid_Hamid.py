import subprocess
import sys
import time

def run_test_case(input_str, expected_output):
    process = subprocess.Popen(
        ["pypy3.10", "B_Hamiiid_Haaamid_Hamid.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input_str)
    actual = stdout.strip()
    if actual == expected_output.strip():
        return True, f"PASSED: output={actual}"
    else:
        return False, f"FAILED: expected=\n{expected_output}\n got=\n{actual}\nstderr=\n{stderr}"

def run_all_tests():
    test_cases = [
        (
            """4\n3 1\n..#\n4 2\n...\n5 3\n##..#\n6 3\n#....#\n""",
            """1\n1\n3\n2"""
        ),
        # Edge cases
        (
            """3\n2 1\n..\n2 2\n..\n3 2\n#.#\n""",
            """1\n1\n2"""
        ),
    ]

    results = []
    start_time = time.time()
    for input_str, expected in test_cases:
        success, message = run_test_case(input_str, expected)
        results.append((success, message))
    end_time = time.time()

    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")

    all_passed = all(success for success, _ in results)
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

# ---- New helper for randomised stress testing ----
def stress_test(max_n=8, num_tests=50, verbose=False):
    import random
    passed = 0
    for _ in range(num_tests):
        n = random.randint(2, max_n)
        x = random.randint(1, n)
        s_list = [random.choice(['.', '#']) for _ in range(n)]
        s_list[x-1] = '.'
        if s_list.count('.') < 2:
            s_list[random.randrange(n)] = '.'
            s_list[random.randrange(n)] = '.'
            s_list[x-1] = '.'
        s = ''.join(s_list)

        inp = f"1\n{n} {x}\n{s}\n"

        # Run reference brute
        proc_ref = subprocess.Popen(
            ["pypy3.10", "brute_B_Hamiiid_Haaamid_Hamid.py"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        out_ref, err_ref = proc_ref.communicate(inp)
        if proc_ref.returncode != 0:
            print("Brute error:", err_ref)
            return
        expected = out_ref.strip()

        # Run solution
        proc_sol = subprocess.Popen(
            ["pypy3.10", "B_Hamiiid_Haaamid_Hamid.py"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        out_sol, err_sol = proc_sol.communicate(inp)
        actual = out_sol.strip()

        if actual != expected:
            print("\nMISMATCH FOUND:\nInput:\n", inp, sep="")
            print("Output:", actual, "\nExpected:", expected)
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed")

if __name__ == "__main__":
    run_all_tests()

