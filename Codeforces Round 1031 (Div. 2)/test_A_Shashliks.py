import subprocess
import sys

PYTHON = "pypy3.10"
SOLUTION = "A_Shashliks.py"

def run_case(input_str, expected_output):
    proc = subprocess.run([
        PYTHON, SOLUTION
    ], input=input_str.encode(), capture_output=True, timeout=2)
    output = proc.stdout.decode().strip()
    expected = expected_output.strip()
    return output == expected, output, expected

test_cases = [
    # Official samples
    ("5\n10 3 4 2 1\n1 10 10 1 1\n100 17 5 2 3\n28 14 5 2 4\n277 5 14 1 3\n", "8\n0\n46\n10\n273"),
    # Custom edge: minimal values (corrected expected output)
    ("1\n1 1 1 1 1\n", "1"),
    # Custom edge: large k, minimal thresholds
    ("1\n1000000000 1 1 1 1\n", str(1000000000)),
    # Custom edge: k < both thresholds
    ("1\n1 2 2 1 1\n", "0"),
    # Custom edge: k == a == b, x != y
    ("1\n5 5 5 2 3\n", "1"),
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