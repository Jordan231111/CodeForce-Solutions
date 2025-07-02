import subprocess
import sys

PYTHON = "pypy3.10"
SOLUTION = "E_Sponsor_of_Your_Problems.py"

def run_case(input_str, expected_output):
    proc = subprocess.run([
        PYTHON, SOLUTION
    ], input=input_str.encode(), capture_output=True, timeout=2)
    output = proc.stdout.decode().strip()
    expected = expected_output.strip()
    return output == expected, output, expected

test_cases = [
    # Cases based on problem note
    ("8\n1 1\n2 3\n4 6\n15 16\n17 19\n199 201\n899 999\n1990 2001\n", "2\n1\n0\n3\n2\n2\n1\n3"),
    # All digits same
    ("1\n1234 1234\n", "8"),
    # Large gap at first digit
    ("1\n100 999\n", "0"),
]

def main():
    print("Test | Result | Output | Expected")
    print("-----|--------|--------|---------")
    for idx, (inp, exp) in enumerate(test_cases):
        ok, out, expected = run_case(inp, exp)
        mark = "✓" if ok else "✗"
        print(f"{idx+1:4} |   {mark}    | {out!r} | {expected!r}")
        if not ok:
            print(f"  Input: {inp!r}")

if __name__ == "__main__":
    main() 