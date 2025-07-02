import subprocess
import tempfile
import os

def test_solution():
    solution_code = '''def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    operations = []
    
    def is_valid():
        for i in range(n-1):
            if a[i] >= a[i+1] or b[i] >= b[i+1]:
                return False
        for i in range(n):
            if a[i] >= b[i]:
                return False
        return True
    
    if is_valid():
        print(0)
        return
    
    changed = True
    while changed:
        changed = False
        
        for i in range(n-1):
            if a[i] > a[i+1]:
                operations.append((1, i + 1))
                a[i], a[i+1] = a[i+1], a[i]
                changed = True
        
        for i in range(n-1):
            if b[i] > b[i+1]:
                operations.append((2, i + 1))
                b[i], b[i+1] = b[i+1], b[i]
                changed = True
        
        for i in range(n):
            if a[i] >= b[i]:
                operations.append((3, i + 1))
                a[i], b[i] = b[i], a[i]
                changed = True
    
    print(len(operations))
    for op in operations:
        print(op[0], op[1])

t = int(input())
for _ in range(t):
    solve()
'''

    test_input = '''6
1
1
2
1
2
1
2
1 3
4 2
2
1 4
3 2
3
6 5 4
3 2 1
3
5 3 4
2 6 1
'''

    def run_test(input_str):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(solution_code)
            temp_file = f.name
        
        try:
            result = subprocess.run(['python3', temp_file], 
                                  input=input_str, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.stdout.strip(), result.stderr.strip()
        finally:
            os.unlink(temp_file)

    def validate_solution(n, original_a, original_b, operations):
        a = original_a[:]
        b = original_b[:]
        
        for op in operations:
            if op[0] == 1:
                i = op[1] - 1
                if 0 <= i < n-1:
                    a[i], a[i+1] = a[i+1], a[i]
            elif op[0] == 2:
                i = op[1] - 1
                if 0 <= i < n-1:
                    b[i], b[i+1] = b[i+1], b[i]
            elif op[0] == 3:
                i = op[1] - 1
                if 0 <= i < n:
                    a[i], b[i] = b[i], a[i]
        
        for i in range(n-1):
            if a[i] >= a[i+1] or b[i] >= b[i+1]:
                return False
        
        for i in range(n):
            if a[i] >= b[i]:
                return False
        
        return True

    stdout, stderr = run_test(test_input)
    
    if stderr:
        print(f"❌ Runtime error: {stderr}")
        return False
    
    lines = stdout.split('\n')
    
    test_cases = [
        (1, [1], [2]),
        (1, [2], [1]),
        (2, [1, 3], [4, 2]),
        (2, [1, 4], [3, 2]),
        (3, [6, 5, 4], [3, 2, 1]),
        (3, [5, 3, 4], [2, 6, 1])
    ]
    
    expected_operations = [0, 1, 1, 1, 9, 6]
    
    line_idx = 0
    results = []
    
    for i, (n, a, b) in enumerate(test_cases):
        k = int(lines[line_idx])
        line_idx += 1
        
        operations = []
        for _ in range(k):
            if line_idx < len(lines):
                parts = lines[line_idx].split()
                operations.append((int(parts[0]), int(parts[1])))
                line_idx += 1
        
        is_valid = validate_solution(n, a, b, operations)
        is_within_limit = k <= 1709
        expected_k = expected_operations[i]
        
        status = "✓" if is_valid and is_within_limit else "✗"
        close_to_expected = abs(k - expected_k) <= 2
        
        results.append((i+1, k, expected_k, is_valid, is_within_limit, close_to_expected, status))
        
        print(f"Test {i+1}: {status} ({k} operations, expected ~{expected_k}, valid={is_valid}, ≤1709={is_within_limit})")
    
    all_passed = all(r[6] == "✓" for r in results)
    print(f"\nOverall: {'✓ All tests passed' if all_passed else '✗ Some tests failed'}")
    
    return all_passed

if __name__ == "__main__":
    test_solution()