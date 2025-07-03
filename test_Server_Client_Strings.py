import os
import subprocess
import sys
from io import StringIO

# Test cases
test_cases = [
    # Sample 1
    {
        "input": """2 6
2 1 at
3 1
2 2 on
1 2
2 2 coder
3 2""",
        "expected": "atcoder"
    },
    # Sample 2
    {
        "input": """100000 3
1 100
2 300 abc
3 200""",
        "expected": ""
    },
    # Sample 3
    {
        "input": """10 10
2 7 ladxf
2 7 zz
2 7 kfm
3 7
1 5
2 5 irur
3 5
1 6
2 6 ptilun
3 6""",
        "expected": "ladxfzzkfmirurptilun"
    },
    # Edge case: no operations on server
    {
        "input": """3 3
2 1 test
2 2 example
2 3 case""",
        "expected": ""
    },
    # Edge case: replace PC with empty server
    {
        "input": """3 4
2 1 test
1 2
2 2 example
3 2""",
        "expected": "example"
    }
]

def run_test(input_data):
    # Save original stdin/stdout
    old_stdin, old_stdout = sys.stdin, sys.stdout
    
    # Redirect stdin/stdout
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()
    
    try:
        # Run solution
        exec(open("Server_Client_Strings.py").read())
        return sys.stdout.getvalue().strip()
    finally:
        # Restore stdin/stdout
        sys.stdin, sys.stdout = old_stdin, old_stdout

# Run tests
all_passed = True
for i, test in enumerate(test_cases):
    result = run_test(test["input"])
    expected = test["expected"]
    
    if result == expected:
        print(f"Test {i+1}: PASSED")
    else:
        print(f"Test {i+1}: FAILED")
        print(f"Input:\n{test['input']}")
        print(f"Expected: '{expected}'")
        print(f"Got: '{result}'")
        all_passed = False

if all_passed:
    print("All tests passed!")
    
    # Run solution with pypy3.10
    try:
        print("\nRunning with pypy3.10...")
        subprocess.run(["pypy3.10", "Server_Client_Strings.py"], 
                       input=test_cases[0]["input"].encode(), 
                       check=True, 
                       timeout=2)
        print("Successfully ran with pypy3.10")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"Error running with pypy3.10: {e}")
else:
    print("Some tests failed. Fix your solution before submitting.") 