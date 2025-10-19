import sys
from io import StringIO
import subprocess
import shutil

PY = "pypy3.10" if shutil.which("pypy3.10") else sys.executable
SOL = "gcnd.py"


def run_case(inp: str) -> str:
    p = subprocess.Popen([PY, SOL], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    if p.returncode != 0:
        raise RuntimeError(err)
    return out.strip()


def test_gcnd_function():
    # simple direct checks via solution behavior with single pair per test
    # 1 test case, n=2, values: 8 5 -> 7
    assert run_case("1\n2\n8 5\n") == "7"
    # 6 6 -> 5
    assert run_case("1\n2\n6 6\n") == "5"
    # 8 8 -> 7
    assert run_case("1\n2\n8 8\n") == "7"
    # 9 8 -> 7
    assert run_case("1\n2\n9 8\n") == "7"
    print("✓ All gcnd function tests passed!")


def test_sample_input():
    """Test with the complete sample input from the problem"""
    sample_input = """3
2
8 5
3
6 6 6
4
8 9 8 8"""
    
    expected_output = """7
5
7"""
    out = run_case(sample_input)
    if out == expected_output.strip():
        print("✓ Sample input test passed!")
    else:
        print("✗ Sample input test failed!")
        print(f"Expected:\n{expected_output.strip()}")
        print(f"Got:\n{out}")


def test_edge_cases():
    # identical and small
    assert run_case("1\n2\n5 5\n") == "4"
    # different small
    assert run_case("1\n2\n5 7\n") == "6"
    print("✓ Edge case tests passed!")


def brute_gcnd_pair(x, y):
    m = max(x, y)
    for z in range(m, 0, -1):
        if x % z and y % z:
            return z
    return 1


def brute_solve_once(arr):
    n = len(arr)
    ans = 0
    for i in range(n):
        for j in range(i+1, n):
            v = brute_gcnd_pair(arr[i], arr[j])
            if v > ans:
                ans = v
    return ans


def stress_random(num_tests=200):
    import random
    for _ in range(num_tests):
        n = random.randint(2, 8)
        arr = [random.randint(1, 50) for _ in range(n)]
        tin = "1\n" + str(n) + "\n" + " ".join(map(str, arr)) + "\n"
        out = run_case(tin)
        expected = str(brute_solve_once(arr))
        assert out == expected, f"Mismatch: arr={arr}, got={out}, expected={expected}"
    print("✓ Stress tests passed!")


if __name__ == "__main__":
    test_gcnd_function()
    test_sample_input()
    test_edge_cases()
    stress_random()
    print("\n✓ All tests passed!")

