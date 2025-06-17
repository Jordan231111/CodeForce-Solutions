#!/usr/bin/env python3
import subprocess

# Test cases: samples and custom edge cases
tests = [
    # Sample from prompt
    ("""7
6 5 2 3
-1 -2 5 4
4 4 2 2
0 0 3 1
10 9 3 2
0 0 4 3
10 9 3 2
0 0 6 3
5 5 2 2
-1 -1 4 -1
5 5 2 2
-1 -1 2 3
7 8 2 4
0 0 0 5
""",
     """Yes
No
No
Yes
No
Yes
No"""),
    # Edge case: a=1, b=1 -> always Yes
    ("""2
10 10 1 1
-5 -5 100 100
1 1 1 1
0 0 0 0
""",
     """Yes
Yes"""),
    # Edge case: one misaligned tile -> No
    ("""1
5 5 2 2
-1 0 2 0
""",
     """No"""),
]

def run_test(input_str, expected):
    # Run with pypy3.10
    result = subprocess.run(
        ['pypy3.10', 'B_Good_Start.py'],
        input=input_str.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode().strip()
    ok = (output == expected.strip())
    print("Input:")
    print(input_str)
    print("Expected:")
    print(expected)
    print("Output:")
    print(output)
    print("Result:", "✓" if ok else "✗")
    print('-' * 40)
    return ok

if __name__ == "__main__":
    all_ok = True
    for inp, exp in tests:
        if not run_test(inp, exp):
            all_ok = False
    if all_ok:
        print("All tests passed!")
    else:
        print("Some tests failed.") 