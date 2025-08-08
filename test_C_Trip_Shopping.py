import subprocess
import time
import textwrap

SAMPLE_INPUT = textwrap.dedent('''\
5
2 1
1 7
3 5
3 2
1 5 3
6 2 4
5 4
1 16 10 10 16
3 2 2 15 15
4 1
23 1 18 4
19 2 10 3
10 10
4 3 2 100 4 1 2 4 5 5
1 200 4 5 6 1 10 2 3 4
''')

SAMPLE_OUTPUT = textwrap.dedent('''\
8
9
30
16
312
''').strip()


def run(test_input: str):
    proc = subprocess.Popen(
        ["pypy3.10", "C_Trip_Shopping.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate(test_input)
    return out.strip(), err.strip()


def run_all_tests():
    start = time.time()
    out, err = run(SAMPLE_INPUT)
    assert out == SAMPLE_OUTPUT, f"Sample failed: expected {SAMPLE_OUTPUT!r}, got {out!r}\nErrors: {err}"

    # Edge case 1: smallest n with overlap
    edge1_input = """1\n2 2\n5 5\n5 5\n"""
    edge1_expected = "0"
    out, _ = run(edge1_input)
    assert out == edge1_expected, f"Edge1 failed, got {out}"

    # Edge case 2: no overlap, multiple identical rounds
    edge2_input = """1\n3 3\n1 10 20\n5 30 40\n"""
    # intervals: (1,5),(10,30),(20,40) -> base=34, min_gap between 5 and 10 is5 -> ans=34+10=44
    edge2_expected = "44"
    out, _ = run(edge2_input)
    assert out == edge2_expected, f"Edge2 failed, got {out}"

    end = time.time()
    print("All tests passed in", end - start, "seconds")


if __name__ == "__main__":
    run_all_tests()

