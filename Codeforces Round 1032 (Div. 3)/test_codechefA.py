import subprocess

def run_test(input_data):
    """Helper function to run the solution against a given input."""
    try:
        process = subprocess.run(
            ['pypy3.10', 'codechefA.py'],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        return process.stdout.strip()
    except FileNotFoundError:
        print("pypy3.10 not found. Please ensure it's in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def test_samples():
    """Tests the solution against the provided sample cases."""
    print("Running Sample Tests...")
    sample_input = "4\n2\n3\n4\n5\n"
    expected_output = "1\n3\n1\n1"
    
    output = run_test(sample_input)
    if output is not None:
        assert output == expected_output, f"Expected '{expected_output}', got '{output}'"
        print("✓ Sample 1 passed")
    print("-" * 20)

def test_edge_cases():
    """Tests the solution against various edge cases."""
    print("Running Edge Cases...")
    
    test_cases = {
        "X=1 (Smallest Input)": ("1\n1\n", "1"),
        "X=100 (Largest Input)": ("1\n100\n", "1"),
        "X=6 (Reduces to 3)": ("1\n6\n", "3"),
        "X=9 (Reduces to 3)": ("1\n9\n", "3"),
    }
    
    for name, (input_data, expected) in test_cases.items():
        output = run_test(input_data)
        if output is not None:
            assert output == expected, f"Test '{name}' failed: Expected '{expected}', got '{output}'"
            print(f"✓ Edge Case {name} passed")
    print("-" * 20)

def test_full_range():
    """Generates expected results for all X from 1 to 100 and verifies."""
    from collections import deque
    print("Running Full Range Test (1 to 100)...")
    
    inputs = ["100"] + [str(i) for i in range(1, 101)]
    expected = []

    for i in range(1, 101):
        q = deque([i])
        visited = {i}
        found_one = False
        while q:
            curr = q.popleft()
            if curr > 3:
                next_val = curr - 3
                if next_val == 1:
                    found_one = True
                    break
                if next_val > 0 and next_val not in visited:
                    visited.add(next_val)
                    q.append(next_val)
            if curr % 2 == 0:
                next_val = curr // 2
                if next_val == 1:
                    found_one = True
                    break
                if next_val > 0 and next_val not in visited:
                    visited.add(next_val)
                    q.append(next_val)
        
        if found_one:
            expected.append("1")
        else:
            expected.append(str(min(visited)))
    
    input_data = "\n".join(inputs) + "\n"
    expected_data = "\n".join(expected)
    
    output = run_test(input_data)
    if output is not None:
        assert output == expected_data, "Full range test failed!"
        print("✓ Full Range Test (1-100) passed")
    print("-" * 20)


if __name__ == "__main__":
    test_samples()
    test_edge_cases()
    test_full_range()
    print("All tests passed!") 