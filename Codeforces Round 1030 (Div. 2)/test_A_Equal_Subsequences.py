import subprocess
import random
import os
import sys
from typing import List

PYTHON = os.environ.get("PYTHON", "pypy3.10")  # default to PyPy 3.10
SOLUTION_FILE = "A_Equal_Subsequences.py"


def count_subseq(bitstr: str, pattern: str) -> int:
    # Count subsequences equal to pattern (len=3)
    p0, p1, p2 = pattern
    n = len(bitstr)
    # dp approach: count prefix occurrences of first two chars
    count_p0 = 0
    count_p0p1 = 0
    res = 0
    for ch in bitstr:
        if ch == p2:  # extend p0p1
            res += count_p0p1
        if ch == p1:  # extend p0
            count_p0p1 += count_p0
        if ch == p0:
            count_p0 += 1
    return res


def run_solution(input_str: str) -> List[str]:
    proc = subprocess.run(
        [PYTHON, SOLUTION_FILE],
        input=input_str.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.decode().strip().split("\n")


def validate_case(n: int, k: int, output: str) -> None:
    assert len(output) == n, f"Length mismatch: expected {n}, got {len(output)}"
    assert output.count("1") == k, f"Count of 1s mismatch: expected {k}, got {output.count('1')}"
    c101 = count_subseq(output, "101")
    c010 = count_subseq(output, "010")
    assert c101 == c010, f"Unequal subsequences: 101={c101}, 010={c010}"


def test_sample() -> None:
    sample_input = """5\n4 2\n5 3\n5 5\n6 2\n1 1\n"""
    expected_cases = [(4, 2), (5, 3), (5, 5), (6, 2), (1, 1)]
    outputs = run_solution(sample_input)
    assert len(outputs) == len(expected_cases)
    for (n, k), out in zip(expected_cases, outputs):
        validate_case(n, k, out)


def test_random_small() -> None:
    trials = 100
    for _ in range(trials):
        n = random.randint(1, 20)
        k = random.randint(0, n)
        input_str = f"1\n{n} {k}\n"
        out = run_solution(input_str)[0]
        validate_case(n, k, out)


if __name__ == "__main__":
    test_sample()
    test_random_small()
    print("All tests passed.") 