import subprocess
import sys

# Test cases: (input, expected_output)
test_cases = [
    ("""12\n1 1\n1\n1 2\n1\n2 1\n2 2\n2 3\n2 2\n1 3\n2 3\n1 2\n3 1\n1 2 3\n3 2\n1 3 4\n3 3\n1 2 3\n4 3\n1 2 3 10\n5 5\n1 2 3 6 7\n6 6\n1 2 3 9 10 11\n""", ["0","1","1","2","3","2","2","4","2","11","8","15"]),
    # Custom edge case: all positions same as s
    ("""1\n1 5\n5\n""", ["0"]),
    # Custom edge case: s outside the range
    ("""1\n2 10\n1 2\n""", ["9"]),
]

def run_test(input_str):
    proc = subprocess.run([
        "pypy3.10", "a.py"
    ], input=input_str, capture_output=True, text=True)
    return proc.stdout.strip().split("\n")

def main():
    all_passed = True
    print("Test Results for A. Letter Home:")
    print("Case | Result | Output | Expected")
    print("-----|--------|--------|---------")
    for idx, (inp, expected) in enumerate(test_cases):
        output = run_test(inp)
        ok = output == expected
        all_passed &= ok
        mark = "✓" if ok else "✗"
        print(f"{idx+1:>4} |   {mark}    | {output} | {expected}")
    if all_passed:
        print("\nAll tests passed.")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    main() 