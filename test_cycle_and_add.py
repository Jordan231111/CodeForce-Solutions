import subprocess
import time

SAMPLE_INPUT = """4
3 2
3 5 4
1 2 0
3 2
3 4 2
2 1 3
4 11
2 3 2 1
5 4 5 1
4 7
4 3 4 2
5 7 6 3
"""

SAMPLE_OUTPUT = """11
15
33
62
"""


def run_with_input(text: str) -> str:
    proc = subprocess.Popen(
        ["pypy3.10", "cycle_and_add.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate(text)
    return out


def run_all_tests():
    results = []
    start = time.time()

    out = run_with_input(SAMPLE_INPUT)
    results.append((out.strip() == SAMPLE_OUTPUT.strip(), "Sample"))

    edge1 = """1
1 5
10
0
"""
    out1 = run_with_input(edge1)
    results.append((out1.strip() == "0", "Edge n=1, d=0"))

    edge2 = """1
5 1
1000000 1000000 1000000 1000000 1000000
1 2 3 4 5
"""
    out2 = run_with_input(edge2)
    results.append((out2.strip().isdigit(), "Edge large B, increasing D"))

    end = time.time()
    print("Test Results:")
    all_passed = True
    check = "\u2713"
    cross = "\u2717"
    for ok, name in results:
        sym = check if ok else cross
        print(f"{sym} {name}")
        all_passed &= ok
    print(f"\nExecution time: {end - start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")


if __name__ == "__main__":
    run_all_tests()


