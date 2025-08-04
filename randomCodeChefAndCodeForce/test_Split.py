import subprocess
import sys
import time

def run_test_case(inp: str, expected: str):
    process = subprocess.Popen(
        ["python3", "Split.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(inp)
    actual = stdout.strip()
    expected = expected.strip()
    return actual == expected, f"Expected: {expected} | Got: {actual}\nStderr: {stderr}"


def run_all_tests():
    sample_input = """4\n5 2\n10110\n5 1\n10110\n4 4\n0101\n6 2\n001001\n"""
    sample_output = """1\n3\n1\n3\n"""

    success, message = run_test_case(sample_input, sample_output)
    print("Sample Test:", "PASSED" if success else "FAILED")
    if not success:
        print(message)

if __name__ == "__main__":
    run_all_tests()
