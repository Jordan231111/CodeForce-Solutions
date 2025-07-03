from add_permutation import solve
import io
import sys

# Save original stdin/stdout
original_stdin = sys.stdin
original_stdout = sys.stdout

# Sample inputs from problem statement
test_input = """5
1 1
2 1
2 2
4 2
6 3
"""

# Expected outputs
expected_output = """1
2 1
1 2
3 4 1 2
6 3 4 5 2 1
"""

# Custom output stream
output_stream = io.StringIO()
sys.stdout = output_stream

# Provide test input
sys.stdin = io.StringIO(test_input)

# Run solution
solve()

# Reset stdin/stdout
sys.stdin = original_stdin
sys.stdout = original_stdout

# Get output
actual_output = output_stream.getvalue()

# Compare with expected output
print("Testing solution with sample inputs:")
print("Result: ", end="")
if actual_output.strip() == expected_output.strip():
    print("PASSED ✓")
else:
    print("FAILED ✗")
    print("\nExpected:")
    print(expected_output)
    print("\nActual:")
    print(actual_output)
    
    # Compare line by line for debugging
    expected_lines = expected_output.strip().split('\n')
    actual_lines = actual_output.strip().split('\n')
    
    for i, (exp, act) in enumerate(zip(expected_lines, actual_lines)):
        if exp != act:
            print(f"Mismatch in test case {i+1}:")
            print(f"Expected: {exp}")
            print(f"Actual: {act}") 