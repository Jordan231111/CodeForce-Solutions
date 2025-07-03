import subprocess
import sys
from io import StringIO

def run_test(input_str, expected_output):
    proc = subprocess.run(
        ["pypy3.10", "A_Password_Length.py"],
        input=input_str.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    actual_output = proc.stdout.decode().strip()
    expected_output = expected_output.strip()
    
    print(f"Input:\n{input_str.strip()}")
    print(f"Expected Output: {expected_output}")
    print(f"Actual Output: {actual_output}")
    
    if actual_output == expected_output:
        print("✓ Passed\n")
        return True
    else:
        print("✗ Failed\n")
        return False

# Official test cases
test_cases = [
    # Sample 1
    {
        "input": "chokudai\n5\n",
        "expected": "Yes"
    },
    # Sample 2
    {
        "input": "ac\n3\n",
        "expected": "No"
    },
    # Sample 3
    {
        "input": "atcoder\n7\n",
        "expected": "Yes"
    },
]

# Edge cases
test_cases.extend([
    # Edge case 1: P and L are exactly the same length
    {
        "input": "a\n1\n",
        "expected": "Yes"
    },
    # Edge case 2: P is max length, L is min length
    {
        "input": "a" * 100 + "\n1\n",
        "expected": "Yes"
    },
    # Edge case 3: P is min length, L is max length
    {
        "input": "a\n100\n",
        "expected": "No"
    }
])

results = []
for i, tc in enumerate(test_cases):
    print(f"Test Case {i+1}:")
    results.append(run_test(tc["input"], tc["expected"]))

print("\nSummary:")
print(f"Passed: {results.count(True)}/{len(results)}")
print(f"Failed: {results.count(False)}/{len(results)}")

# Time complexity: O(1)
# Space complexity: O(1)
# The solution simply compares two values, which is a constant-time operation.
# No additional data structures are used that scale with input size. 