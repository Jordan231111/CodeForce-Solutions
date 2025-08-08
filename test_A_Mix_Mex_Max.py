import subprocess
import time
import textwrap

def run_test_case(test_input: str, expected_output: str):
    process = subprocess.Popen(
        ["pypy3.10", "A_Mix_Mex_Max.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    actual = stdout.strip()
    expected = expected_output.strip()
    return actual == expected, f"Input:\n{test_input}\nExpected:\n{expected}\nActual:\n{actual}\nStderr:\n{stderr}"

def run_all_tests():
    test_cases = [
        (
            textwrap.dedent("""\
            2
            3
            -1 -1 -1
            4
            -1 1 -1 1
            """),
            textwrap.dedent("""\
            YES
            YES
            """),
        ),
        (
            textwrap.dedent("""\
            3
            5
            1 1 1 0 1
            5
            1 2 1 1 1
            3
            0 -1 0
            """),
            textwrap.dedent("""\
            NO
            NO
            NO
            """),
        ),
    ]
    start_time = time.time()
    all_passed = True
    for idx, (inp, outp) in enumerate(test_cases, 1):
        passed, message = run_test_case(inp, outp)
        print(f"Test #{idx}: {'✓' if passed else '✗'}")
        if not passed:
            print(message)
            all_passed = False
    end_time = time.time()
    print(f"\nAll tests passed: {all_passed}")
    print(f"Total time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    run_all_tests()

