import subprocess
import sys
import time
import os

CPP_SOURCE = "berflix.cpp"
BIN_NAME = "berflix"

SAMPLE_INPUT = """20 25
4
1 22 1 30
1 22 50 30
5
3 1 25
2 23 22
4 10 27
1 21 21
3 20 26
"""

SAMPLE_OUTPUT = """3
2
4
4
0
"""


def compile_sources():
    subprocess.run([
        "g++-14", "-std=gnu++20", "-O2", "-pipe", CPP_SOURCE, "-o", BIN_NAME
    ], check=True)


def run_with_input(text: str) -> str:
    proc = subprocess.Popen(
        [f"./{BIN_NAME}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate(text)
    if err:
        sys.stderr.write(err)
    return out


def run_all_tests():
    compile_sources()

    results = []
    start = time.time()

    # Sample test
    out = run_with_input(SAMPLE_INPUT)
    results.append((out.strip() == SAMPLE_OUTPUT.strip(), "Sample"))

    # Edge case 1: n=1, immediate watch after cascade
    edge1 = """5 5
1
10
10
1
1 1 1
"""
    # After update: a=1,d=1 => needs 0 => p=1
    out1 = run_with_input(edge1)
    results.append((out1.strip() == "1", "Edge1"))

    # Edge case 2: no one ever watches
    edge2 = """1000000 1000000
2
1000000 1000000
1000000 1000000
2
1 1000000 1000000
2 1000000 1000000
"""
    out2 = run_with_input(edge2)
    results.append((out2.strip() == "0\n0", "Edge2"))

    end = time.time()

    print("Test Results:")
    all_passed = True
    for ok, name in results:
        print(f"{'\u2713' if ok else '\u2717'} {name}")
        all_passed &= ok
    print(f"\nExecution time: {end - start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")


if __name__ == "__main__":
    run_all_tests()


