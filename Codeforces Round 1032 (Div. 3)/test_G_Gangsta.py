import subprocess

PYTHON = "pypy3.10"
SOLUTION = "g.py"

def run_case(input_str, expected_output):
    proc = subprocess.run([PYTHON, SOLUTION], input=input_str.encode(), capture_output=True, timeout=2)
    output = proc.stdout.decode().strip()
    expected = expected_output.strip()
    return output == expected, output, expected

test_cases = [
    (
        """6\n1\n0\n2\n01\n4\n0110\n6\n110001\n8\n10011100\n11\n01011011100\n""",
        """1\n3\n14\n40\n78\n190""",
    ),
    # All zeros length 4 -> answer equals sum of substring lengths = 20
    ("1\n4\n0000\n", "20"),
    # All ones length 3 -> answer 10
    ("1\n3\n111\n", "10"),
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