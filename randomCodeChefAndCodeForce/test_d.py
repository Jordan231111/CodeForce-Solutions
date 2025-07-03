import subprocess
import sys

def run_test(input_data, expected_output):
    """
    Runs the solution script with the given input and checks the output.
    """
    try:
        # Determine the python executable
        python_executable = 'pypy3.10' if sys.platform != 'win32' else 'python'
        
        p = subprocess.Popen(
            [python_executable, 'd.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = p.communicate(input=input_data)
        
        if p.returncode != 0:
            return "Runtime Error", stderr
            
        actual_output = stdout.strip().splitlines()
        expected_output_lines = expected_output.strip().splitlines()

        if actual_output == expected_output_lines:
            return "Passed", ""
        else:
            return "Failed", f"Expected: {expected_output_lines}, Got: {actual_output}"

    except FileNotFoundError:
        return "Skipped", f"{python_executable} not found. Please ensure it's installed and in your PATH."
    except Exception as e:
        return "Error", str(e)

def main():
    test_cases = [
        {
            "name": "Sample Cases",
            "input": """4
2 1
3 10
1
3 2
10 5 4
11
3 2
10 5 4
10
7 4
100000000 100000000 100000000 100000000 100000000 100000000 100000000
1111""",
            "output": """10
9
15
999999979"""
        },
        {
            "name": "Edge Case: K=N (Impossible)",
            "input": """1
2 2
10 20
01""",
            "output": "0"
        },
        {
            "name": "Edge Case: K=1, N large, sell smallest",
            "input": """1
5 1
10 1 1 1 20
0""",
            "output": "10"
        },
        {
            "name": "Edge Case: K=1, N large, sell largest",
            "input": """1
5 1
10 1 1 1 20
1""",
            "output": "20"
        },
        {
            "name": "Edge Case: All items same cost",
            "input": """1
5 3
7 7 7 7 7
010""",
            "output": "21" # 3 items sold * cost 7
        }
    ]
    
    all_passed = True
    for case in test_cases:
        status, details = run_test(case["input"], case["output"])
        print(f"Test '{case['name']}': {status}")
        if status != "Passed":
            all_passed = False
            if details:
                print(details)
    
    if not all_passed:
        print("\nSome tests failed.")
    else:
        print("\nAll tests passed successfully!")

if __name__ == "__main__":
    main() 