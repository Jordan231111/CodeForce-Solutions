import subprocess
import sys

def run_test():
    # The solution script to test
    solution_file = "H_Ice_Baby.py"
    
    # The interpreter to use
    interpreter = "pypy3.10"

    # Sample input from the problem description
    sample_input = """6
1
1 1
2
3 4
1 2
4
4 5
3 4
1 3
3 3
8
6 8
4 6
3 5
5 5
3 4
1 3
2 4
3 3
5
1 2
6 8
4 5
2 3
3 3
11
35 120
66 229
41 266
98 164
55 153
125 174
139 237
30 72
196 212
109 123
174 196
"""

    # Expected output from the problem description
    expected_output = """1
1 1
1 2 2 3
1 2 2 3 3 3 4 5
1 2 2 2 3
1 2 3 4 5 6 7 7 8 8 9
"""

    try:
        # Run the solution script as a subprocess
        process = subprocess.run(
            [interpreter, solution_file],
            input=sample_input,
            capture_output=True,
            text=True,
            check=True,
            timeout=10 # 10-second timeout for safety
        )
        
        # Normalize whitespace and compare outputs
        actual_output = process.stdout.strip()
        normalized_expected = '\n'.join(line.strip() for line in expected_output.strip().split('\n'))
        
        print("--- Test Protocol: Sample Case ---")
        print(f"Interpreter: {interpreter}")
        print(f"Solution: {solution_file}")
        
        if actual_output == normalized_expected:
            print("\n[✓] Sample Case Passed")
            print("\nExpected Output:")
            print(normalized_expected)
            print("\nActual Output:")
            print(actual_output)
        else:
            print("\n[✗] Sample Case Failed")
            print("\nExpected Output:")
            print(normalized_expected)
            print("\nActual Output:")
            print(actual_output)
            print("\nStderr:")
            print(process.stderr)
            
    except FileNotFoundError:
        print(f"[✗] Error: The interpreter '{interpreter}' or the solution file '{solution_file}' was not found.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[✗] Error: The solution script exited with a non-zero status code: {e.returncode}")
        print("Stderr:")
        print(e.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"[✗] Error: The solution script timed out.")
        sys.exit(1)

if __name__ == "__main__":
    run_test() 