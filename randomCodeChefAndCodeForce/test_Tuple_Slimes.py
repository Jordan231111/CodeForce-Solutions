import subprocess
import sys
import time
import random

SOL = "Tuple_Slimes.py"
BRUTE = "brute_tuple_slimes.py"

sample_input = """3
2
1 2
3 4
3
5 -6
1 2
-1 -3
5
3 8
0 0
-8 7
-7 -2
1 4
"""

sample_output = """6
1
31
"""

def run_prog(file, inp):
    p = subprocess.Popen(["pypy3.10", file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    return p.returncode, out, err

def run_samples():
    code, out, err = run_prog(SOL, sample_input)
    ok = (out.strip() == sample_output.strip())
    return ok, f"Samples {'OK' if ok else 'FAIL'}\nGot:\n{out}\nExpected:\n{sample_output}"


def random_case(n, v=10):
    t = 1
    arr = []
    arr.append(str(t))
    arr.append(str(n))
    for _ in range(n):
        a = random.randint(-v, v)
        b = random.randint(-v, v)
        arr.append(f"{a} {b}")
    return "\n".join(arr) + "\n"


def stress(trials=200):
    for _ in range(trials):
        n = random.randint(1, 8)
        inp = random_case(n, 8)
        _, out1, _ = run_prog(SOL, inp)
        _, out2, _ = run_prog(BRUTE, inp)
        if out1.strip() != out2.strip():
            return False, f"Mismatch!\nInput:\n{inp}\nGot:\n{out1}\nExpected:\n{out2}"
    return True, "Stress OK"


def edge_tests():
    cases = []
    cases.append("1\n2\n0 0\n0 0\n\n")
    cases.append("1\n2\n1000000000 1000000000\n-1000000000 -1000000000\n\n")
    messages = []
    for inp in cases:
        _, out1, _ = run_prog(SOL, inp)
        _, out2, _ = run_prog(BRUTE, inp)
        messages.append((out1.strip() == out2.strip(), f"Edge case -> sol:{out1.strip()} ref:{out2.strip()}"))
    ok = all(x for x,_ in messages)
    text = "\n".join(("✓" if x else "✗") + " " + m for x,m in messages)
    return ok, text


def run_all():
    results = []
    ok1, msg1 = run_samples()
    results.append((ok1, "Samples", msg1))
    ok2, msg2 = edge_tests()
    results.append((ok2, "Edges", msg2))
    ok3, msg3 = stress(150)
    results.append((ok3, "Stress", msg3))
    all_ok = all(x for x,_,_ in results)
    print("Test Results:")
    for ok, name, msg in results:
        print(f"{'✓' if ok else '✗'} {name}: {msg}")
    print(f"Overall: {'PASSED' if all_ok else 'FAILED'}")

if __name__ == "__main__":
    run_all()
